# Scope map

## Preserved catalog scope

The intake preserves exactly the named 1960 Bose-Shrikhande-Parker family and the repository gloss
"negation of Euler's conjecture." It does not silently promote a familiar modern formulation to
the canonical root. The inspected primary source narrows the family but exposes several
proposition-changing choices that the catalog does not resolve.

## Candidate roots, none credited

The statement phase must select one exact root or an explicitly structured package from an
admitted source. Current candidates include:

- the literal negation of Euler's nonexistence conjecture, satisfied by one explicitly scoped
  counterexample;
- existence of a pair of orthogonal Latin squares for every order `v = 4t + 2 > 6`;
- the primary paper's Theorem 10, existence of at least two orthogonal Latin squares of every order
  `v > 6`; or
- the paper's final classification that among positive `v > 2`, a pair exists exactly when
  `v != 6`, with separate evidence for the order-six nonexistence result; or
- an extension to all positive orders, which additionally requires source and convention decisions
  for orders one and two.

These statements are related but not interchangeable. Their quantifiers, proof obligations, small
cases, and source boundaries differ.

## Decisions required at statement freeze

1. Identify the exact historical Euler proposition and whether its order variable ranges over
   positive naturals, orders congruent to 2 modulo 4, or another source-defined domain.
2. Decide whether "negation" means `Not` of a universal nonexistence statement, one counterexample,
   a universal existence family, or a complete iff classification.
3. Freeze a Latin square representation: a labelled `Fin v x Fin v` matrix, three finite carriers,
   a quasigroup table, or another source-faithful encoding, with checked transports.
4. Freeze the Latin predicate and orthogonality predicate, including whether every ordered pair of
   symbols occurs exactly once and whether the two symbol alphabets are identified.
5. Freeze whether "at least two" means one ordered pair, two distinct squares in a family, or a
   lower bound on a source-defined maximum `N(v)`, and check their equivalence under the chosen
   representation.
6. Resolve strict versus non-strict bounds, the `v = 4t + 2` parameterization, natural-number
   subtraction/modulo conventions, and all small orders.
7. Fix the exact theorem/page, incorporated definitions and lemmas, proof and computation
   boundaries, corrections, errata, logic strength, and independent source review.

## Degenerate and boundary cases

No case is excluded at intake. Source review must explicitly decide order zero; orders one and two,
which the paper's Eulerian definition excludes and which depend on pair-versus-distinct-family
semantics; the special order six; orders three through six relative to the `v > 6` root; empty carriers;
whether row, column, and symbol carriers must have identical cardinality; vacuous uniqueness at
small orders; equality or distinctness of the two squares; and whether swapping the pair changes
the witness. A classification root must also supply source-faithful proofs of both existence and
nonexistence directions at every exceptional boundary.

## Explicit exclusions

- `THM-M-0902` is a separate repository target for Euler's conjecture; no status or evidence is
  inherited in either direction.
- An order-10 array or finite checked table may close only a selected counterexample root. It cannot
  prove a uniform order family or a complete classification.
- Existence of a single ordinary Latin square is not existence of two orthogonal Latin squares.
- A record that assumes row/column Latin properties or orthogonality as fields is a representation,
  not an existence proof.
- An orthogonal array, pairwise balanced design, BIB design, or group-divisible design requires a
  checked, source-mapped construction or transport; its name alone does not establish the root.
- The catalog's `已验证` label, the source title, DOI, API probe, successful elaboration of generic
  interfaces, and bounded search results provide no kernel-proof credit.

## Formal boundary

A possible future array substrate is `Matrix (Fin v) (Fin v) (Fin v)`, with row and column
bijectivity for each square and bijectivity of the superposition map from cell coordinates to
symbol pairs. That substrate is not canonical: it fixes labelled identical carriers, an order-zero
convention, and one definition of orthogonality. Exact imports, definitions, expression and
environment fingerprints, alternate-encoding witnesses, and mutation tests belong to the
dependent statement phase.
