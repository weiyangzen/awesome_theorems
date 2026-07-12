# Scope map

## Provisional property family

- A fixed first-order language `L` and a fixed `L`-theory `T`.
- Every `L`-formula `phi`, including formulas with free variables, has a quantifier-free
  `L`-formula `psi` in the same free-variable context.
- Equivalence is uniform over every model of `T` and every assignment to the free variables.
- The statement includes sentences as the zero-free-variable case and treats equality according to
  the language/formula convention selected at statement freeze.

This is the usual meaning of "`T` eliminates quantifiers". It is a property of `T`; it is not true
for an arbitrary theory. Accordingly, these bullets delimit the intended concept but do not freeze
a theorem asserting that an unspecified theory has the property.

## Decisions required at statement freeze

The statement phase must first determine whether this inventory row is meant to define quantifier
elimination, prove a characterization of it, or prove it for a particular theory. It must then
freeze the theory and language; semantic versus syntactic equivalence; formula and free-variable
encoding; parameter and added-constant policy; equality convention; model nonemptiness; whether
the result is mere existence or an effective translation; binder order and universes; and behavior
for inconsistent or empty theories and nullary contexts.

If no source-intended proposition can be identified, the correct outcome is an `H5` target
classification or redirection, not invention of a convenient theory.

## Explicit exclusions

- Quantifier elimination for real closed fields (the adjacent Tarski target `THM-M-0669`) or for
  Presburger arithmetic (the adjacent Ackermann target `THM-M-0670`) as a substitute.
- Prenex normal form: moving all quantifiers to the front does not remove them.
- Skolemization, model completeness, completeness, decidability, or elimination of imaginaries as
  an unproved equivalent replacement.
- Equivalence in one chosen structure when the intended property is modulo all models of `T`.
- Choosing a different quantifier-free formula separately for each model or assignment.
- A hypothesis or structure field that directly assumes the desired equivalent formula and is then
  presented as a proof of quantifier elimination.
- The repository metadata value `已验证` as human-source or kernel evidence.
