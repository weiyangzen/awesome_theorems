# THM-M-1008 validation-phase result

Item: `S56-M-1008-VALIDATION`

Base revision: `4e632139f5060edf088cd107551caac63981263b`

Validation date: `2026-07-14` (`Asia/Shanghai`)

## Scope and result

The node-scoped replay copies the exact statement, conditional obligation composition, proof root,
and exact-type probe into a fresh temporary directory. It invokes the pinned Lean executable with
`--trust=0`, fixed locale/timezone/thread settings, a read-only host, and an unshared network
namespace. The exact Hewitt-Savage proof root elaborates and is transitively sorry-free. The proof
root, conditional composition declarations, and exact-type probe report exactly `propext`,
`Classical.choice`, and `Quot.sound`.

This is narrow nonrelease evidence over the automation-provided shared warm `.lake` closure.
`Validation.lean` imports `Proof.lean` and adds only an exact-type probe; it is not a second proof.
The proof prerequisite is not master-accepted and has no structured proof receipt. Moreover, the
frozen graph still records an `M2` open root and requires the self-independence route, while
`Proof.lean` instead proves probability idempotence directly. Validation therefore fails closed on
dependency acceptance, composition/state reconciliation, complete trust/provenance, cold hermetic
reproduction, and genuinely independent verification.

## Commands and exact results

Commands ran from the repository root. No update, build, fetch, clone, network request, or `.lake`
mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 1546 uniform-L0 Lean 4 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1008
  exit 0: rank 288, planned, legacy artifacts unaccepted, theorem_complete=false

timeout 600s Stage1_Instances/THM-M-1008/check_validation.sh
  exit 0:
  PASS THM-M-1008 network-isolated narrow kernel replay
  PASS exact root/type probe: propext, Classical.choice, Quot.sound
  PASS transitive sorry check: proof root and type probe are sorry-free

python3 -B Stage1_Instances/THM-M-1008/check_validation.py
  exit 0:
  PASS THM-M-1008 narrow validation
  PASS kernel replay: exact statement, conditional composition, proof root, and exact-type probe elaborated under network isolation
  PASS trust observation: checked declarations report exactly propext, Classical.choice, and Quot.sound and the root is transitively sorry-free
  PASS selected provenance: frozen hashes, direct imports, compiled objects, clean mathlib pin, license, and tool identities agree
  PASS hygiene: comment-stripped prohibited-construct scan and kernel sorry checks passed
  FAIL CLOSED authority: proof master acceptance, a proof receipt, and frozen-graph/direct-idempotence-route reconciliation are absent
  FAIL CLOSED trust/provenance: foundation policy, complete transitive declaration/TCB closure, SBOM, and source-boundary acceptance remain open
  FAIL CLOSED hermetic/independent: shared warm .lake and same-worker type probe are neither cold offline replay nor distinct signed verification
  audit_complete=false; theorem_complete=false

python3 -m json.tool Stage1_Instances/THM-M-1008/validation-spec.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-1008/validation-receipt.json >/dev/null
  exit 0 for both structured artifacts

git diff --check -- Stage1_Instances/THM-M-1008 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

## Gate decisions

| Gate | Decision | Evidence or boundary |
|---|---|---|
| Exact kernel replay | provisional pass | The exact frozen target, conditional composition, local proof root, and exact-type probe elaborate from fresh source copies with kernel trust level zero. |
| Placeholder and unsafe hygiene | pass | Transitive Lean sorry checks and a comment-stripped scan found no placeholder, bodyless, unsafe, native/oracle, external, or implemented-by construct. |
| Trust observation | provisional pass | The checked declarations report exactly the three recorded classical axioms; the open foundation node and missing complete TCB closure prevent accepted trust status. |
| Selected local provenance | provisional pass | Exact local hashes, seven direct mathlib source/olean pairs, clean revision/tree/remote, license, manifest, and tool identities agree; complete transitive provenance is absent. |
| Structured authority | fail closed | Proof is only `[_]`, has no structured receipt, and the pre-proof graph's required self-independence composition is not the direct idempotence route implemented in `Proof.lean`. |
| Hermetic reproduction | fail closed | This is a network-isolated warm-cache replay, not a new immutable checkout, empty-cache cold bootstrap, offline-restorable dependency closure, or deterministic release bundle. |
| Independent verification | fail closed | The exact-type probe shares the worker, checkout, proof body, kernel, and cache; no distinct identity, runner, signature, or independently implemented minimal verifier exists. |

The first failed node gate is `dependency.S56-M-1008-PROOF.master_acceptance`; the first failed
release gate is `S56-10.6-HERMETIC-COLD-BUILD`. Accepted authority remains `[H1, M2, R3]`, while
the locally observed proof root is provisionally kernel-closed. `audit_complete=false` and
`theorem_complete=false`. This worker evidence grants no accepted `M0-L`, `H0`, `R0`, `AUDIT-Z`,
`THEOREM-Z`, release, independent-validation, or master-acceptance credit.
