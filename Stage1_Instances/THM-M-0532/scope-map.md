# Scope map

## Included theorem family

- Singular homology of a product `X x Y`, with coefficients fixed by the selected source.
- The homology cross product inducing the graded tensor contribution.
- The Tor correction term and degree shift when the coefficient setting requires it.
- Exactness, naturality, and splitting only in the precise strength asserted by the source.

## Decisions required at statement freeze

The statement phase must select and inspect one exact source theorem and freeze: singular versus
another homology theory; reduced versus unreduced homology; coefficient ring and module sides;
PID, field, freeness, flatness, finite-type, CW, or other hypotheses; the grading and direct-sum
indexing; the construction and sign convention of the cross product; the Tor convention and degree
shift; whether the result is an isomorphism or a natural short exact sequence; and whether a
splitting exists, is chosen, or is natural. It must also settle empty spaces, degree zero, negative
degrees, disconnected spaces, torsion-free specializations, and universe/size assumptions.

These choices change the proposition. In particular, the field-coefficient tensor isomorphism is
strictly less general than the integral short exact sequence and cannot silently replace it.

## Explicit exclusions

- A Kunneth formula for cohomology, sheaf cohomology, spectra, or derived categories unless the
  selected source explicitly makes that the root claim.
- The Eilenberg-Zilber chain equivalence alone, without the asserted homology computation.
- Only the field-coefficient corollary as a substitute for a selected integral theorem.
- A dimension or Betti-number equality that omits torsion data.
- A structure or hypothesis containing the desired exact sequence or isomorphism as input data.
- The repository metadata value `已验证` as human-source or kernel evidence.

No Lean expression is frozen at intake. A later target must expose concrete homology, graded tensor,
cross-product, Tor, exactness, and coefficient interfaces rather than assume the conclusion.
