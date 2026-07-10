import Mathlib.RingTheory.Filtration

/-!
# S1-M-103 / THM-M-0010: Artin-Rees lemma

This Stage1 artifact records a repo-local Lean wrapper around the Artin-Rees
lemma already present in the pinned mathlib dependency.  The proof body remains
mathlib's theorem `Ideal.exists_pow_inf_eq_pow_smul`; this file fixes a local
statement shape and validates that the theorem is available in the repository's
Lake closure.  The checked machine anchor is `local_wrapper_upstream_mathlib`
against mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
-/

universe u v

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_103

variable {R : Type u} {M : Type v} [CommRing R] [AddCommGroup M] [Module R M]

/--
Normalized Stage1 statement shape for the Artin-Rees lemma over a Noetherian
commutative ring and a finite module.

For an ideal `I` and submodule `N`, the intersection filtration
`I ^ n • M ⊓ N` is eventually generated from the fixed finite stage `k`.
-/
def StatementShape [IsNoetherianRing R] [Module.Finite R M] : Prop :=
  ∀ (I : Ideal R) (N : Submodule R M),
    ∃ k : ℕ, ∀ n ≥ k,
      I ^ n • (⊤ : Submodule R M) ⊓ N =
        I ^ (n - k) • (I ^ k • (⊤ : Submodule R M) ⊓ N)

/--
Repo-local wrapper for mathlib's Artin-Rees lemma.

This is a completed local wrapper over the pinned mathlib theorem
`Ideal.exists_pow_inf_eq_pow_smul`.
-/
theorem artinRees_mathlib [IsNoetherianRing R] [Module.Finite R M]
    (I : Ideal R) (N : Submodule R M) :
    ∃ k : ℕ, ∀ n ≥ k,
      I ^ n • (⊤ : Submodule R M) ⊓ N =
        I ^ (n - k) • (I ^ k • (⊤ : Submodule R M) ⊓ N) := by
  exact Ideal.exists_pow_inf_eq_pow_smul (M := M) I N

/-- The normalized Stage1 statement shape is supplied by the checked mathlib wrapper. -/
theorem statementShape_from_mathlib [IsNoetherianRing R] [Module.Finite R M] :
    StatementShape (R := R) (M := M) := by
  intro I N
  exact artinRees_mathlib I N

/--
Completion marker for the exact algebraic module statement in this Stage1 slot.

This intentionally does not claim broader category-level filtered-object or
naturality variants of Artin-Rees.
-/
theorem exactAlgebraicModuleStatement_repoLocalWrapperClosed
    [IsNoetherianRing R] [Module.Finite R M] :
    StatementShape (R := R) (M := M) := by
  exact statementShape_from_mathlib

/-- Checked supporting anchor: the stable filtration used in the mathlib proof is stable. -/
theorem stableFiltration_stable_anchor (I : Ideal R) (N : Submodule R M) :
    (I.stableFiltration N).Stable := by
  exact I.stableFiltration_stable N

/--
Checked supporting anchor: the Rees algebra of a Noetherian ring is Noetherian
in the pinned mathlib API.
-/
theorem reesAlgebra_noetherian_anchor [IsNoetherianRing R] (I : Ideal R) :
    IsNoetherianRing (reesAlgebra I) := by
  infer_instance

/-- mathlib modules checked while locating the Artin-Rees formalization anchor. -/
def mathlibAnchorModules : List String := [
  "Mathlib.RingTheory.Filtration",
  "Mathlib.RingTheory.ReesAlgebra",
  "Mathlib.RingTheory.Finiteness.Nakayama",
  "Mathlib.RingTheory.Noetherian.Basic",
  "Mathlib.RingTheory.Noetherian.Defs"
]

/-- The exact mathlib theorem names used or audited for this Stage1 slot. -/
def mathlibAnchorTheorems : List String := [
  "Ideal.exists_pow_inf_eq_pow_smul",
  "Ideal.Filtration.submodule_fg_iff_stable",
  "Ideal.Filtration.Stable.of_le",
  "Ideal.stableFiltration_stable",
  "reesAlgebra.fg"
]

/-- Machine-status label for the exact Stage1 Artin-Rees wrapper. -/
def machineAnchorStatus : String := "local_wrapper_upstream_mathlib"

/-- Pinned mathlib module containing the terminal Artin-Rees theorem. -/
def machineAnchorModule : String := "Mathlib.RingTheory.Filtration"

/-- Pinned mathlib theorem wrapped by this Stage1 artifact. -/
def machineAnchorTheorem : String := "Ideal.exists_pow_inf_eq_pow_smul"

/-- Pinned mathlib revision audited for this Stage1 wrapper. -/
def machineAnchorMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Completion label for the exact algebraic Artin-Rees module statement. -/
def exactAlgebraicModuleStatementStatus : String := "repo_local_wrapper_closed"

/--
Debt label for broader category-level filtered-object or naturality variants
which are outside the exact module statement wrapped here.
-/
def broaderFilteredObjectNaturalityVariantsStatus : String := "formalization_debt"

/-! ## Theorem-tree package split -/

/--
`L103-001`: checked statement-normalization leaf.

The public Artin-Rees target is normalized to the module-theoretic equality
captured by `StatementShape`.
-/
theorem L103_001_statementNormalization [IsNoetherianRing R] [Module.Finite R M] :
    StatementShape (R := R) (M := M) := by
  exact statementShape_from_mathlib

/--
`L103-002`: checked filtration-model leaf.

The stable filtration used by the upstream proof is available in the local
mathlib closure.
-/
theorem L103_002_filtrationModel (I : Ideal R) (N : Submodule R M) :
    (I.stableFiltration N).Stable := by
  exact stableFiltration_stable_anchor I N

/--
`L103-003`: checked Rees-algebra bridge leaf.

The Noetherian Rees algebra bridge needed by the mathlib filtration proof is
available in the local mathlib closure.
-/
theorem L103_003_reesAlgebraBridge [IsNoetherianRing R] (I : Ideal R) :
    IsNoetherianRing (reesAlgebra I) := by
  exact reesAlgebra_noetherian_anchor I

/--
`L103-004`: checked stability-to-subfiltration bridge leaf.

This records the stable-subfiltration step used in the Artin-Rees proof
package.  It is intentionally stated at the filtration API boundary rather
than as a new category-level naturality claim.
-/
theorem L103_004_stabilityToSubfiltrationBridge [IsNoetherianRing R]
    [Module.Finite R M] {I : Ideal R} {F F' : I.Filtration M}
    (hF : F.Stable) (hF' : F' ≤ F) :
    F'.Stable := by
  exact Ideal.Filtration.Stable.of_le hF hF'

/--
`L103-005`: checked terminal Artin-Rees equality leaf.

This is the terminal equality package, still delegated to the pinned mathlib
proof body through the repo-local wrapper.
-/
theorem L103_005_terminalArtinReesEquality [IsNoetherianRing R] [Module.Finite R M]
    (I : Ideal R) (N : Submodule R M) :
    ∃ k : ℕ, ∀ n ≥ k,
      I ^ n • (⊤ : Submodule R M) ⊓ N =
        I ^ (n - k) • (I ^ k • (⊤ : Submodule R M) ⊓ N) := by
  exact artinRees_mathlib I N

/--
`L103-006`: checked exact-statement closure leaf.

The exact algebraic module statement is repo-local wrapper closed.
-/
theorem L103_006_exactModuleStatementClosure [IsNoetherianRing R]
    [Module.Finite R M] :
    StatementShape (R := R) (M := M) := by
  exact exactAlgebraicModuleStatement_repoLocalWrapperClosed

/--
`L103-007`: checked theorem-tree package closure leaf.

The checked local package leaves all point back to the validated wrapper
boundary; public merge-back remains a serial documentation step.
-/
theorem L103_007_theoremTreePackageClosure [IsNoetherianRing R] [Module.Finite R M] :
    StatementShape (R := R) (M := M) := by
  exact L103_006_exactModuleStatementClosure

/-- Public package names for the Artin-Rees theorem-tree split. -/
def theoremTreePackageSplit : List String := [
  "statement normalization",
  "filtration model",
  "Rees algebra bridge",
  "stability-to-intersection bridge",
  "terminal Artin-Rees equality",
  "public merge-back"
]

/-- Checked local leaf ids for the exact module-theoretic Artin-Rees package. -/
def checkedLocalLeafIds : List String := [
  "L103-001",
  "L103-002",
  "L103-003",
  "L103-004",
  "L103-005",
  "L103-006",
  "L103-007"
]

/--
Unchecked public/integrator follow-up leaves.  These are intentionally metadata
only: they require serial public-doc merge-back, not additional local proof.
-/
def uncheckedPublicFollowupLeafIds : List String := [
  "L103-U01",
  "L103-U02",
  "L103-U03"
]

/-- C005 leaf ledger statuses for public/integrator merge-back. -/
def localLeafLedgerStatuses : List (String × String) := [
  ("L103-001", "checked"),
  ("L103-002", "checked"),
  ("L103-003", "checked"),
  ("L103-004", "checked"),
  ("L103-005", "checked"),
  ("L103-006", "checked"),
  ("L103-007", "checked"),
  ("L103-U01", "unchecked"),
  ("L103-U02", "unchecked"),
  ("L103-U03", "unchecked")
]

/-- C004 package split status for the exact Artin-Rees module statement. -/
def theoremTreePackageSplitStatus : String :=
  "local_leaf_package_checked_public_merge_back_pending"

/-! ## Audit probes -/

#check Ideal.exists_pow_inf_eq_pow_smul
#check Ideal.stableFiltration_stable
#check reesAlgebra.fg
#check artinRees_mathlib
#check statementShape_from_mathlib
#check exactAlgebraicModuleStatement_repoLocalWrapperClosed
#check stableFiltration_stable_anchor
#check reesAlgebra_noetherian_anchor
#check machineAnchorStatus
#check machineAnchorModule
#check machineAnchorTheorem
#check machineAnchorMathlibRevision
#check exactAlgebraicModuleStatementStatus
#check broaderFilteredObjectNaturalityVariantsStatus
#check L103_001_statementNormalization
#check L103_002_filtrationModel
#check L103_003_reesAlgebraBridge
#check L103_004_stabilityToSubfiltrationBridge
#check L103_005_terminalArtinReesEquality
#check L103_006_exactModuleStatementClosure
#check L103_007_theoremTreePackageClosure
#check theoremTreePackageSplit
#check checkedLocalLeafIds
#check uncheckedPublicFollowupLeafIds
#check localLeafLedgerStatuses
#check theoremTreePackageSplitStatus

end S1_M_103
end Stage1
end AwesomeTheorems
