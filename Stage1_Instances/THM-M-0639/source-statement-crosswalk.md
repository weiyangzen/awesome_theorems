# Source-statement crosswalk

## Repository provenance

`Docs/researches/math_theorems.md` records `角谷不动点定理`, Shizuo Kakutani, 1941, and the
one-line gloss `集值映射的不动点` ("a fixed point of a set-valued map"). It supplies no formula,
definitions, hypotheses, theorem locator, proof, bibliography, errata, or formal artifact.
`Docs/Stage0_Blueprint.md` repeats the gloss and explicitly leaves precise definitions and
premises, proof path, dependencies, alternate forms, axioms, machine status, and artifacts open.
The rev-5.6 manifest preserves `已验证` only as untrusted source metadata.

## Primary-source lead

The historical lead is Shizuo Kakutani, *A generalization of Brouwer's fixed point theorem*,
**Duke Mathematical Journal** 8(3) (1941), 457-459,
DOI `10.1215/S0012-7094-41-00838-4`. Crossref metadata confirmed the author, title, journal
volume/issue, publisher, date, DOI, and publisher download locator. The Project Euclid article and
download endpoints returned an automated-access challenge rather than the paper in this worker
environment. Therefore the theorem text, preceding definitions, page-level assumptions, proof
boundary, and errata were not independently inspected here. The citation is a discovery anchor,
not `H0` evidence.

## Candidate crosswalk

| Catalog or likely source phrase | Candidate mathematical component | Candidate Lean surface | Intake status |
|---|---|---|---|
| "set-valued map" | a correspondence whose values remain in its domain | `F : K -> Set K` or `F : E -> Set E` plus containment | family lead only; encoding open |
| Euclidean convex domain | a nonempty closed bounded convex finite-dimensional set | `Set.Nonempty`, `IsClosed`, `Bornology.IsBounded`, `Convex` | source premise not admitted |
| compact-domain reformulation | compactness derived from finite-dimensional closed boundedness | `IsCompact` and a checked transport | alternate candidate only |
| nonempty closed convex values | pointwise inhabited, closed, convex image sets | `Set.Nonempty (F x)`, `IsClosed (F x)`, `Convex` | source wording uninspected |
| upper semicontinuity | open-set containment for nearby correspondence values | `UpperHemicontinuousOn` after definition audit | pinned API elaborated; equivalence unchecked |
| fixed point | some domain point belongs to its image | `exists x, x in K and x in F x` | intended family conclusion; exact binder open |
| `已验证` | untrusted catalog status | no proposition and no proof object | explicitly rejected as evidence |

## Duplicate and formal boundaries

`THM-M-0320` is a separately scheduled analysis/functional-analysis record with the same title and
a nearly identical gloss. Its dossier identifies the same paper and contains later-phase statement
and proof work, but rev-5.6 evaluates every target independently from L0. This intake neither merges
the IDs nor imports any of that target's statement, evidence, receipts, or status. A later source
review must decide whether the catalog records are intentional distinct variants or duplicates and
record an authoritative disposition before cross-target reuse is considered.

Pinned mathlib exposes `UpperHemicontinuousOn` and the basic Euclidean/convex/compactness APIs
checked by `IntakeProbe.lean`. A bounded exact-name search found no Kakutani set-valued fixed-point
declaration in pinned mathlib or the shared repo-local Lean tree. This is feasibility and discovery
evidence only, not the required immutable anchor audit and not proof of global absence.

Before source fidelity can reach `H0`, reviewers must preserve and hash a lawful primary copy,
pinpoint the theorem and incorporated definitions, map every premise and boundary case, inspect
corrections/errata, resolve the duplicate record, and independently approve the mapping. Before
statement credit, the approved claim must be elaborated with minimal pinned imports, serialized and
fingerprinted, transported from any alternate form by checked declarations, and mutation-tested.
