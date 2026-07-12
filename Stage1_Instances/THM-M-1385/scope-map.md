# Scope map

## Preserved theorem family

The intake preserves the second-order linear ODE comparison family named by the catalog: an order
between equation coefficients or potentials forces a corresponding comparison between zeros of
nontrivial solutions. No candidate below is credited as the theorem. Common source conventions
include equations in normal form such as

```text
u'' + p u = 0
v'' + q v = 0
```

or self-adjoint Sturm-Liouville form. Sturm's inspected section XVI uses non-strict coefficient
orders `G'' >= G'` and `K'' <= K'` and says consecutive zeros of `V'` contain a zero of `V''`.
Section XII instead states a global zero-count/order theorem and adds a left-endpoint logarithmic-
flux comparison. The catalog does not select between these source roots or a normalized transport.

## Decisions required at statement freeze

1. Select an approved primary or authoritative source edition and pinpoint one exact theorem;
   record incorporated definitions, translation, proof boundary, corrections or errata, and
   independent review.
2. Fix normal form versus self-adjoint form and every coefficient domain, regularity, positivity,
   nonvanishing, and integrability assumption.
3. Fix the ambient interval, open/closed endpoint conventions, ordered endpoints, and whether the
   theorem is local, global, regular, or singular.
4. Define a solution precisely: classical differentiability, equation equality on which set, and
   whether both compared solutions must be nontrivial.
5. Preserve the source orders `G'' >= G'` and `K'' <= K'`, and fix their exact Lean orientation and
   equation assignment. Any normalized potential form needs a checked transport.
6. Select section XII's global ordered-zero claim or section XVI's consecutive-zero corollary, and
   fix equality cases and whether a zero may occur at an endpoint or must lie strictly inside.
7. Define consecutive zeros, isolation, simplicity, and whether multiplicities matter.
8. Freeze the ordered binders, quantifier dependencies, hypotheses, exact conclusion, foundation
   profile, minimal imports, alternate transports, and required statement mutations.

## Degenerate and boundary cases

Source review must explicitly dispose of an empty or singleton interval; equal or reversed
endpoints; identical coefficients; weak coefficient order with no strict point; zero solutions;
solutions vanishing at both endpoints or on a subinterval; repeated, non-isolated, or endpoint
zeros; coefficients that vanish, change sign, or lack the required regularity; singular endpoints;
and self-adjoint leading coefficients that fail positivity or nonvanishing assumptions. Intake
silently excludes none of these cases.

## Substitution exclusions

- `THM-M-1386`, Sturm's separation theorem for zeros of two linearly independent solutions of the
  same equation, is a neighboring but different catalog item.
- `THM-M-1384`, general Sturm-Liouville theory, cannot replace this comparison theorem.
- Sturm's polynomial theorem, Sturm sequences, and real-root-counting algorithms are different
  results despite sharing the name Sturm.
- Picone comparison, matrix systems, difference equations, time scales, nonlinear extensions,
  singular comparison theorems, and eigenvalue comparison need approved checked transports before
  they can be treated as alternate encodings.
- A special constant-coefficient trigonometric example or one numerical interval cannot replace
  the variable-coefficient theorem family.
- A structure, predicate, or hypothesis that assumes the desired zero-between-zeros result is not a
  proof.
- Generic derivative, integral-curve, interval, set, or zero APIs and the catalog's `verified`
  label provide no target or proof credit.

## Formal boundary

Pinned mathlib provides real derivatives, integral-curve predicates, intervals, and set-level zero
predicates. The intake probe checks those names only. The statement phase must select and map an
exact source proposition, minimize imports, elaborate and fingerprint the complete Lean target,
compile checked transports for any alternate encoding, and mutation-test removed hypotheses,
changed domains, changed binder scope, and boundary cases. No obligation registry or proof graph is
frozen at intake.
