# THM-M-1078 release decision

Item: `S56-M-1078-RELEASE`. Base revision:
`e04243daf889845e1649146b8777095223d800ba`; base tree:
`64f87b307e68abee8e4a7a19f511dbf28dbf1e39`.

## Exact verdict

The release verdict is **blocked**. The lifecycle remains `planned`; no receipt or obligation is
accepted. The intake authority remains `[H1, M4, R4]`, while the latest provisional graph remains
`[H2, M2, R4]`. The conflict is not silently normalized: both projections are preserved pending
master reconciliation, and neither `AUDIT-Z` nor `THEOREM-Z` is accepted. Consequently
`audit_complete=false` and `theorem_complete=false`.

The first node gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`. Validation is only `[_]` worker evidence;
its receipt is `accepted=false`, `release_grade=false`, and bound to an older phase snapshot. The
release item therefore cannot be dependency-legal or accepted.

## Evidence reconciliation

The exact canonical statement is frozen. The current narrow Lean replay proves only two genuine
horizon-local declarations: conditional expectation preserves `MemLp` in the target exponent
range, and terminal `MemLp (f n)` propagates to `k <= n`. Both declarations elaborate at trust
level zero with only `propext`, `Classical.choice`, and `Quot.sound` reported.

That body does not close the target. The frozen `EarlierMemLpBridge` asks for `MemLp (f k)` for
every future `k`, while the proof establishes it only through the terminal horizon. The conditional
root composer therefore cannot consume the proved body. The external Burkholder declaration is
absent from the pinned dependency closure, and predictability and norm bridges also remain open.
The exact frozen cut is:

- `M1078-C-EXTERNAL-PIN`
- `M1078-T-ALLTIME`
- `M1078-B-PREDICTABLE`
- `M1078-B-NORM`

There is also unresolved authority drift. `instance.json` and `README.md` still carry the intake
claim that the exact formal statement is open and record `[H1, M4, R4]`; the later provisional
graph records the exact target and `[H2, M2, R4]`. The local task DAG has no accepted state. The
proof receipt names `M1078-T-ALLTIME`, but its proved formula differs from the all-future composer
interface. No accepted closure is inferred from any of those surfaces.

Release assurance remains absent: there is no accepted pinpoint source or independently reviewed
`R0`, complete transitive provenance/foundation/TCB/SBOM closure, immutable empty-cache cold and
offline restoration, deterministic content-addressed bundle, two distinct signed clean runners,
independent minimal verifier, protected adversarial CI, or master acceptance.

## Commands and results

Commands ran in the isolated worker clone on 2026-07-15 (`Asia/Shanghai`). The scheduler-provided
canonical `.lake` symlink was reused without mutation. No `lake update`, `lake build`, dependency
clone/fetch, or network request was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1078` | 0 | rank 520; planned L0/rework-required; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before release artifacts, only the scheduler-provided `Formalizations/Lean/.lake` symlink was untracked |
| execute the archived `validation-spec.json` `argv` at the release HEAD | 1 expected | freshness assertion rejected the old hard-coded validation base before Lean replay; no stale success was claimed |
| `python3 -B Stage1_Instances/THM-M-1078/check_obligation_tree.py` | 0 | 15 obligations and 51 typed edges passed; exact root open M2 |
| `python3 -B Stage1_Instances/THM-M-1078/check_proof.py` | 0 | horizon-local proof unit passed; frozen interface mismatch remained |
| `cd Formalizations/Lean && lake env lean --trust=0 -j1 -t0 ../../Stage1_Instances/THM-M-1078/Proof.lean` | 0 | both partial declarations elaborated; each reported only the three selected classical axioms |
| `bash Stage1_Instances/THM-M-1078/check_exact_composition.sh` | 0 | conditional composer and generated exact-target transport elaborated; open premises remained |
| `python3 -B Stage1_Instances/THM-M-1078/check_release.py --worker-packet .stage1-worker-selftest.json` | 0 | hashes, authority drift, exact open cut, current Lean replay, and blocked terminal decisions agreed |
| `python3 -m json.tool` over release spec, decision, receipt, and worker packet | 0 | all release JSON artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m1078-release-pycache python3 -m py_compile Stage1_Instances/THM-M-1078/check_release.py` | 0 | release checker syntax checked outside the owned target path |
| `git diff --check -- Stage1_Instances/THM-M-1078 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status boundary

This is a self-tested negative release reconciliation. It advances no lifecycle or debt state and
claims no accepted receipt, accepted obligation, `M0-*`, `E0/E1`, `H0`, `R0`, `AUDIT-Z`,
`THEOREM-Z`, theorem completion, release-grade evidence, or master acceptance.

Reopen only after repairing and kernel-closing the exact proof route, obtaining dependency-ordered
master acceptance through validation, reconciling structured and public state, and then completing
the full cold/offline, provenance, supply-chain, independent-verifier, CI, bundle, and master gates.
