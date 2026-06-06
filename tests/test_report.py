"""Report tests: the distinct-design selection (fast, synthetic)."""

from celltool import objective, report


def _ev(thk, por, score, feasible=True):
    return ({"cathode.thickness_um": thk, "cathode.porosity": por},
            objective.ObjResult(score=score, feasible=feasible))


def test_distinct_designs_dedupes_near_clones():
    evals = [
        _ev(80, 0.346, 271), _ev(80, 0.347, 270.9), _ev(80, 0.348, 270.8),  # clones
        _ev(65, 0.30, 268), _ev(55, 0.28, 255),                              # distinct
    ]
    out = report.distinct_designs(evals, k=5)
    thicks = sorted({round(o["cathode.thickness_um"]) for o, _ in out})
    assert thicks == [55, 65, 80]  # one per distinct region, clones collapsed


def test_distinct_designs_skips_infeasible():
    evals = [_ev(80, 0.30, 300, feasible=False), _ev(65, 0.35, 260, feasible=True)]
    out = report.distinct_designs(evals, k=5)
    assert len(out) == 1
    assert out[0][0]["cathode.thickness_um"] == 65
