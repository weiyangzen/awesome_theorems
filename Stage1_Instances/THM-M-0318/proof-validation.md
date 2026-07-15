# S56-M-0318-PROOF worker validation

Item: `S56-M-0318-PROOF`

Base revision: `557b928b377b386864527c9fb4831d45857837aa`

Validation date: `2026-07-15` (`Asia/Shanghai`)

## Implemented proof route

`Vendor/Gametheory` contains the three-module transitive project-local closure
for the finite-simplex Brouwer theorem from the immutable MIT-licensed source
`math-xmum/Brouwer@c02205edf347ad45f0d62db85497598ba2c4291e`.
`VENDOR_PROVENANCE.md` and `vendor-manifest.json` record the source archive,
revision/tree, original and port hashes, license, build order, nine exactly
reversible Lean 4.29 API edits, and one final-blank-line normalization. The
upstream source bytes reconstruct to all three independently pinned hashes.

`Proof.lean` proves a finite partition-of-unity approximation of a compact set
by a standard simplex. It sends the simplex through `f` and the barycentric
coordinate map, applies the vendored `Brouwer` theorem, and obtains approximate
fixed points in `K`. The existing compact minimization argument turns those
into an exact fixed point. `exactSchauderTarget` uses the frozen
`compose_schauder` certificate, and `schauderFixedPoint` inhabits the unchanged
canonical `SchauderFixedPointTarget` by definitional transport.

This realizes the proof-phase route for `M0318-C`, `M0318-C-NET`,
`M0318-C-MAP`, `M0318-B-BROUWER`, `M0318-L-APPROX`, `M0318-L-LIMIT`,
`M0318-L-CONT`, `M0318-T-COMPOSE`, and `M0318-ROOT`. Those obligations are
kernel-inhabited candidates only: accepted closure remains empty until the
master reconciles the frozen typed graph and provenance record.

## Commands and results

The recorded evidence recipe used the automation-provided canonical `.lake`
symlink read-only. It performs no `lake update`, `lake build`, dependency
clone/fetch, or network operation.

```text
python3 Stage1_Instances/THM-M-0318/build_vendor_manifest.py
  exit 0
  PASS: 3 modules, 182363 vendored bytes, all upstream hashes reconstructed;
  normalized compatibility-operation SHA-256
  39fff43f92e646d6365f6279fd565d0d2d7b873f0922a1df9165f880a36b8790

bash Stage1_Instances/THM-M-0318/check_proof.sh
  exit 0
  Statement, ObligationTree, Scarf, ScarfPath, Brouwer, and Proof compiled in
  a fresh temporary output tree with --trust=0 -t0; nine declarations passed
  assert_no_sorry and each axiom report was exactly
  [propext, Classical.choice, Quot.sound]
  combined output: 1253 bytes, SHA-256
  7ee90d3a951b2316689fb1d184fa47c770e5f008f74a1d29bb293f9bc77158d0

python3 Stage1_Instances/THM-M-0318/check_proof.py
  exit 0
  exact source, reversible provenance, frozen target/inventory, dependency
  pins, receipt, worker packet, hygiene, and no-completion boundary passed

python3 Stage1_Instances/THM-M-0318/check_obligation_tree.py
  exit 0
  12 frozen obligations and 12 typed nodes passed; denominator
  57d77a8f...376f87; the unchanged pre-proof graph remains root-open

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1 through 1546, all L0/rework-required

python3 scripts/stage1_target.py show THM-M-0318
  exit 0: rank 684; planned; theorem_complete=false

python3 -m json.tool on vendor-manifest.json, proof-receipt.json, and
.stage1-worker-selftest.json
  exit 0: all structured artifacts parsed

git diff --check -- Stage1_Instances/THM-M-0318 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

The recorded isolated replay ran in the pinned Lean 4.29 environment and
finished at `2026-07-15T09:46:20+08:00`. The nested-comment-aware source scan
rejects executable placeholders, bodyless declarations, unsafe/oracle hooks,
and native shortcuts. It correctly ignores `sorry` text found only in dead
nested block comments in upstream `Scarf.lean`.

After the recorded gates, an independent-audit probe outside the evidence
recipe ran `lake env lean --help` from the repository root. Lake unexpectedly
started an incomplete clone of `flt-regular` inside the canonical `.lake`
package directory. The probe was stopped, the incomplete directory was
removed, and the pinned mathlib revision/tree and clean status were rechecked.
No file from that attempt was imported, compiled, or used as evidence. This
read-only-policy violation makes an independent clean replay especially
mandatory; it is disclosed rather than counted as validation.

## Status boundary

This is proof-node evidence proposing only `[_]`. It establishes a
placeholder-free kernel inhabitant of the exact canonical root in the pinned
warm environment, but changes no authoritative state and claims no accepted
obligation closure. The prerequisite receipt and this proof receipt await
dependency-ordered master acceptance. Graph/provenance reconciliation,
accepted E0/E1 status, full foundation/TCB review, H0, R0, cold hermetic replay,
independent verification, downstream validation and release, `AUDIT-Z`, and
`THEOREM-Z` remain open. Therefore `theorem_complete=false`.
