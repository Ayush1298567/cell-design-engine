"""Quote-grade cell calculator (the tier-1, trustworthy layer).

Pure bookkeeping over known material properties and geometry: capacity, energy,
mass, volume, and the densities that follow. No physics prediction, so it lands
within a percent or two of a built cell. This is the same algebra BatPaC and the
ISEA database use to reproduce real commercial cells.

Modelling convention (see configs/cell.yaml): a coating's matrix_density is the
solid density excluding pores, so coating mass per area = thickness * (1-porosity)
* matrix_density. Coatings are double-sided; the stack is `num_layers` repeating
units of [Al | cathode x2 | separator | anode x2 | Cu | separator].
"""

from dataclasses import dataclass

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


def _areal_capacity_mAh_cm2(electrode):
    """Reversible areal capacity of one coated side [mAh/cm^2]."""
    t_cm = electrode["thickness_um"] * UM_TO_CM
    coating_mass_per_area = t_cm * (1 - electrode["porosity"]) * electrode["matrix_density_g_cm3"]
    active_mass_per_area = coating_mass_per_area * electrode["active_fraction"]
    return active_mass_per_area * electrode["specific_capacity_mAh_g"]


def compute(cell):
    g = cell["geometry"]
    area_cm2 = (g["electrode_width_mm"] * MM_TO_CM) * (g["electrode_height_mm"] * MM_TO_CM)
    layers = g["num_layers"]
    sides = 2  # double-sided coating

    cath = cell["cathode"]
    anode = cell["anode"]
    sep = cell["separator"]
    cc = cell["current_collectors"]

    # Capacity: cathode-limited (anode carries excess, N/P > 1).
    areal_cath = _areal_capacity_mAh_cm2(cath)
    areal_anode = _areal_capacity_mAh_cm2(anode)
    np_ratio = areal_anode / areal_cath
    capacity_mAh = areal_cath * area_cm2 * sides * layers
    capacity_Ah = capacity_mAh / 1000.0

    energy_Wh = capacity_Ah * cell["cell"]["nominal_voltage_V"]

    # Masses [g].
    def coating_mass(e):
        t_cm = e["thickness_um"] * UM_TO_CM
        return t_cm * (1 - e["porosity"]) * e["matrix_density_g_cm3"] * area_cm2 * sides * layers

    mass_cathode = coating_mass(cath)
    mass_anode = coating_mass(anode)
    mass_al = (cc["cathode_Al_thickness_um"] * UM_TO_CM) * cc["cathode_Al_density_g_cm3"] * area_cm2 * layers
    mass_cu = (cc["anode_Cu_thickness_um"] * UM_TO_CM) * cc["anode_Cu_density_g_cm3"] * area_cm2 * layers
    mass_sep = (sep["thickness_um"] * UM_TO_CM) * sep["matrix_density_g_cm3"] * (1 - sep["porosity"]) * area_cm2 * sides * layers

    # Electrolyte fills the pore volume of both coatings and the separator.
    def pore_volume(e, n_sheets):
        return (e["thickness_um"] * UM_TO_CM) * e["porosity"] * area_cm2 * n_sheets

    pore_total = (
        pore_volume(cath, sides * layers)
        + pore_volume(anode, sides * layers)
        + pore_volume(sep, sides * layers)
    )
    mass_electrolyte = pore_total * cell["electrolyte"]["density_g_cm3"]

    mass_g = (
        mass_cathode + mass_anode + mass_al + mass_cu + mass_sep
        + mass_electrolyte + cell["cell"]["packaging_mass_g"]
    )

    # Volume [cm^3]: stack height * area + packaging.
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
    )
