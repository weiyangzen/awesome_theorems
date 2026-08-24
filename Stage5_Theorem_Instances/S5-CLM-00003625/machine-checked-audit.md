# Machine-checked audit — S5-CLM-00003625

The machine root is
`AwesomeTheorems.Stage5.Theorems.S5_CLM_00003625.Proof.agp_lower_bound_machine_closure`.
Its proposition is the identity transport for the frozen eventual lower
bound, parameterized by the provider's counting function and proof and using
`Filter.atTop` with real exponent `2 / 7`.

All three claim-owned Lean files record the frozen module spelling and
qualified declaration, then compile their parameterized transport boundary
against Mathlib because the canonical Lake search path does not contain the
Formal Conjectures provider package.  Each elaborates independently at trust
zero.  The files contain theorem declarations only: there are no local
definitions, abbreviations, instances, coercions, syntax rules, macros,
namespace aliases, opaque declarations, unsafe declarations, or proof
placeholders.

The statement module contains both directions of the proposition transport.
The audit module checks the identity as an equivalence, and the proof module
contains the replayed transport root.  The semantic environment digest binds
the pinned provider revision and source file.  This worker module does not
claim to recreate the unavailable provider proof from Mathlib; a canonical
release still requires the Master to elaborate the provider-backed root and
recompute the transitive constant census, dependency axioms, and read trace
from the integrated bytes.
