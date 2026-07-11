# Source-statement crosswalk

## Available repository source

`Docs/researches/math_theorems.md` gives the title `更新过程`, attributes it only to "many
mathematicians" in the twentieth century, and supplies the content phrase `更新理论`. The generated
Stage0 record repeats this wording and adds no formula, theorem number, hypotheses, bibliography,
or conclusion. Its `已验证` label is untrusted metadata under rev-5.6.

## Discovery references

- William Feller, *An Introduction to Probability Theory and Its Applications*, Volume II,
  second edition, Wiley, 1971, Chapter XI, is a broad renewal-theory reference candidate.
- David R. Cox, *Renewal Theory*, Methuen, 1962, is a monograph candidate for the subject.

These references contain many inequivalent propositions. They are discovery anchors only: no
edition scan, exact theorem/page, assumptions, proof, or errata has been audited, so neither is `H0`
evidence and neither selects the repository's canonical statement.

## Crosswalk

| Repository element | Mathematical information fixed | Required Lean component | Intake result |
|---|---|---|---|
| `更新过程` | names renewal processes as a subject | one exact proposition over a defined process | object label only |
| `更新理论` | names a theory containing many results | exact quantifiers, hypotheses, and conclusion | not a statement |
| many mathematicians | broad historical provenance | named author/work and theorem/page | unresolved |
| twentieth century | broad date range | immutable source edition and errata record | insufficient |
| `已验证` | catalog status only | inspectable human proof or kernel receipt | no credit |
| stochastic-process category | likely probability setting | probability space, random variables, law, measurability | setting only |

## Candidate statement families, not substitutions

The elementary renewal theorem, a renewal equation, a construction theorem, and asymptotics for a
renewal function are materially different roots with different assumptions and boundary cases.
Smith's and Blackwell's results already have separate repository IDs. The next phase must recover a
source-authorized proposition rather than selecting any of these by familiarity.

## Evidence boundary

No exact human theorem and no Lean declaration is credited. Before statement closure, a reviewer
must identify the authoritative theorem-bearing source and verify its exact wording, edition,
theorem/page, definitions, assumptions, conclusion, and errata. Only after that may a source-to-Lean
map, canonical expression, mutation tests, or formal-candidate audit be produced.
