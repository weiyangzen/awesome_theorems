# Anchor audit

Item: `S56-M-0525-ANCHOR_AUDIT`. The immutable machine inventory is in
`anchor-audit.json`; `AnchorAudit.lean` checks the exact pinned signatures and operation equations.

## Pinned mathlib result

Mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains all mathematical
components needed for the frozen target. `FundamentalGroup X x` unfolds to
`Path.Homotopic.Quotient x x`, and the imported group has the expected identity and inverse.
However, its multiplication is `p * q = q.trans p`, following `CategoryTheory.End.mul_def`, whereas
`Statement.lean` deliberately freezes `p * q = p.trans q`. Thus the public instance is not an
exact root closure and must not be credited as one.

The exact forward-concatenation laws are separately present as
`Path.Homotopic.Quotient.refl_trans`, `trans_refl`, `trans_assoc`, `trans_symm`, and `symm_trans`.
Their terminal bodies use quotient induction and explicit path homotopies. Lean reports the axiom
set `[propext, Classical.choice, Quot.sound]` for each. This is exact pinned proof-component
availability, not yet a proof of `THM_M_0525.Statement`.

## External result

Four plausible public projects were inspected at immutable revisions. The Owen Milner and
Mak1Haru projects are Lean 3; only the latter has a group construction, and neither is an importable
Lean 4 dependency here. Prakol16's Lean 3 project concerns related groupoid results. Chrisflav's
Lean 4 `pi1` project concerns the etale fundamental group of schemes, a different theorem. No exact
external Lean 4 root closure was found by the recorded protocol, and no external candidate receives
machine credit.

## Classification

The candidate inventory for the bounded protocol is complete. The root remains open at `M2`:
exact pinned building blocks exist, but no exact local declaration of the frozen proposition has
been checked. The debt is `formalization_debt`, not `repo_local_integration_debt`, because the only
eligible proof components are already in the pinned mathlib closure. Audit-wide and theorem-wide
completion remain false; the next phase must freeze the obligation tree before constructing the
exact group witness.

## Validation

| Command | Exit | Result |
|---|---:|---|
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0525/AnchorAudit.lean)` | 0 | All candidate types, carrier equality, inherited operation equations, and five axiom reports checked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Recorded during final self-test. |
| `python3 scripts/stage1_target.py check` | 0 | Recorded during final self-test. |
| `python3 scripts/stage1_target.py show THM-M-0525` | 0 | Recorded during final self-test. |
| `python3 -m json.tool Stage1_Instances/THM-M-0525/anchor-audit.json` | 0 | Recorded during final self-test. |
| `git diff --check -- Stage1_Instances/THM-M-0525` | 0 | Recorded during final self-test. |

The canonical `.lake` symlink and existing compiled artifacts were used read-only. No update,
build, clone, or fetch was run.
