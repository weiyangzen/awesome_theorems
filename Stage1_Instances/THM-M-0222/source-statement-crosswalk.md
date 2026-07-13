# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1605-1610` supplies exactly the title `柯西积分公式`, Augustin
Cauchy, 1831, the gloss `全纯函数由边界值表示`, importance "high," and status `已验证`. Git blame
attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, formula,
domain, contour, ordered binder, hypothesis, conclusion, proof boundary, correction history, or
formal artifact.

`Docs/Stage0_Blueprint.md:6167-6192` repeats the gloss and explicitly leaves the target formal
system, logical foundation, precise definitions and premises, proof route, dependencies,
equivalent forms, axioms, machine status, and artifact links open. Its generic planning language
about a known closed result is not source evidence. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Authoritative modern source lead

NIST Digital Library of Mathematical Functions version 1.2.7 (release 2026-06-15), section
1.9(iii), paragraph "Cauchy's Integral Formula," was inspected on 2026-07-13. Equation 1.9.E30
states that if a scalar complex function is continuous within and on a simple closed contour `C`,
analytic within `C`, and `z0` is inside, then

```text
f(z0) = (1 / (2 * pi * i)) * integral_C f(z) / (z - z0) dz.
```

The same section requires positive anticlockwise orientation and equation 1.9.E31 gives the
higher-derivative formula. These stable locators are strong evidence for the conventional modern
family and clarify the catalog's boundary-value gloss. They do not establish that this is the
catalog's intended edition or exact 1831 result, do not provide a historical definition and
translation audit, and have not received independent review. They therefore support only an `H1`
source lead, not `H0`.

## Literal crosswalk

| Repository element | Mathematical decision required | Prospective Lean component | Intake result |
|---|---|---|---|
| `柯西积分公式` | choose value formula and whether derivative extensions belong to the root | one exact `Prop`; derivative formulas separate unless source includes them | classical family recognized; exact root open |
| "holomorphic function" | scalar or Banach-valued codomain; domain and regularity convention | `f : Complex -> E`, `CompleteSpace E`, `DiffContOnCl`, `DifferentiableOn`, or explicit continuity/differentiability | pinned candidates exist; source choice open |
| "boundary values" | circle or contour, orientation, parametrization, and winding convention | `circleIntegral`, a future contour API, or checked transport | DLMF selects a positive simple contour; catalog does not |
| "represented" | normalized or unnormalized equality and Cauchy-kernel convention | inverse scalar action or equality to `(2 * pi * I) • f w` | equivalent mathlib forms checked as APIs; no canonical encoding |
| interior value | center or arbitrary interior point, including boundary/outside exclusions | `w : Complex` and `w ∈ ball c R` for circle candidates | catalog omits all binders and cases |
| Cauchy / 1831 | historical attribution and genealogy | immutable primary edition and pinpoint passage | catalog attribution only; historical audit open |
| `已验证` | untrusted inventory label | accepted source, kernel, trust, and receipt evidence would be required | no H0 or M0 credit |

## Pinned Lean candidate crosswalk

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

| Candidate declaration | Checked role | Unresolved source boundary |
|---|---|---|
| `Complex.two_pi_I_inv_smul_circleIntegral_sub_inv_smul_of_differentiable_on_off_countable` | normalized Banach-valued circle formula with closed-ball continuity and differentiability off a countable set | broader codomain and weaker regularity than the DLMF lead; source identity and exact target open |
| `Complex.circleIntegral_sub_inv_smul_of_differentiable_on_off_countable` | equivalent unnormalized Banach-valued circle formula | same boundary plus normalization choice |
| `DiffContOnCl.two_pi_i_inv_smul_circleIntegral_sub_inv_smul` | normalized wrapper for differentiability on an open disk and continuity on its closure | circle rather than the DLMF simple-contour presentation |
| `DifferentiableOn.circleIntegral_sub_inv_smul` | concise closed-ball differentiability wrapper | stronger regularity than some classical forms; unnormalized conclusion |
| `Complex.circleIntegral_div_sub_of_differentiable_on_off_countable` | scalar division form closest in integrand shape to the modern formula | still a circle and off-countable formulation |
| `AwesomeTheorems.Stage1.S1_M_178.cauchy_integral_formula_anchor` | repo-local wrapper around the pinned closed-ball theorem | belongs to `THM-M-1559`; no ownership, statement, or proof credit transfers |

`IntakeProbe.lean` authenticates representative pinned declarations and reports their current
axioms as `propext`, `Classical.choice`, and `Quot.sound`. This does not audit terminal proof-body
provenance, full dependency and trust closure, license/SBOM, or an exact source-to-Lean transport.
Those belong to the dependent statement and anchor-audit nodes.

## Source and statement gates

Before `H0`, an accountable reviewer must preserve a lawful immutable primary or authoritative
source, select the exact theorem and incorporated definitions, record edition/section/page or
stable equation locators, map every binder, assumption, conclusion and exceptional case, audit the
1831 attribution, translations, corrections and errata, and obtain independent review.

The statement phase must then choose minimal imports, elaborate one exact Lean expression, record
its normalized expression and environment fingerprints, compile every required circle/contour,
scalar/Banach, normalization, and regularity transport, and mutation-test a removed hypothesis,
changed domain, changed binder scope, and boundary case. Until then the canonical statement,
formal target, obligation registry, proof tree, and all proof credit remain open.
