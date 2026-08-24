# Machine-checked audit

The target package records an M0-P closure with trust level zero, an empty
machine cut set, no placeholders, and a cold-from-source replay requirement.
`Statement.lean`, `Proof.lean`, and `Audit.lean` each carry the frozen numeric
provider import and qualified declaration in a provenance comment and use
`import Mathlib` for the executable surface.  The canonical Master must replay
the integrated bytes independently.
