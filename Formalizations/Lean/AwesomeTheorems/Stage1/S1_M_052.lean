import Mathlib.Algebra.Lie.SerreConstruction
import Mathlib.LinearAlgebra.RootSystem.CartanMatrix

/-!
# S1-M-052 / THM-M-0136: Kac-Moody algebras

This Stage1 file deliberately records only the local statement shape and the
mathlib boundary currently available in this repository.  Mathlib provides the
Serre construction `Matrix.ToLieAlgebra` from an integer matrix, but this file
does not assert a completed classification theorem for Kac-Moody Lie algebras.

Statement normalization: the literal phrase "classification of
infinite-dimensional Lie algebras" is too broad for a Lean Stage1 target.  The
selected target in this artifact is the Kac-Moody classification-style statement
that compares Serre-constructed Lie algebras attached to symmetrizable
indecomposable generalized Cartan matrices and asks whether Lie algebra
equivalence recovers the matrix up to reindexing.
-/

namespace AwesomeTheorems.Stage1.S1_M_052

universe u v w

/-- The generalized Cartan matrix axioms used by the Stage1 Kac-Moody
statement-shape candidate. -/
structure GeneralizedCartanMatrix (ι : Type v) where
  toMatrix : Matrix ι ι ℤ
  diag_two : ∀ i, toMatrix i i = 2
  off_diag_nonpos : ∀ {i j}, i ≠ j → toMatrix i j ≤ 0
  zero_iff : ∀ {i j}, i ≠ j → (toMatrix i j = 0 ↔ toMatrix j i = 0)

namespace GeneralizedCartanMatrix

variable {ι : Type v} (A : GeneralizedCartanMatrix ι)

/-- The graph adjacency relation determined by nonzero off-diagonal Cartan
matrix entries. -/
def Adjacent (i j : ι) : Prop :=
  A.toMatrix i j ≠ 0 ∨ A.toMatrix j i ≠ 0

/-- Indecomposability, recorded as connectedness of the Cartan graph. -/
def IsIndecomposable : Prop :=
  ∀ i j : ι, Relation.ReflTransGen A.Adjacent i j

/-- A positive integral symmetrizer for a generalized Cartan matrix. -/
def IsSymmetrizable : Prop :=
  ∃ d : ι → ℕ, (∀ i, d i ≠ 0) ∧
    ∀ i j : ι, (d i : ℤ) * A.toMatrix i j = (d j : ℤ) * A.toMatrix j i

end GeneralizedCartanMatrix

/-- The Serre Lie algebra attached by mathlib to the integer matrix underlying a
generalized Cartan matrix.  The construction is available for any integer
matrix; the generalized Cartan axioms are tracked separately above. -/
abbrev SerreLieAlgebra (R : Type u) [CommRing R] {ι : Type v} [DecidableEq ι]
    (A : GeneralizedCartanMatrix ι) : Type (max u v) :=
  Matrix.ToLieAlgebra R A.toMatrix

/-- Stage1 wrapper: the mathlib Serre construction supplies a Lie algebra
structure for every generalized Cartan matrix. -/
@[reducible]
noncomputable def serreLieAlgebraInstance (R : Type u) [CommRing R] {ι : Type v} [DecidableEq ι]
    (A : GeneralizedCartanMatrix ι) : LieAlgebra R (SerreLieAlgebra R A) :=
  inferInstance

/-- Audit constant recording the repo-local machine-checked boundary: this file
only checks the Serre-construction wrapper, not the classification theorem. -/
def MathlibSerreConstructionBoundary : Prop :=
  ∀ (R : Type u) [CommRing R] {ι : Type v} [DecidableEq ι]
    (A : GeneralizedCartanMatrix ι),
      Nonempty (LieAlgebra R (SerreLieAlgebra R A))

/-- The current repo-local wrapper boundary is inhabited by mathlib's imported
`Matrix.ToLieAlgebra` instance. -/
theorem mathlibSerreConstructionBoundary_checked :
    MathlibSerreConstructionBoundary := by
  intro R _ ι _ A
  exact ⟨inferInstance⟩

/-- Repo-local audit proposition for mathlib's Serre relation definitions:
`Matrix.ToLieAlgebra` is the quotient of the free Lie algebra by the ideal
generated from the six displayed Serre-relation families.  This is an anchor
audit only; it does not prove a Kac-Moody classification theorem. -/
def MathlibSerreRelationDefinitionsBoundary : Prop :=
  ∀ (R : Type u) [CommRing R] {ι : Type v} [DecidableEq ι]
    (A : GeneralizedCartanMatrix ι),
      CartanMatrix.Relations.toSet R A.toMatrix =
        (Set.range <| CartanMatrix.Relations.HH R) ∪
        (Set.range <| CartanMatrix.Relations.EF R) ∪
        (Set.range <| CartanMatrix.Relations.HE R A.toMatrix) ∪
        (Set.range <| CartanMatrix.Relations.HF R A.toMatrix) ∪
        (Set.range <| CartanMatrix.Relations.adE R A.toMatrix) ∪
        (Set.range <| CartanMatrix.Relations.adF R A.toMatrix) ∧
      Matrix.ToLieAlgebra R A.toMatrix =
        (FreeLieAlgebra R (CartanMatrix.Generators ι) ⧸
          CartanMatrix.Relations.toIdeal R A.toMatrix)

/-- The Serre relation audit boundary above is definitionally checked against
mathlib's imported construction. -/
theorem mathlibSerreRelationDefinitionsBoundary_checked :
    MathlibSerreRelationDefinitionsBoundary := by
  intro R _ ι _ A
  constructor <;> rfl

/-- Adjacent mathlib anchor: equality of Cartan matrices determines a finite
reduced root system up to `RootPairing.Equiv`.

This records finite root-system evidence from
`RootPairing.Base.equivOfCartanMatrixEq`.  It is deliberately not a
Kac-Moody-classification closure statement: it assumes mathlib root-system
bases, crystallographic/reduced hypotheses, and finite root index types, rather
than constructing or classifying Serre Kac-Moody Lie
algebras from generalized Cartan matrices. -/
def FiniteRootSystemCartanMatrixAnchor : Prop :=
  ∀ {ι R M N ι₂ M₂ N₂ : Type*} [CommRing R] [IsDomain R] [CharZero R]
    [AddCommGroup M] [Module R M] [AddCommGroup N] [Module R N]
    [AddCommGroup M₂] [Module R M₂] [AddCommGroup N₂] [Module R N₂]
    (P : RootPairing ι R M N) [P.IsRootSystem] [P.IsCrystallographic] [P.IsReduced]
    [Finite ι]
    (P₂ : RootPairing ι₂ R M₂ N₂) [P₂.IsRootSystem] [P₂.IsCrystallographic]
    [P₂.IsReduced] [Finite ι₂] (b : P.Base) (b₂ : P₂.Base)
    (e : b.support ≃ b₂.support),
      (∀ i j, b₂.cartanMatrix (e i) (e j) = b.cartanMatrix i j) →
      Nonempty (P.Equiv P₂)

/-- Checked wrapper around `RootPairing.Base.equivOfCartanMatrixEq`, kept as a
finite root-system adjacent anchor rather than a Kac-Moody theorem. -/
theorem finiteRootSystemCartanMatrixAnchor_checked :
    FiniteRootSystemCartanMatrixAnchor := by
  intro ι R M N ι₂ M₂ N₂ _ _ _ _ _ _ _ _ _ _ _ P _ _ _ _ P₂ _ _ _ _ b b₂ e h
  exact ⟨RootPairing.Base.equivOfCartanMatrixEq b b₂ e h⟩

/-- Equivalence of generalized Cartan matrices up to reindexing. -/
def MatrixEquivalent {ι : Type v} {κ : Type w}
    (A : GeneralizedCartanMatrix ι) (B : GeneralizedCartanMatrix κ) : Prop :=
  ∃ e : ι ≃ κ, ∀ i j : ι, B.toMatrix (e i) (e j) = A.toMatrix i j

namespace MatrixEquivalent

variable {ι : Type v} {κ : Type w}
variable {A : GeneralizedCartanMatrix ι} {B : GeneralizedCartanMatrix κ}

/-- Matrix equivalence is reflexive. -/
theorem refl (A : GeneralizedCartanMatrix ι) : MatrixEquivalent A A := by
  exact ⟨Equiv.refl ι, by intro i j; rfl⟩

/-- Matrix equivalence is symmetric. -/
theorem symm (hAB : MatrixEquivalent A B) : MatrixEquivalent B A := by
  rcases hAB with ⟨e, h⟩
  refine ⟨e.symm, ?_⟩
  intro i j
  simpa using (h (e.symm i) (e.symm j)).symm

/-- Matrix equivalence is transitive. -/
theorem trans {l : Type u} {C : GeneralizedCartanMatrix l}
    (hAB : MatrixEquivalent A B) (hBC : MatrixEquivalent B C) :
    MatrixEquivalent A C := by
  rcases hAB with ⟨eAB, hAB⟩
  rcases hBC with ⟨eBC, hBC⟩
  refine ⟨eAB.trans eBC, ?_⟩
  intro i j
  calc
    C.toMatrix ((eAB.trans eBC) i) ((eAB.trans eBC) j)
        = B.toMatrix (eAB i) (eAB j) := hBC (eAB i) (eAB j)
    _ = A.toMatrix i j := hAB i j

/-- A chosen reindexing equivalence preserves the Cartan graph adjacency
relation. -/
theorem adjacent_reindex_iff (e : ι ≃ κ)
    (h : ∀ i j : ι, B.toMatrix (e i) (e j) = A.toMatrix i j)
    (i j : ι) :
    B.Adjacent (e i) (e j) ↔ A.Adjacent i j := by
  unfold GeneralizedCartanMatrix.Adjacent
  rw [h i j, h j i]

/-- A chosen reindexing equivalence transports paths in the Cartan graph. -/
theorem reflTransGen_adjacent_reindex (e : ι ≃ κ)
    (h : ∀ i j : ι, B.toMatrix (e i) (e j) = A.toMatrix i j)
    {i j : ι} (p : Relation.ReflTransGen A.Adjacent i j) :
    Relation.ReflTransGen B.Adjacent (e i) (e j) := by
  have stepAB : ∀ {x y : ι}, A.Adjacent x y → B.Adjacent (e x) (e y) := by
    intro x y hxy
    exact (adjacent_reindex_iff (A := A) (B := B) e h x y).2 hxy
  induction p with
  | refl =>
      exact Relation.ReflTransGen.refl
  | tail p hxy ih =>
      exact Relation.ReflTransGen.tail ih (stepAB hxy)

/-- Indecomposability is invariant under reindexing of generalized Cartan
matrices. -/
theorem isIndecomposable_iff (hAB : MatrixEquivalent A B) :
    A.IsIndecomposable ↔ B.IsIndecomposable := by
  rcases hAB with ⟨e, h⟩
  constructor
  · intro hA x y
    have p := reflTransGen_adjacent_reindex (A := A) (B := B) e h
      (hA (e.symm x) (e.symm y))
    simpa using p
  · intro hB i j
    have p := reflTransGen_adjacent_reindex (A := B) (B := A) e.symm
      (by
        intro x y
        simpa using (h (e.symm x) (e.symm y)).symm)
      (hB (e i) (e j))
    simpa using p

/-- Symmetrizability is transported forward along a chosen reindexing
equivalence. -/
theorem isSymmetrizable_of_reindex (e : ι ≃ κ)
    (h : ∀ i j : ι, B.toMatrix (e i) (e j) = A.toMatrix i j) :
    A.IsSymmetrizable → B.IsSymmetrizable := by
  rintro ⟨d, hd_pos, hd_symm⟩
  refine ⟨fun k => d (e.symm k), ?_, ?_⟩
  · intro k
    exact hd_pos (e.symm k)
  · intro k l
    calc
      (d (e.symm k) : ℤ) * B.toMatrix k l
          = (d (e.symm k) : ℤ) * A.toMatrix (e.symm k) (e.symm l) := by
              rw [← h (e.symm k) (e.symm l)]
              simp
      _ = (d (e.symm l) : ℤ) * A.toMatrix (e.symm l) (e.symm k) :=
              hd_symm (e.symm k) (e.symm l)
      _ = (d (e.symm l) : ℤ) * B.toMatrix l k := by
              rw [← h (e.symm l) (e.symm k)]
              simp

/-- Symmetrizability is invariant under matrix equivalence. -/
theorem isSymmetrizable_iff (hAB : MatrixEquivalent A B) :
    A.IsSymmetrizable ↔ B.IsSymmetrizable := by
  rcases hAB with ⟨e, h⟩
  constructor
  · exact isSymmetrizable_of_reindex (A := A) (B := B) e h
  · intro hB
    exact isSymmetrizable_of_reindex (A := B) (B := A) e.symm
      (by
        intro i j
        simpa using (h (e.symm i) (e.symm j)).symm)
      hB

end MatrixEquivalent

/--
Statement-shape candidate for a classification-style Kac-Moody theorem.

This is intentionally a proposition, not a theorem with proof.  It freezes the
current formal boundary: a future completed theorem would need explicit
hypotheses under which Lie equivalence of Serre-constructed algebras recovers
the generalized Cartan matrix up to reindexing, or it must replace this
candidate with the standard classification statement selected by the integrator.
-/
def StatementShape (R : Type u) [CommRing R] : Prop :=
  ∀ {ι : Type v} {κ : Type w} [DecidableEq ι] [DecidableEq κ]
    (A : GeneralizedCartanMatrix ι) (B : GeneralizedCartanMatrix κ),
      A.IsSymmetrizable →
      B.IsSymmetrizable →
      A.IsIndecomposable →
      B.IsIndecomposable →
      Nonempty (SerreLieAlgebra R A ≃ₗ⁅R⁆ SerreLieAlgebra R B) →
      MatrixEquivalent A B

/-- Normalized public Stage1 target selected in place of the overbroad phrase
"classification of infinite-dimensional Lie algebras".  This is an alias for
the open statement-shape candidate above, not a completion theorem. -/
abbrev NormalizedKacMoodyClassificationTarget (R : Type u) [CommRing R] : Prop :=
  StatementShape.{u, v, w} R

/-! ## Branch theorem-tree package split -/

/-- The three standard Kac-Moody branches that must be tracked by independent
Stage1 theorem-tree packages. -/
inductive KacMoodyBranch where
  | finite
  | affine
  | indefinite
  deriving DecidableEq, Repr

namespace KacMoodyBranch

/-- Stable branch label for private ledgers and public backfill text. -/
def label : KacMoodyBranch → String
  | finite => "finite"
  | affine => "affine"
  | indefinite => "indefinite"

end KacMoodyBranch

/-- A single package-local leaf budget entry.  This is process data: it records
how a future proof package should be decomposed, not a proof of the terminal
classification theorem. -/
structure BranchLeafLedger where
  leafId : String
  leafSummary : String
  maxProofSteps : Nat
  budget_closed : maxProofSteps ≤ 100

/-- Branch-local theorem-tree package data for the finite, affine, and
indefinite Kac-Moody branches. -/
structure BranchTheoremTreePackage where
  packageId : String
  branch : KacMoodyBranch
  targetStatus : String
  leaves : List BranchLeafLedger

namespace BranchTheoremTreePackage

/-- A package has its own nonempty local leaf ledger, and every leaf is already
budgeted at `<= 100` proof steps. -/
def HasClosedLeafBudgetLedger (P : BranchTheoremTreePackage) : Prop :=
  P.leaves ≠ [] ∧ ∀ leaf ∈ P.leaves, leaf.maxProofSteps ≤ 100

/-- Proof that a package-local ledger satisfies the recorded leaf budgets. -/
theorem hasClosedLeafBudgetLedger_of_budgetFields (P : BranchTheoremTreePackage)
    (h : P.leaves ≠ []) : P.HasClosedLeafBudgetLedger := by
  constructor
  · exact h
  · intro leaf _h
    exact leaf.budget_closed

end BranchTheoremTreePackage

/-- Finite-type Kac-Moody branch package.

This package is intentionally separated from the affine and indefinite packages:
its current machine evidence is the adjacent finite root-system Cartan-matrix
anchor, not a proof of the Serre Kac-Moody classification target. -/
def finiteKacMoodyBranchPackage : BranchTheoremTreePackage where
  packageId := "S1-M-052.branch.finite"
  branch := KacMoodyBranch.finite
  targetStatus := "adjacent finite-root-system anchor only; terminal target open"
  leaves := [
    {
      leafId := "finite.statement-boundary"
      leafSummary := "separate finite root-system equivalence evidence from Serre Kac-Moody classification"
      maxProofSteps := 20
      budget_closed := by decide
    },
    {
      leafId := "finite.mathlib-anchor"
      leafSummary := "audit RootPairing.Base.equivOfCartanMatrixEq as finite reduced crystallographic evidence"
      maxProofSteps := 30
      budget_closed := by decide
    },
    {
      leafId := "finite.gcm-to-serre-gap"
      leafSummary := "record the missing bridge from finite Cartan data to the selected Serre Lie algebra target"
      maxProofSteps := 40
      budget_closed := by decide
    }
  ]

/-- Affine-type Kac-Moody branch package. -/
def affineKacMoodyBranchPackage : BranchTheoremTreePackage where
  packageId := "S1-M-052.branch.affine"
  branch := KacMoodyBranch.affine
  targetStatus := "formalization_debt; no affine terminal classification theorem pinned"
  leaves := [
    {
      leafId := "affine.statement-boundary"
      leafSummary := "isolate the affine generalized-Cartan-matrix case from the finite and indefinite branches"
      maxProofSteps := 25
      budget_closed := by decide
    },
    {
      leafId := "affine.loop-adjacent-anchor"
      leafSummary := "treat mathlib loop-Lie-algebra infrastructure as adjacent evidence only"
      maxProofSteps := 35
      budget_closed := by decide
    },
    {
      leafId := "affine.classification-gap"
      leafSummary := "record the missing affine Kac-Moody classification wrapper or external proof coordinates"
      maxProofSteps := 40
      budget_closed := by decide
    }
  ]

/-- Indefinite-type Kac-Moody branch package. -/
def indefiniteKacMoodyBranchPackage : BranchTheoremTreePackage where
  packageId := "S1-M-052.branch.indefinite"
  branch := KacMoodyBranch.indefinite
  targetStatus := "formalization_debt; no indefinite terminal classification theorem pinned"
  leaves := [
    {
      leafId := "indefinite.statement-boundary"
      leafSummary := "isolate the indefinite generalized-Cartan-matrix case from finite and affine cases"
      maxProofSteps := 25
      budget_closed := by decide
    },
    {
      leafId := "indefinite.symmetrizable-indecomposable-frontier"
      leafSummary := "track symmetrizable indecomposable hypotheses for the selected StatementShape target"
      maxProofSteps := 35
      budget_closed := by decide
    },
    {
      leafId := "indefinite.classification-gap"
      leafSummary := "record the missing indefinite Kac-Moody classification wrapper or external proof coordinates"
      maxProofSteps := 40
      budget_closed := by decide
    }
  ]

/-- All branch packages retained by this Stage1 artifact. -/
def kacMoodyBranchPackages : List BranchTheoremTreePackage := [
  finiteKacMoodyBranchPackage,
  affineKacMoodyBranchPackage,
  indefiniteKacMoodyBranchPackage
]

/-- The finite package owns a nonempty `<= 100` leaf ledger. -/
theorem finiteKacMoodyBranchPackage_budget_checked :
    finiteKacMoodyBranchPackage.HasClosedLeafBudgetLedger :=
  BranchTheoremTreePackage.hasClosedLeafBudgetLedger_of_budgetFields
    finiteKacMoodyBranchPackage (by decide)

/-- The affine package owns a nonempty `<= 100` leaf ledger. -/
theorem affineKacMoodyBranchPackage_budget_checked :
    affineKacMoodyBranchPackage.HasClosedLeafBudgetLedger :=
  BranchTheoremTreePackage.hasClosedLeafBudgetLedger_of_budgetFields
    affineKacMoodyBranchPackage (by decide)

/-- The indefinite package owns a nonempty `<= 100` leaf ledger. -/
theorem indefiniteKacMoodyBranchPackage_budget_checked :
    indefiniteKacMoodyBranchPackage.HasClosedLeafBudgetLedger :=
  BranchTheoremTreePackage.hasClosedLeafBudgetLedger_of_budgetFields
    indefiniteKacMoodyBranchPackage (by decide)

/-! ## External terminal-theorem audit surface -/

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Algebra.Lie.SerreConstruction",
  "Mathlib.Algebra.Lie.Loop",
  "Mathlib.LinearAlgebra.RootSystem.CartanMatrix",
  "Mathlib.LinearAlgebra.RootSystem.GeckConstruction.Basic",
  "Mathlib.LinearAlgebra.RootSystem.RootPositive"
]

/-- Pinned theorem or definition names used by this local artifact. -/
def repoLocalAnchorNames : List String := [
  "Matrix.ToLieAlgebra",
  "CartanMatrix.Relations.toSet",
  "CartanMatrix.Relations.toIdeal",
  "CartanMatrix.Relations.HH",
  "CartanMatrix.Relations.EF",
  "CartanMatrix.Relations.HE",
  "CartanMatrix.Relations.HF",
  "CartanMatrix.Relations.adE",
  "CartanMatrix.Relations.adF",
  "RootPairing.Base.equivOfCartanMatrixEq"
]

/--
Search terms used on 2026-05-01 for the public Lean 4 terminal-theorem audit.

These terms are retained as checked data so later integrators can reproduce the
scope before changing the public blueprint status.
-/
def publicLean4TerminalSearchTerms : List String := [
  "Lean 4 Kac-Moody algebra classification theorem GitHub",
  "site:github.com Lean Kac-Moody algebra classification",
  "site:github.com lean4 KacMoody algebra",
  "site:github.com \"Kac-Moody\" \"theorem\" \"Lean\"",
  "\"Matrix.ToLieAlgebra\" \"Kac-Moody\" Lean",
  "\"CartanMatrix.Relations\" Lean",
  "\"RootPairing.Base.equivOfCartanMatrixEq\"",
  "\"Kac-Moody\" \"Matrix.ToLieAlgebra\"",
  "\"KacMoody\" Lean4",
  "\"Kac-Moody\" \"lean-toolchain\"",
  "\"Kac-Moody\" \"lakefile\""
]

/--
Audit result for `S1-M-052-public-005`.

The 2026-05-01 search found no public Lean 4 project exposing a terminal
Kac-Moody classification theorem with a module/theorem/revision that can be
pinned and checked in this Lake project.  The local pinned mathlib closure
contains `Matrix.ToLieAlgebra` and finite root-system Cartan-matrix anchors,
but no completed theorem proving the classification-style target above.
-/
def publicLean4TerminalClassificationAudit : String :=
  "not found: no candidate public Lean 4 terminal Kac-Moody classification theorem " ++
  "with a concrete module/theorem/revision was identified on 2026-05-01; " ++
  "mathlib supplies Serre-construction and finite root-system anchors only."

/-- Machine proof debt classification for this Stage1 slot after the terminal-theorem audit. -/
def machineProofDebtClassification : String :=
  "formalization_debt"

/--
Repo-local integration-debt gate for this child pass.

Because no external Lean 4 terminal theorem was identified, this pass did not
create an anchor-only completed state and has no upstream proof body to pin.
If a later audit finds such a proof, completion requires a pinned Lake
dependency or vendored proof body plus repo-local validation.
-/
def repoLocalIntegrationDebtGate : String :=
  "not completed; no completed state retains repo_local_integration_debt"

/-! ## S1-M-052-public-008 completion gate -/

/-- Checked process state for `S1-M-052-public-008`.

This is intentionally a gate record rather than a theorem proving
`StatementShape`: the public item must remain open until one of the two machine
closure inputs becomes true in this repository. -/
structure C008ClosureGate where
  terminalTheoremInRepoLocalClosure : Bool
  pinnedExternalProofInRepoLocalClosure : Bool
  completionClaimAllowed : Bool
  noCompletedStateRetainsRepoLocalIntegrationDebt : Bool
  machineStatus : String
  blockingCondition : String

/-- Current repo-local C008 gate: no terminal theorem and no pinned external
proof have entered this Lake validation closure. -/
def c008ClosureGate : C008ClosureGate where
  terminalTheoremInRepoLocalClosure := false
  pinnedExternalProofInRepoLocalClosure := false
  completionClaimAllowed := false
  noCompletedStateRetainsRepoLocalIntegrationDebt := true
  machineStatus := "not_repo_local_closed / formalization_debt"
  blockingCondition :=
    "keep open until a terminal Kac-Moody classification theorem or pinned external proof validates repo-locally"

/-- C008 has no repo-local terminal Kac-Moody classification theorem yet. -/
theorem c008_terminalTheoremInRepoLocalClosure_eq_false :
    c008ClosureGate.terminalTheoremInRepoLocalClosure = false :=
  rfl

/-- C008 has no pinned external proof in this repository's Lean closure yet. -/
theorem c008_pinnedExternalProofInRepoLocalClosure_eq_false :
    c008ClosureGate.pinnedExternalProofInRepoLocalClosure = false :=
  rfl

/-- C008 cannot honestly be marked complete in the current repo-local closure. -/
theorem c008_completionClaimAllowed_eq_false :
    c008ClosureGate.completionClaimAllowed = false :=
  rfl

/-- The open C008 state does not leave a completed-state integration debt. -/
theorem c008_noCompletedStateRetainsRepoLocalIntegrationDebt_eq_true :
    c008ClosureGate.noCompletedStateRetainsRepoLocalIntegrationDebt = true :=
  rfl

#check Matrix.ToLieAlgebra
#check CartanMatrix.Relations.toSet
#check CartanMatrix.Relations.toIdeal
#check RootPairing.Base.equivOfCartanMatrixEq
#check MatrixEquivalent.refl
#check MatrixEquivalent.symm
#check MatrixEquivalent.trans
#check MatrixEquivalent.adjacent_reindex_iff
#check MatrixEquivalent.reflTransGen_adjacent_reindex
#check MatrixEquivalent.isIndecomposable_iff
#check MatrixEquivalent.isSymmetrizable_of_reindex
#check MatrixEquivalent.isSymmetrizable_iff
#check StatementShape
#check NormalizedKacMoodyClassificationTarget
#check finiteKacMoodyBranchPackage_budget_checked
#check affineKacMoodyBranchPackage_budget_checked
#check indefiniteKacMoodyBranchPackage_budget_checked
#check kacMoodyBranchPackages
#check publicLean4TerminalSearchTerms
#check publicLean4TerminalClassificationAudit
#check machineProofDebtClassification
#check repoLocalIntegrationDebtGate
#check C008ClosureGate
#check c008ClosureGate
#check c008_terminalTheoremInRepoLocalClosure_eq_false
#check c008_pinnedExternalProofInRepoLocalClosure_eq_false
#check c008_completionClaimAllowed_eq_false
#check c008_noCompletedStateRetainsRepoLocalIntegrationDebt_eq_true

end AwesomeTheorems.Stage1.S1_M_052
