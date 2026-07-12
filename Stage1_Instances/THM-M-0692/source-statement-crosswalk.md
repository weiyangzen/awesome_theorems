# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `切割消去定理`, attributes it to
Gerhard Gentzen, dates it to 1934, and gives only `相继式演算中的切割消去` ("cut elimination in
sequent calculus"). Stage0 repeats that gloss while leaving definitions, assumptions, proof path,
axioms, and artifacts open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted`. None of these records supplies a formal calculus or proposition.

## Candidate source work

Gerhard Gentzen, *Untersuchungen uber das logische Schliessen. I and II*, *Mathematische
Zeitschrift* 39 (1935), 176-210 and 405-431, is the historical primary publication candidate for
the Hauptsatz. The inventory's 1934 date must not be treated as the publication date. No exact
section, theorem passage, calculus variant, assumptions, translation, or errata has been accepted
during intake, so this citation is a discovery locator rather than `H0` evidence.

A later statement/source audit must inspect an immutable scan or edition, preserve Gentzen's exact
`LK`/`LJ` boundary and rule presentation, record the theorem and page, reconcile terminology and
any translation, check corrections or errata, and obtain independent review.

## Crosswalk

| Repository/source phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "sequent calculus" | `LK`, `LJ`, or another specified calculus | formula, context, sequent, and derivation inductives | family identified; exact calculus open |
| "cut" | inference composing derivations through a cut formula | exact cut constructor/rule and side conditions | absent from source record |
| "elimination" | transform derivations or prove cut admissible | cut-free predicate plus preservation/existence theorem | theorem form open |
| first-order rules | quantifier inferences with eigenvariables | substitution, lifting, and freshness invariants | inclusion open |
| structural behavior | weakening, contraction, exchange | primitive rules or admissibility lemmas | convention open |
| `已验证` | untrusted inventory label | no proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
search found no theorem-specific cut-elimination declaration. `IntakeProbe.lean` checks only `List`,
`Multiset`, `WellFounded`, and `WellFounded.fix`, generic ingredients for possible syntax and
termination encodings. This negative name search and API probe are not the later immutable anchor
audit, and they receive no statement or proof credit.

