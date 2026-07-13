# THM-M-0041 release reconciliation

Item `S56-M-0041-RELEASE` has the exact verdict `blocked`. The lifecycle remains `planned`, the
authoritative root vector remains `[H1, M3, R3]`, and both `audit_complete` and `theorem_complete`
are false. This is a tested negative release decision, not a release or theorem-completion claim.

## Evidence reconciliation

The proof and validation receipts contain useful provisional exact-root evidence. The exact frozen
Cayley-Hamilton target, the local proof routes, and a separately written wrapper over pinned
`Matrix.aeval_self_charpoly` elaborate with only `propext`, `Classical.choice`, and `Quot.sound`.
The release checker repeats the statement plus differential wrapper check in a fresh `/tmp`
directory with the pinned `lake env lean` executable and explicit `LEAN_PATH`.

That kernel replay cannot override structured authority. Every predecessor receipt is `[_]` and
`accepted=false`; the direct validation prerequisite is not master-accepted and is explicitly
`release_grade=false`. The instance and graph retain no accepted receipt or closed obligation,
`root_closed=false`, and the remaining root cut is `M0041-T-CHARPOLY`,
`M0041-A-MATHLIB-ANCHOR`, `M0041-X-SOURCE`, `M0041-S-FOUNDATION`,
`M0041-X-PROVENANCE`, `M0041-X-TRUST`, `M0041-X-READABLE`, and
`M0041-X-WORKFLOW`.

`AUDIT-Z` fails because the source-boundary and readability inventories, graph reconciliation, and
provenance/foundation/trust classifications are not complete and accepted. Open H/R debt alone would
not prevent an otherwise complete audit. `THEOREM-Z` also fails because
there is no immutable clean empty-cache offline replay, complete SBOM/license and dependency archive,
two signed independent-runner attestations, independently implemented minimal release verifier, or
deterministic content-addressed release bundle.

## Commands and results

Commands ran from the worker clone at base revision
`2bfb272c83b2089e9b285d48dce2c30616ff6c36`. The pre-existing canonical `.lake` symlink was reused
read-only. No update, build, clone, fetch, dependency mutation, or network operation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0041
  exit 0: rank 1081, planned L0/rework-required target; theorem_complete=false

python3 -B Stage1_Instances/THM-M-0041/check_release.py
  exit 0: exact-root temporary Lean replay passed; blocked dependency, AUDIT-Z, and THEOREM-Z
  decisions agree with the authoritative instance, graph, receipts, and remaining root cut

python3 -m json.tool Stage1_Instances/THM-M-0041/release-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0041/release-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0041-release-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0041/check_release.py
  exit 0: checker syntax passed without cache output in the owned path

rg -n -i --glob '*.lean' \
  '\b(sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]' \
  Stage1_Instances/THM-M-0041/{Statement,Proof,Validation}.lean
  exit 1 with empty output: expected no-match result

git diff --check -- Stage1_Instances/THM-M-0041 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

The first failed release-node gate is
`dependency.S56-M-0041-VALIDATION.master_acceptance`. The earliest missing release-assurance gate is
`S56-10.6-HERMETIC-COLD-BUILD`. The release item is self-tested for a provisional `[_]` handoff;
the theorem remains unfinished and only the integration lane may accept or promote state.
