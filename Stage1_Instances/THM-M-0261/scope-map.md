# Scope map

## Preserved theorem family

- The normalized complex quadratic family `f_c(z) = z^2 + c`, parameterized by `c` in the
  complex plane.
- The critical orbit beginning at `0` and the Mandelbrot parameter locus defined by failure of
  that orbit to escape to infinity, or by a source-approved equivalent formulation.
- Ordinary topological connectedness of this parameter locus as a subset of the complex plane.
- The Douady-Hubbard proof route through the parameter Bottcher map or conformal isomorphism on
  the complement, only after all analytic premises and the implication to connectedness are mapped.

These bullets delimit the recognizable source theorem family. They are not an accepted canonical
statement and do not assert any proof.

## Decisions required at statement freeze

1. Fix an accepted immutable primary edition and exact locator. The current candidates are the
   1982 Douady-Hubbard C. R. note and the expanded English Orsay notes, whose Chapter 8 derives
   connectedness as Corollary 8.3(a) from Theorem 8.1. Publication identity, translation,
   incorporated definitions, corrections, and errata require independent review.
2. Freeze the quadratic-map normalization. `z^2 + c` must not be silently replaced by a conjugate
   family without a checked parameter-space transport.
3. Freeze the Mandelbrot-set definition: bounded range of `n |-> f_c^[n] 0`, non-escape of the
   critical orbit, membership of `0` in the filled Julia set, or connectedness of that filled Julia
   set. Standard relationships among these forms still require source-faithful checked bridges.
4. Choose the exact boundedness/non-escape encoding, including metric boundedness versus an escape
   radius or filter limit, and whether the orbit is written from `0` or its first value `c`.
5. Choose `IsConnected` versus nonemptiness plus `IsPreconnected`. Any nonemptiness proof and its
   role in root composition must remain explicit.
6. Resolve the ambient topology. The root concerns a subset of `Complex`, not merely a connected
   complement in the Riemann sphere or a filled Julia set for one parameter.
7. Freeze directions for equivalent forms. A conformal isomorphism of complements, fullness,
   simple connectivity of a complement, and capacity one are not definitionally the root theorem.
8. Resolve `c = 0`, the real cusp `c = 1/4`, boundary parameters, empty/nonempty conventions,
   escape-radius equality, iterate-zero inclusion, and finite initial orbit segments.

## Explicit exclusions

- Local connectedness, the Mandelbrot local-connectivity conjecture, or path connectedness.
- Connectedness or local connectedness of every Julia or filled Julia set without the required
  parameter-locus root.
- The parameter-locus definition, compactness, fullness, capacity one, external-ray landing,
  hyperbolicity density, or interior classification substituted for connectedness.
- A conformal-map structure that assumes the needed injectivity, surjectivity, complement topology,
  or connectedness conclusion as data.
- A finite escape-time approximation, plotted fractal, floating-point orbit test, sampled grid,
  numerical image, or unchecked certificate.
- The object/topic target `THM-M-1430` or duplicate metadata target `THM-M-1431` as inherited
  statement, source, proof, receipt, or completion credit.
- The catalog label `已验证`, a paper title, or successful adjacent API checks as `H0` or `M0`.

## Duplicate-record boundary

`THM-M-1431` is a separate rev-5.6 target whose title is the Douady-Hubbard theorem and whose
catalog authors, year, connectedness gloss, and untrusted status duplicate this target. This intake
records the collision for later integration-lane reconciliation. It does not merge target IDs,
modify the other target, or share evidence by assumption.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides complex numbers, function
iteration, set ranges, metric boundedness, connectedness, preconnectedness, and compactness. A
bounded name search found no exact Mandelbrot-connectedness declaration in pinned mathlib or
repo-local Lean sources. `IntakeProbe.lean` only checks those adjacent APIs. The search and probe
are intake discovery, not the downstream immutable anchor audit, statement gate, or proof evidence.

The remote `girving/ray` candidate at immutable revision
`0ca7b1e746b2911557ac76f56259068cfd1423ab` defines a non-escape locus and declares
`isConnected_mandelbrot`, but uses Lean `v4.27.0-rc1` and another mathlib revision. It was inspected
as immutable source only, not fetched into `.lake`, built, integrated, or credited.
