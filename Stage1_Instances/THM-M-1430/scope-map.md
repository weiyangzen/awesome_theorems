# Scope map

## Preserved source scope

The repository fixes only the name `Mandelbrot集`, the gloss `复二次多项式的参数空间`
("parameter space of complex quadratic polynomials"), Benoit Mandelbrot, 1980, importance
"high," and an untrusted `已验证` status. This supports an object/topic boundary in complex
quadratic dynamics. It supplies no definition, quantified proposition, hypotheses, conclusion,
theorem locator, proof, or formal artifact.

The familiar set

```text
{c : C | the orbit of 0 under z |-> z^2 + c is bounded}
```

is a candidate normalization for later source review, not the canonical claim frozen by this
intake. A definition alone also does not identify what theorem, if any, this target asks Lean to
prove.

## Proposition-changing decisions

An approved target correction or immutable primary-source proposition must freeze:

- whether the target is an object definition, a characterization, or a theorem about the object;
- the quadratic-family coordinates, such as monic centered `z^2 + c`, a general quadratic, or the
  logistic form `lambda * z * (1 - z)`, with checked parameter transports where credited;
- the parameter and phase-space domains, normally the full complex plane rather than its real
  slice, together with all universes and structures;
- the marked critical point or critical value and whether iteration starts at `n = 0` or `n = 1`;
- the exact orbit and set encodings and the placement of every binder;
- boundedness as bounded range, an explicit uniform norm bound, or an escape-radius predicate;
- every strict or non-strict inequality and all boundary cases; and
- one truth-valued conclusion, with its full hypotheses and exceptional cases.

These choices are a resolution checklist, not an asserted theorem.

## Candidate families not credited

- Definition by bounded critical orbit for `z^2 + c`.
- Equivalence between critical-point and critical-value orbit boundedness.
- Escape-radius characterizations used by numerical membership tests.
- Compactness, closedness, or elementary parameter bounds.
- Connectedness, local connectivity, or boundary and hyperbolic-component results.
- Measure, dimension, density, computability, or undecidability results.

No item in this list is selected, asserted, or credited at intake.

## Explicit exclusions

Connectedness is not available as a convenient default: the repository separately assigns
`Mandelbrot集的连通性` to `THM-M-1431` (the Douady-Hubbard theorem). The Julia set
(`THM-M-1428`), Fatou set (`THM-M-1429`), umbrella complex-dynamics topic (`THM-M-1427`),
Yoccoz theorem (`THM-M-1432`), and Brjuno condition (`THM-M-1433`) are distinct targets as well.

Also excluded are a newly chosen definition disguised as theorem closure, a tautological
membership-by-unfolding proof, a finite-orbit special case, a numerical escape-time renderer or
image, and a structure that assumes the desired conclusion as a field. None identifies or proves
the repository target.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides `Complex`, function iteration,
norms, ranges, and bounded-set predicates, but a bounded intake search found no named Mandelbrot or
complex-quadratic-parameter-space declaration. These are encoding ingredients only, not an
exhaustive anchor audit, checked definition transport, theorem statement, or proof.
