# THM-M-0590 release-phase reconciliation

Item: `S56-M-0590-RELEASE`. Base revision:
`fd50bb07f6632a2ad0bdc17737c200432ee242c8`; base tree:
`ed66432029954bfa5b17e0afda5f3817eeb32d48`.

## Exact verdict

The release verdict is `blocked`. Lifecycle remains `planned`, the conservative root vector remains
`[H1, M4, R3]`, and both `audit_complete` and `theorem_complete` are false. No receipt or new frozen
obligation is accepted, and this worker makes no release or theorem-completion claim.

The first workflow failure is `S56-10.2-DEPENDENCY-ACCEPTANCE`. The validation receipt is only
provisional worker evidence, explicitly has `accepted=false` and `release_grade=false`, and has no
dependency-ordered master acceptance. Independently, the exact theorem gate fails because neither
directional BDF package has a proof body. The open root cut is `M0590-B-FORWARD` and
`M0590-T-BACKWARD`.

## Evidence reconciliation

The current narrow replay elaborates the exact statement, the conditional composition declaration,
five local support declarations, and three same-worker probes at trust level zero. The nine proof
declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`; the probes report 18,827
transitively used declarations across 752 modules, with no bodyless nonaxiom or unsafe declaration.
This is useful warm-cache nonrelease evidence. It does not construct either directional package,
close the premise-free root, or create an accepted obligation receipt.

The integrated validation receipt remains internally consistent with its recorded owned input
hashes and negative decision, but its recipe is pinned to base `e73a459aa33f8b656019c9c36e3d5dfc84dffc30`
and the validation-phase root packet. At the current release base it exits before Lean at the exact
HEAD assertion. The release checker therefore records that historical boundary and performs its own
fresh bounded replay rather than treating the stale recipe as current release validation.

`AUDIT-Z` is independently blocked because source-boundary and evidence classification, review, and
public projection reconciliation remain incomplete. The source crosswalk lacks an accepted exact
theorem/page, assumption and errata mapping, and independent source review. The typed evidence graph
is empty, and root provenance, foundation, TCB, and review records remain pending. The retained H1
and R3 debts separately prevent `THEOREM-Z`. The README and intake also retain statement-era
M3/open-gate prose while later structured evidence records exact target elaboration and M4; this
worker records the disagreement without rewriting authoritative or public state.

Release additionally lacks immutable clean input, a cold empty-cache offline-restorable build,
complete transitive provenance/TCB/SBOM/license closure, two distinct signed runners, an independently
implemented minimal verifier, protected adversarial CI, and a deterministic build-twice evidence
bundle. The automation-provided `.lake` symlink is a shared warm cache and is nonrelease evidence.

## Commands and exact results

Commands ran from the worker clone on 2026-07-15 (Asia/Shanghai). The pinned `.lake` symlink was
reused read-only. No dependency update, build, clone, fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0590` | 0 | Rank 630; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0590/check_obligation_tree.py` | 0 | 17 obligations and 37 typed edges passed; root and both directional packages remain open M4. |
| `Stage1_Instances/THM-M-0590/check_proof.sh` | 0 | Statement, conditional composition, and five partial bodies elaborated at trust zero; no sorry; allowed axioms only. |
| `python3 -I -B Stage1_Instances/THM-M-0590/check_validation.py` | 1 | Expected current-snapshot fail-closed result: the historical checker rejects the changed HEAD before running Lean. |
| `python3 -I -B Stage1_Instances/THM-M-0590/check_release.py` | 0 | Current hashes, dependency state, graph boundary, network-isolated trust-zero warm replay, and blocked release decision passed. |
| `python3 -O -I -B Stage1_Instances/THM-M-0590/check_release.py` | 1 | Expected: checker refuses Python execution with assertions disabled. |
| `python3 -m json.tool <file>` for each release and worker JSON artifact | 0 | All structured artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0590-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0590/check_release.py` | 0 | Checker syntax compiled outside the repository. |
| `git diff --check -- Stage1_Instances/THM-M-0590 .stage1-worker-selftest.json` | 0 | No tracked-diff diagnostics; `check_release.py` separately checked byte-level text hygiene on every changed untracked output. |

## Status boundary

This artifact self-tests only a truthful negative release decision. It proposes `[_]` for master
review of the release-phase report, not for the theorem. It grants no `H0`, `M0`, `E0/E1`, `R0`,
`AUDIT-Z`, `THEOREM-Z`, release, theorem-completion, accepted-state, or master-acceptance credit.

Retry first requires exact placeholder-free bodies for both directional packages and every required
dependency, root composition, and fresh dependency-legal proof and validation acceptance. It then
requires H0/R0 and audit review, reconciled public/evidence state, complete trust and supply-chain
closure, and the full cold/offline/independent/deterministic release protocol.
