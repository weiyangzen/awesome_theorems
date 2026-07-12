# Scope map

## Preserved subject family

The intake preserves exactly the catalog family `existence and counting of Latin squares`. A later
statement phase may select a root only after an immutable source passage is mapped and independently
reviewed. Candidate components, none credited as the theorem at intake, include:

- finite row, column, and symbol carriers of a common source-specified order;
- an array in which every row and every column contains each symbol exactly once;
- an existence proposition for a source-specified range of orders and convention for order zero;
- a counting function on labelled or reduced squares, or on a source-specified equivalence class;
- an exact value, formula, recurrence, bound, divisibility result, or asymptotic result; and
- checked transports among array, quasigroup-table, and orthogonal-array representations.

## Decisions required at statement freeze

The statement phase must freeze all of the following from an approved source rather than a familiar
convention:

1. Whether the catalog intends one theorem, a conjunction, or a package of separately rooted
   existence and enumeration propositions.
2. The order domain and quantifier order, including whether `n = 0` is allowed and how orders one
   and two are treated.
3. Whether rows, columns, and symbols are all `Fin n`, arbitrary finite types of equal cardinality,
   or three distinct carriers connected by explicit equivalences.
4. Whether the Latin condition means pairwise distinct entries, row and column bijections, unique
   occurrence of every symbol, or a quasigroup law, and the checked equivalences among them.
5. Whether existence is unconditional at each order, concerns a partial-square completion or
   embedding problem, or imposes extra algebraic, symmetry, reducedness, or orthogonality data.
6. Whether counting is total labelled count, reduced count, an isomorphism or isotopy count, a main
   class count, or another quotient; and whether the conclusion is an exact value, general formula,
   recurrence, congruence, bound, or asymptotic statement.
7. The complete definitions, constants, thresholds, computation or certificate boundary, proof
   source, corrections, errata, ordered binders, hypotheses, conclusion, and logic strength.

## Degenerate and boundary cases

Source review must explicitly dispose of the empty carrier and `0 x 0` array; order one; whether a
row or column condition is vacuous; unequal or empty row, column, and symbol carriers; labelled
versus unlabelled carriers; reducedness at small order; empty quotient classes; and the precise
relationship between existence and positivity of a chosen counting function.

## Explicit exclusions

- `THM-M-0902` (Euler's conjecture about orthogonal Latin squares) and `THM-M-0903`
  (Bose-Shrikhande-Parker) are separate targets; their statements or evidence do not transfer.
- Completion or embedding of partial Latin squares, Latin rectangles, transversals, Sudoku,
  magic squares, and mutually orthogonal Latin squares cannot substitute for an ordinary-square
  root unless the approved source explicitly selects one.
- A cyclic group table proves one source-compatible existence statement only after the exact target
  and representation transport are frozen; it does not prove any counting claim.
- A finite table of known counts, numerical search, or unchecked enumerator cannot establish a
  uniform counting theorem or a source-unspecified quotient count.
- A matrix, binary operation, or record with the desired Latin property assumed as a field is a
  representation interface, not a proof of existence or enumeration.
- The catalog's untrusted `verified` label and the intake API probe supply no human-source or
  machine-proof credit.

## Formal boundary

The leading array candidate is a function type such as `Matrix (Fin n) (Fin n) (Fin n)` with
source-selected row and column bijectivity predicates. That shape is not canonical: it fixes one
carrier for three roles, labels every element, and permits an order-zero convention. Pinned mathlib
provides the underlying matrix, finite-cardinality, and equivalence APIs, but the bounded search did
not locate an exact Latin-square or quasigroup declaration. Exact imports, definitions, expression
fingerprints, representation transports, and mutation tests belong to the statement phase.
