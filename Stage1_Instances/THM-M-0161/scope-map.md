# Scope map

## Included theorem family

- A real interval `I` as the parameter domain and oriented Euclidean three-space as the ambient
  space.
- Prescribed scalar functions `kappa` and `tau` on `I`, with strictly positive curvature and the
  regularity required by the selected source.
- Existence of an arc-length-parametrized sufficiently smooth curve whose curvature is `kappa` and
  whose torsion is `tau`.
- Uniqueness of such a curve up to a proper Euclidean rigid motion (translation followed by an
  orientation-preserving orthogonal transformation).
- The Frenet frame and its differential system as the expected construction bridge, not as a
  substitute for the existence-and-uniqueness conclusion.

## Decisions required at statement freeze

The statement phase must inspect and select one exact source theorem, then freeze:

- whether `I` is open, closed, compact, or an arbitrary interval and whether endpoints are treated
  by one-sided derivatives;
- the precise differentiability or continuity hypotheses on `kappa`, `tau`, and the resulting
  curve, including which derivative-based definition of torsion is used;
- whether the theorem prescribes signed torsion in an oriented `R^3`, and hence whether uniqueness
  is under proper rigid motions rather than all Euclidean isometries;
- whether the curve is required to be unit-speed in the conclusion or is considered modulo an
  orientation-preserving reparametrization;
- ordered binders for the interval, coefficient functions, initial point/frame, constructed curve,
  and competing curve;
- the meaning of equality of curvature and torsion on all of `I`, including endpoint and empty or
  singleton interval behavior;
- whether existence and uniqueness are one canonical proposition or checked component theorems
  with an exact conjunction/transport wrapper.

The canonical Lean target must expose concrete curves, derivatives, Euclidean norm and inner
product, curvature, signed torsion, arc-length parametrization, and proper rigid motion. It must not
store the desired curve or congruence theorem as an input field.

## Degenerate and boundary cases

Strict positivity of `kappa` is proposition-critical: it makes the principal normal and Frenet
frame available and excludes inflection points. Zero curvature must not be admitted by weakening
the hypotheses. Zero torsion is allowed if the selected source allows it and should yield the
planar case. Empty or degenerate intervals, interval endpoints, reversal of parameter orientation,
and reflections require explicit source-aligned decisions and mutation tests.

## Explicit exclusions

- The planar fundamental theorem determined by curvature alone.
- The Frenet-Serret formulas alone (`THM-M-0162`) without integration, existence, and uniqueness.
- Only the uniqueness half or the repository gloss "determined" with existence omitted.
- Curves modulo arbitrary reflections when signed torsion is prescribed.
- A local result on a smaller interval as a substitute for the source's global interval result.
- An abstract ODE solution theorem or a structure containing the desired curve as assumed data.
- The repository metadata value `已验证` as human-source or kernel evidence.
