# Scope map

## Included claim

- The object is a finite-dimensional smooth manifold, not a topological or PL manifold.
- Compactness is included so the requested decomposition is finite.
- A handle of index `k` is modeled mathematically by `D^k x D^(n-k)`, attached along
  `S^(k-1) x D^(n-k)` to an earlier boundary level.
- The conclusion is existence of finitely many ordered handle attachments reconstructing the
  manifold up to the smooth equivalence specified by the selected source.

## Decisions reserved for the statement phase

The pinpoint source must determine whether the canonical theorem concerns a closed manifold, a
manifold with boundary relative to a chosen incoming boundary, or a compact cobordism. It must also
fix connectedness, second countability, corners created during attachment, collars, whether a
zero-handle is part of the data, and whether reconstruction means diffeomorphism, diffeomorphism
relative to boundary, or equality of a filtered manifold.

The formal statement must order the manifold/model/dimension/boundary binders explicitly. It must
also decide the empty and zero-dimensional cases and distinguish an intrinsic handle-decomposition
structure from a mere list of index counts.

## Scope relationships

- A Morse function with distinct critical values and suitable boundary behavior is a standard
  proof route; it is not the theorem's conclusion unless a source states an equivalence.
- The one-critical-point sublevel-set attachment lemma is a principal local bridge, not the whole
  compact-manifold theorem.
- A relative handle decomposition of a cobordism may imply the closed version after checked
  specialization, but that transport is future proof work.
- A noncompact manifold may require a locally finite/countable decomposition. It is excluded from
  the frozen finite claim rather than being hidden under the word "manifold".

## Explicit exclusions

- CW decomposition, triangulation, or homotopy equivalence as a substitute for diffeomorphic
  reconstruction.
- Handle cancellation, uniqueness, Cerf theory, and minimal-handle statements.
- A structure taking the desired decomposition as an input field.
- Morse inequalities or the Morse lemma alone.

The later Lean target must define concrete handle attachment and reconstruction data or document a
precise missing-API blocker. An existential over an unconstrained certificate is not eligible.
