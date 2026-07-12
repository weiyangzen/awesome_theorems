# Scope map

## Included claim

- `X` and `Y` are topological spaces equipped with CW-complex structures.
- `f : X -> Y` is a specified continuous map.
- Weak homotopy equivalence is expanded into two requirements: a bijection on path components and
  isomorphisms `pi_n(X, x) -> pi_n(Y, f(x))` for every `x : X` and every `n >= 1`.
- The conclusion is relative to `f`: there is a homotopy inverse for `f`, equivalently a homotopy
  equivalence whose forward continuous map is `f`.
- Disconnected and empty CW complexes remain included. The component condition handles dimension
  zero; higher homotopy groups carry explicit basepoints.

## Statement-phase decisions

The formal encoding must choose a concrete map on path components and functorial induced maps on
`HomotopyGroup.Pi`. It must also connect whole-space CW structures to the pinned mathlib
`CWComplex C` interface, likely with `C = Set.univ`, without replacing the CW hypothesis by an
unrelated finiteness or local-contractibility condition. Binder order, universe levels, and the
representation of positive dimensions must then be frozen and mutation-tested.

The source audit must determine whether the selected primary theorem is stated for connected CW
complexes, arbitrary CW complexes, or CW-type spaces. If it is connected, a separately checked
componentwise bridge is required for this canonical disconnected formulation.

## Explicit exclusions

- The converse, that a homotopy equivalence induces homotopy-group isomorphisms, as a substitute.
- A statement only about simply connected spaces, homology isomorphisms, or fundamental groups.
- Whitehead torsion, simple homotopy equivalence, or the simple-homotopy Whitehead theorem.
- The Whitehead product and the long exact sequence of a pair.
- Existence of an unrelated homotopy equivalence between `X` and `Y` that does not identify `f` as
  its forward map.
- A result for spaces merely having CW homotopy type unless an exact checked transport to the
  chosen canonical statement is supplied.
