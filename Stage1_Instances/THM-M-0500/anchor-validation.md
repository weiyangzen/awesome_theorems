# Anchor audit validation

The audit found an exact candidate in the already pinned mathlib checkout:
`Nat.infinite_setOf_prime_and_eq_mod` at revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Its conclusion is the canonical target after
introducing the four frozen binders. `AnchorAudit.lean` checks that relationship directly, without
an encoding transport, and Lean reports only `propext`, `Classical.choice`, and `Quot.sound` for
both the upstream theorem and the audit wrapper.

The upstream file is `Mathlib/NumberTheory/LSeries/PrimesInAP.lean` (SHA-256
`d99edfb234cc2c044332951a16f32bbfad58c8c73cc51faf4e9219d3bc6684c2`). The terminal theorem body
reduces finite support of the prime-residue-class summand to a contradiction with
`ArithmeticFunction.vonMangoldt.not_summable_residueClass_prime_div`; this is a real proof body,
not the deprecated alias or unbounded-form wrapper. Full transitive declaration/trust closure is
intentionally deferred to the obligation-tree and validation phases.

Public LeanSearch queries returned the same mathlib theorem family. Anonymous GitHub repository
searches found no separate project for two queries, after which the shared anonymous rate limit was
exhausted; code search also required authentication. These failures and response hashes are kept in
`anchor-audit.json`. Accordingly, the external negative result is bounded and access-limited, not
an exhaustive-discovery claim.

## Commands and results

Base revision: `e9d545372b66f73be63271b2fb408ef134d1d6f7`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0500` | 0 | rank 877; planned; theorem completion false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0500/AnchorAudit.lean` | 0 | exact candidate wrapper elaborated; upstream type/body and both axiom sets printed |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned commit and tree match the audit record |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; dependency checkout unchanged |
| `sha256sum .../PrimesInAP.lean .../mathlib/LICENSE` | 0 | source and license hashes match the audit record |
| `python3 -m json.tool Stage1_Instances/THM-M-0500/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0500` | 0 | no whitespace errors |

The clone's untracked `Formalizations/Lean/.lake` link to canonical pinned artifacts was used
read-only. No Lake update/build, fetch, clone, or dependency mutation was performed.

## Boundary

This is a self-tested anchor-audit node pending master acceptance. The exact upstream closure is a
later proof-integration candidate, not proof-phase credit here. Root state remains `[H1, M3, R4]`;
`audit_complete` and `theorem_complete` remain false.
