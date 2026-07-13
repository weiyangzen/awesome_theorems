# THM-M-1520 release reconciliation

Item: `S56-M-1520-RELEASE`. Base revision:
`504e508e93fd30c552d715ef48be068d5e131df2`; base tree:
`745f1603c60b7bb726e7789f08a6170c82621b6a`.

## Exact verdict

The verdict is `blocked`. Lifecycle remains `planned`, the accepted root vector remains
`[H2, M3, R3]`, and both `audit_complete` and `theorem_complete` are false. No receipt is accepted
and no theorem-completion promotion is claimed.

The first failed release-node gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`:
`S56-M-1520-VALIDATION` is only a provisional `[_]` worker projection. Its receipt is
`accepted=false`, `release_grade=false`, and has no master acceptance. The validation receipt in
turn records proof master acceptance as its first failed predecessor gate.

## Evidence reconciliation

The frozen target elaborates, and the recorded validation worker obtained useful provisional
trust-zero results for partial and conditional declarations. Those results do not prove the exact
root. `LiouvilleAnalyticPackage` is an unconstructed premise; the only closed graph node is the
conditional assembly `M1520-T-ASSEMBLE`. The root remains M3/open, with `M1520-T-ALL-TIMES` as its
minimal cut and `M1520-C-VARIATION.kernel_closure` as the first missing analytic theorem gate.

The current integrated checkout also cannot replay the validation recipe exactly as recorded.
`check_validation.py` is hard-bound to the validation worker's prior base and phase-specific root
`.stage1-worker-selftest.json`; the current root packet belongs to this release handoff, so the
historical checker exits before the Lean replay. This does not invalidate the content-addressed
historical worker observation, but it prevents treating
that observation as a current, self-contained validation dependency or release recipe.

`AUDIT-Z` is independently blocked. The source remains H2 without an accepted primary proposition,
assumption/errata/node crosswalk, or independent source review. Readability remains R3 without an
independently accepted R0 reconstruction. Foundation, transitive provenance, and the complete TCB
remain open.

`THEOREM-Z` is also blocked. There is no premise-free root proof, immutable clean release input,
cold empty-cache network-denied build, offline restoration, complete SBOM/license archive, two
signed independent-runner attestations, independently implemented minimal verifier, protected
adversarial CI result, or deterministic build-twice evidence bundle. The automation-provided
`.lake` symlink is a shared warm cache and is classified only as nonrelease evidence.

## Validation

Commands ran on 2026-07-14 (`Asia/Shanghai`). No dependency update, build, clone, fetch, or `.lake`
mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1520
  exit 0: rank 189 remains planned, L0/rework-required, and theorem-incomplete

python3 Stage1_Instances/THM-M-1520/check_obligation_tree.py
  exit 0: 16 obligations and 32 typed edges passed; root open M3; analytic package M4

cd Formalizations/Lean && lake env lean --trust=0 -t0 \
  ../../Stage1_Instances/THM-M-1520/Statement.lean
  exit 0: pinned Lean 4.29.0 elaborated the exact canonical LiouvilleStatement as Prop

python3 -I -B Stage1_Instances/THM-M-1520/check_validation.py
  exit 1: expected fail-closed current replay; the recorded base and phase packet are unavailable

python3 -I -B Stage1_Instances/THM-M-1520/check_release.py
  exit 0: hashes, authority, receipt boundary, open root, and negative terminal decisions passed

python3 -O -I -B Stage1_Instances/THM-M-1520/check_release.py
  exit 1 as expected: the checker refuses Python execution with assertions disabled

python3 -m json.tool on release-spec.json, release-decision.json, release-receipt.json, and the
worker packet
  exit 0 for each structured artifact

git diff --check -- Stage1_Instances/THM-M-1520 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

Retry requires dependency-ordered master acceptance, a placeholder-free construction of the full
analytic package and exact root, accepted H0/R0 and trust/provenance/TCB closure, a self-contained
structured replay, and the full cold/offline/independent deterministic release protocol.

Status boundary: this artifact self-tests only the truthful negative release decision. It is not
release-grade evidence, an accepted receipt, theorem completion, or master acceptance.
