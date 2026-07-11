# Source-statement crosswalk

## Candidate primary sources

- David Hilbert, "Mathematische Probleme" (1900), Problem 21, is the historical formulation
  candidate. The authoritative edition/translation, exact pages, and wording remain to be checked.
- Josip Plemelj's early twentieth-century work on Riemann functions is the historical positive
  solution candidate. The exact publication, theorem location, hypotheses, and the gap/restriction
  relevant to the modern formulation remain to be inspected.
- A. A. Bolibrukh's late twentieth-century counterexample work is the primary correction candidate
  for the unrestricted formulation. Exact bibliographic metadata, statement, and hypotheses remain
  open and must be established before freezing a negated or restricted theorem.

These are discovery anchors only, not `H0` evidence. Secondary summaries are insufficient to choose
between the connection-on-a-bundle, trivial-bundle Fuchsian-system, irreducible, and unrestricted variants.

## Crosswalk

| Repository/source phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Riemann-Hilbert problem" | prescribed monodromy realization | representation and monodromy of a connection | family identified; variant open |
| "linear differential equation" | system/flat meromorphic connection | complex vector bundle, connection, horizontal transport | model open |
| "given singular points" | punctured projective line | finite set and complement in `ℂP¹` | included; infinity convention open |
| "regular singular" / Fuchsian | controlled local pole behavior | local analytic regularity predicate | included; equivalence open |
| unrestricted existence | realization on a trivial bundle | exact existential target | unsafe until counterexample boundary is sourced |
| restricted positive result | e.g. irreducible data or nontrivial bundle | explicit hypotheses and conclusion | candidate only |

## Existing repository boundary

No target-specific Lean artifact was present at intake. The general mathlib analysis, Hilbert-space,
and differential-equation APIs named by the legacy blueprint do not identify an exact declaration
for this problem and receive no statement or proof credit.

Before `H0`, an independent reviewer must verify stable primary editions, translations, exact
theorem/counterexample locations, definitions, every hypothesis, and errata, then approve the
source-to-Lean mapping. Before statement acceptance, the selected proposition must explicitly say
whether it is a positive restricted theorem or a counterexample to unrestricted existence.
