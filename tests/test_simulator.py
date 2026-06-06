"""Simulator tests. These run the DFN, so they are slower than the unit tests.

They cover the relative-metric contract, the physics directions the model must
obey, the porosity->active-fraction coupling, the unit scale, and the failure
path.
"""

from celltool import config, simulator

CELL = config.load_config("configs/cell.yaml")


def _design(thk, por):
    from celltool import calculator
    return calculator.realize_design(CELL, {"cathode.thickness_um": thk, "cathode.porosity": por})


def test_evaluate_runs_and_is_sane():
    m = simulator.evaluate_design(_design(65, 0.35), spec_c_rate=3.0)
    assert m.ok
    assert 0.0 < m.rate_capability < 1.0   # always lose some capacity at high rate
    assert 0.0 < m.temp_rise_C < 100.0     # heats, but not a runaway artifact
    assert 2.5 < m.mean_voltage_V < 4.2


def test_more_porosity_improves_rate():
    low = simulator.evaluate_design(_design(65, 0.25), spec_c_rate=3.0)
    high = simulator.evaluate_design(_design(65, 0.45), spec_c_rate=3.0)
    assert high.rate_capability > low.rate_capability


def test_thicker_cathode_not_better_rate():
    # With the anode co-balanced, a thicker cathode cannot improve rate capability
    # (longer transport path, higher areal current). Guards the anode-limiting
    # artifact the review found.
    thin = simulator.evaluate_design(_design(55, 0.35), spec_c_rate=3.0)
    thick = simulator.evaluate_design(_design(80, 0.35), spec_c_rate=3.0)
    assert thick.rate_capability <= thin.rate_capability + 1e-6


def test_porosity_active_fraction_coupling():
    # Overriding porosity must move the active-material volume fraction so the
    # electrode composition stays physical (porosity + active <= 1).
    p = simulator._base_params(_design(65, 0.45))
    por = p["Positive electrode porosity"]
    act = p["Positive electrode active material volume fraction"]
    assert abs(por - 0.45) < 1e-9
    assert por + act <= 1.0 + 1e-9


def test_thickness_unit_scale():
    p = simulator._base_params(_design(65, 0.30))
    assert abs(p["Positive electrode thickness [m]"] - 65e-6) < 1e-12


def test_failure_path_returns_ok_false_without_raising():
    m = simulator.evaluate_design(_design(65, 0.001), spec_c_rate=3.0)
    assert m.ok is False
    assert m.temp_rise_C == float("inf")
