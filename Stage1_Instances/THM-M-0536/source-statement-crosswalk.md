# Source-statement crosswalk

## Repository source

`Docs/Stage0_Blueprint.md:14685-14688` names `THM-M-0536` and states: "同伦等价空间有相同的同调群"
(homotopy equivalent spaces have the same homology groups). The rev-5.6 manifest repeats the name,
category, and an untrusted "verified" source label, but supplies no proof citation or conventions.
The label therefore provides no H0 or machine credit.

## Candidate theorem sources

- Allen Hatcher, *Algebraic Topology* (2002), Chapter 2, Section 2.1, Proposition 2.10 and
  Corollary 2.11 are candidate modern statement/proof anchors: homotopic maps induce the same
  homology map, hence homotopy equivalent spaces have isomorphic homology groups. Exact PDF page,
  coefficient convention, edition identity, and errata have not yet received independent review.
- Samuel Eilenberg and Norman Steenrod, *Foundations of Algebraic Topology* (Princeton University
  Press, 1952) is a candidate foundational source for the homotopy axiom. The exact chapter,
  theorem/page, relationship to the singular-homology formulation, and errata remain to be audited.

These remain human-source discovery anchors pending the separately assigned anchor audit. For the
statement phase, Hatcher's ordinary singular-homology reading fixes integral coefficients (his
default convention in Section 2.1), natural grading, and the induced-map conclusion of Corollary
2.11. This is sufficient to avoid inventing a different homology theory, but it does not promote H1.

## Crosswalk

| Repository component | Mathematical reading | Required Lean component | Intake status |
|---|---|---|---|
| "spaces" | topological spaces `X`, `Y` | `(X Y : Type) [TopologicalSpace X] [TopologicalSpace Y]` | frozen and elaborated |
| "homotopy equivalent" | maps with homotopy-inverse laws | `e : ContinuousMap.HomotopyEquiv X Y` | frozen and elaborated |
| "homology groups" | unreduced integral singular homology in degree `n : ℕ` | `singularHomologyFunctor (ModuleCat ℤ) n`, coefficient `ModuleCat.of ℤ ℤ` | frozen and elaborated |
| "same" | forward induced map is an isomorphism | `IsIso (...map (TopCat.ofHom e.toFun))` | frozen and elaborated |
| forward/inverse laws | induced maps compose to identities by functoriality and homotopy invariance | checked composition plus induced-map equality | required downstream proof boundary |

## H-status boundary

The human theorem is standard and candidate proof sources are identified, but the exact edition,
pinpoint statement, assumptions, coefficient conventions, proof-to-node mapping, errata, and
independent reviewer are not frozen. The dossier therefore remains `H1`, not `H0`. The canonical
Lean expression now elaborates, but no proof or source-to-formal audit is accepted, so machine
status remains `M4`.
