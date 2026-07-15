# THM-M-1146 proof recheck at `557b928b`

Item: `S56-M-1146-PROOF`

Date: `2026-07-15`

Base revision: `557b928b377b386864527c9fb4831d45857837aa`

## Verdict

`blocked`. The exact target remains open. This current-base recheck supersedes the freshness of
`proof-recheck-2026-07-15-head-195f312e.*`; the Lean sources and frozen proof architecture have not
changed since that packet, so it records no new proof body or closed obligation.

The existing bodies re-elaborate at trust level zero and close conjugation preservation plus both
strict off-axis branches. They do not prove harmonicity at a point on the real axis. The conditional
composer still consumes the unproved `ReflectedHarmonicPackage`.

The first failed gate remains `M1146-L-GLUING`. At an axis point, mathlib's `HarmonicAt` requires a
two-times continuously differentiable germ and a locally vanishing classical Laplacian. The frozen
hypotheses provide harmonicity only on the strict upper side and continuity up to the axis. They do
not close `HarmonicAt` definitionally.

No `.stage1-worker-selftest.json` was written: this proof phase is incomplete, the root remains
`M3`, and the immediate root cut remains `M1146-B-MERGE`.

## Route Audit

The unchanged pinned environment contains complex-partial analyticity, convex primitive and Morera
interfaces, holomorphic conjugation, piecewise continuity, and forward mean-value and Poisson
formulas. It still has no real-axis Schwarz-reflection theorem, harmonic axis-gluing theorem,
converse mean-value result, or applicable weak-to-classical regularity theorem.

The shortest visible analytic route is still a substantial development: construct a holomorphic
primitive on an upper half-ball with a controlled real boundary trace, reflect it, establish
continuity on a full ball, split every Morera rectangle at the real axis, prove the two boundary
integrals cancel, and transfer the resulting analytic real part back to `oddReflection`. The
off-countable Cauchy-Goursat theorem cannot discard the uncountable axis segment. Isolated removable
singularity lemmas do not remove a line. No terminal repo-local or compatible immutable external
Lean proof was found.

Nearby Poisson and weak maximum-principle bodies belong to other targets. Even as read-only route
leads, they do not supply the missing uniqueness, semidisk frontier, or axis-gluing package, and
therefore receive no proof credit here.

## Validation

All checks used the existing pinned Lean artifacts read-only. No Lake update/build, dependency
clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, passed |
| `python3 scripts/stage1_target.py show THM-M-1146` | 0 | Rank 351; planned; L0/rework-required; theorem incomplete |
| `timeout 900 env LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-1146/check_statement.py` | 0 | Exact expression hash `14336b88...deef53d`; five mutations killed |
| `python3 Stage1_Instances/THM-M-1146/check_obligation_tree.py` | 0 | 18 obligations and 40 typed edges passed; root open M3 |
| isolated `lake env lean --trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` | 0 | All elaborated; printed axioms were only `propext`, `Classical.choice`, and `Quot.sound` |
| prohibited-construct scan over owned Lean files | 1 | Expected no-match exit; no placeholder, bodyless axiom, unsafe/oracle, or native shortcut found |
| unchanged-route audit against repo-local and pinned mathlib sources | 0 | Route ingredients only; no terminal axis-gluing or exact reflection declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1146/proof-recheck-2026-07-15-head-557b928b.json` | 0 | Current-base blocker JSON valid |
| added-file whitespace checks for this Markdown and JSON pair | 1 | Expected added-file status; no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest correctly absent |

Environment: Lean `4.29.0` commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`;
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Reopen Condition

Resume after a placeholder-free implementation of `M1146-L-GLUING` and its boundary/locality
prerequisites, or after locating an immutable compatible terminal Lean 4 proof that can be pinned,
exact-type transported, and checked without dependency mutation. This packet is blocker evidence,
not a proof receipt or a request for scheduler promotion.
