# THM-M-0984 rev-5.6 dossier

This directory is the rev-5.6 `planned` instance for the strong law of large
numbers. The repository source row says only "Borel, 1909" and "almost-sure
convergence". That wording does not uniquely select a modern strong-law
variant. The intake therefore records the existing iid integrable mathlib
target as provisional and preserves the historical Borel/Bernoulli
interpretation as an unresolved scope question rather than silently treating
the two as identical.

## Scope map

| Surface | Provisional in-scope object | Intake boundary |
|---|---|---|
| Historical root | Borel's 1909 almost-sure frequency result | Exact publication, theorem, language, and hypotheses require primary-source audit |
| Modern candidate root | Pairwise-independent, identically distributed, integrable Banach-valued random variables; empirical averages converge almost surely to the expectation | This is a candidate normalization, not yet a checked interpretation of the terse source row |
| Domains | Measurable sample space, complete real normed target with Borel structure, arbitrary measure | Exact universe and typeclass serialization belongs to statement phase |
| Statement layer | Bundled data, explicit hypotheses, real-valued specialization, and Bernoulli specialization | No transport or equivalence receives credit at intake |
| Boundary cases | `n = 0`, degenerate measure, a.e.-zero variables, Bernoulli parameters at 0 and 1 | Must be tested after the canonical interpretation is selected |
| Proof architecture | measurability/integrability, independence, identical distribution, truncation/maximal estimates, almost-sure convergence, transport to root | Seed only; the frozen obligation registry belongs to a later phase |
| Formal candidate | `ProbabilityTheory.strong_law_ae` and the legacy local `S1_M_264.StatementShape` | Existing code is discovery input only and carries no rev-5.6 proof credit |
| Excluded variants | non-iid Kolmogorov criteria, martingale, triangular-array, and ergodic strong laws | Not interchangeable with the provisional root without a checked relationship |

The structured domains, binders, hypotheses, conclusion, boundary cases, and
profiles are in `intake.json`. The source-to-statement uncertainty and the
required resolution are in `source_statement_crosswalk.md`.

## Statement artifact

`Statement.lean` freezes and elaborates the intake-selected modern iid
integrable target using only `Mathlib.Probability.StrongLaw`. The explicit
target and bundled `StrongLawData` form have a checked iff; four structural
mutations are distinguished and the zero-index and zero-sequence boundaries
are kernel checked. Exact fingerprints and replay commands are recorded in
`statement.json` and `statement-validation.md`.

This statement result does not resolve the source-identity issue. In
particular, it does not claim that the modern Banach-valued theorem is the
exact historical Borel 1909 frequency theorem.

## Anchor audit

`AnchorAudit.lean` kernel-checks the exact frozen modern target through pinned
mathlib declaration `ProbabilityTheory.strong_law_ae` at revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The candidate and provenance
ledger is in `anchor-audit.json`, with exact commands and limitations in
`anchor-audit-validation.md`. This classifies the modern machine candidate as
`M0-W`; it does not upgrade the historical source crosswalk or complete later
rev-5.6 gates.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`

`INTAKE`, `STATEMENT`, and `ANCHOR_AUDIT` have provisional master state `[_]`.
`OBLIGATION_TREE` is now worker self-tested and awaits master acceptance. All
later phases remain open.

## Obligation architecture

`obligation-registry.json` freezes ten stable obligations and denominator
`7869ad0637404b744050b4cf6ded4d80ae7403c59158fea2f9aea2b8f48a1d92`.
`typed-graphs.json` separates proof, refinement, provenance, evidence, trust,
documentation, and workflow edges. `ObligationTree.lean` kernel-checks the
child-to-parent composition while deliberately retaining the deep exact
strong-law theorem as an explicit premise. No obligation is marked closed;
`M0984-L-TERMINAL` remains the proof cut set, and source identity remains H1.

## Intake verdict

Lifecycle remains `planned`; provisional root vector is `[H1, M0-W, R3]` for
the frozen modern target. The pinned mathlib theorem supplies its exact
machine body, but the first failed theorem gate remains source identity: the
source row is too terse to prove that this iid Banach-valued formalization is
the intended Borel theorem. Proof, validation, readability, and release gates
also remain open. The theorem is not complete.

## Validation

On base revision `c6aa0f2ba41dd389c2bcf01dd532923615781719`, the commands in
`validation.md` establish target membership, standard consistency, JSON
syntax, and dossier-local integrity only. No Lean proof result is claimed.
