"""Calculator tests.

Two kinds: *_arithmetic tests pin independently hand-computed values (they verify
the algebra, not the physics); the external-reference and sanity tests pin the
demo cell to the real LG M50 / Chen2020 cell so a physically wrong number cannot
pass (CLAUDE.md rules 6, 7).
"""

import math

from celltool import calculator, config

CELL = config.load_config("configs/cell.yaml")


def test_cathode_areal_capacity_arithmetic():
    # 75um -> 0.0075 cm; (1-0.30) solid; 4.6 g/cm3 matrix; 0.95 active; 195 mAh/g
    # = 0.0075 * 0.70 * 4.6 * 0.95 * 195 = 4.47379 mAh/cm^2
    m = calculator.compute(CELL)
    assert math.isclose(m.areal_capacity_cathode_mAh_cm2, 4.47379, rel_tol=1e-4)


def test_capacity_arithmetic():
    # 4.47379 * 100 cm^2 * 2 sides * 30 layers / 1000 = 26.843 Ah (cathode-limited)
    m = calculator.compute(CELL)
    assert math.isclose(m.capacity_Ah, 26.843, rel_tol=1e-3)


def test_np_ratio_arithmetic_and_safe():
    m = calculator.compute(CELL)
    assert math.isclose(m.np_ratio, 1.0945, rel_tol=1e-3)
    assert m.np_ratio > 1.0  # anode carries excess (safety)


def test_energy_consistent():
    m = calculator.compute(CELL)
    assert math.isclose(m.energy_Wh, m.capacity_Ah * CELL["cell"]["nominal_voltage_V"], rel_tol=1e-9)


def test_external_reference_physical():
    # Pin to the real LG M50 / Chen2020 cell, NOT to the config (rule 6).
    # Real single-side cathode areal capacity is ~4.3-4.9 mAh/cm^2; a healthy
    # NMC811/graphite cell is ~640-750 Wh/L and ~250-310 Wh/kg.
    m = calculator.compute(CELL)
    assert 4.3 < m.areal_capacity_cathode_mAh_cm2 < 4.9
    assert 640 < m.energy_density_Wh_L < 750
    assert 250 < m.specific_energy_Wh_kg < 310


def test_mass_conservation():
    # The aggregate must equal the sum of its parts (catches a dropped term).
    m = calculator.compute(CELL)
    assert math.isclose(sum(m.mass_breakdown_g.values()), m.mass_g, rel_tol=1e-9)
    # one component hand-pinned independently:
    # cathode coating = 0.0075 * 0.70 * 4.6 * 100 cm^2 * 2 * 30 = 144.9 g
    assert math.isclose(m.mass_breakdown_g["cathode_coating"], 144.9, rel_tol=1e-4)


def test_anode_limited_clamp():
    # Push the cathode past the anode: cell becomes anode-limited and capacity
    # plateaus. Guards the min(cathode, anode) clamp specifically.
    thick = calculator.compute(config.with_overrides(CELL, {"cathode.thickness_um": 110}))
    # anode (88um) areal = 4.8965 mAh/cm^2 -> 4.8965*100*2*30/1000 = 29.379 Ah
    assert math.isclose(thick.capacity_Ah, 29.379, rel_tol=1e-3)
    assert thick.np_ratio < 1.0
    # pushing the cathode even thicker changes nothing (true plateau)
    thicker = calculator.compute(config.with_overrides(CELL, {"cathode.thickness_um": 200}))
    assert math.isclose(thicker.capacity_Ah, thick.capacity_Ah, rel_tol=1e-9)


def test_cathode_limited_thickening():
    # Inside the cathode-limited band (N/P > 1), capacity scales with cathode.
    base = calculator.compute(config.with_overrides(CELL, {"cathode.thickness_um": 65}))
    more = calculator.compute(config.with_overrides(CELL, {"cathode.thickness_um": 75}))
    assert base.np_ratio > 1.0 and more.np_ratio > 1.0
    assert more.capacity_Ah > base.capacity_Ah


def test_realize_design_holds_np_across_search_box():
    # Co-balancing keeps N/P at the target as the cathode varies (resolves the
    # design-vars-vs-envelope contradiction the review found).
    for thk in (50, 65, 80):
        for por in (0.25, 0.35, 0.45):
            cell = calculator.realize_design(CELL, {"cathode.thickness_um": thk, "cathode.porosity": por})
            m = calculator.compute(cell)
            assert math.isclose(m.np_ratio, CELL["cell"]["target_np_ratio"], rel_tol=1e-6)
