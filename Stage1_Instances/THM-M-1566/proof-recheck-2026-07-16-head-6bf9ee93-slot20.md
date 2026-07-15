# THM-M-1566 proof-phase recheck at base 6bf9ee93

Item: `S56-M-1566-PROOF`

Recorded at: `2026-07-16T04:40:03+08:00`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

## Verdict

`blocked`. No consistent positive proof body can inhabit the exact frozen Lean
target. The unchanged, placeholder-free kernel declaration

```text
Stage1Instances.THMM1566.not_GIPCorollary59Target :
  Not (Stage1Instances.THMM1566.GIPCorollary59Target.{0})
```

was replayed against the existing pinned Lean and mathlib objects. Its model
sets `Omega := Unit`, uses the Dirac probability measure, takes every
non-solution carrier to be `Unit`, and takes `Solution := Empty`. The numerical
premises are inhabited at `alpha = beta = 3/4`. Applying the positive target
therefore supplies an inhabitant of `Empty`.

This refutes the frozen abstract encoding, not Corollary 5.9 in the cited
Gubinelli-Imkeller-Perkowski paper. Adding only `Nonempty api.Solution` would
not repair it because another universally quantified API can interpret
`solvesLimitEquation` as false. Repair requires a concrete source-faithful
semantics or substantive noncircular adequacy hypotheses, followed by a new
statement fingerprint and refrozen downstream artifacts.

The new `dependency-reuse-ledger.json` records the required v2 context before
proof work. The supplied graph digest and target context agree exactly. There
are no hard parents, transitive hard ancestors, reuse hints, or shared groups,
so the audited inspections and decisions are empty. This is not a mathematical
independence claim and transfers no proof credit.

The conditional theorem `root_of_existence_and_uniqueness` remains a valid
placeholder-free assembler, but it consumes the open existence and uniqueness
packages and cannot close the root. No positive body or proof receipt was
added. The item remains `[ ]`; `.stage1-worker-selftest.json` is deliberately
absent.

## Validation

All commands ran in this worker clone. The pre-existing automation-provided
`Formalizations/Lean/.lake` symlink was reused without update, build, clone,
fetch, network access, or dependency mutation. Lean outputs were confined to a
fresh `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | The checked-in DAG differs from fresh deterministic generation because the mandatory ledger is excluded from relationship discovery but enters the generated evidence inventory. The authoritative DAG was not edited and still hashes to `73e99d22...0eca`; the integration lane must regenerate this protected projection. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1566` | 0 | Rank 182, planned lifecycle, theorem incomplete. |
| Inline `validate_dependency_reuse_ledger(...)` with the supplied graph digest and base revision | 0 | Context `068170c7...c5c`, zero inspections, zero decisions, and no unresolved compatibility obligation passed. |
| `python3 Stage1_Instances/THM-M-1566/check_anchor_audit.py` | 0 | Four candidates, four searches, five Lean probes, and the M4 boundary agree. |
| `python3 Stage1_Instances/THM-M-1566/check_obligation_tree.py` | 0 | 15 obligations and 40 typed edges pass; denominator `7ae15c07...3fe640`; root remains open M4. |
| Isolated pinned `lake env lean` replay of `Statement.lean` and `ProofCountermodel.lean` under `/tmp` | 0, 0 | `not_GIPCorollary59Target` elaborates and reports only `propext`, `Classical.choice`, and `Quot.sound`; statement object SHA-256 `1e1c07a6...32793`. |
| `rg -n '\b(sorry\|admit\|sorryAx\|native_decide\|implemented_by)\b\|^[[:space:]]*(axiom\|opaque\|constant\|unsafe\|external)[[:space:]]' Stage1_Instances/THM-M-1566 --glob '*.lean'` | 1 | Expected no-match; no prohibited proof escape appears in the owned Lean sources. |
| `python3 -m json.tool` on both new JSON records | 0 | Both structured artifacts parse. |
| `git diff --check -- Stage1_Instances/THM-M-1566` | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false completion handoff was emitted. |

The aggregate `check_stage1_standard.py` invokes the currently failing v2 DAG
validator and the repository-wide cron test suite. It was stopped after that
prerequisite failure and is not claimed as successful proof evidence.

## Status Boundary

The first failed proof gate is positive exact-root kernel closure at
`M1566-ROOT`, originating in unconstrained `M1566-S-INTERFACE` and directly
refuting `M1566-T-EXISTENCE`. The actionable cut set is statement/interface,
existence, and root. `root_closed=false`, `audit_complete=false`, and
`theorem_complete=false`; there is no accepted receipt or provisional state.

More than five unresolved proof rechecks exist. Identical proof-lane retries
should stop. The master must reopen the statement/interface prerequisite,
repair the target, and refreeze downstream evidence before proof resumes.
