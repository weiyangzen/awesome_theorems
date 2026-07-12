# Scope map

## Preserved theorem family

- The normalized complex quadratic family `f_c(z) = z^2 + c`, parameterized by `c` in the
  complex plane.
- The critical orbit beginning at `0` and the Mandelbrot parameter locus defined by its failure to
  escape to infinity, equivalently by boundedness of that orbit after the exact source definitions
  and transport are accepted.
- Ordinary topological connectedness of this parameter locus as a subset of the complex plane.
- The source proof route through the parameter Böttcher map or conformal isomorphism on the
  complement, only after every analytic premise and the implication to connectedness are mapped.

These bullets delimit the received theorem family. They are not yet an accepted canonical
statement or a proof.

## Decisions required at statement freeze

1. Fix an immutable primary edition and exact locator. Leading candidates are the 1982 Douady-
   Hubbard note and the expanded Orsay notes; the latter state connectedness as Corollary 8.3 after
   Theorem 8.1. Translation, publication identity, incorporated definitions, corrections, and
   errata require independent review.
2. Freeze the quadratic-map normalization. The `z^2 + c` parameterization must not be silently
   replaced by a conjugate family without a checked parameter-space transport.
3. Freeze the Mandelbrot set definition: bounded range of `n |-> f_c^[n] 0`, non-escape of the
   critical orbit, membership `0` in the filled Julia set, or connectedness of that filled Julia
   set. These are standard related forms but need source-faithful definitions and checked bridges.
4. Choose the exact boundedness/non-escape encoding, including metric boundedness versus an escape
   radius, the meaning of tending to infinity, and whether the orbit includes the zeroth iterate.
5. Choose `IsConnected` versus `IsPreconnected`. In mathlib `IsConnected` includes nonemptiness;
   any proof of nonemptiness and its place in composition must remain explicit.
6. Resolve set topology and ambient compactification conventions. The root concerns a subset of
   `Complex`, not a connected complement in the Riemann sphere or a claim only about the filled
   Julia set for one parameter.
7. Freeze all equivalent-form directions. A conformal isomorphism of complements, fullness,
   simple connectivity of a complement, and capacity one are not definitionally the root theorem.
8. Resolve boundary cases such as `c = 0`, the real cusp `c = 1/4`, parameters exactly on the
   boundary, empty/nonempty conventions, escape-radius equality, and finite initial orbit segments.

## Explicit exclusions

- Local connectedness of the Mandelbrot set, the full MLC conjecture, or path connectedness.
- Connectedness or local connectedness of every Julia or filled Julia set without the required
  parameter hypothesis.
- The parameter-locus definition itself, compactness, fullness, capacity one, external-ray
  landing, hyperbolicity-density, or interior classification used as a substitute for the root.
- A conformal-map structure that assumes injectivity, surjectivity, or the desired complement
  topology as fields and then projects connectedness without proving the source obligations.
- A finite escape-time approximation, plotted fractal, floating-point orbit test, sampled grid,
  numerical image, or unchecked certificate.
- The neighboring object target `THM-M-1430` or duplicate metadata target `THM-M-0261` as inherited
  statement, source, proof, or completion credit.
- The repository label `已验证` ("verified"), a paper title, or successful adjacent API checks as `H0` or
  `M0` evidence.

## Duplicate-record boundary

`THM-M-0261` is a separate rev-5.6 target whose Chinese title translates to "Mandelbrot-set
connectedness" and whose catalog authors, year, gloss, and untrusted status duplicate this record.
This intake records the collision so the integration lane can reconcile identity deliberately.
It does not merge target IDs, modify the other owned path, share receipts, or import proof credit.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides complex numbers, function
iteration, set ranges, metric boundedness, connectedness, preconnectedness, and compactness. A
bounded exact-topic search found no Douady-Hubbard, Mandelbrot, filled-Julia, Böttcher, or complex-
dynamics target declaration in pinned mathlib or repo-local Lean sources. The API probe and name
search are intake discovery only, not an exhaustive anchor audit, statement elaboration, or proof
evidence.
