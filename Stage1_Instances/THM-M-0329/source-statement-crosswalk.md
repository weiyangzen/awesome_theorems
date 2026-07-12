# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names the Lax-Milgram theorem, attributes it to Peter Lax and
Arthur Milgram, gives the year 1954, and supplies only `变分问题的解的存在唯一性` ("existence and
uniqueness of the solution of a variational problem"). Stage0 repeats that gloss while leaving
exact definitions, assumptions, proof route, axioms, and artifacts open. The manifest retains
`已验证` only as `source_status_untrusted`; it supplies no proof credit.

## Human-source candidate

Peter D. Lax and Arthur N. Milgram, "Parabolic equations", in *Contributions to the Theory of
Partial Differential Equations*, Annals of Mathematics Studies 33, Princeton University Press
(1954), pp. 167-190, is the primary-source candidate. This bibliographic locator has not yet been
inspected at theorem/page granularity, checked for the exact assumptions and notation, or reviewed
for errata. It therefore supports `H1`, not `H0`. The statement phase must record the precise
result/page and a clause-by-clause assumption crosswalk before freezing the human claim.

## Crosswalk

| Repository/source concept | Mathematical content to freeze | Candidate Lean component | Intake status |
|---|---|---|---|
| variational space | real or complex Hilbert space, completeness | `InnerProductSpace ℝ V`, `CompleteSpace V` | real candidate probed; source open |
| bounded bilinear form | continuity and argument order | `V →L[ℝ] V →L[ℝ] ℝ` | candidate probed |
| coercivity | positive constant and diagonal lower bound | `IsCoercive B` | exact pinned definition probed |
| right-hand side | continuous functional or Riesz vector | `continuousLinearMapOfBilin`-based representation | encoding choice open |
| existence | a solution for each datum | `IsCoercive.continuousLinearEquivOfBilin` and application lemma | candidate only |
| uniqueness | unique vector satisfying the variational equality | `IsCoercive.unique_continuousLinearEquivOfBilin` | candidate only |
| stability/isomorphism | bounded solution operator, if included by source | `V ≃L[ℝ] V` | stronger packaging; source mapping open |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.InnerProductSpace.LaxMilgram` explicitly presents a real-Hilbert-space
Lax-Milgram formulation. The intake probe checks the coercivity predicate and three public
declarations. This confirms that a credible formal candidate exists in the pinned closure, so the
machine status is not `M4`. It does not establish exact statement identity, terminal provenance,
axiom policy, or `M0-W`; those belong to later statement and anchor-audit phases.

Mathlib's module documentation cites Peter Howard's Spring 2020 PDE notes as the proof route and
also depends on the Riesz-representation API. Those are discovery facts, not a completed human
source crosswalk.
