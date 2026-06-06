"""Config tests: override safety and cell/platform consistency."""

import pytest

from celltool import calculator, config

CELL = config.load_config("configs/cell.yaml")
PLATFORM = config.load_config("configs/platform.yaml")


def test_with_overrides_changes_value_without_mutating_input():
    before = CELL["cathode"]["thickness_um"]
    out = config.with_overrides(CELL, {"cathode.thickness_um": 999})
    assert out["cathode"]["thickness_um"] == 999
    assert CELL["cathode"]["thickness_um"] == before  # input untouched


def test_with_overrides_bad_paths_raise_clear_error():
    for bad in ("bogus.thickness_um", "cathode.bogus", "cathode.thickness_um.deeper"):
        with pytest.raises(KeyError, match="not found in cell config"):
            config.with_overrides(CELL, {bad: 1})


def test_demo_cell_inside_manufacturing_envelope():
    env = PLATFORM["manufacturing_envelope"]
    m = calculator.compute(CELL)
    assert env["np_ratio"]["min"] <= m.np_ratio <= env["np_ratio"]["max"]
    assert env["cathode.thickness_um"]["min"] <= CELL["cathode"]["thickness_um"] <= env["cathode.thickness_um"]["max"]
    assert env["cathode.porosity"]["min"] <= CELL["cathode"]["porosity"] <= env["cathode.porosity"]["max"]


def test_search_box_is_subset_of_envelope():
    # The optimizer's search range must sit inside the hard manufacturing envelope.
    dv = PLATFORM["design_variables"]
    env = PLATFORM["manufacturing_envelope"]
    for key in ("cathode.thickness_um", "cathode.porosity"):
        assert dv[key]["min"] >= env[key]["min"]
        assert dv[key]["max"] <= env[key]["max"]
