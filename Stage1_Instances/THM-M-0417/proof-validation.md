# THM-M-0417 proof-phase validation

Item: `S56-M-0417-PROOF`. Base revision:
`bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`.

## Implemented proof bodies

`Proof.lean` discharges the three mathematical interfaces frozen by the obligation tree. The
half-body lemma carries out the Haar-scaling and `ENNReal` calculation, the Blichfeldt bridge
specializes the pinned Blichfeldt theorem, and difference extraction constructs the nonzero
lattice difference from an overlap. `closesViaFrozenComposition` consumes all three through the
existing `root_compose` certificate. `closesFrozenStatementViaComposition` then checks that this
route has the exact proposition named by `Statement.lean`.

An independent direct wrapper, `minkowskiConvexBody`, applies
`MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_lt_measure` from pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. The wrapper and local reconstruction do not receive
duplicate terminal-body credit. The source and compiled-body hashes are bound in
`proof-receipt.json`.

This closes the seven formal/mathematical proof obligations provisionally. It does not close the
separate source or trust boundaries, and it does not establish theorem completion.

## Commands and exact results

Commands ran in the worker clone on 2026-07-13 UTC. The pre-existing canonical pinned `.lake`
symlink was reused. No `lake update`, `lake build`, dependency clone/fetch, network operation, or
`.lake` mutation was performed.

```text
$ bash Stage1_Instances/THM-M-0417/check_proof.sh
exit 0
the three child bodies, direct exact wrapper, frozen composition, canonical Statement transports,
and root exact-type certificate elaborated
all ten printed upstream/local theorem probes reported only:
  [propext, Classical.choice, Quot.sound]
PASS THM-M-0417 proof: exact pinned wrapper and frozen composition checked
machine proof cut set: empty; source/trust and downstream release gates remain

$ python3 Stage1_Instances/THM-M-0417/check_obligation_tree.py
exit 0: 9 required obligations, 0 exclusions, 7 typed graphs, DAG, aliases, recipes, and ledgers passed

$ python3 Stage1_Instances/THM-M-0417/check_anchor_audit.py
exit 0: pinned mathlib and legacy sources, proof-body scan, exact wrapper, and revisions passed

$ python3 Docs/tools/check_stage1_standard.py
exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

$ python3 scripts/stage1_target.py check
exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

$ python3 scripts/stage1_target.py show THM-M-0417
exit 0: rank 72, planned, L0/rework_required, theorem_complete false

$ python3 -m json.tool Stage1_Instances/THM-M-0417/proof-receipt.json >/dev/null
exit 0

$ rg -n '\b(sorry|admit|sorryAx|native_decide)\b|^[[:space:]]*(axiom|unsafe|external)[[:space:]]' \
    Stage1_Instances/THM-M-0417/Proof.lean
exit 1 with empty output: pass, no prohibited proof source

$ git diff --check -- Stage1_Instances/THM-M-0417 .stage1-worker-selftest.json
exit 0 with no output
```

## Boundary

The proof-phase machine root cut set is empty, pending master acceptance. `M0417-X-SOURCE` and
`M0417-X-TRUST` remain open. Human-source `H0`, readable `R0`, transitive provenance and TCB review,
hermetic/offline replay, independent validation, release, and master acceptance are downstream
gates. Accordingly `audit_complete` and `theorem_complete` remain false.
