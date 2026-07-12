# Scope map

## Included claim

Let `M` be a closed oriented smooth manifold of dimension `4k`. Its oriented fundamental class and
cup product give a symmetric middle-dimensional intersection pairing. The theorem identifies the
signature of that pairing with the characteristic number

```text
<L_k(p_1(TM), ..., p_k(TM)), [M]>.
```

Here `L_k` is the degree-`4k` Hirzebruch `L`-polynomial and `p_i(TM)` are the Pontryagin classes of
the real tangent bundle. This is an equality in the integers after the rational characteristic
class is evaluated. The formal statement must construct or import both sides; it may not store the
equality as structure data.

## Domains and binders to freeze at statement phase

- Whether the selected source assumes `M` connected, and whether the theorem is stated for smooth
  manifolds or first for an oriented differentiable manifold in an older convention.
- The exact cohomology coefficients used to define the intersection form and rational `L`-class,
  plus the checked agreement of rational and real signatures.
- The orientation/fundamental-class representation and sign convention for the intersection form.
- The normalization of Pontryagin classes and the multiplicative sequence with characteristic
  power series `sqrt(x) / tanh(sqrt(x))` (or the source's equivalent convention).
- Binder order, universes, finiteness hypotheses, tangent-bundle model, and all typeclass inputs.
- Whether `k = 0`, the empty manifold, and disconnected manifolds are included by the source or are
  handled through separately checked additivity and boundary lemmas.

## Required formal interfaces

The eventual target needs concrete APIs for closed oriented smooth manifolds, tangent bundles,
Pontryagin classes, rational cohomology and cup product, a fundamental-class evaluation, the
middle-dimensional intersection form, finite-dimensional signature, the `L`-polynomial, and the
bridge from its top-degree evaluation to an integer. Missing interfaces must be recorded as API
blockers, not replaced with arbitrary types or assumed packages.

## Explicit exclusions

- The index theorem for the signature operator without a checked equivalence to the stated
  characteristic-number formula.
- Only the four-dimensional specialization `signature(M) = <p_1(TM),[M]>/3`.
- A theorem for complex projective varieties, a cobordism-invariance statement, or a congruence
  consequence substituted for the general smooth `4k`-manifold theorem.
- A definition of `L`-genus as the manifold signature, which would make the result tautological.
- An abstract record containing the intersection form, characteristic number, or their equality as
  assumed fields.
- The Stage0 `已验证` label or mathematical consensus treated as Lean kernel evidence.
