# Source-statement crosswalk

The repository discovery text in `Docs/researches/math_theorems.md` records `给定度序列的随机图`
("a random graph with a prescribed degree sequence"), attributes the configuration model to Bela
Bollobas, and dates it to 1980. It does not state a proposition, assumptions, or a conclusion.

| Claim component | Human source anchor | Lean target at intake | Assessment |
|---|---|---|---|
| Historical pairing construction | B. Bollobas, *A Probabilistic Proof of an Asymptotic Formula for the Number of Labelled Regular Graphs*, European Journal of Combinatorics 1(4) (1980), 311-316, DOI `10.1016/S0195-6698(80)80030-8` | none selected | Crossref bibliographic metadata corroborates author, title, date, journal, volume, issue, and pages; the primary theorem text has not been accepted |
| Prescribed degree data | repository phrase "given degree sequence" | future finite type and `V -> Nat` data | the 1980 title concerns regular graphs; it must not be treated as a premise-level source for an arbitrary-degree theorem without inspecting the paper and further primary sources |
| Pairing sample space | standard configuration-model reading uses labelled half-edges and pairings | future finite matching type and probability measure | absent from the repository statement; labels and the uniform object must be fixed |
| Resulting object | contraction of pairs generally gives a multigraph with loops and parallel edges | future multigraph encoding | calling the output a graph does not decide multigraph versus simple graph |
| Exact conclusion | possible degree preservation, simplicity probability, conditioning identity, enumeration, or asymptotic result | no proposition selected | wholly absent; choosing one now would broaden or substitute the target |

The DOI is a discovery locator, not an immutable evidence receipt:
<https://doi.org/10.1016/S0195-6698(80)80030-8>.

No `H0` claim is made. `H2` records only that a plausible primary historical source and bibliography
are identified while exact theorem/page, premise mapping, arbitrary-degree genealogy, edition hash,
errata/corrections, and independent review remain open. The statement phase must first decide what
the repository entry is meant to assert, then locate a primary numbered statement matching that
choice. A regular-graph enumeration theorem, an arbitrary-degree simplicity theorem, and the basic
degree invariant are not interchangeable.
