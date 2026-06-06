# CLAUDE.md — Custom Cell Design Engine

Project-specific rules for this repo. Ayush's global `~/.claude/CLAUDE.md` (working
style, voice, quality bar) loads automatically on top of this; this file only adds
what is specific to this project. When Ayush says "check rule N," it means a
numbered rule below.

## What this is

Custom Cell Design Engine for IBC: requirements in, ranked buildable cell designs
plus a DoE build plan out. Full concept in `docs/THE_IDEA.md`. Internship history,
people, and the decision log in `docs/PROJECT_HISTORY.md`. Read both before any
non-trivial design decision.

## Hard rules

1. **Scope gate: DFN validation only.** The sanctioned scope is implementing and
   validating PyBaMM's DFN model. Do not build the optimizer, agent layer,
   calculator, or knowledge base until that scope is explicitly expanded. If a
   task seems to require them, stop and flag it.

2. **Build bottom-up, never ahead.** Order: calculator -> validated DFN ->
   calibration loop -> optimizer -> agent layer. Each layer works and is
   independently valuable before the next starts. No scaffolding for layers we
   are not on.

3. **Every step ends with proof, not claims.** A step is done when there is an
   artifact Ayush can see: a rendered plot, a passing pytest run, a printed error
   table, a measured timing number. "Looks done" is not done. Show the output.

4. **Two human-owned files.** The `cell.yaml` schema and `ASSUMPTIONS.md` are
   authored by Ayush. I may propose a strawman for him to react to, but I never
   finalize them, and Ayush signs off every field. The schema is the IBC handoff
   interface; ASSUMPTIONS.md is what Sasi reviews. Both must sound like Ayush and
   he must be able to explain every part to a battery engineer.

5. **Trust-tier every number.** Label each output with the confidence of the layer
   that produced it: quote-grade (calculator algebra), design-guidance (calibrated
   DFN), directional (uncalibrated DFN and all degradation), ground truth (pilot
   line). Never present a directional number as if it were quote-grade.

6. **Validation has two bars, do not blur them.** Bar one (now): reproduce
   known-good published results for a known cell (e.g. Chen2020 against PyBaMM's
   reference output). Bar two (later, data-gated): match IBC's actual cells. The
   evidence is always an overlay plot plus an RMSE in millivolts, never "it
   matches."

7. **Never hardcode a value to make a test pass.** If a test fails, the code or
   the assumption is wrong. Fix the cause or flag it. A green test sitting on a
   hardcoded number is worse than a red one, because it hides the problem.

8. **Explain as you build, but do not gate on technical approval.** For
   structural choices (schema, validation harness), explain the design and the
   reasoning in chat as it is built, so Ayush understands the system he will
   present. Per rule 11, technical and implementation structure is my call;
   only high-level forks wait for Ayush.

9. **Tutor as you go.** When using a PyBaMM/PyBOP API or a technique Ayush may not
   know, explain in chat what it does and why it was chosen. Building the tool and
   building Ayush's expertise are the same task.

10. **Commit after every verified step.** Small commits, tight messages, so a bad
    experiment rolls back cleanly instead of being untangled.

11. **Most effective route, not the easiest, and own the technical calls.**
    Default to the highest-leverage approach even when it costs more effort.
    Never pick a weaker method because it is quicker. Make all technical and
    implementation decisions autonomously and explain the reasoning in chat
    (rule 9). Bring only high-level decisions to Ayush: scope, strategy, and
    anything that changes what the deliverable is or what we tell IBC. When
    unsure whether a decision is high-level, lean toward deciding it and noting
    the call rather than asking.

## If the same error hits three times

Stop. Do not attempt a fourth fix. Explain the error and the current assumption in
plain language so the wrong assumption gets found together, not patched over.

## Stack

Python. PyBaMM (DFN simulation), PyBOP (Bayesian optimization + parameter fitting),
NumPy, Matplotlib, PyYAML, pytest. Pin versions; record the environment so results
reproduce.
