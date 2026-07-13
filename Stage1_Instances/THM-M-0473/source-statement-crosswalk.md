# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md:3476-3481` supplies the title `裴蜀定理`, attributes it to
Etienne Bezout (ASCII rendering), dates it to 1779, and states only `ax+by=gcd(a,b)有整数解`.
Git blame attributes
all six uncited catalog lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, edition,
theorem/page, exact quantifiers, domain declaration, gcd convention, proof, errata, or formal
artifact.

`Docs/Stage0_Blueprint.md:12974-12999` repeats the gloss while leaving exact definitions and
premises, proof history, dependencies, equivalent forms, axioms, and machine artifacts open. The
rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and resets the target to
`L0 / rework_required`. These repository records identify the theorem family but cannot establish
`H0`.

No primary edition or authoritative modern theorem/page was admitted during intake. The source
phase must preserve and hash an immutable passage, record all incorporated definitions and
assumptions, check corrections and errata, crosswalk each statement component, and obtain an
independent review. The historical attribution and date also remain catalog metadata until then.

## Component crosswalk

| Catalog component | Mathematical decision | Prospective Lean component | Intake status |
|---|---|---|---|
| `a`, `b` | signed integer inputs or natural inputs | `a b : Int` or `a b : Nat` | integer family selected; exact encoding open |
| `gcd(a,b)` | nonnegative gcd and its ambient type | `Int.gcd a b : Nat`, cast to `Int` | sign/cast convention identified |
| `x`, `y` | integer coefficient witnesses | `Exists fun x : Int => Exists fun y : Int => ...` | integer witnesses required |
| `ax+by` | integer multiplication and addition | `a * x + b * y` | orientation/binder order open |
| "has solutions" | universal in inputs, existential in coefficients | outer `forall a b`, inner `exists x y` | quantifier family identified |
| `已验证` | untrusted inventory label | no proof object | explicitly rejected as evidence |

## Pinned Lean discovery anchors

At manifest-pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, module `Mathlib.Data.Int.GCD` describes and contains:

```text
Nat.gcd_eq_gcd_ab (a b : Nat) :
  (Nat.gcd a b : Int) = (a : Int) * Nat.gcdA a b + (b : Int) * Nat.gcdB a b

Int.gcd_eq_gcd_ab (a b : Int) :
  (Int.gcd a b : Int) = a * Int.gcdA a b + b * Int.gcdB a b
```

The same file defines the extended-Euclidean coefficient functions `gcdA` and `gcdB`. Its source
comments explicitly call both declarations Bezout's lemma. `IntakeProbe.lean` imports only this
module, checks the declarations, prints their immediate axiom reports, and kernel-checks
existential natural-input and integer-input wrappers plus the `(0,0)` case. Both inspected
declarations report `propext` and `Quot.sound` in the current environment.

This is real pinned API elaboration evidence for an `M3` intake candidate, not an `M0` claim. The
probe does not freeze the canonical target, prove a checked source transport, audit all transitive
dependencies or the terminal body, precommit the discovery inventory, or perform an independent
anchor audit. Those tasks remain downstream and open.

## Fidelity boundary

The catalog's displayed equation strongly disambiguates elementary Bezout identity from the
algebraic-geometry namesake, but it omits proposition-changing domain and convention choices. The
intake therefore records a recognizable family and direct formal candidates without pretending
that a pinpoint human source or exact Lean proposition has already been accepted.
