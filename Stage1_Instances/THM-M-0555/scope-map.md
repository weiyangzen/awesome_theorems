# Scope map

## Included subject boundary

- A fibration (in the source-appropriate sense) with fiber `F`, total space `E`, and base `B`.
- A homological spectral sequence whose second page is expressed by homology of `B` with the local
  coefficient system formed from homology of `F`.
- Differentials, page indexing, convergence, and the filtration on homology of `E` needed to make
  the abutment meaningful.
- Naturality only if it is part of the selected source theorem, rather than an assumed enhancement.

## Statement decisions still required

The metadata phrase "homology spectral sequence of a fibration" does not determine a unique root.
The statement phase must use a stable primary-source edition to freeze:

1. singular, Serre, or other fibration hypotheses and any path-connectedness/CW assumptions;
2. constant coefficients versus a ring or local coefficient system, including the action of
   `pi_1(B)` on fiber homology;
3. homological indexing and differential bidegree;
4. the exact starting page and identification of its terms;
5. weak/strong convergence and the precise filtration whose associated graded is the infinity page;
6. edge cases such as disconnected base/fiber, nontrivial monodromy, and first-quadrant boundedness.

## Explicit exclusions

- The Leray-Serre cohomology spectral sequence, a generalized-cohomology version, or the Leray
  spectral sequence for sheaves as a substitute for the homology theorem.
- Merely defining a spectral sequence or proving a low-dimensional exact sequence.
- A trivial-product special case in place of the fibration result.
- Any proposition that assumes the desired spectral sequence or its convergence.
- The untrusted Stage0 `已验证` label as proof or source-fidelity evidence.

Later phases must separately freeze universes, categorical/object encodings, imports, declaration
type, environment fingerprint, checked transports, and statement mutations.
