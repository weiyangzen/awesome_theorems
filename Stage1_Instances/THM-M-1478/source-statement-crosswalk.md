# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10784-10789` supplies exactly the title `L-稳定性`, the
attribution `众多数学家`, the period `20世纪`, the gloss `数值方法的稳定性`, importance "high,"
and status `已验证`. Git provenance places all six uncited lines in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no method, test equation,
stability function, definition, binder, hypothesis, conclusion, proof, source locator, correction
record, or formal artifact.

`Docs/Stage0_Blueprint.md:40189-40214` repeats the catalog fields while explicitly leaving exact
definitions and premises, proof route, dependencies, equivalent forms, axioms, machine status,
and artifact links open. Its generic planning text is not source evidence. The rev-5.6 manifest
retains `已验证` only as `source_status_untrusted` and resets the target to
`L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| L-stability | a named stability property, characterization, or theorem family | exact predicate or exact truth-valued proposition | undefined |
| stability | absolute, A-, stiff-decay, contractive, power-bounded, or another sourced notion | complete stability predicate and problem class | unspecified |
| numerical methods | a general class or one selected scheme | method structure, coefficient data, recurrence or update semantics | unspecified |
| implied decay intuition | behavior of a stability object on stiff modes | exact function/domain/filter/limit statement and pole policy | absent from the record |
| many mathematicians / twentieth century | a source family | immutable edition and pinpoint proposition, definitions, proof, corrections, reviewer | no locator |
| `已验证` | untrusted inventory status | reviewed human-source packet or kernel receipt would be required | no H or M credit |

The title does not say whether the intended root defines L-stability, proves a characterization,
verifies a method, or states an existence or limitation theorem. The familiar textbook definition
cannot be silently installed because neither it nor its scope and limiting convention appears in
the received source.

## Source-family leads

Ernst Hairer and Gerhard Wanner, *Solving Ordinary Differential Equations II: Stiff and
Differential-Algebraic Problems*, second revised edition, Springer, 1996, DOI
`10.1007/978-3-642-05221-7`, is a strong modern source-family lead. The authors' table of contents
locates "The Stability Function" at page 40, "A-Stability" at page 42, and "L-Stability and
A(alpha)-Stability" at page 44 in Chapter IV.3. Later chapters treat particular implicit
Runge-Kutta and related method families. The authors' correction sheet for the 2010 printing
changes the intervals in which L-stability holds for an eight-stage parameterized method on page
98. This demonstrates that exact method, result, edition, and correction choices are material.

The DOI `10.1137/0504057` was noted as a possible historical lead to Byron L. Ehle's "A-Stable
Methods and Pade Approximations to the Exponential." No stable external response was retained or
hashed for this observation, so it is an uncredited search lead rather than recorded source
evidence, and not a catalog-cited L-stability proposition.

The repository cites neither source. No exact definition or theorem, incorporated definitions,
complete assumptions, proof boundary, correction impact, source ownership, or independent review
was admitted. The Hairer-Wanner lead remains `E5` discovery evidence and the unretained Ehle
observation remains below that evidence threshold; neither receives `H0` credit.

## Source exit gate

Before ordinary statement work, accountable reviewers must admit and hash one immutable source;
select one exact truth-valued proposition and every incorporated definition; map all ordered
binders, method data, test problem, stability-function domain and poles, A-stability component,
limit filter/path, hypotheses, conclusions, constants, and exceptional cases; audit the relevant
edition and corrections; reconcile ownership with `THM-M-1396`, `THM-M-1398`, `THM-M-1399`, and
`THM-M-1475` through `THM-M-1477`; and obtain an independent numerical-analysis source review.
The H classification must then be recomputed.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded exact-topic
search found no named L-stability, A-stability, Runge-Kutta, stability-function, stability-region,
amplification-factor, Dahlquist, or Radau declaration in repository-local Lean or the relevant
pinned mathlib source areas. `IntakeProbe.lean` checks complex-limit, rational-function,
finite-matrix, and ODE interfaces adjacent to a possible future encoding. This is not an exhaustive
anchor audit or a global absence claim.

Two representation hazards are frozen rather than resolved. The complex cocompact filter encodes
escape in arbitrary complex directions, not specifically along the negative real axis, inside a
sector, or within the left half-plane. Also, mathlib's total `RatFunc.eval` returns zero when its
reduced denominator evaluates to zero; reduced rational continuation and solvability of an
unreduced implicit Runge-Kutta stage system need not have the same domain. A credited target must
choose and encode both boundaries from the admitted source.

The canonical module, declaration/expression, elaborated-expression hash, environment fingerprint,
checked transports, and statement mutations remain null. Adjacent APIs supply no exact statement,
H0, M0, or proof credit.
