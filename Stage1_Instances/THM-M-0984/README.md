# THM-M-0984 rev-5.6 intake

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

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`

Only `INTAKE` is addressed here. Master acceptance is still required before
the dependent statement task becomes eligible.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first
failed theorem gate is the exact source/statement identity gate: the source
row is too terse to prove that the legacy iid Banach-valued formalization is
the intended Borel theorem. Even after that is resolved, the Lean expression
hash, environment fingerprint, checked transports, and mutations remain open.
The theorem is not complete.

## Validation

On base revision `c6aa0f2ba41dd389c2bcf01dd532923615781719`, the commands in
`validation.md` establish target membership, standard consistency, JSON
syntax, and dossier-local integrity only. No Lean proof result is claimed.
