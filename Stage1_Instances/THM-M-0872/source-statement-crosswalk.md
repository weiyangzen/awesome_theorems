# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6390-6395` supplies exactly the title `Bodlaender算法`, Hans
Bodlaender attribution, year 1996, gloss `树宽的线性时间近似`, importance "high," and status
`已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, approximation
factor, graph or decomposition definition, parameter convention, algorithm, cost model, binders,
hypotheses, conclusion, proof boundary, corrections, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:23792-23817` repeats the gloss while explicitly leaving the formal
system, logical foundation, exact definitions and premises, proof route, dependencies, alternate
forms, axioms, machine state, and artifact links open. The rev-5.6 manifest retains `已验证` only
as untrusted metadata and resets the target to `L0 / rework_required`.

## Year-matched primary-source lead

Crossref and DBLP metadata identify Hans L. Bodlaender, *A Linear-Time Algorithm for Finding
Tree-Decompositions of Small Treewidth*, *SIAM Journal on Computing* 25(6), December 1996, pages
1305-1317, DOI `10.1137/S0097539793251219`. The observed Crossref response and DBLP BibTeX are
digest-bound in `instance.json`. The publisher article endpoint returned HTTP 403, so the journal
body, exact theorem numbering, proof, and errata were not inspected in this run.

Utrecht University's repository also identifies the open 1992 technical-report precursor
RUU-CS-92-27 under handle `1874/16670`. Its repository metadata and bitstream record were inspected:
the latter reports an 863740-byte original named `bodlaender__alineairtime.pdf` with MD5
`5a693dd987524c9e28fd34ba8b424e6a`. The current content endpoint generated a different 21-page
wrapper PDF on each request and exposed only repository cover metadata to text extraction, so that
mutable wrapper is not admitted as the theorem text or immutable proof source. A STOC 1993
precursor has DOI `10.1145/167088.167161`.

The repository/OpenAIRE summary of the source family says: for constant `k`, a linear-time
algorithm, given `G = (V,E)`, determines whether the treewidth of `G` is at most `k` and, if so,
finds a tree decomposition of width at most `k`. This is a strong source-family lead, but the
catalog-to-paper identity, exact edition and theorem locator, incorporated definitions, proof and
correction audit, and independent review remain open. It supports neither H0 nor canonical target
selection at intake.

## Component crosswalk

| Catalog component | Source-family component | Prospective Lean surface | Intake status |
|---|---|---|---|
| "treewidth" | minimum, over tree decompositions, of maximum bag size minus one | dossier-local tree-decomposition and width definitions over `SimpleGraph` | absent in pinned mathlib; convention unresolved |
| "approximation" | no approximation factor appears in the year-matched article summary | exact or approximate result must be one explicit `Prop` | material mismatch; root unresolved |
| "linear time" | for constant/fixed `k`, runtime linear in graph input size | encoded algorithm plus checked machine/cost bound with `k`-dependent constant policy | model and quantifier order unresolved |
| "Bodlaender algorithm" | decision whether `tw(G) <= k`, plus positive decomposition output | sound/complete executable result and certificate relation | algorithm and output encoding absent |
| Hans Bodlaender / 1996 | exact journal bibliographic match | no formal component | bibliographic/source-family lead only |
| `已验证` | catalog status label | no Lean proposition or proof object | explicitly untrusted; no H or M credit |

## Neighbor boundary

`THM-M-0870` owns the broad treewidth record and `THM-M-0871` owns Courcelle's theorem. Their
future definitions may be shared, but neither transfers canonical statement identity, proof credit,
or status. Later constant-factor approximation algorithms cannot be substituted merely because
they better match the Chinese word `近似`; the author, year, guarantee, and theorem must be reconciled.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.SimpleGraph.Acyclic` supplies `SimpleGraph`, `SimpleGraph.IsAcyclic`, and
`SimpleGraph.IsTree`; `Mathlib.Computability.TuringMachine.Computable` supplies
`TM2ComputableInTime` and `TM2OutputsInTime`. The discovery-only probe checks those interfaces.
They provide graph/tree and step-bound substrate, but no bags, tree decomposition, width, treewidth,
Bodlaender algorithm, fixed-parameter bound, or approximation theorem. A bounded source search
found no exact-topic declaration in pinned mathlib or the repo-local Lean tree. This is not an
exhaustive external anchor audit or a formal absence theorem.

Before leaving `H5`, accountable reviewers must choose and preserve one exact proposition, resolve
the approximation-versus-exact mismatch, record an edition and pinpoint theorem/definition/proof
crosswalk plus corrections, fix all quantifiers and boundary cases, reconcile neighboring targets,
and independently approve the decision. Only then may the statement phase elaborate and
mutation-test an identical Lean expression.
