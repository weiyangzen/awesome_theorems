# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `向量值不等式`, attributes it only to
"many mathematicians", dates it to the twentieth century, and states `向量值算子的有界性`
("boundedness of vector-valued operators"). `Docs/Stage0_Blueprint.md` repeats that gloss. The
rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`. None supplies an operator,
formula, domains, exponents, hypotheses, conclusion, named source, theorem/page, errata, or formal
artifact.

The neighboring maximal-function, weighted-norm, and extrapolation entries locate the broad
harmonic-analysis area but do not disambiguate this entry. Adjacency is not source evidence.

## Candidate source work

The statement/source audit must first identify which theorem family the inventory intended, then
inspect an immutable primary or authoritative source passage. It must record the edition or paper,
theorem/section and page, original operator and norm notation, all parameter ranges, constant
dependencies, assumptions, proof boundary, and errata. An independent reviewer must confirm that
mapping. No particular Fefferman-Stein, Marcinkiewicz-Zygmund, or Littlewood-Paley theorem is
accepted at intake merely because its usual name fits the broad gloss.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "operator" | one sublinear/linear operator or an indexed family | exact function or map, domain/codomain, algebraic and analytic hypotheses | absent; identity open |
| "vector-valued" | `ell^q` aggregation, square function, or Banach-valued function | index type, sequence norm or Banach space, measurability and summability | absent; encoding open |
| "boundedness" | strong `L^p`, weak type, or two-sided norm comparison | explicit norm inequality and quantified constant with dependencies | absent from source record |
| "many mathematicians" | no unique theorem attribution | pinpoint primary or authoritative source identity | unresolved |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Lp` infrastructure, continuous linear maps, and convolution and checks representative
declarations. They can encode parts of several candidate readings, but do not select an operator,
sequence norm, exponent range, or bound. A bounded repository/mathlib text search located only
general vector-valued analytic infrastructure and no declaration that can be credited as this
unspecified theorem. That negative search is not the exhaustive immutable anchor audit required
downstream.
