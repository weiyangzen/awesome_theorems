# THM-M-0034 proof worker validation

Item: `S56-M-0034-PROOF`

Base revision: `6ac589f0d8c5a9eeb726a1a05def7f9467ea2e2d`

Validation date: `2026-07-15` (`Asia/Shanghai`)

## Implemented route

`Proof.lean` now supplies a placeholder-free exact-root kernel inhabitant of the unchanged
`Stage1Instances.THM_M_0034.QuillenSuslinTarget`. The vendored terminal theorem proves the stronger
statement over a principal ideal domain and an arbitrary finite variable type. The local adapter
specializes the coefficient ring to the target field and the variable type to `Fin n`; the target's
positive-dimension premise is retained but is unnecessary for the stronger theorem.

The eight-module terminal import closure comes from the Apache-2.0-noticed project
`mbkybky/QuillenSuslin` at immutable commit
`51ed173b17b274e61f759556ab3e1c090267d1bd`, tree
`264c487a24b2158bf8432459fd0b1e326acdf1eb`, and archive SHA-256
`ad8bd7662861ddf984f6c244f3b1d3eabbe4b0fd9b33f51dd85e2918d737babf`.
`PORT_PROVENANCE.md` and `vendor-manifest.json` record the complete import closure, upstream and
vendored hashes, build order, and reversible Lean 4.29/mathlib compatibility edits. Every upstream
production file declares Apache-2.0, but the archive omits the referenced root license file, so
`Vendor/LICENSE` supplies the standard Apache 2.0 text locally rather than claiming an archive
byte-copy.

## Frozen-route boundary

This proof uses the route already recorded as the informational `M0034-X-ALT-PID`. The frozen
selected proof graph instead names the unrelated, unlicensed
`edmund-ukaisi/QuillenSuslin@e8d85a6f6fa210ba0be12bd02aa22009699f0c35` body at
`M0034-X-EXTERNAL-BODY`. A worker cannot silently replace that selected revision, change terminal
body identity, or convert an informational alternative into a required proof edge. Such a change
requires a registry v2 or append-only route delta and master acceptance.

Accordingly, this packet records an observed exact-root kernel inhabitant but proposes no closed
obligation IDs. The frozen proof graph remains open at `M0034-X-EXTERNAL-BODY`; the accepted root
vector stays `H1/M3/R4`, and no authoritative state changes. This is proof-node evidence only, not
accepted graph closure, validation, release, audit completion, or theorem completion.

## Commands and results

All validation uses only the existing pinned Lean/mathlib artifacts. No `lake update`, `lake build`,
dependency clone/fetch, network operation, or `.lake` mutation is performed.

```text
python3 -B Stage1_Instances/THM-M-0034/build_vendor_manifest.py
  exit 0
  Reconstructed all eight immutable upstream modules byte-for-byte, checked the
  complete seven-edge local import closure, and verified the normalized
  compatibility operation ledger and semantic-diff digests.

bash Stage1_Instances/THM-M-0034/check_proof.sh
  exit 0
  Compiled Statement, all eight vendored modules, Proof, and ProofAudit from
  source in a fresh temporary tree with --trust=0 -t0 and strict implicit
  settings. `quillenSuslin` and the exact root passed assert_no_sorry and each
  reported exactly [propext, Classical.choice, Quot.sound].

python3 -B Stage1_Instances/THM-M-0034/check_proof.py
  exit 0
  Re-ran both checks above and passed exact target, frozen route, source
  closure, provenance, pin, receipt, no-completion boundary, and changed-path
  assertions.

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and all 1546 uniform-L0 targets passed.

python3 scripts/stage1_target.py check
  exit 0; 1546 unique ordered targets, ranks 1 through 1546, passed.

python3 scripts/stage1_target.py show THM-M-0034
  exit 0; rank 1078, planned, L0/rework-required, theorem_complete=false.

python3 -B Stage1_Instances/THM-M-0034/check_obligation_tree.py
  exit 1; known stale pre-proof inventory assertion. The frozen prerequisite
  validator's instance.json inventory predates proof artifacts. This proof
  worker did not modify prerequisite authority artifacts to manufacture a pass.

python3 -m json.tool on vendor-manifest.json, proof-receipt.json, and the root
self-test packet
  exit 0; all structured artifacts parsed without duplicate-key acceptance in
  the fail-closed proof checker.

git diff --check -- Stage1_Instances/THM-M-0034 .stage1-worker-selftest.json
  exit 0; no whitespace diagnostics. The checker separately verifies newline,
  NUL, and trailing-whitespace hygiene for the new receipt layer.
```

## Status boundary

This is self-tested proof-node evidence proposing only `[_]`. It establishes a placeholder-free
exact-root kernel inhabitant in the pinned warm environment, but the frozen proof graph remains
open and the accepted numerator remains empty. Master route reconciliation, accepted predecessor
and proof receipts, full transitive foundation and trust review, H0 source review, R0 readable
reconstruction, cold hermetic replay, independent verification, downstream validation and release,
`AUDIT-Z`, and `THEOREM-Z` remain open. Therefore `theorem_complete=false`.
