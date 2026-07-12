# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` contains two identical source records named `s-配边定理`. Each
attributes the result to Dennis Sullivan (1967), summarizes it as "simple homotopy equivalence and
h-cobordism," and labels it `已验证`. `Docs/Stage0_Blueprint.md` supplies only the theorem name. The
rev-5.6 manifest repeats the name and carries that label as `source_status_untrusted`.

These records establish the intended topic but not an exact theorem. In particular they omit the
smooth/PL/topological category, dimension bound, compactness and connectedness, boundary data,
torsion convention, and product conclusion. The verified label supplies neither source-fidelity
nor Lean proof evidence.

## Primary-source candidates

- Barry Mazur, "Relative neighborhoods and the theorems of Smale," *Annals of Mathematics* 77
  (1963), 232-249.
- John Stallings, "On infinite processes leading to differentiability in the complement of a
  point," in *Differential and Combinatorial Topology (A Symposium in Honor of Marston Morse)*,
  Princeton University Press (1965), 245-254.
- D. Barden, "The structure of manifolds," unpublished/limited-circulation work commonly cited in
  historical attributions of the s-cobordism theorem.

These are bibliographic discovery anchors, not accepted source receipts. This intake did not inspect
stable scans to locate exact theorem numbers or verify assumptions, proof genealogy, or errata.
The later source audit must do that work and must resolve the repository's Sullivan/1967
attribution against the historical Barden-Mazur-Stallings attribution. A modern exposition may aid
notation, but cannot silently replace the required primary-source genealogy.

## Statement crosswalk

| Repository/source phrase | Frozen mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "h-cobordism" | compact smooth cobordism with both boundary inclusions homotopy equivalences | manifold-with-boundary and relative homotopy-equivalence structures | included; API open |
| "simple homotopy equivalence" | incoming inclusion is simple | finite cellular model plus simple-homotopy predicate | included; representation open |
| s-condition | Whitehead torsion of `M0 -> W` vanishes in `Wh(pi1 M0)` | fundamental group, group ring, Whitehead group, and torsion | included; conventions open |
| high dimension | `dim W >= 6` | exact natural-number dimension hypothesis | included; source convention open |
| product conclusion | `W` is diffeomorphic to `M0 x [0,1]` relative to `M0` | relative diffeomorphism respecting boundary/collar data | included; encoding open |
| converse | a relative product has zero torsion | reverse implication in the same exact proposition | included; proof architecture open |

## Lean discovery boundary

A scoped text search of repository Lean/instance artifacts and the canonical pinned mathlib source
used the query family `s-cobord`, `simple homotopy`, `Whitehead torsion`, `WhiteheadTorsion`, and
`hCobord`. It found no exact declaration or target-specific legacy module. References in other
theorem dossiers describe open s-cobordism obligations and are not reusable proof bodies.

This result is only intake discovery. The anchor-audit phase must repeat symbol, module, declaration,
and upstream-project searches at immutable revisions and record exact candidate types, bodies,
axioms, licenses, and dependency feasibility. Before statement acceptance, a reviewed primary
source must be mapped row by row to a canonical Lean proposition, including category, dimension,
relative-boundary behavior, torsion basepoint choices, and all degenerate cases.
