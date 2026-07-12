# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` identifies Kurt Goedel, gives the year 1929, and glosses the
claim as `逻辑有效式可证` ("logically valid formulas are provable"). `Docs/Stage0_Blueprint.md`
repeats that metadata but supplies no edition, theorem number, page, formal calculus, equality or
domain convention, proof, or errata record. Its `已验证` label is untrusted under rev-5.6 and gives
neither human-source nor machine-proof credit.

## Candidate primary sources

- Kurt Goedel, *Ueber die Vollstaendigkeit des Logikkalkuels*, doctoral dissertation, University
  of Vienna (submitted 1929). This is the historical source suggested by the repository date. A
  stable facsimile, exact theorem/page, incorporated definitions, and corrections have not been
  inspected in this intake.
- Kurt Goedel, "Die Vollstaendigkeit der Axiome des logischen Funktionenkalkuels", *Monatshefte
  fuer Mathematik und Physik* **37** (1930), 349-360. This is the published primary candidate. The
  exact numbered statement, page, notation, equality convention, proof-system rules, and relation
  to the dissertation must be checked against an immutable copy before source acceptance.

The ASCII transliterations above avoid pretending that a particular digitization has been pinned.
They are discovery anchors only, not `H0` evidence. No errata search or independent review has yet
been performed.

## Metadata-to-statement crosswalk

| Repository component | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "completeness theorem" | semantic completeness of classical first-order predicate logic | one concrete object logic with syntax, semantics, and derivations | family identified; calculus open |
| "logically valid" | formula true under every interpretation/model | universal realization over nonempty structures and valuations | included; exact source convention open |
| "formula" | provisionally a closed formula/sentence | `Sentence` or universal closure of a formula | included; transport open |
| "provable" | finite formal derivation from logical axioms/rules and no premises | inductive derivation from empty theory/context | included; calculus open |
| Goedel, 1929 | dissertation result later published in 1930 | provenance only; no Lean implication | candidate source identified |
| `已验证` | Stage0 screening metadata | no proof or source-review object | rejected as evidence |

## Formal-library discovery boundary

The pinned mathlib source contains first-order syntax and semantic realization, including
`Mathlib/ModelTheory/Semantics.lean`. A repository search also found
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_298.lean`, which explicitly describes its local
derivation kernel and semantic bridge as **not** a completeness theorem. Neither observation is a
complete pinned-candidate audit, and neither closes this target.

Before `H0`, a source reviewer must pin a stable primary edition; record the exact statement and
page plus every incorporated definition and rule; enumerate language, equality, domain, formula,
validity, and provability conventions; inspect corrections and later editorial notes; and approve
a row-by-row mapping to the canonical Lean statement. Before statement acceptance, the formal
review must select a concrete calculus, elaborate the exact target, check transports for strong and
satisfiability forms, and record counter-mutations for each material scope choice.
