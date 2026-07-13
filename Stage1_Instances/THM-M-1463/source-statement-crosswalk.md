# THM-M-1463 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10679-10684` supplies exactly the title
`Petrov-Galerkin方法`, the attribution `众多数学家`, the period `20世纪`, the gloss
`推广的Galerkin方法`, importance "high," and status `已验证`. All six uncited lines entered the
repository in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no
bibliography, definition, formula, binder, hypothesis, conclusion, proof, correction history, or
formal artifact.

`Docs/Stage0_Blueprint.md:39784-39809` repeats the same gloss while explicitly leaving the target
formal system, foundation, background, exact definitions and premises, proof route, dependencies,
equivalent formulations, axioms, machine status, and artifact links open. The rev-5.6 manifest
retains `已验证` only as `source_status_untrusted` and resets the target to
`L0 / rework_required`.

The word `推广` (generalized) does not say what is generalized or assert a conclusion. The usual
distinct-trial/test-space reading is a subject-family discriminator, not an exact source statement.

## Bibliographic source lead

Crossref publisher metadata was inspected for Ivo Babuška, *The finite element method with
Lagrangian multipliers*, *Numerische Mathematik* 20 (1973), pages 179-192, DOI
`10.1007/BF01436561`. This is a credible historical lead for the inf-sup and Petrov-Galerkin
theorem family, but it is not `H0`: the catalog does not cite it, the article body and theorem
passages were not inspected in this intake, and no premise mapping, proof boundary, erratum audit,
immutable admitted copy, or independent review exists.

The Banach-Nečas-Babuška theorem, Babuška stability and quasi-optimality results, and later
Petrov-Galerkin literature remain candidate source families. Their names cannot repair the missing
catalog proposition.

## Clause crosswalk

| Repository element | Mathematical component to select | Prospective Lean component | Intake result |
|---|---|---|---|
| `Petrov-Galerkin` | distinct trial and test spaces in a variational discretization | normed-space types, subspaces, inclusions, and a continuous bilinear or sesquilinear map | family recognized; exact spaces absent |
| `推广` | extension of ordinary Galerkin by spaces, test functions, stability theory, or another feature | explicit relationship to the ordinary Galerkin encoding | no direction or conclusion stated |
| variational equation | find `u_h` in `U_h` such that `b u_h v_h = l v_h` for all `v_h` in `V_h` | ordered existential/universal binders and coercions | not present in catalog |
| stability | coercivity, primal and adjoint inf-sup, kernel condition, or Fortin criterion | positive constants, norm inequalities, kernels/ranges, and dimension hypotheses | choice and constants absent |
| error or convergence | quasi-optimality, best approximation, a priori error, or mesh convergence | exact infimum/distance and bound with every regularity premise | conclusion absent |
| many mathematicians / twentieth century | broad attribution only | immutable edition and theorem/page locator | not a source citation |
| `已验证` | untrusted inventory label | accepted source and kernel receipts | no H or M credit |

## Variant and neighbor boundary

Ordinary Galerkin takes the same trial and test space and is separately cataloged as `THM-M-1462`.
Discontinuous Galerkin is separately cataloged as `THM-M-1464`. Lax-Milgram (`THM-M-0329`) is a
coercive Hilbert-space well-posedness theorem, while Banach-Nečas-Babuška and Babuška estimates are
broader inf-sup theorem families. None may be imported as the root without an accepted
source-to-statement identity review.

## Source gate

Before leaving `H5`, accountable reviewers must redirect the method label to one stable,
truth-valued proposition; preserve an immutable primary or authoritative source; freeze every
definition, domain, binder, hypothesis, constant, conclusion, and degenerate case; inspect the
proof boundary and corrections; justify the relationship to this catalog target and its neighbors;
and obtain independent approval. Human-proof status must then be classified afresh rather than
inherited from `已验证`.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`IntakeProbe.lean` checks continuous bilinear-map norm bounds, subspace inclusions and orthogonal
projection, and the real coercive Lax-Milgram API. These are adjacent interfaces only. A bounded
repo-local and pinned-mathlib search found no source-identical Petrov-Galerkin terminal theorem.

The canonical module, expression, expression hash, environment fingerprint, checked transports,
and statement mutations remain null. No H0, M0, R0, audit completion, or theorem completion is
claimed.
