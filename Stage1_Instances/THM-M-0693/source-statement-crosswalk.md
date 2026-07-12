# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records `相继式演算`, Gerhard Gentzen, 1934, and only the gloss
`证明的形式系统` ("a formal system of proof"). `Docs/researches/formalization_classification.md`
adds the schematic sequent `Gamma |- Delta`, separation of structural and logical rules, and
examples of identity, cut, and left/right rules. These are secondary descriptive notes, not an
exact formal calculus or theorem statement. Stage0 leaves definitions, premises, proof path,
axioms, and machine artifacts open. The manifest preserves `已验证` only as untrusted metadata.

## Primary-source locators

Gentzen's paired papers *Untersuchungen ueber das logische Schliessen I* and *II*, published in
*Mathematische Zeitschrift* 39 (1935), are plausible historical locators for the calculi associated
with the repository's 1934 date. They are discovery candidates only. An exact immutable edition,
passage, calculus, notation translation, theorem/page, premise boundary, corrections/errata, and
independent review have not been accepted. No `H0` claim follows from this bibliography.

## Crosswalk

| Repository phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| `Gamma |- Delta` | ordered or unordered antecedent/succedent contexts | formula type plus list/multiset/set contexts and a sequent type | representation open |
| identity `A |- A` | initial sequent schema | derivation constructor with exact context conventions | descriptive example only |
| cut | composition through a cut formula | exact cut rule or admissibility proposition | rule shown; do not substitute `THM-M-0692` |
| left/right rules | connective- and quantifier-specific inference rules | inductive derivation constructors and eigenvariable conditions | rule inventory absent |
| "formal system of proof" | definition of a calculus, not itself a truth-valued theorem | an object-level calculus plus a concrete `Prop` metatheorem | no proposition supplied |
| `已验证` | inventory status | none | explicitly rejected as H/M evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe checks generic first-order language, bounded formula, theory, list, and membership APIs. A
bounded name search found no mathlib module presenting a theorem-specific sequent calculus. This is
encoding and negative discovery evidence only, not the later immutable anchor audit and not proof
credit.

Before `H0`, a proof-theory reviewer must approve the exact source passage, object logic, calculus,
rule side conditions, root proposition, assumptions, translation, and errata. Before statement
credit, those components must map row by row to one elaborated Lean expression with checked
transports and all required mutations.
