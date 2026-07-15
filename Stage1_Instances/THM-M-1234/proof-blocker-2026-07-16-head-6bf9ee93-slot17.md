# THM-M-1234 proof-phase current-base blocker

Item: `S56-M-1234-PROOF`. Phase: `proof`. Base revision:
`6bf9ee93a322e7d25cf9249226222095f95d1cff`.

## Verdict

`blocked`. The exact target is

```lean
Stage1Rev56.THMM1234.Statement :=
  forall (u0 : StaticVelocity) (omega0 : StaticVorticity),
    InitialData u0 omega0 -> Nonempty (GlobalWeakSolution u0 omega0)
```

No repo-local or pinned declaration proves this universal whole-plane
Yudovich existence statement. A fresh trust-zero replay confirms only the
existing conditional assembly, the deliberately weak constant-in-time
candidate construction, its trace, the zero-data special case, and the
closure-package diagnostics. The exact root remains open.

The frozen predecessor architecture cannot support a truthful positive proof
handoff. `CandidateConstructionPackage` does not consume the approximation,
energy, or compactness children. `EquationAndTraceClosurePackage` quantifies
over every structural candidate rather than the candidate obtained from the
construction. In particular, the checked zero-candidate diagnostics show that
this closure premise would force every admissible initial-velocity pairing and
initial-vorticity test pairing to vanish. It therefore is not a usable closure
theorem for arbitrary nonzero data.

The predecessor is only worker-provisional `[_]`. Its typed graph names
`M1234-ROOT` as a root node although its node list contains
`THM-M-1234-ROOT`, and all 14 validation entries are shell-string aliases
rather than the required structured recipes. These are predecessor repairs,
not proof-phase changes that this worker may silently rewrite.

The required v2 dependency/reuse audit is now recorded in
`dependency-reuse-ledger.json`. The target has no direct parents, transitive
ancestors, hard edges, reuse hints, or shared groups, so the audited closure,
inspection set, and decision set are all empty. The ledger is bound to graph
SHA-256 `73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`
and context SHA-256
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

No `.stage1-worker-selftest.json` exists because the positive proof phase did
not pass. This artifact is blocker evidence, not a proof receipt, and changes
no scheduler state.

## Validation

All Lean commands used the existing pinned `.lake` artifacts read-only. No
`lake update`, `lake build`, dependency clone/fetch, or dependency mutation was
run. Generated Lean artifacts were confined to a fresh `/tmp` directory and
removed after replay.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 1 | Fail-closed: the checked-in v2 theorem DAG differs from fresh generation solely because the newly required ledger is included in `structured_json_files`; graph discovery itself excludes this ledger. This is a global validator/inventory incompatibility, not proof evidence. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | Same deterministic-inventory mismatch after writing the mandatory ledger. Before the ledger was added, the checker passed for 1546 theorems, 10822 preserved states, 2 hard edges, 5 hints, 310 groups, and acyclicity. |
| `python3 scripts/stage1_execution_cron.py --validate-only --workers 0` | 1 | Fail-closed at the same v2 deterministic-inventory check; no scheduler state was modified. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546; all remain L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | Rank 158, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges parsed; denominator `cfa0a02c68993c8b3eefc0edfe7d3d7bd20e2b58d140f47a1f5444a8ba734c5d`; root open M3 and analytic packages open M4. |
| Schema-1.1 ledger validation through `scripts/stage1_execution_cron.py` | 0 | Exact graph/context/base binding passed; 0 inspections and 0 reuse decisions match the empty v2 closure. |
| Fresh isolated `lake env lean` executable with `--trust=0 -t0` over all six target Lean modules | 0 | All modules elaborated. Printed declarations depend only on `propext`, `Classical.choice`, and `Quot.sound`. |
| Scoped prohibited-token scan over target Lean sources | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, unsafe/oracle/extern/native escape, or related placeholder device. |
| Exact-topic scan over 9,676 pinned package Lean files | 1 | Expected no-match for Yudovich/Yudovitch, incompressible Euler, or bounded vorticity. |
| Typed-root predicate over `typed-graphs.json` | 1 | Expected fail-closed result: `root_node_id` does not name an existing node. |
| Structured-recipe predicate over `validation-specs.json` | 1 | Expected fail-closed result: all recipes lack the mandatory structured fields. |
| Blocker/ledger invariant check, `jq empty Stage1_Instances/THM-M-1234/*.json`, scoped `git diff --check`, and `test ! -e .stage1-worker-selftest.json` | 0 | Both new structured artifacts match the blocked/empty-context invariants, every owned JSON file parses, no whitespace errors were found, and no false completion packet exists. |

Fresh Lean output hashes:

| Output | SHA-256 |
|---|---|
| `Statement.olean` | `1709e38a5b8cc96159b7042585666cb84536b4b3d9e26a63697992cd9820d308` |
| `AnchorAudit.olean` | `d7aa0bc24b71af14a4110099cccf1f5a3f1d82c3d8eb349b36cd6a2b0d43d385` |
| `ObligationTree.olean` | `2521d53bc0b3ea2c9d0b7e7bcae9854ebe5081fc0cecd39a8a5fdfdf4324fc50` |
| `ConstructionProof.olean` | `e6ce672d3510b41c7dc26ebe4ad1a2af25f384a347fbdd2b7de8b60aa35070c0` |
| `ClosurePackageDiagnostic.olean` | `90d593506849a7714bbbf0a32d30bcaa2c5b23a289c79e4af7cb8550efc69931` |
| `Proof.olean` | `876e8f28d5426ae04e43026b695f75ec8fc45668ebf2fde3935cd7a8404586a5` |
| Combined kernel log | `4a79e1bb618e0787d519fede5d0b82391658302627cf549df490569d28b631fb` |

## Retry Boundary

Do not retry this unchanged root-sized proof item. The master must reconcile
the many existing blocker packets against the five-tick split rule, reopen and
repair the predecessor architecture with child-consuming formal targets and
candidate-specific closure, correct the typed root and structured recipes,
then split approximation, estimates, compactness, nonlinear momentum passage,
and trace into separate proof leaves. The other valid retry condition is an
immutable exact compatible Lean 4 terminal body that can be pinned, imported,
and checked for exact type, provenance, trust, and composition.

Remaining root cut set: `M1234-A-STRUCTURE`, `M1234-E-CLOSURE`.
The exact theorem, proof phase, audit, validation, release, and theorem
completion all remain unfinished.
