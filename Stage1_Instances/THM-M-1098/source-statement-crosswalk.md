# Source-statement crosswalk

## Repository source boundary

`Docs/researches/math_theorems.md` gives only the authors "Meyn/Tweedie", the year 1993, and the
phrase "a stability condition for Markov chains". `Docs/Stage0_Blueprint.md` repeats that phrase
while leaving definitions, assumptions, proof route, axioms, and formal artifacts unspecified. The
rev-5.6 manifest marks its `已验证` source status as untrusted. These records establish the intended
topic but do not identify a theorem.

## Candidate primary source

- Sean P. Meyn and Richard L. Tweedie, *Markov Chains and Stochastic Stability*, Springer-Verlag,
  1993 (first edition). This monograph matches the repository authors and date and is the primary
  source candidate for the drift/stability family. The exact chapter, theorem number, page,
  referenced definitions, edition wording, corrections, and errata have not been inspected here.

The second edition (Cambridge University Press, 2009) may be consulted to identify corrections, but
it may not silently replace the 1993 attribution. This bibliographic anchor is discovery evidence,
not `H0`; statement freeze requires an inspected, stable edition and an independent source review.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Markov chain" | general-state-space transition law | measurable space, Markov kernel, and required iterates | included; exact model open |
| "drift" | expected one-step change of a Lyapunov function | kernel integral defining `PV` and a pointwise inequality | family identified; exact operator open |
| "condition" | negative drift outside a controlled set | quantified constants, function bounds, and indicator/set split | exact inequality open |
| controlled set | small or petite set in the source sense | concrete minorization or sampled-kernel predicate | predicate and witnesses open |
| "stability" | recurrence, invariant measure, moment bound, or convergence | one exact predicate or quantified estimate | ambiguous; exact conclusion open |
| Meyn/Tweedie, 1993 | monograph theorem and definitions | source IDs attached to target binders and hypotheses | candidate only; locator open |
| `已验证` | repository screening label | accepted source review or kernel receipt | no credit |

## Non-equivalent candidate shapes

An additive inequality such as `PV <= V - f + b * 1_C` can support recurrence and invariant-measure
conclusions under appropriate source hypotheses. A geometric inequality such as
`PV <= lambda * V + b * 1_C`, with `lambda < 1`, can support stronger rate conclusions under
additional irreducibility, aperiodicity, and set assumptions. These schematic formulas only explain
the ambiguity; neither is the canonical statement, and no conclusion is inferred from them here.

## Required source and machine audit

Before `H0`, an independent reviewer must record the selected edition, theorem/page, every imported
definition and premise, correction status, and a row-by-row map to the exact Lean expression. The
review must distinguish small from petite sets, recurrence from positive Harris recurrence,
existence from uniqueness of an invariant law, and qualitative convergence from geometric or
subgeometric bounds.

No repo-local or external Lean declaration is credited at intake. The anchor-audit phase must search
the pinned mathlib revision and credible Lean 4 projects and record exact module/declaration types,
immutable revisions, proof-body provenance, placeholders, axioms, and dependency feasibility. A
name search or adjacent Markov-kernel API is not evidence that this theorem is formalized.
