# Scope map

## Preserved theorem family

- A complex-valued function defined at least on the open unit disk.
- Holomorphicity on that disk.
- The essential normalization that the origin is fixed, if the classical Schwarz lemma rather
  than the bare self-map class is selected.
- The standard contraction conclusions and their equality/rotation boundary, in exactly the
  combination selected by an immutable reviewed source.

These bullets delimit the Schwarz-lemma family; they are not a canonical statement or proof.

## Decisions required at statement freeze

1. Select and preserve an immutable primary or authoritative source edition, exact theorem and
   definition locators, incorporated assumptions, corrections, errata, and independent review.
2. Decide whether the canonical root contains only `|f(z)| <= |z|`, also `|f'(0)| <= 1`, and/or
   the equality rigidity clause. These are related but distinct conclusions.
3. Fix the unit disk as `{z : Complex | norm z < 1}` and decide whether the source's map is a total
   `Complex -> Complex` constrained on the disk, a subtype map, or another exact representation.
4. Fix "holomorphic on the unit disk" as complex differentiability on the open disk or prove a
   checked transport from the source's analytic convention.
5. Preserve `f(0) = 0`. Without it, a constant nonzero disk self-map violates the usual norm
   conclusion; the catalog gloss alone is not a theorem.
6. Decide whether "to itself" means `f(D) subset D` (strict open-disk self-map) or the weaker
   pointwise bound `|f(z)| <= 1`. Mathlib's main candidate accepts a closed-ball target.
7. Freeze equality cases: equality at a nonzero interior point, equality of derivative norm at
   zero, their disjunction, and the exact conclusion `f(z) = a*z` with `|a| = 1` on the disk.
8. Resolve total-function behavior outside the disk, the boundary `|z| = 1`, the zero point in an
   equality premise, strict versus non-strict inequalities, and whether generalized centers,
   radii, or normed-space codomains are alternate encodings rather than the root.

## Explicit exclusions

- A bare statement that a holomorphic disk self-map exists or is merely a disk self-map.
- Schwarz-Pick, maximum-modulus, Borel-Caratheodory, Riemann-mapping, or conformal-automorphism
  theorems substituted for the normalized Schwarz lemma.
- Only the pointwise inequality, only the derivative inequality, or only rigidity unless the
  reviewed source selects exactly that root.
- A result for arbitrary center/radius or arbitrary complex normed codomain silently substituted
  for the classical complex unit-disk theorem, even if it implies the selected statement.
- A closed-disk bound used as identical to a strict open-disk self-map without a checked one-way
  implication and an explicit direction boundary.
- An assumed rotation, contraction, or abstract structure that contains the desired conclusion.
- The untrusted `已验证` label, a theorem-name match, or successful API elaboration used as H0/M0.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Analysis.Complex.Schwarz` provides pointwise, derivative, slope, and affine equality-case
theorems. The intake probe also verifies that a strict unit-disk self-map plus `f(0)=0` derives both
usual inequalities. This is a usable formal candidate (`M3`), not an accepted root: exact source
scope, expression identity, transport, terminal-body provenance, and trust closure remain for
downstream phases.
