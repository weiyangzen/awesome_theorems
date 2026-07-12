# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `不可描述基数`, attributes it only to
"many mathematicians", dates it to the twentieth century, and gives the statement
`不可描述基数的性质` ("properties of indescribable cardinals"). Stage0 repeats that metadata while
leaving the exact definition, assumptions, proof, equivalent formulations, axioms, and machine
artifact open. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`.

Thus the repository supplies no definition, theorem, ordered hypotheses, conclusion, edition,
theorem/page locator, errata record, or formal declaration. The neighboring entries on weakly
compact and Ramsey cardinals locate the subject but cannot select a statement.

## Candidate source work

An authoritative set-theory source must be selected at the later source audit. It must identify an
exact definition or theorem and record the edition, theorem/definition number and page, formula
hierarchy conventions, structure and parameter assumptions, proof boundary, and errata. A second
reviewer must verify the transcription. No monograph passage or historical attribution is accepted
at intake, so this dossier makes no `H0` claim.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "cardinal" | a cardinal `kappa`, usually with large-cardinal side conditions | `Cardinal`, ordinal/rank coding, exact side-condition predicates | nearby cardinal API probed; domain open |
| "indescribable" | reflection for a fixed `Pi^m_n` or `Sigma^m_n` formula class | typed syntax, complexity predicate, valuation, satisfaction, and rank restriction | all semantic choices open |
| `V_kappa` to `V_alpha` | cumulative-hierarchy structures and `alpha < kappa` | a checked hierarchy/model encoding and inclusion/parameter transports | no canonical encoding selected |
| "properties" | implication, equivalence, existence, ideal, or preservation result | one concrete proposition with ordered binders and hypotheses | absent from source record |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports cardinal regularity and model-theory syntax. It checks `Cardinal.IsInaccessible` and
generic first-order language/formula types. These are only possible ingredients. A bounded name
search found no mathlib declaration named for indescribability; that observation neither proves
absence nor replaces the later immutable anchor audit. In particular, the probe supplies no
cumulative-hierarchy semantics, higher-order complexity hierarchy, reflection predicate, exact
statement, or proof.
