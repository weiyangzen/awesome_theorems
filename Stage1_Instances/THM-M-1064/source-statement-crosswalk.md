# Source-statement crosswalk

## Candidate primary and authoritative sources

- A. V. Skorokhod, *Studies in the Theory of Random Processes*, Addison-Wesley (1965), English
  translation. This is the historical source family suggested by the Stage0 attribution/year, but
  the exact chapter, theorem, original-language edition, and translation correspondence have not
  yet been inspected.
- D. H. Root, "The existence of certain stopping times on Brownian motion", *Annals of
  Mathematical Statistics* 40 (1969), 715-718. This is a primary paper for a classical Brownian
  embedding construction, not evidence that its precise variant is the repository's intended
  random-walk statement.

These are discovery anchors only, not `H0` evidence. Exact theorem/page, wording, hypotheses,
proof boundary, edition, and errata require primary-source inspection and independent review.

## Statement crosswalk

| Repository phrase | Possible source component | Required Lean component | Intake status |
|---|---|---|---|
| "Skorokhod embedding" | a law represented by a stopped process | probability measure, filtration, stopping time, stopped value, `HasLaw` | included; variant open |
| "embedding a random walk" | simultaneous/iterated representation of partial sums | increment law, partial-sum process, increasing stopping times | intended phrase frozen; exact theorem open |
| centered/integrable law | classical admissibility conditions | Bochner integrability and expectation zero | source-dependent; not yet accepted |
| Brownian motion | usual continuous driving process | Brownian-process definition and natural filtration | source-dependent; API open |
| equality in distribution | embedded values reproduce target laws | exact `HasLaw` assertions and measures | included at conceptual level |
| stopping-time control | almost-sure finiteness, ordering, moments | measurable stopping times and a.e./integral bounds | source-dependent |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_220.lean` imports law, independence, optional
stopping, and hitting-time APIs. It then chooses a finite-state discrete variant and defines
`SkorokhodEmbeddingConclusion` with the desired law and control facts as fields. Consequently its
`StatementShape` asks for a conclusion package whose substantive contents are not derived. This is
useful API-discovery material but is neither an exact source crosswalk nor a terminal proof.

The similarly named Skorokhod weak-convergence representation theorem is explicitly outside this
target. Before `H0`, an independent reviewer must approve the selected primary theorem and every
assumption/conclusion row. Before statement credit, Lean must elaborate that exact mapping rather
than the legacy finite-state substitution.
