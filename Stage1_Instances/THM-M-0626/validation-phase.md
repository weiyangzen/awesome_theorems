# THM-M-0626 validation-phase evidence

Item: `S56-M-0626-VALIDATION`. Base revision:
`48abbb2d2eeb89816c5ffc0ad8faafa4b9d24dd0`; base tree:
`0f26e2c78fb5fff9277cbbdfef5e145fd4ef06f1`.

## Validation scope

The node recipe re-elaborates `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and the new
`Validation.lean` in a fresh temporary module directory. Each Lean subprocess runs inside a
Bubblewrap network namespace with outbound networking unavailable. `Validation.lean` imports
neither `Proof` nor `ObligationTree`; it separately writes the exact global-continuity wrapper over
the pinned local `IsConnected.image` theorem. This is differential same-worker corroboration, not
an independent proof body or distinct-runner attestation.

The validator binds the canonical expression and registry denominator, proof receipt, exact
mathlib revision/tree/remote, clean dependency source, terminal file/blob/body/compiled-object
hashes, license, executable identities, reported axioms, and local prohibited-construct boundary.
The pinned terminals, five local open-set leaves, frozen compositions, three exact proof roots, and
differential wrapper are sorry-free. All nontrivial checked routes report exactly `propext`,
`Classical.choice`, and `Quot.sound`.

## Commands and results

All commands ran from the worker clone on 2026-07-13 (Asia/Shanghai). The pre-existing canonical
pinned `.lake` symlink was reused read-only. No `lake update`, `lake build`, clone, fetch, dependency
mutation, or network operation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0626
  exit 0: rank 1320, planned L0/rework-required target; theorem_complete=false

bash Stage1_Instances/THM-M-0626/check_proof.sh
  exit 0: 15 terminal, leaf, composition, and exact-root declarations are sorry-free; the
  nontrivial declarations report only [propext, Classical.choice, Quot.sound]

python3 -B Stage1_Instances/THM-M-0626/check_validation.py
  exit 0: exact target, frozen composition, proof roots, and differential root elaborate under
  network isolation; local trust/provenance/pin/hygiene checks pass; release gates fail closed

python3 -m json.tool Stage1_Instances/THM-M-0626/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0626/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

git diff --check -- Stage1_Instances/THM-M-0626 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; untracked files also passed per-file no-index checks
```

## Fail-closed gates

The pinned cache was warm and shared with the canonical automation checkout. Network isolation of
the Lean subprocesses is stronger than an ordinary warm replay, but it is not a separate clean
checkout, empty-cache bootstrap, content-addressed offline restoration, full transitive declaration
and TCB closure, complete SBOM, or second-platform attestation. The separate wrapper used the same
worker, toolchain, and dependency cache; there is no distinct verifier identity, independently
provisioned runner, second signature, or independently implemented release verifier.

The proof prerequisite remains provisional `[_]`. Consequently the accepted structured state stays
`[H1, M3, R4]`, `root_closed=false`, with no accepted proof obligation, even though the local
kernel replay supports an `M0-W` candidate. H0, R0, full provenance/trust, cold hermetic release,
independent verification, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, and master acceptance
remain open.

Snapshot-bound predecessor checkers are not current validation gates: `check_proof.py` expects the
proof-phase base and self-test packet, while `check_obligation_tree.py` preserves its pre-integration
workflow snapshot. This phase instead binds their immutable inputs and receipts by hash and directly
replays the claimed Lean declarations.

## Status boundary

This is a self-tested validation-node handoff for master inspection. It truthfully records passed
narrow gates and failed release gates. It does not claim E0/E1, accepted M0, independent evidence,
theorem completion, release, or master acceptance.
