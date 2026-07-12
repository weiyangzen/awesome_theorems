# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `哈代-李特尔伍德圆法`, attributes it
to Godfrey Hardy and John Littlewood, dates it to 1918, and gives only `堆垒数论的基本方法`
("a fundamental method of additive number theory"). `Docs/Stage0_Blueprint.md` repeats that phrase
and explicitly leaves the exact definition, assumptions, proof path, dependencies, axioms, and
machine artifact open. The rev-5.6 manifest carries `已验证` only in the untrusted source-status
field. None of these records contains a proposition.

## Primary-source boundary

The historical attribution points toward Hardy-Littlewood work on additive number theory, but the
inventory gives no paper title, edition, theorem, page, or one of the several results obtained by
the method. Intake does not promote the attribution to `H0`. The source phase must select an
immutable scan or edition, quote one theorem, record its page and assumptions, inspect relevant
errata, and obtain independent review. A later textbook formulation is acceptable as a locator but
cannot silently choose the target in place of the missing repository statement.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "additive number theory" | a representation problem for integers | exact summand set, power/prime predicate, count and target domain | absent |
| "circle" | coefficient extraction over `R/Z` or a contour | `AddCircle`, Haar integral, additive character or a source-selected contour | pinned APIs probed; choice open |
| "method" | major/minor arc proof architecture | measurable arc sets, decomposition, estimates and composition theorem | not a proposition |
| main contribution | singular series/integral and asymptotic main term | exact definitions, convergence and local-factor conditions | absent |
| error control | minor-arc and approximation bounds | norms, asymptotic filter, uniform parameters, constants | absent |
| `已验证` | untrusted inventory label | no Lean expression and no proof credit | explicitly rejected |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded probe
imports `Mathlib.Analysis.Fourier.AddCircle` and checks the additive circle, normalized Haar
measure, Fourier monomial, and Fourier coefficient APIs. Repository-local search also finds a
`Mathlib.Combinatorics.KatonaCircle` module; its documentation identifies the Katona double-counting
method, so it must not be mistaken for the Hardy-Littlewood analytic method. These observations are
encoding and disambiguation evidence only, not the later immutable formal-anchor audit.

