# Source-statement crosswalk

## Repository source record

`Docs/Stage0_Blueprint.md` and `Docs/researches/math_theorems.md` provide the title, Nathan
Seiberg/Edward Witten attribution, year 1994, and the gloss "new invariants of four-manifolds".
They provide no theorem number, page, exact assumptions, proof, errata audit, or formal declaration.
Their `已验证` label is explicitly untrusted under rev-5.6 and supplies no `H0` or machine credit.

## Candidate primary sources

- Edward Witten, "Monopoles and Four-Manifolds", *Mathematical Research Letters* **1** (1994),
  769-796, DOI `10.4310/MRL.1994.v1.n6.a13`. This is the primary discovery candidate for the
  four-manifold invariants defined from monopole equations. A stable copy, exact pages/equations,
  incorporated definitions, and corrections have not yet been audited.
- Nathan Seiberg and Edward Witten, "Electric-Magnetic Duality, Monopole Condensation, and
  Confinement in N=2 Supersymmetric Yang-Mills Theory", *Nuclear Physics B* **426** (1994), 19-52,
  DOI `10.1016/0550-3213(94)90124-4`, with erratum **430** (1994), 485-486, DOI
  `10.1016/0550-3213(94)00449-8`. This is physical genealogy, not by itself a pinpoint source for
  one mathematical four-manifold invariance theorem.

These are bibliographic discovery anchors only. Neither has been admitted as immutable, reviewed
source evidence in this dossier.

## Metadata-to-statement crosswalk

| Repository phrase | Candidate source meaning | Required formal component | Intake disposition |
|---|---|---|---|
| "Seiberg-Witten invariants" | a family indexed by `Spin^c` data and defined from monopole moduli spaces | index type, equations, quotient, orientation, codomain, and choice-independence | family identified; exact root unresolved |
| "new invariants" | construction plus a theorem that the output does not depend on prohibited auxiliary choices | quantified choice data and exact equality/chamber conclusion | likely central claim; not source-frozen |
| "four-manifolds" | smooth oriented four-manifolds, with source-specific compactness and Betti hypotheses | concrete manifold category and every required predicate | domain family identified; assumptions open |
| 1994 / Seiberg and Witten | historical locator for the physical and mathematical papers | provenance only | no theorem or proof credit |
| `已验证` | secondary inventory status | none | rejected as source and kernel evidence |

## Required next crosswalk

Before statement acceptance, a source reviewer must select one stable primary edition and record the
pinpoint proposition, pages and incorporated definitions; audit errata; enumerate every manifold,
orientation, Betti-number, `Spin^c`, regularity, reducible, dimension and coefficient hypothesis;
separate gauge invariance, compactness, transversality, orientation and metric/perturbation
independence; and distinguish the `b2+ > 1` and chamber-dependent cases. An independent reviewer
must approve that mapping.

The formal crosswalk must then map every sourced object and binder to concrete Lean types and
predicates, record missing analytic and gauge-theory APIs without abstracting them away, and check
all alternate encodings by kernel-elaborated transports. The separate dossiers for `THM-M-0585`
and `THM-M-0608` are discovery comparisons only and cannot satisfy this target's gates.

No theorem-specific repo-local Lean declaration was identified by the intake repository search.
The only nearby `Formalizations/Lean` match uses an explicitly non-evidentiary abstract package;
this negative local result is not a pinned-mathlib or external-project anchor audit.
