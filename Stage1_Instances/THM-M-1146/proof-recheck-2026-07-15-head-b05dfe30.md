# THM-M-1146 proof recheck at `b05dfe30`

Item: `S56-M-1146-PROOF`

Date: `2026-07-15`

Base revision: `b05dfe30bf9c4067039b9414912ec94f3153bb0b`

## Verdict

`blocked`. The exact frozen target remains open. The existing proof bodies were replayed from
fresh temporary outputs at trust level zero. They still close Laplacian/conjugation preservation
and the two strict off-axis branches without placeholders, but they do not prove harmonicity at a
point of the real axis. The conditional composer still consumes the unproved
`ReflectedHarmonicPackage`.

The first failed gate is `M1146-L-GLUING`. At an axis point, mathlib's `HarmonicAt` requires a
two-times continuously differentiable germ and a locally vanishing classical Laplacian. The frozen
hypotheses supply harmonicity only on the strict upper side and continuity up to the axis. Those
facts do not close `HarmonicAt` by definition or by an available pinned theorem.

No `.stage1-worker-selftest.json` was written. This proof phase is not complete, the root remains
`M3`, no new obligation was closed, and the immediate root cut remains `M1146-B-MERGE`.

## Route Audit

The current pinned API still has only ingredients for a new proof:

- `HarmonicOnNhd.exists_analyticOnNhd_ball_re_eq` requires harmonicity on a full open ball. It
  cannot produce the needed holomorphic representative on a half-ball touching the axis.
- `HasDerivAt.conj_conj` supports reflection after a holomorphic representative has been built.
- `IsConservativeOn.isExactOn_ball` supplies Morera on a disk, but applying it would require a new
  theorem splitting every rectangle at `im = 0` and proving the reflected boundary integrals
  cancel.
- `integral_boundary_rect_eq_zero_of_differentiable_on_off_countable` cannot discard the
  uncountable real-axis segment.
- The harmonic mean-value and Poisson results are forward implications; no converse mean-value or
  harmonic axis-gluing theorem is present.

Repository-local Poisson and weak-maximum-principle developments live in other targets' owned
paths and provide no eligible terminal bridge here. Even if independently reproduced, a Poisson
route would still require a new semidisk uniqueness theorem and substantial frontier/topology
bookkeeping. A scoped repository and pinned-mathlib search found no exact Schwarz-reflection or
harmonic-gluing declaration.

## Validation

All Lean checks reused the automation-provided pinned `.lake` artifacts read-only. No Lake update,
Lake build, dependency clone/fetch, network access, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, passed |
| `python3 scripts/stage1_target.py show THM-M-1146` | 0 | Rank 351; planned; L0/rework-required; theorem incomplete |
| `timeout 900 env LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-1146/check_statement.py` | 0 | Exact expression hash `14336b88...deef53d`; five mutations killed |
| `python3 Stage1_Instances/THM-M-1146/check_obligation_tree.py` | 0 | 18 obligations and 40 typed edges passed; root open M3 |
| isolated `lake env lean --trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` | 0 | All elaborated; printed axioms were only `propext`, `Classical.choice`, and `Quot.sound` |
| prohibited-construct scan over owned Lean files | 1 | Expected no-match exit; no placeholder, bodyless axiom, unsafe/oracle, or native shortcut found |
| scoped repository and pinned-mathlib route searches | 0 | Route fragments found, but no terminal axis-gluing or exact reflection candidate |
| `python3 -m json.tool Stage1_Instances/THM-M-1146/proof-recheck-2026-07-15-head-b05dfe30.json` | 0 | Current-base blocker JSON valid |
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
