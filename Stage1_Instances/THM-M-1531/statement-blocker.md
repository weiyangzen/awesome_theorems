# Exact-statement gate: blocked

Item: `S56-M-1531-STATEMENT`

## Decision

The accepted intake does not identify a unique mathematical theorem that can be frozen as the
exact Higgs-mechanism target. The repository source record supplies only the phrase "spontaneous
breaking of gauge symmetry." The intake's three primary-source candidates have not been inspected
at equation level, and the dossier deliberately leaves open the gauge group, representation,
spacetime and regularity regime, Lagrangian/potential, vacuum conditions, and mass conclusion.
Those choices materially change both the binders and the proposition.

In particular, the source phrase does not decide among existence of one massive gauge mode,
positivity on every broken infinitesimal direction, or a kernel/rank equality between a mass form
and the vacuum stabilizer. It also does not settle zero coupling, a trivial representation, an
empty broken sector, residual symmetry, or degenerate quadratic terms. Selecting one of these
without a pinpoint source crosswalk would invent missing mathematics and violate the rev-5.6 exact
statement gate.

The legacy `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_198.lean` cannot supply the target. Its
`HiggsMechanismData` contains both `vacuumBreaksSomeGaugeSymmetry` and `hasNonzeroMassMode` as input
fields, while its `HiggsMechanismConclusion` merely projects those facts. Treating that interface
wrapper as the Higgs mechanism would assume the desired conclusion rather than derive it.

## Lean boundary checked

`StatementProbe.lean` imports only `Mathlib.GroupTheory.GroupAction.Basic` and elaborates the
group-action definitions of an unbroken stabilizer and existence of a transformation moving the
vacuum. This is a substrate check only. It intentionally does not introduce uninterpreted mass
operators, arbitrary second-variation functions, or hypotheses containing a mass conclusion,
because those would produce a broadened or circular substitute rather than the exact theorem.

Repository and pinned-mathlib searches found no gauge-Higgs or spontaneous-symmetry-breaking
formalization. The only case-insensitive pinned-mathlib matches for "Higgs" concern the unrelated
matroid author/theorem name. The pinned mathlib revision is
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Validation record

Base revision: `e291daffd22e3ff6fc8031f413e88a1a41b1af26`.

Commands ran in this worker clone on 2026-07-12. Lean reused the existing pinned Lake environment;
no update, fetch, build, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1531/StatementProbe.lean` (from `Formalizations/Lean`) | 0 | group action, unbroken-set membership, broken-symmetry predicate, and identity membership elaborated |
| `lake env lean --version` (from `Formalizations/Lean`) | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `rg -n -i 'Higgs|spontaneous symmetry|symmetry breaking|gauge boson' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/.lake/packages/mathlib/Archive --glob '*.lean'` | 0 | two unrelated matroid matches; no gauge-Higgs statement API |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1531` | 0 | rank 198, planned, L0/rework-required, theorem incomplete |
| `rg -n '[ \t]+$' Stage1_Instances/THM-M-1531/StatementProbe.lean Stage1_Instances/THM-M-1531/statement-blocker.md` | 1 | no trailing-whitespace match (expected no-match exit) |

## Gate result and retry condition

First failed gate: rev-5.6 section 5 exact canonical statement identity. Machine status remains
`M4`; no canonical expression, expression fingerprint, checked alternate transport, or meaningful
mutation suite is claimed.

Retry only after an authoritative stable source is inspected and one exact model/result is approved
with equation/page, assumptions, conventions, boundary cases, and a row-level source-to-Lean
crosswalk. The resulting mass form must be derived from the selected representation, covariant
kinetic term, and vacuum rather than supplied together with the desired spectral conclusion.

No `.stage1-worker-selftest.json` is emitted because the assigned statement phase is blocked, not
self-tested complete. This record does not advance anchor-audit, obligation-tree, proof,
validation, release, audit-completion, or theorem-completion state.
