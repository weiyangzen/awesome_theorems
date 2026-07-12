# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10362-10367` supplies exactly the title `Lyapunov指数`, the
attribution Aleksandr Lyapunov, the year 1892, the gloss `轨道分离的指数率`, importance "high",
and status `已验证`. This six-line record was introduced by repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It contains no bibliography, stable source ID,
formula, definition, theorem statement, or proof.

`Docs/Stage0_Blueprint.md:38564-38589` repeats these fields and explicitly leaves the exact
definitions and premises, proof process, dependencies, equivalent forms, axioms, machine status,
and artifact links open. Its generic closed-result and leaf-audit boilerplate is planning metadata,
not source evidence. The rev-5.6 manifest carries `已验证` only as `source_status_untrusted` and
resets this target to `L0 / rework_required`.

## Crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `Lyapunov指数` | a family of asymptotic dynamical growth quantities | no single `Prop` follows from the name of an invariant | not a stable proposition |
| "orbit" | orbit of a map, flow, or cocycle base | phase type, time type, map/action/cocycle, base point, regularity, invariant scope | all open |
| "separation" | distance between two orbits or norm of a tangent/cocycle vector | metric or derivative/cocycle action, perturbation/direction, nonzero conditions | meaning open |
| "exponential rate" | logarithmic growth normalized by discrete or continuous time | log convention, norm/metric, denominator, limit/limsup/liminf, real or extended-real result | all open |
| Aleksandr Lyapunov / 1892 | historical attribution | source provenance only | no edition, work, theorem/page, assumptions, proof, or errata |
| `已验证` | untrusted inventory metadata | inspectable source proof and kernel receipt would be required | no H or M credit |

## Variant and neighbor boundary

A metric formula such as the rate of `dist ((f^[n]) x) ((f^[n]) y)` is not definitionally the
directional derivative-growth formula, and neither is the same statement as a cocycle spectrum.
Replacing an ordinary limit by a limsup changes existence content. A maximal pointwise exponent,
an almost-everywhere exponent, norm independence, invariance along an orbit, and existence of a
measurable splitting are separate claims with separate hypotheses.

The adjacent repository record `THM-M-1419` explicitly owns Oseledets' multiplicative ergodic
theorem and glosses it as existence of Lyapunov exponents. `THM-M-1420` owns Pesin theory and
`THM-M-1421` owns the entropy formula. A second Oseledets record, `THM-M-1056`, concerns random
matrix exponents. This separation rules out adopting one of those conclusions merely because it
would turn the received quantity label into a theorem.

## Source gate

Before an approved correction can leave `H5`, an accountable reviewer must identify and preserve
an immutable primary or authoritative source; select an exact theorem, definition-plus-property,
or other truth-valued passage and page/section; transcribe every definition, ordered binder,
hypothesis, conclusion, and exceptional case; check corrections and errata; and justify why that
proposition represents `THM-M-1418` rather than a neighboring target. A second reviewer must
approve the source-to-canonical-statement mapping.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded exact-name
search found no occurrence of "Lyapunov", "Liapunov", "Oseledets", "multiplicative ergodic", or
"linear cocycle" in Lean sources. Pinned APIs do include function-iterate notation and its
semiconjugacy laws, `dist`, `fderiv`, `HasFDerivAt`, `Real.log`, and `Filter.limsup`;
`IntakeProbe.lean` verifies representative names. They are discovery facts only, not a complete
formal-candidate audit and not evidence for a canonical target.

The canonical module, declaration or expression, elaborated expression hash, checked transports,
and statement mutations remain null. No H0, M0, or readable-proof closure is claimed.
