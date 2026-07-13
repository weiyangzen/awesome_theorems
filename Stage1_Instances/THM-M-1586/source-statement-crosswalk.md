# Source-statement crosswalk

## Repository records

`Docs/researches/math_theorems.md:11686-11691` supplies exactly the title `Hamming界`, Richard
Hamming, 1950, the gloss `纠错码的球包装界`, importance `high`, and status `已验证`. Git history
attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, theorem
locator, formula, alphabet, code definition, parameter ranges, proof boundary, correction history,
reviewer, or formal artifact.

`Docs/researches/cs_theorems.md:614` repeats the same title, attribution, year, gloss, importance,
and untrusted status. Stage0 does not project that row as a separate Hamming-bound UID even though
it projects nearby coding rows; this is an intake-boundary fact, not authority to merge evidence.

`Docs/Stage0_Blueprint.md:43120-43145` repeats the mathematical gloss while explicitly leaving the
formal system, exact definitions and premises, proof history, dependencies, equivalent statements,
axioms, machine status, and artifact links open. Rev-5.6 preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal component crosswalk

| Catalog element | Necessary mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| `Hamming界` | one finite or asymptotic sphere-packing theorem | one exact `Prop` plus checked transports | theorem family only |
| "error-correcting code" | codewords in a Hamming word space and a correction/separation contract | finite set/subset, encoder image, or linear submodule | code model open |
| "sphere" | Hamming ball with explicit center, radius, and membership inequality | finite filter or metric ball with cardinality theorem | encoding and boundary open |
| "packing" | pairwise disjoint balls and containment in the ambient word space | disjoint-union cardinality inequality | proof architecture only, not a selected claim |
| "bound" | exact cardinality, dimension, extremal-size, or rate inequality | natural/integer/real inequality with casts | conclusion form open |
| Richard Hamming / 1950 | historical source identity | immutable source and pinpoint crosswalk | bibliographic lead identified; H0 open |
| `已验证` | would require reviewed H evidence and kernel receipts | accepted source and machine evidence | no credit |

## Primary-source discovery lead

Crossref identifies R. W. Hamming, *Error Detecting and Error Correcting Codes*, *Bell System
Technical Journal* 29(2), April 1950, pages 147-160, DOI
`10.1002/j.1538-7305.1950.tb00463.x`. The Crossref record is a bibliographic metadata source, not
the paper's theorem text. Semantic Scholar identifies the same DOI, title, author, and year and
points to a repository scan candidate at the Naval Postgraduate School.

The scan host did not accept a connection from this worker, while the DOI landing page returned an
automated-access challenge. Therefore no complete primary text, exact section/equation locator,
incorporated definitions, proof boundary, or errata was inspected. The likely source family is
credible enough for `H1` discovery, but not for `H0` or for selecting a canonical formula.

## Candidate-root crosswalk

| Candidate root | Material content | Why not canonical at intake |
|---|---|---|
| Finite q-ary nonlinear Hamming bound | `|C|` times a radius-`t` q-ary Hamming-ball volume is at most `q^n` under pairwise distance at least `2*t+1` | catalog fixes none of alphabet, code, parameters, or arithmetic conventions |
| Minimum-distance form | radius is `floor ((d-1)/2)` and the inequality is stated using minimum distance `d` | needs a definition for empty/singleton codes and exact natural-number boundary rules |
| Binary specialization | ball volume is `sum choose(n,i)` and ambient size is `2^n` | may match the historical paper but is narrower than the usual unqualified modern name |
| Linear `[n,k,d]_q` form | `q^k` replaces code cardinality and yields a dimension/cardinality constraint | assumes finite-field and linear-code structure absent from the catalog |
| Perfect-code equality | equality characterizes a partition of the word space by decoding balls | stronger/different conclusion than the supplied upper-bound gloss |
| Asymptotic rate form | translates finite packing into an entropy upper bound on achievable rate | introduces limits, entropy, and parameter regimes absent from the 1950 gloss |

## Finite packing proof skeleton, not yet an obligation registry

For a prospective finite statement, pairwise distance at least `2*t+1` makes radius-`t` Hamming
balls about distinct codewords disjoint by the triangle inequality. Each ball has the same finite
cardinality for a constant alphabet, and their disjoint union lies inside the `q^n`-element word
space. Counting gives the packing inequality. This explanation discriminates the theorem from the
Gilbert covering lower bound and Singleton puncturing bound. It is not a frozen proof tree, a
source-faithful reconstruction, or proof evidence.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`hammingDist`, symmetry, the triangle inequality, its coordinate-cardinality upper bound,
`Hamming`, the finite instance, the metric-distance bridge, `Fintype.card_fun`, and `Nat.choose`.
A bounded exact-topic search found no Hamming-bound, sphere-packing-code, code-minimum-distance, or
code-size declaration in pinned mathlib or repository-local Lean.

These declarations are supporting interfaces only. Mathlib's `Hamming.lean` explicitly says the
metric is relevant to coding theory and minimum distance, but it defines no code object or bound.
The canonical module, declaration/expression, elaborated-expression hash, environment fingerprint,
checked transports, and statement mutations remain null. Search and probe results are intake
discovery evidence, not an exhaustive downstream anchor audit or proof of global absence.

## Statement gate

Before proof execution, accountable reviewers must preserve and hash a lawful complete primary or
authoritative source, select one exact result, transcribe every incorporated definition and
assumption, decide binary/q-ary and arbitrary/linear scope, fix binder order and all boundary cases,
audit corrections and errata, reconcile the duplicate and neighbor records, and independently
approve the mapping. The statement phase must then freeze minimal imports, serialize and hash the
elaborated target and environment, compile every credited transport, and run removed-hypothesis,
changed-domain, binder-scope, and boundary mutations.

Until then, the canonical mathematical and Lean targets remain null. `H1` does not refute or
downgrade the classical theorem; it records that this repository has not yet established exact
source-statement identity.
