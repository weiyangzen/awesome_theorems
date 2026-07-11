# THM-M-0106 validation-phase record

Item: `S56-M-0106-VALIDATION`

Base revision: `08188d9b8d9d1f42b83c7fbc17ffabba5bc76d61`

Validation timestamp: `2026-07-11T20:18:02Z`

## Scope and result

The narrow validator re-elaborates the exact proof body and a separately
written exact-target probe from fresh temporary module files. `Validation.lean`
does not import or call `Proof.lean`: it proves the checked historical
affine-Spec encoding from pinned mathlib's
`exists_finite_inj_algHom_of_fg`, then applies the frozen statement's iff
transport. Both declarations report only `propext`, `Classical.choice`, and
`Quot.sound`.

The Python verifier also checks proof-receipt input hashes, target and registry
identity, the pinned clean mathlib checkout, and local placeholder/axiom/unsafe
hygiene. The structured provisional receipt is `validation-receipt.json`.

## Commands and exact results

Commands ran from the repository root unless stated otherwise. No update,
build, fetch, clone, or dependency mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0106
  exit 0: execution rank 30; lifecycle planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0106/check_validation.py
  exit 0: exact proof and independently written exact-target probe elaborated;
  axiom profile, proof-receipt hashes, pinned clean mathlib revision, registry
  identity, and local prohibited-token scan passed

python3 Stage1_Instances/THM-M-0106/check_statement.py
  exit 0: expression SHA-256
  4980834b63da78609158f944b53234d72089e2bfaacb348461de2651aa671209;
  all four structural mutations distinguished

python3 Stage1_Instances/THM-M-0106/check_anchor_audit.py
  exit 0: audited expression definitionally matches the frozen target

python3 Stage1_Instances/THM-M-0106/check_obligation_tree.py
  exit 0: 18 obligations and 39 typed edges passed; this frozen pre-proof
  artifact truthfully retains its earlier open-root boundary

python3 Stage1_Instances/THM-M-0106/check_proof.py
  exit 0: exact unconditional proof body and required pinned bridges passed

python3 -m json.tool Stage1_Instances/THM-M-0106/validation-receipt.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-0106 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

## Failed gates and boundary

The first failed rev-5.6 gate is section 10.6 hermetic reproduction. This run
used the canonical pinned but warm shared `.lake` artifacts; it did not create
a new checkout with empty user/package/build caches, restore an offline
dependency archive, or perform a cold network-denied build. Complete TCB,
SBOM/license, deterministic bundle, and signature evidence is absent.

The same-workspace Lean probe is useful independent implementation evidence,
but it is not section 10.7 independent verification: there is no separately
provisioned runner, distinct verifier identity, second signed attestation, or
independently implemented minimal release verifier. H0/R0 reviews, graph/state
reconciliation, `AUDIT-Z`, `THEOREM-Z`, release, and master acceptance remain
open. Therefore `audit_complete=false` and `theorem_complete=false`; this
validation node is self-tested only as truthful provisional evidence.
