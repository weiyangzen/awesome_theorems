# THM-M-0405 validation-phase result

Item: `S56-M-0405-VALIDATION`. Base revision:
`09a2e94f8f331e8fa7938c55db7dddafb47a6c74`.

## Narrow validation

The structured recipe re-elaborates `Statement.lean`, the conditional branch
composition in `ObligationTree.lean`, all 18 proof-phase algebraic declarations,
and four separately written Lucas lemmas from `Validation.lean`. Each Lean
process runs through `lake env lean --trust=0` in a fresh temporary output directory, with fixed
locale, timezone, and thread count and a bubblewrap network namespace. The
differential module imports neither `Proof` nor `ObligationTree`.

The checked declarations use no axiom outside `propext`, `Classical.choice`,
and `Quot.sound`. The four local Lean files pass a nested-comment-aware scan
for placeholders, bodyless declarations, unsafe/oracle devices, and the four
differential declarations pass `assert_no_sorry`. Current source hashes and
the clean pinned mathlib revision, tree, origin, and license agree with the
receipt.

This is intentionally a negative-root validation. The proof predecessor is
only provisional and closes zero frozen obligations. No declaration proves
either universal primitive-divisor branch or `Statement`; the checked
`statement_of_branches` theorem consumes both branches as premises. The root
therefore remains `[H1, M4, R3]`, with `M0405-X-BHV-BRIDGE` as the minimal
open cut and `theorem_complete=false`.

## Commands and results

Commands ran from repository root on 2026-07-14 (Asia/Shanghai). The
automation-provided canonical `.lake` symlink was reused without mutation. No
`lake update`, `lake build`, dependency clone, or dependency fetch was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0405` | 0 | rank 18, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before edits, only the pre-existing untracked `Formalizations/Lean/.lake` symlink; nonrelease worktree |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `09a2e94f...c74`, tree `31b53f41...149` |
| `python3 Stage1_Instances/THM-M-0405/check_obligation_tree.py` | 0 | 15 obligations, 30 typed edges, denominator `cd9daee4...da793`; root open M4 |
| `python3 -I -B Stage1_Instances/THM-M-0405/check_validation.py` | 0 | network-isolated trust-zero replay passed for the exact statement, conditional interfaces, 18 partial proof declarations, and four differential declarations; root and release gates remained fail-closed |
| `rg -n '\b(sorry\|admit\|sorryAx\|implemented_by\|native_decide)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe\|extern)[[:space:]]+' Stage1_Instances/THM-M-0405/{Statement,ObligationTree,Proof,Validation}.lean` | 1 | expected no-match exit; no prohibited source construct found |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...a95`, tree `bdc39a31...e2b`; dependency worktree clean |
| `timeout 180s bash Stage1_Instances/THM-M-0405/check_proof.sh` | 1 | its Lean phases reached the historical evidence checker, which rejects current HEAD because `check_proof.py` is bound to old base `4683af33...`; the validation recipe independently binds and checks current integrated inputs |

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | Fresh local oleans elaborate at trust level zero for every extant local declaration and the differential probe. |
| Placeholder and unsafe boundary | provisional pass | No prohibited source device occurs; each differential declaration is kernel-reported sorry-free. |
| Axiom observation | provisional pass | Every checked declaration uses only the selected classical trio. This is not a complete accepted foundation/TCB closure. |
| Direct local provenance | provisional pass | Current inputs are hash-bound; the pinned mathlib revision/tree/origin/license and source cleanliness agree. Full transitive body/import/artifact and source-boundary provenance remains open. |
| Proof dependency and exact root | fail closed | The proof receipt is unaccepted, closes zero frozen obligations, and supplies neither primitive-divisor branch nor the BHV bridge. |
| Human-source fidelity | fail closed | The exact primary BHV theorem/page/definition/errata crosswalk remains incomplete; the source label is not H0 evidence. |
| Hermetic release replay | fail closed | The run reused shared warm artifacts, not a clean checkout with empty caches, cold rebuild, offline restoration, and complete SBOM/TCB archive. |
| Independent verification | fail closed | The differential module shares this worker, checkout, toolchain, and cache; no distinct signed verifier or independently provisioned runner exists. |

The prerequisite dossier also has two fail-closed inconsistencies:
`obligation-tree.md` says 12 human-source-required obligations while the
registry says 11, and `typed-graphs.json` names nonexistent
`obligation-graphs.json` paths. These grant no proof or provenance credit.

The validation node is self-tested only as an honest, nonrelease blocked
receipt. It grants no accepted obligation state, root closure, `M0-*`,
`E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master
acceptance.
