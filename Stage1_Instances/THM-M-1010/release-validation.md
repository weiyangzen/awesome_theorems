# THM-M-1010 release reconciliation

Item: `S56-M-1010-RELEASE`

Base revision: `43f55bb87aa8883be277a6660f49c6f8ba647082`

Decision date: `2026-07-15` (`Asia/Shanghai`)

## Exact verdict

`blocked`. The lifecycle remains `planned`, the authoritative root vector remains
`[H1, M3, R3]`, and both `audit_complete` and `theorem_complete` remain false. This worker accepts
no receipt and makes no `E0`, `E1`, accepted `M0`, `AUDIT-Z`, `THEOREM-Z`, release,
theorem-completion, or master-acceptance claim. The release receipt is explicitly
`release_grade=false`.

The first failed workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`:
`S56-M-1010-VALIDATION` is provisional `[_]`, `accepted=false`, `release_grade=false`, stale at
this integrated base, and not master accepted. The first theorem gate is
`M1010-N-PARTITIONS`; the first reproduction gate is `S56-10.6-HERMETIC-COLD-BUILD`.

## Evidence reconciliation

The frozen exact statement elaborates. A current narrow replay copies `Statement.lean`,
`ObligationTree.lean`, `Proof.lean`, and `Validation.lean` into a fresh temporary target directory
and invokes pinned Lean with `--trust=0` while the release checker runs under
`bubblewrap --unshare-net`. The conditional composer and three partial proof bodies elaborate. All
seven axiom reports list exactly `propext`, `Classical.choice`, and `Quot.sound`; four validation
sorry checks pass; the audited closure contains no bodyless nonaxioms or unsafe declarations.

This is current nonrelease evidence only. `target_of_couplingPackage` is conditional on an
uninhabited package. `exists_common_space_exact_marginals` constructs independent representatives
with the correct laws but gives no almost-sure convergence. The other declarations cover only
constant-law sequences. There is no unconditional inhabitant of `CouplingPackage` or `Target`, so
the five-node cut remains open and the root stays `M3`.

The archived validation receipt remains useful historical evidence, but its recorded checker is
not current-replayable. It requires revision `fd995645725ec3633e4da7e6d759deb14f530861`, the old
validation state `[ ]` with zero attempts, and a validation worker packet. At this integrated base it
stops before Lean. The release checker records that expected freshness failure and performs a
separate current narrow replay rather than misreporting the predecessor recipe as passing.

`AUDIT-Z` is false independently. The primary source is identified only at `H1`; exact theorem/page
wording, assumptions, errata, node mapping, and independent review remain open. No accepted
independently reviewed `R0` reconstruction exists. Release also lacks accepted complete
proof-body provenance and TCB closure, an immutable empty-cache cold build, offline restoration,
SBOM/licenses, two signed independent runners, an independently implemented minimal verifier,
protected adversarial CI, and a deterministic content-addressed evidence bundle.

## Commands and results

Commands ran inside the worker clone on `2026-07-15`. No command ran `lake update`, `lake build`,
dependency clone/fetch, or mutated `.lake`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | Exactly 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1010` | 0 | Rank 290 remains planned, L0/rework-required, and theorem-incomplete. |
| `python3 -B Stage1_Instances/THM-M-1010/check_obligation_tree.py` | 1 | Structural assertions reached the Lean step, whose second import ignored the temporary `LEAN_PATH` and searched the shared local build path; no release evidence is credited to this failed legacy helper. The release checker independently validates the 15-obligation registry and graph. |
| `bash Stage1_Instances/THM-M-1010/check_proof.sh` | 0 | The statement, conditional composer, and three partial bodies elaborated under trust zero; zero frozen obligations closed; proof and theorem completion remained false. |
| `python3 -I -B Stage1_Instances/THM-M-1010/check_validation.py --probe` | 1 (expected freshness failure) | The predecessor checker stopped before Lean because its required base and validation DAG state are stale. |
| recorded `bubblewrap --unshare-net ... python3 -I -B Stage1_Instances/THM-M-1010/check_release.py` recipe | 0 | Current hashes, authority, narrow trust-zero replay, and blocked terminal decisions agreed. |
| `python3 -m json.tool` on the release spec, decision, receipt, and worker packet | 0 | Every structured release artifact parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m1010-release-pycache python3 -m py_compile Stage1_Instances/THM-M-1010/check_release.py` | 0 | The checker compiled with generated output outside the repository. |
| `git diff --check -- Stage1_Instances/THM-M-1010 .stage1-worker-selftest.json` plus the checker's byte scan | 0 | No whitespace, final-newline, CR, NUL, or trailing-space error was found. |

Retry requires master-accepted exact bodies for the five-node cut and their composition into
`Target`; accepted H0/R0 and `AUDIT-Z`; accepted foundation, provenance, and TCB closure; cold
offline supply-chain evidence; independent runner and minimal-verifier agreement; a deterministic
signed bundle; and final master `THEOREM-Z` reconciliation.

Status boundary: this packet self-tests only the truthful negative release decision. It supplies no
accepted receipt, audit completion, theorem completion, release, or master acceptance.
