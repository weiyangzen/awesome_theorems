# Statement blocker

## First failed gate

The rev-5.6 exact-statement gate is blocked before Lean target elaboration. The repository gives
only the title `GMRES` and the gloss "generalized minimal residual method." The primary 1986 paper
contains multiple inequivalent results and algorithm variants, while the catalog selects none.

The most tempting substitution is Corollary 3, finite termination in at most `N` steps. It applies
to unrestarted finite-dimensional GMRES in exact arithmetic. The same source explicitly shows that
restarted GMRES(1) can be stationary, so interpreting the catalog as unconditional convergence or
as finite termination of every restarted variant would be false.

## Retry condition

An accountable statement review must select an immutable primary-source result and freeze its
matrix or operator domain, scalar field, dimension, invertibility and spectral assumptions,
Krylov/Arnoldi definitions, iteration and restart parameters, exact-arithmetic boundary, ordered
binders, hypotheses, conclusion, and every degenerate case. An independent source reviewer must
approve that crosswalk. Then the statement phase can elaborate the exact Lean expression and run
the required mutations.

Until that happens, `canonical_statement`, `canonical_claim`, the Lean module/expression and its
fingerprints, alternate encodings, obligation registry, and discovery protocol remain null. The
intake is self-tested, but the statement, audit, proof, release, `AUDIT-Z`, and `THEOREM-Z` gates are
open.
