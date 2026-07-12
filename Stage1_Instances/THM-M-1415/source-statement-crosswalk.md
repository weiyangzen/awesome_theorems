# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:10341`-`:10346` is the catalog record. It gives `Markov分割`,
Yakov Sinai and Rufus Bowen, 1970, and only `双曲系统的符号化` (`symbolization of
hyperbolic systems`). It gives no domain, definitions, quantifiers, hypotheses, conclusion,
citation, proof, or formal artifact. The six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; that is catalog provenance, not a mathematical
source revision.

`Docs/Stage0_Blueprint.md:38483`-`:38508` repeats the gloss while explicitly leaving the exact
definitions and premises, proof route, dependency graph, equivalent forms, axioms, machine status,
and artifact links open. The rev-5.6 manifest therefore retains `已验证` only as
`source_status_untrusted` and starts the target at `L0 / rework_required`.

## Primary-source discovery candidates

Crossref publisher metadata identify Rufus Bowen, *Markov Partitions for Axiom A
Diffeomorphisms*, *American Journal of Mathematics* **92**(3) (July 1970), starting at p. 725,
DOI `10.2307/2373370`. The title strongly supports an existence-theorem family for Axiom A
diffeomorphisms. Intake did not inspect the article text, exact theorem/page range, definitions,
assumptions, conclusion bundle, proof boundary, corrections, or errata.

Crossref publisher metadata also identify Ya. G. Sinai, *Markov partitions and
C-diffeomorphisms*, *Functional Analysis and Its Applications* **2**(1) (1968), 61-82, DOI
`10.1007/BF01075361`. This is consistent with the catalog attribution but conflicts with its bare
year 1970. Intake did not inspect the original or translated article text, define
`C`-diffeomorphism, audit the translation relationship, or locate an exact theorem passage and
assumptions.

A related Sinai follow-up is *Construction of Markov partitions*, *Functional Analysis and Its
Applications* **2**(3) (1968), 245-253, DOI `10.1007/BF01076126`. Its distinct title and issue add
another plausible source boundary. Intake inspected publisher metadata only and did not determine
its exact relationship to the first Sinai paper or the catalog target.

OpenAlex records both articles as closed access with no repository full text. That is a bounded
access observation, not evidence that no lawful copy exists. Because only metadata were inspected,
the citations are discovery anchors rather than `H0` packets. The repository title and gloss also
do not decide whether Bowen's existence result, Sinai's formulation, the derived coding theorem,
or a combination is intended.

## Component crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean surface | Intake assessment |
|---|---|---|---|
| `Markov分割` | finite family of source-defined rectangles with cover/disjoint-interior and Markov properties | finite family of sets, relative topology, stable/unstable data, boundary and transition predicates | theorem family identified; exact definition open |
| "hyperbolic systems" | exact system class, regularity, invertibility, and invariant hyperbolic set | phase type, dynamics, derivative or abstract hyperbolicity, invariant subtype, compactness/local product structure | all proposition-changing choices open |
| "symbolization" | itinerary or coding through a full shift or subshift of finite type | alphabet, `Nat`/`Int` path space, shift, admissibility relation, coding map | desired conclusion family only |
| Markov property | forward stable and backward unstable inclusions, with source boundary conventions | checked set/plaque inclusions under the map and inverse | definitions absent from repository |
| coding strength | shift-commuting map, continuity, surjectivity, multiplicity/injectivity clauses | `Function.Semiconj` plus source-specific regularity and fiber results | generic semiconjugacy API exists; no exact target |
| Bowen / 1970 | possible Axiom A primary source | documentation and source review only | metadata checked; theorem text not inspected |
| Sinai / 1970 | possible Sinai paper, actually cataloged by publishers as 1968 | documentation, translation and chronology review | unresolved mismatch; theorem text not inspected |
| `已验证` | untrusted catalog status | no proposition or proof component | explicitly rejected as evidence |

## Pinned Lean boundary

The pinned environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. `IntakeProbe.lean` checks generic APIs for set
partitions, stream shifts, semiconjugacy, iterated semiconjugacy, and transport of periodic points.
These are representation ingredients only. A bounded name search found no Markov-partition,
subshift, symbolic-dynamics, Axiom A, Anosov, or hyperbolic-set target surface in pinned mathlib or
the repository's Lean sources.

That bounded result is feasibility evidence, not the later immutable anchor audit, an exhaustive
external-project claim, or evidence for a canonical statement. The machine status remains `M4`
for the unselected root.

## First downstream blocker

The statement phase must obtain and hash an immutable primary edition, identify one exact
definition/theorem/page passage, map every assumption and conclusion, audit proof boundaries,
translation and errata, and obtain independent source approval. It must explain why the selected
proposition is this catalog target rather than a neighboring symbolic-dynamics, hyperbolicity, or
spectral-decomposition result. Only then may it freeze ordered binders, boundary cases, minimal
imports, an elaborated expression, checked alternate transports, and mutation tests.

The provisional human status is `H1`: credible primary publications exist, but the exact theorem,
definitions, premises, translation, errata, and source-to-target mapping remain unaudited. It is
not `H0`, and it does not authorize selecting a proposition from titles or secondary memory.
