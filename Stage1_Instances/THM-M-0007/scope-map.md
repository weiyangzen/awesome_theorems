# Scope map

## Included mathematical boundary

- Abelian categories `C`, `D`, and `E`, with enough injectives where right-derived functors require
  them, and additive left-exact functors `F : C -> D` and `G : D -> E`.
- The acyclicity condition: every injective `I` of `C` is sent by `F` to a `G`-acyclic object.
- A natural first-quadrant cohomological spectral sequence with page
  `E_2^{p,q} ~= R^p G (R^q F(X))` and abutment `R^{p+q}(G composed with F)(X)`.
- Naturality in `X`, the actual differential/bidegree structure, and a precise convergence notion.

## Choices reserved for the statement phase

The next node must freeze the exact source convention for functor composition, enough-injectives
assumptions, the definition of `G`-acyclic, indexing and page orientation, boundedness, convergence,
and whether the result is objectwise or a natural spectral sequence of functors. It must also pin
the Lean toolchain, imports, declaration type, and environment fingerprint, then mutation-test the
left-exactness and acyclicity hypotheses.

## Explicit exclusions

- A long exact sequence, derived-functor existence theorem, or hypercohomology spectral sequence as
  a substitute for the Grothendieck spectral sequence.
- Merely packaging the expected page and abutment as unrelated object isomorphisms.
- Treating opaque `Prop` fields called naturality or convergence as their mathematical content.
- The legacy `S1_M_094.lean` module or an external theorem name as accepted proof evidence.

Boundary cases to inspect include zero objects, vanishing higher derived functors, `p = 0` or
`q = 0`, and collapse when one functor is exact.
