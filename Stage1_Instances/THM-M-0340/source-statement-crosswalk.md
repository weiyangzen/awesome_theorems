# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `巴拿赫-塔斯基分球悖论`, attributes it to
Stefan Banach and Alfred Tarski, gives the year 1924, and states `选择公理下的分球定理` ("the
ball-splitting theorem under the axiom of choice"). Stage0 repeats that gloss while leaving exact
definitions, premises, proof path, equivalent forms, axioms, and machine artifact open. The
rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`.

This is topic-level secondary metadata. It supplies no quoted statement, primary-source edition,
theorem/page locator, assumptions, errata, or formal declaration.

## Candidate primary-source work

The likely historical anchor is Banach and Tarski's 1924 paper *Sur la decomposition des ensembles
de points en parties respectivement congruentes*, *Fundamenta Mathematicae* 6. This bibliographic
lead is not accepted as an `H0` source crosswalk at intake: the later source audit must inspect an
immutable scan or edition, locate the exact theorem and pages, transcribe its domains and
congruence relation, record errata/translation decisions, and obtain independent review. Modern
ball/sphere and five-piece formulations must be separately crosswalked rather than attributed to
the original paper from memory.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "ball" | open/closed positive-radius ball in real `R^3` | `EuclideanSpace R (Fin 3)`, `Metric.ball` or `Metric.closedBall` | APIs probed; choice open |
| "ball" | boundary two-sphere | `Metric.sphere` | candidate only; not interchangeable |
| "splitting" | finite partition moved by congruences | `Equidecomp X G` for an exact acting group | generic API probed; action open |
| "two copies" | two disjoint congruent targets or tagged coproduct | exact target sets and checked representation bridge | absent |
| "under choice" | classical/choice foundation used in construction | explicit foundation and axiom audit | not frozen |
| "1924" | historical Banach-Tarski theorem family | immutable edition, theorem/page, assumptions, errata | bibliographic lead only |
| `已验证` | untrusted inventory label | no Lean proposition or proof credit | explicitly rejected |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded probe
imports the equidecomposition API and Euclidean geometry. It checks `Equidecomp`, its source and
target projections, `EuclideanSpace`, metric balls/spheres, and isometry types. The local name
search found the general equidecomposition infrastructure but no declaration named for the
Banach-Tarski theorem. This observation is only intake evidence and does not replace the later
immutable anchor audit.

