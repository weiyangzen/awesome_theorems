# THM-M-0156 Lean 4 anchor audit

Item: `S56-M-0156-ANCHOR_AUDIT`  
Audit date: 2026-07-12  
Base revision: `af0b9c3534733bf19ba3f83c1a063916aaac92fe`

## Immutable mathlib result

The audit is scoped to the exact frozen rectangular target
`Stage1Instances.THM_M_0156.DivergenceTheoremTarget`. The local Lake manifest pins mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and Lean
`leanprover/lean4:v4.29.0`. No update, build, fetch, clone, or dependency mutation was performed.

The exact candidate is
`MeasureTheory.integral_divergence_of_hasFDerivAt_off_countable` in
`Mathlib.MeasureTheory.Integral.DivergenceTheorem`. Its rectangular domain, continuity condition,
interior Frechet derivative, integrable coordinate divergence, and signed face-flux equation agree
with the frozen target. The candidate is stronger only because it permits a countable exceptional
set. `AnchorAudit.lean` independently restates the target and kernel-checks the exact adapter obtained
by selecting the empty exceptional set.

The earlier `BoxIntegral.hasIntegral_GP_divergence_of_forall_hasDerivWithinAt` is a proof-family
ancestor, not an independent root proof body. Exact source blobs, SHA-256 hashes, comparison,
dependency feasibility, and license are recorded in `anchor-audit.json`. The owning Bochner source
contains no `sorry`, `proof_wanted`, axiom declaration, or unsafe declaration. The narrow adapter's
axiom report is `propext`, `Classical.choice`, and `Quot.sound`.

## External Lean 4 search

Repository-local and pinned-mathlib searches were followed by bounded public searches. Sourcegraph's
exhaustive exact-name query returned 16 occurrences, all in mathlib. Its moving indexed revision was
used only for discovery; the candidate was inspected and checked at the immutable local pin. A
GitHub repository-metadata phrase query returned zero complete results, while a broad
`divergence language:Lean` query returned five projects about program divergence, optimization
divergences, or physics rather than the Gauss divergence theorem. No distinct credible external
candidate was established. This is not a claim that all public Lean code was exhaustively searched.

## Classification boundary

The exact pinned candidate supports proposed `M0-W` status, pending the obligation-tree, proof,
complete transitive trust/provenance, hermetic replay, independent-review, and master-acceptance
gates. Human-source status remains `H1`, readability remains `R4`, and both audit completion and
theorem completion remain false. This phase supplies candidate-audit evidence only.

## Validation

Commands ran in this worker clone against existing pinned artifacts.

| Command | Exit/result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0; 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0156` | 0; rank 655, planned, L0, theorem complete false |
| `python3 Stage1_Instances/THM-M-0156/check_anchor_audit.py` | 0; two pinned candidates, hashes, and fail-closed boundary verified |
| `python3 -m json.tool Stage1_Instances/THM-M-0156/anchor-audit.json` | 0; valid JSON |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0156/AnchorAudit.lean` | 0; exact empty-exception adapter elaborated; expected three axioms printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0156/Statement.lean` | 0; predecessor frozen statement re-elaborated |
| `git diff --check -- Stage1_Instances/THM-M-0156 .stage1-worker-selftest.json` | 0; no whitespace errors |

Known open gates are the downstream gates listed above and the non-exhaustive boundary of public
code search. They do not invalidate this bounded, immutable candidate audit and do prevent any
theorem-completion claim.

An initial combined validation invocation was launched with `Formalizations/Lean` as its working
directory while the Python paths were still repository-root-relative. Its five Python commands
failed with file-not-found errors; both following Lean commands exited 0. The Python checks were
then rerun from the repository root and exited 0 as recorded above. This was a working-directory
mistake, not a candidate or dependency failure.
