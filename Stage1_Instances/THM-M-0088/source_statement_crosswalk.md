# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| A category embeds in a functor category by sending `A` to `Hom(-, A)` | N. Yoneda, "On the homology theory of modules," *J. Fac. Sci. Univ. Tokyo Sect. I* 7 (1954), 193-227; original source identified, exact page/theorem and scan hash pending | `CategoryTheory.yoneda` | Historical root located, but no pinpoint premise/errata audit: `H1` |
| The embedding is fully faithful | Standard corollary of the Yoneda lemma; S. Mac Lane, *Categories for the Working Mathematician*, 2nd ed., Springer, 1998, Yoneda chapter; pinpoint pending | `CategoryTheory.Yoneda.fullyFaithful` | Exact formal candidate located; no rev-5.6 elaboration or dependency evidence yet |
| Morphisms correspond bijectively to natural transformations between representables | Same fully-faithful content at each pair `X,Y` | `FullyFaithful.homEquiv` for `yoneda` | Candidate consequence, not a substitute root |
| Element/evaluation form of the Yoneda lemma | Yoneda lemma, stronger reusable mechanism from which the embedding follows | `CategoryTheory.yonedaEquiv`, `CategoryTheory.yonedaLemma` | Collateral mechanism; its presence does not independently close this root |

The repository source wording, "a category can be embedded in its presheaf category," is frozen
here as existence of the canonical contravariant Yoneda functor together with full faithfulness.
"Embedding" does not mean surjective or essentially surjective onto all presheaves. Lean's
`C : Type u` and `[Category.{v} C]` encode local smallness and universe choices that the informal
sentence suppresses.

The statement phase must inspect the pinned declaration type, serialize the normalized expression
and environment, and test mutations that drop fullness, change variance, alter universe/domain
choices, or replace the representable subcategory by the whole presheaf category. No `H0` or `M0`
claim is made.
