# THM-M-1146 proof recheck at `47111bb1`

Item: `S56-M-1146-PROOF`

Date: `2026-07-15`

Base revision: `47111bb19566742918ac6be4a1a454070335b4a3`

## Verdict

`blocked`. The exact frozen Schwarz-reflection root remains open at the real-axis harmonic-gluing
obligation `M1146-L-GLUING`. The current checked bodies prove preservation under conjugation, the
two strict off-axis harmonic branches, continuity of the odd reflection on the symmetric domain,
and conditional composition of an axis proof. They do not prove `HarmonicAt` on the axis.

This current-base attempt found no new eligible proof body in the target history, available worker
copies, or pinned mathlib tree. At an axis point, mathlib's `HarmonicAt` requires a
`ContDiffAt Real 2` germ and an eventually zero classical Laplacian. The frozen hypotheses supply
only one-sided harmonicity, continuity through the axis, and a zero trace. Those facts do not close
the required germ definitionally.

No `.stage1-worker-selftest.json` was written. The assigned proof phase is incomplete, the root
remains `M3`, and theorem completion is false.

## Route Audit

Pinned mathlib provides the forward harmonic mean-value theorem, local holomorphic representatives
for functions harmonic on a full ball, Morera interfaces, off-countable Cauchy-Goursat, and
reflection calculus. It provides no converse harmonic mean-value theorem, harmonic axis-gluing
theorem, or Schwarz-reflection theorem.

A real Morera route still needs a holomorphic representative on an upper half-ball with a
controlled boundary trace and a proof that arbitrary rectangle integrals cancel after splitting at
the uncountable real-axis segment. The off-countable theorem cannot discard that segment. A
Poisson/maximum-principle route still needs a license-clean disk Dirichlet construction, uniqueness,
and semidisk frontier infrastructure. The nearby target-local Poisson development has a restrictive
provenance boundary and cannot be silently credited here.

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
| scoped target-history, worker-copy, and pinned-mathlib route audit | 0 | Existing proof sources are unchanged; only forward mean-value route ingredients were found, with no eligible axis or root closure |
| `python3 -m json.tool Stage1_Instances/THM-M-1146/proof-recheck-2026-07-15-head-47111bb1.json` | 0 | Current-base blocker JSON is valid |
| scoped whitespace checks for this Markdown/JSON pair | 1 | Expected added-file status; no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest correctly absent |

Environment: Lean `4.29.0` commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`;
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

Source hashes: `Statement.lean` `1eed1535...1bdf5dd`; `ObligationTree.lean`
`1c8ddbb8...01812e8`; `Proof.lean` `31c325c8...759d0c4`; `ProofNext.lean`
`019fc699...110f37`.

## Reopen Condition

Resume after a placeholder-free implementation of axis harmonic gluing and its boundary/locality
prerequisites, or an immutable compatible terminal proof whose exact type, provenance, license,
trust closure, and composition can be checked without dependency mutation. This packet is blocker
evidence, not a proof receipt or a request for scheduler promotion.
