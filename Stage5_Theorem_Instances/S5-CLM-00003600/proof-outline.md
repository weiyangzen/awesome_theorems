# Proof outline

## H-PROBLEM — Problem and quantifier polarity

`answer(False)` reduces the left side of the frozen biconditional to `False`. Thus it suffices to refute the assertion that every qualifying polynomial has only convex sublevel-set components.

## H-COUNTEREXAMPLE — Concrete polynomial counterexample

Take `f(z)=z^6-z`, `c=0.582`, and `m=6`. The proof establishes monicity, exactly six distinct roots, and positivity of `c`.

## H-ROOTS — Six roots

Factor `f=X(X^5-1)`. Separability of `X^5-1` and an explicit fifth-root-of-unity enumeration show that the roots are `0` together with five distinct fifth roots of unity, hence `(f.rootSet ℂ).ncard=6`.

## H-COMPONENTS — Six components

The critical circle and five boundary rays lie outside the `c`-sublevel set. Six pairwise-disjoint open regions—one inner disk and five angular sectors—therefore cover it. Connectedness forces each root component into its own region; the root-to-component image is bijective, so there are six components.

## H-NONCONVEX — Non-convex component

Two points on radial segments from zero lie in the zero component. Their midpoint is evaluated explicitly and lies outside the sublevel set. If that component were convex, it would contain the midpoint, a contradiction.

## H-ROOT — Biconditional closure

The counterexample refutes the universal right-hand proposition. Both sides of the frozen biconditional are false, yielding the exact theorem. No source `sorry` theorem is invoked.
