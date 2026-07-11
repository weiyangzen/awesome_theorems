# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` gives only the title "gradient estimate for harmonic functions,"
the attribution "many mathematicians," the twentieth century, the statement "a bound on derivatives
of harmonic functions," importance "high," and status `已验证`. `Docs/Stage0_Blueprint.md` merely
lists the title. No bibliography, edition, theorem number, page, assumptions, proof, or errata record
is attached. Thus no primary source or `H0` credit is asserted at intake.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "harmonic functions" | identifies the subject | domain, codomain, regularity, Laplacian/harmonic predicate | unresolved |
| title: "gradient estimate" | suggests a first-derivative bound | derivative representation, norm, evaluation region | provisional only |
| statement: "derivatives" | permits one or more derivative orders | order, Fréchet/coordinate derivative, quantifiers | unresolved |
| "bound" | asserts a quantitative inequality | RHS norm, radius/boundary distance, constant and dependencies | unresolved |
| PDE category | distinguishes the neighboring holomorphic Cauchy estimate | namespace and target type | fixed only as disambiguation |
| `已验证` | untrusted repository label | inspectable source and kernel receipts | no credit |

## Lean boundary

No target-specific legacy slot is listed by the rev-5.6 manifest. Intake does not nominate or credit
a mathlib declaration. The statement phase must first transcribe an exact primary-source theorem,
then elaborate its canonical Lean expression with minimal pinned imports. Candidate discovery and
proof credit belong to later phases and may not select a broader, weaker, or merely convenient
estimate retroactively.
