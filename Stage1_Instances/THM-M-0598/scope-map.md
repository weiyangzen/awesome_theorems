# Scope map

## Frozen repository scope

- The inventory name is "Morse theory", attributed to Marston Morse and dated 1934.
- Its only mathematical gloss is the relationship between manifold topology and critical points of
  smooth functions.
- This wording identifies a theorem family but does not determine a single exact proposition.

## Provisional central claim family

- A finite-dimensional smooth manifold `M` and a sufficiently regular real-valued Morse function
  `f`, with compactness or properness assumptions supplied by the selected source.
- Regular-interval behavior: sublevel sets at two regular levels with no intervening critical point
  have the same source-specified smooth or homotopy type.
- Critical-level behavior: crossing one isolated nondegenerate critical point attaches a handle (or
  the source's equivalent cell) whose dimension is the Morse index.
- The conclusion must explicitly identify the two sublevel sets, attachment map/pair, equivalence
  notion, and any smoothing of corners.

## Decisions required at statement freeze

The next phase must select one exact theorem rather than conjoin folklore. It must fix the source
edition and theorem/page; whether `M` is compact, closed, or has boundary; properness and
boundedness of `f`; finite dimension and scalar field; regular values and endpoint conventions;
whether critical values or critical points are isolated; whether exactly one critical point occurs
in the band; the Hessian/nondegeneracy and Morse-index definitions; and whether the conclusion is a
diffeomorphism, deformation retract, homotopy equivalence, CW-cell attachment, or smooth handle
attachment. Empty bands, multiple equal critical values, extrema of index `0` or `dim M`, boundary
critical points, and noncompact manifolds require explicit treatment.

## Explicit exclusions

- Morse inequalities (`THM-M-0599`) or the Morse lemma (`THM-M-0600`) as substitutes for this root.
- Morse homology, Floer theory, infinite-dimensional Morse theory, or a numerical critical-point
  count unless the selected source makes that exact claim the root.
- A theorem merely saying that a Morse function exists, or an abstract structure that assumes the
  desired handle attachment/equivalence as a field.
- Treating the repository label `已验证`, nearby differential-topology APIs, or a statement-only
  formalization as proof evidence.

No Lean statement is frozen at intake. The formal target must expose the manifold, function,
sublevel sets, critical-point hypotheses, index, and topological change, or record the first exact
missing API without weakening the claim.
