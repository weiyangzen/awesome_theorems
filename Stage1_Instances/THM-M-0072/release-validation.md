# THM-M-0072 release reconciliation

Item: `S56-M-0072-RELEASE`. Base revision:
`d44ed2b11fb201a761afad9b133caa8bc97fd710` (tree
`9602084a1c32fa6685f1c60eff540528226decff`).

## Exact verdict

`blocked`. The lifecycle remains `planned`, the accepted root vector remains
`[H1, M3, R4]`, and both `AUDIT-Z` and `THEOREM-Z` are blocked. Therefore
`audit_complete=false`, `theorem_complete=false`, and the accepted receipt list
remains empty. This worker accepts no receipt and makes no theorem-completion or
release claim.

The first failed gate is
`dependency.S56-M-0072-VALIDATION.master_acceptance`. The prerequisite validation
receipt is only a provisional `[_]` worker packet with `accepted=false` and
`release_grade=false`. Release is consequently not dependency-legal.

## Evidence reconciliation

The integrated proof is meaningful provisional evidence. A fresh current-base
replay copies `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and
`Validation.lean` to a temporary directory and elaborates them in order with the
pinned Lean executable, `--trust=0 -t0`, a read-only host and dependency closure,
and a Bubblewrap network namespace. Fourteen declarations are sorry-free, the
exact root and exact-type aliases elaborate, and their reported axioms are exactly
`propext`, `Classical.choice`, and `Quot.sound`.

This does not override structured authority. `instance.json` and
`typed-graphs.json` remain the honest pre-proof snapshot: `H1/M3/R4`, no accepted
receipt or obligation, `root_closed=false`, and `M0072-T-OUTSIDE` as the remaining
root cut in accepted state. The proof and validation receipts propose root `M0-L`, but neither is
master accepted or reconciled into the graph.

The historical validation receipt is content-bound but its recorded recipe is not
fresh at this release base. Running
`python3 -I -B Stage1_Instances/THM-M-0072/check_validation.py --probe` exits 1 at
the deliberate base-revision assertion because that phase checker binds
`97cd9c492d95baa9b55d2d8b341844107f07e686`, while this integrated checkout is
`d44ed2b11fb201a761afad9b133caa8bc97fd710`. The release checker records the
staleness and performs its own current-base narrow replay rather than modifying or
misrepresenting the historical receipt.

`AUDIT-Z` is unavailable because source-boundary, evidence, task, graph, and debt
projections are not accepted and reconciled. The pinpoint 1968 source remains
`H1`: the catalog says 1964 and no independent source reviewer has accepted the
identity correction, preservation/errata record, or complete node crosswalk. No
independently accepted `R0` reconstruction exists.

The first release-specific failure is `S56-10.6-IMMUTABLE-CLEAN-INPUT`. The worker
uses the automation-provided untracked shared warm `.lake` symlink. There is no
empty-cache cold build, offline restoration archive, complete TCB/provenance,
SBOM/license closure, deterministic build-twice evidence bundle, two signed
separately provisioned runners, or independently implemented minimal verifier.

## Commands and results

Commands ran from the repository root. No `lake update`, `lake build`, dependency
clone/fetch, checkout, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0072/check_release.py` | 0 | Current-base network-isolated exact-root replay passed; release reconciliation derived `blocked`, unchanged `H1/M3/R4`, and both terminal decisions false. |
| `python3 -I -B Stage1_Instances/THM-M-0072/check_validation.py --probe` | 1 (expected fail-closed) | Historical validation checker rejected current HEAD at its base-revision guard; it was not cited as fresh release evidence. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0072` | 0 | Rank 1102 remains planned, rework-required, and theorem-incomplete. |
| `python3 -m json.tool` over the release decision, receipt, spec, and worker packet | 0 | All structured release artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0072-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0072/check_release.py` | 0 | Checker syntax compiled outside the repository. |
| `git diff --check -- Stage1_Instances/THM-M-0072 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

## Status boundary

This is a self-tested negative release decision for master review. It grants no
accepted `M0-L`, `H0`, `R0`, `E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release,
theorem-completion, independent-verification, or master-acceptance credit.
