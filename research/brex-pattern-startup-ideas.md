# Finding the Next Brex: Structurally Orphaned Markets (June 2026)

> **The brief.** Find a problem where a *new* company is **literally the only thing that can
> solve it** — a customer segment with money and urgency that incumbents do not merely serve
> badly but **structurally cannot serve at all** — in a billion-dollar or fast-growing market.
> The template is **Brex**: venture-backed startups had millions in the bank but could not get
> a corporate card, because every bank underwrites corporate cards on *personal credit* and/or
> *trailing revenue*. A cash-rich, revenue-less startup was not a bad customer — it was an
> **unrepresentable** one. No bank's underwriting model had a field that could say "yes." Brex
> issued a card underwritten on the cash balance instead, and owned a customer no incumbent could.
>
> **How this was produced.** A swarm of ~17 research agents fanned out across six domains
> (fintech, AI-native, healthcare/biotech, climate/energy/industrial, SMB/creator economy,
> and new-regulation/defense), each instructed to apply one test — *structural lock-out, not
> "serves poorly"* — and to verify every claim against live 2026 sources and report whether the
> gap is still open. Ideas an incumbent could close by "adding a feature" were rejected. The
> regulation/defense branch recursively spawned its own nested sub-swarm, so that cluster is the
> most heavily fact-checked.

---

## The pattern, stated precisely

Every genuine Brex-shaped opportunity has the same four-part signature. Use it as a filter:

1. **A customer segment that exists now, with money and urgency.** Not a "someday" market.
2. **A structural lock-out** — the incumbent's *risk/underwriting/onboarding model itself*,
   or a *law*, makes the customer unrepresentable. This is the crux. It must be a wall, not a
   gap. ("KYC requires a legal person." "Factoring needs an existing invoice." "Underwriting
   needs loss history." "Reg requires a FedRAMP-equivalent cloud.")
3. **A large or fast-compounding market.**
4. **The gap is still open** — incumbents are *structurally barred* from closing it (auditor
   independence, a 40-year-old rules system, an ESG screen, a legal-personhood requirement),
   not just slow.

The single most reliable generator of this signature in 2026 is **a brand-new class of economic
actor or a brand-new law** — because the moment one appears, an entire class of customers exists
that every incumbent system was architecturally built *before*, and therefore cannot represent.

---

## The winner

### #1 — The financial liability & underwriting layer for the AI agent economy

**Three of the six independent domain swarms converged on this from different starting points
(fintech, AI-native, SMB/creator).** That convergence is the strongest signal in the entire
study. It is the cleanest modern restatement of Brex: a **new class of economic actor** —
autonomous AI agents that hold value, pay for compute/APIs, buy goods, and transact with other
agents — that the financial system was architected before and **cannot represent**.

**The structural lock-out (the crux).** Two independent walls, both load-bearing:

- **Onboarding/identity.** KYC/AML law requires an account holder to be a *legal person* with a
  verified identity and a *beneficial owner who bears liability*. An autonomous agent is none of
  these. A bank's onboarding system has no field that can say "yes" to an agent as the customer —
  the same shape as Brex, one layer deeper. The industry has had to invent a *new* primitive,
  "Know Your Agent" (KYA), precisely because KYC "was never built for non-human actors."
- **Post-transaction recourse (the sharpest, most-open wedge).** This is the standout finding.
  Visa, Mastercard, Amex, and Stripe/OpenAI all *activated agent payments* in 2026 — the
  front-end (authorization) now exists. But the entire chargeback/dispute regime (Reg E, Reg Z,
  card-network reason codes) is built on one premise: **a human made the purchase decision.**
  When an agent buys, there is no human decision to adjudicate against. The networks cannot
  retrofit this — their dispute rails are a 40-year-old rules system baked into issuer/acquirer
  cores — so they **shipped acceptance and deliberately left disputes unbuilt.** The CFPB's
  January 2026 advisory held that the consumer's right of recourse is *not* extinguished by an
  agent mandate, creating live liability ambiguity for every merchant. Disputes on
  agent-initiated transactions are already running ~2.4× the rate of comparable human
  card-not-present transactions, with a *different composition* the existing system can't
  classify. **Money is flowing through a rail that has no recourse layer, and the only entities
  who could build it have publicly punted.**

**What the startup builds.** The underwriting + identity + liability rail for machine commerce:
(a) a verifiable agent-identity standard cryptographically binding each agent to a KYC'd human/LLC
owner who carries liability; (b) programmable, policy-bound spend controls (per-task budgets,
allowlists, kill-switch) with credit underwritten **against the principal's deposited balance,
Brex-style**, not the agent's non-existent credit file; (c) — the wedge — an **agent-commerce
dispute & liability clearing layer**: a verifiable mandate/audit trail of what the agent was
authorized to do, automated adjudication mapping agent intent-logs to network reason codes, and
liability routing between the human principal, the agent operator, and the merchant.

**Market.** Agentic commerce is forecast at **$1.5T (Juniper) to ~$5T (McKinsey) by 2030**;
chargeback cost alone is tracking to **$28.1B in 2026**; AI-agent software spend ~$206B in 2026
(Gartner). The x402 agent-payment protocol already processed ~165M transactions and ~500K active
agent wallets in early 2026.

**Why it's still open.** Everyone is fighting over the **rails and the front door** (Coinbase
Agentic Wallets, Mastercard Agent Pay for Machines, Meow agentic banking, Stripe/OpenAI ACP,
Skyfire). **No one owns the structurally-hard layer behind the door** — identity-to-liability
binding, agent credit underwriting, and dispute/recourse. The networks are *barred* from the
recourse piece by their own architecture; that is the moat. **Window: ~12–18 months** before a
network or Meow extends down into it, so the defensible asset must be the underwriting/dispute
*system of record*, not another wallet.

> **One-line pitch:** *Brex underwrote the startup the bank couldn't model; this underwrites —
> and adjudicates disputes for — the autonomous agent the entire payments system was built
> before.*

---

## The ranked shortlist (strong alternatives, cleanest structural locks first)

### #2 — AI performance & liability insurance

The cleanest *pure* structural "no" in the whole study: **incumbents are literally writing the
exclusion that creates the market.** ISO rolled out **absolute AI exclusions effective January
2026** — standard carriers are carving AI risk *out* of policies — because underwriting *is* the
quantification of frequency × severity from loss history, and AI risk has **no stable loss
history, mutates on every retrain, and is correlated across sectors.** A traditional carrier
cannot rationally price it.

- **Segment:** every company deploying agents into revenue-bearing/customer-facing roles, plus
  the AI vendors themselves (40% of enterprise apps embed agents by end-2026, per Gartner).
- **Build:** a specialist MGA/carrier underwriting on **model evals, continuous monitoring, and
  behavioral telemetry** (often parametric — pay out on a measured performance-deviation trigger)
  instead of historical loss tables, bundled with the governance/observability that produces the
  proprietary underwriting data.
- **Market:** AI-insurance premiums forecast ~$4.8B by 2032 (~80% CAGR). The telling number:
  **only ~5 standalone AI-liability products exist worldwide.**
- **Open?** Filling but wide open. Early movers exist (Armilla at Lloyd's, Munich Re aiSure,
  YC-backed Mount, AIUC, Counterpart). The structural "no" from standard carriers means the
  category is being *created* by specialists, not defended by incumbents.

### #3 — Per-dose acquisition financing for cell & gene therapies

A textbook structural lock with no dominant incumbent. To administer a one-time cell/gene therapy,
a provider must **buy the dose first** — sickle-cell therapies are priced at **$2.2M–$3.1M per
dose** — then wait to be reimbursed, often *below* acquisition cost (Medicare's inpatient CAR-T
DRG base is ~$269K against a far higher acquisition cost).

- **The crux:** medical-receivables **factoring (a ~$2B/yr industry) cannot help** — factoring
  advances against an *existing receivable*, but the problem is the **cash outflow before any
  receivable exists.** Banks underwrite the clinic's balance sheet, not a per-dose,
  drug-collateralized, reimbursement-contingent advance. No standard lender prices per-dose,
  outcome-contingent risk.
- **Build:** advance the drug-acquisition cost, take assignment of the reimbursement claim, price
  payer-mix + outcomes-based-contract risk — i.e., **underwrite the dose and the payer contract,
  not the borrower** (the Brex move).
- **Market:** US cell/gene-therapy CDMO market ~$3.14B (2025), ~28% CAGR; the relevant figure is
  the multimillion-dollar-per-dose volume with reimbursement structurally lagging.
- **Open?** Yes on the provider-financing side. Activity exists in *adjacent* lanes
  (payer-side outcomes contracting, CMS's CGT Access Model), but no dominant player does per-dose
  acquisition financing for community/outpatient providers — and the 340B outpatient shift expands
  the addressable base.

### #4 — Interconnection-deposit financing for clean-energy projects

The cleanest Brex analogy in climate. Developers must pay large, escalating **interconnection
deposits to hold a grid-queue position years before** the project has site control, permits,
offtake, or revenue. ~**2,060 GW** sat in US interconnection queues at end-2025, with ~5-year
median wait.

- **The crux:** project-finance lenders underwrite on *contracted cash flows and completed
  assets* — neither exists at the deposit stage. The asset on the balance sheet is a
  *refundable-then-non-refundable interconnection deposit*, a collateral type banks have **no
  model for and no appetite to touch.** The market is explicitly "nascent among commercial lenders
  with few options available."
- **Build:** a specialist lender underwritten on the **deposits themselves** — a borrowing base of
  pledged deposits, loan sizing recalculated as deposits convert from refundable to
  non-refundable as projects clear milestones. *Brex-for-queue-positions.*
- **Market:** >$22B of renewable projects were cancelled in H1 2025 alone; sunk cost per abandoned
  MW averages ~$200K; the deposit float across 2,000+ GW is many billions.
- **Open?** Wide open. The only proof point is a single $3M public-bank facility (NY Green Bank →
  Delaware River Solar). No fintech has productized it nationally. (Twin product: **parametric
  "queue-delay" insurance** for the same stranded-capital risk — also open, but gated on
  reinsurance capacity.)

### #5 — A compliance operating system for GENIUS-Act stablecoin issuers (PPSIs)

A brand-new *legal entity type* minted by a 2025 law. The GENIUS Act created the **Permitted
Payment Stablecoin Issuer (PPSI)**, and a wave of sub-$10B banks, fintechs, and brands are forming
as issuers in 2026–2028 — without a compliance department.

- **The crux (a *recurring* lock, which is rarer and stickier):** the law makes the obligation
  *perpetual and weekly* — monthly public attestation **+ confidential weekly reserve reporting to
  regulators**, a full BSA/AML program with a named officer (separate FinCEN PPSI rule, April
  2026), and redemption SLAs with freeze logic. Issuance platforms (Bridge/Stripe, Paxos, Brale)
  are *infrastructure* and **disclaim** these duties; the Big Four auditors are **independence-
  barred** from building the controls they themselves attest. So no incumbent can own it.
- **Build:** a horizontal "compliance OS" unifying reserve-data-to-attestation, weekly
  regulator reporting, turnkey BSA/AML program, and redemption-liquidity monitoring — sold to the
  long tail, *complementary* to issuance platforms.
- **Market:** stablecoin supply ~$1T late 2026 → **$1.2T–$2T by 2028** (Coinbase / US Treasury);
  per-issuer recurring ACV scales with issuer count, which the law is designed to multiply.
- **Open?** The issuance and attestation layers are taken; the **unified recurring-operations
  system of record for sub-$10B PPSIs is still open.** (Reject the EU/MiCA twin: only ~19
  authorized EMT issuers, already bank-grade — gap effectively closed.)

---

## Real, but the window is closing (proceed only with a sharper wedge)

These passed the structural test but a well-capitalized entrant is already in the lane, so the
greenfield land-grab is largely gone.

- **CMMC Level 2 / CUI compliance for the small defense industrial base.** Genuinely structural —
  **DFARS 252.204-7012 forces a FedRAMP-Moderate-*equivalent* cloud** (post-2023: 100% of
  controls, no open POA&Ms, 3PAO-validated) for any system touching CUI, so commercial M365 and
  generic MSPs are *legally* disqualified. Huge orphaned segment: **~76K–118K Level 2 firms**
  (counts differ by rulemaking), **only 1% feel ready**, median SPRS 60 vs. 110 required, and
  ~$116K median first-year cost crushing sub-$500K-revenue shops. **But contested** — PreVeil,
  Summit 7, Cuick Trac, and (April 2026) OSIbeyond's fixed-price CaaS are already attacking it.
  The remaining wedge is a *truly productized, transparently-priced, self-serve full stack*
  (enclave + GCC High + auto-SSP/POA&M + live SPRS) for the sub-50-employee contractor — not
  "offering the bundle," which several incumbents already claim.

- **Banking for defense-tech startups.** Perfect Brex shape (cash-rich, revenue-light, frozen out
  by fintech AUPs that bar "weapons/munitions" and by automated KYC/AML that flags ITAR/classified
  supply chains). **But Palmer Luckey's Erebor took the deposit side** — OCC national charter Feb
  2026, ~$635M capital, ~$4B+ valuation, explicitly targeting defense/AI/crypto founders. And
  EO 14331 (Aug 2025) is dismantling the "reputation-risk" lever banks used to debank. Remaining
  wedge is the *lending* side: contract-receivable / milestone-based venture debt underwritten on
  DoD/OTA/SBIR payment mechanics (Leonid Capital is the only defense-native player there), plus
  ITAR/CMMC-compliance as a fintech moat.

- **EU AI Act conformity-dossier automation.** Genuine white space: the signed **Annex V
  Declaration of Conformity** is a *product-specific, liability-bearing engineering dossier* that
  the GRC-incumbent (Vanta/Drata/OneTrust) "observe-controls-and-collect-evidence" paradigm
  structurally cannot produce, and ISO 42001 explicitly does **not** confer presumption of
  conformity. **But the high-risk deadline slipped** (provisionally to Dec 2027 / Aug 2028 under
  the Digital Omnibus, not yet law as of June 2026), deflating the forcing function — so urgency
  is a timing bet, not a wall.

---

## What the swarm explicitly rejected (and why)

Recording these matters as much as the picks — each is a plausible-sounding idea that **fails the
structural test** because an incumbent already adapted or the barrier is political, not structural:

| Rejected idea | Why it fails the test |
|---|---|
| Creator / gig / 1099 mortgages | Non-QM bank-statement/DSCR lenders (Griffin, MBANC) already productized it — feature gap, not a wall. |
| Cannabis banking | Barrier is a federal-law/political *wait* (eroding: Schedule III move, ~42% ACH by 2026). *No one* can serve until law changes, so a new company isn't uniquely the solution. |
| Patient-side GLP-1 / weight-loss BNPL | Saturated (Cherry, Sunbit, CareCredit, Scratch Pay). No wall left. |
| Generic BESS / battery property insurance | MGAs (Altelium, NARDAC, ~8 Lloyd's syndicates) already underwrite it — "serves poorly," not "cannot serve." |
| Biotech "NewCo" banking | Real post-SVB orphan, but **filled** (JPMorgan, Citi, Mercury, Brex + a venture-debt boom). |
| Agent payment *rails* / wallets | Genuine crux but crowded (Coinbase, Mastercard, Visa, Stripe, Meow). The orphan is the *liability/dispute* layer behind the rail (idea #1), not the rail. |
| Creator card / creator banking | Crux is real but closing fast (Karat, Visa+Lumanu, Willa, CreatorFi) — contested, not orphaned. |
| MiCA stablecoin compliance | Only ~19 authorized EMT issuers, already bank-grade — effectively closed. |
| AI-native accounting / usage-based rev-rec | Incumbents-add-a-feature (Campfire, Puzzle, Numeric already ship it). |

---

## Bottom line

If you want **one** idea with the tightest Brex fit — a brand-new class of customer that the
incumbent's model *cannot represent*, a market measured in trillions, and a structurally-hard
layer the only-possible-incumbents have *publicly declined to build* — it is:

> **The identity, underwriting, and dispute/liability rail for the AI agent economy** — and within
> it, the sharpest, most-open wedge is the **post-transaction dispute & recourse layer for
> agent-initiated commerce**, because the card networks turned on agent *payments* in 2026 while
> deliberately leaving agent *disputes* unbuilt, and their 40-year-old human-authorizer rules
> system structurally cannot adjudicate a non-human buyer.

If that is too early-stage or too platform-risk-exposed for the appetite, the cleanest *pure*
structural locks with nearer-term revenue are **#2 (AI liability insurance — incumbents are
literally writing the exclusion)** and **#3 (per-dose cell/gene-therapy acquisition financing —
the cash goes out before any receivable exists, so factoring is structurally blocked)**.

---

*Methodology note: figures are drawn from a swarm of agents that verified claims against live 2026
web sources and flagged confidence levels; market sizes from analyst/industry forecasts should be
treated as directional, not audited. Regulatory dates (esp. the EU AI Act Digital Omnibus and CMMC
rollout phases) were in flux as of June 2026 and should be re-confirmed before any decision. Full
per-domain findings, with inline source URLs, were generated by the research agents that produced
this synthesis.*
