# THM-M-1146 proof recheck at `6bf9ee93` (slot29)

Item: `S56-M-1146-PROOF`

Recorded at: `2026-07-16T04:58:23+08:00`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

## Verdict

`blocked`. The exact frozen Schwarz-reflection root remains open at real-axis harmonic gluing,
`M1146-L-GLUING`. The existing checked bodies prove preservation under complex conjugation, both
strict off-axis harmonic branches, continuity of the odd reflection on the symmetric domain, and
conditional composition from an axis proof. They do not prove `HarmonicAt` when `z.im = 0`.

At an axis point, pinned mathlib's `HarmonicAt` requires a `ContDiffAt Real 2` germ and an
eventually zero classical Laplacian. The frozen hypotheses provide one-sided harmonicity,
continuity through the axis, and zero boundary trace. Obtaining the required germ is a substantive
Schwarz-reflection/gluing theorem, not a definitional simplification or local tactic gap.

No `.stage1-worker-selftest.json` was written. The assigned proof phase stays `[ ]`, the root stays
`[H3, M3, R3]`, no new obligation is closed, and theorem completion is false.

## Dependency Audit

The new `dependency-reuse-ledger.json` uses schema `stage1-dependency-reuse-ledger/1.1`, graph digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`, context digest
`7003836c7ea18486e9405d6d16a2c13b7c6f28cb6bba570b3be0c9d8bd43acfc`, and this exact base
revision. THM-M-1146 has no hard parent, ancestor, edge, or reuse hint. All three weak shared-module
groups were inspected and recorded `not_applicable`; there are no unresolved compatibility
obligations and no cross-target proof credit.

The scheduler's narrow ledger validator passed. Its SHA-256 is
`d23f6efd74674a8741b274155cd66ccdb0acf78e922d369c128597625a442d29`.

## Route Audit

Pinned mathlib provides forward harmonic mean-value and Poisson formulas, local holomorphic
representatives on full balls, Morera interfaces, off-countable Cauchy-Goursat, piecewise
continuity, and conjugation calculus. It provides no converse harmonic mean-value theorem,
harmonic axis-gluing theorem, or Schwarz-reflection theorem.

Pinned `Convex.exists_forall_hasDerivWithinAt` can construct a primitive of the harmonic complex
partial on a convex open upper half-ball, but current APIs do not provide its needed controlled
continuous boundary trace on the diameter. A cross-axis Morera proof would still require manual
rectangle split/cancellation across the uncountable real-axis segment; the off-countable theorem
cannot discard that segment. A Poisson/uniqueness route still needs a dependency-eligible,
provenance-cleared disk Dirichlet construction, harmonic uniqueness, and semidisk frontier
infrastructure. THM-M-1138/1140 are weak shared-group evidence only, not hard or reuse
dependencies, and their maximum-principle files were inspected and rejected for proof reuse. The
nearby THM-M-1148 Poisson development is outside this target's dependency context; its source also
has a restrictive unresolved provenance/license boundary. None can be silently imported, copied,
or credited here.

Two informal read-only worker assessments found no concise compilable route from current pinned
APIs. These guide the blocker classification but are not independent validation receipts. No
eligible root or axis body was found in current target sources or repository history.

## Validation

All Lean checks reused the automation-provided pinned `.lake` link read-only. Proof-replay outputs
were confined to `/tmp` and removed; the statement checker's temporary target-local sources were
also removed. No `lake update`, `lake build`, dependency clone/fetch, network request, or dependency
mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 1 | Failed because the checked-in v2 theorem DAG differs from fresh generation after the new structured JSON artifacts became visible to its evidence inventory. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | Same generated-inventory freshness failure. This worker is forbidden to edit that DAG. |
| Read-only in-memory deterministic DAG build and structural comparison | 0 | Only THM-M-1146 `evidence_inventory` differed: the new ledger and blocker JSON were added; nothing was removed and reusable artifacts were unchanged. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1146` | 0 | Rank 351; planned; L0/rework-required; theorem incomplete. |
| Scheduler `validate_dependency_reuse_ledger(...)` with exact graph/base assertions | 0 | Empty hard closure; three weak groups audited `not_applicable`; no unresolved obligations. |
| `timeout 900 env LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-1146/check_statement.py` | 0 | Exact expression hash `14336b88...deef53d`; all five structural mutations killed. |
| `python3 Stage1_Instances/THM-M-1146/check_obligation_tree.py` | 0 | 18 obligations and 40 typed edges passed; root open M3 and reflected package open M4. |
| Isolated `lake env lean --trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `ProofNext.lean` | 0 | All four modules elaborated; all printed bodies used only `propext`, `Classical.choice`, and `Quot.sound`; no diagnostics. |
| Prohibited-construct scan over target-owned Lean files | 1 | Expected no-match exit; no placeholder, bodyless axiom, unsafe/oracle, or native shortcut found. |
| Scoped pinned-mathlib source search and target-history/declaration searches | 0 | Found route ingredients, partial bodies, and conditional composers, but no eligible axis or root closure. |
| `python3 -m json.tool` on the new blocker JSON and dependency ledger | 0 | Both structured artifacts are valid JSON. |
| Added-file whitespace checks on the ledger and new JSON/Markdown pair | 1 | Expected added-file status for each file; no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest correctly absent. |

Environment: Lean `4.29.0` commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`;
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

Source SHA-256 values: `Statement.lean` `1eed1535...1bdf5dd`; `ObligationTree.lean`
`1c8ddbb8...01812e8`; `Proof.lean` `31c325c8...759d0c4`; `ProofNext.lean`
`019fc699...110f37`.

## Reopen Condition

Resume after a placeholder-free implementation of axis harmonic gluing and its boundary/locality
prerequisites, or an immutable compatible terminal proof whose exact type, dependency relation,
provenance, license, trust closure, and composition can be checked without dependency mutation.
The integration lane must also regenerate the theorem DAG inventory after merging the new
target-owned artifacts.

This packet is blocker evidence, not a proof receipt or a request for scheduler state promotion.
