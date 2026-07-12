# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `代数复杂性`, Leslie Valiant, the year
1979, and only `代数计算复杂性` ("algebraic computational complexity") as its statement. The entry
appears twice with identical metadata. Stage0 repeats it while leaving the precise definitions,
assumptions, proof process, date of proof, dependencies, equivalent formulations, axioms, and
formal artifacts open. The rev-5.6 manifest preserves `已验证` solely as
`source_status_untrusted`.

The adjacent item `THM-M-0735` is VP versus VNP and is marked unresolved. That adjacency is useful
for rejecting accidental substitution but is not evidence identifying a theorem for this item.
No title, paper edition, theorem number, page, exact hypotheses, conclusion, or proof passage is
provided.

## Source work required

The attribution and year suggest Valiant's 1979 algebraic-complexity work, but a bibliographic guess
cannot freeze the target. A later source audit must inspect an immutable primary source and identify
one exact proved proposition, including its computation model, field or ring assumptions,
polynomial-family conventions, reductions, asymptotic quantifiers, theorem/page, and errata. It
must also explain why that result, rather than the paper's definitions or open conjectures, is the
intended repository target and obtain independent review.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "algebraic computation" | arithmetic circuit or straight-line program | source-faithful inductive syntax and evaluation semantics | absent |
| "complexity" | circuit size, depth, degree, class membership, or reduction | exact resource measure and ordered asymptotic quantifiers | ambiguous |
| "algebraic" | polynomials over a specified coefficient domain | `MvPolynomial` or a checked alternate encoding plus coefficient assumptions | basic pinned API probed only |
| Valiant, 1979 | possible bibliographic locator | immutable paper edition and pinpoint theorem | not yet inspected or accepted |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports the pinned `Mathlib.Algebra.MvPolynomial` degree, evaluation, and variable modules and
checks multivariate-polynomial construction, evaluation, variable support, and total degree. A
bounded name search found no mathlib arithmetic-
circuit, VP, VNP, or algebraic-complexity API. This is only an encoding-feasibility observation,
not the later immutable formal-anchor audit and not evidence for a canonical statement.
