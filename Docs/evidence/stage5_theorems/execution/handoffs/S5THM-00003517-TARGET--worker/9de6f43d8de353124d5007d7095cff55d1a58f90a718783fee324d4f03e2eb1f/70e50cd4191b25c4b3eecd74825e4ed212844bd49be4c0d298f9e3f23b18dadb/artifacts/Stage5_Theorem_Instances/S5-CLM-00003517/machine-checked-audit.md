# Machine-checked audit

The proposed root is the claim-owned epsilon-light subset statement equivalent
to the frozen Formal Conjectures declaration.  Its proof DAG has no remaining
machine cut and records trust level zero.  The frozen provider proof body is
not a dependency; only its source statement bytes and identity are anchors.

The local Lean surface contains theorem and lemma declarations only.  It adds
no definitions, abbreviations, notation, syntax, macros, coercions, aliases,
instances, opaque declarations, unsafe declarations, or claim-specific
axioms.  The exact provider module and qualified declaration appear in each
file solely in a provenance comment, while each file actively imports
`Mathlib` as required by the claim.

The worker did not invoke Lean, Lake, or Elan.  `machine-closure.json` is a
provisional replay record for the controller.  The canonical Master must
recompute declaration types, bodies, dependencies, axiom sets, root expression,
and transitive non-foundation environment at trust zero from a cold offline
build before it can accept this package.
