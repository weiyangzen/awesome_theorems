import Mathlib.ModelTheory.Satisfiability

/-!
Pinned-environment discovery probe for the THM-M-0644 intake.

The checked declarations align with the repository wording, but this file is not the statement
certificate: it does not serialize the elaborated expression, check alternate encodings or
mutations, audit provenance/axioms, or assign proof credit.
-/

#check FirstOrder.Language.Theory.IsSatisfiable
#check FirstOrder.Language.Theory.IsFinitelySatisfiable
#check FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable
