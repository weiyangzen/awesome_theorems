# Source-statement crosswalk

## Repository record and provenance

The retained source record is `Docs/researches/math_theorems.md:1801-1806`. It supplies exactly:

- title `哈代空间理论` ("Hardy space theory");
- attribution to Godfrey Hardy;
- year 1915;
- phrase `单位圆盘上的Hardy空间` ("Hardy spaces on the unit disk");
- importance "high"; and
- formalization status `已验证` ("verified").

All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no citation, theorem or page, verbatim
proposition, definition, hypotheses, conclusion, proof, correction record, or formal artifact.
Stage0 repeats the phrase at `Docs/Stage0_Blueprint.md:6923-6948` while leaving exact definitions
and premises, equivalent forms, proof path, axioms, and machine artifacts as `待补充` (to be
supplied). The manifest therefore preserves `已验证` only as `source_status_untrusted`.

## Statement-component crosswalk

| Repository component | Required mathematical source detail | Required Lean component | Intake disposition |
|---|---|---|---|
| "unit disk" | exact open disk, coordinate and boundary-circle conventions | `Complex.UnitDisc` or a checked equivalent set/subtype transport | family fixed; encoding open |
| "Hardy space" | exponent, analytic-function carrier, radial or boundary definition, equality, norm/quasinorm | concrete carrier/predicate and all structures | unresolved |
| radial means | integrand (`abs f` or a power), angular normalization, radius range, supremum/limit | `Real.circleAverage` or another exact integral expression with integrability obligations | absent from record |
| theorem conclusion | definition, completeness, boundary values, coefficients, evaluation bound, factorization, or another result | one binder-complete `Prop` or type | blocking: no conclusion exists |
| Godfrey Hardy / 1915 | exact publication and relationship to the modern `H^p` formulation | source provenance only | bibliographic lead found, mapping open |
| `已验证` | cited human and machine evidence | exact declaration, proof body, build and trust receipt | explicitly rejected as evidence |

## Bibliographic discovery lead

Crossref metadata for DOI `10.1112/plms/s2_14.1.269` identifies G. H. Hardy, "The Mean Value of
the Modulus of an Analytic Function," *Proceedings of the London Mathematical Society*, series 2,
volume 14, issue 1 (1915), pages 269-277. The author and date align with the catalog, and the title
makes it a credible historical lead for radial integral means.

Only bibliographic metadata was inspected. No lawful immutable article text, pinpoint theorem,
incorporated definitions, exact assumptions, proof boundary, corrections or errata, or independent
review was obtained. The catalog does not cite this paper, and the metadata does not show which
modern Hardy-space proposition the catalog intends. The lead is therefore `E5` discovery material,
not an accepted primary proof source or `H0` evidence.

## Pinned Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded exact-topic
search found no declaration named for a Hardy space. The discovery-only probe checks:

| Pinned declaration | What it authenticates | Why it is not the target |
|---|---|---|
| `Complex.UnitDisc` | the complex open-unit-disc subtype | supplies a possible domain only |
| `Complex.UnitDisc.norm_lt_one` | membership gives norm less than one | no analytic-function space or theorem |
| `AnalyticOnNhd` | a general analytic-on-a-set predicate | no radial integrability or Hardy bound |
| `Real.circleAverage` | normalized circle averaging | no exponent, supremum, or `H^p` carrier |
| `CircleIntegrable` | integrability on a circle | no uniform radial bound or boundary theorem |
| `DiffContOnCl.circleAverage` | a complex mean-value theorem on a disk | evaluates an analytic function at the center; it is not Hardy-space theory |

These checks establish only that adjacent pinned interfaces elaborate. The negative name search is
bounded intake discovery, not the immutable formal-anchor audit required downstream. No terminal
declaration or proof body is selected or credited.

## First blocker

Exact canonical-claim identity fails before Lean statement elaboration. A source reviewer must
select and independently approve one definition-complete proposition, including exponent range,
domain, analytic and measure conventions, binders, hypotheses, conclusion, constants, and boundary
cases. Until then the canonical statement and formal target remain null, the received catalog
wording remains provisionally `H5`, machine debt remains `M4`, and no proof or theorem-completion
claim is permitted.
