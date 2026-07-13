# THM-M-0093 rev-5.6 intake

`THM-M-0093` is the representation-theory catalog item named the highest-weight theorem. The
repository attributes it to Elie Cartan in 1913 and supplies the gloss "irreducible representations
of semisimple Lie algebras are classified by highest weight." The attribution and the `verified`
label are untrusted inventory metadata under rev-5.6.

## Intake result

This directory is a fail-closed `planned` dossier. The gloss identifies the classical
highest-weight classification family, but it is not an exact proposition. It does not say that the
Lie algebra and its representations are finite-dimensional, choose a scalar field and Cartan or
Borel data, define dominant integral weights, or state whether classification means existence,
uniqueness, a bijection on isomorphism classes, or all of these. Those clauses cannot be supplied
silently from memory.

Pavel Etingof's author-issued MIT course notes were inspected as a modern source lead. In the
complex finite-dimensional semisimple setting, Proposition 25.5 makes every finite-dimensional
irreducible module highest-weight; Proposition 25.12 and Corollary 25.13 give the unique simple
quotient and classification of irreducible highest-weight modules; and Theorem 25.17 identifies
the finite-dimensional parameters as dominant integral weights. This disambiguates a standard
root, but the catalog does not cite those notes and no complete definition/assumption/proof-node,
correction, historical-attribution, or independent review has been admitted. It supports `H1`,
not `H0`.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned Lie-module, generalized-weight-space, Cartan, root
system, semisimplicity, and enveloping-algebra APIs. A bounded exact-topic search found no
highest-weight representation or classification declaration in repo-local Lean or pinned mathlib.
The affine predicates in legacy `S1_M_053.lean` concern another theorem and are not a substitute.

The canonical mathematical statement and Lean expression therefore remain null. The provisional
vector is `[H1, M4, R4]`: a complete modern proof lead is known but exact source fidelity is open;
no usable exact formal artifact is credited; and no source-faithful reconstruction can attach to an
unfrozen root. All six downstream tasks remain open. No accepted execution state, audit completion,
theorem completion, or master acceptance is claimed.
