# THM-M-0394 Release Decision Handoff

## Exact verdict

`S56-M-0394-RELEASE` is **blocked**. The lifecycle remains `planned`, the frozen dossier root vector
remains `[H3, M3, R3]`, `audit_complete=false`, and `theorem_complete=false`. There are no accepted
receipt IDs and no theorem-completion promotion.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation prerequisite is `[_]`
worker evidence with `support_state=provisional_worker_selftest`, not a master-accepted dependency.
Even after dependency acceptance, `THEOREM-Z` fails exact-root kernel closure.

## Reconciliation

The frozen registry contains 17 root-relevant obligations. The proof and validation receipts give
useful same-workspace kernel evidence for the logical genus split `M0394-S3` and conditional branch
composition `M0394-B`. They explicitly report `root_closed=false`. Neither positive-genus
Diophantine finiteness nor genus-zero S-unit finiteness has a proof body, and the semantic/model
bridges, terminal `M0394-T`, and canonical root remain open.

There is also a conservative reconciliation boundary: the frozen typed graph still records
`M0394-S3` as `M3`, while the provisional proof receipt proposes local closure. Under rev-5.6's
weaker-status rule, this cannot promote the graph or root. `M0394-B` is already `M0-L` in the graph,
but only as a conditional composition consuming two unproved branches.

Source fidelity remains `H3` and readability remains `R3`; neither has independent acceptance.
The warm pinned-cache checks are not an empty-cache hermetic build, and the same-checkout validation
probe is not a distinct signed runner or independently implemented release verifier. SBOM/license,
offline replay, protected CI, deterministic bundle, and master reconciliation evidence are absent.

## Self-test evidence

Commands ran from base revision `81c2e54a7a83ea2d1470d4ce833f433e23d0141e` on 2026-07-12.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: rev-5.6 standard and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets/ranks; all L0/rework-required

python3 scripts/stage1_target.py show THM-M-0394
  exit 0: rank 7; planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0394/check_validation.py
  exit 0: frozen inputs and 17-node boundary verified; partial proof and
  independent probes elaborated; root remains open

python3 Stage1_Instances/THM-M-0394/check_release.py
  exit 0: blocked decision, unaccepted dependency, H3/M3/R3 root, 15 open
  root-relevant obligations, and both terminal decisions false

git diff --check -- Stage1_Instances/THM-M-0394 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The validation recipe reused the pre-existing canonical pinned `.lake` symlink and ran narrowly
scoped `lake env lean` checks through the recorded scripts. No update, build, clone, fetch, network
access, or `.lake` mutation occurred. This is a self-tested blocked release decision pending master
acceptance, not release-grade evidence and not theorem completion.
