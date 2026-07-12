# Scope map

## Metadata boundary

The repository supplies only the Chinese name `庞特里亚金运算`, attribution to Lev Pontryagin,
the year 1947, and the gloss "stable cohomology operations on integral cohomology". These fields
are discovery metadata, not a statement. In particular, they do not determine an operation's
source and target coefficient groups, degree, space category, naturality domain, stability law, or
the proposition to prove about it.

## Candidate intended subject

The closest standard named cohomology operation is the Pontryagin square. A source-selected version
would need to specify all of the following:

- a precise class of spaces or pairs and the cohomology theory/model;
- a degree and an operation such as `H^(2n)(X; Z/2) -> H^(4n)(X; Z/4)` (only if confirmed by the
  selected source), rather than the metadata's unsupported integral-to-integral gloss;
- naturality and the exact reduction, quadratic, cup-product, or suspension identities that form
  the theorem;
- coefficient homomorphisms, grading/sign conventions, and boundary or relative variants;
- whether the target is construction/existence, uniqueness, or one named identity.

The degree-doubling type means that calling the usual Pontryagin square a stable operation is not a
harmless wording choice. The statement phase must resolve this conflict from a primary source.

## Explicit exclusions

- Pontryagin characteristic classes of real vector bundles.
- Pontryagin duality, Pontryagin spaces, the Pontryagin product, and the maximum principle.
- A generic cohomology operation with the required properties assumed as hypotheses.
- Replacing the operation by cup square, Steenrod square, or a coefficient-reduction identity alone.
- Treating the metadata label `已验证`, a nearby topology API, or an unpinned external citation as
  proof credit.

The statement phase must freeze the exact human claim, ordered binders, degenerate cases, Lean
expression and imports, environment fingerprint, foundation/TCB/computation profiles, checked
transports, and hypothesis/domain mutations before proof work begins.
