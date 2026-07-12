# Scope map

## Included topic boundary

- A source-specified forcing preorder or partial order and its ordering convention.
- A source-specified definition of properness, including the ambient countable elementary models
  and the exact genericity requirement.
- One exact theorem selected by the source: a characterization, preservation result, iteration
  result, or result about a named forcing notion.
- Ground model, generic extension, name interpretation, cardinal, and countability infrastructure
  needed by that theorem.
- All hypotheses on models, cardinals, support, iteration length, separativity, and chain conditions.

## Ambiguities to resolve at statement freeze

The repository record does not decide among materially different propositions:

1. the definition or an equivalent characterization of a proper forcing notion;
2. the theorem that proper forcing preserves `ω₁` (or stationary subsets of `ω₁`);
3. a preservation theorem for countable-support iterations of proper forcing;
4. preservation of all cardinals, which the repository gloss appears to suggest but does not state
   with conditions and must not be silently identified with properness;
5. a theorem that a particular forcing construction is proper.

The statement phase must inspect an immutable source and freeze one proposition, ordered binders,
model/foundation conventions, hypotheses, conclusion, and boundary cases. In particular, it must
distinguish preservation of `ω₁` from preservation of arbitrary cardinals.

## Explicit exclusions

- Proper Forcing Axiom (`THM-M-0784`) or forcing axioms generally (`THM-M-0795`).
- The forcing theorem/fundamental theorem (`THM-M-0792`) and iteration technique
  (`THM-M-0793`) as substitutes, although a selected theorem may depend on them.
- Chain conditions, closure, distributivity, or cardinal preservation as definitions of properness.
- A tautology obtained by assuming the desired preservation conclusion as part of a custom
  `Proper` predicate.
- An order-theoretic ideal/cofinal theorem presented as a forcing-extension theorem without a
  checked semantic bridge.
- The inventory label `已验证` as evidence of a human proof or Lean closure.

No canonical Lean target is frozen at intake because the source record does not identify one.
