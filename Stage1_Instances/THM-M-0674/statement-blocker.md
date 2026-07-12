# Statement-phase blocker

Item: `S56-M-0674-STATEMENT`  
Base revision: `0cf4360f9f55c0e8ed28d6d7087b57409eb53cf5`

## First failed gate

The rev-5.6 exact-claim gate fails before Lean target selection. The authoritative repository source
for `THM-M-0674` says only "existence of saturated models". It supplies no quantified theorem,
saturation convention, cardinal, model-size conclusion, input model or theory, language-size
condition, or primary-source theorem/page. These omissions distinguish genuinely different standard
results, so choosing one would broaden or substitute the source rather than elaborate it exactly.

In particular, the title does not determine whether the intended claim is:

- a saturated elementary extension of every structure, with no prescribed output cardinality;
- a saturated model of a satisfiable or complete theory at an exact cardinal;
- unary saturation or realization of all tuples indexed by a type of cardinality `< kappa`;
- saturation over subsets of the carrier or over arbitrary parameter maps; or
- conditional on language bounds, regularity, or `kappa ^< kappa = kappa`.

The historical `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_300.lean` chooses the strongest
listed tuple convention, exact cardinality, and a small-power hypothesis. Its own `StatementShape`
has no proof body and the rev-5.6 intake correctly classifies it only as discovery input. It cannot
supply missing source authority.

## Pinned API inspection

The pinned dependency does contain enough primitives to encode a target after the mathematical
variant is fixed. `Mathlib.ModelTheory.Types` provides complete types and realized types;
`Mathlib.ModelTheory.ElementaryMaps` provides elementary embeddings; and
`Mathlib.ModelTheory.Satisfiability` provides satisfiability and bundled models. A scoped search found
no model-theoretic saturated-model predicate or terminal existence theorem in pinned mathlib. That
search is only a feasibility check, not anchor-audit or proof credit.

Because no exact canonical proposition exists, there is no truthful minimal import: an
elementary-extension target needs `Mathlib.ModelTheory.ElementaryMaps`, whereas the legacy
exact-cardinality theory target can elaborate from the type/satisfiability APIs. Likewise, the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations have no
canonical expression against which to be tested. No `Statement.lean`, expression hash, checked
transport, statement receipt, or `[_]` self-test claim is emitted.

## Validation performed

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure valid; 15 assurance groups and 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Manifest valid; 1546 unique targets with ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0674` | 0 | Rank 300; planned, L0/rework-required, theorem-complete false. |
| `rg -n 'IsSaturated|Saturated|saturated' Formalizations/Lean/.lake/packages/mathlib/Mathlib/ModelTheory` | 1 | No model-theoretic saturation declaration in the pinned mathlib source tree. |
| `git diff --check -- Stage1_Instances/THM-M-0674` | 0 | No whitespace errors after this artifact was added. |

No `lake update`, `lake build`, clone, fetch, or `.lake` mutation was performed. A Lean invocation
would only elaborate a substituted candidate, not the exact target required by this item.

## Retry condition

Inspect and freeze a stable primary-source edition, theorem number/page, definition of saturation,
all hypotheses, and exact conclusion. Then encode precisely that variant, determine its minimal
pinned import by removal tests, serialize its elaborated expression and environment fingerprint,
and run all four required statement mutations. Until that input exists, the truthful verdict is
`blocked`; lifecycle remains `planned`, root machine debt remains `M4`, and theorem completion is
false.
