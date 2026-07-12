# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `restriction theorem`, attributes it to Elias
Stein, gives the year 1986, and provides only the gloss "restriction of the Fourier transform to a
surface". Stage0 repeats these fields. The rev-5.6 manifest preserves the source's `verified` label
only as `source_status_untrusted`. None supplies a bibliographic work, edition, theorem number,
page, surface, dimension, hypotheses, conclusion, proof, errata, or formal artifact.

The next source entry is a distinct "Fourier restriction conjecture", attributed to Stein in 1979,
with the same gloss and status "partially solved". This adjacency is repository evidence that the
short gloss is not sufficient to decide whether THM-M-0375 means the Stein-Tomas theorem, some
other proved range, or a generic topic label. It is not evidence for any particular proposition.

## Candidate source work

The Stein-Tomas sphere restriction theorem is a plausible candidate because it is a central proved
restriction result, but it is not accepted as the canonical claim at intake. A later source audit
must locate the intended primary or authoritative source at an immutable edition, record the exact
theorem/page and normalization, map every assumption and endpoint, check errata, and obtain
independent source review. The unexplained year 1986 must be reconciled rather than silently used to
name a theorem.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Fourier transform" | Euclidean Fourier transform with a fixed phase and measure normalization | `VectorFourier.fourierIntegral` or `FourierTransform.fourier` plus a concrete pairing | pinned API probed; convention open |
| "surface" | sphere or a source-specified hypersurface | subtype/set, parametrization or level set, measurability, and surface measure | `Metric.sphere` and `Measure.toSphere` probed; intended surface open |
| "restriction" | trace/restriction of a transform, often defined first on a dense test class | representative policy, coercion/restriction map, density and extension interface | theorem-level interface absent |
| norm estimate | an `Lp -> Lq` bound with exact exponents and constant dependence | `eLpNorm`, measures, exponents, and a quantified inequality | ingredients probed; conclusion absent |
| extension form | adjoint surface extension estimate | integral operator and a checked duality bridge | alternate only; not frozen |
| `verified` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports Fourier-transform, sphere-measure, and `Lp`-seminorm modules. It checks seven relevant
definitions. This establishes only that candidate statement ingredients elaborate. The local name
search found Fourier infrastructure but no source-identified restriction theorem; a complete anchor
audit is a downstream task and no absence claim about all external Lean projects is made.

