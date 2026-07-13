# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md:6665-6670` supplies the title `二项式定理`, the attribution
`众多数学家`, the time `古代`, and the phrase `(a+b)^n的展开公式`. Git blame attributes all six
uncited catalog lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no bibliography, edition,
theorem/page, quantified domain, commutativity premise, definition of the coefficient, exact sum,
proof passage, correction history, errata, or reviewer.

`Docs/Stage0_Blueprint.md:24850-24875` repeats the phrase while explicitly leaving exact definitions
and premises, proof history, equivalent statements, axiom use, machine status, and artifact links
open. The rev-5.6 manifest retains `已验证` only as `source_status_untrusted` and resets the target to
`L0 / rework_required`. These records locate the intended theorem family but cannot establish
`H0`.

No primary historical edition or independently reviewed modern authoritative statement was
admitted during intake. The attribution and ancient date are therefore retained exactly as
untrusted catalog metadata, not asserted as audited genealogy. A future source audit must select a
pinpoint statement and proof, map every incorporated definition and assumption, inspect translations,
corrections, and errata, and obtain independent review.

## Clause crosswalk

| Catalog component | Conventional interpretation | Pinned Lean surface | Intake status |
|---|---|---|---|
| `a`, `b` | two elements of one coefficient algebra | `a b : R` | domain and algebraic structure absent; candidate only |
| `+` and multiplication | semiring operations | `[CommSemiring R]`, or `[Semiring R]` with `Commute a b` | proposition-changing premise not source-selected |
| `n` | nonnegative integer exponent | `n : Nat` | conventional candidate; catalog gives no explicit quantifier or domain |
| left side | natural power of the sum | `(a + b) ^ n` | direct notation match |
| expansion index | each `m` from zero through `n` | `m in Finset.range (n + 1)` | endpoints absent from catalog; candidate only |
| coefficient | binomial coefficient `n choose m` | `Nat.choose n m`, cast to `R` or acting by `nsmul` | coefficient convention and cast absent |
| monomial | one power of each summand | `a ^ m * b ^ (n - m)` | exponent order and subtraction convention absent |
| equality | expansion equals original power | Lean equality in `R` | equality direction and alternate forms not frozen |
| `已验证` | untrusted inventory label | no expression, source review, or receipt | rejected as evidence |

## Pinned Lean leads

At manifest-pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Data.Nat.Choose.Sum` contains:

```text
add_pow [CommSemiring R] (a b : R) (n : Nat) :
  (a + b) ^ n =
    sum m in Finset.range (n + 1), a ^ m * b ^ (n - m) * (n.choose m : R)

Commute.add_pow [Semiring R] (h : Commute a b) (n : Nat) :
  (a + b) ^ n =
    sum m in Finset.range (n + 1), a ^ m * b ^ (n - m) * (n.choose m : R)

Commute.add_pow' [Semiring R] (h : Commute a b) (n : Nat) :
  (a + b) ^ n =
    sum m in Finset.antidiagonal n, n.choose m.1 • (a ^ m.1 * b ^ m.2)
```

The module documentation explicitly calls these binomial-theorem variants. Its `Commute.add_pow`
body proceeds by induction on `n`, separates the first, last, and middle summands, applies Pascal's
recurrence, and recombines the sums. That architecture is a downstream proof-tree lead, not an
intake obligation registry.

`IntakeProbe.lean` imports the proof-bearing module, checks the named declarations, compares the
commutative wrapper with the explicit-commutation form, reports candidate axioms, and checks the
zero and quadratic boundaries. The successful probe establishes usable exact-topic interfaces, so
the provisional machine level is `M3`; it does not freeze the root, audit the terminal body or
transitive dependency closure, or confer `M0-W` proof credit.

## First downstream gate

Before statement acceptance, an independent source review must approve the coefficient domain,
commutativity contract, coefficient and sum conventions, exponent order, binder order, equality,
and every boundary row. The statement phase must then elaborate and fingerprint one exact
expression using declared minimal imports, check all credited alternate encodings, and reject the
required removed-hypothesis, changed-domain, changed-scope, and boundary mutations.
