"""Report tests: distinct-design selection (fast, synthetic) + grid/file correctness."""

import math

from celltool import calculator, config, objective, optimizer, report

CELL = config.load_config("configs/cell.yaml")
PLATFORM = config.load_config("configs/platform.yaml")
RFQ = config.load_config("configs/rfq.yaml")


def _ev(thk, por, score, feasible=True):
    # scores are arbitrary ranking inputs, NOT calculator outputs (no oracle here)
    return ({"cathode.thickness_um": thk, "cathode.porosity": por},
            objective.ObjResult(score=score, feasible=feasible))


def test_distinct_designs_dedupes_near_clones():
    evals = [
        _ev(80, 0.346, 300), _ev(80, 0.347, 299), _ev(80, 0.348, 298),  # clones
        _ev(65, 0.30, 290), _ev(55, 0.28, 280),                          # distinct
    ]
    out = report.distinct_designs(evals, k=5)
    thicks = sorted({round(o["cathode.thickness_um"]) for o, _ in out})
    assert thicks == [55, 65, 80]


def test_distinct_designs_skips_infeasible():
    evals = [_ev(80, 0.30, 300, feasible=False), _ev(65, 0.35, 260, feasible=True)]
    out = report.distinct_designs(evals, k=5)
    assert len(out) == 1
    assert out[0][0]["cathode.thickness_um"] == 65


def test_evaluate_grid_shape_and_values():
    # tiny 2x2 grid; lock axis orientation and that cells match the calculator
    grid = report.evaluate_grid(CELL, PLATFORM, RFQ, n_thk=2, n_por=2)
    assert grid["specific_energy"].shape == (2, 2)  # (n_por, n_thk)
    for i, por in enumerate(grid["pors"]):
        for j, thk in enumerate(grid["thks"]):
            cell = calculator.realize_design(CELL, {"cathode.thickness_um": float(thk), "cathode.porosity": float(por)})
            expected = calculator.compute(cell).specific_energy_Wh_kg
            assert math.isclose(grid["specific_energy"][i, j], expected, rel_tol=1e-9)


def test_inf_temp_renders_as_limit_not_inf(tmp_path):
    from celltool import agents
    # all-infeasible history whose top design died before the thermal checkpoint (temp=inf)
    ov = {"cathode.thickness_um": 92, "cathode.porosity": 0.30}
    res = objective.ObjResult(score=-1e6 - 100, feasible=False, metrics={
        "specific_energy_Wh_kg": 260, "capacity_Ah": 22.0, "energy_density_Wh_L": 620,
        "rate_capability": 0.55, "temp_rise_C": float("inf"), "sim_ok": True})
    optr = optimizer.OptResult(ov, res, [(ov, res)], [(ov, res)], 0)

    summary = agents.report_summary(optr, RFQ)
    assert ">limit" in summary and "inf C" not in summary

    class _Run:
        spec = RFQ
        strategy = {"n_calls": 1, "rationale": "t"}
        opt = optr
    out = tmp_path / "r.md"
    report.write_report(_Run(), summary, "design_space.png", str(out))
    text = out.read_text()
    assert ">limit" in text
    assert "| inf |" not in text


def test_write_report_creates_file(tmp_path):
    res = optimizer.optimize(CELL, PLATFORM, RFQ, n_calls=8, n_initial=4, seed=0)

    class _Run:
        spec = RFQ
        strategy = {"n_calls": 8, "rationale": "test"}
        opt = res
    out = tmp_path / "report.md"
    report.write_report(_Run(), "summary line", "design_space.png", str(out))
    text = out.read_text()
    assert out.exists()
    assert "Ranked designs" in text or "NO FEASIBLE DESIGN FOUND" in text
