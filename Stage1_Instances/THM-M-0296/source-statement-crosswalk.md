# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:2125-2130` supplies exactly the Chinese title
`里斯-索林插值定理`, attribution `Marcel Riesz/Thorvald Thorin`, year `1939`, gloss
`算子的插值理论`, importance high, and status `已验证`. Git blame attributes all six uncited lines
to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, theorem
locator, formula, definitions, binders, hypotheses, proof boundary, corrections, reviewer, or
formal artifact.

`Docs/Stage0_Blueprint.md:8170-8195` repeats the topic gloss and attribution while explicitly
leaving the formal system, exact definitions and premises, proof route, dependencies, alternate
forms, axioms, machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only
as untrusted source metadata and resets the target to `L0 / rework_required`.

## Bibliographic leads, not accepted sources

Crossref metadata was inspected for Marcel Riesz's *Sur les maxima des formes bilineaires et sur
les fonctionnelles lineaires*, Acta Mathematica 49 (1926), 465-497, DOI
`10.1007/BF02564121`. It is a primary-source lead for the earlier convexity theorem, but its text,
exact proposition, assumptions, and relation to this catalog entry were not admitted.

The zbMATH Open API returned records `2510273`, `3034022`, and `2518255` for G. O. Thorin's
*An extension of a convexity theorem due to M. Riesz*. They locate a five-page 1939 Lund
publication and a 1938/1939 parallel-publication ambiguity. One historical review describes an
analytic log-convexity generalization, but intake did not obtain and preserve the primary full text
or a source-to-operator-theorem proposition. The catalog's expanded personal name likewise remains
unverified. Metadata and review text are discovery leads, not primary source text; no lead has an
accepted errata audit, source-to-node mapping, or independent review. The provisional human status
is therefore `H1`, not `H0`.

## Clause crosswalk

| Repository component | Conventional source-family component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "operator" | linear operator initially acting on a common class of functions | linear map or compatible endpoint maps between `MeasureTheory.Lp` spaces | operator identity, domain, linearity field, density, and extension semantics open |
| "interpolation" | endpoint strong-type estimates imply an intermediate strong-type estimate | endpoint `MemLp`/norm hypotheses and a continuous linear map at interpolated exponents | endpoint exponent ranges and bound forms open |
| interpolated exponents | reciprocal exponents are affine in an interpolation parameter | `ENNReal` exponents plus real reciprocal equations or a checked alternate encoding | infinity, division, endpoint, and binder conventions open |
| interpolated constant | geometric combination of endpoint bounds | real or `ENNReal` powers and an operator-norm inequality | nonnegativity, zero powers, sharpness, and exact conclusion open |
| proof engine | analytic family plus a three-lines estimate in standard complex proofs | `Complex.HadamardThreeLines.*` and future analytic-family construction | pinned three-lines APIs exist, but the construction and root theorem do not |
| `已验证` | inventory label only | kernel/source receipts would be required | no H or M credit |

## Pinned Lean boundary

The pinned probe elaborates `MeasureTheory.Lp`, `MeasureTheory.MemLp`,
`ContinuousLinearMap.compLp`, `ContinuousLinearMap.compLpL`, and three variants of the Hadamard
three-lines norm bound. These declarations establish nearby infrastructure only. `compLp` applies a
single codomain map pointwise at a fixed exponent; it is not an operator interpolation result.
Hadamard three-lines controls an analytic function on a strip; it does not construct the analytic
family required for Riesz-Thorin or state the resulting `Lp` operator bound.

A bounded case-insensitive exact-name search of repository-local Lean and pinned mathlib found no
Riesz-Thorin declaration. Search absence is intake discovery, not a complete formal-candidate audit
or a proof that no semantic equivalent exists.

## Source and statement gate

Before statement freeze, accountable reviewers must preserve an immutable primary or authoritative
edition, pinpoint the exact theorem and every standing assumption, reconcile the date and naming,
audit corrections, map every domain/exponent/operator/bound/conclusion clause, and approve the
scope. The formal statement phase must then elaborate the source-identical Lean proposition with
minimal pinned imports, expression/environment fingerprints, checked alternate transports, and
removed-hypothesis, changed-domain, binder-scope, and boundary mutations. Until then the canonical
statement and formal target remain null.
