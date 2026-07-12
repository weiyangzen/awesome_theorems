# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9978-9983` supplies exactly the title `KAM theory`, attribution to
Kolmogorov/Arnold/Moser, the year 1963, the gloss `近可积哈密顿系统的稳定性` (`stability of
nearly integrable Hamiltonian systems`), importance `high`, and status `verified`. Git history
places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:37236-37261` repeats the metadata but explicitly leaves the exact
definitions and premises, proof route, dependencies, equivalent forms, axiom policy,
machine-checked status, and artifact links open. The rev-5.6 manifest preserves `verified` only as
untrusted metadata and resets this target to `L0 / rework_required`.

The catalog contains no bibliography, theorem or page locator, Hamiltonian formula, phase space,
ordered binders, hypotheses, conclusion, incorporated definitions, constants, proof boundary,
translation provenance, correction record, or reviewer. Its wording names an umbrella theory and
a phenomenon; it is not one stable truth-valued proposition.

## Literal crosswalk

| Catalog element | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `KAM theory` | Kolmogorov, Arnold, Moser, measure, differentiable, isoenergetic, and later branches | one exact source-versioned `Prop` | umbrella theory, not a proposition |
| nearly integrable | `H = h + epsilon f` or another source-specific perturbative model | Hamiltonian carrier, split, norm, and smallness relation | model and quantifiers absent |
| Hamiltonian system | action-angle flow, symplectic map, lower-dimensional torus, or another setting | phase space, symplectic form, vector field or map, trajectory semantics | carrier and dynamics absent |
| stability | invariant-torus persistence, conjugacy, positive-measure survival, or finite-time action confinement | embedding or transform, invariance equation, estimates, measure or time quantifiers | conclusion absent |
| Kolmogorov/Arnold/Moser | three historically different branches and proof roles | source provenance and node mapping only | no root or source edition selected |
| 1963 | Arnold proof year or broad KAM chronology | immutable source locator only | conflicts with 1954/1962 component dates |
| `verified` | untrusted inventory field | accepted source review and kernel receipt would be required | no H or M credit |

## Source-family discovery boundary

A. N. Kolmogorov's 1954 note is cataloged as *On the Preservation of Conditionally Periodic
Motions Under Small Variations of the Hamilton Function*, *Doklady Akademii Nauk SSSR* 98(4),
527-530. A later English reprint, *Preservation of conditionally periodic movements with small
change in the Hamilton function*, has pages 51-56 and DOI `10.1007/BFb0021737`. These are strong
leads for the original analytic branch, not a selection of the umbrella target.

V. I. Arnol'd's *Proof of a theorem of A. N. Kolmogorov on the invariance of quasi-periodic motions
under small perturbations of the Hamiltonian*, *Russian Mathematical Surveys* 18(5) (1963), 9-36,
DOI `10.1070/RM1963v018n05ABEH004130`, is a stable primary proof-source lead matching the catalog
year. It does not by itself identify all of KAM theory with its particular contract.

J. K. Moser's 1962 work *On invariant curves of area-preserving mappings of an annulus* is the
historical differentiable twist-map branch. The repository separately owns that result as
`THM-M-1371`, so its source and proof cannot be transferred to this umbrella root.

Luigi Chierchia and John Mather, *Kolmogorov-Arnold-Moser theory*, Scholarpedia 5(9):2123 (2010),
DOI `10.4249/scholarpedia.2123`, revision 91405, distinguishes Kolmogorov's fixed-frequency analytic
normal-form theorem, Arnold's proof scheme, Moser's differentiable twist-map case, positive-measure
consequences, and later variants. It is a reviewed secondary discriminator only. Its breadth
confirms that the catalog theory label does not choose a single root; it cannot supply primary
source `H0` evidence.

No complete source edition, exact result, incorporated-definition map, proof boundary, translation
and correction audit, repository-owned immutable source packet, or independent source review is
accepted. The discovery leads receive no H0 or proof credit.

## Neighbor and duplicate boundary

The adjacent mathematical records separately name the original Kolmogorov-Arnold theorem,
Moser's twist theorem, Nekhoroshev's finite-time estimate, generic Hamiltonian systems, and
Liouville-Arnold integrability. That separation is affirmative evidence against choosing one as a
silent synonym for this umbrella item.

`Docs/researches/physics_theorems.md:6613-6619` and `Docs/Stage0_Blueprint.md:66581-66608` contain
`THM-P-0774`, a physics-catalog record saying that most nonresonant tori remain intact under a small
perturbation. It is absent from the 1546-target rev-5.6 manifest. Its more specific wording helps
expose one possible branch but supplies no target identity, source, status, or proof credit.

## Source gate

Before an approved correction can leave `H5`, an accountable owner must preserve and hash an
immutable primary source, select one exact theorem and justify why it represents `THM-M-1369`
rather than a neighboring record, transcribe every incorporated definition, ordered binder,
hypothesis, conclusion, constant dependency, and boundary case, map the complete proof and
correction boundary, and obtain independent source review. A correction that instead redirects or
splits this topic must preserve the original non-propositional record and make root ownership
explicit.

Only after that decision may a statement phase freeze minimal imports, a canonical Lean
expression, checked transports, expression and environment fingerprints, and the required
mutations. Until then the mathematical and Lean targets remain null.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`AnalyticAt`, `UnitAddTorus`, `UnitAddTorus.mFourier`, `IsIntegralCurve`, `Flow`, `Matrix.J`,
`Matrix.J_transpose`, and `Matrix.symplecticGroup`. A bounded case-insensitive search found no KAM
or Hamiltonian quasi-periodic persistence declaration in repo-local Lean or pinned mathlib. The
legacy Liouville-Arnold file contains only the neighboring integrability boundary.

These are discovery facts only, not an exhaustive external candidate audit or a proof of absence.
No canonical statement, proof body, audit completion, or theorem completion is claimed.
