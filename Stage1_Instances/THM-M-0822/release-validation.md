# THM-M-0822 release reconciliation

Item `S56-M-0822-RELEASE` has the exact verdict `blocked`. The lifecycle remains
`planned`, the accepted root vector remains `[H1, M3, R4]`, and both
`audit_complete` and `theorem_complete` are false. This worker accepts no receipt
or obligation and proposes only `[_]` for integration review of this negative
decision.

## First failed gate

`S56-10.2-DEPENDENCY-ACCEPTANCE` fails first. `S56-M-0822-VALIDATION` is only a
provisional `[_]` worker projection. Its receipt has `accepted=false` and
`release_grade=false`, and records proof master acceptance as its nested first
failure. The release node therefore is not dependency-legal for master
acceptance.

The first release-specific failure is immutable clean input. The next is
`S56-10.6-HERMETIC-COLD-BUILD`: the available replay uses the
automation-provided shared warm pinned `.lake` closure. It is neither an
empty-cache cold build nor a content-addressed offline restoration.

## Evidence reconciled

The positive machine evidence is real but provisional. The existing
network-isolated `--trust=0` replay elaborates the exact maximum-value target,
all six frozen composition certificates, the target-owned attaining-star
route, `Finset.erdos_ko_rado`, and
`Stage1Instances.THM_M_0822.Proof.erdosKoRadoMaximum`. All selected declarations
are sorry-free, and the root reports exactly `propext`, `Classical.choice`, and
`Quot.sound`.

That replay does not alter the weaker accepted authority. The instance and
typed graph retain an empty accepted receipt/obligation set and `root_closed=false`.
The instance merge inventory is also phase-stale: it stops at obligation-tree
artifacts and does not yet list the proof or validation artifacts. Release
records that disagreement rather than rewriting predecessor authority.

`AUDIT-Z` remains blocked by missing accepted H0 source translation, errata
disposition, node mapping, and independent review; missing independently
reviewed R0 reconstruction; and unreconciled evidence links across the frozen
inventory. `THEOREM-Z` additionally lacks accepted machine closure, a complete
foundation/provenance/trust/TCB boundary, content-addressed SBOM and license
archive, immutable clean cold/offline reproduction, deterministic build-twice
bundle, two distinct signed runner attestations, an independently implemented
minimal verifier, protected release CI, and master acceptance.

## Commands and results

Commands ran from the worker clone on 2026-07-15 (Asia/Shanghai). The pinned
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, dependency mutation, or network request ran.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0822` | 0 | Rank 1380; planned; L0/rework-required; theorem incomplete. |
| `bash Stage1_Instances/THM-M-0822/check_validation.sh` | 0 | Network-isolated trust-zero exact-root replay passed; the root was sorry-free with exactly the three recorded axioms. |
| `python3 -I -B Stage1_Instances/THM-M-0822/check_release.py` | 0 | Target, DAG, hashes, authority boundary, kernel replay, and blocked `AUDIT-Z`/`THEOREM-Z` decisions passed. |
| `python3 -O -I -B Stage1_Instances/THM-M-0822/check_release.py` | 1 | Expected: the checker refuses optimized Python with assertions disabled. |
| `python3 -m json.tool` on the three release JSON artifacts and worker packet | 0 | All structured artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0822-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0822/check_release.py` | 0 | Checker syntax compiled outside the repository. |
| `git diff --check -- Stage1_Instances/THM-M-0822 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics. |

The release checker is the terminal node-specific recipe. It also invokes
`check_validation.sh`, so the exact Lean replay is performed again inside the
reconciliation rather than accepted from prose or from the historical receipt
alone.

Status boundary: this is only a self-tested negative release decision. It
grants no accepted `H0`, `M0`, `E0/E1`, `R0`, `AUDIT-Z`, `THEOREM-Z`, release,
theorem-completion, independent-verification, or master-acceptance credit.
