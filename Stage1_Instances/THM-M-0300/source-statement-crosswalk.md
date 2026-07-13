# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:2153-2158` supplies the title `哈代空间原子分解` ("Hardy
space atomic decomposition"), Charles Fefferman and Elias Stein, the year 1972, the literal gloss
`H^1空间的原子分解` ("atomic decomposition of the `H^1` space"), importance `高` ("high"),
and status `已验证` ("verified"). All six uncited lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record does not identify a publication,
edition, theorem, page, formula, definition, premise, proof boundary, correction, reviewer, or
formal artifact.

`Docs/Stage0_Blueprint.md:8278-8303` repeats the gloss while explicitly leaving exact definitions
and premises, proof route, dependencies, equivalent formulations, axioms, machine status, and
artifact links open. The rev-5.6 manifest retains `已验证` only as untrusted metadata and resets the
target to `L0 / rework_required`.

## Source status and bibliographic boundary

No primary theorem text was obtained, inspected, or proposition-level crosswalked for this target.
The attribution and date make C. Fefferman and E. M. Stein, "H^p spaces of several variables,"
*Acta Mathematica* 129 (1972), 137-193, DOI `10.1007/BF02392215`, a plausible discovery lead.
Only bibliographic metadata was checked; the paper is not accepted here as the source of this
catalog statement, and no theorem/page, definition, hypothesis, conclusion, proof, or erratum from
it is credited.

Later titles such as R. R. Coifman, "A real variable characterization of H^p" (1974), and R. H.
Latter, "The atomic decomposition of Hardy spaces" (1979), further demonstrate that the generic
gloss and 1972 attribution do not by themselves select one standard atom theorem. They are
bibliographic discrimination leads only. A source audit must preserve an immutable exact edition,
locate the incorporated theorem and definitions, map assumptions and proof boundaries, check
corrections, and obtain independent review before any `H0` claim.

Because the received wording does not select one proposition, its current human-source
classification is `H5`, not `H0` or `H1`. This classifies the catalog wording as unstable; it does
not classify a future source-selected theorem as false or open.

## Component crosswalk

| Repository phrase | Possible mathematical component | Required Lean surface | Intake assessment |
|---|---|---|---|
| `H^1` space | real, analytic, boundary, or metric-measure Hardy space | exact carrier, measure, representatives, normed model | unidentified |
| atom | localized function with size and cancellation constraints | source-specific predicate over an exact function type | convention open |
| atomic decomposition | countable scalar representation | coefficient and atom sequences, summability, series convergence, equality relation | conclusion open |
| decomposition theorem | representation alone or space/norm characterization | source-selected implications and quantitative bounds | wording insufficient |
| `已验证` | untrusted catalog status | no Lean proposition or proof body | explicitly rejected |

The unresolved map includes domain and dimension, scalar field, Hardy norm, atom support and size
normalization, cancellation order, coefficient indexing, convergence topology, equality modulo
almost everywhere or distributions, converse inclusion, norm-equivalence constants, and all
boundary cases. Choosing values for these fields at intake would broaden or substitute the target.

## Duplicate crosswalk

`Docs/researches/math_theorems.md:2633-2638` separately records `THM-M-0362`, `原子分解定理`
("Atomic decomposition theorem"), with exactly the same authors, year, gloss, importance, and
status. `Docs/Stage0_Blueprint.md:9962-9987` likewise leaves its exact definitions, proof, axioms,
and formal artifacts open. The two IDs have different categories and execution ranks but no stated
mathematical distinction.

This is strong duplicate evidence, not an accepted identity decision. The existing `THM-M-0362`
dossier is read-only discovery input and cannot supply source authority, statement precision,
receipt, or proof credit to `THM-M-0300`.

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded exact-topic
search found no concrete Hardy-space or atomic-decomposition root in mathlib or repo-local Lean.
`IntakeProbe.lean` checks generic `Lp`, `MemLp`, integrability, Bochner integral, Haar volume,
filter convergence, and summability interfaces. These are possible substrate only. The probe
defines neither `H^1` nor an atom and declares no target or proof body.

These observations are bounded intake discovery, not the later immutable anchor audit and not a
global absence claim. Before the statement gate, an approved source must fix one proposition and
its ordered binders and boundaries; concrete Lean foundations must then be implemented or pinned,
the exact expression elaborated and fingerprinted, imports minimized, transports checked, and all
four required mutation classes executed.
