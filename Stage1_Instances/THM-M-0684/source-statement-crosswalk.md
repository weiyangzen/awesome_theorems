# Source-statement crosswalk

## Repository sources

`Docs/researches/math_theorems.md` has two nearby records. The proof-theory record says `系统不能证明
自身一致性` ("a system cannot prove its own consistency"); a later logic record says `一致形式系统
不能证明自身一致性` ("a consistent formal system cannot prove its own consistency"). Both name
Kurt Godel, date the result to 1931, and mark formalization status `已验证`. Neither supplies a
theory class, strength assumption, proof predicate, consistency formula, conclusion level, proof
source, edition, theorem/page, assumptions, errata, or formal artifact. Stage0 uses the shorter
record and explicitly leaves exact definitions and premises open. The manifest preserves the label
only as `source_status_untrusted`.

The two wordings are not enough to infer a proposition. Adding "consistent" avoids one obvious
counterexample but does not supply the usual effectiveness and arithmetic-strength conditions.

## Primary-source boundary

The 1931 attribution is a locator, not an accepted H0 citation. The source phase must inspect an
immutable edition/translation of the relevant Godel result or a precise modern theorem chosen as
the canonical claim. It must record theorem number and page, map every assumption and notation,
identify the proof boundary and known errata, and obtain independent review. This intake neither
invents those bibliographic fields nor treats historical attribution as a completed crosswalk.

## Crosswalk

| Repository phrase | Required mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "system" / "formal system" | exact theory and effective axiom/proof presentation | language, sentence, theory, derivation relation | absent; syntax APIs probed only |
| "consistent" | exact external assumption and internal `Con(T)` sentence | coded contradiction/proof predicate and consistency formula | absent |
| "prove" | arithmetized provability predicate for the selected calculus | syntax/proof encoding plus representability results | absent |
| "its own" | diagonal self-reference and link between coding and `T` | fixed-point/diagonalization and checked interpretation | absent |
| "cannot" | exact internal or metatheoretic non-derivability conclusion | a concrete `Prop` with all binders and hypotheses | absent |
| `已验证` | untrusted inventory label | no proposition or proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded probe
imports `Mathlib.ModelTheory.Encoding`. It checks the types of first-order sentences and theories,
and the syntax encoding. The module itself records incompleteness infrastructure as future
computability work; the probe is therefore only an environment and vocabulary check.
It does not define an arithmetized proof predicate, state the second incompleteness theorem, or
establish that no suitable external Lean 4 development exists. Formal candidate discovery belongs
to the later anchor-audit phase after the exact target is frozen.
