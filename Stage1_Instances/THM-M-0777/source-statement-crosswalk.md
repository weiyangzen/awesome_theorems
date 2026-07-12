# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives the title `哥德尔不完全性定理`, attributes it to Kurt
Godel in 1931, and states `包含算术的一致形式系统不完全` ("a consistent formal system containing
arithmetic is incomplete"). Stage0 repeats that sentence and leaves definitions, premises, proof,
dependencies, axioms, and machine artifacts open. The rev-5.6 manifest retains `已验证` only in the
field `source_status_untrusted`. None of these records supplies a theorem number, page, edition,
translation, errata record, or exact formal proposition.

## Candidate primary source

Kurt Godel, "Uber formal unentscheidbare Satze der Principia Mathematica und verwandter Systeme I",
*Monatshefte fur Mathematik und Physik* 38 (1931), 173-198, is the historical primary-source
candidate. The statement phase must inspect an immutable scan or edition, identify the exact theorem
and page, record its formal-system and consistency assumptions, check translation and errata, and
obtain independent review. This bibliographic locator is not yet `H0` evidence.

The later Rosser improvement is a candidate only if the repository gloss is intentionally resolved
to ordinary consistency. It must then be cited as a different source and theorem rather than being
attributed to the assumptions of Godel's original result.

## Crosswalk

| Repository phrase | Mathematical choice still required | Required Lean component | Intake status |
|---|---|---|---|
| "formal system" | effective theory, syntax, axioms, calculus | encoded formulas, proofs, theory and provability predicate | absent |
| "containing arithmetic" | extension or interpretation of a fixed arithmetic base | numerals, representability/arithmetization interface | absent |
| "consistent" | consistency, omega-consistency, 1-consistency, or soundness | a precisely scoped metatheoretic predicate | ambiguous |
| "incomplete" | a sentence for which neither it nor its negation is provable | closed sentence, negation, two unprovability claims | direction identified; exact form open |
| "1931 / Godel" | original theorem and its assumptions | source-node provenance, not a Lean term | candidate source identified |
| `已验证` | untrusted inventory label | no proposition and no proof credit | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Logic.Godel.GodelBetaFunction` defines `Nat.beta`, `Nat.unbeta`, and proves
`Nat.beta_unbeta_coe`. Its module documentation says the lemma is used for finite-sequence coding
and is "a step towards eventually including" the first incompleteness theorem. The bounded intake
probe checks these three declarations only. Repository and pinned-mathlib searches found no main
incompleteness declaration; that bounded negative result is not the later immutable anchor audit.
