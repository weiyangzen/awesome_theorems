# THM-M-1246 proof-phase validation

Item: `S56-M-1246-PROOF`

Validated: `2026-07-14` (`Asia/Shanghai`)

Base revision: `92246ea92c0c44282c05728798bc7c7e4a5a1464`

## Implemented proof

The local proof closes the exact sharp Euclidean `L2` Hardy target. For a
positive `eps`, `RegularizedIBP.lean` computes the divergence of
`x / (‖x‖^2 + eps)` coordinate by coordinate and proves the summed
compact-support integration-by-parts identity. `SharpEstimate.lean` combines
the radial operator-norm bound with sharp Young's inequality and the pointwise
bound

`(|u| * ‖x‖ / (‖x‖^2 + eps))^2 <= |u|^2 / (‖x‖^2 + eps)`.

This yields the exact constant `(2 / (n - 2))^2` for every regularized
density. `HardyLimit.lean` proves inverse-square integrability in dimension at
least three with a radial majorant and removes the regularization by dominated
convergence. `Proof.hardyTerminal` inhabits the frozen terminal without an
extra premise, and `Proof.hardyInequality` passes it through the checked
`root_of_hardyTerminal` transport.

This is provisional `M0-W` proof-node evidence for a local exact-root body.
The terminal uses positive denominator regularization rather than the frozen
tree's literal punctured-domain cutoff construction. Accordingly, the exact
typed terminal and root are kernel closed, but the internal planned leaf IDs
are not individually claimed and need a master architecture-delta review. It
does not claim master acceptance or theorem completion; validation, trust,
provenance, readability, independent replay, and release remain downstream.

## Commands and results

The raw Lean recipe uses only existing pinned oleans. No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation is part of this
evidence.

```text
bash Stage1_Instances/THM-M-1246/check_proof.sh
  exit 0
  Raw Lean 4.29.0 compiled Statement, ObligationTree, RegularizedIBP,
  SharpEstimate, HardyLimit, and Proof with --trust=0 -t0.
  hardyTerminal axioms: [propext, Classical.choice, Quot.sound]
  hardyInequality axioms: [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1246
  exit 0: rank 426, planned, theorem_complete=false

python3 Stage1_Instances/THM-M-1246/check_proof.py
  exit 0: exact root markers, source hashes, frozen inputs, receipt,
  placeholder policy, pins, and worker packet passed

python3 -m json.tool Stage1_Instances/THM-M-1246/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for both JSON artifacts

rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe|opaque)[[:space:]]' \
  Stage1_Instances/THM-M-1246/{RegularizedIBP,SharpEstimate,HardyLimit,Proof}.lean
  exit 1 with empty output: expected pass, no prohibited construct found

git diff --check -- Stage1_Instances/THM-M-1246 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

## Status boundary

The exact root is kernel-elaborated and proposed for proof-node acceptance as
an alternate terminal body, with internal architecture reconciliation open.
The authoritative item remains open until the integration lane accepts the
receipt. The accepted dossier remains `H2/M3/R4`; `theorem_complete=false`.
