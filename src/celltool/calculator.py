"""Quote-grade cell calculator (the tier-1, trustworthy layer).

Pure bookkeeping over known material properties and geometry: capacity, energy,
mass, volume, and the densities that follow. No physics prediction, so capacity,
mass and volume land within a percent or two of a built cell. (Energy uses a flat
nominal voltage as a deliberate first-order choice; load-dependent voltage
depression is the DFN tier's job, so energy is less tight than capacity at rate.)

Modelling convention (see configs/cell.yaml): a coating's matrix_density is the
TRUE solid composite density excluding pores, so coating mass per area =
thickness * (1 - porosity) * matrix_density. Coatings are double-sided; the stack
is `num_layers` repeating units of [Al | cathode x2 | separator | anode x2 | Cu |
separator].
"""

import copy
from dataclasses import dataclass, field

from . import config

UM_TO_CM = 1e-4
MM_TO_CM = 0.1


@dataclass
class CellMetrics:
    capacity_Ah: float
    energy_Wh: float
    mass_g: float
    volume_cm3: float
    specific_energy_Wh_kg: float
    energy_density_Wh_L: float
    np_ratio: float
    areal_capacity_cathode_mAh_cm2: float
    stack_thickness_mm: float
    mass_breakdown_g: dict = field(default_factory=dict)


def _coating_mass_per_area_g_cm2(e):
    """Solid coating mass per coated-side area [g/cm^2], pores excluded."""
    return (e["thickness_um"] * UM_TO_CM) * (1 - e["porosity"]) * e["matrix_density_g_cm3"]


def _areal_capacity_mAh_cm2(electrode):
    """Reversible areal capacity of one coated side [mAh/cm^2]."""
    active_mass_per_area = _coating_mass_per_area_g_cm2(electrode) * electrode["active_fraction"]
    return active_mass_per_area * electrode["specific_capacity_mAh_g"]


def balance_anode(cell):
    """Co-size the anode thickness to hold cell.target_np_ratio against the cathode.

    N/P (anode areal capacity / cathode areal capacity) is a safety/lifetime
    choice, so it must be controlled, not left to drift when the cathode changes.
    """
    out = copy.deepcopy(cell)
    target_np = cell["cell"]["target_np_ratio"]
    areal_cath = _areal_capacity_mAh_cm2(cell["cathode"])
    areal_anode = _areal_capacity_mAh_cm2(cell["anode"])
    # areal capacity is linear in thickness, so scale thickness to hit the target
    out["anode"]["thickness_um"] = cell["anode"]["thickness_um"] * (target_np * areal_cath / areal_anode)
    return out


def realize_design(base_cell, overrides):
    """Apply design overrides, then co-balance the anode. The single design
    pipeline both the calculator and the simulator consume, so they always
    describe the same cell."""
    return balance_anode(config.with_overrides(base_cell, overrides))


def compute(cell):
    g = cell["geometry"]
    area_cm2 = (g["electrode_width_mm"] * MM_TO_CM) * (g["electrode_height_mm"] * MM_TO_CM)
    layers = g["num_layers"]
    sides = 2  # double-sided coating

    cath = cell["cathode"]
    anode = cell["anode"]
    sep = cell["separator"]
    cc = cell["current_collectors"]

    # Capacity is set by the limiting electrode. With N/P > 1 the cathode limits
    # (the intended design); if the cathode is pushed past the anode it becomes
    # anode-limited and capacity plateaus.
    areal_cath = _areal_capacity_mAh_cm2(cath)
    areal_anode = _areal_capacity_mAh_cm2(anode)
    np_ratio = areal_anode / areal_cath
    capacity_Ah = min(areal_cath, areal_anode) * area_cm2 * sides * layers / 1000.0

    # Energy uses nominal voltage (first-order, rate-blind); see module docstring.
    energy_Wh = capacity_Ah * cell["cell"]["nominal_voltage_V"]

    # Mass breakdown [g].
    mass = {
        "cathode_coating": _coating_mass_per_area_g_cm2(cath) * area_cm2 * sides * layers,
        "anode_coating": _coating_mass_per_area_g_cm2(anode) * area_cm2 * sides * layers,
        "separator": _coating_mass_per_area_g_cm2(sep) * area_cm2 * sides * layers,
        "Al_collector": (cc["cathode_Al_thickness_um"] * UM_TO_CM) * cc["cathode_Al_density_g_cm3"] * area_cm2 * layers,
        "Cu_collector": (cc["anode_Cu_thickness_um"] * UM_TO_CM) * cc["anode_Cu_density_g_cm3"] * area_cm2 * layers,
    }
    # Electrolyte fills the pore volume of both coatings and the separator.
    pore_volume = sum(
        (e["thickness_um"] * UM_TO_CM) * e["porosity"] * area_cm2 * sides * layers
        for e in (cath, anode, sep)
    )
    mass["electrolyte"] = pore_volume * cell["electrolyte"]["density_g_cm3"]
    mass["packaging"] = cell["cell"]["packaging_mass_g"]
    mass_g = sum(mass.values())

    # Volume [cm^3]: stack height * area + flat packaging overhead.
    unit_thickness_cm = (
        sides * cath["thickness_um"] * UM_TO_CM
        + sides * anode["thickness_um"] * UM_TO_CM
        + cc["cathode_Al_thickness_um"] * UM_TO_CM
        + cc["anode_Cu_thickness_um"] * UM_TO_CM
        + sides * sep["thickness_um"] * UM_TO_CM
    )
    stack_thickness_cm = unit_thickness_cm * layers
    volume_cm3 = stack_thickness_cm * area_cm2 + cell["cell"]["packaging_volume_cm3"]

    return CellMetrics(
        capacity_Ah=capacity_Ah,
        energy_Wh=energy_Wh,
        mass_g=mass_g,
        volume_cm3=volume_cm3,
        specific_energy_Wh_kg=energy_Wh / (mass_g / 1000.0),
        energy_density_Wh_L=energy_Wh / (volume_cm3 / 1000.0),
        np_ratio=np_ratio,
        areal_capacity_cathode_mAh_cm2=areal_cath,
        stack_thickness_mm=stack_thickness_cm / MM_TO_CM,
        mass_breakdown_g=mass,
    )
