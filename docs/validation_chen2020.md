# DFN validation against Chen2020 experimental data

First validation of the PyBaMM DFN model against real LG M50 discharge data
(Zenodo 4032561), at four C-rates, isothermal 25 C, literature parameters
(uncalibrated). Reproduce with `python scripts/validate_chen2020.py`.

## Setup

- Model: Doyle-Fuller-Newman, PyBaMM 26.6.0
- Parameters: `Chen2020` (literature, not fitted to these specific cells)
- Mesh: 32 points/domain (converged to 2.6 mV vs finest, see `convergence_dfn.py`)
- Initial state: 100% SOC, discharge to 2.5 V cutoff
- Reference: cell02, discharges at C/10, C/2, 1C, 1.5C
- Thermal: isothermal at 25 C (no thermal coupling yet)

## Results

| Rate | Capacity error | IR (start-V) error | Bias | Scatter |
|------|---------------:|-------------------:|-----:|--------:|
| C/10 | +2.7% | +7 mV | +40 mV | 15 mV |
| C/2  | +2.9% | +2 mV | +39 mV | 16 mV |
| 1C   | +1.3% | +28 mV | +44 mV | 17 mV |
| 1.5C | -0.3% | +71 mV | +38 mV | 18 mV |

The shape error (voltage on normalized depth-of-discharge, knee excluded) is
split into **bias** (mean signed offset) and **scatter** (std about the mean).

## What this says

1. **The physics shape is sound.** After removing the systematic offset, the
   model tracks the real discharge curve to 15-18 mV scatter across every rate.
   That matches the literature's best-fit figure (~18 mV) and is design-guidance
   grade.

2. **The dominant error is a ~40 mV systematic bias**, nearly constant across all
   rates. A constant bias is a reference/OCV offset, which is exactly what
   calibration to a cell's own data removes. This is the uncalibrated-parameter
   penalty, and it is the single most calibratable error in the table.

3. **Capacity is within ~3% uncalibrated**, shrinking at higher rate.

4. **The IR error grows with rate** (7 -> 71 mV from C/10 to 1.5C). This is the
   known high-rate weakness, and it points to thermal coupling as the next
   improvement: at 1.5C the real cell self-heats, lowering its resistance, which
   the isothermal model cannot capture.

## Trust tier

This is **directional / tier 3** (uncalibrated literature parameters). It says
PyBaMM's DFN machinery is sound and that the physics shape is right; it is not a
claim about IBC cells. The result is the evidence for the core thesis: the
underlying model is good, and calibration on a manufacturer's own data is what
converts directional into design-guidance.

## Next

- Add lumped thermal model, re-run, expect the high-rate IR/end-of-discharge
  error to drop.
- Calibrate (PyBOP) against cell02 and check whether the +40 mV bias collapses.
- Extend to cells 03/04 for cell-to-cell spread, and build the validation matrix
  across C-rate x temperature.
