# Source-statement crosswalk

## Repository sources inspected

`Docs/researches/math_theorems.md:9747-9752` is the complete repository research record. It gives
the title `比较定理`, proposer "many mathematicians," time "twentieth century," gloss
`微分不等式与解的比较`, importance "high," and status `已验证`. Git history traces all six
uncited lines to repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. That is repository
provenance, not an immutable mathematical source.

`Docs/Stage0_Blueprint.md:36345-36370` repeats the same metadata while explicitly leaving the
background, precise definitions and premises, proof process and date, dependencies, equivalent
forms, axioms, machine status, and artifact links open. The rev-5.6 manifest carries `已验证` only
in `source_status_untrusted` and resets the target to `L0 / rework_required`.

The source generator assigns theorem IDs from parse order, while the Stage1 generator copies the
catalog fields and mechanically computes the ODE profile's score and lane. Thus `THM-M-1336`, rank
947, and score 108 are stable repository identities or scheduling metadata, not theorem locators or
additional statement content.

A repository-wide bounded search found no other source statement or target-owned artifact for
`THM-M-1336`. No primary textbook or paper edition, theorem number, page, assumption list, errata
record, proof boundary, translation, or reviewer is identified.

## Crosswalk

| Repository phrase | Possible mathematical component | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `比较定理` | a theorem that propagates an order or bound | a future declaration after source selection | generic family name, not a proposition |
| "differential inequalities" | an inequality between derivatives, Dini derivatives, vector fields, or integrals | `HasDerivWithinAt`, slopes, integral inequalities, or a source-selected interface | derivative notion and inequality direction absent |
| "solutions" | exact ODE solutions, sub/supersolutions, or comparison functions | functions plus an ODE/integral-curve predicate | state space, vector field, interval, and solution notion absent |
| "comparison" | pointwise order, strict separation, non-crossing, or quantitative distance bound | `f t ≤ g t`, `f t < g t`, or a norm/distance inequality | exact conclusion absent |
| "many mathematicians, twentieth century" | historical topic marker | immutable primary edition and pinpoint locator required | no bibliographic identity or theorem locator supplied |
| `已验证` | catalog classification | no Lean proposition or proof object | explicitly rejected as evidence |

## Pinned Lean candidates not credited

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `Mathlib.Analysis.Calculus.MeanValue.image_le_of_deriv_right_le_deriv_boundary` compares
  continuous scalar functions on `[a,b]` using initial order, right-derivative witnesses, and a
  global weak derivative inequality.
- The same module also exposes strict first-contact and liminf-slope variants with different
  hypotheses.
- `Mathlib.Analysis.ODE.Gronwall.dist_le_of_approx_trajectories_ODE` compares approximate
  trajectories quantitatively under a Lipschitz vector field.
- `Mathlib.Analysis.ODE.Gronwall.dist_le_of_trajectories_ODE` compares exact trajectories by an
  exponential distance bound.
- `le_gronwallBound_of_liminf_deriv_right_le` and
  `norm_le_gronwallBound_of_norm_deriv_right_le` are Gronwall-like bounds and overlap the separately
  cataloged `THM-M-1337`.

The discovery-only probe elaborates these declarations. They differ in domains, binders,
hypotheses, and conclusions, so their presence confirms that the catalog wording does not select a
unique target. This is neither a complete anchor audit nor proof credit.

## Missing source-to-statement decisions

Before a canonical statement can be frozen, the dependent statement phase must obtain and
independently review an immutable primary or authoritative source and record:

1. the exact theorem passage and every incorporated definition, with stable locators and content
   hashes;
2. the complete state-space, interval, function, vector-field, solution, regularity, uniqueness,
   monotonicity, derivative, initial-order, and boundary assumptions;
3. the exact quantifier order, strictness, comparison direction, and proposition-level conclusion;
4. the treatment of empty/reversed intervals, endpoint equality, equilibria, maximal domains,
   loss of uniqueness, and vector-order boundary cases;
5. the relationship to the neighboring Gronwall and Bihari-LaSalle targets so no duplicate or
   substituted root is selected;
6. edition, translation, correction and errata status, proof boundary, dependent passages, and an
   assigned independent source reviewer.

Until those decisions are made, the received target is classified `H5`: it is not yet a stable
proposition. This routing classification does not assert that standard comparison theorems are
false or historically open.

## Lean boundary

The pinned declarations above supply credible statement candidates and reusable infrastructure,
but none can be normalized against a null canonical proposition. No module or declaration is
therefore frozen in `instance.json`, and no M0 or M1 state is assigned. The statement phase must
first select the source proposition, then elaborate it with minimal pinned imports, serialize its
expression and environment, check any transport to a candidate, and perform the required removed-
hypothesis, changed-domain, binder-scope, and boundary mutations.
