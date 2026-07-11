# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` gives only the title "Liouville theorem", Joseph Liouville,
1844, the statement "bounded harmonic functions are constant", importance "high", and the status
`已验证`. `Docs/Stage0_Blueprint.md` lists the target but adds no bibliography or assumptions. No
edition, theorem number, page, proof, or errata record is attached, so no primary source is asserted
and no `H0` credit is available at intake.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "harmonic function" | a function satisfying a harmonicity condition | domain, codomain, regularity and Laplacian/harmonic API | unresolved |
| "bounded" | a global boundedness hypothesis | norm/order formulation and quantifier scope | unresolved |
| "constant" | all values agree / function is constant | exact predicate or existential constant | unresolved |
| PDE category | excludes unrelated named Liouville theorems | namespace and target type | fixed only as disambiguation |
| Joseph Liouville, 1844 | historical attribution | primary edition and theorem location | unverified metadata |
| `已验证` | untrusted repository label | inspectable source and kernel receipts | no credit |

## Lean boundary

No target-specific legacy slot is listed by the rev-5.6 manifest. Intake therefore does not nominate
or credit a mathlib declaration. The statement phase must first freeze the human formulation, then
elaborate a canonical Lean expression with minimal pinned imports. Candidate discovery belongs to
the later anchor-audit phase and cannot retroactively choose a more convenient theorem here.
