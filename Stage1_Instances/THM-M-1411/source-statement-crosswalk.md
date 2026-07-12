# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10313-10318` supplies exactly the title `双曲动力系统`, the
attribution "many mathematicians," the period "twentieth century," the gloss `双曲性的理论`,
importance "high," and status `已验证`. The six-line record was introduced by repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; it contains no citation or theorem statement.

`Docs/Stage0_Blueprint.md:38375-38400` repeats the same gloss and explicitly leaves exact
definitions and premises, the proof process, dependencies, equivalent forms, axioms, machine
status, and artifact links to be supplied. The rev-5.6 manifest carries `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

## Crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `双曲动力系统` | a broad field including local, uniform, partial, and nonuniform hyperbolicity | no single declaration follows from a field name | not a stable proposition |
| "dynamical system" | a discrete self-map/diffeomorphism, flow, group action, or cocycle | phase type, structures, time domain, map/action, regularity, invariant set | all open |
| "hyperbolicity" | derivative spectral condition or invariant contracting/expanding splitting | tangent or vector bundle, derivative/cocycle, subbundles, norms, constants, iterate inequalities | meaning and scope open |
| "theory" | definitions plus many possible theorems and consequences | one exact `Prop` with ordered binders, hypotheses, and conclusion | no truth-valued conclusion supplied |
| many mathematicians / twentieth century | very broad historical context | provenance documentation only | no edition, stable ID, theorem, page, assumptions, proof, or errata |
| `已验证` | untrusted inventory metadata | inspectable source proof and kernel receipt would be required | no H or M credit |

## Neighbor and variant boundary

The adjacent repository records separately name Anosov diffeomorphisms, Axiom A, spectral
decomposition, Markov partitions, hyperbolic-system measures, Lyapunov exponents, Oseledets'
theorem, and Pesin theory. Other catalog targets own Hartman-Grobman, stable manifolds, the Smale
horseshoe, and structural stability. This separation is affirmative evidence that no one familiar
member of that family may be chosen merely because it is convenient to state in Lean.

## Source gate

Before an approved correction can leave `H5`, an accountable reviewer must identify and preserve
an immutable primary or authoritative source, select an exact theorem and page/section, transcribe
every definition, ordered binder, hypothesis, conclusion, and exceptional case, check corrections
and errata, and justify why that proposition represents `THM-M-1411` rather than a neighboring
target. A second reviewer must approve the source-to-canonical-statement mapping.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded exact-topic
name search under `Mathlib/Dynamics` found no occurrences of "hyperbolic dynamics," "hyperbolic
dynamical," "hyperbolicity," "uniformly hyperbolic," "Anosov," or "Axiom A." Pinned APIs do
include `IsInvariant`, `Flow`, `Function.IsPeriodicPt`, `mfderiv`, and `tangentMap`; an unrelated
`Matrix.IsHyperbolic` concerns the discriminant of a two-by-two matrix. These are discovery facts
only, not a complete formal-candidate audit and not evidence for a canonical target.

The canonical module, declaration or expression, normalized expression hash, checked transports,
and statement mutations remain null. No H0, M0, or readable-proof closure is claimed.
