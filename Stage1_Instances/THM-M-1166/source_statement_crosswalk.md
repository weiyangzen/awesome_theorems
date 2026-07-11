# Source-statement crosswalk

| Claim component | Available source anchor | Required formal decision | Intake assessment |
|---|---|---|---|
| Item identity | `Docs/researches/math_theorems.md` names `椭圆型方程` | Preserve the subject identity | Repository metadata only |
| Human statement | The same entry says `二阶椭圆型方程的理论` | Select one truth-valued theorem and its exact conclusion | Not a proposition; no exact root is supplied |
| Attribution and date | “众多数学家”, “20世纪” | Record a primary author/work, edition, theorem/page, assumptions, and errata | Too broad for H evidence |
| Operator | Not stated | Freeze order, linearity, divergence form, coefficients, and ellipticity | Open |
| Domain and solutions | Not stated | Freeze dimension, domain/boundary regularity, function spaces, data, and weak/classical notion | Open |
| Lean representation | No formal artifact is cited | Identify a declaration or elaborate an exact expression with minimal pinned imports | `M4`; no candidate receives credit |

The catalogue label `已验证` is untrusted under rev-5.6. It is neither a primary mathematical
proof citation nor kernel evidence. Repository search found no statement for this ID beyond the
same catalogue wording and its generated projections.

## Non-equivalent readings

At least the maximum principle, weak Dirichlet solvability, elliptic regularity, Schauder estimates,
and fundamental-solution results could reasonably fall under the catalogue phrase. They differ in
quantifiers, hypotheses, and conclusions and cannot be interchangeable encodings of one canonical
claim. In particular, selecting Schauder estimates would duplicate neighboring `THM-M-1167`.

## Required source audit

1. Identify the catalogue compiler's intended theorem or obtain an authoritative primary/scholarly
   source that states one exact result; record edition, theorem/page, assumptions, and content hash.
2. Check corrections and reconcile the source's ellipticity, operator, domain, boundary, and
   solution conventions with a modern statement.
3. Map every source assumption and conclusion to ordered Lean binders before selecting a module.
4. Obtain independent review of the selection and crosswalk before assigning H0 or performing the
   statement gate.

Current human status is `H5`: there is not yet an exact human theorem to audit. This is a concrete
source-identification blocker, not a claim that elliptic PDE theory lacks established results.
