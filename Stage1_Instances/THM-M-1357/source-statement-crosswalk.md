# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:9894-9899` supplies exactly the title `Nyquist稳定性判据`,
attribution to Harry Nyquist, the year 1932, the gloss `反馈系统的稳定性`, importance "high," and
status `已验证`. Git history attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The entry contains no model, formula, definition,
binder, hypothesis, conclusion, bibliography, edition, theorem or page locator, proof boundary,
correction record, or formal artifact.

`Docs/Stage0_Blueprint.md:36912-36937` repeats the gloss while explicitly leaving the target proof
system, logical foundation, background, exact definitions and premises, proof process,
dependencies, equivalent formulations, axioms, machine status, and artifact links open. The
rev-5.6 manifest retains `已验证` only as untrusted source metadata and resets this target to
`L0 / rework_required`.

## Historical source lead

Crossref metadata resolves DOI `10.1002/j.1538-7305.1932.tb02344.x` to H. Nyquist,
*Regeneration Theory*, *Bell System Technical Journal* 11(1), January 1932, pages 126-147. This is
a plausible primary-source lead that corroborates the catalog attribution and year. The repository
does not cite it, and intake did not obtain and review a lawful immutable full text, identify one
exact proposition, map its notation and assumptions, check corrections, or obtain independent
source review. Crossref metadata is therefore discovery evidence only, not an accepted source or
an `H0` crosswalk.

## Component crosswalk

| Repository element | Mathematical alternatives | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "feedback system" | negative or positive feedback; SISO or MIMO; continuous or discrete time; transfer or state-space model | future typed interconnection, transfer function, or realization definitions | topology, sign, domain, and semantics absent |
| "stability" | internal, asymptotic, exponential, BIBO, input-output; strict or non-strict half-plane/disk | future exact predicate over modes, poles, trajectories, or operators | conclusion not selected |
| "Nyquist criterion" | encirclements of `-1` by `L`, or zeros of `1 + L`; classical or generalized contour | a future winding/index predicate and meromorphic pole/zero counts | contour, orientation, signs, and equivalence direction absent |
| pole/zero count | open-loop RHP poles `P`, closed-loop characteristic zeros `Z`, multiplicities and boundary rules | `MeromorphicOn.divisor`, `meromorphicOrderAt`, finite sums over a source-selected region | adjacent divisor API only; no system mapping or count identity |
| plot or contour | imaginary-axis contour closed in a half-plane, indented contour, or unit circle | source-selected path/loop plus a winding-number interface | no winding-number or complete argument-principle API was located by the bounded search |
| Harry Nyquist / 1932 | historical attribution and likely paper lead | provenance metadata only | not a reviewed theorem/page locator |
| `已验证` | untrusted inventory label | no Lean declaration or proof object | explicitly rejected as evidence |

## Proposition boundaries

The abstract argument-principle identity, a classical scalar closed-loop stability equivalence, a
generalized MIMO determinant test, and a discrete-time unit-circle criterion are not interchangeable
targets. Nor can input-output stability be substituted for internal stability when cancellations or
nonminimal realizations may hide unstable modes. Boundary poles, contour indentation, orientation,
and whether clockwise or counterclockwise encirclements are positive change the literal count
formula. The repository chooses none of these options, so intake cannot truthfully fill ordered
binders, hypotheses, a conclusion, or an exact Lean expression.

The neighboring targets `THM-M-1355` (linear-system stability) and `THM-M-1356`
(Routh-Hurwitz criterion) are scope boundaries, not interchangeable sources or proof credit.

## Lean boundary and retry requirement

At the pinned mathlib revision, `MeromorphicOn.divisor`, `meromorphicOrderAt`, `logDeriv`,
`circleMap`, and `periodic_circleMap` elaborate. They are only ingredients for possible future
encodings. The bounded local search found no obvious control-system or terminal Nyquist
declaration, but it is not the required immutable external anchor audit and does not prove global
absence.

Before the statement phase can close, accountable reviewers must preserve and hash an immutable
source edition; identify its exact theorem, section, and page; transcribe all incorporated
definitions, ordered binders, assumptions, conclusion, proof boundary, and correction status;
resolve the scope choices and neighboring-target boundaries; and independently approve the
mapping. Only then may the Lean statement gate freeze minimal imports, an elaborated expression,
checked transports, and removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
