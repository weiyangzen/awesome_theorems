# Source-statement crosswalk

## Located repository source

`Docs/researches/math_theorems.md` names Axel Harnack, gives the year 1887, and summarizes the claim
as `正调和函数的比较` (comparison of positive harmonic functions). `Docs/Stage0_Blueprint.md`
repeats that summary but explicitly leaves definitions, hypotheses, proof, axioms, and machine
artifact open. The metadata label `已验证` is not primary-source evidence.

## Primary-source candidates requiring inspection

- Axel Harnack's 1887 work on logarithmic potential theory is the historical-source lead supplied
  by the repository metadata. Exact title, edition, theorem/page, wording, and errata have not been
  verified and must not be inferred from the name.
- A modern potential-theory text may be used to disambiguate contemporary hypotheses, but cannot
  silently replace the historical claim. Its exact edition, theorem/page, assumptions, and errata
  must be recorded before it can support H status.

These are discovery leads, not `H0` evidence.

## Crosswalk

| Repository phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| positive harmonic functions | function, codomain, harmonicity, positivity | concrete harmonic predicate and pointwise order | included; encoding open |
| comparison | quantitative value or sup/inf inequality | quantified points/set and exact inequality | included; form open |
| domain | connected open Euclidean region or ball | ambient space, openness, connectedness, containment | omitted by source summary |
| constant | geometry-dependent and function-independent bound | explicit constant or existential with dependencies | omitted by source summary |
| interior | comparison away from the boundary | compact containment or concentric radii | omitted by source summary |

Before `H0`, an independent reviewer must verify the chosen edition, theorem/page, definitions,
all hypotheses, constant dependencies, dimensional edge cases, and errata, and approve the exact
source-to-Lean row mapping. Until then the first statement blocker is source ambiguity, not proof.
