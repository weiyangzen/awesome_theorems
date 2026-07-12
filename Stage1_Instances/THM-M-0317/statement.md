# Exact statement receipt

Item: `S56-M-0317-STATEMENT`. This receipt claims statement elaboration only, not a proof of the
fixed-point theorem and not acceptance of any downstream node.

## Source-fidelity decision

The canonical claim is the theorem printed in A. Tychonoff, "Ein Fixpunktsatz," *Mathematische
Annalen* **111** (1935), section 2, p. 770:

> Bei jeder stetigen Abbildung einer konvexen, bikompakten Menge eines linearen topologischen
> lokal-konvexen Raumes in sich gibt es wenigstens einen Fixpunkt.

In English: every continuous self-map of a convex compact subset of a locally convex topological
linear space has at least one fixed point. Section 1, pp. 767-768 defines scalars as real numbers,
defines a topological linear space by continuous addition and scalar multiplication, states that
such a space is necessarily Hausdorff and regular under the cited convention, and defines local
convexity by a convex-neighborhood basis at zero. Thus `Statement.lean` uses `Module ℝ E`,
`IsTopologicalAddGroup E`, `ContinuousSMul ℝ E`, `T2Space E`, and `LocallyConvexSpace ℝ E`.
The source's nonempty intent is made explicit: without it the empty compact convex set falsifies
the conclusion.

The inspected stable scan is the Goettingen digitization of volume 111, persistent work ID
`PPN235181684_0111`; its IIIF canvases `00000771` through `00000780` are printed pages 767-776.
DOI `10.1007/BF01472256` independently identifies the same article and pagination. Errata and
independent source review remain downstream human-source work, so this receipt does not claim `H0`.

## Formal target

The canonical Lean declaration is
`AwesomeTheorems.THM_M_0317.TychonoffFixedPointTarget` in `Statement.lean`. Its ordered context is:

1. universe `u`, ambient `E : Type u`;
2. real topological vector-space structures, Hausdorff separation, and real local convexity;
3. subset `K : Set E` and ambient map `f : E -> E`;
4. `K.Nonempty`, `IsCompact K`, `Convex ℝ K`, `Continuous f`, and `Set.MapsTo f K K`;
5. conclusion `exists x in K, Function.IsFixedPt f x`.

The two declared imports are the narrow modules owning local convexity and the fixed-point
predicate. The checked theorem `ambient_subtype_fixed_point_iff` transports the conclusion to the
equivalent subtype self-map encoding. It is a transport only and supplies no existence proof.

The environment fingerprint is Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; repository base
`1794fae27ddcf6d19b6984502e27a9233890d8d1`; `lean-toolchain` SHA-256
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; and
`lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. The canonical source plus
printed elaboration has receipt hash
`94c90b4b7a6dda1083b80b80907264b91e89cf5f2a6cb285e06a161be238dff2` plus
`3e984e643a23974aa55134e30794113e0709761ed1c6f366ef624f8067b6cd7b`.

## Mutation and boundary checks

Four kernel-checked negative witnesses reject the required non-equivalent mutations: removing
nonemptiness on the empty boundary, replacing an in-domain fixed point with an ambient fixed point,
moving the fixed-point existential before the map binder, and removing `MapsTo` using translation
by two on `[0,1]`. These declarations establish that those mutations cannot be credited as the
canonical target.

## Status boundary

This is an `M3` statement/interface artifact. No `sorry`, axiom, theorem assumption, placeholder,
or proof of `TychonoffFixedPointTarget` occurs. The anchor audit, obligation registry, theorem proof,
trust closure, hermetic replay, and independent review remain open.
