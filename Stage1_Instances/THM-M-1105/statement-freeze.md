# Statement freeze

The statement phase selects the standard bounded-entry real-symmetric Wigner theorem rather than
claiming that this modern formulation is verbatim Wigner 1955.  The exact target is the proposition
`Stage1.THM_M_1105.WignerSemicircleLaw` in `Statement.lean`.

## Frozen variant

- Dimensions are `n + 1`, so every empirical spectral measure is nonempty.
- `A n` is an unnormalised real symmetric random matrix on one probability space `P`.
- The upper-triangular entries are mutually independent and all entries are measurable.
- Every entry is centred; off-diagonal entries have second moment one. Diagonal variance is not
  fixed. A uniform almost-sure bound supplies the deliberately strong moment/tail hypothesis.
- Symmetry is expressed by `Matrix.IsHermitian`; over `Real` this is ordinary symmetry. Its proof
  supplies mathlib's real eigenvalue enumeration, including multiplicity.
- Eigenvalues are scaled by `1 / sqrt (n + 1)`. Their empirical probability measure is expressed
  extensionally through its integral against every bounded continuous `f`.
- The conclusion is almost sure convergence of those test-function averages to the integral of
  `f(x) * sqrt(4-x^2)/(2*pi)` over `[-2,2]`.

The quantifier order `for P-almost every omega, for every bounded continuous f` is intentional and
stronger than giving a separate exceptional null set for each test function. The theorem is a
stable modern Wigner semicircle-law target. Primary-source genealogy and whether the chosen bounded
version appears in one source with exactly these hypotheses remain H-axis work for the later audit;
that does not alter the frozen proposition.

## Boundary and mutation checks

The target does not assume spectral convergence. Removing `hA_hermitian` makes the real eigenvalue
term unavailable; changing `n + 1` to `n` introduces an empty zero-dimensional empirical measure
and division by zero; removing normalization changes the spectral scale; changing `i < j` variance
to all `i,j` adds a diagonal hypothesis; moving `forall f` outside the almost-everywhere binder
weakens the common-null-set conclusion. These are proposition-changing mutations, not transports.

The declaration is a `def` whose value is a proposition, not a theorem with a proof body. This is
deliberate: the statement phase establishes kernel elaboration only and neither uses a placeholder
nor claims proof closure. The printed type in `statement-validation.md` is the elaborator's canonical
binder/type view.

