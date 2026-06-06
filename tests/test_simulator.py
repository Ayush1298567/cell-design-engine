"""Simulator tests. These run the DFN, so they are slower than the unit tests.

They check structure, physical sanity, and one direction the physics must obey
(more porosity -> better rate capability).
"""

from celltool import simulator


def test_evaluate_runs_and_is_sane():
    m = simulator.evaluate_design({"cathode.thickness_um": 65, "cathode.porosity": 0.35}, spec_c_rate=3.0)
    assert m.ok
    assert 0.0 < m.rate_capability < 1.0   # always lose some capacity at high rate
    assert m.temp_rise_C > 0.0             # discharge generates heat
    assert m.cap_ref_Ah > 0.0


def test_more_porosity_improves_rate():
    low = simulator.evaluate_design({"cathode.thickness_um": 65, "cathode.porosity": 0.25}, spec_c_rate=3.0)
    high = simulator.evaluate_design({"cathode.thickness_um": 65, "cathode.porosity": 0.45}, spec_c_rate=3.0)
    assert high.rate_capability > low.rate_capability
