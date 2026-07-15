# THM-M-0927 release reconciliation

Item: `S56-M-0927-RELEASE`. Base revision:
`062e0b530c644c6d9c62556518568dd91a7374cd`; base tree:
`0879a3d554dc3011e1c5b513107c330547ea185c`. Decision date: 2026-07-15
(Asia/Shanghai).

## Verdict

`blocked`. This release worker accepts no receipt, obligation, debt promotion,
lifecycle transition, or theorem state. The authoritative lifecycle remains
`planned`, the accepted root remains `[H1, M3, R4]`, and both `AUDIT-Z` and
`THEOREM-Z` remain false.

The current exact radical root does have useful provisional machine evidence. A
fresh current-head direct replay elaborates `Statement.lean`,
`ObligationTree.lean`, `Proof.lean`, and the differential `Validation.lean` at
trust level zero. The proof root and the direct recomposition are sorry-free and
report exactly `propext`, `Classical.choice`, and `Quot.sound`; the closure has
12,891 declarations in 509 modules with no unexpected bodyless or unsafe
declaration. This is a current warm-cache observation, not accepted `M0-W` or
release evidence.

## Reconciliation

The direct prerequisite `S56-M-0927-VALIDATION` is only scheduler-provisional
`[_]`. Its receipt is `accepted=false`, `release_grade=false`, and `blocked`, so
the first node gate is
`dependency.S56-M-0927-VALIDATION.master_acceptance`. Its own first failure is
proof master acceptance.

The structured authority has not admitted the later proof observations:
`instance.json` is still `planned` at `[H1, M3, R4]` with no accepted receipt;
`task-dag.json` keeps every downstream task open; and `typed-graphs.json` has no
accepted closure, still lists `M0927-T-FUNCTION-BINET` in the root cut, and
retains eight unverified decomposition plans. The release worker records this
conflict at the weaker status and does not rewrite predecessor artifacts.

Primary-source `H0` and independently reviewed `R0` evidence are absent. There
is no accepted foundation policy or complete transitive proof-origin, compiled
artifact, TCB, computation, SBOM, license, and archive closure. The first
reproduction failure is `S56-10.6-HERMETIC-COLD-EMPTY-CACHE`: the replay reads
the shared pinned warm `.lake`, rather than rebuilding from immutable clean
input and an empty cache with offline restoration. There are no two signed
independent clean runners, independently implemented minimal verifier,
protected mutation/adversarial CI, or deterministic content-addressed release
bundle.

## Commands and results

No `lake update`, `lake build`, dependency clone/fetch, checkout repair, or
`.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0927` | 0 | Rank 1546; planned, L0/rework-required, theorem incomplete. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0927/check_release.py` | 0 | Current hashes, dependency state, structured authority, fresh trust-zero replay, and the blocked release decision passed. |
| `/usr/bin/python3 -m json.tool` on the release JSON artifacts and root worker packet | 0 | All structured artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0927-release-pycache /usr/bin/python3 -m py_compile Stage1_Instances/THM-M-0927/check_release.py` | 0 | Checker compiled outside the repository. |
| `PYTHONOPTIMIZE=1 /usr/bin/python3 -B Stage1_Instances/THM-M-0927/check_release.py` | 1 expected | Fail-closed guard rejected disabled assertions before evidence checks. |
| `git diff --check -- Stage1_Instances/THM-M-0927 .stage1-worker-selftest.json` | 0 | No scoped whitespace diagnostics. |

The integrated validation checker is deliberately not cited as a current
replay. It is bound to base revision
`c93e664d3a7e0383b037cfa2d5e47ba14adfb2cb` and its validation worker packet.
The release checker authenticates that historical provisional receipt and runs
the narrow current-head replay independently of that snapshot assertion.

## Status boundary

This artifact self-tests only a truthful negative release decision. It proposes
`[_]` for master review of the release-phase report, not for the theorem. It
grants no `H0`, `M0-W`, `E0/E1`, `R0`, `AUDIT-Z`, `THEOREM-Z`, release,
theorem-completion, accepted-state, or master-acceptance credit.
