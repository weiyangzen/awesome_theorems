# THM-M-1146 proof recheck at `e27b85e1`

Item: `S56-M-1146-PROOF`  
Date: `2026-07-15`  
Base revision: `e27b85e1503047c5e4bd8d5410b6fba5c4dda896`

## Verdict

`blocked`. The exact target remains open. The existing `Proof.lean` bodies were re-elaborated at
trust level zero and still close conjugation preservation plus both strict off-axis branches. They
do not prove harmonicity at a point on the real axis, and the conditional composer still consumes
the unproved `ReflectedHarmonicPackage`.

The first failed gate is `M1146-L-GLUING`. At an axis point, mathlib's `HarmonicAt` requires a
two-times continuously differentiable germ and a locally vanishing classical Laplacian. The frozen
hypotheses give harmonicity only on the strict upper side and continuity up to the axis. These facts
do not close `HarmonicAt` definitionally.

No `.stage1-worker-selftest.json` was written: this proof phase is not complete, the root remains
`M3`, no new obligation was closed, and the immediate root cut remains `M1146-B-MERGE`.

## Route Audit

Pinned mathlib contains useful fragments: local analytic representatives for harmonic functions on
full balls, holomorphic conjugation calculus, Morera interfaces, piecewise continuity, and forward
mean-value and Poisson formulas. It does not contain a half-ball primitive, rectangle splitting and
cancellation across the axis, a converse mean-value theorem, a harmonic gluing theorem, a real-axis
Schwarz reflection theorem, or applicable distributional regularity.

A new Morera route would need to construct a holomorphic representative on an upper half-ball,
reflect it, prove the piecewise function continuous on a full ball, split arbitrary rectangles at
the axis, establish reflected interval-integral identities and cancellation, and transport the real
part back to harmonicity. The available APIs supply pieces of that development, not the decisive
axis-gluing result. The off-countable Cauchy-Goursat theorem does not apply to the uncountable real
axis.

Nearby Poisson bodies under `THM-M-1148` and a weak maximum principle under `THM-M-1138` belong to
other targets' owned paths and cannot receive proof credit here. They also do not provide an
eligible uniqueness or axis-gluing bridge. No compatible immutable external Lean 4 terminal proof
was found.

## Validation

All checks used the existing pinned Lean artifacts read-only. No Lake update/build, dependency
clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, passed |
| `python3 scripts/stage1_target.py show THM-M-1146` | 0 | Rank 351; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1146/check_statement.py` | 0 | Exact expression hash `14336b88...deef53d`; five mutations killed |
| `python3 Stage1_Instances/THM-M-1146/check_obligation_tree.py` | 0 | 18 obligations and 40 typed edges passed; root open M3 |
| isolated `lake env lean --trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` | 0 | All elaborated; printed axioms were only `propext`, `Classical.choice`, and `Quot.sound` |
| prohibited-construct scan over owned Lean files | 1 | Expected no-match exit; no placeholder, bodyless axiom, unsafe/oracle, or native shortcut found |
| scoped repository and pinned-mathlib route searches | 0 | Route fragments found, but no terminal axis-gluing or exact reflection candidate |
| `python3 -m json.tool Stage1_Instances/THM-M-1146/proof-recheck-2026-07-15-head-e27b85e1.json` | 0 | Current-base blocker JSON valid |
| `git diff --check -- Stage1_Instances/THM-M-1146` | 0 | No whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest correctly absent |

Environment: Lean `4.29.0` commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`;
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Reopen Condition

Resume after a placeholder-free implementation of `M1146-L-GLUING` and its continuity/locality
prerequisites, or after locating an immutable compatible terminal Lean 4 proof that can be pinned,
exact-type transported, and checked without dependency mutation. This recheck is blocker evidence,
not a proof receipt or a request for scheduler promotion.
