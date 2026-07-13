# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1619-1624` supplies exactly the title `刘维尔定理`, Joseph
Liouville, 1844, the gloss `有界整函数必为常数` ("every bounded entire function is constant"),
importance "high," and status `已验证`. Git blame places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no bibliography, formula, definition,
quantifier order, proof boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:6221-6246` repeats the gloss while explicitly leaving the target formal
system, logical foundation, precise definitions and premises, proof route, dependencies,
equivalent formulations, axioms, machine state, and artifact links open. Its generic theorem-tree
language is planning metadata. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Human-source boundary

The classical complex-analysis theorem is historically established, so the recognizable family is
provisionally `H1`, not an open mathematical problem. The catalog's Liouville/1844 attribution is
only a bibliographic lead: this intake did not admit an immutable primary or authoritative edition,
locate an exact theorem and incorporated definitions, map its assumptions and conclusion, inspect
translations or errata, trace its proof nodes, or obtain independent review. No source is accepted
as `H0`.

## Clause crosswalk

| Catalog component | Mathematical decision | Prospective Lean surface | Intake result |
|---|---|---|---|
| "function" | scalar complex function or a library generalization | `f : Complex -> Complex` versus `f : E -> F` | scalar family suggested; exact binders open |
| "entire" | holomorphic on all of `Complex` under a fixed definition | `Differentiable Complex f` or checked analytic equivalent | definition and transport open |
| "bounded" | bounded image or an explicit global norm bound | `Bornology.IsBounded (Set.range f)` or checked equivalent | quantifiers and source definition open |
| "constant" | pairwise equality, existential value, or function equality | the three pinned `Differentiable.*_of_bounded` conclusion shapes | canonical encoding open |
| Liouville / 1844 | historical attribution | immutable source and pinpoint locators | catalog lead only; no admitted text |
| `已验证` | untrusted inventory label | accepted human and kernel receipts would be required | no H or M credit |

## Pinned formal candidates

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.Complex.Liouville` exposes:

| Declaration | Candidate conclusion | Intake boundary |
|---|---|---|
| `Differentiable.apply_eq_apply_of_bounded` | `f z = f w` for arbitrary `z w` | pairwise form over general complex normed spaces |
| `Differentiable.exists_const_forall_eq_of_bounded` | `exists c, forall z, f z = c` | closest prose shape, but still a library generalization |
| `Differentiable.exists_eq_const_of_bounded` | `exists c, f = Function.const E c` | function-equality encoding; source transport open |

All three take `Differentiable Complex f` and `Bornology.IsBounded (Set.range f)` and allow
arbitrary complex normed domain and codomain spaces without a codomain completeness premise.
`IntakeProbe.lean` checks the interfaces and reports their direct axiom summaries as `propext`,
`Classical.choice`, and `Quot.sound`. This is strong `M3` interface evidence only. Intake does not
inspect terminal bodies or transitive provenance, prove a scalar specialization wrapper, establish
an elaborated root fingerprint, accept a foundation profile, or claim `M0-W`; those gates belong to
the statement and anchor-audit nodes.

## Namesake and substitution boundary

The repository separately records Hamiltonian phase-space volume preservation as `THM-M-1520` and
bounded harmonic functions as `THM-M-1143`. The pinned module
`Mathlib.Analysis.Complex.Harmonic.Liouville` also contains the harmonic variant. None shares target
identity, state, or proof credit with this bounded-entire complex-function theorem. Number-theoretic
Liouville declarations and corollaries such as polynomial root existence are likewise not root
substitutes.

Before leaving intake, the statement route remains blocked on an admitted exact source proposition
and independent crosswalk review. It must then freeze the scalar/generalization decision, exact
binders and imports, expression and environment fingerprints, checked alternate transports, and
the required removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
