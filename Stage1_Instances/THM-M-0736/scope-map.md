# Scope map

## Included topic boundary

- Finite propositional formulas or another source-specified language and its semantics.
- A source-specified propositional proof system, derivation relation, or polynomial-time verifier.
- A source-specified family of valid formulas or tautologies.
- A representation-sensitive proof-length or proof-size measure.
- One exact lower-bound conclusion with all uniformity and asymptotic quantifiers fixed.

## Ambiguities to resolve at statement freeze

The repository record does not select a proposition. At minimum, the source phase must decide:

1. the proof system and its rules, verifier, soundness, and completeness convention;
2. the syntax, semantics, and encoding of formulas and proofs;
3. the hard formula family and its parameterization;
4. whether the resource is symbols, lines, clauses, width, depth, or encoded bit length;
5. whether the claimed lower bound is polynomial, exponential, or another function, and whether it
   holds eventually, infinitely often, or for every parameter;
6. whether auxiliary variables, abbreviations, dag-like reuse, and padding are allowed.

Boundary cases remaining open include zero parameters, empty derivations, formulas outside the
system's range, unprovable inputs, several encodings of one proof, and lower bounds made vacuous by
the nonexistence of proofs.

## Explicit exclusions

- A generic definition or survey statement presented as though it were a theorem.
- A resolution, cutting-planes, polynomial-calculus, or bounded-depth-Frege result selected without
  a source crosswalk identifying it as this target.
- An unrestricted Frege claim, separately suggested by `THM-M-0737`, or an extended-Frege claim,
  separately represented by `THM-M-0738`.
- Circuit lower bounds, natural-proofs barriers, or algebraic complexity as substitutes.
- A cardinality fact about lists or finite sets substituted for a proof-complexity lower bound.
- The repository label `已验证` as human-proof or machine-proof evidence.

No canonical Lean target is frozen at intake because no proposition is present in the source
record.
