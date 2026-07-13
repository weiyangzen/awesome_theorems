# THM-M-1053 validation-phase evidence

Item: `S56-M-1053-VALIDATION`. Base revision:
`a3c20fd2f4da1879baa00bd5455573c49d4b2fa0`; base tree:
`2ae6946f2b059449025558b6033de33c332412ee`.

## Validation scope

The node recipe re-elaborates `Statement.lean`, `ObligationTree.lean`, both locally ported analytic
modules, `Proof.lean`, and `Validation.lean` with Lean `--trust=0` in fresh temporary output space.
Every Lean subprocess runs inside a Bubblewrap network namespace with the root, toolchain, and
pinned dependency inputs read-only. Only the temporary module directory is writable.

`Validation.lean` imports neither `Proof` nor `ObligationTree`. It is a separately written exact-
type reconstruction that builds the conditional-expectation witness directly from the ported
general Birkhoff theorem and uses uniqueness against the ported ergodic integral-limit theorem.
This is a same-worker differential check, not a distinct-runner attestation or a second proof body.

The proof and differential declarations are sorry-free and report exactly `propext`,
`Classical.choice`, and `Quot.sound`. The validator also reconstructs the two upstream source byte
streams from the documented compatibility port, checks their immutable hashes and Apache-2.0
license, and binds the statement, registry denominator, proof receipt, dependency pin, clean
mathlib tree, remote, toolchain manifests, and executable identities.

## Commands and results

Commands ran from the worker clone on 2026-07-14 (Asia/Shanghai). The automation-provided pinned
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
checkout, or network request ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1053
  exit 0: rank 245, planned L0/rework-required target; theorem_complete=false

python3 Stage1_Instances/THM-M-1053/check_obligation_tree.py
  exit 0: the frozen 16-obligation registry and 35 typed edges passed; authoritative root remains open

python3 -B Stage1_Instances/THM-M-1053/check_validation.py
  exit 0: network-isolated trust-zero exact-root, proof-route, port, and differential replay passed;
  authority, graph, foundation/TCB/provenance, cold-hermetic, and independent gates failed closed

python3 -m json.tool Stage1_Instances/THM-M-1053/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-1053/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m1053-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-1053/check_validation.py
  exit 0: validator compiled outside the repository tree

rg -n --glob '*.lean' '<prohibited construct pattern>' \
  Stage1_Instances/THM-M-1053
  exit 1 with empty output: expected pass, no prohibited construct found

git diff --check -- Stage1_Instances/THM-M-1053 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; untracked files also passed per-file no-index checks
```

The snapshot-bound predecessor `check_proof.py` is not a current validation gate: it deliberately
expects the proof worker's older base revision, execution state, dirty set, and self-test packet.
This phase hash-binds that proof receipt and directly replays every Lean source instead of weakening
the predecessor checker or falsely reporting that its stale workspace assertions pass.

## Fail-closed gates

The exact unchanged `StatementShape` reaches the kernel through the proof route and a separately
written differential route. That does not reconcile the frozen graph. Its dense-class leaf was not
realized by the successful maximal/conditional-expectation route, and its
`ErgodicLimitIdentificationPackage` is false because it relates an arbitrary invariant `g` to an
unrelated `f`; the proof's checked one-point counterexample refutes it. The proof prerequisite is
also only provisional `[_]`, never master accepted. Accepted state therefore remains
`[H2, M1, R4]`, with no accepted closed obligation and `root_closed=false`.

Network and filesystem isolation strengthen this narrow replay, but `.lake` is warm and shared.
This is not a separate clean checkout, empty-cache cold bootstrap, content-addressed offline
restoration, or deterministic release bundle. The theorem-specific foundation policy and complete
Lean/compiler/bootstrap/plugin/native/checker TCB inventory are unaccepted, complete transitive
declaration/source provenance and SBOM evidence are absent, and the differential wrapper shares the
worker identity, checkout, kernel, and cache. Pinpoint independently reviewed `H0` and `R0`, a
distinct signed runner, an independently implemented minimal release verifier, `AUDIT-Z`,
`THEOREM-Z`, release, and theorem completion remain false.

## Status boundary

This is self-tested validation-node evidence proposing only `[_]` for master inspection. It records
the narrow gates that passed and the assurance gates that failed closed. It does not claim `E0` or
`E1`, accepted `M0-P`, frozen-graph closure, accepted foundation/TCB, complete provenance,
independent validation, audit completion, theorem completion, release, or master acceptance.
