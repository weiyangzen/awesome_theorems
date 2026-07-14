# THM-M-0559 proof-phase validation

Item: `S56-M-0559-PROOF`. Base revision:
`00f98378e8c1c63097871ae62aeed895d83b0cb4`.

## Verdict

`partial_proof_self_tested_root_blocked`. `Proof.lean` contains six placeholder-free
component-reduction lemmas toward `M0559-N-COMPONENTS` and an implementation candidate for frozen
branch `M0559-B-EMPTY`. Component bijectivity first transfers the
empty/nonempty boundary from `X` to `Y`; under `IsEmpty X`, the proof constructs the unique
homeomorphism `X ≃ₜ Y`, converts it to `ContinuousMap.HomotopyEquiv`, and checks that its forward
map is the prescribed `f`.

The frozen branch record has only a planned statement fingerprint. The checked declaration is
therefore a provisional implementation candidate pending master exact-statement mapping, not an
accepted `M0-L` or closed-obligation claim. It does not prove the nonempty cellular construction or
the canonical `WhiteheadTarget`. The accepted root vector remains `H3 / M4 / R4`.

## Validation

Validation ran in this worker clone on 2026-07-15. The pre-existing
`Formalizations/Lean/.lake` symlink points at the canonical pinned artifacts and was reused
read-only. No dependency update, build, clone, fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0559` | 0 | rank 607; planned; hard-statement-first partial-verification lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0559/check_obligation_tree.py` | 0 | frozen 18-obligation, 88-edge architecture passed; denominator `040c9f0d...3446fc`; root remains open M4 |
| `bash Stage1_Instances/THM-M-0559/check_proof.sh` | 0 | trust-zero narrow replay passed; six component-reduction lemmas and `empty_branch` are sorry-free and report exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0559/check_proof.py` | 0 | source hashes, frozen branch fingerprint and denominator, receipt/blocker boundary, cut set, dependency pin, and prohibited devices passed |
| prohibited-device scan over `Proof.lean` | 1 (expected) | no `sorry`, `admit`, `sorryAx`, bodyless axiom/constant/opaque, `unsafe`, `extern`, `implemented_by`, or `native_decide` matched |
| `python3 -m json.tool` on proof receipt, blocker, and worker self-test | 0 | all structured artifacts parsed |
| `git diff --check -- Stage1_Instances/THM-M-0559 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The checked proof-source SHA-256 is
`f0b1ec9ac606a8943e2aaaf711f2704caf628a33532d71709b0ff370f454b660`. The frozen, planned
`M0559-B-EMPTY` fingerprint is
`planned:v1:sha256:88b464348899c1bf86fc9c32d442c1c5658f203528e14e15f7c616c78cb9d9e4`.

## Remaining blocker

The first incomplete obligations are `M0559-N-COMPONENTS` and `M0559-B-NONEMPTY`: the new quotient
lemmas provide representative-level component coverage and path reflection, but do not yet build
component subspaces, restrict their CW structures, or recompose componentwise inverses. Beneath the
nonempty branch, the first wholly missing substantive bodies are `M0559-C-SKELETON` and
`M0559-L-EXTENSION`. Pinned
mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies the classical CW-complex definition,
homotopy groups, and homotopy equivalences, but no theorem constructing a homotopy inverse from the
frozen component and positive-dimensional homotopy-group bijections. The frozen root cut remains
`M0559-N-COMPONENTS` plus `M0559-T-FORWARD`; the nonempty branch, skeleton construction,
obstruction extension, colimit continuity, component recomposition, and exact forward-map package
remain open.

The audited external archive `jzxia/WhiteheadTheorem@ee1d4a5c332e6b95853bfa0719efd9f435317307`
contains a terminal Whitehead proof but uses Lean 4.21.0-rc3, mathlib `2239a8d`, a custom
sequential-colimit CW type, one universe, a nonempty hypothesis, and a different induced-map
predicate. It is anchor-only and has no checked bridge to this target.

There is also a scope risk: pinned mathlib's `Topology.CWComplex` deliberately does not require
Hausdorffness, and the frozen target has no `T2Space` assumptions. A disposable trust-zero probe
constructed a CW structure on two-point indiscrete `Bool`, confirming that a conventional proof
cannot silently add Hausdorffness. That example is contractible and is not presented as a
counterexample; it instead constrains any future port. If Hausdorffness is required, the statement
must be reopened and refrozen rather than changed in this proof phase.

Until the missing bodies or an exact pinned integration exist, `root_closed=false`,
`audit_complete=false`, and `theorem_complete=false`.
