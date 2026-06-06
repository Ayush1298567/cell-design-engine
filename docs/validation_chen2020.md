# DFN validation against Chen2020 experimental data

Validation of the PyBaMM DFN against real LG M50 discharge data (Zenodo 4032561),
four C-rates, isothermal 25 C, literature parameters (uncalibrated). Reproduce
with `python scripts/validate_chen2020.py`.

## Setup

- Model: Doyle-Fuller-Newman, PyBaMM 26.6.0
- Parameters: `Chen2020` (literature, not fitted to these cells)
- Mesh: 32 points/domain (within 2.6 mV of the 48-pt mesh; estimated absolute
  discretisation error ~3.7 mV, far below the physics error budget)
- Initial state: 100% SOC, discharge to 2.5 V
- Reference: cell02, discharges at C/10, C/2, 1C, 1.5C
- Thermal: isothermal at 25 C (no thermal coupling)

## Results

| Rate | Cap err | Start-V err | Scatter (DoD) | Scatter (raw) | Cell T mean / rise |
|------|--------:|------------:|--------------:|--------------:|-------------------:|
| C/10 | +2.7% | +7 mV | 15 mV | **32 mV** | 27 C / +2 C |
| C/2  | +2.9% | +2 mV | 16 mV | **31 mV** | 31 C / +8 C |
| 1C   | +1.3% | +28 mV | 17 mV | **19 mV** | 38 C / +17 C |
| 1.5C | -0.3% | +71 mV | 18 mV | **19 mV** | 46 C / +28 C |

- **Scatter (DoD)**: std of the voltage residual after normalising each curve to
  its own capacity (this forces the endpoints to coincide, so it *removes* the
  capacity error from the residual) and removing the mean bias.
- **Scatter (raw)**: the same residual on the native capacity axis, with the
  capacity offset kept in. This is the honest uncalibrated-model number.
- **Start-V err**: v_sim[0] - v_exp[0]. NOT a clean IR/resistance: it carries the
  OCV/SOC reference offset and is single-sample noisy (the non-monotonic 7->2->28
  ->71 sequence is the tell). Do not read it as ohmic resistance.
- **Cell T**: the experiment self-heats; at 1C/1.5C it runs 17-28 C above the
  chamber, so the isothermal-25 C comparison is thermally confounded at those rates.

## What this says

1. **The DFN shape is in the right ballpark, strongest at low rate.** On the
   honest raw-capacity axis the residual is ~31 mV at C/10-C/2 and ~19 mV at the
   higher rates. The DoD-normalised ~15-18 mV is smaller because it removes the
   ~3% capacity offset; both are reported above so the choice is visible. This is
   *directional* evidence that the physics shape is reasonable. It is **not** a
   fitted-model comparison, so it should not be equated with the literature's
   best-fit (~18 mV), which is a *calibrated* number.

2. **The dominant error is a ~40 mV near-constant offset (hypothesis: largely
   calibratable).** The mean bias is ~38-44 mV across rates. It is consistent
   with an OCV/reference plus SOC-alignment mismatch (the model pins SOC=1 to the
   4.2 V cutoff OCV, while the cell's relaxed full-charge OCV is ~4.185 V), and it
   is not flat within a discharge (small near full charge, ~+60 mV mid-plateau).
   Whether it collapses under calibration is the test the planned PyBOP fit will
   settle; until then "calibratable" is a hypothesis, not a result.

3. **Capacity is within ~3% uncalibrated**, shrinking at higher rate.

4. **High-rate comparison is temperature-confounded.** At 1C/1.5C the real cell
   self-heats 17-28 C above the chamber while the model is isothermal at 25 C, so
   the high-rate residual mixes shape error with an uncontrolled temperature
   delta. The growing start-V error (to +71 mV) is consistent with this. Adding
   the thermal model is the fix before those rates are quoted.

## Trust tier

**Directional / tier 3** (uncalibrated literature parameters). This establishes
that PyBaMM's DFN machinery is sound and the physics shape is reasonable. It is
not design-guidance grade and makes no claim about IBC cells; calibration on a
manufacturer's own data is what would convert directional into design-guidance.

## Next

- Add the lumped thermal model, feed the measured chamber temperature, and re-run
  1C/1.5C before those numbers are shown externally.
- Calibrate (PyBOP) against cell02 and test whether the ~40 mV bias collapses.
- Extend to cells 03/04 (cell-to-cell spread) and build the C-rate x temperature
  validation matrix.
