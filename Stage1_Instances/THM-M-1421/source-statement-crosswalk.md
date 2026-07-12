# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:10383` records `Pesin熵公式`, Yakov Pesin, 1977, and only
`熵与Lyapunov指数` ("entropy and Lyapunov exponents"). It supplies no formula, definitions,
hypotheses, theorem/page locator, proof, errata, or formal artifact. `Docs/Stage0_Blueprint.md:38645`
repeats those fields and explicitly leaves the exact premises, proof route, dependencies,
equivalent forms, axioms, and machine status open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

## Primary-source candidate

The leading candidate is Ya. B. Pesin, *Characteristic Lyapunov Exponents and Smooth Ergodic
Theory*, **Russian Mathematical Surveys** 32(4) (1977), 55-114, DOI
`10.1070/RM1977v032n04ABEH001639`, Math-Net `rm3219`. The official English PDF was inspected on
2026-07-12; its observed SHA-256 was
`ea326f02cf721c59a27582d329acbffaba7fb844a8e13b89d2fb4291ffb0f35b`.

Section 5, Theorem 5.1 (printed page 81, equation (5.0)) considers a `C^2` diffeomorphism preserving
the standing measure. With distinct forward characteristic exponents arranged increasingly and
`q_i(x)` their multiplicities, it states entropy as minus the integral of the negative exponents,
counted with multiplicity; when there are no negative values, the empty sum is zero. Section 1.1's
standing setup uses a compact smooth Riemannian manifold and a normalized smooth measure compatible
with, in the paper's words equivalent to, Riemannian volume. Section 1.6 describes the result using
the sum of positive characteristic Lyapunov exponents.

This is strong discovery evidence, not `H0`. An immutable archival edition and exact translation
must be approved; all referenced definitions and assumptions must be transcribed; the apparent
positive/negative formulation bridge and entropy convention must be proved; corrections and errata
must be checked; every proof boundary must be mapped; and an independent reviewer must approve the
crosswalk. Modern variants with different regularity or measure hypotheses cannot be folded into
the 1977 theorem without separate source and transport evidence.

## Crosswalk

| Source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| `C^2` diffeomorphism of `M` | compact smooth Riemannian manifold, invertible discrete dynamics, regularity | manifold model, `ContMDiff`/diffeomorphism data, tangent derivative cocycle | generic `mfderiv` substrate probed; exact system open |
| preserves normalized smooth `nu` | invariant probability measure and its equivalence to Riemannian volume | concrete measure, probability/regularity predicates, `MeasurePreserving` | generic preservation API probed; source measure interface open |
| entropy `h(f)` | exact metric/Kolmogorov-Sinai entropy and logarithm/value conventions | measurable partitions, partition entropy, iterated joins, supremum interface | absent from probed target APIs; topological `coverEntropy` is explicitly nonmatching |
| characteristic exponents | derivative-cocycle limits on a common conull set | tangent cocycle, Oseledets spectrum, measurability and integrability | no exact pinned interface located at intake |
| `q_i(x)` | point-dependent multiplicity of each distinct exponent | measurable finite indexing/rank and summability | `Finset.sum` only is generic substrate |
| negative-sum equation (5.0) | minus integral of negative forward exponents; empty sum zero | measurable/integrable exponent sum and exact equality | formula candidate inspected; not frozen |
| positive-exponent paraphrase | inverse/time-reversal/sign relation and entropy invariance | checked equivalence or implication declarations | no witness; not credited as alternate encoding |
| `已验证` | untrusted inventory metadata | no Lean declaration or proof component | explicitly rejected as evidence |

## Lean boundary

The pinned environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. `IntakeProbe.lean` checks representative
measure-preserving, topological-entropy, manifold-derivative, integration, and finite-sum APIs. A
bounded pinned-source search found no Pesin, Lyapunov, Oseledets, metric-entropy, or
measure-theoretic-entropy target name. This negative result is intake discovery only, not an
exhaustive formal-candidate audit.

Before statement credit, a formal reviewer must approve one exact source-faithful Lean expression,
its environment fingerprint, checked transports, and mutations covering removed hypotheses,
domain, binder scope, and boundary cases. Until then the root remains `H1/M4`, and no proof search
or completion claim is legal.
