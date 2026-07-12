# Source-statement crosswalk

## Repository discovery sources

The currently available sources are repository records, not primary mathematical theorem sources:

1. `Docs/researches/math_theorems.md`, lines 11339-11344, names "Bäcklund transformation",
   attributes it to Albert Bäcklund, dates it to 1876, and describes it only as "a transformation
   of integrable systems". Its `已验证` label supplies no theorem text or evidence.
2. `Docs/Stage0_Blueprint.md`, beginning at line 42246, repeats the name, description, attribution,
   and date. It explicitly leaves the exact definitions, assumptions, proof, equivalent forms,
   axioms, and machine artifact to be filled in.
3. `Docs/Stage1_Targets_rev-5.6.json` identifies this record as `THM-M-1554`, execution rank 566,
   `L0 / rework_required`, and marks the historical source status untrusted.

These are real provenance for why the target is in the queue. They do not identify a paper,
edition, page, equation normalization, or theorem statement. In particular, the date and attribution
alone do not determine whether the intended object is Bäcklund's geometric surface transformation,
a later sine-Gordon formulation, or another integrable-system specialization.

## Claim crosswalk

| Source phrase or omission | Intake interpretation | Required exact-statement evidence | Status |
|---|---|---|---|
| "Bäcklund transformation" | a family of parameterized differential transformations | named equation and displayed transformation equations | open |
| "transformation of integrable systems" | transformation must preserve solutions or relate compatible systems | pinpoint theorem specifying source and target solution predicates | open |
| Albert Bäcklund / 1876 | historical attribution only | stable primary bibliography plus page/formula and convention audit | open |
| exact definitions and premises: missing | domain, regularity, parameter, signs, and scales are not recoverable | reviewed ordered premise map | open |
| equivalent formulation: missing | compatibility and preservation must not be conflated | checked implication/equivalence map | open |
| machine artifact: missing | no formal candidate receives proof credit | exact module, declaration, revision, and terminal-body audit | open |

## Source decision required

Before canonical Lean elaboration, the statement owner must select one immutable mathematical
source containing the exact Bäcklund equations and preservation/compatibility theorem, record its
edition or revision and pinpoint locations, map every assumption and conclusion, check errata, and
obtain independent review. A detailed modern source may be needed to disambiguate conventions, but
the historical attribution must then be recorded separately rather than presented as the exact
source of the modern PDE theorem.

No `H0` or `E4` evidence is claimed. The source state is `H3`: the repository's intended subject is
identifiable, while the exact proposition and primary proof source remain unresolved. No mathlib or
external Lean candidate is credited during intake; that search belongs to `ANCHOR_AUDIT` after the
statement gate.
