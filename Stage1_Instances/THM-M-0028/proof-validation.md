# THM-M-0028 proof-phase validation

Item: `S56-M-0028-PROOF`. Base revision:
`7d0965498598e684e3e3d0a01836c2bf36a02959`.

## Implemented proof route

`Proof.lean` installs the pinned `isNoetherianRing_iff_ideal_fg` theorem at the frozen
`FiniteGenerationToNoetherian` interface and `monotone_stabilizes_iff_noetherian` at the frozen
`NoetherianToChainStabilization` interface. The first converts the exact finite-generation premise
to `IsNoetherianRing R`; the second specializes the regular-module ascending-chain equivalence and
returns the unchanged `Nat →o Ideal R` tail equality. The proof includes the zero ring.

`idealAscendingChainTheorem_via_frozen_composition` consumes both registered bridges through
`root_of_bridges`. A direct exact-root wrapper provides a second type check over the same two
terminal bodies; aliases are deduplicated and receive no extra proof credit.

The upstream bodies are in `Mathlib/RingTheory/Noetherian/Defs.lean` lines 159-162 and 193-204 at
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, source blob
`66ddf1f73601e7dbeb04e37b95fcc61e34ee3c14`, file SHA-256
`a0e5c5a1aceb564f885573d5c51ec124be20abbd19fabc6af8c798b637530f0b`, and combined body
SHA-256 `15ae568432091fd1cc53f8136d5c12d441abf60af630459c4d27e4d3627c8ebc`. This phase
proposes exact-root `M0-W` only, pending master acceptance and downstream validation.

## Commands and results

Validation ran in the worker clone on 2026-07-13 (Asia/Shanghai). The existing canonical pinned
`.lake` symlink was reused read-only; no update, build, dependency clone/fetch, network operation,
or `.lake` mutation was performed.

```text
bash Stage1_Instances/THM-M-0028/check_proof.sh
  exit 0
  isolated temporary Statement.olean and ObligationTree.olean elaborated; both pinned terminals,
  both exact bridges, the direct exact root, and the frozen-composition root were sorry-free; the
  root axiom reports were exactly [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0028
  exit 0: rank 1073, planned, L0/rework_required, theorem_complete=false

python3 -B Stage1_Instances/THM-M-0028/check_proof.py
  exit 0: exact source, frozen target/denominator, pins, terminal bodies, composition, receipt,
  worker packet, and no-completion boundary passed

rg -n -i --glob '*.lean' '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|native_decide|extern[[:space:]]' \
  Stage1_Instances/THM-M-0028/Proof.lean
  exit 1 with empty output: expected pass, no prohibited construct found

python3 -m json.tool Stage1_Instances/THM-M-0028/proof-receipt.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-0028 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

This is narrow proof-phase evidence only and does not claim theorem completion. The accepted state
remains `[H1, M3, R3]` with empty accepted proof state until the integration lane acts.
`M0028-S-FOUNDATION`, H0, R0, full transitive provenance and trust, validation, hermetic replay,
independent verification, release, `AUDIT-Z`, and `THEOREM-Z` remain downstream.
