# Machine-checked audit — S5-CLM-00003517

Machine closure is recorded at M0-P with trust zero and an empty machine cut
set.  The root is the task-local `audited_root` theorem, and the source
environment is content-addressed to the frozen Formal Conjectures provider.

The three Lean files are independently elaborated with the exact provider
module import.  The source theorem is explicitly marked as sorry-backed in the
intake record; the target package does not add that axiom or any claim-specific
oracle.  The Master is required to recompute the transitive declaration body,
type, dependency, and axiom census before integration.

Semantic-substitution mutations considered: replacing the provider import,
renaming the qualified source declaration, introducing a local `IsEpsilonLight`
definition, and adding notation for source identifiers.  Each is rejected by
the frozen validator's exact-import, qualified-reference, and shadow checks.
