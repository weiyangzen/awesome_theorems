# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10672-10677` supplies exactly the title `Galerkin方法`, attribution
to Boris Galerkin, year 1915, gloss `投影方法` ("projection method"), importance "high," and status
`已验证`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, mathematical
definitions, binders, hypotheses, conclusion, proof boundary, corrections, or formal artifact.

`Docs/Stage0_Blueprint.md:39757-39782` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate formulations,
axioms, machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

## Historical source boundary

The attribution is consistent with a frequently reported 1915 Galerkin publication concerning
series methods for elastic rods and plates. This is only a bibliographic lead: the repository gives
no citation, and bounded lookup did not yield a primary text with a stable edition, page, result,
assumption list, or correction record suitable for admission. No title transliteration, secondary
summary, or historical biography is treated as the exact source statement. Human status remains
`H5` for the catalog target until an independently reviewed source correction turns the method
label into one stable proposition.

## Component crosswalk

| Catalog component | Possible mathematical component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "Galerkin method" | a variational problem on `V` and a discrete problem on `V_h` | normed/inner-product spaces, submodules, continuous linear maps | spaces, form, functional, and equations absent |
| "projection" | orthogonality of the residual/error against the trial/test space | `Submodule.orthogonalProjection` and orthogonality APIs | candidate symmetric special case only |
| possible solvability reading | continuous/discrete existence and uniqueness for a coercive form | `IsCoercive.continuousLinearEquivOfBilin` | adjacent Lax-Milgram substrate, not Galerkin correctness |
| possible error reading | best approximation or Cea quasi-optimality | norms, infima, coercivity and boundedness constants | conclusion and constants absent |
| possible convergence reading | approximation spaces become dense and discrete solutions converge | indexed subspaces and limits | family, topology, and rate absent |
| `已验证` | untrusted inventory label | no Lean proposition or proof object | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only
probe checks coercivity and Lax-Milgram equivalence APIs plus finite-dimensional orthogonal
projection, its orthogonality characterization, and minimality. A bounded case-insensitive search
for `Galerkin`, `Cea lemma`, and quasi-optimality found no exact-topic declaration in pinned mathlib
or the repo-local Lean sources. Incidental uses of the word Galerkin in unrelated approximation
notes provide no target evidence. This is not a global absence claim or the later immutable external
anchor audit.

Before the statement phase can elaborate anything, accountable reviewers must select an immutable
primary-source proposition, transcribe every incorporated definition and hypothesis, audit
corrections, resolve the trial/test-space and exact-arithmetic boundaries, and independently approve
why that proposition is this catalog target. Only then may the phase freeze minimal imports, ordered
binders, an elaborated expression, checked transports, and the required removed-hypothesis,
changed-domain, binder-scope, and boundary mutations.
