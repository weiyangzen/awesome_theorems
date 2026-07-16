# Source-statement crosswalk

This file is the statement contract's selected crosswalk role. The intake selected the classical
unique-harmonic-representative claim below, but the exact primary-source edition/page and an
independent fidelity review remain open. The repository's terse source phrase, "harmonic forms and
cohomology," is not itself H0 evidence.

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Unique harmonic representative of each real de Rham class on a compact oriented Riemannian manifold | W. V. D. Hodge, *The Theory and Applications of Harmonic Integrals*, Cambridge University Press (1941), the classical harmonic-integral theorem | No concrete root declaration identified | Primary monograph identified, but edition/page/theorem wording and errata have not been independently pinned: `H1` |
| Harmonic forms map isomorphically to de Rham cohomology | F. W. Warner, *Foundations of Differentiable Manifolds and Lie Groups*, GTM 94, Springer (1983), Chapter 6 treatment of harmonic forms and de Rham cohomology | Future concrete manifold/de Rham wrapper | Secondary theorem-level pinpoint and assumptions audit remain open |
| Closed forms modulo exact forms | Standard definition of de Rham cohomology | `ClosedFormsQuotientModel.DeRhamCohomology` in `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_109.lean` | Abstract quotient shape only; its relations are supplied as fields and it is not mathlib's manifold de Rham object |
| A harmonic form yields a cohomology class | Consequence of harmonic forms being closed | `ClosedFormsQuotientModel.harmonic_has_deRham_class` | Checked legacy API-shape fact, but closedness is a structure field; it neither establishes existence nor uniqueness |
| Hodge star, codifferential, Laplacian, and analytic inputs | Classical Hodge-theory construction | `HodgeAPISplit` | Interface only: elliptic regularity and finite dimensionality are propositions stored as data, not proved |
| Existence and uniqueness root | Harmonic-representative theorem | Fields of `HodgeTheoryDatum` | Not an eligible theorem candidate: the desired facts are assumptions inside an abstract package |

The source phrase in the generated blueprint, "harmonic forms and cohomology," is underdetermined.
This intake selects the standard real de Rham harmonic-representative theorem and explicitly fixes
compactness, orientation, a Riemannian metric, and no boundary. The statement phase must confirm
whether connectedness is unnecessary, select concrete mathlib-compatible manifold and form models,
and check the equivalence between unique representatives and the harmonic-to-cohomology
isomorphism. It must not substitute the legacy `Nonempty` wrapper.

No `H0` or machine-closure claim is made. Source audit must pin an edition and exact theorem/pages,
map every analytic and geometric assumption, search corrections/errata, and obtain independent
review before source fidelity can close.

## Exact premise and boundary map

| Selected claim component | Intended Lean binder or hypothesis | Current pinned boundary |
|---|---|---|
| smooth finite-dimensional real manifold | model space, `ModelWithCorners`, charted space, `IsManifold` | adjacent manifold vocabulary exists |
| smooth Riemannian metric | Riemannian tangent bundle data and `IsRiemannianManifold` | adjacent Riemannian vocabulary exists |
| compact, oriented, without boundary | `CompactSpace`, orientation data, boundaryless model/manifold condition | compactness and boundaryless substrate exist; the exact orientation/form integration is unfrozen |
| real smooth p-forms | bundled smooth alternating covector fields on the manifold | missing; pinned `DifferentialForm.Basic` explicitly says manifold forms are not defined yet |
| real de Rham cohomology | closed smooth p-forms modulo exact forms | missing |
| harmonic representative | kernel of the Hodge Laplacian | Hodge star, codifferential, Laplacian, and harmonic-form predicate are missing |
| representative of class c | harmonic-form class map into de Rham cohomology | missing |
| unique existence | `ExistsUnique` over the fiber of that class map | cannot be typed until the preceding objects exist |

The exact canonical Lean declaration, elaborated expression fingerprint, checked transport to the
harmonic-to-cohomology isomorphism, and removed-hypothesis/changed-domain/changed-scope/boundary
mutations therefore remain blocked. The elaborating `Statement.lean` module is an interface probe
only and must not be read as the target theorem.
