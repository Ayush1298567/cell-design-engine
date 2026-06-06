# Assumptions

DRAFT for Ayush to edit. This lays out every assumption the engine currently
makes, so the conversation on the 8th is about whether these match how IBC
actually works, not about what the tool magically does. We would rather be told
"that assumption is wrong" now than find out after a prototype build.

## What the tool is assuming about its job

The tool assumes its job is to beat the engineer's first guess, not the lab. It
does not try to predict a cell perfectly, because nothing short of building and
testing the cell does that. What it assumes it can do is start the design closer
to the answer and make each physical build teach more, so the existing build-test
loop converges in fewer passes. If that assumption is wrong, which means IBC's
first guesses are already very good or the number of custom requests is small,
then the value is much lower and we should know that early.

It also assumes the real problem is "tailor one of IBC's platforms fast and
well," not "search every possible cell." We built it to search inside a platform
family and inside a manufacturing envelope, because that is where IBC has data
and experience, and because every design it proposes should be something the line
could actually build next month.

## Modeling assumptions (the physics layer)

1. **The calculator is just bookkeeping, and we trust it.** Capacity, energy,
   mass, volume, and N/P come from algebra over material properties and geometry.
   This makes sense because it is not predicting physics, it is adding up known
   numbers, so it lands within a percent or two of a built cell. These are the
   numbers we would put in front of a customer.

2. **The DFN simulation is directional right now, not absolute.** We validated it
   against a real published cell (LG M50), and the physics shape is right, but it
   runs on literature parameters, so its absolute numbers describe that published
   cell, not IBC's cells. We treat its rate and thermal outputs as rankings ("design
   A beats design B on power, here is why"), not as promises. In fact this is the
   single most important thing to be honest about, because a tool that claims
   lab-grade accuracy loses the first engineer who checks it.

3. **We assume calibration fixes the gap, and that is a hypothesis until we run
   it.** Our validation showed the model sits about 40 mV off the real cell in a
   fairly constant way, which is the kind of error calibration removes. We assume
   that once we fit the model to IBC's own test data the directional numbers
   become design-guidance numbers. We have not proven this on IBC cells yet,
   because we do not have IBC test data yet.

4. **Cycle life is always a ranking, never a number.** Degradation physics is
   reliable about direction ("this design plates less lithium, so it should age
   slower") and unreliable about exact lifetimes. We assume nobody wants us to
   promise "832 cycles," because that is the number physics defends least and the
   number customers care about most.

5. **The thermal number is a self-heating proxy, not a pack temperature.** It
   ranks designs by how hot they run relative to each other. The absolute degrees
   are not a calibrated cell temperature yet, that needs a pack-level thermal
   model, which is later work.

## Data assumptions (what is real vs placeholder)

Everything in the demo cell, the search bounds, and the requirements is a
literature placeholder, not an IBC value. The chemistry is NMC811 / graphite, the
cell is loosely the LG M50 family, and the targets are made up for an example
drone. This is on purpose, so the engine runs and we can show the flow, but none
of these numbers should be read as IBC's. The whole thing is config-driven, so
plugging in IBC's real platforms, manufacturing limits, and example requests is
editing a config file, not rewriting code.

## Trust tiers (how to read any number the tool prints)

- **Quote-grade:** calculator algebra. Customer-facing.
- **Design-guidance:** the DFN after it has been calibrated to IBC cells. Not there yet.
- **Directional:** the DFN today (literature parameters), and all degradation. Rankings only.
- **Ground truth:** the pilot line. The only real truth.

## What we are assuming about the process (need IBC to confirm)

These are the assumptions we are least sure about, and they are the ones that
size the whole thing:

- That custom requests happen often enough that cutting design time matters.
- That a typical engagement takes more than one build-test loop to converge, so
  there is a loop to remove.
- That engineers would actually use a tool that outputs ranked designs with
  reasoning, in a format close to what they already use.

If any of these is off, the priority changes, and we would rather hear it on the
8th than build toward the wrong thing.

## Proposed success metric (for discussion)

We propose judging the tool not on simulation accuracy in absolute terms, but on
two things: does the calibrated DFN match IBC's own cells within the error band
the literature reports (tens of millivolts in the conditions it was fitted for),
and does a starting design from the tool need fewer build-test loops than the
current first guess. The first is measurable as soon as we have IBC test data.
The second is the real prize and takes a few real engagements to measure. Open to
a better metric, this is our starting point.

## Known limits we are not hiding

- Uncalibrated, so absolute non-calculator numbers are wrong for IBC cells.
- The DFN error grows at high discharge rates and near the end of discharge at
  high temperature, which is a known weak zone in the literature too.
- It does not fix yield, which is likely IBC's real production bottleneck. It
  helps the front of the business and frees pilot-line slots, and we say that out
  loud rather than overselling.
