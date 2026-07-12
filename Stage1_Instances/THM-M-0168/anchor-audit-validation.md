# Anchor-audit validation record

Item: `S56-M-0168-ANCHOR_AUDIT`  
Base revision: `81a476ca1d6d291cdb0760d9dd206fc7ae943180`  
Audit date: 2026-07-12

## Result

The exact repo-local artifact is only the proposition
`Stage1Instances.THM_M_0168.BernsteinMinimalGraphTarget`; it has no proof body. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` provides the `ContDiff` and Frechet-derivative APIs
checked by `AnchorAudit.lean`, but the complete pinned source search found no two-dimensional
minimal-surface Bernstein theorem. Hits for `Bernstein` are approximation polynomials or the
Schroeder-Bernstein theorem and are explicitly different mathematics.

The bounded public Lean search found no exact external candidate. Its only relevant project was
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`. At that immutable
revision, `Hypersurfaces.lean` defines `meanCurvature`, and `Manifolds.lean` proves
`meanCurvature_parametric_eq_levelSet`. These are useful extrinsic-geometry infrastructure, but
their pointwise curvature relation neither assumes an entire minimal graph nor concludes that its
graphing function is affine. The project pins the same Lean 4.29.0 and mathlib commit as this
repository. It is not a dependency here, and because it has no exact closure, importing it would
not discharge even the root theorem. Its differential-geometry sources also contain other `sorry`
declarations (for example `rigidity_theorem`), so this audit makes no transitive trust claim.

The exact root therefore remains `M4` with `formalization_debt`. This is a completed bounded anchor
inventory, not a proof that no Lean implementation exists anywhere, and not theorem completion.

## Commands and results

Commands ran in this worker clone. Lean used only the existing pinned `.lake` artifacts; no update,
fetch, clone, or dependency build was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0168` | 0 | rank 665; planned; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'bernstein|minimal[ _-]?surface|minimal graph|mean curvature' Formalizations/Lean/.lake/packages/mathlib/Mathlib ... --glob '*.lean'` | 0 | only unrelated Bernstein names; no minimal-surface rigidity declaration |
| Sourcegraph queries recorded in `anchor-audit.json` | 0 | exact-name searches: 0; `meanCurvature`: four matches in one external project |
| Commit-addressed Sourcegraph raw reads of atlas-lean toolchain, manifest, and two modules | 0 | Lean 4.29.0, matching mathlib pin, and candidate types/proof text inspected |
| GitHub unauthenticated web code searches recorded in `anchor-audit.json` | 0 | sign-in boundary; no negative result credited |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0168/AnchorAudit.lean` | 0 | five pinned calculus declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0168/Statement.lean` | 0 | exact canonical target re-elaborated |
| `python3 Stage1_Instances/THM-M-0168/check_anchor_audit.py` | 0 | schema/status boundary, probes, pins, and external metadata agreed |
| `git diff --check -- Stage1_Instances/THM-M-0168` | 0 | no whitespace errors |

## Open integration gate

Reopen only when a candidate supplies a repository URL, immutable revision, toolchain, module,
declaration, and exact normalized type or checked transport. Its proof body, placeholders, axioms,
unsafe/oracle boundaries, dependencies, and license must then be audited and a repo-local wrapper
must elaborate. Until then, no `M0-P`, `M1`, or theorem-completion credit is valid.
