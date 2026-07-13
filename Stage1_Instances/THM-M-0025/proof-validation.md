# THM-M-0025 proof-phase validation

Item: `S56-M-0025-PROOF`. Base revision:
`72f928bdf1a47d7c119826db45575bd02a3a63ce`.

## Implemented proof route

`Proof.lean` installs the exact pinned `Polynomial.isNoetherianRing` theorem at the frozen
`ExactPolynomialAnchor` interface. `hilbertBasisTheorem_via_frozen_composition` then consumes the
registered finite-generation transports through `root_of_exactPolynomialAnchor` and returns the
unchanged canonical `HilbertBasisTheoremTarget`. A direct exact-root wrapper provides a second
type check over the same terminal body; aliases are deduplicated and receive no extra proof credit.

The upstream terminal body and its instance installation are in
`Mathlib/RingTheory/Polynomial/Basic.lean` lines 732-806 at
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, source blob
`1ae18244a4534f336f1d9280a1f5f8fd1a5acd9f`, and file SHA-256
`7cedafd3e1fc910b152c699375e8670f0db7d6261d7ebdd3dd8ff2420fda5b9c`. The body is pinned
upstream, not vendored or independently reconstructed locally, so this phase proposes exact-root
`M0-W` only, pending master acceptance and downstream validation.

## Commands and results

Validation ran in the worker clone on 2026-07-13 (Asia/Shanghai). The existing canonical pinned
`.lake` symlink was reused read-only; no update, build, dependency clone/fetch, network operation,
or `.lake` mutation was performed.

```text
bash Stage1_Instances/THM-M-0025/check_proof.sh
  exit 0
  isolated temporary Statement.olean and ObligationTree.olean elaborated; the pinned terminal,
  exact anchor, direct exact root, and frozen-composition root were all sorry-free and each axiom
  report was exactly [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0025
  exit 0: rank 1070, planned, L0/rework_required, theorem_complete=false

python3 -B Stage1_Instances/THM-M-0025/check_proof.py
  exit 0: exact source, frozen target/denominator, pin, terminal source body, composition,
  receipt, worker packet, and no-completion boundary passed

python3 -B Stage1_Instances/THM-M-0025/check_obligation_tree.py
  exit 1: the predecessor's frozen checker still requires authoritative DAG state `[ ]`, while the
  integration lane has since promoted S56-M-0025-OBLIGATION_TREE to `[_]`; no authority file was
  changed by this worker

python3 -B Stage1_Instances/THM-M-0025/check_anchor_audit.py
  exit 1: the predecessor checker is bound to its historical base revision
  94f6abf9359f26384e0f68bef694dc5b9aae624c, not this assigned proof base; the proof checker
  independently rechecks the current anchor hash, exact mathlib revision/tree/blob, clean package,
  terminal source body, and prohibited constructs

rg -n -i --glob '*.lean' '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|native_decide|extern[[:space:]]' \
  Stage1_Instances/THM-M-0025/Proof.lean
  exit 1 with empty output: expected pass, no prohibited construct found

python3 -m json.tool Stage1_Instances/THM-M-0025/proof-receipt.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-0025 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

This is narrow proof-phase evidence only and does not claim theorem completion. The accepted state
remains `[H1, M3, R3]` with empty accepted proof state until the integration lane acts.
`M0025-S-FOUNDATION`, H0, R0, full transitive provenance and trust, validation, hermetic replay,
independent verification, release, `AUDIT-Z`, and `THEOREM-Z` remain downstream. The two stale
predecessor-validator failures above do not invalidate this proof-phase self-test: their underlying
frozen artifacts are unchanged, and the assigned proof's exact target, pin, source body,
composition, axiom closure, and placeholder boundary are checked by `check_proof.py` and
`check_proof.sh` against the current base.
