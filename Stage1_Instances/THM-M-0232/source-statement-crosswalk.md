# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1675-1680` supplies exactly the title `鲁歇定理`, Eugène Rouché,
1862, the gloss `全纯函数零点个数比较`, importance "high," and status `已验证`. All six uncited
lines entered the repository in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has
no bibliography, formula, definition of contour or zero count, hypotheses, proof, correction or
errata record, or formal artifact.

`Docs/Stage0_Blueprint.md:6437-6462` repeats those fields and explicitly leaves the formal system,
logical foundation, precise definitions and premises, proof route, dependencies, alternate forms,
axioms, machine state, and artifact links open. Its generic statement that a closed result is
believed to exist is planning metadata, not source or machine evidence. The rev-5.6 manifest keeps
`已验证` only as `source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Mathematical decision | Prospective Lean component | Intake result |
|---|---|---|---|
| `鲁歇定理` | which historical or modern Rouché theorem variant | one exact `Prop` plus checked alternate-form transports | family identified; root open |
| "holomorphic functions" | functions, common ambient domain, and regularity on interior/boundary/neighborhood | `f g : ℂ → ℂ` with exact `AnalyticOnNhd`, `DifferentiableOn`, or source-matched predicates | binders and predicates open |
| "number of zeros" | interior set, finiteness, multiplicity, and identically-zero convention | finite sum/cardinality based on `analyticOrderNatAt`, a divisor restriction, or another checked encoding | representation open |
| "comparison" | equality of counts for `f` and `f + g`, or for `f` and `g`, under which strict inequality | exact norm inequality on an exact boundary and equality conclusion | direction and function roles open |
| Rouché, 1862 | historical source and attribution | immutable edition, theorem/page, definitions, proof-node and errata mapping | source lead only |
| `已验证` | untrusted inventory metadata | inspectable human and kernel receipts would be required | no H or M credit |

## Inspected source leads

The University of St Andrews MacTutor biography of Eugène Rouché was inspected on 2026-07-13. It
identifies *Mémoire sur la série de Lagrange*, volume 39 of the *Journal de l'École Polytechnique*,
1862, and quotes a formulation: if `f` and `g` are regular within and on a closed contour, `f` is
nonzero there, and `|g| < |f|` on the contour, then `f` and `f + g` have the same number of zeros
inside. This is a secondary historical lead, not H0: it supplies no original page locator in the
memoir, definition chain, multiplicity wording, proof passage, corrections, errata, or independent
review.

The Bibliothèque nationale de France SRU catalog was also inspected. Records
`ark:/12148/cb312529403` and `ark:/12148/cb31252939w` identify Eugène Rouché's *Mémoire sur la
série de Lagrange*, Paris, Imprimerie impériale, 1866, 31 pages. The difference between that catalog
date and the repository/biographical 1862 journal date must be resolved as an edition or offprint
question. Bibliographic metadata does not establish an exact accepted theorem or proof.

## Alternate-form boundary

The perturbation form `|g| < |f|` comparing `f` with `f + g`, the difference form
`|f - g| < |f|` comparing `f` with `g`, disk and Jordan-domain versions, and winding-number or
divisor versions are plausible members of the family. None is canonical until statement work
selects an immutable source proposition and Lean compiles the relationship in every credited
direction. A specialized disk theorem or a source with additional finiteness and nonvanishing
hypotheses cannot silently stand in for a more general root.

## Neighbor and duplicate boundary

`Docs/researches/math_theorems.md:1682-1687` separately catalogs `THM-M-0233`, the argument
principle, with a zero-and-pole counting formula. It may support a future proof, but it is not this
root and contributes no intake or proof credit here.

`Docs/researches/math_theorems.md:1689-1694` separately catalogs `THM-M-0234` as `儒歇定理`, also
attributed to Eugène Rouché in 1862, with the gloss "stability of the number of zeros of functions."
This likely overlaps or duplicates the present family, but the records do not specify whether a
different variant was intended. The IDs remain separate authority records. A source reviewer and
integration scope reviewer must allocate exact propositions or correct the target set; workers may
not merge them or transfer evidence.

## Source gate

The provisional `H1` classification means only that a published, historically proved theorem
family and plausible source leads are known. H0 requires a lawful immutable edition, exact theorem
and incorporated definition locators, premise/transition/conclusion mapping, proof boundary,
translation policy, corrections and errata audit, dependent source IDs, and an identified
independent reviewer. No source is admitted to H0 by this intake.
