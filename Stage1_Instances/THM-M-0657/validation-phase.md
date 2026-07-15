# THM-M-0657 validation-phase evidence

Item: `S56-M-0657-VALIDATION`. Base revision:
`8b9311952b6b4186c774d25758d16597a7c10a8b`; base tree:
`69a7cea0132f4b76e7324c2d5cc320dec94d2f10`.

## Validation scope

The structured recipe re-elaborates disposable copies of `Statement.lean`,
`ObligationTree.lean`, `Proof.lean`, and `Validation.lean`. Every Lean process
runs with `--trust=0 -t0` in a Bubblewrap network namespace. The host root,
toolchain, and canonical pinned dependency cache are read-only; only a fresh
temporary output directory is writable.

`Validation.lean` imports neither `Proof` nor `ObligationTree`. It separately
reconstructs target-cardinality model existence, categoricity of the
infinite-model theory, its Los-Vaught completeness consequence, and the final
binder composition from an explicit uniqueness-transfer premise. This is a
same-worker differential check, not a distinct proof body or an independent
runner attestation. In particular, the premise retains the complete open
Morley rank, stability, saturation, and saturated-uniqueness argument.

The validator binds the canonical expression, frozen denominator, proof
receipt and blocker, local source hashes, exact mathlib revision/tree/remote,
clean mathlib worktree, selected source and compiled-object hashes, license,
and executable identities. The checked proof and validation declarations are
sorry-free and use only `propext`, `Classical.choice`, and `Quot.sound`. A Lean
environment walk from the four differential declarations observed 9214
transitively used declarations in 356 modules, with no unexpected bodyless or
unsafe declaration. This is a trust observation, not an accepted foundation
policy or complete release TCB/provenance inventory.

## Commands and results

All commands ran in the worker clone on 2026-07-15 (Asia/Shanghai). The
pre-existing canonical pinned `.lake` symlink was reused read-only. No `lake
update`, `lake build`, clone, fetch, dependency mutation, or network operation
was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0657
  exit 0: rank 702, planned L0/rework-required target; theorem_complete=false

python3 Stage1_Instances/THM-M-0657/check_obligation_tree.py
  exit 0: 14 obligations and 56 typed edges passed; frozen root remains open M3

python3 -I -B Stage1_Instances/THM-M-0657/check_validation.py --worker-packet .stage1-worker-selftest.json
  exit 0: network-isolated trust-zero narrow replay, selected provenance checks,
  and all fail-closed receipt assertions passed

python3 -m json.tool Stage1_Instances/THM-M-0657/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0657/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m0657-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0657/check_validation.py
  exit 0: validator syntax passed without writing bytecode into the repository

rg -n '\b(sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|^[[:space:]]*(axiom|constant|opaque|unsafe|extern)[[:space:]]' \
  Stage1_Instances/THM-M-0657 -g '*.lean'
  exit 1 (expected no match): no prohibited executable Lean construct was found

git diff --check -- Stage1_Instances/THM-M-0657 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; untracked files also passed explicit hygiene checks
```

## Fail-closed gates

The proof prerequisite remains provisional `[_]`; no receipt or obligation is
master-accepted. The two unconditional bodies provisionally bound to
`M0657-L-COMPLETENESS` and `M0657-C-EXISTENCE` replay successfully, but the
frozen graph still records `[H1, M3, R3]` with an empty accepted closure. The
first mathematical gap is `M0657-C-MORLEY-RANK`, followed by
stability, saturation, saturated-model isomorphism, target uniqueness, and the
unconditional root.

Network and filesystem isolation strengthen this replay, but the dependency
cache is warm and shared. This is not a separate clean checkout, empty-cache
bootstrap, content-addressed offline restoration, or deterministic release
build. The foundation/TCB profiles remain planned. The closure walk is not a
serialized source-origin graph, complete TCB inventory, or SBOM. The separate
Lean implementation used this worker identity, checkout, kernel, and cache;
no distinct signed runner or independently implemented release verifier
exists.

Primary-source `H0`, independently reviewed readable `R0`, complete
provenance/trust, cold hermetic release, independent verification, `AUDIT-Z`,
`THEOREM-Z`, release, theorem completion, and master acceptance all remain
open.

## Status boundary

This is a self-tested validation-node handoff for integration-lane inspection.
It records narrow gates that passed and assurance/release gates that failed.
It does not claim accepted obligation closure, `M0`, `E0`/`E1`, accepted
foundation/TCB closure, theorem completion, release, or master acceptance.
