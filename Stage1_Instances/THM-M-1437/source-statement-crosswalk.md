# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10495-10500` supplies exactly the title `Feigenbaum普适性`,
Mitchell Feigenbaum, 1975, the gloss `倍周期分岔的普适常数`, importance "high", and status
`已验证`. Git blame attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, formula,
theorem locator, map class, binders, hypotheses, conclusion, proof, or formal artifact.

`Docs/Stage0_Blueprint.md:39077-39102` repeats the gloss while explicitly leaving exact definitions
and premises, proof route, dependencies, equivalent forms, axioms, machine status, and artifact
links open. Its generic assertion that a closed result exists is not primary-source evidence. The
rev-5.6 manifest retains `已验证` only as `source_status_untrusted` and resets the target to
`L0 / rework_required`.

## Bibliographic discovery boundary

Mitchell J. Feigenbaum, *Quantitative universality for a class of nonlinear transformations*,
*Journal of Statistical Physics* **19**(1), 25-52 (July 1978), DOI
`10.1007/BF01020332`, is a strong candidate source family. Crossref metadata fixes that citation.
The publisher abstract considers recursions `x_(n+1) = lambda f(x_n)` whose maps have a unique
differentiable maximum and local critical order `z > 1`. It separately describes alpha scaling,
a universal fixed-point function, and parameter convergence at rate delta, with numerical values
for `z = 2`. It also says the results were computationally determined for various maps and ends,
"At present our treatment is heuristic."

Feigenbaum's sequel, *The universal metric properties of nonlinear transformations*, *Journal of
Statistical Physics* **21**(6), 669-706 (December 1979), DOI `10.1007/BF01107909`, develops a
renormalization hierarchy and a fixed-point functional equation. Its publisher abstract describes
delta through an eigenvalue of a linearized operator, explicitly calls uniqueness of the
eigenvalue above one a conjecture, and conditions a stability conclusion on that spectral
conjecture.

These inspected publisher/Crossref records are E5 discovery leads. No full primary edition,
pinpoint theorem, complete definitions, proof boundary, corrections or errata, or independent
review is frozen. The catalog year 1975 conflicts with the publication years and identifies no
unpublished edition. Neither abstract can silently select an unconditional root or establish H0.

Oscar Lanford's 1982 computer-assisted proof and Mikhail Lyubich's 1999 universality theorem are
later proof-source leads owned by neighboring catalog targets `THM-M-1438` and `THM-M-1439`.
Their existence helps expose the source ambiguity; it does not identify `THM-M-1437`.

## Component crosswalk

| Repository element | Mathematical component to freeze | Required Lean component | Intake assessment |
|---|---|---|---|
| `Feigenbaum普适性` | one exact universality, fixed-point, or hyperbolicity proposition | exact `Prop` with ordered binders and selected family/operator | topic family only |
| "period doubling" | a specified cascade of stable cycles and bifurcation parameters | parameterized maps, iterates, exact/minimal period, stability, parameter sequence | definitions absent |
| "universal constant" | delta or alpha; exact limit, asymptotic, eigenvalue, enclosure, or value claim | exact real/complex quantity and equality, limit, spectrum, or bound | constant and logical claim open |
| Mitchell Feigenbaum / 1975 | attribution and alleged source date | immutable edition, theorem/page, source hash, corrections, proof boundary | unreconciled with 1978/1979 records |
| `已验证` | untrusted inventory label | accepted source review and kernel receipt would be required | no H or M credit |

## Variant and neighbor boundary

Delta parameter scaling, alpha spatial scaling, fixed-point existence, fixed-point uniqueness,
renormalization convergence, a single expanding eigenvalue, universality over a map class, and a
numerical enclosure are separate statements. A theorem for one logistic family is not universality
over all source-specified unimodal families. A coordinate or parameter reparameterization can alter
raw ratios unless the exact invariant formulation and normalization are fixed.

The out-of-scope physics catalog record `THM-P-0784` gives `delta ≈ 4.669` and the year 1978, but
it still gives no definition, tolerance, limiting sequence, or map class. It is boundary provenance,
not a source correction or an eligible substitute for this mathematics target.

## Source gate

Before the target can leave `H5`, an accountable reviewer must approve a stable truth-valued target
correction, preserve and hash an immutable primary edition, identify an exact theorem and every
incorporated definition, transcribe all ordered binders, hypotheses, and conclusion clauses,
separate proved, heuristic, computational, and conjectural content, reconcile 1975, check
translations, corrections, and errata, and justify the boundary against `THM-M-1436`,
`THM-M-1438`, and `THM-M-1439`. A second qualified reviewer must approve the mapping. The corrected
proposition's H status must then be classified afresh; it cannot inherit `已验证`.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks iteration, periodic and fixed points, minimal period, semiconjugacy, and limit APIs. A
bounded source-name search found no Feigenbaum, Coullet-Tresser, Lanford, period-doubling, or
target-specific dynamical-renormalization declaration in repo-local or pinned mathlib Lean sources.

The canonical module, declaration/expression, elaborated-expression hash, checked transports, and
statement mutations remain null. The probe and search are intake feasibility evidence only, not a
complete formal-candidate audit and not H0, M0, or readable-proof closure.
