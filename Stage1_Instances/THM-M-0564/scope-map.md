# Scope map

## Preserved source scope

The only claim supplied by the repository is the broad phrase "the theory of characteristic
classes of vector bundles". Its subject matter includes assignments of cohomology classes to
vector bundles, normally constrained by pullback naturality and often described through universal
bundles or classifying spaces. This description is a scope boundary, not a frozen theorem.

## Decisions required before statement freeze

An authoritative correction must select exactly one proposition and fix:

- real, complex, oriented, or other vector bundles and the category of base spaces;
- the cohomology theory, coefficient ring, grading, and reduced/unreduced convention;
- the class family, such as Stiefel-Whitney, Chern, Pontryagin, or Euler classes;
- whether the result is a definition/axiomatization, existence and uniqueness theorem,
  classification by a universal class, Whitney-sum formula, or another named result;
- ordered quantifiers, rank restrictions, pullback maps, trivial-bundle normalization, and boundary
  cases such as rank zero, an empty base, and disconnected bases.

These choices cannot be inferred from the title. In particular, the adjacent manifest targets
`THM-M-0565`, `THM-M-0566`, and `THM-M-0567` separately name three major class families, which is
additional evidence that none of them may silently replace this generic record.

## Explicit exclusions

- Any one Stiefel-Whitney, Pontryagin, Chern, or Euler class theorem chosen without source approval.
- A predicate or structure containing naturality and normalization as assumed fields and then
  presenting field projection as the source theorem.
- Euler characteristic, characteristic functions, Pontryagin duality, or other uses of the word
  "characteristic" unrelated to characteristic classes of vector bundles.
- The repository label `已验证` as evidence of a human proof or kernel closure.

No Lean target is frozen at intake. The first retry condition is an approved, source-located
proposition that resolves the choices above without broadening or substituting the record.
