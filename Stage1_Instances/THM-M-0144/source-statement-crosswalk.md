# Source-statement crosswalk

## Available source record

The repository inventory supplies only: the Chinese title `曼宁对应`, Yuri Manin, year 1974, and
the phrase `形式群与上同调理论` ("formal groups and cohomology theories"). It gives no publication,
edition, theorem number, page, hypotheses, or proof reference. Its `已验证` label is untrusted under
rev-5.6. A repository-wide search found no theorem-specific Lean artifact for `THM-M-0144`.

No primary source is claimed here. The familiar relationship between complex-oriented cohomology
theories and formal group laws is only a discovery direction; its standard formulations have
multiple authors and materially different conclusions. Assigning one of them to Manin without a
source would substitute a theorem.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "formal groups" | formal group or formal group law, probably one-dimensional and commutative | coefficient ring, formal power series, group-law identities, coordinate/isomorphism notion | domain unresolved |
| "cohomology theories" | generalized multiplicative cohomology theory, possibly complex-oriented | represented theory or axiomatized functor, products, coefficients, orientation | domain unresolved |
| "correspondence" | association, classification, equivalence, or realization | exact map and quantified inverse/existence properties | conclusion unresolved |
| Yuri Manin / 1974 | bibliographic locator | no proof credit | primary publication unidentified |

## Gates to source fidelity

Before `H0`, a stable primary edition must be inspected and an independent reviewer must verify the
exact title, theorem/page, definitions, ordered assumptions, conclusion, proof boundary, translation
issues, and errata. Before statement credit, every verified source component must map row by row to
an elaborated Lean expression. A later anchor audit must separately search pinned mathlib and
credible external Lean 4 projects; the negative repository search here is not that audit.
