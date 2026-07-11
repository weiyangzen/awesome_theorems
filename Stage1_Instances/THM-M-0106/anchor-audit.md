# THM-M-0106 immutable anchor audit

## Status boundary

This is the audit artifact for `S56-M-0106-ANCHOR_AUDIT`. It identifies and
checks a mathlib candidate against the frozen statement. It does not promote
the dependency node, claim accepted proof credit, classify H0/R0, or claim
theorem completion. Acceptance remains with the integration lane.

## Environment and search scope

- Repository base inspected: `85ea3ad356d7424c28a5e5d582c20beeefd79292`.
- Lean: `leanprover/lean4:v4.29.0`.
- Lake manifest pins mathlib URL
  `https://github.com/leanprover-community/mathlib4.git` at immutable commit
  `8a178386ffc0f5fef0b77738bb5449d50efeea95` (the dependency checkout HEAD
  agrees). The commit date is `2026-03-30T18:47:58Z`.
- The repo-local search covered all Lean files, the full checked-out mathlib
  source, and every other package already present in the pinned Lake closure.
  No dependency was fetched or updated.
- External discovery on 2026-07-12 used GitHub's unauthenticated repository
  search for the exact phrase `"Noether normalization" Lean` (zero results)
  and attempted GitHub code search for
  `exists_finite_inj_algHom_of_fg language:Lean` (HTTP 401, authentication
  required). A grep.app query was also attempted and returned HTTP 429.
  These negative/blocked searches are discovery evidence only, not proof that
  no other Lean 4 formalization exists.

## Candidate inventory

| ID | Immutable source | Declaration | Exact type and body provenance | Assessment |
|---|---|---|---|---|
| `ANCHOR-ML-INTEGRAL` | mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Mathlib/RingTheory/NoetherNormalization.lean:275` | `exists_integral_inj_algHom_of_fg` | Produces an injective polynomial-algebra map with `g.IsIntegral`. Its source body obtains a finite-variable polynomial quotient presentation and invokes `exists_integral_inj_algHom_of_quotient`; that theorem is proved in the same file by induction on the variable count, using the Nagata coordinate change and integral quotient maps defined above it. | Strong upstream precursor, but its conclusion is integral rather than the frozen target's explicit `g.Finite` plus affine morphism. |
| `ANCHOR-ML-FINITE` | same commit and module, line 288 | `exists_finite_inj_algHom_of_fg` | Exact algebraic core: `∃ s, ∃ g, Function.Injective g ∧ g.Finite`. The source body invokes `ANCHOR-ML-INTEGRAL` and upgrades integrality to module-finiteness using finite type. | Exact algebraic candidate. `AnchorAudit.lean` checks its type and composes it with the frozen affine bridge. |
| `ANCHOR-ML-SPEC` | same pinned mathlib closure, module `Mathlib.AlgebraicGeometry.Morphisms.Finite` (transitively imported) | `AlgebraicGeometry.IsFinite.SpecMap_iff` | Equates finiteness of an affine `Spec.map` with `AlgHom.Finite`. | Exact checked bridge from the algebraic candidate to the geometric conjunct. |
| `ANCHOR-LEGACY` | repository commit above, `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_030.lean` | `noetherNormalization_algebraic_mathlib_wrapper` and affine wrappers | Repo-local historical wrappers around the same mathlib declarations. | Discovery input only under the uniform L0 rework rule; no independent proof body and no rev-5.6 credit. |
| `ANCHOR-EXTERNAL-NONE` | searches recorded above | none identified | No independently maintained non-mathlib candidate could be pinned from the bounded searches. Existing non-mathlib Lake packages contain no matching source. | No anchor-only external completion claim and hence no external integration credit or residual positive-result integration blocker. Search completeness remains limited by HTTP 401/429. |

## Exact relationship to the frozen target

`Stage1Instances.THM_M_0106.mathlibCandidate_closes_frozenTarget` elaborates at
`FrozenTargetAuditExpression`; `check_anchor_audit.py` combines the two audited
modules and requires `Iff.rfl` between this expression and the frozen
`NoetherNormalizationTarget`, rejecting any definitional difference. The theorem obtains the polynomial map from
`exists_finite_inj_algHom_of_fg`, constructs the already frozen
`affineSpaceMorphism`, transports `g.Finite` with `IsFinite.SpecMap_iff`, and
checks the required composite by simplification. Thus the pinned mathlib
candidate is technically feasible and needs no new external dependency.

The audit does not count this closure as accepted M0: the obligation registry,
proof/provenance graphs, transitive trust closure, release replay, and master
receipt are later nodes. The `#print axioms` probes report only `Classical.choice`,
`propext`, and `Quot.sound`; no new axiom, `sorry`, unsafe declaration, oracle,
or external solver is introduced by the audit module. The inspected mathlib
source contains concrete theorem bodies rather than declarations without bodies.

## Validation

Commands were run from the repository root unless a `cwd` is stated.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: check_stage1_standard: ok (15 assurance groups, 41 legacy rows,
  300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
  exit 0: stage1_target: ok (1546 unique targets, ranks 1..1546, all
  L0/rework_required)

python3 scripts/stage1_target.py show THM-M-0106
  exit 0: rank 30, baseline L0, lifecycle planned, theorem_complete false

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0106/AnchorAudit.lean
  exit 0: all four #check probes elaborated; all three #print axioms probes
  returned [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0106/check_anchor_audit.py
  exit 0: audit expression exactly matches the frozen statement; the anchor
  module and its exact-type closure theorem elaborate

python3 Stage1_Instances/THM-M-0106/check_statement.py
  exit 0: statement sha256
  4980834b63da78609158f944b53234d72089e2bfaacb348461de2651aa671209;
  all four statement mutations killed; mathlib revision agrees

git diff --check -- Stage1_Instances/THM-M-0106
  exit 0: no whitespace errors
```

## Classification and next boundary

The pinned candidate classification is `local_wrapper_upstream_mathlib`
*feasible*, pending the proof, provenance, validation, and acceptance nodes.
The independently searched external classification is `no candidate
identified`, not `external_upstream_anchor_only`. Human-source status remains
open; the Stacks tag in mathlib is a useful source lead but this machine-anchor
phase does not supply the primary-source edition/page/assumption/errata review
needed for H0.
