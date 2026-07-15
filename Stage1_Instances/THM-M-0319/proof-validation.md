# THM-M-0319 proof worker validation

Item: `S56-M-0319-PROOF`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Validation date: `2026-07-15` (`Asia/Shanghai`)

## Implemented route

`Proof.lean` now inhabits the unchanged
`Stage1Instances.THM_M_0319.BrouwerFixedPointTarget`. A finite open-ball cover
and subordinate partition of unity send the compact convex carrier to a
standard simplex. The vendored simplex Brouwer theorem gives an approximate
fixed point, and compact minimization of `dist (f x) x` makes it exact.

`Vendor/Gametheory` contains the three-module transitive source closure for
the simplex theorem from the immutable MIT-licensed project
`math-xmum/Brouwer@c02205edf347ad45f0d62db85497598ba2c4291e`.
`VENDOR_PROVENANCE.md` and `vendor-manifest.json` record its revision, tree,
archive, license, original and port hashes, build order, and nine reversible
Lean 4.29 API compatibility edits. The local bridge is adapted from the
repository-local THM-M-0318 construction. No source from the unlicensed Harfe
candidate named by the earlier audit and blocker is used.

The frozen obligation graph predates this new route and models the Harfe/cube
architecture. The proof receipt therefore reports only an observed exact-root
kernel inhabitant and requires master graph/provenance reconciliation. It does
not claim accepted obligation closure or change the root vector.

## Commands and results

The proof recipe used only the existing pinned Lean/mathlib artifacts. The
top-level shared `flt-regular` checkout was already incomplete, so the script
queried mathlib's Lake project only for the pinned Lean executable and composed
`LEAN_PATH` from already materialized top-level build directories. It ran no
Lake update/build, dependency clone/fetch, network operation, or cache mutation.

```text
python3 Stage1_Instances/THM-M-0319/build_vendor_manifest.py
  exit 0
  PASS: 3 modules, 182363 bytes; all upstream hashes reconstructed;
  reversible patch SHA-256
  39fff43f92e646d6365f6279fd565d0d2d7b873f0922a1df9165f880a36b8790

bash Stage1_Instances/THM-M-0319/check_proof.sh
  exit 0
  Statement, Scarf, ScarfPath, Brouwer, and Proof compiled from source in a
  fresh temporary tree with --trust=0 -t0; seven declarations passed
  assert_no_sorry and each axiom report was exactly
  [propext, Classical.choice, Quot.sound]; output 975 bytes, SHA-256
  329383e3b0a5c43ba2a1c8826ea5a3d39cb542e1537693294791657a7d1d7a77

python3 Stage1_Instances/THM-M-0319/check_proof.py --require-receipt
  exit 0
  exact target, frozen denominator, licensed provenance, vendored hashes,
  proof route, source hygiene, and no-completion boundary passed

python3 Stage1_Instances/THM-M-0319/check_obligation_tree.py
  exit 0
  12 frozen obligations and 31 typed edges passed; denominator
  9d15b5ea...cee8; the unchanged pre-proof graph remains root-open

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework-required

python3 scripts/stage1_target.py show THM-M-0319
  exit 0; rank 685, planned, theorem_complete=false

python3 -m json.tool on vendor-manifest.json, proof-receipt.json, and
.stage1-worker-selftest.json
  exit 0; all structured artifacts parsed

git diff --check -- Stage1_Instances/THM-M-0319 .stage1-worker-selftest.json
  exit 0; no whitespace diagnostics on tracked changes; a separate scoped
  text scan found none in the newly added proof artifacts
```

## Status boundary

This is self-tested proof-node evidence proposing only `[_]`. It establishes a
placeholder-free exact-root kernel inhabitant in the pinned warm environment,
but changes no authoritative state. The predecessor and proof receipts await
master acceptance. Frozen-graph reconciliation, accepted E0/E1 status, full
foundation/TCB review, H0, R0, cold hermetic replay, independent validation,
downstream validation and release, `AUDIT-Z`, and `THEOREM-Z` remain open.
Therefore `theorem_complete=false`.
