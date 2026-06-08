# Responses to Vipin Garg's review

Point-by-point on the comments left on the May 2026 proposal, with what changed.
The proposal itself is superseded by `THE_IDEA.md` and the working engine; these
responses fold the feedback into the current state.

## C1 — roles: PM writes the PRD, engineers design/implement

Fair, the proposal's wording ("the engineer describes what the customer needs")
conflated roles. Corrected framing: the input is a **customer requirement**, the
same thing a product/sales person turns into a PRD or an RFQ after talking to the
customer. The tool consumes that requirement and produces a first design; the
**engineer** is the user who reviews, decides, and does the real design,
manufacturing, and test. The current concept already starts from "Customer RFQ"
rather than "engineer describes," so this is a wording fix, not a structural one.
The tool sits where the early PRD-to-first-design exploration happens, and hands
ranked starting points to the engineers.

## C2 — add a block diagram

Done. See `docs/diagrams/system_architecture.png` (rendered) and
`docs/diagrams/system.drawio` (editable). It shows the blocks and layers: people,
the LLM agent layer (bounded judgment only), the deterministic orchestrator, the
math-and-physics tools, and the knowledge/calibration layer. The diagram makes the
"LLM orchestrates, it does not do the science" split visual: the agents are one
colored layer, the math and physics are a separate layer, and the orchestrator
validates everything in between.

## C3 — add a human-in-the-loop after intake, before the run

Considered, but we are keeping the run fully autonomous rather than adding a
separate mid-pipeline approval gate. The human is already in the loop at both
ends: a person writes the requirement going in, and engineers review the ranked
output and decide what to actually build coming out. The run itself (search and
scoring) is the part we want automated, with no human pause in the middle.

## C4 — don't just mimic the existing workflow; review it first

Good push, and we agree. The plan is not to hard-code IBC's current
request-to-design flow. The first step (the conversation with Kunal) is to
understand that flow **and** judge where it is slow or manual, then propose the
better flow rather than freeze the existing one in software. The earlier "fit the
existing workflow" line is softened to: understand the current workflow, keep what
works for adoption, and improve the parts where the automation can do better.

## C5 — architecture needs more work, let's talk

Since the proposal, the architecture is no longer on paper: the engine is built
and runs end to end (calculator, validated DFN, optimizer, orchestrator, report,
with the agent decision points as stubbed seams). The architecture diagram above
reflects what actually exists plus the planned pieces (knowledge base, calibration
loop). Happy to walk through it live.

## C6 — use draw.io

`docs/diagrams/system.drawio` opens and edits directly in draw.io / diagrams.net.
The rendered `docs/diagrams/system_architecture.png` is the same diagram for quick
viewing.
