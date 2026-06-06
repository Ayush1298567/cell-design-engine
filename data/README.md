# Validation data

Experimental discharge data for the LG M50 cell, used to validate the DFN model.
The raw CSVs are not committed (run `python data/download_data.py` to fetch and
verify them by MD5).

## Source

Chang-Hui Chen, Ferran Brosa Planella, Kieran O'Regan, Dominika Gastol,
W. Dhammika Widanage, Emma Kendrick. *Development of Experimental Techniques for
Parameterization of Multi-scale Lithium-ion Battery Models.* Journal of The
Electrochemical Society, 167(8):080534, 2020.
https://doi.org/10.1149/1945-7111/ab9050

Dataset: https://zenodo.org/records/4032561 (CC BY 4.0)

## Files

Three LG M50 cells (cell02, cell03, cell04). Each is a Maccor cycler export:
13 metadata rows, then a table with these columns.

| Column | Meaning |
|--------|---------|
| `Step` | Procedure step number (identifies rest / charge / discharge phase) |
| `Step Time [s]` | Seconds since the current step started |
| `Capacity [Ah]` | Cycler-accumulated charge throughput |
| `Current [A]` | Positive on discharge in this export |
| `Voltage [V]` | Terminal voltage |
| `Md` | Mode: `R` rest, `C` charge, `D` discharge, `O` other |
| `Temperature Cell [degC]` | Cell surface temperature |
| `Temperature Chamber [degC]` | Thermal chamber temperature |

## Characterization discharges (from full charge)

Each is a CC discharge to a 2.5 V cutoff after a CC-CV charge to 4.2 V and a rest.
Nominal capacity is 5 Ah.

| Step | Current | C-rate |
|------|---------|--------|
| 7 | 0.5 A | C/10 |
| 12 | 2.5 A | C/2 |
| 17 | 5.0 A | 1C |
| 22 | 7.5 A | 1.5C |

(Step 2 is a 0.5 A preconditioning discharge, not from full charge; excluded.)
