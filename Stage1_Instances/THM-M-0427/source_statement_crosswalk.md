# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Artin Euler product attached to a Galois representation | E. Artin, *Uber eine neue Art von L-Reihen*, Abhandlungen aus dem Mathematischen Seminar der Universitat Hamburg 3 (1924), 89-108 | A future concrete replacement for `ArtinLFunctionModel`; representation and ramification APIs are discovery inputs | Primary source identified bibliographically, but exact page/formula, edition hash, translation, and assumptions audit remain open |
| Meromorphic continuation via reduction to one-dimensional characters | R. Brauer, *On Artin's L-series with general group characters*, Annals of Mathematics 48 (1947), 502-514 | Future virtual-character/Brauer-induction bridge plus Hecke/Dirichlet analytic APIs | Primary theorem source located; theorem numbering, hypotheses, normalization, and node mapping are not yet audited |
| Functional equation | Artin's original L-series work and later completed formulations; exact authoritative statement must be selected in the source audit | No exact Lean declaration selected | Included only provisionally because the legacy scope names it; source-normalized gamma/conductor/root-number conventions are unresolved |
| Trivial-representation specialization | Classical identification with a Dedekind zeta function | mathlib Dedekind-zeta anchors in `S1_M_081.lean` | Candidate boundary test only; no checked equality with an Artin Euler product exists locally |
| One-dimensional/abelian specialization | Class field theory identifies the relevant Artin and Hecke L-functions | mathlib Dirichlet-L anchors in `S1_M_081.lean` | Adjacent API, not an Artin-to-Hecke transport and not root closure |
| General holomorphy for nontrivial irreducibles | Artin holomorphy conjecture | none | Explicitly excluded: it is not a generally proved theorem and must not be smuggled into the target |

The manifest's Chinese description, `伽罗瓦表示的L-函数`, names a subject rather than a unique
theorem. This intake therefore freezes the narrow classical package that later phases must either
confirm from exact sources or revise without broadening it: concrete Euler factors, meromorphic
continuation, and a precisely normalized functional equation. The statement phase must not use the
legacy abstract structure's proposition fields as evidence, since their existential packaging does
not define the intended analytic objects.

Discovery identifiers (not immutable evidence receipts): Artin DOI
`10.1007/BF02954628`; Brauer DOI `10.2307/1969121`. No `H0` claim is made. Required follow-up is an
edition/file hash, exact theorem/page/formula crosswalk, assumptions and convention table, errata
search, and independent review.
