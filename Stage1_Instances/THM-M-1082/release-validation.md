# THM-M-1082 Release Decision Handoff

## Exact verdict

`S56-M-1082-RELEASE` is **blocked**. The lifecycle remains `planned`, the accepted root vector
remains `[H2, M4, R4]`, and both `audit_complete` and `theorem_complete` remain false. No receipt is
accepted and no theorem-completion promotion is claimed.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation prerequisite is only
`[_]` worker evidence with `support_state=provisional_worker_selftest`, not a master-accepted
dependency. The release item therefore cannot be accepted even though its narrow replay succeeds.

## Reconciliation

The provisional validation evidence is substantive: the exact statement, registered directional
proofs, child-to-parent composition, exact proof root, and a same-worker independently written root
all elaborate against pinned Lean 4.29.0 and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The checked roots report only `propext`,
`Classical.choice`, and `Quot.sound`, and the checked sources pass the placeholder/unsafe scan.

That evidence is not release-grade. The authoritative intake record remains `[H2, M4, R4]`, while
the frozen pre-proof graph records an `M3` root; only the master can reconcile those states against
the provisional proof. There is no accepted pinpoint primary-source `H0` crosswalk or independently
reviewed `R0` reconstruction, so `AUDIT-Z` is also open.

The validation reused a shared warm `.lake` cache in a worker clone. There is no immutable clean
release snapshot, cold empty-cache network-denied build, offline archive restoration, complete
transitive TCB/provenance inventory, SBOM/license closure, protected CI and mutation evidence, two
separately provisioned signed runners, independently implemented minimal release verifier, or
deterministic content-addressed release bundle. A separate Lean proof in the same worker and cache
does not satisfy section 10.7.

## Self-test

Run from base revision `00641d8cecb3ce45e4fa66318bc97c9a63bb176e` on 2026-07-12:

```text
python3 Stage1_Instances/THM-M-1082/check_release.py
  exit 0
  release-decision: ok (blocked; validation unaccepted; H2/R4 and release gates open;
  audit_complete=false; theorem_complete=false)

python3 Stage1_Instances/THM-M-1082/check_validation.py
  exit 0
  PASS exact statement, composition, proof root, direct probe, trust, and provenance checks
  BLOCKED release gates: cold empty-cache hermetic replay and distinct-runner verification

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1082
  exit 0: rank 524; lifecycle planned; theorem_complete=false

git diff --check -- Stage1_Instances/THM-M-1082 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

No `lake update`, `lake build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed. The pre-existing untracked `.lake` symlink is excluded from changed paths and is not
release evidence.

## Retry boundary

The integration lane must accept the prerequisite and reconcile the authoritative root state. A
separately provisioned release lane must then close independent H0/R0 review, complete trust and
provenance, hermetic supply-chain replay, independent verification, CI/mutation, deterministic
bundle, and master-acceptance gates. Until then the exact theorem-completion verdict is false.
