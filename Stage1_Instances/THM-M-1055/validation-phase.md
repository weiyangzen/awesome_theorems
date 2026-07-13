# THM-M-1055 validation-phase evidence

Item: `S56-M-1055-VALIDATION`. Base revision:
`67b1bf1758649d2be86775230c7d4bfe117ade2b`; base tree:
`5f872831428a9d9805e61aad3868be443c29cef2`.

## Validation scope

The structured recipe re-elaborates `Statement.lean`, `ObligationTree.lean`, both locally ported
analytic modules, `Proof.lean`, and the new `Validation.lean` in a fresh temporary directory. Every
Lean process runs with `--trust=0` inside a Bubblewrap network namespace. The root filesystem,
toolchain, and canonical pinned dependency cache are read-only; only temporary local `.olean` files
are writable.

`Validation.lean` imports neither `Proof` nor `ObligationTree`. It separately specializes
`ErgodicTheory.tendsto_birkhoffAverage_ae_integral` to the exact frozen target. This checks the
wrapper independently of the proof module, but it shares the terminal body, worker identity, and
cache. It is differential corroboration, not a distinct-runner attestation or second proof body.

The validator binds the canonical expression, frozen denominator, proof receipt, local source and
license hashes, upstream revision/archive/source hashes, exact two-change port delta, executable
identities, and clean pinned mathlib revision/tree/remote. Proof and differential declarations are
sorry-free and report exactly `propext`, `Classical.choice`, and `Quot.sound`. These are useful
trust and provenance observations, not an accepted foundation profile, complete transitive TCB or
source-origin graph, SBOM, or release bundle.

## Commands and results

All commands ran in the worker clone on 2026-07-14 (Asia/Shanghai). The automation-provided pinned
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
`.lake` mutation, or network operation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1055
  exit 0: rank 247, planned L0/rework-required target; theorem_complete=false

python3 Stage1_Instances/THM-M-1055/check_obligation_tree.py
  exit 0: frozen 14-obligation registry and 30 typed edges passed; pre-proof root remains open

python3 -B Stage1_Instances/THM-M-1055/check_validation.py
  exit 0: exact target, frozen composition, both analytic ports, proof root, and differential root
  elaborated with --trust=0 under read-only/network-isolated Bubblewrap; local trust, provenance,
  pin, graph-boundary, receipt, and hygiene checks passed; release gates remained fail-closed

python3 -m json.tool Stage1_Instances/THM-M-1055/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-1055/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m1055-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-1055/check_validation.py
  exit 0: validator syntax passed without writing bytecode into the target

rg -n '\b(sorry|admit|sorryAx|implemented_by|native_decide|extern)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]' \
  Stage1_Instances/THM-M-1055 -g '*.lean'
  exit 1 (expected no match): no prohibited Lean construct was found

git diff --check -- Stage1_Instances/THM-M-1055 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; untracked files also passed per-file no-index checks
```

The snapshot-bound predecessor `check_proof.py` was not used as a current gate: it deliberately
expects the earlier proof worker's base commit, DAG state, dirty set, and root packet. Its receipt is
hash-bound, while this validation phase independently replays the Lean sources instead of weakening
or falsely claiming that stale checker passes.

## Fail-closed gates

The proof prerequisite is only provisional `[_]`, not master accepted. Moreover, the frozen
`M1055-A-EXTERNAL-INTEGRATION` node names `lua-vr/pointwise-birkhoff@fc06094c...`, while the
successful local port comes from `marcmorningstar/lean4-ergodic-theory@ed3fa6b8...`. The worker
does not rewrite the frozen registry or graph. The accepted state remains `[H2, M4, R4]`,
`root_closed=false`, with zero accepted obligations, even though the exact canonical root reaches
the kernel through the alternate route.

Network and filesystem isolation strengthen this replay, but the cache is warm and shared. This is
not a separate clean checkout, empty-cache bootstrap, content-addressed offline restoration, or
deterministic release build. Foundation and TCB profiles are unaccepted, complete transitive
provenance/SBOM evidence is absent, and the differential wrapper is not a distinct signed runner or
independently implemented release verifier. Pinpoint independently reviewed `H0` and `R0`,
`AUDIT-Z`, `THEOREM-Z`, release, theorem completion, and master acceptance remain open.

## Status boundary

This is a self-tested validation-node handoff for master inspection. It records the narrow gates
that passed and the assurance gates that failed closed. It does not claim `E0`/`E1`, accepted
`M0`, reconciled graph closure, accepted foundation/TCB, independent evidence, theorem completion,
release, or master acceptance.
