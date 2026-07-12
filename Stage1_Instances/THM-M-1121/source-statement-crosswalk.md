# Source-statement crosswalk

## Repository record and candidate source

The repository inventory supplies the title "Smirnov theorem", Stanislav Smirnov, the year 2001,
and the gloss "conformal invariance of triangular-lattice percolation". Its `已验证` field is
explicitly untrusted under rev-5.6. It gives no theorem number, domain class, boundary markings,
discretization, observable, or convergence mode, so it cannot by itself identify an exact
proposition.

The primary candidate matching the author, year, and gloss is Stanislav Smirnov, *Critical
percolation in the plane: conformal invariance, Cardy's formula, scaling limits*, **Comptes Rendus
de l'Académie des Sciences - Series I - Mathematics** 333 (2001), 239-244, DOI
`10.1016/S0764-4442(01)01991-7`. This intake records the paper only as a discovery anchor. An
immutable edition has not yet been inspected theorem by theorem, so the exact numbered result,
definitions, assumptions, proof boundaries, errata, and relation between its Cardy-formula and
broader scaling-limit statements remain unapproved. No `H0` credit is assigned.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "triangular lattice" | critical site model, dual hexagonal encoding, orientation, and mesh | countable planar lattice/hexagonal cells and mesh embedding | family identified; encoding open |
| "percolation" | independent Bernoulli coloring at `p = 1/2` | product probability space, measurable configuration, critical law | intended model identified; construction open |
| planar domain | source domain class and boundary regularity | planar set/domain predicates, topology, boundary or prime-end data | domain class open |
| crossing probability | marked arcs and exact connecting event | finite/discrete domain, path predicate, measurable crossing event | observable identified; conventions open |
| "conformal invariance" | covariance/invariance under conformal maps | conformal equivalence and transported boundary data | exact formulation open |
| Cardy's formula | normalized conformal coordinate and limiting value | explicit real-valued Cardy function or checked equivalent | candidate conclusion; normalization open |
| mesh limit | allowed approximations and convergence quantifiers | mesh-indexed probabilities and exact convergence predicate | topology and quantifier order open |
| "scaling limits" | crossing-only result versus configuration/interface result | separate target and topology for any stronger limit | must not be inferred from the gloss |

## Human and machine boundary

A repository-local search found no existing `THM-M-1121` theorem artifact and no Lean declaration
for critical percolation, Cardy's formula, or this conformal-invariance theorem in the checked
project sources. This limited intake search is not the later exhaustive formal-anchor audit and
makes no claim about external Lean projects or the complete pinned mathlib API.

Before `H0`, an independent reviewer must inspect an immutable primary edition, select the exact
theorem and pinpoint locator, map every definition and assumption, check errata and later
corrections, and approve the row-by-row mapping. Before statement credit, that claim must map to an
elaborated Lean target without changing the lattice, critical parameter, domain regularity,
boundary event, discretization, Cardy normalization, convergence mode, or quantifier order.
