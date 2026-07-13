# THM-M-0030 validation-phase evidence

Item: `S56-M-0030-VALIDATION`. Base revision:
`bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`; base tree:
`ca999baf360c6ce2440bbc2c01aeb8d519269a90`.

## Validation scope

The structured node recipe re-elaborates `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and
the new `Validation.lean` in a fresh temporary module directory. Every Lean subprocess runs with
`--trust=0` inside a Bubblewrap network namespace. The root filesystem, toolchain, and dependency
cache are read-only; only the temporary directory holding local `.olean` files is writable.

`Validation.lean` imports neither `Proof` nor `ObligationTree`. Instead of invoking the exact ideal
terminal theorem, it separately specializes mathlib's pinned finite-module theorem at `M = R` and
checks the ideal/submodule conversion. This is a differential same-worker check, not a distinct
proof body or independent-runner attestation.

The validator binds the canonical expression, frozen denominator, proof receipt, exact mathlib
revision/tree/remote, clean mathlib worktree, terminal source/blob/route/body/compiled-object
hashes, license, and executable identities. The proof declarations and differential root are
sorry-free and report exactly `propext`, `Classical.choice`, and `Quot.sound`. A Lean environment
walk over the four terminal declarations plus the differential root observed 11193 transitively
used declarations in 482 modules, with no unexpected bodyless or unsafe declaration. This is a
trust/provenance observation, not an accepted foundation policy or complete release TCB/SBOM.

## Commands and results

All commands ran in the worker clone on 2026-07-14 (Asia/Shanghai). The pre-existing canonical
pinned `.lake` symlink was reused read-only. No `lake update`, `lake build`, clone, fetch,
dependency mutation, or network operation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0030
  exit 0: rank 1075, planned L0/rework-required target; theorem_complete=false

bash Stage1_Instances/THM-M-0030/check_proof.sh
  exit 0: four terminals and all 18 local interface/composition/root declarations reported only
  [propext, Classical.choice, Quot.sound]; all nine requested declarations were sorry-free

python3 -B Stage1_Instances/THM-M-0030/check_validation.py
  exit 0: exact target, frozen composition, proof roots, and differential root elaborated with
  --trust=0 under read-only/network-isolated Bubblewrap; local trust/provenance/pin/hygiene checks
  passed; release gates remained fail-closed

python3 -m json.tool Stage1_Instances/THM-M-0030/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0030/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m0030-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0030/check_validation.py
  exit 0: validator syntax passed without writing into the owned target

rg -n '\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|^[[:space:]]*(axiom|constant|unsafe)[[:space:]]' \
  Stage1_Instances/THM-M-0030 -g '*.lean'
  exit 1 (expected no match): no prohibited Lean construct was found

git diff --check -- Stage1_Instances/THM-M-0030 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; untracked files also passed per-file no-index checks
```

## Fail-closed gates

The proof prerequisite remains provisional `[_]`. The authoritative accepted state therefore
stays `[H1, M3, R3]`, `root_closed=false`, with no accepted obligation, even though the kernel
replay supports an exact `M0-W` candidate.

Network and filesystem isolation strengthen this replay, but the pinned cache is warm and shared.
This is not a separate clean checkout, empty-cache bootstrap, content-addressed offline
restoration, or deterministic release build. The theorem's foundation and TCB profiles remain
planned rather than accepted. The closure walk is not a serialized source-origin graph, complete
TCB inventory, or SBOM. The separately written wrapper used this worker identity, checkout,
kernel, and dependency cache; no distinct signed runner or independently implemented release
verifier exists. An unrelated manifest package is absent and was neither fetched nor used.

Primary-source `H0`, independently reviewed readable `R0`, full provenance/trust, cold hermetic
release, independent verification, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, and master
acceptance all remain open.

## Status boundary

This is a self-tested validation-node handoff for master inspection. It records the narrow gates
that passed and the release gates that failed. It does not claim `E0`/`E1`, accepted `M0`, accepted
foundation/TCB closure, independent evidence, theorem completion, release, or master acceptance.
