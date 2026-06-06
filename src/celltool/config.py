"""Config loading and design-override helpers.

Everything in the engine is config-driven so IBC values plug in later by editing
YAML, not code. A "design" is a flat dict of dotted paths -> values
(e.g. {"cathode.thickness_um": 80, "cathode.porosity": 0.35}) that the optimizer
varies; with_overrides applies it onto a base cell config.
"""

import copy

import yaml


def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)


def with_overrides(cell, overrides):
    """Return a deep copy of `cell` with dotted-path overrides applied.

    Every segment is validated, so a typo anywhere in the path (not just the leaf)
    fails with the same readable message rather than a raw KeyError/TypeError.
    """
    out = copy.deepcopy(cell)
    for dotted, value in overrides.items():
        node = out
        keys = dotted.split(".")
        for k in keys[:-1]:
            if not isinstance(node, dict) or k not in node:
                raise KeyError(f"override path '{dotted}' not found in cell config")
            node = node[k]
        if not isinstance(node, dict) or keys[-1] not in node:
            raise KeyError(f"override path '{dotted}' not found in cell config")
        node[keys[-1]] = value
    return out
