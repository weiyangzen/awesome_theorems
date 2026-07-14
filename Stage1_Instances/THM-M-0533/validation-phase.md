# THM-M-0533 validation-phase result

Item: `S56-M-0533-VALIDATION`. Base revision:
`9293a4d141848287a1f656eefe9929eb30465393`.

## Narrow Validation

The structured recipe re-elaborates the hash-bound canonical statement source
and declaration in `Statement.lean`,
the conditional root composition in `ObligationTree.lean`, the genuine partial
theorem in `Proof.lean`, and a separately written reconstruction in
`Validation.lean`. Every Lean process uses the pinned Lean 4.29.0 executable
at trust level zero and writes fresh outputs below a private `/tmp` directory.
Bubblewrap clears the environment, mounts the host read-only, fixes locale,
timezone, and thread count, and denies network access to the validator and all
child processes.

The differential module imports neither `Proof` nor `ObligationTree`. It proves
only `firstMap U V n ≫ secondMap U V n = 0`, by explicitly expanding the
biproduct composite and cancelling the two equal inclusion-induced maps. It
does not construct the connecting morphisms or any exactness package.

All three checked proof/composition declarations use no axiom outside
`propext`, `Classical.choice`, and `Quot.sound`. The four Lean sources pass a
nested-comment-aware scan for placeholders, bodyless declarations, unsafe
code, and oracle devices. Current hashes and the clean pinned mathlib revision,
tree, origin, license, and selected source/olean artifacts agree.

This is intentionally a negative-root validation. The graph reports
`M0533-S-DEFINITIONS` and the conditional assembly interface
`M0533-T-ASSEMBLE` as pre-proof closures. The latter is an illegal closed-parent
classification because its construction and exactness children remain open;
only the master may reconcile that frozen structured artifact. The proof and
validation phases close no new frozen obligation. The inherited five-item list
beginning with `M0533-C-SUBDIVISION` is only a priority blocker set, not a
complete or proven minimal graph cut; recurring exactness obligations are also
open.
The root stays `[H3, M3, R4]`, `audit_complete=false`, and
`theorem_complete=false`.

The canonical declaration is re-elaborated from a hash-bound source and its
name/type category is printed by Lean. No independently serialized elaborated
expression digest exists in the dossier, so the exact expression-fingerprint
acceptance gate remains fail-closed.

## Commands And Results

Commands ran from the repository root on 2026-07-15 (Asia/Shanghai). The
automation-provided canonical `.lake` symlink was reused without mutation. No
`lake update`, `lake build`, dependency clone, or dependency fetch was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0533` | 0 | Rank 590, planned, legacy artifacts unaccepted, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0533/check_obligation_tree.py` | 0 | 19 obligations, 37 typed edges, denominator `238242df...8dfc`; root open M3. |
| Execute the `validation-spec.json` argv without shell interpolation | 0 | Network-isolated trust-zero narrow replay passed; exact root and release gates remained fail-closed. |
| `git diff --check -- Stage1_Instances/THM-M-0533 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The final validation runner summary is:

```text
PASS THM-M-0533 network-isolated trust-zero replay of the hash-bound canonical source/declaration
PASS conditional composition, the partial proof, and its differential reconstruction use only the observed classical axiom subset
PASS frozen hashes, placeholder scan, and selected pinned mathlib source/olean provenance
OPEN M0533-C-SUBDIVISION and four other root-cut obligations; exact root, release hermeticity, and distinct-runner verification fail closed
```

## Gate Decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | Fresh local oleans elaborate the hash-bound canonical statement source/declaration and every claimed conditional, partial, or differential declaration at trust level zero. |
| Exact expression fingerprint | fail closed | The source/declaration is bound and re-elaborated, but no independently serialized elaborated-expression digest is available. |
| Placeholder and unsafe boundary | provisional pass | No prohibited source device occurs; the differential theorem also passes `assert_no_sorry`. |
| Axiom observation | provisional pass | Checked declarations use only the observed classical trio. This is not an accepted complete foundation/TCB closure. |
| Selected direct provenance | provisional pass | Local inputs are hash-bound; the mathlib revision/tree/origin/license and selected source/olean artifacts agree. Full transitive provenance remains open. |
| Proof dependency and exact root | fail closed | The predecessor is not master accepted; the inherited five priority blockers and additional recurring exactness obligations remain open. |
| Parent closure consistency | fail closed | The frozen graph calls conditional `M0533-T-ASSEMBLE` closed despite its open required children; this receipt gives it no accepted closure credit. |
| Human-source and readability | fail closed | H3/R4 and independent H0/R0 review remain open. |
| Hermetic release replay | fail closed | The run reused a current checkout and shared warm cache, not an empty-cache cold rebuild with offline restoration and complete SBOM/TCB archive. |
| Independent verification | fail closed | The differential module shares this worker, checkout, toolchain, and cache; no distinct signed verifier or independently provisioned runner exists. |

The validation node is self-tested only as an honest, nonrelease blocked
receipt. It grants no newly or accepted closed obligation, exact root closure,
`M0-*`, `E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master
acceptance. In particular, this receipt is not exact expression-identity
acceptance.
