"""Calculator tests: hand-checked algebra plus physical-sanity bounds.

The hand-computed values are independent arithmetic, not values copied from the
code (CLAUDE.md rule 7).
"""

import math

from celltool import calculator, config

CELL = config.load_config("configs/cell.yaml")


def test_cathode_areal_capacity_hand_checked():
    # 75um -> 0.0075 cm; (1-0.30) solid; 3.4 g/cm3 matrix; 0.95 active; 195 mAh/g
    # = 0.0075 * 0.70 * 3.4 * 0.95 * 195 = 3.30671 mAh/cm^2
    m = calculator.compute(CELL)
    assert math.isclose(m.areal_capacity_cathode_mAh_cm2, 3.30671, rel_tol=1e-4)


def test_np_ratio_safe():
    m = calculator.compute(CELL)
    # anode areal / cathode areal, sized for ~1.1
    assert math.isclose(m.np_ratio, 1.112, rel_tol=1e-2)
    assert m.np_ratio > 1.0  # anode must carry excess (safety)


def test_capacity_hand_checked():
    # 3.30671 mAh/cm^2 * 100 cm^2 * 2 sides * 30 layers / 1000 = 19.840 Ah
    m = calculator.compute(CELL)
    assert math.isclose(m.capacity_Ah, 19.840, rel_tol=1e-3)


def test_energy_consistent():
    m = calculator.compute(CELL)
    assert math.isclose(m.energy_Wh, m.capacity_Ah * CELL["cell"]["nominal_voltage_V"], rel_tol=1e-9)


def test_physical_sanity_ranges():
    m = calculator.compute(CELL)
    assert 150 < m.specific_energy_Wh_kg < 350  # high-energy NMC range
    assert 300 < m.energy_density_Wh_L < 800
    assert m.mass_g > 0 and m.volume_cm3 > 0


def test_thicker_cathode_more_capacity_but_lower_np():
    base = calculator.compute(CELL)
    thicker = calculator.compute(config.with_overrides(CELL, {"cathode.thickness_um": 90}))
    assert thicker.capacity_Ah > base.capacity_Ah   # more active material
    assert thicker.np_ratio < base.np_ratio         # cathode caught up to anode
