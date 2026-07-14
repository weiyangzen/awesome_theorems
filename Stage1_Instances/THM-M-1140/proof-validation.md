# THM-M-1140 proof-phase validation

Item: `S56-M-1140-PROOF`. Base revision:
`a1a7e939e58f103f5ff5d23af51437fa8658aa04`.

## Implemented proof

`Proof.lean` now proves the exact local declaration
`Stage1Instances.THM_M_1140.harmonicStrongMaximumPrinciple :
HarmonicStrongMaximumPrinciple` without importing a strong maximum principle.

The analytic part constructs a Gaussian barrier on a compact tangent annulus. A
local maximum has nonpositive Laplacian, while the barrier has strictly positive
Laplacian in the annulus. Compact maximum comparison puts its maximum on the
frontier; differentiating along the inward tangent line then contradicts the
comparison inequality. This rules out a strict drop near an interior maximizer
and inhabits the frozen `InteriorLocalRigidity` package. The existing clopen
argument inhabits `ConnectedLevelPropagation`, and the frozen conditional theorem
composes both packages into the canonical target.

The zero-dimensional case is preserved. A `Nontrivial` instance is derived only
inside an assumed strict-drop contradiction, where the strict inequality supplies
distinct points. No dimension restriction, theorem substitution, or new premise
is introduced.

This is a provisional `M0-L` proof-body proposal for the 14 frozen required-machine
obligations. The frozen registry and graph retain their pre-proof M3 snapshot, as
required. In particular, the planned `M1140-L-MEAN-VALUE` semantic bridge is
implemented by an explicit Gaussian-barrier route rather than a mean-value theorem;
the integration lane must decide whether the formal output is closed as mapped or
a registry-v2 method supersession is needed before accepting closure. Human-source,
readability, provenance, trust, validation, and release gates are not claimed.

## Commands and results

Commands ran on 2026-07-15 in the worker clone. The proof checker copied the actual
owned sources to a fresh `/tmp` directory, compiled `Statement.lean`,
`ObligationTree.lean`, and `Proof.lean` to fresh oleans with the pinned Lean 4.29.0
environment via `lake env lean --trust=0`, and removed the directory on exit. It
used only the existing pinned `LEAN_PATH`. No update, build, dependency clone/fetch, network
operation, or `.lake` mutation was performed.

```text
bash Stage1_Instances/THM-M-1140/check_proof.sh
  exit 0: fresh Statement, ObligationTree, and Proof elaboration passed under
  --trust=0; the package composition, local rigidity, connected propagation, and
  exact root each reported [propext, Classical.choice, Quot.sound]

python3 -B Stage1_Instances/THM-M-1140/check_proof.py
  exit 0: exact target, frozen hashes and denominator, local proof surfaces,
  provisional receipt, pinned mathlib identity, and prohibited constructs passed

python3 Stage1_Instances/THM-M-1140/check_obligation_tree.py
  exit 0: frozen 16-obligation and 36-edge pre-proof architecture still validates

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework-required

python3 scripts/stage1_target.py show THM-M-1140
  exit 0: rank 345, planned, L0/rework-required, theorem_complete=false

rg -n -i --glob '*.lean' '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|native_decide|extern[[:space:]]' \
  Stage1_Instances/THM-M-1140/Proof.lean
  exit 1 with empty output: expected pass, no prohibited construct found

python3 -m json.tool Stage1_Instances/THM-M-1140/proof-receipt.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-1140 .stage1-worker-selftest.json
  exit 0: no scoped whitespace errors
```

The proof source SHA-256 is
`998609dc7186a333fbf3ae6220e6b7f63bd1b5c22995af1bd752a9d2d7de98ae`;
the statement source SHA-256 is
`c0f7ef8b8c003598b09d5984804630ca3d47bfde472c7748e5ee2035e6ef418a`.
An independent read-only audit in the shared workspace checked the mathematical
barrier argument, the compact maximum comparison, and the `n = 0` boundary case.
That is corroboration, not the distinct signed runner required for release.

Accepted state remains `[H2, M3, R3]` until master acceptance. The next workflow
cut is `S56-M-1140-VALIDATION`, followed by release; H0, R0, complete provenance
and trust, cold hermetic replay, independent verification, `AUDIT-Z`, `THEOREM-Z`,
and theorem completion all remain open.
