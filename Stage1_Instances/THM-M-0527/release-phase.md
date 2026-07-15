# THM-M-0527 release-phase reconciliation

Item: `S56-M-0527-RELEASE`. Base revision:
`a9274bb02f984e5c74d2c97339044c6db8eb14f9`.

## Exact verdict

The release verdict is `blocked`. The lifecycle remains `planned`, the conservative root vector
remains `[H1, M3, R3]`, and both `audit_complete` and `theorem_complete` are false. No receipt or
frozen obligation is accepted, and this worker makes no release or theorem-completion claim.

The first workflow failure is `S56-10.2-DEPENDENCY-ACCEPTANCE`. The validation receipt is only
provisional worker evidence, explicitly has `accepted=false` and `release_grade=false`, and has no
dependency-ordered master acceptance. Independently, the exact theorem gate fails because no
placeholder-free body constructs a connected cover realizing every subgroup and proves its exact
induced range. The remaining root cut is `M0527-EX-COVER` and `M0527-EX-RANGE`.

## Evidence reconciliation

A fresh narrow replay elaborates the exact frozen statement and all fourteen genuine partial
declarations in `Proof.lean` at trust level zero. The validation probe reports them sorry-free, and
each declaration reports exactly `propext`, `Classical.choice`, and `Quot.sound`. These declarations
establish the fiber criterion for two existing pointed connected covers. They do not inhabit
`CoveringSpaceClassificationTarget`, because its surjectivity conjunct still requires the missing
arbitrary-subgroup covering construction and exact-range proof.

`AUDIT-Z` is separately blocked. `README.md` and `task-dag.json` are intake-era projections which
still say that no exact proposition or registry is frozen and that all later local tasks are open;
later structured statement and obligation evidence contradict those projections. The frozen graph
also retains `M0527-FIB` in its cut with no composition certificate, while later proof evidence
truthfully claims zero closed frozen obligations. The source record remains H1 without pinpoint
edition/page/assumption/errata mapping and independent review, and readability remains R3 without
an independently reviewed node-by-node reconstruction.

Release additionally lacks accepted transitive provenance, foundation, axiom, and TCB closure;
immutable clean input; an empty-cache cold offline replay; complete SBOM/license archives; two
distinct signed runners; an independently implemented minimal verifier; protected adversarial CI;
and a deterministic twice-built evidence bundle. The weaker status therefore wins.

## Commands and exact results

Commands ran from the worker clone on 2026-07-15 (Asia/Shanghai). The automation-provided pinned
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency clone, dependency
fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0527` | 0 | Rank 584; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0527/check_obligation_tree.py` | 0 | 34 obligations and 40 typed edges passed; root remained open M3 with no proof-completion claim. |
| `python3 -I -B Stage1_Instances/THM-M-0527/check_release.py` | 0 | Current hashes, dependency state, graph boundary, trust-zero warm replay, and the blocked `AUDIT-Z`/`THEOREM-Z` decision passed. |
| `python3 -m json.tool Stage1_Instances/THM-M-0527/release-spec.json Stage1_Instances/THM-M-0527/release-decision.json Stage1_Instances/THM-M-0527/release-receipt.json .stage1-worker-selftest.json` | 0 | All release JSON artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0527-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0527/check_release.py` | 0 | Checker syntax compiled outside the repository. |
| `git diff --check -- Stage1_Instances/THM-M-0527 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The integrated validation recipe is intentionally not presented as current release replay. It is
bound to base revision `874745ff39044c1e45ed30a04111d3d84aa0e348` and that phase's worker packet,
so it fails its snapshot guard on the release base. The release checker authenticates its immutable
receipt and performs a fresh bounded Lean replay on the unchanged statement/proof/probe inputs.

## Status boundary

This artifact self-tests only a truthful negative release decision. It proposes `[_]` for master
review of the release-phase report, not for the theorem. It grants no `H0`, `M0`, `E0/E1`, `R0`,
`AUDIT-Z`, `THEOREM-Z`, release, theorem completion, accepted state, or master acceptance.
