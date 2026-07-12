# Scope map

## Preserved theorem family

The intake preserves the catalog's finite-simple-group classification family without manufacturing
a formal taxonomy. A later statement phase may freeze a root only from an approved immutable source
that supplies the exact list and conventions. Prospective mathematical components include:

- a finite, nontrivial group whose only normal subgroups are trivial and total;
- classification up to group isomorphism;
- cyclic groups of prime order;
- alternating groups in the source-selected degree range;
- the source-selected parameterized families of finite simple groups of Lie type, with every
  parameter restriction, quotient, twist, exceptional case, and low-rank coincidence resolved; and
- the exact 26 sporadic isomorphism types.

No component list above is asserted, counted, or credited as the canonical proposition at intake.

## Decisions required at statement freeze

1. Pin an authoritative statement and complete proof-source boundary, including edition, theorem or
   chapter/page locator, definitions incorporated by reference, corrections, and independent review.
2. Fix the carrier universe, `Group` and finiteness interfaces, nontriviality convention, normal
   subgroup definition, and exact meaning of simple.
3. Fix classification up to `MulEquiv` or another explicitly checked equivalence relation.
4. Decide whether cyclic prime-order groups are included and how the abelian branch relates to the
   phrase "18 infinite families."
5. Define each alternating and Lie-type family as actual group objects, not uninterpreted labels;
   freeze parameter fields, admissibility predicates, central quotients, twisted constructions,
   simplicity exclusions, and exceptional isomorphisms.
6. Enumerate all 26 sporadic groups by exact formal representatives and prove or cite checked
   identity, simplicity, finiteness, and pairwise-nonisomorphism facts required by the conclusion.
7. Resolve the convention behind the number 18 and the treatment of the Tits group, which can be
   described as a Lie-type exception or alongside the sporadic cases without being sporadic.
8. Decide whether the theorem asserts exhaustiveness only, existence plus uniqueness of a family and
   parameter, pairwise disjointness, or a stronger canonical classification.
9. Freeze ordered binders, typeclass dependencies, hypotheses, conclusion, logical principles, and
   all quotient and finite-field foundations.

## Boundary cases

Source review must explicitly handle the trivial group; groups with prime cardinality; abelian
simple groups; alternating groups in small degrees; Lie-type parameters whose standard presentation
is not simple; central quotients; accidental isomorphisms within and between families; duplicate
parameter presentations; the Tits group; and the difference between "is one of" and a unique
classification datum.

## Substitution exclusions

- The common four-class summary (cyclic, alternating, Lie type, sporadic) cannot replace the literal
  18-family/26-sporadic claim without a checked source bridge.
- Classification of finite simple abelian groups, simplicity of `A5`, an odd-order theorem, a
  recognition theorem, or one Lie-type or sporadic family is not the full classification.
- A predicate such as `IsClassified`, a structure field containing the desired disjunction, or an
  assumed enumeration is only an interface or restatement, not proof.
- Cardinality lists, character tables, computer databases, and name tables do not by themselves
  establish group construction, simplicity, exhaustiveness, or uniqueness.
- Generic finite-group, quotient, matrix-group, finite-field, or simple-group APIs alone provide no
  theorem credit. The catalog label `部分验证` provides no H or M credit.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery probe checks `IsSimpleGroup`, transport
under group equivalence, the exact finite abelian-simple cardinality classification, and `A5`
simplicity. The alternating-group module still records general alternating-group simplicity as a
TODO. A bounded exact-topic search found no terminal CFSG, sporadic-group, or 18-family declaration.
This is intake discovery, not the downstream immutable anchor audit or a global absence claim.
