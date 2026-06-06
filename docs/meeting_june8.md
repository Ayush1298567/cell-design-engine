# June 8 kickoff with Sasi — talking script

11am PT, Google Meet. Goal: walk out with his guidance on the validation
approach, the Kunal intro, agreement on a success metric, and a check-in cadence.
Lead with what he scoped (DFN validation), then show the engine as where it goes.
Do not oversell. The honesty is the credibility.

## 0. One-line frame (say this early)

"Since you scoped us to validate the DFN, that is what we led with, and it came
out well. We also went ahead and wired up the full flow as a working prototype on
literature data, so you can see where this is headed, but the validation is the
real deliverable."

## 1. The validation (lead here, this is what he asked for)

- We implemented PyBaMM's DFN and validated it against real published cell data
  (the LG M50, the Chen2020 dataset), at four discharge rates.
- Honest result: the physics shape is right. On the raw comparison the model
  tracks the real cell to roughly 30 mV at low rate and tighter at high rate,
  and the dominant error is a near-constant ~40 mV offset, which is exactly the
  kind of error calibration removes.
- We are careful about two things: at high rate the comparison is partly
  temperature-confounded because the real cell self-heats and our run is
  isothermal, and the headline "tight" number depends on how you normalize, so
  we report both the flattering and the honest version.
- Takeaway for him: the machinery is sound, the error left over is the kind that
  calibrating on IBC's own cells removes. That is the whole thesis, now with
  numbers behind it.

## 2. The engine (show the prototype, frame as "where this goes")

- Walk the flow: a plain-language requirement goes in, and the tool produces
  ranked buildable designs plus a map of the design space, searching inside a
  platform's manufacturing envelope.
- If screen-sharing, show the design-space heatmap: energy goes up toward thick,
  dense electrodes, but that corner is infeasible on power and heat, so the best
  feasible design sits on the constraint boundary, and the optimizer finds it in
  tens of simulations.
- Key architecture point he will care about: the language-model parts never hold
  the wheel. They pick from menus, a deterministic program checks every answer,
  and the physics is the final filter. Today those parts are deterministic stubs,
  so the whole thing runs with no API and no cost.

## 3. The honest framing (say this plainly, it builds trust)

- Every number is labeled by how much to trust it: quote-grade from the
  calculator, directional from the uncalibrated simulation, ground truth only
  from the pilot line.
- Right now everything above the calculator is directional, because it is not yet
  calibrated to IBC cells, and all the demo values are literature placeholders,
  not IBC's.
- It does not fix yield, which is probably the real production bottleneck. It
  helps the front of the business and frees pilot-line slots. We are not pitching
  it as more than that.

## 4. Point him at ASSUMPTIONS.md

"We wrote down every assumption the tool makes. We would rather you tell us which
ones are wrong now than after a build. The ones we are least sure about are the
process ones, which is the whole reason we want time with Kunal."

## 5. The asks (do not leave without these)

1. **Kunal intro.** We need to understand how IBC actually goes from a customer
   request to a cell design, what tools and formats engineers use, and the three
   sizing questions below. This is the highest-leverage thing for the project.
2. **Success metric.** Propose ours (does the calibrated model match IBC cells
   within the literature error band, and does a tool-generated start need fewer
   build-test loops), and ask if that is the right bar.
3. **API funding.** The agent layer runs on the Claude API. Ask if the company
   can cover that as a project cost. It is small, but we did not want to front it.
4. **Check-in cadence.** He offered weekly check-ins on May 22, let's lock one.
5. **Logistics.** Remote work question (asked May 21, still open) and the CIA.

## 6. The three sizing questions for Kunal (and partly for Sasi)

1. How many custom cell requests does IBC handle per year, and how many do you
   lose or decline on response time?
2. For a typical custom engagement, how many build-test iterations does it take to
   converge, and what does one iteration cost in time and money?
3. What does the current request-to-design process look like: who does it, with
   what tools, producing what output format?

Plus the open one: what actually limits you right now, yield, throughput, design
turnaround, or test capacity?

## 7. If he asks "is it accurate / is it done"

"The engine is built and runs end to end. It is accurate at the calculator level
today. The simulation is validated but not yet calibrated to your cells, so its
absolute numbers are directional until we fit it to your test data. So it is
demoable now, and it becomes deployable once we plug in your values and calibrate.
That calibration loop is the part an outside vendor cannot build, because it runs
on data that never leaves IBC."
