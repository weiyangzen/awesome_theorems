# S56-M-0987-RELEASE worker evidence

Date: `2026-07-12`

Base revision: `e9d0ffbd4833905f2353a3b82ffd9263891b786b`

The exact release verdict is `blocked`. Lifecycle remains `planned`; no receipt is accepted, and
neither `AUDIT-Z` nor `THEOREM-Z` is established. The first gate fails at dependency acceptance:
the validation receipt is provisional worker evidence, is not release-grade, and has not been
master accepted.

The exact selected real-valued iid CLT root is locally kernel-closed through the pinned mathlib
theorem `ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub`. This supports only a
provisional `M1` classification. The accepted vector remains `[H2, M3, R3]`: the frozen typed graph
predates proof closure, the public source began as a broader theorem-family label, and H0/R0 review
is absent. The checkout also lacks complete transitive trust/TCB closure, a cold empty-cache offline
replay, SBOM/license archives, distinct-runner attestations, an independent minimal verifier, and a
deterministic signed release bundle.

## Commands and exact results

All commands ran in the worker clone. The canonical pinned `.lake` symlink was reused; no update,
build, fetch, clone, or network operation ran.

```text
$ python3 Docs/tools/check_stage1_standard.py
check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
exit 0

$ python3 scripts/stage1_target.py check
stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
exit 0

$ python3 scripts/stage1_target.py show THM-M-0987
exit 0; rank 267, planned, L0/rework_required, theorem_complete false

$ python3 Stage1_Instances/THM-M-0987/check_release.py
release reconciliation ok: provisional validation receipt hash and frozen root agree
release blocked: dependency is unaccepted and audit/release assurance remains open
AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]
exit 0

$ python3 -m json.tool Stage1_Instances/THM-M-0987/release-decision.json
exit 0

$ git diff --check -- Stage1_Instances/THM-M-0987 .stage1-worker-selftest.json
exit 0; no output
```

`check_release.py` binds the decision to the validation receipt and stale frozen root, then reruns
the narrow validation recipe. That recipe performs real `lake env lean` elaboration of the exact
proof/composition declarations and the independently transcribed same-checkout target. This
self-tests only the truthful blocked decision; it is not release evidence and changes no
authoritative state.
