# Source-statement crosswalk

## Repository record and candidate sources

The repository inventory supplies the Chinese label "preferential attachment model", the authors
Barabasi/Albert, the year 1999, and the gloss "scale-free network model". Its `已验证` field is
explicitly untrusted under rev-5.6. It gives no numbered proposition, exact process, probability
space, degree observable, convergence mode, or quantifiers, so it cannot identify an exact theorem.

The historical primary candidate is Albert-Laszlo Barabasi and Reka Albert, *Emergence of Scaling
in Random Networks*, **Science** 286 (1999), 509-512, DOI
`10.1126/science.286.5439.509`. This is the natural source for the repository attribution, but the
intake has not treated its model discussion and continuum calculation as a pinned, numbered,
rigorous theorem statement.

A rigorous candidate is Bela Bollobas, Oliver Riordan, Joel Spencer, and Gabor Tusnady, *The degree
sequence of a scale-free random graph process*, **Random Structures & Algorithms** 18 (2001),
279-290, DOI `10.1002/rsa.1009`. Its precise random graph process and degree-sequence results are a
possible formal target, not an automatic substitute for the Barabasi-Albert record. Both entries
are discovery anchors rather than `H0` evidence; exact editions, theorem locators, assumptions,
errata, and source compatibility remain to be reviewed.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "preferential attachment" | endpoint probability and its normalization | stochastic transition kernel on finite (multi)graphs | family identified; exact rule open |
| growing network | seed and per-step vertex/edge update | time-indexed random graph process | included; initial and update conventions open |
| "scale-free" | exact degree mass/tail formula and exponent | degree-count random variable and asymptotic proposition | intended phenomenon identified; theorem strength open |
| degree distribution | expectation, empirical proportion, or random measure | measurable graph statistic and probability law | observable family identified; exact choice open |
| asymptotic claim | fixed or growing degree range and convergence mode | filter/probability convergence with ordered binders | unresolved and proposition-critical |
| Barabasi/Albert, 1999 | historical model and heuristic analysis | no machine-proof credit | candidate paper identified only |
| later rigorous result | exact model-to-model compatibility | checked equality, equivalence, or implication transport | candidate only; no transport established |

## Human and machine boundary

A repository-wide theorem-name search found no existing artifact for `THM-M-1116`. This intake
does not perform the later exhaustive mathlib or external Lean 4 anchor audit and makes no claim
that a formal preferential-attachment development exists.

Before `H0`, an independent reviewer must inspect an immutable primary edition, select the exact
numbered theorem or displayed result, map every definition and assumption, check errata, distinguish
heuristic from proved steps, and approve the row-by-row mapping. Before statement credit, that claim
must map to an elaborated Lean target without replacing the process, weakening the convergence
mode, fixing degree where the source is uniform, or assuming the desired power law.
