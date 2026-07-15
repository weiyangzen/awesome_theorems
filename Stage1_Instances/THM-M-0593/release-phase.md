# THM-M-0593 release decision

Item: `S56-M-0593-RELEASE`. Base revision:
`e46e0735d0940bb558acaf027d8386de2579f55d`; base tree:
`9f03ecc77e82eda1f0ea3f0f4b08d1d7419ce0cf`.

## Exact verdict

The release verdict is **blocked**. The lifecycle remains `planned`; no receipt or obligation is
accepted. The authoritative root vector remains `[H1, M4, R4]`. Later proof and validation
evidence only provisionally support `[H1, M2, R4]`, and the exact root remains open. Neither
`AUDIT-Z` nor `THEOREM-Z` is accepted, so `audit_complete=false` and
`theorem_complete=false`.

The first failed node gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`. Validation is only `[_]` worker
evidence: its receipt has `accepted=false`, `release_grade=false`, and no integration-lane
acceptance. The release item therefore cannot be dependency-legal or accepted.

## Evidence reconciliation

The current narrow replay checks the exact Euclidean statement, frozen conditional composition,
the zero-codomain and `m < n` proof bodies, and the separately written same-worker validation
probes. All seven theorem declarations are sorry-free and report no principles beyond `propext`,
`Classical.choice`, and `Quot.sound`.

This is not a proof of Sard's theorem. The only root-facing proof declaration is
`sardTarget_of_hardDimensionBranch (hard : HardDimensionBranch) : SardTarget`. No declaration
constructs the hard `0 < n` and `n <= m` branch. The authoritative frozen cut remains
`M0593-L-DIMENSION-IMAGE`, `M0593-L-RANK-REDUCTION`, and `M0593-L-TAYLOR`; provisional branch
evidence only removes `M0593-L-DIMENSION-IMAGE` from that cut. No accepted state changes.

Structured scope is also unreconciled. `instance.json` and `README.md` retain the intake manifold
paraphrase and say the exact formal statement is open. `Statement.lean` and `statement.md` later
freeze the narrower Euclidean open-region specialization selected from Sard's 1942 paper. The local
task DAG remains all open, while the global scheduler marks prior phases only worker-provisional.
Under the weaker-state rule, none of these surfaces can promote closure.

The archived validation receipt remains hash-bound provisional evidence, but its checker is tied to
its earlier revision, earlier DAG state, and validation-phase root packet. The release checker does
not misreport that phase-bound recipe as current. It performs a fresh trust-zero replay against the
same pinned sources instead. That replay uses fresh target outputs but the scheduler-provided shared
warm `.lake` closure, so it is nonrelease evidence.

Release assurance remains absent: there is no accepted H0 source review, independently accepted R0
reconstruction, complete transitive provenance/foundation/TCB/SBOM closure, immutable clean cold and
offline replay, deterministic content-addressed bundle, two distinct signed runners, independent
minimal verifier, protected adversarial CI, or master acceptance.

## Commands and results

Commands ran in the isolated worker clone on 2026-07-15 (`Asia/Shanghai`). The canonical `.lake`
symlink was reused without mutation. No `lake update`, `lake build`, dependency clone/fetch, or
network request was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0593` | 0 | rank 633; planned L0/rework-required; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before release artifacts, only the scheduler-provided `Formalizations/Lean/.lake` symlink was untracked |
| `python3 -I -B Stage1_Instances/THM-M-0593/check_obligation_tree.py` | 0 | 22 obligations and 43 typed edges passed; authoritative root remains open M4 |
| `python3 -I -B Stage1_Instances/THM-M-0593/check_release.py --worker-packet .stage1-worker-selftest.json` | 0 | hashes, authority conflict, fresh partial Lean replay, open root cuts, and blocked terminal decisions agreed |
| `python3 -m json.tool` over release spec, decision, receipt, and worker packet | 0 | all structured release artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0593-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0593/check_release.py` | 0 | release checker syntax checked without repository bytecode |
| `git diff --check --no-index /dev/null Stage1_Instances/THM-M-0593/check_release.py` | 1 expected for new content | empty output; representative new-file whitespace check passed, and the checker directly checked every handoff file |

## Status boundary

This is a self-tested negative release reconciliation. It advances no lifecycle or debt state and
claims no accepted receipt, accepted obligation, `M0-*`, `E0/E1`, `H0`, `R0`, `AUDIT-Z`,
`THEOREM-Z`, theorem completion, release-grade evidence, or master acceptance.

Reopen only after kernel-closing the exact hard Morse-Sard branch, obtaining dependency-ordered
master acceptance through validation, reconciling structured scope and public state, and completing
the cold/offline, provenance, supply-chain, independent-verifier, CI, bundle, and master gates.
