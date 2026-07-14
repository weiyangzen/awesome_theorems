# THM-M-0442 validation-phase result

Item: `S56-M-0442-VALIDATION`. Base revision:
`a1a7e939e58f103f5ff5d23af51437fa8658aa04`.

## Narrow validation

The structured recipe re-elaborates the frozen Lean target in `Statement.lean`,
the conditional composition in `ObligationTree.lean`, all five partial
declarations in `Proof.lean`, and three separately written elementary lemmas in
`Validation.lean`. Every Lean process runs through `lake env lean --trust=0`
in a fresh temporary output directory with fixed locale, timezone, and thread
count. The complete Python recipe, including all child Lean processes, runs
with a cleared environment in one Bubblewrap network namespace. The
differential module imports neither `Proof` nor `ObligationTree`.

Every checked declaration uses no axiom outside `propext`,
`Classical.choice`, and `Quot.sound`. The four local Lean files pass a
nested-comment-aware scan for placeholders, bodyless declarations, unsafe
code, and oracle devices; all three differential declarations also pass
`assert_no_sorry`. Current source hashes and the clean pinned mathlib
revision, tree, origin, and license agree with the receipt.

This is intentionally a negative-root validation. `Proof.lean` checks two
order bounds, two torsion-cardinality transports, and the implication from the
desired classification to a weaker cardinality bound. It supplies no field of
`MazurEngine` and closes none of the 21 frozen obligations. The first missing
deep package is `M0442-M-MODULI`; all thirteen members of the frozen root cut
remain open. The root stays `[H1, M4, R4]`, and `audit_complete=false` and
`theorem_complete=false`.

## Commands and results

Commands ran from the repository root on 2026-07-15 (Asia/Shanghai). The
automation-provided canonical `.lake` symlink was reused without mutation. No
`lake update`, `lake build`, dependency clone, or dependency fetch was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0442` | 0 | rank 88, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before edits, only the pre-existing untracked `Formalizations/Lean/.lake` symlink; nonrelease worktree |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `a1a7e939...a04`, tree `d881fd96...dcf` |
| execute the `validation-spec.json` argv without shell interpolation; capture combined stdout/stderr | 0 | network-isolated trust-zero narrow replay passed; exact root, hermetic release, and independent gates remained fail-closed |
| `python3 Stage1_Instances/THM-M-0442/check_obligation_tree.py` | 0 | 21 obligations and 20 proof edges passed; root remains open |
| `python3 -m json.tool Stage1_Instances/THM-M-0442/validation-spec.json` | 0 | structured recipe parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0442/validation-receipt.json` | 0 | provisional negative validation receipt parsed |

The validation runner's exact summary is:

```text
PASS THM-M-0442 network-isolated trust-zero replay of the frozen Lean target
PASS conditional composition, five partial declarations, and three differential declarations use only the selected classical axiom subset
PASS frozen hashes, proof blocker, placeholder scan, and pinned mathlib provenance; zero frozen obligations closed
OPEN M0442-M-MODULI and twelve other root-cut obligations; hermetic release and distinct-runner verification fail closed
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | Fresh local oleans elaborate the frozen target and every claimed conditional, partial, or differential declaration at trust level zero. |
| Placeholder and unsafe boundary | provisional pass | No prohibited source device occurs; each differential declaration is kernel-reported sorry-free. |
| Axiom observation | provisional pass | Every checked declaration uses only the selected classical trio. This is not an accepted complete foundation/TCB closure. |
| Direct local provenance | provisional pass | Current inputs are hash-bound; the pinned mathlib revision/tree/origin/license and source cleanliness agree. Full transitive body/import/artifact and source-boundary provenance remains open. |
| Proof dependency and exact root | fail closed | The proof predecessor is unaccepted, closes no frozen obligation, proves only consequences of the desired result, and leaves `MazurEngine` uninhabited. |
| Human-source fidelity | fail closed | Complete proof-source reconstruction, errata disposition, readable reconstruction, and independent H0/R0 reviews remain open. |
| Hermetic release replay | fail closed | The run reused shared warm artifacts, not a clean checkout with empty caches, cold rebuild, offline restoration, and complete SBOM/TCB archive. |
| Independent verification | fail closed | The differential module shares this worker, checkout, toolchain, and cache; no distinct signed verifier or independently provisioned runner exists. |

The validation node is self-tested only as an honest, nonrelease blocked
receipt. It grants no accepted obligation state, exact root closure, `M0-*`,
`E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master
acceptance.
