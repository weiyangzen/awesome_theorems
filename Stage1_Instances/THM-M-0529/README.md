# THM-M-0529 rev-5.6 statement

This directory is the executing statement dossier for the repository item named "homology groups." The source
phrase is not itself a theorem: the intake interprets "topological invariant" at its narrowest
standard theorem boundary, namely that a homeomorphism induces degreewise isomorphisms after the
homology theory and coefficients are fixed. The statement phase must select and inspect a primary
source before this claim can become an exact Lean target.

The statement phase fixes that boundary as ordinary, unreduced integral singular homology in every
natural-number degree. `Statement.lean` elaborates the exact claim that applying the pinned mathlib
singular-homology functor to the `TopCat` isomorphism associated to a homeomorphism produces an
isomorphism. This includes degree zero and empty spaces.

`statement-certificate.json` freezes binders, expression output and hashes, imports, environment,
and mutation checks. Exact commands and results are recorded in `validation.md`. This is statement
elaboration only: no source acceptance, anchor audit, proof, audit completion, or release is claimed.
