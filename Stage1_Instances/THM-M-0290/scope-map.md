# Scope map

## Preserved theorem family

The intake preserves the classical one-dimensional periodic Carleson-Hunt family suggested by the
catalog title, attribution, date, and `L^p` Fourier-series gloss. A candidate reading concerns
almost-everywhere convergence of symmetric Fourier partial sums of a periodic `L^p` function when
`p > 1`. That sentence is a scope description derived from known candidates, not the frozen
canonical claim.

The repository does not authorize silently selecting a period, function model, endpoint range, or
normalization. Every credited root and alternate encoding will need a pinpoint source crosswalk and
a checked Lean transport.

## Proposition-changing decisions

An approved exact source statement must freeze all of the following:

1. The exponent type and range: one fixed `p`, all `p` with `1 < p < infinity`, a range including
   `p = infinity`, or another source-specific convention.
2. The domain: an additive circle, a specified interval with periodic identification, or another
   equivalent model; also its period and endpoint conventions.
3. Real- or complex-valued functions, and whether vector-valued variants are excluded.
4. Haar or Lebesgue measure, total-mass normalization, Fourier-character sign, coefficient
   normalization, and the identification between circle and interval formulations.
5. An actual measurable function with a `MemLp` hypothesis versus an element of an `Lp`
   almost-everywhere equivalence class, including the chosen representative.
6. The partial sums: inclusive symmetric frequencies `[-N, N]`, another cutoff, or a directed
   finite-set formulation, and the exact initial index.
7. The conclusion: pointwise `Tendsto` outside a null set to the selected representative, with all
   topology, filter, equality-almost-everywhere, and representative-invariance details.
8. The ordered binders, quantifier dependencies, side conditions, universes, typeclass context,
   foundation profile, and every alternate encoding with its checked relationship witness.

These choices change the proposition or its proof boundary. The intake records them without
selecting among them.

## Degenerate and boundary cases

Source review must explicitly dispose of `p = 1`, `p = infinity`, and invalid or extended-real
exponents; zero and constant functions; real versus complex values; the zero cutoff; null-set
changes of representative; nonmeasurable raw functions; zero or negative period parameters;
circle versus half-open interval endpoints; and any dependence of coefficients or limits on the
chosen representative. No case is silently excluded while the root is unfrozen.

## Excluded substitutions

- Carleson's `p = 2` theorem family alone, including the separately cataloged `THM-M-0346` dossier, cannot replace the
  full source-selected `L^p` family.
- `L^p`-norm, `L^2`-norm, convergence in measure, weak convergence, Cesaro/Fejer convergence, or
  convergence only along a subsequence cannot replace full almost-everywhere partial-sum
  convergence.
- Pointwise convergence under continuity, smoothness, bounded variation, absolute coefficient
  summability, or another extra regularity hypothesis is not the arbitrary `L^p` theorem.
- A maximal-operator inequality alone is not the root unless its implication to the exact
  convergence target is checked and composed.
- A structure, hypothesis, axiom, oracle, or definition that assumes the desired convergence
  supplies no proof credit.
- Generic AddCircle, Fourier, measure, `MemLp`, `Lp`, or convergence APIs are infrastructure only.
- The catalog's untrusted `已验证` label, a bibliographic citation, or the API probe is not human or
  machine proof evidence.

## Neighbor boundary

`THM-M-0346` is the separately cataloged Carleson `L^2` family/specialization. Its artifacts identify useful
mathlib and external discovery candidates, but its statement, receipts, proof credit, and status do
not transfer to this target. A future proof may use an exact stronger Carleson-Hunt theorem or
specialize this target to `p = 2` only through checked source identity and encoding transports.
