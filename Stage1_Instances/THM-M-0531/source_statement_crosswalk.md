# Source-statement crosswalk

| Claim component | Human-source discovery anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Repository wording | `Docs/researches/math_theorems.md`, topological entry near lines 3939-3944 | none | Secondary metadata only: it says homology/cohomology relation but supplies no coefficient group, degree, hypotheses, arrows, or exactness claim |
| Cohomological UCT | Allen Hatcher, *Algebraic Topology* (Cambridge University Press, 2002), Section 3.1, Theorem 3.2, printed p. 195 | no terminal declaration identified | Strong statement-selection lead: a split exact sequence relating `H^n(C; G)`, `Hom(H_n(C), G)`, and `Ext(H_(n-1)(C), G)` for a free chain complex; immutable scan hash, exact wording, errata, and independent review remain open |
| Topological specialization | Hatcher, same section, applying the free-chain-complex theorem to cellular or singular chains | `AlgebraicTopology.singularHomologyFunctor` | Singular-homology substrate exists in the pinned mathlib revision; no cohomology comparison or specialization theorem is credited |
| `Ext` term | Same theorem's left term | `Ext` in `Mathlib.CategoryTheory.Abelian.Ext` | The derived-functor API exists and elaborates, but availability is not a UCT proof |
| Naturality | Naturality described around the source theorem | future natural-transformation and short-exact-sequence objects | Exact naturality variables and commuting diagrams must be copied from the selected source, not inferred |
| Splitting | Source theorem states a split short exact sequence, with the usual non-naturality caveat to be checked exactly | no witness identified | Intake excludes any claim of canonical or natural splitting |

The source lead is a modern textbook formulation, not yet an accepted `H0` primary-source packet.
The later source audit must preserve an immutable edition, verify the printed theorem and surrounding
hypotheses, check corrections/errata, and map every term and arrow to the selected formal target.

The repo-local Lean search at pinned mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95` found singular-homology and `Ext` substrate but no text
or declaration named `UniversalCoefficient` or "universal coefficient". This is only a bounded
intake observation, not the required anchor audit and not proof of absence.

The exact statement phase must resolve these mutations before proof work: replace cohomology by
homology, replace `Ext/Hom` by `Tor/tensor`, shift `n-1`, change integral to arbitrary base-ring
chains, toggle reduced theory, add connectedness, or strengthen a noncanonical split to a natural
split. None is accepted as definitionally equivalent at intake.
