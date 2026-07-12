# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9999-10004` supplies exactly the title `Nekhoroshev estimate`,
Nikolai Nekhoroshev, 1977, the gloss `exponential stability of nearly integrable systems`, high
importance, and status `verified`. Git provenance places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, equation, theorem or
page locator, definition, binder, assumption, conclusion, proof boundary, erratum, reviewer, or
formal artifact.

`Docs/Stage0_Blueprint.md:37317-37342` repeats the gloss while explicitly leaving the formal
system, foundation, precise definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. Its generic planning sentence about a known closed
result is not source evidence. The rev-5.6 manifest retains `verified` only as untrusted metadata
and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Catalog element | Necessary mathematical component | Prospective Lean component | Intake result |
|---|---|---|---|
| nearly integrable system | an exact Hamiltonian split, phase space, canonical equations, domains, and perturbation norm | finite-dimensional coordinate model, functions, derivatives, and integral curves | all choices absent |
| stability | a quantified action drift bound for every allowed solution and initial condition | norm inequality over a selected trajectory predicate | variables, norm, radius, and quantifiers absent |
| exponential | an explicit lower time scale and positive exponent with constant dependencies | `Real.exp`, `Real.rpow`, inequalities, and source-matched constants | formula and exponent absent |
| Nikolai Nekhoroshev / 1977 | historical attribution | source provenance only | strong primary lead located, not selected by catalog |
| verified | untrusted inventory field | accepted source review and kernel receipt would be required | no H0 or M credit |

The noun phrase does not say whether the intended nondegeneracy is steepness or quasi-convexity,
whether regularity is analytic or weaker, or which of several incompatible radius/time estimates is
the conclusion.

## Primary source lead

N. N. Nekhoroshev, *An exponential estimate of the time of stability of nearly-integrable
Hamiltonian systems*, Russian Mathematical Surveys **32**:6 (1977), 1-65, translated from Uspekhi
Mat. Nauk 32:6, 5-66, DOI `10.1070/RM1977v032n06ABEH003859`, MathNet record `rm3304`, was
inspected as the historically matching primary source. The 65-page English PDF observed during
intake had SHA-256
`0bfe624cf108096badd7e27fc40ca800e2948b68dce2bf8b9c653e0eaec4def6`.

| Locator | Source component | Prospective target component | Intake disposition |
|---|---|---|---|
| Section 1.4, printed p.4 | an introductory exponential estimate | human orientation only | source expressly says it is not completely accurate and differs from Theorem 4.4 |
| Sections 1.7 and 4.1, pp.6-8 and 28-29 | steepness, coefficients, indices, and the derived quantity `zeta` | a substantial source-specific nondegeneracy definition stack | definitions not yet transcribed or reviewed |
| Section 4.3, p.29 | analytic complex domain, real-valued Hamiltonian, bounded Hessian, and canonical equations for `H = H0 + H1` | domains, analyticity, Hamiltonian dynamics, and environment choices | major formal infrastructure and exact mapping remain open |
| Theorem 4.4, p.30 | for sufficiently small positive `M = sup_F |grad H1|`, every allowed real solution has action drift `< d/2` through `min(C,T)`, where `d=M^b` and `T=M^-1 exp((1/M)^a)` with source-defined positive exponents | the plausible primary root | not selected by catalog; complete binders and dependencies are not frozen |
| Remark 4.5, p.30 | `sup_F |H1|` may replace the gradient norm; `M0` dependence is delimited | alternate encoding/statement relationship and constant policy | proposition-changing option still open |

The paper's opening note says proofs of technical lemmas used by the main theorem were to appear
elsewhere, and that those proofs together with Sections 5-9 make the proof complete. The sequel is
Nekhoroshev, *An exponential estimate ... II*, Trudy Seminara imeni I. G. Petrovskogo 5 (1979),
5-50; an English version later appeared in *Topics in Modern Mathematics* (1985), 1-58, DOI
`10.1007/978-1-4684-1653-4_1`. An H0 record must bind both parts, identify the exact lemma-to-root
proof boundary, audit corrections and translation, and receive independent review. Intake does not
claim that work has been done.

## Modern variant discriminators

J. Poeschel, *Nekhoroshev estimates for quasi-convex Hamiltonian systems*, Mathematische
Zeitschrift 213 (1993), 187-216, DOI `10.1007/BF03025718`, is a standard quasi-convex variant.
It is not interchangeable with the original general steep theorem.

Abed Bounemoura and Jean-Pierre Marco, *Improved exponential stability for near-integrable
quasi-convex Hamiltonians*, Nonlinearity 24 (2011), 97-112, DOI
`10.1088/0951-7715/24/1/005`, arXiv `1004.1014v2`, was inspected as an open modern
discriminator. Its PDF had SHA-256
`90f0f6b3b3b183b8898f4e961f0127b3a143453f76645d960d3095fda5b9b818`. Theorem 2.1 fixes an
analytic complex strip, strict quasi-convexity, third-derivative bounds, initial actions in a half
ball, and a parameterized improved radius/time tradeoff. This is not the same contract as the 1977
steep theorem.

Abed Bounemoura, *Nekhoroshev estimates for finitely differentiable quasi-convex Hamiltonians*,
Journal of Differential Equations 249 (2010), 2905-2920, DOI `10.1016/j.jde.2010.06.004`,
arXiv `1002.1804v2`, was also inspected. Its PDF had SHA-256
`2c1d5fdcb35662a67cd1f1f4098df0aa2f5168a70fb56f640175a177b1fda768`. Theorem 2.1 assumes
`C^k`, `k >= 3`, and quasi-convexity, and gives polynomial time rather than exponential time. It
demonstrates that the missing regularity field changes the theorem materially.

These records support `H1` source reconstruction, not H0. No immutable accepted source packet,
complete premise/proof/errata map, or independent source review exists.

## Duplicate boundary

`Docs/researches/physics_theorems.md:6621-6627` and `Docs/Stage0_Blueprint.md:66610-66637`
contain `THM-P-0775`, a physics-catalog record saying that actions in a nearly integrable system
remain stable for exponentially long times. It is absent from `Docs/Stage1_Targets_rev-5.6.json`
and the applicable-target list. Its stronger wording still omits the model and theorem contract.
Without a master-owned alias/deduplication decision it cannot select the `THM-M-1372` root or
transfer source, machine, or readability credit.

## Source and formal gates

Before leaving `H1`, an accountable domain reviewer must select one immutable exact proposition,
justify it against the catalog and duplicate, record the edition and pinpoint locators, incorporate
every definition and assumption, bind the complete proof and correction boundary, and obtain an
independent source review. Only then may the statement phase freeze ordered binders, a canonical
Lean expression, minimal imports, checked transports, expression/environment fingerprints, and
mutations.

At the pinned mathlib revision, `IntakeProbe.lean` elaborates only generic analytic-function, ODE,
flow, real-power, and exponential interfaces. A bounded exact-topic search found no Nekhoroshev
declaration in pinned mathlib or repo-local Lean. The later immutable candidate audit remains open;
no formal absence theorem, proof body, audit completion, or theorem completion is claimed.
