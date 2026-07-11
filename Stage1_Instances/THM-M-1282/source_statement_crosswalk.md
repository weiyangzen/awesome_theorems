# Source-statement crosswalk

| ID / claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| `SRC-1282-ROOT`: compact locally conformally flat `n >= 3` manifold has a constant-scalar-curvature conformal metric | Repository Stage0 record, `THM-M-1282`, says `Yamabe问题(共形平坦)` and attributes it to Richard Schoen (1984) | No repo-local declaration identified | This is the scope being frozen, but Stage0 is metadata, not primary evidence: `H2`, `M4` |
| Schoen's 1984 contribution to the Yamabe problem | R. Schoen, "Conformal deformation of a Riemannian metric to constant scalar curvature," *Journal of Differential Geometry* 20 (1984), 479-495, DOI `10.4310/jdg/1214439291` | Future root and proof-architecture nodes | Primary paper identified bibliographically; the paper's scope is broader than the Stage0 parenthetical, so an exact theorem/page/assumption crosswalk and errata review are required before `H0` |
| Conformal metric formulation | Same geometric problem; exact pinpoint pending | Future manifold/metric declaration and an existential positive smooth conformal factor | Mathematical encoding candidate only; exponent, dimension representation, and connectedness convention remain open |
| Yamabe PDE formulation | Schoen 1984, analytic setup and variational argument; exact equation/page pin pending | Future conformal Laplacian and positive-solution expression | Candidate alternate encoding; no checked transport |
| Variational minimizer formulation | Schoen 1984, Yamabe functional framework; exact proposition/page pin pending | Future Sobolev quotient/minimizer expression | Candidate alternate encoding; no checked transport or library-feasibility claim |

## Scope discrepancy and required resolution

The source title and standard historical attribution concern completion of the Yamabe problem, while
the repository record narrows `THM-M-1282` to the conformally flat case. This intake does not broaden
the theorem to all compact manifolds and does not infer that every hypothesis used in the 1984
argument belongs in the target. The statement phase is blocked from claiming exactness until a
primary-source passage is pinned for precisely the narrow claim, or the integration lane supplies an
authoritative correction without changing this worker's owned scope.

The later source audit must archive an immutable copy/hash, identify theorem or page ranges and all
assumptions, check published corrections/errata, and map each premise to a formal binder. It must also
distinguish the locally conformally flat case from the non-locally-conformally-flat Aubin inequality
and from dimension/spin qualifications historically associated with positive-mass inputs.

Discovery link (not an immutable evidence receipt):

- Schoen paper: <https://doi.org/10.4310/jdg/1214439291>

No `H0` or machine-closure claim is made.
