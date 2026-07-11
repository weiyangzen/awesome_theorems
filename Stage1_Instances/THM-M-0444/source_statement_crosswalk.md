# Source-statement crosswalk

| Claim component | Available source anchor | Lean target | Intake assessment |
|---|---|---|---|
| Target identity | Repository Stage0 metadata: Victor Kolyvagin, proposed background year 1990, `construction of an Euler system` | none | Metadata-level description only; it cannot freeze a proposition |
| Euler-system construction | V. A. Kolyvagin, *Euler systems*, in *The Grothendieck Festschrift*, Vol. II, Progress in Mathematics 87, Birkhauser (1990), pp. 435-483 | none located or credited | Primary-source candidate by title and period; exact theorem/page, edition scan, assumptions and errata still require audit |
| Heegner-point classes commonly associated with Kolyvagin's method | V. A. Kolyvagin, *Finiteness of E(Q) and Sha(E,Q) for a subclass of Weil curves*, Math. USSR-Izv. 32 (1989), 523-541 | none | Related primary source candidate, not evidence that this is the intended root |
| Indexed classes | Must be extracted from the selected primary theorem: index set, fields, coefficient module and cohomological degree | none | unresolved |
| Distribution relation | Must specify corestriction target, Euler polynomial and arithmetic/geometric Frobenius convention | none | unresolved |
| Exceptional/local hypotheses | Must include all bad primes, ramification, reduction and admissibility restrictions in the selected theorem | none | unresolved |

The phrase "Kolyvagin Euler system" names a theory/construction family rather than one unambiguous
closed proposition. In particular, an abstract statement saying that some family satisfies a
user-supplied norm relation would be a definition-shaped tautology, not Kolyvagin's construction.
Likewise, replacing construction with a downstream Selmer or BSD consequence would broaden or
substitute the target.

The next phase must first select a primary-source theorem by edition, theorem number and page. It
must then transcribe every datum, ordered binder, hypothesis, relation, convention and boundary
case; check corrections/errata; and only then propose and mutation-test a Lean expression. Until
that work is independently reviewed, the human-source status remains `H3` and machine status `M4`.

Discovery links (not immutable evidence receipts):

- Kolyvagin, *Euler systems*: <https://doi.org/10.1007/978-0-8176-4575-5_11>
- Kolyvagin, *Finiteness of E(Q) and Sha(E,Q) for a subclass of Weil curves*: <https://doi.org/10.1070/IM1989v032n03ABEH000779>

