# Machine-checked audit

The exact provider module is imported by every Lean surface.  The three
transport declarations are theorem-only wrappers whose proof term is the
qualified frozen provider declaration.  The intended replay is a cold,
from-source Lean kernel check at `--trust=0`; no target-local axiom,
placeholder, unsafe declaration, or bodyless oracle is introduced.

The machine closure record binds the semantic-environment digest and records
an empty machine cut set for canonical-Master re-evaluation.
