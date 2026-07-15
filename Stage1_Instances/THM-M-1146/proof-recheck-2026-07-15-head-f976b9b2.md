# THM-M-1146 proof recheck at `f976b9b2`

Item: `S56-M-1146-PROOF`

Date: `2026-07-15`

Base revision: `f976b9b21418bfda4bc815ba2a7238e932666231`

## Verdict

`blocked`. The exact frozen Schwarz-reflection root remains open at the real-axis harmonic-gluing
obligation `M1146-L-GLUING`. The checked sources prove conjugation preservation, both strict
off-axis harmonic branches, continuity of the odd reflection on the symmetric domain, and
conditional composition of an axis proof. They do not prove `HarmonicAt` at an axis point.

At such a point, mathlib's `HarmonicAt` requires a `ContDiffAt Real 2` germ and an eventually zero
classical Laplacian. The frozen hypotheses provide upper-side harmonicity, continuity through the
axis, and zero boundary trace. These facts do not produce that germ definitionally.

No `.stage1-worker-selftest.json` was written. The proof phase is incomplete, the root remains
`M3`, and theorem completion is false.

## Route Audit

Pinned mathlib has a viable but substantial Morera route. On a strict upper half-ball,
`HarmonicAt.differentiableAt_complex_partial` and
`Convex.exists_forall_hasDerivWithinAt` can construct a holomorphic representative. However, its
imaginary-part boundary trace still needs a new limiting/tangential-derivative argument. After
reflecting that representative, `Complex.isConservativeOn_and_continuousOn_iff_isDifferentiableOn`
would require manually splitting every crossing rectangle with
`intervalIntegral.integral_add_adjacent_intervals` and cancelling the shared axis integral. The
off-countable Cauchy-Goursat theorem cannot discard the uncountable real-axis segment.

No packaged upper-half-ball representative, boundary reflection, harmonic gluing, converse
harmonic mean-value theorem, or Schwarz-reflection theorem was found. The alternative local
Dirichlet route needs a clean Poisson existence theorem plus maximum-principle uniqueness and
semidisk frontier infrastructure. The nearby target-local Poisson development belongs to another
owned path and has a restrictive provenance boundary, so it cannot be credited or copied here.

## Validation

All Lean checks reused the automation-provided pinned `.lake` link read-only. No Lake update/build,
dependency clone/fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, passed |
| `python3 scripts/stage1_target.py show THM-M-1146` | 0 | Rank 351; planned; L0/rework-required; theorem incomplete |
| `timeout 900 env LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-1146/check_statement.py` | 0 | Exact expression hash `14336b88...deef53d`; all five mutations killed |
| `python3 Stage1_Instances/THM-M-1146/check_obligation_tree.py` | 0 | 18 obligations and 40 typed edges passed; root open M3 and reflected package open M4 |
| isolated `lake env lean --trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `ProofNext.lean` | 0 | All four modules elaborated from fresh temporary outputs; every printed body used only `propext`, `Classical.choice`, and `Quot.sound` |
| prohibited-construct scan over owned Lean files | 1 | Expected no-match exit; no placeholder, bodyless axiom, unsafe/oracle, or native shortcut found |
| scoped pinned-mathlib and repository route audit | 0 | Route ingredients found, but no eligible axis or root closure |
| `python3 -m json.tool Stage1_Instances/THM-M-1146/proof-recheck-2026-07-15-head-f976b9b2.json` | 0 | Structured blocker record valid |
| `git diff --check -- Stage1_Instances/THM-M-1146` | 0 | No whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest correctly absent |

Environment: Lean `4.29.0` commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`;
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Reopen Condition

Resume after a placeholder-free implementation of axis harmonic gluing and its boundary/locality
prerequisites, or an immutable compatible terminal proof whose exact type, provenance, license,
trust closure, and composition can be checked without dependency mutation. This is blocker
evidence, not a proof receipt or a request for scheduler promotion.
