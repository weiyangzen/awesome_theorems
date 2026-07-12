# Source-statement crosswalk

## Repository record and candidate sources

The repository inventory gives the label "Seiberg-Witten theory", the authors Nathan Seiberg and
Edward Witten, the year 1994, and the gloss "new invariants of four-manifolds". It gives no exact
theorem, hypotheses, or definition, and its `已验证` field is explicitly untrusted under rev-5.6.

A primary discovery candidate is Edward Witten, *Monopoles and four-manifolds*, Mathematical
Research Letters 1 (1994), 769-796, DOI `10.4310/MRL.1994.v1.n6.a13`. It introduces the monopole
invariants and states their properties and applications, but this intake has not selected and
independently audited an exact numbered/displayed result, all conventions, or corrections.

The physical genealogy includes Nathan Seiberg and Edward Witten's 1994 electric-magnetic duality
papers. Those sources motivate the equations but must not be substituted for a rigorous
four-manifold invariance theorem merely because the repository attributes the theory to both
authors. Rigorous mathematical treatments proving analytic foundations are also required by a
future human-source audit. All sources listed here are discovery anchors, not `H0` evidence.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "four-manifold" | smooth closed oriented `X`, plus source side conditions | smooth oriented 4-manifold and compactness/boundary interfaces | family included; exact domain open |
| "Seiberg-Witten" | spin-c structure, connection, spinors, and monopole equations | spin-c bundles, connection/curvature, Dirac operator, gauge action | included; conventions and APIs open |
| moduli space | gauge classes of solutions with regularity and compactness | quotient/configuration space and finite-dimensional oriented moduli object | necessary proof boundary; exact model open |
| "new invariant" | signed count or pairing associated with each spin-c structure | integer-valued or source-specified invariant | intended conclusion; dimension and codomain open |
| metric independence | cobordism across generic choices | equality/chamber-dependent transformation under changed auxiliary data | exact `b2+` and chamber hypotheses open |
| diffeomorphism invariance | compatibility with oriented diffeomorphisms and spin-c pullback | transport theorem for the invariant | intended property; exact formulation open |
| 1994 / Seiberg and Witten | historical locator and theory genealogy | no machine-proof credit | metadata only |

## Human and machine boundary

The repository-wide Lean search found only
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_252.lean`, where Seiberg-Witten data is explicitly
a proposition-valued missing package in a four-manifold-classification audit. That file states it
is not theorem evidence for Seiberg-Witten theory. The pinned-mathlib name search found no
theorem-specific declaration. These narrow negative searches are intake evidence, not the later
immutable external-anchor audit and not proof of global nonexistence.

Before `H0`, an independent reviewer must select an immutable primary theorem and rigorous proof
source, verify pinpoint locators, definitions, assumptions, orientation and chamber conventions,
and errata, and approve the row-by-row mapping. Before statement credit, the approved claim must be
mapped to an elaborated Lean expression without assuming compactness, transversality, orientation,
or invariance as opaque input fields.
