# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10539-10544` supplies exactly the title `不动点迭代`, the
attribution `众多数学家`, the period `20世纪`, the gloss `方程求根的迭代方法`, importance
"high," and status `已验证`. All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, stable source
identifier, equation, definition, quantified theorem, assumptions, proof, errata, or formal
artifact.

`Docs/Stage0_Blueprint.md:39244-39269` repeats these fields and explicitly leaves exact definitions
and premises, proof process, dependencies, equivalent forms, axioms, machine status, and artifact
links as `待补充`. Its generic closed-result and leaf-audit text is generated planning metadata,
not source evidence. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `方程求根` (finding equation roots) | solve `F(x) = 0` | types, `F`, domain, equality or residual predicate | all unspecified |
| `不动点` (fixed point) | solve `g(x) = x` | self-map `g`, `Function.IsFixedPt`, and a checked root/fixed-point bridge | map and bridge absent |
| `迭代` (iteration) | recurrence `x_(n+1) = g(x_n)` | `Function.iterate`, initial point, indexing, invariant-domain proof | only method shape implied |
| `方法` (method) | algorithm or proof technique | one truth-valued correctness/convergence proposition | no conclusion supplied |
| `已验证` | untrusted screening label | accepted source and kernel receipts | no credit |

The literal wording therefore cannot populate the canonical domain, ordered quantifiers,
hypotheses, conclusion, alternate encodings, degenerate cases, or expression fingerprint required
by the rev-5.6 intake contract.

## Candidate statements and collision boundary

Pinned mathlib contains at least two materially different formal candidates:

| Candidate | Exact pinned anchor | What it states | Why it is not selected |
|---|---|---|---|
| limit transfer | `Mathlib.Dynamics.FixedPoints.Topology.isFixedPt_of_tendsto_iterate` | convergence of `g^[n] x` plus continuity at the limit implies that the limit is fixed | assumes convergence; gives no root bridge, existence, rate, or solver correctness |
| contraction/Picard iteration | `Mathlib.Topology.MetricSpace.Contracting.ContractingWith.exists_fixedPoint` and `ContractingWith.tendsto_iterate_fixedPoint` | under complete-space and contraction hypotheses, iterates converge to a fixed point, with existence and error estimates | the catalog states none of these hypotheses or conclusions, and adjacent target `THM-M-1444` separately owns Banach's theorem |

The repository also has separate nearby targets for Newton, secant, and bisection methods. Their
adjacency confirms that "root-finding iterative method" is not permission to borrow any convenient
root-finding theorem. Candidate names and matching vocabulary are E3/E5 discovery evidence at
best; they cannot establish statement identity.

## Source gate and retry condition

No primary mathematical source is identified. The first downstream gate is an accountable target
correction that cites an immutable edition and theorem/page, selects one exact truth-valued claim,
maps every equation, binder, premise, conclusion and boundary case, audits errata, explains its
relationship to `THM-M-1444`, and receives independent source review. Only then may the statement
phase freeze a Lean expression and test transports and mutations.

Until that correction exists, `H5` describes the catalog target's ill-posed proposition status,
`M4` records the absence of a source-identical usable formal artifact, and `R4` records the absence
of an anchorable proof reconstruction. These classifications do not say that standard fixed-point
iteration results are false or mathematically open.

## Lean discovery boundary

`IntakeProbe.lean` imports the two minimal public mathlib modules needed to check the iteration,
fixed-point, continuity-at-limit, contraction, convergence, and error-bound candidates. It does not
declare a theorem or encode a root equation. Passing elaboration authenticates those adjacent APIs
at the pinned toolchain only; it provides no canonical statement, source fidelity, proof-body
credit, or completion evidence for `THM-M-1443`.
