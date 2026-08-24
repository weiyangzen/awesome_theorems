# Machine-checked audit

The claim-owned Lean surface has three standalone modules.  Each imports
`Mathlib`, contains the exact frozen provider module/declaration only as a
provenance comment, and declares theorem/lemma-style transports only.  A
source scan finds no `sorry`, `admit`, `axiom`, `opaque`, unsafe declaration,
definition, abbreviation, notation, syntax, macro, instance, coercion, or
namespace alias.

The proposed closure is `M0-L`: `statement`, `proof`, and `audit_root` all have
the local root `claim ↔ claim`, with both directions implemented by the
identity proof.  The observed claim-owned axiom set is empty and the foundation
profile for `S5-CLM-00003514@1` allows no transitive axioms or bodyless
declarations.

This worker did not run Lean, Lake, or Elan because the immutable claim forbids
it.  Consequently every elaborated-expression and declaration-census digest is
a proposed binding, not Master acceptance.  The canonical Master must compile
all three modules at trust zero, substitute the actual frozen source root at
the semantic boundary, recompute the transitive environment, and reject the
package if that independent replay differs.
