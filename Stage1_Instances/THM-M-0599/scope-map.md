# Scope map

## Repository claim

`Docs/researches/math_theorems.md` records the title, Marston Morse, 1934, and the gloss
`Betti numbers and Morse indices`. `Docs/Stage0_Blueprint.md` repeats this while leaving the exact
definitions, hypotheses, proof route, axioms, and formal artifact open. Its `verified` label is
untrusted metadata under rev-5.6 and supplies neither human-source nor kernel credit.

## Provisional included claim family

- A closed smooth finite-dimensional manifold `M` and a smooth Morse function `f : M -> R`.
- The finite count `c_k` of critical points of `f` having Morse index `k`.
- Betti numbers `b_k`, after choosing a coefficient field or other source-supported coefficient
  convention that makes the dimensions finite.
- The weak inequalities `c_k >= b_k` and the strong alternating inequalities in each degree.
- The equivalent polynomial formulation `M_f(t) - P_M(t) = (1 + t) Q(t)`, with `Q` having
  nonnegative integer coefficients, only if checked transports establish equivalence under the
  selected finiteness and coefficient conventions.

This is a theorem family, not a frozen canonical statement.

## Decisions required at statement freeze

The statement phase must select a stable source edition, theorem/page, and wording; fix compactness,
boundary, connectedness, and smoothness conventions; choose coefficients; define Betti numbers and
Morse index; decide how critical points are counted; and select weak, strong, polynomial, or package
form as the root. It must also specify behavior outside `0 <= k <= dim M`, the zero-dimensional and
empty-manifold cases, and whether orientability is actually required.

Lean universes, manifold models, ordered binders, explicit versus typeclass assumptions, minimal
imports, foundation/TCB profiles, and equivalence witnesses remain open. The target may not assume
the desired inequalities, a Morse complex with the desired homology, or the polynomial factorization
as opaque input.

## Explicit exclusions

- Morse theory or the Morse lemma alone, without the Betti-number inequalities.
- Morse-Bott, equivariant, infinite-dimensional, stratified, manifold-with-boundary, or noncompact
  variants substituted for the classical closed-manifold theorem.
- The Euler-characteristic equality alone; it is weaker than the strong inequalities.
- A finite sequence or chain-complex inequality detached from a checked bridge identifying its
  ranks with critical-point counts and its homology with that of `M`.
- A structure containing the desired inequalities as fields, numerical examples, or the catalog's
  source-status label as proof evidence.

The neighboring targets for Morse theory and the Morse lemma are separate theorem identities and
supply no proof credit for this target.
