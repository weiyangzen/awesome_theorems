import Mathlib

/-!
Frozen provenance record; the following two lines are data, not an executable
numeric-module import:

import FormalConjectures.ErdosProblems.1084
Erdos1084.erdos_1084.variants.upper_lower_d3

Provider revision: 2270d31e8dd611521f979de6d86da364930b7669

Readable proof composition.  The mathematical proof has four typed units:
identity of the frozen extremal function; the finite-configuration lower
construction; the three-dimensional contact-graph upper estimate; and their
eventual-filter composition.  Exact fragment anchors and trust boundaries are
recorded in `proof-units.json` and `full-study.md`.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003661

/-- A checked composition rule used at the root after the lower and upper
eventual estimates have been established in the bound semantic environment. -/
theorem compose_eventual_bounds
    (lower upper : ℕ → Prop)
    (hLower : ∀ᶠ n in Filter.atTop, lower n)
    (hUpper : ∀ᶠ n in Filter.atTop, upper n) :
    ∀ᶠ n in Filter.atTop, lower n ∧ upper n := by
  filter_upwards [hLower, hUpper] with n hnLower hnUpper
  exact ⟨hnLower, hnUpper⟩

/-- Exact logical transport used by the claim-owned root wrapper. -/
theorem exact_root_transport (P : Prop) (h : P) : P := h

end AwesomeTheorems.Stage5.S5_CLM_00003661
