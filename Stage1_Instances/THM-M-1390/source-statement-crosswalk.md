# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10125-10130` supplies exactly the title
`Courant极小极大原理`, Richard Courant, 1920, the gloss `特征值的变分刻画`, importance "high,"
and status `已验证`. Git history attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, formula, definition,
binder, hypothesis, conclusion, proof boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:37803-37828` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof process, dependencies, equivalent forms, axioms,
machine status, and artifact links open. Rev-5.6 preserves `已验证` only as untrusted source
metadata and resets the target to `L0 / rework_required`.

## Inspected historical source lead

Richard Courant, "Ueber die Eigenwerte bei den Differentialgleichungen der mathematischen Physik,"
*Mathematische Zeitschrift* 7 (1920), 1-57, DOI `10.1007/BF01199396`, is a strong primary-source
lead matching the catalog attribution and year. A 57-page scan exposed by Zenodo record `2131750`
was inspected in temporary storage. It had 3,656,768 bytes, MD5
`27f31d9a9db658f5522cc9cafc8b1dd4`, and SHA-256
`2145238915d5524b5f2582fc65fe820cacf4f636e0aabece11c062b8967f7764`.

The exact candidate anchor is Section 3, "Die Maximum-Minimum-Eigenschaft der Eigenwerte und
Eigenfunktionen," Satz 3a, journal pages 18-19. In the paper's setting, `L(u) + lambda*k*u = 0` is
a self-adjoint elliptic boundary-value problem on a domain `G`. For arbitrary piecewise-continuous
test functions `v_1, ..., v_(n-1)`, the source defines `d{v_1,...,v_(n-1)}` as the minimum or lower
bound of the energy over continuous, piecewise continuously differentiable `phi` satisfying
weighted orthogonality to each `v_i`, weighted unit normalization, and the selected boundary
condition. Satz 3a states that the nth eigenvalue `lambda_n` is the greatest such lower bound, with
attainment at the first eigenfunctions and `phi = u_n`; apart from the Dirichlet case, it also
discusses omitting the boundary condition from the variational competitor class.

This pinpoints a plausible historical root but does not yet make it canonical or `H0`. The catalog
does not cite the paper or Satz 3a, and the scan's OCR is imperfect. An accountable reviewer must
inspect the German source and its preceding definitions, fix the exact differential expression,
coefficient and domain regularity, energy/boundary term signs, admissible boundary cases, index and
multiplicity conventions, and minimum/infimum and maximum/supremum distinctions; audit corrections
and translations; map the proof boundary; and approve the relationship to modern variants.

## Component crosswalk

| Repository/source element | Possible mathematical component | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `Courant极小极大原理` | historical PDE maximum-minimum theorem or a modern Courant-Fischer/operator variant | one source-selected exact `Prop` | recognizable family, exact root open |
| "eigenvalues" | indexed discrete spectrum, possibly repeated by multiplicity | finite index plus a source-defined eigenvalue enumeration | operator and ordering absent |
| "variational" | extremum of an energy or Rayleigh quotient over constrained functions/subspaces | quotient/energy, admissible carrier, subspace or orthogonality constraints | functional and competitor class absent |
| "characterization" | equality between the nth eigenvalue and a min-max/max-min value, possibly with attainment | exact equality and witness clauses | orientation and attainment absent |
| Richard Courant, 1920 | strong link to the inspected paper and Satz 3a | provenance only until admitted and reviewed | `H1`, not `H0` |
| `已验证` | untrusted inventory field | accepted source proof and kernel receipt would be required | no proof credit |

## Historical-PDE to modern-operator boundary

Courant's Satz 3a fixes an elliptic differential expression, a weighted integral normalization,
specific regularity classes, and boundary-value problems. A finite-dimensional Courant-Fischer
theorem instead quantifies over subspaces of a Hermitian vector space. Modern infinite-dimensional
versions may use compact self-adjoint operators or semibounded closed forms and must address
essential spectrum and form domains. These are related generalizations/specializations, not mere
spellings. No checked implication or equivalence among them is available at intake.

The nearby repository target `THM-M-0055` already names the Rayleigh quotient theorem with the gloss
"variational characterization of Hermitian matrix eigenvalues." Selecting only a largest/smallest
Rayleigh-quotient result here would collapse distinct targets and lose the nth-eigenvalue content
suggested by Courant's original maximum-minimum principle.

## Lean discovery boundary

Pinned `Mathlib.Analysis.InnerProductSpace.Rayleigh` defines
`ContinuousLinearMap.rayleighQuotient`, relates its extrema on nonzero vectors and spheres, and
proves existence of eigenvalues at the global supremum and infimum in finite dimension.
`Mathlib.Analysis.InnerProductSpace.Spectrum` supplies finite-dimensional self-adjoint eigenvalues,
an eigenbasis, and `eigenvalues_antitone`. These are useful adjacent interfaces, but they do not by
themselves state the kth-eigenvalue subspace/orthogonality min-max equality.

A bounded case-insensitive search for `Courant`, `Fischer`, and eigenvalue/minimax patterns over
pinned mathlib and repo-local Lean found no exact-topic declaration. This is neither the later
immutable formal-candidate audit nor a global absence claim. The canonical module, expression,
fingerprints, checked transports, and statement mutations remain null. No statement elaboration,
formal proof, audit completion, or theorem completion is claimed.
