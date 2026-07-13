# THM-M-1009 validation-phase result

Item: `S56-M-1009-VALIDATION`  
Base revision: `3bb4cb3ae15dff8b48c93242019edec3bf858e48`  
Validation time: `2026-07-13T17:41:58Z`

## Scope and result

The node-scoped validator re-elaborates temporary source copies of the exact
frozen statement, obligation-tree composition, and local proof root with Lean
kernel trust level zero. Both root declarations report exactly `propext`,
`Classical.choice`, and `Quot.sound`. The validator also checks the frozen
expression and denominator fingerprints, proof-receipt linkage, prohibited
constructs, Lean executable identity, clean pinned mathlib revision, and the
direct import's source and olean hashes.

`Validation.lean` imports only `Statement.lean`. It independently implements
the final passage from bounds by every measurable tail to the limiting limsup
measure, plus an exact-target type probe. It assumes the substantive tail-bound
and tail-limit interfaces, so it is useful differential composition evidence,
not an independent mathematical proof and not a distinct-runner attestation.

## Commands and exact results

Commands ran from the repository root unless stated otherwise. The existing
pinned dependency closure was reused. No update, build, clone, fetch, network
operation, or `.lake` mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 1546 uniform-L0 Lean 4 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1009
  exit 0: execution rank 289; planned; legacy artifacts unaccepted;
  theorem_complete=false

timeout 360s Stage1_Instances/THM-M-1009/check_proof.sh
  exit 0: exact root and frozen composition elaborated; both declarations
  report [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-1009/check_proof.py
  exit 0: proof source, receipt, hashes, pin, hygiene, and local root closure
  passed with the downstream validation self-test manifest present

timeout 360s python3 Stage1_Instances/THM-M-1009/check_statement.py
  exit 0: exact expression fingerprint and four structural mutations passed

python3 Stage1_Instances/THM-M-1009/check_obligation_tree.py
  exit 0: 15 obligations and 28 typed edges passed; the frozen pre-proof graph
  truthfully retains root_closed=false

python3 Stage1_Instances/THM-M-1009/check_validation.py
  exit 0:
  PASS THM-M-1009 narrow validation
  kernel: exact frozen root and frozen composition replayed from temporary source copies
  trust: both root paths report exactly propext, Classical.choice, Quot.sound; hygiene passed
  provenance: frozen hashes, proof linkage, Lean identity, clean mathlib pin, source and olean hashes passed
  differential: independently written final composition and exact-type probe elaborated without importing Proof
  blocked: proof master acceptance, graph reconciliation, cold offline hermetic replay, and distinct-runner verification

python3 -m json.tool Stage1_Instances/THM-M-1009/validation-spec.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-1009/validation-receipt.json >/dev/null
  exit 0 for both structured artifacts

git diff --check -- Stage1_Instances/THM-M-1009 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

## Gate decisions

| Gate | Decision | Evidence or boundary |
|---|---|---|
| Exact kernel replay and composition | pass locally | The exact target root and frozen composition elaborate from temporary sources under `--trust=0`. |
| Placeholder and unsafe hygiene | pass | No `sorry`, `admit`, `sorryAx`, local axiom, opaque/unsafe/oracle, or native shortcut occurs in checked sources or output. |
| Observed axiom profile | provisional pass | The two root paths and independent composition probe report exactly the three recorded classical axioms; no complete accepted TCB profile is claimed. |
| Local provenance | pass | Frozen hashes, proof linkage, Lean identity, clean mathlib pin, and direct source/olean hashes agree. |
| Proof dependency and graph freshness | fail closed | Proof is only provisional `[_]`; the authoritative frozen graph still records the pre-proof `M3` root and awaits master reconciliation. |
| Hermetic reproduction | fail closed | A shared warm `.lake` was reused; there was no fresh checkout, empty-cache cold build, offline restoration, host-enforced network denial, SBOM/license closure, or complete TCB inventory. |
| Independent verification | fail closed | The separate composition implementation ran in this mutable clone and shared cache; there is no second identity, signed attestation, independently provisioned runner, or independent minimal release verifier. |

This is truthful nonrelease worker evidence only. The accepted vector remains
`[H1, M3, R3]`; `audit_complete=false` and `theorem_complete=false`. It grants
no proof acceptance, accepted `M0-L`, `H0`, `R0`, `AUDIT-Z`, `THEOREM-Z`,
release, or master-acceptance credit.
