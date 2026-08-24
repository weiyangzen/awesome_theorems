# Machine-checked audit — S5-CLM-00003492

The candidate root is
`AwesomeTheorems.Stage5.S5_CLM_00003492.proof_maximalLength_le` at machine
level `M0-L`. Its local dependency cone consists of two lemmas:
`proof_exists_equal_first_two` and
`proof_not_two_increases_of_equal_first_two`. The audit transports are direct
identity proofs on the delta-expanded proposition.

Static worker checks establish the following before harvest:

- every Lean surface actively imports only `Mathlib` and records the exact
  frozen numeric provider import and qualified declaration in a provenance
  comment;
- there are no local definitions, abbreviations, notation, syntax, macros,
  coercions, aliases, instances, axioms, opaque declarations, unsafe
  declarations, placeholders, or provider proof-body references;
- all root-relevant local declarations have bodies and the proof DAG has no
  remaining machine cut;
- the only expected kernel foundations are the standard Mathlib foundations
  `propext`, `Classical.choice`, and `Quot.sound`; `sorryAx` is excluded;
- the source file, declaration, type, provider revision, and delta-expanded
  semantic surface are digest-bound in `statement-crosswalk.json`.

This document is not a claim that the worker invoked Lean. Per the immutable
claim, Master alone performs cold from-source offline compilation, trust-zero
axiom inspection, exact expression/environment recomputation, and semantic
substitution mutations after integration. The release receipt therefore keeps
`master_accepted` false.
