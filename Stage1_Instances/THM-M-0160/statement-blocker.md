# Statement gate blocker

Item: `S56-M-0160-STATEMENT`  
Theorem: `THM-M-0160`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The authoritative repository record supplies only the title "fundamental theorem of surface
theory," the attribution to Ossian Bonnet, the year 1867, and the gloss "a surface is determined by
its first and second fundamental forms." It supplies no primary-source edition, theorem/page, or
definitions. The completed intake correctly records that this wording does not decide among
materially different propositions: local or global realization, coordinate domain or abstract
surface, regularity class, connectedness and simple connectedness, orientation and normal sign,
the exact Gauss-Codazzi equations, immersion versus embedding, and proper versus arbitrary
Euclidean-motion uniqueness.

Those choices alter the binders, hypotheses, and conclusion. In particular, "determined" could
refer only to uniqueness for already-existing immersions, while the classical Bonnet theorem also
has an existence half subject to compatibility conditions. Selecting one textbook variant without
an authoritative source freeze would broaden or substitute the metadata rather than elaborate its
exact claim. Under rev-5.6 sections 2 and 5, statement ambiguity and a missing expression
fingerprint are hard blockers.

Pinned mathlib contains general manifold immersion and Riemannian-metric infrastructure, but the
scoped source search found no second-fundamental-form, shape-operator, Gauss-Codazzi, or Bonnet
surface theorem API. `StatementInfrastructure.lean` checks only the available `Manifold.IsImmersion`
and `IsContMDiffRiemannianBundle` declarations. It deliberately declares no canonical theorem,
proof, axiom, opaque proxy predicate, or locally invented compatibility relation.

Consequently the required exact ordered binders, hypotheses, conclusion, degenerate cases,
normalized elaborated expression, expression fingerprint, checked transports, and meaningful
removed-hypothesis/domain/binder/boundary mutations cannot truthfully be produced. Machine debt
remains `M4`; statement acceptance and theorem completion are false.

## Environment fingerprint

- Repository base revision: `93c99233108bb249d1bca807a3a56a2b63e0cd54`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

Commands ran inside this worker clone. Lean used only the existing pinned `.lake` artifacts; no
update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0160/StatementInfrastructure.lean` | 0 | Pinned `Manifold.IsImmersion` and `IsContMDiffRiemannianBundle` API declarations elaborated; no canonical target was asserted |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'secondFundamental|second_fundamental|shapeOperator|shape_operator|Gauss.Codazzi|Codazzi|Bonnet' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No matching pinned mathlib source declaration |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0160` | 0 | Rank 659, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0160` | 0 | No whitespace errors |

## Retry condition

Provide an immutable primary-source edition and pinpoint theorem that fixes the local/global scope,
domain and regularity, positivity and symmetry conditions, explicit Gauss-Codazzi compatibility
equations and sign convention, existence conclusion, and rigid-motion uniqueness convention. The
statement phase can then encode that exact claim, adding source-faithful missing definitions where
needed, and run all four required mutation classes.

Until that retry condition is met, the statement gate is not self-tested to completion. Therefore
no `.stage1-worker-selftest.json` is emitted.
