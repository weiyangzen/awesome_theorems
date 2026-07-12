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

These are discovery anchors only. The statement phase must inspect and select a stable edition;
the anchor-audit phase must separately investigate formal candidates at the pinned revision.

## Crosswalk

| Repository component | Mathematical reading | Required Lean component | Intake status |
|---|---|---|---|
| "spaces" | topological spaces `X`, `Y` | types with `TopologicalSpace` instances and universe policy | included; binders open |
| "homotopy equivalent" | maps `f : X -> Y`, `g : Y -> X` with composites homotopic to identities | packaged homotopy equivalence or explicit continuous maps and homotopies | included; encoding open |
| "homology groups" | degreewise singular homology with fixed coefficients | concrete homology functor/object and coefficient parameters | included; theory and coefficients open |
| "same" | group/module isomorphism | an induced degreewise `Iso`/equivalence preserving algebraic structure | fixed as isomorphic, exact category open |
| forward/inverse laws | induced maps compose to identities by functoriality and homotopy invariance | checked composition plus induced-map equality | required downstream proof boundary |

## H-status boundary

The human theorem is standard and candidate proof sources are identified, but the exact edition,
pinpoint statement, assumptions, coefficient conventions, proof-to-node mapping, errata, and
independent reviewer are not frozen. The intake therefore records `H1`, not `H0`. No canonical Lean
expression or checked source-to-formal transport exists yet, so the machine status remains `M4`.
