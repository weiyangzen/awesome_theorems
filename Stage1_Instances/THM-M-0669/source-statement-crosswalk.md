# Source-statement crosswalk

## Repository source

`Docs/Stage0_Blueprint.md` gives the content "quantifier elimination for real closed fields". The
rev-5.6 manifest retains the title "Tarski quantifier elimination" and `\u5df2\u9a8c\u8bc1` only as
untrusted metadata. Neither record supplies definitions, a proof source, edition, theorem number,
page, assumptions, errata, or a formal declaration.

## Candidate primary sources

- Alfred Tarski, *A Decision Method for Elementary Algebra and Geometry*, second edition, RAND
  Corporation (1951), is a historical primary-source candidate for effective elimination and the
  decision method. The exact theorem/page, language, and relationship of this edition to the
  repository's formula-level claim have not yet been inspected.
- Alfred Tarski, "Sur les ensembles definissables de nombres reels I", *Fundamenta Mathematicae*
  17 (1931), is an earlier historical candidate concerning definable real sets. Its exact statement,
  pages, hypotheses, and role in the full theory-of-real-closed-fields formulation remain open.

These citations are discovery anchors, not `H0` evidence. A source audit must inspect an immutable
edition, distinguish the result over the real numbers from transfer to arbitrary real closed
fields, record exact theorem/page and definitions, check corrections/errata, and obtain independent
row-by-row review.

## Crosswalk

| Repository/source phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "real closed fields" | all models of the real-closed-field theory | concrete language, theory, structures, and link to `IsRealClosed` or an axiomatic equivalent | included; encoding open |
| "quantifier elimination" | every formula has a quantifier-free equivalent | formula syntax, quantifier-free predicate, witness formula | included; exact predicate open |
| "equivalent" | agreement for every model and valuation | semantic realization or theory-relative equivalence | included; semantic/syntactic choice open |
| same parameters/free variables | elimination does not change the external interface | one common free-variable type and checked relabeling discipline | included |
| Tarski decision method | effective corollary or stronger algorithmic presentation | computable transformation and correctness, if source-selected | excluded from root until source bridge is frozen |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, generic first-order
syntax and semantics, theory-relative formula equivalence, the ring language, and the algebraic
`IsRealClosed` class exist. `IntakeProbe.lean` checks these ingredients using the pinned Lean
executable. The scoped search located no theorem-specific real-closed-field quantifier-elimination
declaration. This negative result is only intake discovery, not the later immutable anchor audit.

The algebraic `IsRealClosed` class is not itself a first-order theory or a proof of quantifier
elimination. Before statement acceptance, the chosen source components must map to an elaborated
Lean proposition and the language/theory-to-typeclass relationship must be explicit and checked.
