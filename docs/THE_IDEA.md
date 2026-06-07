# THE IDEA — Custom Cell Design Engine, explained completely

Last updated: June 5, 2026. Ayush G & Rohan Prasad, for International Battery
Company (IBC). This document explains the idea in full: the problem, the
business logic, every component, the technical foundations, the honest
limitations, and the open questions. It is written so that someone with no
battery background can follow it, and so that a battery engineer reading it
finds nothing oversold.

The whole idea in one sentence: IBC sells custom cells, and every custom cell
starts with an expensive guess. This tool makes the first guess better and
cheaper.

---

## 1. The problem: how a custom cell gets designed today

A battery cell is a manufactured object with dozens of design choices baked
into it: which chemistry, how thick each electrode is coated, how porous the
electrodes are after pressing, what particle sizes the materials have, what
electrolyte goes in, how many layers get stacked, what the can dimensions
are. Change any of these and the cell's energy, power, heat behavior, weight,
cost, and lifetime all shift, usually in coupled and competing ways. Thicker
electrodes store more energy but deliver power worse and run hotter. Higher
porosity moves ions faster but wastes volume. Everything trades against
everything.

When a customer comes to a cell maker like IBC with an application (a drone
that needs 45 minute flights, 80 amps at takeoff, desert heat, 500 cycles,
recharge under 30 minutes, inside a fixed volume and weight), someone has to
turn that into a specific cell design. Here is how that actually happens in
industry today, step by step:

**Step one: start from a heritage design.** Nobody derives a cell from
physics on a blank sheet. An experienced engineer pulls up the closest cell
the company has already built and tested, because that design is known to be
manufacturable and its real behavior is known. The new design will be an
adjustment of it.

**Step two: spreadsheet-level cell calculation.** The first quantitative pass
is essentially arithmetic. Given materials, coating loadings, thicknesses,
densities, and can geometry, you can compute capacity, stored energy, mass,
volume, and layer counts with simple algebra. This step is highly accurate
(within a percent or two of the built cell) because it is bookkeeping over
known material properties, not physics prediction. Most cell companies have
some version of this as a spreadsheet; academic and government versions
(BatPaC, the ISEA cell database) reproduce real commercial cells closely.

**Step three: electrode tuning.** Now the judgment calls: exact thicknesses,
porosities, the balance between the two electrodes. This is where experience
and rules of thumb carry the load, and where the more sophisticated teams add
physics simulation to predict rate capability and heating before committing
to a build.

**Step four: build prototypes.** The design gets coated, pressed, stacked,
filled, and formed into real A-sample cells on the pilot line. This takes
weeks, consumes engineering hours, and occupies a slot on equipment the
company needs for everything else it does.

**Step five: test.** The prototypes get cycled, rate-tested, and
temperature-tested for weeks to months.

**Step six: iterate.** If the prototypes miss the spec, go back to step
three, redesign, rebuild, retest. Repeat until the cell passes, then advance
through the B-sample and C-sample maturity gates with the customer and into
production.

The loop between steps three and six is the expensive part of the whole
business of custom cells. Every extra pass costs weeks of calendar time,
engineer attention, and pilot-line capacity. Every claim about this tool's
value reduces to one question: does it cut the number of passes through that
loop?

---

## 2. Who IBC is and why this is their problem

IBC designs and manufactures lithium-ion cells, with R&D in San Jose, a 50
MWh pilot plant in Korea, and a Gigafactory ramping in India (built as a
"copy exact" replica of the Korean line, which is what you do when you want
to move a working process without breaking its yield). Their customers are
niche and spec-driven: drones, humanoids and robotics, ATVs, defense, eVTOL,
space, grid and datacenter storage. These are exactly the buyers who show up
with unusual requirements that off-the-shelf cells do not meet, which is why
IBC explicitly sells custom cell design as a service alongside its standard
products.

The standard products matter to this idea. IBC's line is built around three
prismatic platforms:

- **Prabal 1000**: mid-nickel cathode with graphite, 50 Ah, over 210 Wh/kg,
  over 5000 cycles. The long-life workhorse for industrials, ATVs, robotics.
- **Prabal 2000**: LFP chemistry, 40-45 Ah, over 160 Wh/kg, over 10,000
  cycles. Built for stationary storage where lifetime is everything.
- **Prabal 3000**: high-nickel cathode with a silicon anode, 70 Ah, over 300
  Wh/kg, over 1000 cycles. The energy-density play for aviation, drones,
  defense, space.

Plus a cylindrical line and module/pack products. The consequence for this
tool: a customer almost never gets a blank-sheet cell. They get matched to
the nearest platform, and that platform gets tailored: capacity, dimensions,
electrode loadings, maybe a chemistry grade. So the real design problem at
IBC is not "search the universe of possible cells." It is "tailor one of
three known families, fast and well." That is a smaller, better-understood
search space, it is where IBC's manufacturing experience and data actually
exist, and the tool is built around it.

IBC also has two software efforts that this tool connects to. Nyaya AI is
their manufacturing intelligence platform (defect detection, yield, state of
charge and health estimation, remaining useful life). Battery Nexus is
described as the place where requirements go in and designs come out, which
is, almost word for word, what this engine is.

One honest boundary, stated up front because it builds credibility rather
than costing it: IBC's hardest production problem, from every public signal
(the existence of Nyaya, funding announcements about AI for yield
enhancement, the copy-exact factory strategy), is yield during scale-up:
making cells consistently and transferring that consistency from pilot to
Gigafactory. This tool does not fix yield. It improves the front of the
business (quoting and design convergence) and it frees pilot-line slots by
removing redundant prototype loops, which indirectly helps everything that
competes for that line. We do not claim more than that.

---

## 3. The value, precisely

Three levers, in increasing order of money:

**Lever one: senior engineer hours.** The translation from customer spec to
first candidate design currently lives in a few experts' heads and takes
days of their attention per request. The tool does the translation and the
exploration automatically, so the expert's job becomes reviewing ranked
candidates with reasoning attached instead of producing them from scratch.

**Lever two: quote speed.** A customer who asks "can you build a cell that
does X, and what would it weigh and cost" gets an engineering-grounded answer
in a day instead of weeks. For a company competing for niche customers
against bigger vendors, answering first with credible numbers wins deals.
Notably, this lever runs mostly on the calculator layer, which is the single
most trustworthy component in the whole system. It works even before any
simulation is calibrated.

**Lever three: fewer prototype iterations.** The big one. If better starting
designs, plus smarter selection of which prototypes to build (explained in
section 6 under the build plan), take a typical engagement from three
build-test loops to two, that is weeks of calendar time, real money, and a
freed pilot-line slot on every custom engagement, forever.

The size of the prize is a simple product:

(custom requests per year) x (cost of one build-test loop) x (loops removed)

All three numbers exist only inside IBC. If they handle thirty custom
requests a year, this tool is a serious asset. If they handle three, it is a
nice-to-have and the effort belongs elsewhere. This is why the first real
conversation with IBC's design team (Kunal, per Santi) matters more than any
code written before it.

---

## 4. The reframe: what this idea is and is not

The original pitch leaned on breadth ("optimize any cell, any chemistry")
and on accuracy ("trust the simulation"). Both needed correcting, and the
corrected version is the idea this document describes.

**On breadth:** the tool searches within IBC's three platform families and
inside IBC's manufacturing envelope (the coating thicknesses their machines
can lay down, the porosities their calendering can hit, the formats they
build). Same architecture as before, smarter bounds, far more credible
outputs, because every candidate it proposes is something IBC could actually
manufacture next month.

**On accuracy:** no simulation is "the same as running experiments in a
lab," and pitching that would kill the tool's credibility with the first
engineer who checks. The corrected claim is sharper and true:

**The tool does not compete with the lab. It competes with the engineer's
first guess.**

Today's human process cannot predict a cell perfectly either; that is
precisely why prototypes get built and tested. The tool wins not by being as
good as the lab but by making the starting point better than an expert's
first guess and by making each physical build teach more, so the lab
converges in fewer iterations. The lab remains the final word, always.

**What the tool is not:** not a replacement for testing, not a yield fixer,
not a claim of lab-grade accuracy, and not a replacement for engineers. It
replaces the early-stage exploration of "which part of the design space
should we even be looking at," so engineers spend their time on detailed
design, manufacturing, and judgment.

---

## 5. Trust tiers: the product principle that makes engineers believe it

Every number the tool outputs is labeled with the confidence of the layer
that produced it. This is not a disclaimer buried in a footnote; it is a core
feature, because a tool that never claims more than it knows is a tool an
engineer will actually use.

**Tier one, quote-grade: the cell calculator.** Capacity, stored energy,
energy density, mass, volume, layer counts. These come from arithmetic over
known material properties and land within a percent or two of the built
cell. These numbers can go in front of a customer.

**Tier two, design-guidance grade: calibrated DFN simulation.** Once the
physics model has been fitted to IBC's own cells using IBC's own test data,
its voltage curves, rate capability, and thermal predictions are good (tens
of millivolts of error in the conditions it was fitted for), with known weak
zones at very high discharge rates and at high temperature near the end of
discharge. These numbers guide design decisions and get reported with their
error bars.

**Tier three, directional: uncalibrated DFN and all degradation
predictions.** A DFN model running on published literature parameters
(which is where any proof of concept starts) describes the specific
commercial cells those parameters were measured on, not IBC's cells. Its
absolute numbers are wrong for IBC; its rankings and trends are still
informative ("design A beats design B on power, and here is why").
Degradation predictions (how fast a cell ages) are directional always, even
when calibrated: "A should age slower than B because it plates less lithium
at this charge rate," never "this cell will last 832 cycles." Cycle life is
the number customers care about most and the number physics models can
defend least, so the tool treats it with corresponding humility.

**Ground truth: the pilot line.** Built and tested cells are the only truth.
The tool's relationship to them is to make every build count.

---

## 6. The system, end to end, every step explained

The engine is a pipeline. A plain Python program called the orchestrator (a
state machine: a program that always knows what stage it is in and what
comes next) runs everything. Language-model agents are consulted at defined
checkpoints. Specialized tools do all the math and physics. One language
model plays every agent role; each "agent" is the same model given one
narrow job, its own instructions, and a bounded menu of decisions it is
allowed to return. Here is each step, what it does, and why it exists.

**Step 1. Customer RFQ.** Everything starts with an application described in
plain language. "We build agricultural drones. Flights are 45 minutes,
motors pull 80 A at takeoff and 25 A at cruise, it gets to 45 C in the field,
we need 500 charge cycles, recharge in under 30 minutes, and the battery bay
is this size and this weight budget." No battery vocabulary required from
the customer.

**Step 2. Intake agent.** A conversation, not a form. The agent knows what a
cell design requires (operating conditions, duty cycle, hard constraints,
chemistry preferences) and asks for whatever is missing. It also surfaces
what the customer implies but does not say: desert operation implies thermal
margin; sub-30-minute recharge implies lithium plating risk during fast
charge; airborne use implies vibration and weight sensitivity. Its output is
a structured specification: cell-level targets plus a test protocol that
mirrors the real duty cycle (takeoff, climb, cruise, land, at the right
currents and durations), so every simulation downstream is judged against
the customer's actual life, not a generic lab test. Before the autonomous run
begins, an IBC engineer reviews and approves this structured spec: a
human-in-the-loop gate that catches a misread requirement before any compute is
spent and keeps a person accountable for what the run optimizes. The
"autonomous" part is everything after this approval, not the requirements.

**Step 3. Platform matcher.** Before any optimization, the spec is matched
against IBC's platform families and the library of heritage designs. A
high-energy aviation request lands in Prabal 3000 territory; a
lifetime-dominated storage request lands in 2000 territory; ambiguous cases
get flagged for multi-chemistry comparison. This anchors the search where
IBC has manufacturing experience and data, and it mirrors how IBC's own
engineers think, which matters for adoption.

**Step 4. Cell calculator.** The algebra layer described in section 1, made
instant. Given candidate materials, loadings, thicknesses, and geometry, it
computes capacity, energy, mass, volume, and layer counts. For a large
fraction of customer questions ("what would a 60 Ah version weigh?") this
layer alone is the answer, minutes after intake, at quote-grade confidence.

**Step 5. Screening (design of experiments, part one).** Before spending
simulation budget, a sensitivity analysis (Morris or Sobol methods, the
modern descendants of factorial screening from classical design of
experiments) determines which three or four design parameters actually move
the objectives for this specific application. For a power-limited drone cell
that might be cathode thickness and porosity, with particle size barely
mattering; for a storage cell the ranking differs. The optimizer then
searches a smaller, smarter space. This is the classic experimental-design
flow: screen first to find what matters, optimize second.

**Step 6. Strategy agent.** Reads the spec plus retrieved knowledge (section
8) and makes the opening judgment calls: which two or three search
approaches to run in parallel (energy-first, power-first, balanced), which
simulation tools fit the application (drones get drive cycles and rate
sweeps; storage gets long degradation runs), and what the scoring weights
should be. Important clarification: the parallel approaches are not three
products for three goals. They are three starting points in different parts
of the design space, all hunting the same single best design that meets all
requirements, so that good solutions are not missed by searching from only
one direction. The agent suggests search regions; it never picks raw
parameter numbers. Numbers belong to the optimizer.

**Step 7. PyBOP optimizer (Bayesian optimization).** The component that
decides which exact designs to simulate next. Explained from scratch in
section 7; the short version is that it maintains a statistical map of "how
good is each region of the design space," picks the next trials to balance
exploring unknown regions against exploiting promising ones, and updates the
map after every batch of results. Every trial is informed by every previous
trial. This is pure math, no language model involved.

**Step 8. Validation layer.** A rule-based gate between the optimizer and
the simulator. Every candidate is checked before any compute is spent: is it
physically sensible, is it inside IBC's coating and calendering envelope, do
the geometry and layer counts close. Bad candidates die here for free
instead of producing a garbage simulation or a crashed solver.

**Step 9. PyBaMM DFN simulation.** The virtual lab. PyBaMM is the leading
open-source battery simulation package; DFN (Doyle-Fuller-Newman) is the
standard physics model of a lithium-ion cell, explained in section 7. A cell
recipe goes in; voltage curves, temperature, and capacity come out in a
fraction of a second, with thousands of simulations runnable in parallel on
an ordinary multi-core machine. A lightweight fixer agent handles failures:
it sees the error and context, applies a standard fix from a known decision
tree (relax solver tolerances, switch solvers, retry a malformed response,
exclude an obviously wrong result), tries at most three times, then skips
and logs. A failure costs a retry, never the run.

**Step 10. Analysis agent.** Sits where a human engineer would sit between
experiment rounds. Plain code first aggregates the round's results into
clean metrics per design (energy, power compliance, temperature rise,
constraint margins). The agent then reads those metrics and explains what
worked and why ("all top designs run hot above 2C; thickness is buying
energy but costing thermal headroom"), and returns strategic adjustments
chosen from a bounded menu: narrow an approach, abandon a failing one,
tighten a constraint, switch from cheap screening simulations to full
degradation runs. Its answer comes back as structured data the orchestrator
validates and executes; a malformed or out-of-bounds decision is rejected
and retried, never obeyed.

**Step 11. Progress check.** There is no fixed round limit, deliberately.
After each batch, code computes the raw improvement numbers (how much did
the top designs' scores move), and the analysis agent judges whether that
constitutes meaningful progress. While gains are real, the run continues;
there is no reason to stop a search that is still finding better cells. When
improvement flattens, the agent calls the run done and hands off. Run length
is therefore emergent: an easy spec plateaus in a few rounds, a tight
multi-constraint spec runs longer, and effort scales with difficulty rather
than with an arbitrary cap.

**Step 12. Evaluation agent.** Scores the surviving designs on what physics
alone does not capture. Manufacturing feasibility: can this be coated,
pressed, and sourced, scored against IBC's actual equipment limits. Relative
cost: which design is cheaper and by roughly how much. Safety: thermal
margins and lithium plating flags. Chemistry comparison: if the customer did
not choose a chemistry, the full optimization runs separately per candidate
chemistry and the results are compared honestly. Scoring weights are
configured per application: drones weight energy density, storage weights
lifetime.

**Step 13. Build plan (design of experiments, part two, and the step that
ties the tool to IBC's economics).** Instead of just ranking the top five
designs, the tool proposes the three to six prototypes that would jointly
teach the most when physically built and tested. The naive choice (build the
five best-scoring designs) is wasteful, because five near-clones of the
winner teach almost nothing new. The DoE choice spreads the builds across
the informative directions of the design space (for example: the best
design, the best design at the other end of the porosity range, the best
alternative chemistry, one deliberately at the edge of the thermal
constraint), so the test results discriminate between hypotheses and
recalibrate the models hard. This applies classical design of experiments
exactly where it was invented for: the regime where each experiment is
expensive. Pilot-line builds are that regime.

**Step 14. Report agent.** Writes the deliverable in whatever format IBC's
engineers already use: ranked designs with complete parameter sets,
simulation data per design, a constraint compliance table with margins,
plain-language tradeoff explanations, and design-space maps. The maps are
heatmaps of the whole explored landscape, showing where good designs live
and where constraints bind. They matter because they give engineers
intuition about the space, not just an answer: if performance is flat across
a porosity range, the factory does not need to hit an exact number, and an
engineer might spot something in the landscape the system missed. The
engineer can also refine conversationally ("push cycle life above 800,"
"switch to LFP"), which triggers a new optimization round on top of existing
results rather than starting over.

**Step 15. Engineer review, build, test, and the feedback loop.** The
tool's job ends at a recommendation. IBC engineers review, decide, build,
and test, exactly as they do today. Then the loop closes: the real test data
is uploaded back into the system, the optimizer refits the physics model's
parameters so its predictions match what the factory actually produced, and
the calibrated parameters enter the knowledge base. Over time, predictions
move from "literature cells" to "IBC's actual materials and process," and
design number twenty starts from everything learned in designs one through
nineteen. This loop is what turns a one-time tool into a permanent,
compounding part of IBC's workflow, and it is the part an outside software
vendor cannot replicate, because it runs on data that never leaves IBC.

**Who is in charge, one sentence each.** PyBOP decides what to try next
(adaptive math). The analysis agent decides when to stop (judged progress,
no cap). The language-model agents decide where to focus and how to spend
the budget (bounded judgment from menus). The orchestrator executes
everything (deterministic Python). PyBaMM is the only component that knows
physics. Humans make every consequential call at the end.

---

## 7. Technical foundations, from the ground up

**What the DFN model actually is.** A lithium-ion cell works by shuttling
lithium between two porous electrodes through a liquid electrolyte. The
Doyle-Fuller-Newman model is the standard mathematical description of that
process. It treats each electrode as a porous sponge of active-material
particles and solves, as one coupled system of differential equations: how
lithium diffuses inside the particles, how lithium ions move through the
electrolyte filling the pores, how charge is conserved in both the solid and
liquid phases, how fast the insertion reaction runs at each particle surface
(which depends on local conditions), and how much heat all of this
generates. Extensions add aging mechanisms: the slow growth of the SEI layer
(a film on the anode that permanently consumes lithium) and lithium plating
(metallic lithium depositing during aggressive charging, which both ages the
cell and creates safety risk). Solve all of it together and you get the
cell's voltage, temperature, and capacity over time for any usage pattern.
This is why DFN can answer design questions: change the electrode thickness
in the equations and the predicted behavior changes the way a real cell's
would.

**Why DFN is genuinely hard to use well: parameterization.** The equations
need roughly thirty input parameters. Some are easy (thicknesses,
geometry). Several are not measurable with a ruler: diffusion coefficients,
reaction rate constants, transport properties of the electrolyte. Getting
those numbers for a specific real cell is called parameterization, and it is
the hard scientific core of this whole field. Three facts shape everything:

First, parameters do not transfer. A parameter set measured for one cell
describes that cell's materials and process. IBC's cells need IBC's
parameters.

Second, fitting is underdetermined. If you tune parameters until the model
matches a measured voltage curve, you can get excellent predictions in the
fitted conditions while individual parameter values remain non-unique and
physically wrong, which means the model misleads you the moment you leave
those conditions. The cure is richer data: rate sweeps at multiple currents,
GITT (a pulse technique that isolates diffusion), EIS (impedance
spectroscopy, which separates different internal processes by frequency),
ideally anchored by direct physical measurements. The richer the data, the
more the fit is forced to be physically true rather than merely curve-fit.

Third, published parameter sets exist because someone did months of careful
experiments on one specific commercial cell. The standard set this project
starts with (Chen2020, characterizing an LG cylindrical cell) is the product
of exactly that work. Running on it proves the machinery; it does not
predict IBC's cells.

The path through all three: start on literature parameters with everything
labeled directional, then calibrate to IBC's cells using PyBOP's fitting
capability on IBC's test data, then keep recalibrating as the feedback loop
delivers fresh build-and-test data. Calibration is not a finishing touch; it
is the step that converts the tool from a demo into an instrument.

**Where DFN is weak even when calibrated.** Published validation work shows
the error growing at higher discharge rates and near the end of discharge at
elevated temperatures. The tool handles this by mapping its own weakness:
the validation matrix (a small factorial across C-rates and temperatures)
quantifies error in each operating region, so predictions are reported with
the error bar of the region they were made in. And cycle life, as stated in
the trust tiers, is always a ranking with reasoning, never a promised
number: degradation physics gives reliable directions, not reliable
lifetimes, and simulating hundreds of cycles is costly enough that
extrapolation adds its own uncertainty.

**Bayesian optimization, explained from scratch.** The design space here has
around ten dimensions. A blind grid sweep wastes nearly all its simulations
on bad regions; reinforcement learning needs thousands of training episodes
before it is useful, which is wrong for a problem that starts cold.
Bayesian optimization is the standard answer for expensive black-box
optimization. It maintains a Gaussian process, which is a statistical model
that, given the results observed so far, estimates both the predicted
quality of any untried design and the uncertainty of that prediction. An
acquisition function then picks the next trials by balancing two pulls:
exploit (sample near the best results so far) and explore (sample where
uncertainty is high, because something better might be hiding there). After
each batch of simulation results, the map updates and the cycle repeats. The
practical effect: the optimizer finds good designs in hundreds of
simulations instead of tens of thousands, and it works from run one. PyBOP
is the package that provides this, built specifically on top of PyBaMM, and
it doubles as the parameter-fitting engine for calibration, which is a
convenient two-for-one.

**Design of experiments, and why it is the right language for IBC.**
Classical DoE was invented for the world where each experiment costs real
money and you can afford eight to thirty of them: lay out a deliberate plan
of runs (factorial designs and their descendants) that extracts the maximum
information, including interaction effects, from the minimum number of
experiments. Bayesian optimization is its adaptive descendant for the cheap-
experiment world. This project uses both, each where it belongs: DoE
thinking for the expensive physical world (the build plan in step 13, and
the validation matrix), Bayesian optimization for the cheap simulated world
(step 7), and DoE-descended sensitivity screening to shrink the space before
optimizing (step 5). A side benefit: DoE is the native statistical language
of manufacturing engineers. IBC's process people almost certainly run DoEs
on coating and calendering already, so describing the tool as "adaptive DoE
plus a physics simulator" connects it to something they already trust.

**Why the language model never holds the steering wheel.** Language models
hallucinate; this is contained by architecture rather than wished away. The
LLM is consulted at checkpoints and answers in structured form (JSON),
picking from menus of legal actions with bounded values. The orchestrator,
which is deterministic Python, validates every answer and executes only
legal ones; a hallucinated action or out-of-range value is a rejected
message and a retry, never an obeyed command. Below that, the rule-based
validation layer checks every candidate design before simulation, and the
physics itself is the final filter. The worst case a hallucination can cause
is a wasted retry. This is the same containment pattern serious companies
use to deploy language models anywhere: constrain the outputs, ground the
inputs in retrieved data, verify with something that cannot hallucinate, and
keep humans at the consequential step. It is also why the agents are split
into narrow roles: a prompt that is good at interviewing a customer is bad
at critiquing simulation results, so each job gets its own clean
instructions instead of one giant do-everything prompt.

**The knowledge base.** A retrieval system (ChromaDB with embeddings) that
every agent consults before deciding: published parameter sets, electrode
design heuristics, IBC's manufacturing constraints, material properties,
application profiles for IBC's markets, and the results of every past run.
Retrieval grounds the agents' decisions in real data instead of model
memory. And because every completed run and every physical build feeds back
in, the system compounds: if a porosity range keeps winning for drone cells,
the next drone run starts already knowing it.

---

## 8. Prior art and the market: is this already solved?

The pattern of "language model orchestrates specialized scientific tools"
is proven in research systems (Coscientist for chemistry experiments,
ChemCrow, ChatBattery, MARS), which is where the architecture came from.
None of them do this task.

Commercially, the neighboring category exists and is paid for, which
validates the premise. Ionworks, founded by PyBaMM's creators, sells
simulation-as-a-service explicitly aimed at replacing experiments and
exploring design spaces in the cloud, with test-data ingestion and
parameterization services. About:Energy sells parameterized cell models
delivered into customers' own tools, plus parameterization as a service.
COMSOL and GT-AutoLion are the established licensed-software options. So
"companies pay for simulation-driven design help" is a fact, not a hope.

The gap this idea sits in: all of those tools are operated by simulation
specialists. Nobody ships the autonomous loop (requirements conversation in,
ranked buildable designs and a DoE build plan out, no simulation expert in
the middle), and nobody can ship the version calibrated continuously on one
manufacturer's own pilot-line data, because that data never leaves the
manufacturer. The moat is not the language model. The moat is the embedded
calibration loop, which is precisely the thing two interns inside IBC's
walls can build and an external vendor cannot.

The skeptic's question, answered honestly: "isn't this just PyBaMM in a
chatbot wrapper?" The simulation and optimization layers are indeed standard
tools, used by everyone. The wrapper is the product: intake that speaks
application language, platform-bounded search, trust-tiered honesty,
strategic iteration without a human in the loop, DoE build selection, and a
calibration flywheel. Ionworks raised venture money to build a manual
version of this wrapper. The claim here is automating it for one company's
specific workflow.

---

## 9. Risks and unknowns, stated plainly

**The value size is unverified.** The whole business case multiplies three
numbers (requests per year, cost per loop, loops removable) that we have not
seen. The Kunal conversation either sizes this up or down.

**Everything above the calculator is data-gated.** Calibration needs IBC's
test data at sufficient richness, on IBC's timeline, not ours. Until then,
simulation outputs are directional, and the demo must be framed that way.

**Adoption risk.** Even a good tool fails if engineers do not use it. The
mitigations are baked in (platform-bounded search, output in their formats,
trust tiers, intake that asks their questions), but the risk is real,
especially at a company whose attention is on a yield fight.

**Scope versus one summer.** The full fifteen-step engine is more than a
summer. The realistic good outcome is the trustworthy core (calculator,
validated and then calibrated DFN, optimizer) working end to end, with the
agent layer partial. The idea is deliberately structured so partial outcomes
are independently valuable: the calculator alone speeds quotes; a calibrated
DFN setup alone is an asset; the optimizer alone improves starting designs.

**Performance claims.** Simulation timing estimates (fractions of a second
per run, thousands in parallel) degrade once degradation and drive-cycle
runs enter the mix. No number goes in front of IBC that has not been
measured.

---

## 10. The three questions that size everything

1. How many custom cell requests does IBC handle per year, and how many do
   they decline or lose on response time?
2. For a typical custom engagement, how many prototype build-test iterations
   does it take to converge, and what does one iteration cost in time and
   money?
3. What does the current request-to-design process look like: who does it,
   with what tools, producing what output format?

The first two multiply into the business case. The third defines what the
tool must plug into. None can be answered outside IBC.

---

## Appendix: small glossary

- **C-rate**: discharge speed relative to capacity. 1C empties the cell in
  one hour, 2C in half an hour.
- **Porosity**: the fraction of an electrode that is empty space (filled
  with electrolyte). More porosity moves ions faster; less packs more
  energy.
- **Calendering**: pressing coated electrodes to a target thickness and
  porosity.
- **N/P ratio**: anode-to-cathode capacity balance; a key safety and
  lifetime design choice.
- **SEI**: a film that forms on the anode and slowly consumes lithium; the
  main background aging mechanism.
- **Lithium plating**: metallic lithium depositing on the anode during
  aggressive charging; ages the cell and creates safety risk.
- **GITT / EIS**: test techniques (current pulses / frequency sweeps) that
  isolate internal cell properties; the data that makes model fitting
  physically meaningful.
- **RFQ**: request for quote; a customer asking what IBC can build for them.
- **A/B/C samples**: industry maturity stages for prototype cells on the way
  to production.
- **DFN**: Doyle-Fuller-Newman, the standard physics model of a lithium-ion
  cell.
- **PyBaMM / PyBOP**: the open-source simulation package and the
  optimization/fitting package built on top of it.
- **Bayesian optimization**: adaptive search that uses all results so far to
  choose the next trials; works from run one.
- **DoE**: design of experiments; planning a minimal set of experiments to
  learn the most, the native statistical method of manufacturing.
