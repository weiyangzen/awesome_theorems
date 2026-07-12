# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives the Chinese title `描述集合论`, attributes it only to
"many mathematicians" in the twentieth century, and states `波兰空间上可定义集合的理论` ("the
theory of definable sets on Polish spaces"). Stage0 repeats this record. The rev-5.6 manifest
preserves `已验证` only as `source_status_untrusted`. None supplies a definition, theorem,
hypotheses, conclusion, proof source, edition, page, or formal artifact.

## Candidate source work

An authoritative monograph or primary paper must be selected at the source-audit phase. The audit
must record edition, theorem/definition number and page, hypotheses, proof boundary, and errata,
then receive independent review. Choosing a familiar theorem now would broaden the topic gloss into
an invented target, so no author or named theorem is assigned at intake.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Polish spaces" | separable completely metrizable topological spaces | `PolishSpace` with the exact topology/measurable context | pinned API probed; domain open |
| "definable sets" | Borel sets | `MeasurableSet` under `BorelSpace` | candidate only |
| "definable sets" | analytic/Suslin sets | `MeasureTheory.AnalyticSet` | candidate only |
| "theory" | closure, separation, characterization, regularity, hierarchy, or uniformization theorem | one concrete proposition with every hypothesis | absent from source record |
| `已验证` | untrusted inventory label | no Lean proposition or proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.MeasureTheory.Constructions.Polish.Basic` and checks `PolishSpace`,
`MeasureTheory.AnalyticSet`, analytic closure under continuous images, measurable-to-analytic
conversion, analytic separation, and the bi-analytic measurable-set result. These are candidate
encoding ingredients only. The similarly named projective-measure modules concern probability
projective limits, not descriptive-set-theoretic projective pointclasses.

