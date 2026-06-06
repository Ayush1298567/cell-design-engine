# PROJECT_HISTORY.md — how we got here

Last updated: June 5, 2026. A record of the internship, the idea's evolution,
the key decisions and why they were made, and where things stand. Pairs with
THE_IDEA.md (the full concept). Anything dated here may have moved on by the
time you read it; treat it as a snapshot.

## People

- **Sasi Kuppannagari** — COO of IBC, owns the internship, approved the
  project, scoped Phase 1. sasi@ibcbatt.com, 503-349-9313.
- **Santi Adavani** — IBC, made the original outreach, now advisory.
  santi@ibcbatt.com.
- **Rohan Prasad** — co-intern and collaborator on the project.
  rohan.pr1671@gmail.com.
- **Kunal** — IBC contact identified by Santi as the person who can explain
  IBC's internal design process and tooling. Intro to be set up via Sasi
  (not yet requested).
- **Ramesh** — Santi's colleague who originally referred Ayush.
- **Bonnie** — earlier pending intro via Sasi, status unclear.

## Timeline

**March 2026.** Santi reaches out (referred by Ramesh) pitching an internship
at the intersection of physics and AI. Resume sent same day. Intro call Mar
26. Ayush shares MIT BWSI CubeSat flight software repos Mar 27.

**April-May.** Follow-ups while Santi works out logistics. May 11: Ayush
sends three concrete contribution areas (Nyaya AI defect triage automation,
test data automation, internal tooling/dashboards) and offers to build a POC
before starting. May 13: Santi hands off to Sasi.

**May 21.** 1-1 call with Sasi: Battery Nexus, June 15 start date, IBC's
custom-cell-per-use-case business. That evening Ayush emails Sasi: asks about
remote work, proposes teaming with Rohan, and pitches the cell design
optimization tool (PyBaMM + Bayesian optimization).

**May 22.** Sasi calls the concept very compelling, asks for a writeup of use
case, simulation scope, physics models, expected outcomes. Offers a review
call and weekly check-ins.

**May 25-28.** Proposal PDF sent (the "Cell Design Optimization Tool" doc,
earlier working name "Aether Labs"). Ayush directly asks whether it would
actually be useful to IBC. Follow-up nudge May 28.

**May 29.** Sasi replies: loves the depth and overall solution. Scopes the
first deliverable to implementing and validating PyBaMM's DFN model, with
both Ayush and Rohan on it; the rest of the proposal comes after. Proposes a
June 10 review meeting.

**May 30 - June 1.** Ayush confirms the DFN focus, asks to move the meeting
(out of state on the 10th). Sasi, traveling in Seoul, sets **June 8, 11am
PT, online (Google Meet)**. Invite sent and accepted. Kickoff is locked.

**June 1-2 (Santi thread).** Santi reviews the proposal: idea looks good, and
he flags the two gating questions from the proposal's own "what we need from
IBC" list: how IBC actually goes from customer request to cell design, and
what tools/formats their engineers use. After a brief miscommunication he
clarifies that **Kunal** is the right person for those questions and Sasi can
facilitate. He also points to Anthropic's Agent Skills for the agent design.
Ayush commits to asking Sasi for time with Kunal (not yet done). Thread
closed warmly.

**June 3-5 (working sessions in this project).** Deep design work, see the
decision log below: the technical flowchart PDF, the honest evaluation, the
DoE integration, the research pass on IBC and the industry, and the full
reframe into the Custom Cell Design Engine (THE_IDEA.md, and the reframed
PDF with figures).

## How the idea evolved (decision log, with reasons)

1. **LLM as orchestrator, not scientist.** Every working system in this
   space (Coscientist, ChemCrow, ChatBattery, MARS) uses the LLM to
   coordinate specialized tools, not to do the science. Shaped the whole
   architecture from the start.
2. **Bayesian optimization over RL.** RL needs thousands of training
   episodes; BO works from run one. Right for a cold-start POC.
3. **PyBaMM as the engine.** Chosen after comparing COMSOL, LIONSIMBA,
   DandeLiion, BattMo. PyBOP adds the optimization/fitting layer on top.
4. **One best design, not three designs.** The parallel approaches
   (energy-first, power-first, balanced) are different starting points
   converging on the single best design meeting all constraints.
5. **Search bounds are optimizer ranges, not defaults.** The optimum can
   land anywhere inside them; they exist to exclude the unmanufacturable.
6. **Staged scoping (Sasi's call, May 29).** Validate the DFN physics
   foundation before building the optimizer and agent layers on top.
   Deliberate risk reduction.
7. **No fixed round cap (June 4).** Replaced the "converged when <2% change
   or 8 rounds" rule. The analysis agent now judges after each batch
   whether top designs are still meaningfully improving; code computes the
   raw numbers, the agent makes the call; runs continue while progress is
   real and stop on plateau. Reason: no reason to stop a search that is
   still finding better cells; an arbitrary cap throws away gains.
8. **DoE integrated (June 5).** Three insertion points: sensitivity
   screening before optimization, the validation matrix as a small
   factorial, and (the big one) the build plan: proposing the 3-6 prototypes
   that jointly teach the most when built, instead of five near-clones of
   the winner. Sparked by a DoE explainer video; BO is adaptive DoE, and DoE
   is the right tool where experiments are expensive (the pilot line).
9. **Platform-bounded search (June 5, from research).** IBC sells three
   Prabal platforms plus custom tailoring; customers get matched and
   tailored, not blank-sheet designs. The tool now searches within IBC's
   platform families and manufacturing envelope. Smaller space, real data,
   credible outputs.
10. **Value prop corrected (June 5).** Killed "accurate like a lab" framing
    (unattainable and trust-destroying). The tool competes with the
    engineer's first guess, not with the lab. Value = fewer build-test
    loops, faster quotes, fewer senior-engineer hours. Value equation:
    RFQs/year x cost per loop x loops removed.
11. **Trust tiers (June 5).** Every output labeled with the confidence of
    the layer that produced it: quote-grade (calculator algebra),
    design-guidance (calibrated DFN), directional (literature-parameter DFN
    and all degradation), ground truth (pilot line). Core product principle.
12. **Honest bottleneck boundary (June 5, from research).** IBC's likely
    production bottleneck is yield at scale-up (Nyaya's existence, "copy
    exact" factory transfer, yield-focused funding language). The tool does
    not fix yield; it helps the front end and frees pilot-line slots. We say
    this out loud.

## Research findings (June 5 session)

- **IBC**: founded 2022, ~$64M raised, Series A June 2025. Products: Prabal
  1000/2000/3000 prismatic platforms + cylindrical line + packs. 50 MWh
  Korea pilot (cells currently shipped to India), Rs 390 crore Gigafactory
  in Karnataka, "copy exact" strategy, ~1000 two-wheeler packs deployed in
  2025, order book ~Rs 200M. Founder publicly calls device technology /
  manufacturability the hardest part.
- **Industry process**: heritage design -> spreadsheet cell calculation
  (accurate, it is algebra) -> tuning by rules of thumb -> A/B/C sample
  maturity loop on pilot lines. The build-test loop is the cost center.
- **Market**: Ionworks (PyBaMM founders, YC) and About:Energy sell
  simulation-as-a-service and parameterization; category is real and paid.
  Nobody ships the autonomous requirements-to-design loop embedded inside
  one manufacturer. The moat is the in-house calibration flywheel.
- **DFN limits (literature)**: ~30 parameters, identifiability problems
  (good fits with non-unique parameters), parameters non-transferable
  between cells, error grows above ~1C and at high temperature near end of
  discharge (RMSE up to ~84 mV in failure zones; ~18 mV median when well
  fitted), degradation predictions directional. Cure: rich fitting data
  (rate sweeps, GITT, EIS) and mapping the model's own error by region.

## Artifacts produced so far

- **Proposal PDF** (May 25, sent to Sasi): the original Cell Design
  Optimization Tool writeup. Treat as superseded by THE_IDEA.md on framing,
  still the document Sasi approved.
- **Cell_Design_Tool_Technical_Flow.pdf** (June 4): full technical
  flowchart + per-component explanations; updated to the no-round-cap
  progress check.
- **Custom_Cell_Design_Engine_Reframed.pdf** (June 5): the reframed concept
  with business case, three figures, 15-step walkthrough, technical
  foundations, IBC fit.
- **THE_IDEA.md** (June 5): the complete explanatory concept document.
- **CLAUDE.md / CONTEXT.md** (June 5): repo-ready briefs, currently on hold
  per Ayush (no Phase 1 build yet).

## Current open items

- Ask Sasi for time with **Kunal** (committed to Santi June 2, not sent).
  The three sizing questions for that meeting: custom RFQs per year;
  iterations and cost per build-test loop; current process, tools, and
  output format. Plus: "what actually limits you right now: yield,
  throughput, design turnaround, or test capacity?"
- **June 8, 11am PT, Google Meet**: kickoff with Sasi on simulation
  approach, model assumptions, inputs/outputs, cell parameters, validation
  methodology. Goal: walk in with our assumptions and a proposed success
  metric, leave with his guidance and ideally the Kunal intro + check-in
  cadence.
- Remote work question: asked May 21, still unanswered.
- CIA (confidentiality agreement): mentioned May 21, not yet received.
- Weekly check-ins: offered by Sasi May 22, not yet scheduled.
- Internship start: June 15.

## Working preferences (Ayush)

Casual, direct writing; no AI-sounding language, no em dashes. Emails should
read like two interns wrote them. Plain language over jargon; visuals for
technical explanations. Iterates on framing across passes; researches prior
art before committing; consistently asks "would this actually be useful"
rather than "does this sound impressive." Treats project docs as dated
snapshots, not current truth.
