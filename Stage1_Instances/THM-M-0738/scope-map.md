# Scope map

## Included discovery boundary

- A source-specified propositional language and Frege calculus.
- The precise extension mechanism, including freshness and definitional constraints on extension
  variables.
- Proof objects, line validity, end formula, semantic validity, and the selected proof-size measure.
- A concrete soundness, completeness, simulation, polynomial-equivalence, proof-length, or
  automatability statement only after an immutable source selects it.

These are candidate surfaces for statement discovery, not components of a frozen root theorem.

## Ambiguities blocking statement freeze

1. **Calculus:** Hilbert, sequent, and other Frege presentations differ syntactically and require
   an explicit translation before complexity claims can be compared.
2. **Extension mechanism:** extension axioms, an extension rule, and circuit abbreviations require
   exact freshness, ordering, and acyclicity conventions.
3. **Proof representation and size:** sequences versus DAGs and symbol count versus formula/circuit
   size change polynomial simulation statements.
4. **Claim family:** soundness, implicational completeness, p-simulation of Frege, robustness under
   presentation changes, automatability, and proof lower bounds are different propositions.
5. **Historical/source identity:** the title, Cook attribution, and year do not provide an edition,
   theorem number, page, or exact result, and cannot by themselves establish a source crosswalk.

The statement phase must independently inspect an immutable primary source and freeze ordered
binders, every syntactic predicate, semantic valuation, complexity convention, hypotheses,
conclusion, and small/degenerate cases before elaboration or mutation testing.

## Explicit exclusions

- Replacing Extended Frege with ordinary Frege, resolution, cutting planes, or another proof system.
- Substituting basic soundness because it is easier when the intended item might concern simulation
  or proof complexity.
- Claiming a general superpolynomial lower bound, or its negation, from the phrase "properties".
- Encoding the desired conclusion as a field or hypothesis and projecting it tautologically.
- Treating the source label `已验证`, the author/year metadata, or an API probe as proof evidence.

No canonical Lean target is frozen at intake.

