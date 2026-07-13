# THM-M-0441 validation-phase result

Item: `S56-M-0441-VALIDATION`. Base revision:
`18ff7447208231633bf2e01e8aad3111af56531a`.

## Narrow validation

The structured recipe re-elaborates the frozen Lean target in `Statement.lean`, the conditional
composition in `ObligationTree.lean`, all fourteen partial declarations from
`Proof.lean`, and three separately written elementary lemmas from
`Validation.lean`. Every Lean process runs through `lake env lean --trust=0`
in a fresh temporary output directory with fixed locale, timezone, and thread
count. The complete Python recipe, including all child Lean processes, runs
with a cleared environment in one Bubblewrap network namespace. The differential module imports
neither `Proof` nor `ObligationTree`.

Every checked declaration uses no axiom outside `propext`,
`Classical.choice`, and `Quot.sound`. The four local Lean files pass a
nested-comment-aware scan for placeholders, bodyless declarations, unsafe
code, and oracle devices; the three differential declarations also pass
`assert_no_sorry`. Current source hashes and the clean pinned mathlib
revision, tree, origin, and license agree with the receipt.

This is intentionally a negative-root validation. The first failed gate is
source-statement identity: the current target admits `n = 0`, restricts `T` to
natural cutoffs, requires `0 < c`, and replaces connected positive-dimensional
semialgebraic components by preconnected nontrivial ones; `pilaWilkie_iff` is
only reflexivity and supplies none of the four checked source transports. The proof predecessor is
provisional, closes no frozen obligation, and supplies no inhabitant of the
four fields consumed by `ObligationTree.engine_compose`. The `n = 0`, empty,
and semialgebraic branches are genuine partial results but are not the general
Pila-Wilkie theorem. Accepted state remains `[H1, M3, R4]`; this validation
proposes `[H1, M5, R4]` for the candidate relative to the source theorem and
requests statement refreeze, pending master reconciliation. The six-node cut
describes only the frozen internal proposition; `theorem_complete=false`.

## Commands and results

Commands ran from the repository root on 2026-07-14 (Asia/Shanghai). The
automation-provided canonical `.lake` symlink was reused without mutation. No
`lake update`, `lake build`, dependency clone, or dependency fetch was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0441` | 0 | rank 87, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before edits, only the pre-existing untracked `Formalizations/Lean/.lake` symlink; nonrelease worktree |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `18ff7447...31a`, tree `9ea9aab3...7b6` |
| execute the `validation-spec.json` argv without shell interpolation; capture combined stdout/stderr | 0 | ran inside a cleared-environment network namespace from `2026-07-14T05:07:28+08:00` to `05:07:39+08:00`; 427-byte stdout SHA-256 `72cece4f...20c4`; source identity, root, and release gates remained fail-closed |
| `python3 Stage1_Instances/THM-M-0441/check_obligation_tree.py` | 0 | 21 obligations and 18 proof edges passed; root remains open |
| `python3 -m json.tool Stage1_Instances/THM-M-0441/validation-spec.json` | 0 | structured recipe parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0441/validation-receipt.json` | 0 | provisional negative validation receipt parsed |
| direct byte-level newline, CR/NUL, and trailing-whitespace checks in `check_validation.py` | 0 | all six untracked handoff files passed |

The validation runner's exact summary is:

```text
PASS THM-M-0441 network-isolated trust-zero replay of the frozen Lean target
PASS conditional composition, 14 proof declarations, and 3 differential declarations use only the selected classical axiom subset
PASS frozen hashes, proof receipt, placeholder scan, pinned mathlib provenance, and honest open-M3 boundary
OPEN source-identity transport and M0441-C-PARAM; hermetic release and distinct-runner verification fail closed
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | Fresh local oleans elaborate at trust level zero for the frozen Lean target and every claimed conditional or partial declaration. |
| Placeholder and unsafe boundary | provisional pass | No prohibited source device occurs; each differential declaration is kernel-reported sorry-free. |
| Axiom observation | provisional pass | Every checked declaration uses only the selected classical trio. This is not an accepted complete foundation/TCB closure. |
| Direct local provenance | provisional pass | Current inputs are hash-bound; the pinned mathlib revision/tree/origin/license and source cleanliness agree. Full transitive body/import/artifact and source-boundary provenance remains open. |
| Source-statement identity | fail closed | No checked transport reconciles positive source arity, real height cutoffs, the source constant convention, or connected positive-dimensional algebraic components with the frozen Lean target. |
| Proof dependency and exact root | fail closed | The proof receipt is unaccepted, closes no frozen obligation, and leaves the parameterization, determinant, block, and dimension-induction engines unproved. |
| Human-source fidelity | fail closed | Complete proof-source reconstruction, errata disposition, and independent H0/R0 reviews remain open. |
| Hermetic release replay | fail closed | The run reused shared warm artifacts, not a clean checkout with empty caches, cold rebuild, offline restoration, and complete SBOM/TCB archive. |
| Independent verification | fail closed | The differential module shares this worker, checkout, toolchain, and cache; no distinct signed verifier or independently provisioned runner exists. |

The validation node is self-tested only as an honest, nonrelease blocked
receipt. It grants no accepted obligation state, root closure, `M0-*`,
`E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master
acceptance.
