# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Symmetrization lowers the Dirichlet integral | G. Polya and G. Szego, *Isoperimetric Inequalities in Mathematical Physics*, Annals of Mathematics Studies 27, Princeton University Press (1951), the symmetrization/Dirichlet-integral treatment | none located in the repo-local mathlib search | Historical primary monograph identified, but theorem/page, edition hash, assumptions, and errata are not yet audited |
| Finite-`p` Sobolev formulation `||grad u*||_p <= ||grad u||_p` | F. Brock, "Continuous rearrangement and symmetry of solutions of elliptic problems," *Proceedings of the Indian Academy of Sciences (Mathematical Sciences)* 110 (2000), 157-204, as a discovery route to modern formulation and proof genealogy | no exact declaration identified | Secondary formulation anchor only; immutable source and premise mapping remain open |
| Equality/rigidity conditions | J. E. Brothers and W. P. Ziemer, "Minimal rearrangements of Sobolev functions," *Journal fur die reine und angewandte Mathematik* 384 (1988), 153-179 | none | Neighboring refinement deliberately excluded from the root; useful later for boundary auditing |
| Bounded-domain zero-extension form | Classical consequence of the whole-space inequality for `W_0^{1,p}` | no checked wrapper | Alternate encoding only; requires formal zero-extension and symmetric-ball transport |

The Stage0 description alone does not say whether only the quadratic Dirichlet energy or the full
finite-`p` Sobolev inequality is intended. This intake adopts the standard stronger named theorem and
records the quadratic form only as its specialization. It does not claim that the cited sources have
yet passed `H0`: page-level statement text, all conventions, edition/file hashes, corrections, and
independent review remain required.

No public Lean closure is claimed. The statement phase must first establish the availability or
required definitions for distribution functions, Schwarz rearrangement, Sobolev membership, and
weak-gradient energy; it must then serialize the exact expression and mutation-test the scope before
the anchor audit observes proof candidates.
