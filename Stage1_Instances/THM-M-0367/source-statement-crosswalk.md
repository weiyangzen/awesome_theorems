# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `L^p有界性定理`, attributes it only to
"many mathematicians", dates it to the twentieth century, and gives the gloss `各种算子的L^p有界性`
("Lp boundedness of various operators"). `Docs/Stage0_Blueprint.md` repeats that record and leaves
the exact definitions, hypotheses, proof, equivalent forms, axioms, and artifacts open. The
rev-5.6 manifest retains `已验证` solely as `source_status_untrusted`.

No author, operator, paper, book edition, theorem number, page, hypotheses, conclusion, proof
source, errata, or formal declaration is supplied. Consequently there is no primary-source claim
to crosswalk and no basis for `H0`. The current phrase is classified `H5` as ill-posed until it is
corrected to a source-identified proposition.

## Crosswalk

| Repository phrase | Missing mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "operators" | exact operator or source-defined family | definition on functions or a densely defined map | absent |
| `L^p` | measure spaces, value spaces, exponent and endpoint range | `Measure`, `Lp`, `MemLp`, exponent in `ENNReal` | generic APIs probed; parameters absent |
| "boundedness" | norm inequality, strong/weak type, extension, constant | eLpNorm inequality or concrete continuous linear map construction | conclusion absent |
| "various" | finite list, quantified class, or informal survey label | explicit indexed family and uniform hypotheses if genuinely quantified | absent |
| `已验证` | untrusted inventory label | no proposition or proof credit | explicitly rejected as evidence |

## Source work required

The next phase must first obtain a target correction or select an immutable primary/authoritative
source that uniquely identifies the intended operator theorem. It must record edition, theorem and
page, definitions, every assumption, endpoint and constant conventions, proof boundary, and errata,
then obtain independent review. A textbook chapter on operator theory or a paper proving a different
Lp estimate is not enough.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks generic types for `MeasureTheory.MemLp`, `MeasureTheory.Lp`, `MeasureTheory.eLpNorm`, and
`ContinuousLinearMap`. These show only that common encoding ingredients exist. No bounded name
search, API probe, or generic continuous-map fact can identify which source theorem was intended;
formal candidate discovery must wait for the exact statement and then run as its own immutable
anchor audit.
