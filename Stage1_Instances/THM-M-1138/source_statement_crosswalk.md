# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Catalogue identity | `Docs/researches/math_theorems.md`, entry `极值原理`: `调和函数的最大值原理` | none selected | Repository source identifies the subject but omits hypotheses and conclusion details |
| Weak boundary maximum principle | Sheldon Axler, Paul Bourdon, Wade Ramey, *Harmonic Function Theory*, 2nd ed., Springer, 2001, Chapter 1, section "The Maximum Principle" | Future exact statement over a Euclidean domain | Credible textbook discovery anchor; edition hash, exact theorem/page, errata, and premise-to-node audit remain open, so no H0 credit |
| Boundedness and boundary continuity | Needed so the closure is compact and a boundary maximum is meaningful | Candidates using `IsCompact`, `frontier`, `ContinuousOn`, and a harmonic predicate | Exact types and library availability are intentionally deferred to statement/anchor-audit phases |
| Minimum principle | Apply the maximum principle to `-u` | Candidate checked transport | Not part of the root and not credited at intake |
| Strong principle | An interior maximum forces constancy on a connected domain | Separately owned by `THM-M-1140` | Explicitly excluded to avoid broadening or substituting the assigned theorem |

The English root is the standard weak form. This interpretation is constrained by the adjacent
separate strong-principle target, but the catalogue is not a primary mathematical source. Before
H0, the source audit must pin a scan or publisher artifact, verify the precise theorem number and
page against that artifact, search corrections/errata, and map each premise and conclusion to the
final Lean expression.

Discovery link (not an immutable evidence receipt):
<https://link.springer.com/book/10.1007/978-1-4757-8137-3>.

No machine candidate is claimed. The later anchor audit must search the pinned mathlib revision and
record every candidate's exact declaration type, proof-body provenance, axioms, and dependency pin.
