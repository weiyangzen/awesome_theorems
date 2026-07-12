# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` provide only the generic title,
Andreas Floer attribution, year 1988, and invariant gloss. They provide no citation, definition,
theorem locator, hypotheses, or proof. In particular, the wording does not decide between the
Hamiltonian and Lagrangian theories or the low-dimensional gauge-theory variants.

## Candidate primary sources

- Andreas Floer, "Morse theory for Lagrangian intersections", *Journal of Differential Geometry*
  28 (1988), 513-547. Candidate for a Lagrangian-intersection construction/invariance target.
- Andreas Floer, "Symplectic fixed points and holomorphic spheres", *Communications in
  Mathematical Physics* 120 (1989), 575-611. Candidate for a Hamiltonian fixed-point/Floer-homology
  target in a specified symplectic regime.
- Andreas Floer, "Witten's complex and infinite dimensional Morse theory", *Journal of
  Differential Geometry* 30 (1989), 207-221. Candidate for the chain-complex and continuation
  framework, but not automatically the exact theorem intended by the repository title.

These bibliographic entries are discovery anchors only. Exact theorem numbers/pages, edition or
scan identity, definitions, assumptions, proof-node mapping, and errata have not been inspected and
therefore do not establish `H0`. An independent source review remains required.

## Provisional crosswalk

| Repository phrase | Possible mathematical component | Source decision required | Required Lean component | Intake status |
|---|---|---|---|---|
| "Floer homology" | homology of a trajectory-counting chain complex | select one Floer variant and theorem | concrete generator type, graded chains, differential, homology | family identified; exact objects open |
| symplectic geometry | Hamiltonian periodic-orbit or Lagrangian-intersection theory | select geometric category and compactness hypotheses | symplectic manifold and Hamiltonian/Lagrangian APIs | ambiguous |
| low-dimensional topology | gauge-theoretic Floer invariant | decide whether this is intended at all | connections/moduli/gauge quotient infrastructure | excluded unless explicitly selected; overlaps `THM-M-0610` |
| invariant | independence of auxiliary data or geometric isotopy/diffeomorphism invariance | select exact equivalence and quantifier order | continuation maps, chain homotopies, induced homology equivalence | conclusion open |
| trajectory count | differential and `d^2 = 0` | fix regularity, compactness, gluing, orientations, coefficients | finite signed/mod-2 counts and boundary-of-moduli argument | analytic interface open |

## Lean discovery boundary

A scoped repository and pinned-mathlib text search found no declaration mentioning Floer homology.
The nearby symplectic legacy file discusses missing pseudoholomorphic-curve infrastructure but does
not encode this target. Text-search absence is not a full anchor audit; it supports only `M4` at
intake. The statement phase must elaborate a source-faithful expression before any formal candidate
can receive credit, and the later anchor audit must repeat a declaration/API search against the
pinned revision.
