# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10525-10530` supplies exactly the title `割线法`, attribution
`众多数学家`, period `20世纪`, gloss `方程求根的超线性方法`, importance "high", and status
`已验证`. All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, stable source
identifier, theorem number, page, displayed recurrence, assumptions, proof, errata, or formal
artifact.

`Docs/Stage0_Blueprint.md:39190-39215` repeats those fields and explicitly leaves the target system,
exact definitions and premises, proof process, dependencies, equivalent forms, axioms, machine
status, and artifact links open. Its generic closed-result and leaf-audit wording is generated
planning metadata, not source or proof evidence. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `方程求根` (finding roots) | solve `f(a) = 0` | scalar-versus-system choice, domain/codomain, `f`, root `a`, membership and equality/residual predicate | all unspecified |
| `割线` (secant) | two-point divided-difference recurrence | sequence or state pair, starts, indexing, division and domain-safety proofs | implied by name only; recurrence absent |
| `超线性` (superlinear) | an asymptotic error-rate property | selected Q/R/order definition, filters, norms, nonzero errors, quantified limit | taxonomy and exact conclusion absent |
| `方法` (method) | recurrence, convergence, rate, correctness, or algorithm | one truth-valued proposition | no proposition selected |
| `众多数学家` / `20世纪` | historical metadata | verified edition and theorem/page | not a source citation |
| `已验证` | untrusted screening label | accepted source and kernel receipts | no credit |

The literal wording cannot populate the canonical domain, ordered binders, hypotheses, conclusion,
alternate encodings, excluded cases, expression hash, or environment fingerprint required by the
rev-5.6 statement contract.

## Formal discovery boundary

The pinned library provides general ingredients for possible future encodings: filter convergence,
little-o asymptotics, field division, function iteration, and the real golden ratio. The exact
bounded name/vocabulary search recorded in `validation.md` located no declaration implementing or
proving a numerical secant-method theorem in the searched repository and pinned-mathlib roots.
`IntakeProbe.lean` elaborates only those ingredients. These are successful pinned substrate checks,
not E3 evidence for `THM-M-1441`: without a canonical proposition or obligation, no target evidence
tier attaches. They cannot establish statement identity, the recurrence, convergence, rate, or
proof closure, and the downstream formal-candidate audit remains open.

The adjacent repository targets sharpen the non-substitution boundary: Newton iteration
`THM-M-1440`, bisection `THM-M-1442`, fixed-point iteration `THM-M-1443`, and Banach fixed point
`THM-M-1444` have different method definitions and hypotheses. No statement or proof credit is
shared merely because all can participate in root finding.

## Source gate and retry condition

No primary mathematical source is identified at intake. An accountable source reviewer must pin an
immutable primary or approved authoritative edition and exact theorem/page, audit definitions and
errata, select one truth-valued secant-method claim, and map every recurrence field, binder,
assumption, rate definition, conclusion, constant, and boundary case. A numerical-analysis reviewer
must independently approve its separation from neighboring targets.

Only after that correction may the statement phase choose minimal imports, elaborate an exact Lean
expression, serialize its environment fingerprint, check alternate transports, and run statement
mutations. Until then `H5` describes the catalog target's ill-posed proposition status, `M4` the
absence of a source-identical usable formal artifact, and `R4` the absence of an anchorable proof
reconstruction. These classifications do not deny established secant-method mathematics.
