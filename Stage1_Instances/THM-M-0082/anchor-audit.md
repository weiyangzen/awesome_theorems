# Immutable Lean anchor audit

Item: `S56-M-0082-ANCHOR_AUDIT`  
Base revision: `c8855fd0eb87514348ace46003c6075c576fbfb6`  
Audit date: 2026-07-12

## Selected exact candidate

The selected candidate is
`CategoryTheory.isRightAdjoint_of_preservesLimits_of_solutionSetCondition` in
`Mathlib.CategoryTheory.Adjunction.AdjointFunctorTheorems`, pinned by
`Formalizations/Lean/lake-manifest.json` to mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The source file SHA-256 is
`38a9febac8fd666a6fdaa7167e8b5291f2d01d43fa131849a7124f1bb2de30e1`.

At that revision the declaration requires `[HasLimits D]`,
`[PreservesLimitsOfSize.{vD, vD} G]`, and `SolutionSetCondition.{vD} G`, and concludes
`G.IsRightAdjoint`. `AnchorAudit.lean` checks that exact application after the explicit hypotheses
of the frozen target are installed as instances. No extra local-smallness, nonemptiness,
well-poweredness, coseparating-family, or equal-object-universe premise appears.

The terminal body is present in the pinned mathlib source at lines 82-98. It reduces the goal to
initial objects in each structured-arrow category, turns the solution family into a weakly initial
family, uses products to obtain a weakly initial object, and uses wide equalizers to obtain an
initial object. Lean reports the axiom closure `[propext, Classical.choice, Quot.sound]`. The body
has no unresolved proof terms and does not cross an unsafe or oracle interface.

## Candidate disposition

`solutionSetCondition_of_isRightAdjoint` is a useful converse anchor but proves the opposite
direction. `isRightAdjoint_of_preservesLimits_of_isCoseparating` is the special theorem and adds
well-poweredness plus a small coseparating property, so it is excluded from the canonical root.
The historical `S1_M_135.lean` wrapper reaches the selected theorem, but rev-5.6 treats it only as
discovery input.

All existing pinned Lean dependency sources were searched for the declaration name,
`SolutionSetCondition`, and both general and unqualified adjoint-functor-theorem phrases. No
distinct external implementation was found. A public GitHub repository query for the quoted
theorem phrase plus Lean returned zero repositories on 2026-07-12. An auxiliary grep.app query was
rate-limited (`HTTP 429`), so it supplies no positive or negative evidence. No dependency was
fetched or changed.

## Human-source and status boundary

The machine anchor audit does not upgrade human-source fidelity. Freyd's 1964 monograph and Mac
Lane's second edition remain discovery citations because an exact theorem/page, assumptions,
errata check, and independent crosswalk have not been accepted. The human classification therefore
remains `H2`.

The exact pinned candidate removes uncertainty about whether a Lean implementation exists, but the
root remains `M4`: the obligation tree, proof integration, transitive provenance/trust checks, and
release evidence belong to downstream nodes. This audit grants no proof credit and does not claim
audit or theorem completion.

## Validation

Commands ran in this worker clone. Lean commands used the existing canonical `.lake` artifacts.

| Command | Exit | Result |
|---|---:|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact pin `8a178386...eea95` |
| `sha256sum Formalizations/Lean/.lake/packages/mathlib/Mathlib/CategoryTheory/Adjunction/AdjointFunctorTheorems.lean` | 0 | exact source hash above |
| `rg -n -i 'general adjoint functor theorem\|adjoint functor theorem\|SolutionSetCondition' Formalizations/Lean/.lake/packages --glob '*.lean'` | 0 | selected mathlib family only; no distinct pinned external implementation |
| `lake env lean ../../Stage1_Instances/THM-M-0082/AnchorAudit.lean` | 0 | exact candidate application elaborated; axiom set printed |
| `python3 -m json.tool Stage1_Instances/THM-M-0082/anchor-audit.json` | 0 | structured receipt valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0082` | 0 | no whitespace errors |

