# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names Faber and Krahn, dates the result to 1923, and describes it
only as "the isoperimetric inequality for the first eigenvalue." `Docs/Stage0_Blueprint.md` repeats
that phrase and leaves definitions, assumptions, proof history, axioms, and artifacts open. These
are discovery metadata, not a citable exact theorem and not evidence for the `verified` label.

## Candidate primary sources

- Georg Faber's 1923 work on the lowest vibration frequency/fundamental tone of a membrane is a
  historical primary-source candidate.
- Edgar Krahn's independent work on the corresponding minimum problem is a historical
  primary-source candidate (the repository attribution does not establish its exact publication
  year or edition).

Exact titles, journal/edition, theorem/page, original wording, hypotheses, and errata have not been
verified from scans in this intake. They must not be invented from secondary recollection. The
statement phase must inspect at least one stable primary edition; a modern source may clarify
current Sobolev-domain conventions but cannot silently replace the historical claim.

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "first eigenvalue" | least Dirichlet eigenvalue of `-Delta` | concrete `lambda1` via spectrum or Rayleigh infimum | included; definition open |
| "isoperimetric" | optimization at fixed Euclidean volume | Lebesgue volume and equal-volume ball | included; normalization open |
| Faber-Krahn inequality | `lambda1(B) <= lambda1(Omega)` | ordered comparison with all hypotheses | human scope frozen |
| sharpness | balls attain the bound | checked ball evaluation/attainment | included; encoding open |
| equality case | only balls are minimizers | congruence/translation or a.e. domain equivalence | included; source conditions open |

## Source-fidelity gate

Before `H0`, an independent reviewer must verify edition, theorem/page, every domain and dimension
hypothesis, the eigenvalue convention, equality language, and known errata, then approve a
row-by-row source-to-Lean mapping. No Lean or external formal candidate has been audited at intake;
that work belongs to `S56-M-1287-ANCHOR_AUDIT` after exact statement elaboration.
