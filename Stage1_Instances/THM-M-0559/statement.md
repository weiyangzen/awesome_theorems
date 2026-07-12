# Statement freeze

Item: `S56-M-0559-STATEMENT`

`Statement.lean` freezes the unbased, possibly disconnected form of Whitehead's theorem. For
whole-space CW complexes `X` and `Y`, it states that a continuous map `f : X -> Y` which is
bijective on path components and bijective on every positive-dimensional based homotopy group is
the forward map of a homotopy equivalence.

## Encoding decisions

- Whole-space CW structures are `Topology.CWComplex (Set.univ : Set X)` and similarly for `Y`.
- Path components are `ZerothHomotopy`; `zerothHomotopyMap` is the quotient map induced by `f`.
- `homotopyGroupMap f n x` is defined by postcomposition of `GenLoop (Fin n)` representatives and
  quotient functoriality. The quotient-respect proofs are checked by Lean.
- Dimension zero is represented only by `ZerothHomotopy`. Homotopy-group hypotheses start at
  `1 <= n`, so the two conditions are not conflated.
- The conclusion binds `e.toFun = f`; existence of an unrelated homotopy equivalence is explicitly
  excluded.
- Empty and disconnected CW complexes remain in scope. No inhabitedness, connectedness, or chosen
  global basepoint is added.

The canonical declaration is `Stage1Instances.THM_M_0559.WhiteheadTarget`. The checked theorem
`whiteheadTarget_iff_expandedSourceShape` expands the named weak-equivalence predicate by `Iff.rfl`.
Three separately elaborated mutations remove the component condition, change the dimension
boundary, or weaken the conclusion to an unrelated equivalence; none is canonical.

## Minimal pinned imports

The direct imports are `Mathlib.Topology.CWComplex.Classical.Basic`,
`Mathlib.Topology.Homotopy.Equiv`, and `Mathlib.Topology.Homotopy.HomotopyGroup`, from pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. Each owns one target-facing interface: CW
structures, homotopy equivalences, or homotopy groups. The component quotient is supplied
transitively by the homotopy-group module.

This phase establishes exact target elaboration only. It supplies no proof of Whitehead's theorem,
no primary-source acceptance, no anchor audit, and no theorem-completion credit.
