# Proof outline — two-variable cancellation

The frozen claim is the solved two-variable variant of the Zariski
Cancellation Problem.  Its root proposition is

`{k : Type*} [Field k] : IsCancellative k (MvPolynomial (Fin 2) k)`.

The outline is represented as a typed DAG in `proof-units.json`:

1. bind the exact provider declaration and elaborated root expression;
2. transport that root into the claim-owned Lean surface;
3. compose the proof object at the exact root;
4. reconstruct every node through content-addressed readable fragments;
5. replay all steps cold under the pinned trust-zero environment.

The worker package supplies the evidence boundary and leaves final kernel
acceptance to Master.  No hypothesis, inference edge, output, exception, or
trust boundary is omitted from the inventory.
