import Mathlib.Algebra.LinearRecurrence
import Mathlib.Data.Set.Finite.Basic
import Mathlib.GroupTheory.Finiteness
import Mathlib.GroupTheory.OrderOfElement
import Mathlib.NumberTheory.Height.NumberField
import Mathlib.NumberTheory.Height.Northcott
import Mathlib.NumberTheory.NumberField.ProductFormula
import Mathlib.NumberTheory.NumberField.Units.DirichletTheorem
import Mathlib.RingTheory.DedekindDomain.SInteger
import Mathlib.RingTheory.RootsOfUnity.PrimitiveRoots

/-!
# S1-M-016 / THM-M-0403: Schlickewei--Evertse theorem

This Stage1 artifact records a conservative Lean 4 statement-shape boundary for
the Schlickewei--Evertse finiteness theorem as it is used for zeroes of
nondegenerate linear recurrence sequences.

The terminal theorem is not proved here.  The checked content is limited to:
* an explicit exponential-polynomial zero-set statement shape;
* a companion linear-recurrence zero-set statement shape with an explicit
  nondegeneracy placeholder;
* a named audit/proof-package split for future M0387-level public backfill;
* small local wrappers around definitional membership, the empty-set finiteness
  criterion, and mathlib's geometric-solution/characteristic-polynomial bridge.
-/

noncomputable section

open scoped BigOperators
open scoped NumberField

namespace AwesomeTheorems.Stage1.S1_M_016

universe u

/-- Audit identifier for the source theorem. -/
def theoremUID : String := "THM-M-0403"

/-- Current machine-proof debt classification for this Stage1 artifact. -/
def machineProofDebt : String := "formalization_debt"

/--
This artifact does not retain repo-local integration debt: no external Lean 4
ESS/S-unit or Schlickewei--Evertse closure has been pinned into this repository.
-/
def repoLocalIntegrationDebtRetained : Bool := false

/-- Checked gate: this artifact records no completed-state repo-local integration debt. -/
theorem repoLocalIntegrationDebtRetained_eq_false :
    repoLocalIntegrationDebtRetained = false :=
  rfl

/--
Data for a simple exponential polynomial
`∑ i, coeff i * root i ^ n` over a field.

The `ratio_nontorsion` field is the usual nondegeneracy condition for the simple
root case: distinct characteristic roots have quotient which is not of finite
multiplicative order.
-/
structure ExponentialPolynomialData (K : Type u) [Field K] (r : ℕ) where
  coeff : Fin r → K
  root : Fin r → K
  coeff_ne_zero : ∀ i, coeff i ≠ 0
  root_ne_zero : ∀ i, root i ≠ 0
  ratio_nontorsion : ∀ i j, i ≠ j → ¬ IsOfFinOrder (root i / root j)

/--
The three candidate public targets considered for `THM-M-0403`.

The canonical Stage1 target is intentionally the simple nondegenerate
exponential-polynomial zero-finiteness branch.  The ESS multiplicative-equation
theorem is the expected deep input for a terminal proof, and the full
`LinearRecurrence` zero theorem is kept as a downstream wrapper so this slot
does not duplicate the Skolem--Mahler--Lech periodic branch owned by
`S1-M-017`.
-/
inductive PublicTheoremTarget where
  | essMultiplicativeEquation
  | simpleExponentialPolynomialZeroFiniteness
  | fullLinearRecurrenceZeroTheorem
  deriving DecidableEq, Repr

/-- Frozen canonical target for the public Stage1 surface of this slot. -/
def canonicalPublicTheoremTarget : PublicTheoremTarget :=
  PublicTheoremTarget.simpleExponentialPolynomialZeroFiniteness

/-- The ESS theorem is a deep input target, not the canonical public wrapper. -/
def essMultiplicativeEquationIsDeferredInput : Bool :=
  canonicalPublicTheoremTarget ≠ PublicTheoremTarget.essMultiplicativeEquation

/-- The full recurrence theorem is a downstream wrapper target, not this root target. -/
def fullLinearRecurrenceTheoremIsDeferredWrapper : Bool :=
  canonicalPublicTheoremTarget ≠ PublicTheoremTarget.fullLinearRecurrenceZeroTheorem

/-- Evaluate the exponential polynomial attached to `D` at index `n`. -/
def ExponentialPolynomialData.eval {K : Type u} [Field K] {r : ℕ}
    (D : ExponentialPolynomialData K r) (n : ℕ) : K :=
  ∑ i : Fin r, D.coeff i * D.root i ^ n

/-- Zero indices of a simple exponential polynomial. -/
def exponentialPolynomialZeroSet {K : Type u} [Field K] {r : ℕ}
    (D : ExponentialPolynomialData K r) : Set ℕ :=
  {n | D.eval n = 0}

/--
Stage1 normalized statement shape for the simple-root zero-finiteness theorem.

For every nonempty finite sum of nonzero exponential terms whose pairwise root
quotients are not torsion, the set of zero indices is finite.
-/
def SimpleNondegenerateZeroFinitenessShape (K : Type u) [Field K] [CharZero K] : Prop :=
  ∀ (r : ℕ), 0 < r → ∀ D : ExponentialPolynomialData K r,
    (exponentialPolynomialZeroSet D).Finite

/--
Canonical public theorem target after freezing `THM-M-0403-P00`.

This is a named alias rather than a new proof claim: it records that the public
Stage1 target is the simple nondegenerate exponential-polynomial zero-finiteness
statement, not the terminal ESS theorem and not the full recurrence theorem.
-/
def CanonicalPublicTheoremTargetShape (K : Type u) [Field K] [CharZero K] : Prop :=
  SimpleNondegenerateZeroFinitenessShape K

/-- Zero indices of a mathlib linear recurrence sequence. -/
def recurrenceZeroSet {K : Type u} [Zero K] (u : ℕ → K) : Set ℕ :=
  {n | u n = 0}

/--
The nonzero quotient of two characteristic roots as an element of the unit
group.

`rootsOfUnity` in mathlib is a subgroup of units, while the statement-level
nondegeneracy condition for exponential polynomials is written on field
elements.  This wrapper is the checked bridge object for those two APIs and the
two-term smoke test below.
-/
abbrev nonzeroRootRatioUnit {K : Type u} [Field K] {r : ℕ}
    (D : ExponentialPolynomialData K r) (i j : Fin r) : Kˣ :=
  Units.mk0 (D.root i / D.root j)
    (div_ne_zero (D.root_ne_zero i) (D.root_ne_zero j))

/--
Witness that a recurrence sequence has already been reduced to the simple
nondegenerate exponential-polynomial branch.

A terminal formalization must replace this predicate with the chosen
characteristic-root / splitting-field object model, or connect it to a pinned
external ESS/S-unit dependency.
-/
def RecurrenceNondegenerateData (K : Type u) [Field K]
    (_E : LinearRecurrence K) (u : ℕ → K) : Prop :=
  ∃ (r : ℕ) (_hr : 0 < r) (D : ExponentialPolynomialData K r),
    ∀ n : ℕ, u n = D.eval n

/--
Companion statement shape for zeroes of linear recurrences already reduced to
the simple nondegenerate exponential-polynomial branch.
-/
def LinearRecurrenceZeroFinitenessShape (K : Type u) [Field K] [CharZero K] : Prop :=
  ∀ (E : LinearRecurrence K) (u : ℕ → K),
    E.IsSolution u →
      RecurrenceNondegenerateData K E u →
        (recurrenceZeroSet u).Finite

/--
Canonical Stage1 statement boundary for this slot.

The direct executable artifact is the simple exponential-polynomial
zero-finiteness shape; the recurrence formulation is retained separately to
avoid duplicating the Skolem--Mahler--Lech periodic branch in `S1-M-017`.
-/
def StatementShape (K : Type u) [Field K] [CharZero K] : Prop :=
  CanonicalPublicTheoremTargetShape K

/-- Membership in the exponential-polynomial zero set unfolds to evaluation. -/
theorem mem_exponentialPolynomialZeroSet_iff {K : Type u} [Field K] {r : ℕ}
    (D : ExponentialPolynomialData K r) (n : ℕ) :
    n ∈ exponentialPolynomialZeroSet D ↔ D.eval n = 0 :=
  Iff.rfl

/-- Membership in the recurrence zero set unfolds to the sequence value. -/
theorem mem_recurrenceZeroSet_iff {K : Type u} [Zero K] (u : ℕ → K) (n : ℕ) :
    n ∈ recurrenceZeroSet u ↔ u n = 0 :=
  Iff.rfl

/-- The canonical statement shape is currently the simple nondegenerate shape. -/
theorem statementShape_iff (K : Type u) [Field K] [CharZero K] :
    StatementShape K ↔ SimpleNondegenerateZeroFinitenessShape K :=
  Iff.rfl

/-- The frozen target selection is the simple exponential-polynomial branch. -/
theorem canonicalPublicTheoremTarget_eq :
    canonicalPublicTheoremTarget =
      PublicTheoremTarget.simpleExponentialPolynomialZeroFiniteness :=
  rfl

/-! ## Skolem--Mahler--Lech periodic-branch coordination for `THM-M-0403-P08` -/

/--
Owner slot for the periodic/finite-union branch of recurrence zero sets.

This string is metadata, but it is paired below with checked references to the
actual `S1_M_017` statement surfaces.
-/
def skolemMahlerLechPeriodicBranchOwnerSlot : String := "S1-M-017 / THM-M-0404"

/--
Checked owner gate for `THM-M-0403-P08`.

The Schlickewei--Evertse slot keeps the simple nondegenerate finite-zero
branch.  It does not own the Skolem--Mahler--Lech conclusion that a recurrence
zero set is eventually periodic or a finite union of arithmetic progressions.
-/
def skolemMahlerLechPeriodicBranchOwnedHere : Bool := false

/-- Checked P08 gate: the SML periodic branch is not owned by this slot. -/
theorem skolemMahlerLechPeriodicBranchOwnedHere_eq_false :
    skolemMahlerLechPeriodicBranchOwnedHere = false :=
  rfl

/--
Canonical S1-M-017 finite-union arithmetic-progression statement surface.

This is recorded as a declaration name rather than imported here so the required
direct validation command for this file does not depend on a prebuilt sibling
`.olean`.
-/
def s1m017FiniteUnionAPStatementShapeName : String :=
  "AwesomeTheorems.Stage1.S1_M_017.StatementShape"

/--
Canonical S1-M-017 eventual-periodic companion statement surface.

The bridge between the S1-M-017 variants is owned by `THM-M-0404-P03`.
-/
def s1m017EventuallyPeriodicStatementShapeName : String :=
  "AwesomeTheorems.Stage1.S1_M_017.StatementShapeEventuallyPeriodic"

/--
P08 coordination rows for serial public backfill.

The declaration names for `S1_M_017.StatementShape` and
`S1_M_017.StatementShapeEventuallyPeriodic` anchor the periodic/AP branch to
the neighboring slot rather than reintroducing it here under a competing
canonical name.  The child ledger records the direct compile probe for
`S1_M_017.lean`.
-/
def skolemMahlerLechPeriodicBranchCoordinationRows : List String := [
  "THM-M-0403 canonical target: SimpleNondegenerateZeroFinitenessShape over exponential-polynomial data",
  "THM-M-0403 recurrence surface: LinearRecurrenceZeroFinitenessShape is only a downstream finite-zero wrapper after nondegenerate exponential-polynomial reduction",
  "THM-M-0404 finite-union owner: AwesomeTheorems.Stage1.S1_M_017.StatementShape",
  "THM-M-0404 eventual-periodic owner: AwesomeTheorems.Stage1.S1_M_017.StatementShapeEventuallyPeriodic",
  "duplication gate: S1-M-016 must not publish finite-union arithmetic-progression or eventual-periodic recurrence-zero conclusions as its canonical target"
]

/-- The P08 coordination table currently records five rows. -/
theorem skolemMahlerLechPeriodicBranchCoordinationRows_length :
    skolemMahlerLechPeriodicBranchCoordinationRows.length = 5 :=
  rfl

/--
Checked P08 target split: the full recurrence theorem is not this slot's
canonical public target.
-/
theorem fullLinearRecurrenceTheoremIsDeferredWrapper_eq_true :
    fullLinearRecurrenceTheoremIsDeferredWrapper = true :=
  rfl

/-- The named public target shape is definitionally the simple branch. -/
theorem canonicalPublicTheoremTargetShape_iff (K : Type u) [Field K] [CharZero K] :
    CanonicalPublicTheoremTargetShape K ↔
      SimpleNondegenerateZeroFinitenessShape K :=
  Iff.rfl

/--
Checked reduced case: if an exponential polynomial has no zero indices by
hypothesis, then its zero set is finite.

This is a smoke-test wrapper only, not a proof of the Schlickewei--Evertse
theorem.
-/
theorem finite_exponentialPolynomialZeroSet_of_no_zero {K : Type u} [Field K]
    {r : ℕ} (D : ExponentialPolynomialData K r)
    (h : ∀ n : ℕ, D.eval n ≠ 0) :
    (exponentialPolynomialZeroSet D).Finite := by
  have h_empty : exponentialPolynomialZeroSet D = ∅ := by
    ext n
    simp [exponentialPolynomialZeroSet, h n]
  simp [h_empty]

/--
Checked one-term smoke test: a single nonzero exponential term with nonzero root
has no zero indices.
-/
theorem oneTerm_zeroSet_empty {K : Type u} [Field K]
    (D : ExponentialPolynomialData K 1) :
    exponentialPolynomialZeroSet D = ∅ := by
  ext n
  simp [exponentialPolynomialZeroSet, ExponentialPolynomialData.eval,
    D.coeff_ne_zero 0, D.root_ne_zero 0]

/-- Consequently, the one-term zero set is finite. -/
theorem oneTerm_zeroSet_finite {K : Type u} [Field K]
    (D : ExponentialPolynomialData K 1) :
    (exponentialPolynomialZeroSet D).Finite := by
  simp [oneTerm_zeroSet_empty D]

/--
Zero indices for a normalized two-term exponential polynomial
`c0 * q ^ n + c1`.

The unit ratio `q` is the low-dimensional model for the quotient of two
nonzero characteristic roots.
-/
def twoTermUnitZeroSet {K : Type u} [Field K] (c0 c1 : K) (q : Kˣ) :
    Set ℕ :=
  {n | c0 * (q : K) ^ n + c1 = 0}

/--
Checked two-term smoke test: if the root ratio is not torsion, then the
normalized two-term zero set has at most one index.

This proves only the low-dimensional wrapper.  It is not a terminal
Schlickewei--Evertse proof.
-/
theorem twoTermUnitZeroSet_subsingleton {K : Type u} [Field K]
    {c0 c1 : K} {q : Kˣ} (hc0 : c0 ≠ 0) (hq : ¬ IsOfFinOrder q) :
    (twoTermUnitZeroSet c0 c1 q).Subsingleton := by
  intro n hn m hm
  have hn_eq : c0 * (q : K) ^ n = -c1 :=
    eq_neg_of_add_eq_zero_left hn
  have hm_eq : c0 * (q : K) ^ m = -c1 :=
    eq_neg_of_add_eq_zero_left hm
  have hp : (q : K) ^ n = (q : K) ^ m :=
    mul_left_cancel₀ hc0 (hn_eq.trans hm_eq.symm)
  have hpu : q ^ n = q ^ m := by
    ext
    simpa using hp
  exact (injective_pow_iff_not_isOfFinOrder.mpr hq) hpu

/-- Consequently, the normalized two-term zero set is finite. -/
theorem twoTermUnitZeroSet_finite {K : Type u} [Field K]
    {c0 c1 : K} {q : Kˣ} (hc0 : c0 ≠ 0) (hq : ¬ IsOfFinOrder q) :
    (twoTermUnitZeroSet c0 c1 q).Finite :=
  (twoTermUnitZeroSet_subsingleton hc0 hq).finite

/--
The concrete two-term exponential-polynomial zero condition is equivalent to
the normalized unit-ratio condition obtained by dividing by the second root.
-/
theorem twoTerm_eval_zero_iff_unitRatio {K : Type u} [Field K]
    (D : ExponentialPolynomialData K 2) (n : ℕ) :
    D.eval n = 0 ↔
      D.coeff 0 * ((nonzeroRootRatioUnit D 0 1 : Kˣ) : K) ^ n +
        D.coeff 1 = 0 := by
  have hroot1pow : D.root 1 ^ n ≠ 0 := pow_ne_zero n (D.root_ne_zero 1)
  have hqpow :
      ((nonzeroRootRatioUnit D 0 1 : Kˣ) : K) ^ n =
        D.root 0 ^ n / D.root 1 ^ n := by
    simp [nonzeroRootRatioUnit, div_pow]
  calc
    D.eval n = 0 ↔ D.eval n / D.root 1 ^ n = 0 := by
      constructor
      · intro h
        simp [h]
      · intro h
        exact (div_eq_zero_iff.mp h).resolve_right hroot1pow
    _ ↔ D.coeff 0 * ((nonzeroRootRatioUnit D 0 1 : Kˣ) : K) ^ n +
          D.coeff 1 = 0 := by
      rw [hqpow]
      simp [ExponentialPolynomialData.eval, Fin.sum_univ_two]
      field_simp [hroot1pow]
      simp [D.root_ne_zero 1]

/-- The two-term zero set is the normalized unit-ratio zero set. -/
theorem twoTerm_zeroSet_eq_unitZeroSet {K : Type u} [Field K]
    (D : ExponentialPolynomialData K 2) :
    exponentialPolynomialZeroSet D =
      twoTermUnitZeroSet (D.coeff 0) (D.coeff 1)
        (nonzeroRootRatioUnit D 0 1) := by
  ext n
  exact twoTerm_eval_zero_iff_unitRatio D n

/--
Checked two-term smoke test for the `ExponentialPolynomialData` wrapper: a
two-term nondegenerate simple exponential polynomial has a finite zero set.
-/
theorem twoTerm_zeroSet_finite {K : Type u} [Field K]
    (D : ExponentialPolynomialData K 2) :
    (exponentialPolynomialZeroSet D).Finite := by
  have hq : ¬ IsOfFinOrder (nonzeroRootRatioUnit D 0 1) := by
    intro hfin
    exact D.ratio_nontorsion 0 1 (by decide)
      ((Units.isOfFinOrder_val).mpr hfin)
  rw [twoTerm_zeroSet_eq_unitZeroSet D]
  exact twoTermUnitZeroSet_finite (D.coeff_ne_zero 0) hq

/-- P07 audit result: the low-dimensional smoke-test wrappers are checked. -/
def lowDimensionalSmokeTestWrappersClosed : Bool := true

/-- Checked P07 gate for one-term and two-term smoke-test wrappers. -/
theorem lowDimensionalSmokeTestWrappersClosed_eq_true :
    lowDimensionalSmokeTestWrappersClosed = true :=
  rfl

/-- Concrete checked wrappers supplied for `THM-M-0403-P07`. -/
def lowDimensionalSmokeTestWrappers : List String := [
  "oneTerm_zeroSet_empty: local proof that a one-term nonzero exponential polynomial has empty zero set",
  "oneTerm_zeroSet_finite: finite one-term zero-set wrapper",
  "twoTermUnitZeroSet_subsingleton: normalized two-term non-torsion unit-ratio zero set has at most one index",
  "twoTermUnitZeroSet_finite: finite normalized two-term zero-set wrapper",
  "twoTerm_eval_zero_iff_unitRatio: concrete Fin 2 exponential polynomial reduces to normalized unit-ratio form",
  "twoTerm_zeroSet_finite: finite two-term ExponentialPolynomialData zero-set wrapper"
]

/-- The P07 wrapper table currently records six checked rows. -/
theorem lowDimensionalSmokeTestWrappers_length :
    lowDimensionalSmokeTestWrappers.length = 6 :=
  rfl

/--
Checked bridge: the simple exponential-polynomial statement implies the
recurrence formulation once the recurrence has been reduced to such a
nondegenerate exponential-polynomial presentation.
-/
theorem linearRecurrenceShape_of_simpleShape {K : Type u} [Field K] [CharZero K]
    (hSimple : SimpleNondegenerateZeroFinitenessShape K) :
    LinearRecurrenceZeroFinitenessShape K := by
  intro E u _hsol hreduce
  rcases hreduce with ⟨r, hr, D, h_eq⟩
  have h_zeroSet :
      recurrenceZeroSet u = exponentialPolynomialZeroSet D := by
    ext n
    simp [recurrenceZeroSet, exponentialPolynomialZeroSet, h_eq n]
  simpa [h_zeroSet] using hSimple r hr D

/--
Checked mathlib bridge: a geometric sequence is a solution exactly when its
ratio is a root of the recurrence characteristic polynomial.
-/
theorem geometric_solution_iff_root_charPoly {K : Type u} [CommRing K]
    (E : LinearRecurrence K) (q : K) :
    (E.IsSolution fun n => q ^ n) ↔ E.charPoly.IsRoot q :=
  E.geom_sol_iff_root_charPoly q

/-! ## M0387 audit and proof-package split -/

/--
Proof-planning packages for a future Schlickewei--Evertse formalization.

The constructors are stable theorem-tree nodes, not proof claims.  They keep the
statement/audit/proof-package split inside the checked artifact while the
terminal theorem remains formalization debt.
-/
inductive SchlickeweiEvertseProofPackage where
  | canonicalStatementBoundary
  | mathlibLinearRecurrenceAnchorAudit
  | multiplicativeGroupEquationInput
  | sUnitAndHeightInfrastructure
  | exceptionalSubsumClassification
  | finiteZeroExtraction
  | recurrenceWrapperBridge
  | publicCompletionGate
  deriving DecidableEq, Repr

/-- Canonical order for the Schlickewei--Evertse proof-package queue. -/
def schlickeweiEvertseProofPackageSplit :
    List SchlickeweiEvertseProofPackage := [
  SchlickeweiEvertseProofPackage.canonicalStatementBoundary,
  SchlickeweiEvertseProofPackage.mathlibLinearRecurrenceAnchorAudit,
  SchlickeweiEvertseProofPackage.multiplicativeGroupEquationInput,
  SchlickeweiEvertseProofPackage.sUnitAndHeightInfrastructure,
  SchlickeweiEvertseProofPackage.exceptionalSubsumClassification,
  SchlickeweiEvertseProofPackage.finiteZeroExtraction,
  SchlickeweiEvertseProofPackage.recurrenceWrapperBridge,
  SchlickeweiEvertseProofPackage.publicCompletionGate
]

/-- The current proof-package split has eight named nodes. -/
theorem schlickeweiEvertseProofPackageSplit_length :
    schlickeweiEvertseProofPackageSplit.length = 8 :=
  rfl

/--
Machine-checkable status labels for the current proof-package queue.

Rows labelled `open` are deliberately not encoded as proof obligations here:
without a local proof body or pinned external dependency, turning them into
theorems would either add an unsafe placeholder or misstate the repo-local
closure.
-/
def schlickeweiEvertseProofPackageStatus : List String := [
  "canonicalStatementBoundary: checked; StatementShape is the characteristic-zero simple nondegenerate exponential-polynomial zero-finiteness shape",
  "mathlibLinearRecurrenceAnchorAudit: checked anchors include LinearRecurrence.IsSolution and geom_sol_iff_root_charPoly",
  "multiplicativeGroupEquationInput: open formalization_debt; no ESS multiplicative-equation theorem is pinned/imported/checked",
  "sUnitAndHeightInfrastructure: partial anchors only; S-integer/S-unit and height modules are available but no terminal S-unit finiteness theorem is present",
  "exceptionalSubsumClassification: open formalization_debt; root-ratio nondegeneracy has a checked IsOfFinOrder/rootsOfUnity bridge, but no ESS exceptional-subsum classification is proved",
  "finiteZeroExtraction: open formalization_debt; no local proof from ESS/Subspace input to finite zero set",
  "recurrenceWrapperBridge: checked conditional bridge from SimpleNondegenerateZeroFinitenessShape to LinearRecurrenceZeroFinitenessShape",
  "publicCompletionGate: open serial integration; ledger backfill required before public checklist closure"
]

/--
Repo-local integration-debt gate for this Stage1 slot.

The current artifact is not a completed theorem state.  It records a checked
statement boundary, anchors, and package split while leaving the terminal
Schlickewei--Evertse proof as formalization debt.
-/
def repoLocalIntegrationDebtGate : List String := [
  "repoLocalIntegrationDebtRetained = false in the checked Lean artifact",
  "no external Lean 4 ESS/S-unit/Subspace-theorem proof has been pinned/imported/checked",
  "mathlib anchors are local object-model support, not anchor-only completion evidence",
  "completion remains blocked until StatementShape is proved by local_proof_body, local_wrapper_upstream_mathlib, or external_upstream_pinned dependency closure"
]

/-- M0387 machine-proof debt classification for this Stage1 artifact. -/
def machineProofDebtClassification : List String := [
  "mathematical_debt: none for the classical Schlickewei--Evertse finiteness theorem",
  "formalization_debt: terminal ESS/Subspace-method proof body is not present in this repository",
  "repo_local_integration_debt: not retained as a completed-state claim; no external proof is used as completion evidence"
]

/--
The terminal proof obligation remains the normalized statement shape.

This definition records the open formalization target without adding an unsafe
placeholder.
-/
def SchlickeweiEvertseFormalizationDebt (K : Type u) [Field K] [CharZero K] :
    Prop :=
  StatementShape K

/-- The formalization-debt target is exactly the normalized statement shape. -/
theorem schlickeweiEvertseFormalizationDebt_iff
    (K : Type u) [Field K] [CharZero K] :
    SchlickeweiEvertseFormalizationDebt K ↔ StatementShape K :=
  Iff.rfl

/-- M0387-level completion-gate rows for public backfill. -/
def m0387CompletionGateRows : List (String × String × String) := [
  ("machine theorem/module anchor",
    "partial",
    "LinearRecurrence and finite-set wrappers compile; no terminal ESS theorem anchor exists locally"),
  ("statement boundary",
    "checked",
    "CanonicalPublicTheoremTargetShape and StatementShape compile as the simple nondegenerate zero-finiteness branch"),
  ("repo-local validation",
    "pending rerun after each edit",
    "required command: cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_016.lean"),
  ("repo-local integration debt",
    "satisfied for non-completion state",
    "no completed theorem claim and no anchor-only external proof evidence"),
  ("proof-package split",
    "checked metadata",
    "schlickeweiEvertseProofPackageSplit fixes eight package nodes for future <=100-step leaf ledgers"),
  ("public proof-process merge",
    "pending serial integration",
    "worker ledger supplies backfill text without editing shared public docs")
]

/-- Remaining theorem-internal leaves after this package-split child. -/
def m0387RemainingChildLeaves : List String := [
  "prove or import a terminal ESS/Subspace-theorem input over the selected characteristic-zero field interface",
  "connect mathlib S-unit/height infrastructure to the multiplicative-group equation used by Schlickewei--Evertse",
  "connect the checked root-ratio torsion API to an ESS exceptional-subsum classification theorem",
  "prove finite zero extraction from the multiplicative-equation finiteness package",
  "strengthen RecurrenceNondegenerateData into a characteristic-root reduction for mathlib LinearRecurrence",
  "merge the statement/audit/proof-package split into the serial public blueprint and todo surfaces"
]

/-! ## Finite-rank group API audit for `THM-M-0403-P03` -/

/--
The additive quotient of the number-field unit group by torsion.

This is the concrete mathlib object replacing the old abstract
`HasFiniteRankSubgroup` placeholder for the available unit-group branch:
finite-rank information is represented by `Module.Free`, `Module.Finite`, and
`Module.finrank` on this quotient, together with `Monoid.FG`/`Subgroup.FG` for
the full unit group and its generated subgroups.
-/
abbrev UnitsModTorsion (K : Type u) [Field K] [NumberField K] :=
  Additive ((𝓞 K)ˣ ⧸ NumberField.Units.torsion K)

/--
Concrete finite-rank unit-group package available in mathlib.

This is support infrastructure for future ESS/S-unit work, not a proof of the
Schlickewei--Evertse multiplicative-equation theorem.
-/
def FiniteRankUnitGroupAPI (K : Type u) [Field K] [NumberField K] : Prop :=
  letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
  Module.Free ℤ (UnitsModTorsion K) ∧
    Module.Finite ℤ (UnitsModTorsion K) ∧
    Module.finrank ℤ (UnitsModTorsion K) = NumberField.Units.rank K ∧
    Monoid.FG (𝓞 K)ˣ ∧
    (⊤ : Subgroup (𝓞 K)ˣ).FG ∧
    Subgroup.closure (Set.range (NumberField.Units.fundSystem K)) ⊔
      NumberField.Units.torsion K = ⊤

/-- mathlib wrapper: units modulo torsion form a free `ℤ`-module. -/
theorem unitsModTorsion_free (K : Type u) [Field K] [NumberField K] :
    letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
    Module.Free ℤ (UnitsModTorsion K) := by
  letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
  infer_instance

/-- mathlib wrapper: units modulo torsion form a finite `ℤ`-module. -/
theorem unitsModTorsion_finite (K : Type u) [Field K] [NumberField K] :
    letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
    Module.Finite ℤ (UnitsModTorsion K) := by
  letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
  infer_instance

/-- mathlib wrapper: the finite rank of units modulo torsion is `NumberField.Units.rank K`. -/
theorem unitsModTorsion_finrank (K : Type u) [Field K] [NumberField K] :
    letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
    Module.finrank ℤ (UnitsModTorsion K) = NumberField.Units.rank K := by
  letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
  exact NumberField.Units.rank_modTorsion K

/-- mathlib wrapper: the full unit group is finitely generated as a monoid. -/
theorem unitGroup_monoid_fg (K : Type u) [Field K] [NumberField K] :
    Monoid.FG (𝓞 K)ˣ :=
  inferInstance

/-- mathlib wrapper: the top subgroup of the unit group is finitely generated. -/
theorem unitGroup_topSubgroup_fg (K : Type u) [Field K] [NumberField K] :
    (⊤ : Subgroup (𝓞 K)ˣ).FG := by
  rw [← Group.fg_def, Group.fg_iff_monoid_fg]
  exact unitGroup_monoid_fg K

/--
mathlib wrapper: the chosen fundamental units plus torsion generate the full
unit group.
-/
theorem unitGroup_closure_fundSystem_sup_torsion_eq_top
    (K : Type u) [Field K] [NumberField K] :
    Subgroup.closure (Set.range (NumberField.Units.fundSystem K)) ⊔
        NumberField.Units.torsion K = ⊤ :=
  NumberField.Units.closure_fundSystem_sup_torsion_eq_top K

/-- Checked replacement package for the old `HasFiniteRankSubgroup` placeholder. -/
theorem finiteRankUnitGroupAPI (K : Type u) [Field K] [NumberField K] :
    FiniteRankUnitGroupAPI K := by
  letI : Module ℤ (UnitsModTorsion K) := AddCommGroup.toIntModule (UnitsModTorsion K)
  exact ⟨unitsModTorsion_free K, unitsModTorsion_finite K,
    unitsModTorsion_finrank K, unitGroup_monoid_fg K,
    unitGroup_topSubgroup_fg K, unitGroup_closure_fundSystem_sup_torsion_eq_top K⟩

/-- P03 audit result: no abstract `HasFiniteRankSubgroup` predicate is retained. -/
def hasFiniteRankSubgroupPlaceholderRetained : Bool := false

/-- Checked P03 gate for the placeholder-removal audit. -/
theorem hasFiniteRankSubgroupPlaceholderRetained_eq_false :
    hasFiniteRankSubgroupPlaceholderRetained = false :=
  rfl

/-- Concrete mathlib replacements used for finite-rank group data in this slot. -/
def finiteRankGroupAPIReplacements : List String := [
  "Group.FG",
  "Subgroup.FG",
  "Monoid.FG",
  "Module.Free ℤ (Additive ((𝓞 K)ˣ ⧸ NumberField.Units.torsion K))",
  "Module.Finite ℤ (Additive ((𝓞 K)ˣ ⧸ NumberField.Units.torsion K))",
  "Module.finrank ℤ (Additive ((𝓞 K)ˣ ⧸ NumberField.Units.torsion K))",
  "NumberField.Units.rank",
  "NumberField.Units.rank_modTorsion",
  "NumberField.Units.fundSystem",
  "NumberField.Units.closure_fundSystem_sup_torsion_eq_top"
]

/-! ## Roots-of-unity / torsion API audit for `THM-M-0403-P04` -/

/-- The unit-level root ratio coerces back to the statement-level quotient. -/
theorem nonzeroRootRatioUnit_coe {K : Type u} [Field K] {r : ℕ}
    (D : ExponentialPolynomialData K r) (i j : Fin r) :
    ((nonzeroRootRatioUnit D i j : Kˣ) : K) = D.root i / D.root j :=
  rfl

/--
Checked unit-level API for root-ratio nondegeneracy.

This is the object-model version of the statement-field condition
`D.ratio_nontorsion`, aligned with mathlib's `rootsOfUnity` API on units.
-/
def RootRatioNondegenerate {K : Type u} [Field K] {r : ℕ}
    (D : ExponentialPolynomialData K r) : Prop :=
  ∀ i j, i ≠ j → ¬ IsOfFinOrder (nonzeroRootRatioUnit D i j)

/-- `IsOfFinOrder` for a unit is equivalent to membership in some positive roots-of-unity subgroup. -/
theorem unit_isOfFinOrder_iff_exists_mem_rootsOfUnity {K : Type u} [Field K]
    (u : Kˣ) :
    IsOfFinOrder u ↔ ∃ n : ℕ, 0 < n ∧ u ∈ rootsOfUnity n K := by
  constructor
  · intro h
    rcases (isOfFinOrder_iff_pow_eq_one.mp h) with ⟨n, hn, hpow⟩
    exact ⟨n, hn, (mem_rootsOfUnity n u).mpr hpow⟩
  · rintro ⟨n, hn, hmem⟩
    exact isOfFinOrder_iff_pow_eq_one.mpr
      ⟨n, hn, (mem_rootsOfUnity n u).mp hmem⟩

/-- Negated unit torsion is equivalently exclusion from all positive roots-of-unity subgroups. -/
theorem unit_not_isOfFinOrder_iff_forall_not_mem_rootsOfUnity {K : Type u} [Field K]
    (u : Kˣ) :
    ¬ IsOfFinOrder u ↔ ∀ n : ℕ, 0 < n → u ∉ rootsOfUnity n K := by
  constructor
  · intro h n hn hmem
    exact h ((unit_isOfFinOrder_iff_exists_mem_rootsOfUnity u).mpr ⟨n, hn, hmem⟩)
  · intro h hfin
    rcases (unit_isOfFinOrder_iff_exists_mem_rootsOfUnity u).mp hfin with
      ⟨n, hn, hmem⟩
    exact h n hn hmem

/--
The statement-level `ratio_nontorsion` field and the checked unit-level
root-ratio API are equivalent.
-/
theorem rootRatioNondegenerate_iff_ratio_nontorsion {K : Type u} [Field K]
    {r : ℕ} (D : ExponentialPolynomialData K r) :
    RootRatioNondegenerate D ↔
      ∀ i j, i ≠ j → ¬ IsOfFinOrder (D.root i / D.root j) := by
  constructor
  · intro h i j hij hfin
    have hunit :
        IsOfFinOrder (nonzeroRootRatioUnit D i j) := by
      apply Units.isOfFinOrder_val.mp
      simpa [nonzeroRootRatioUnit] using hfin
    exact h i j hij hunit
  · intro h i j hij hfin
    apply h i j hij
    exact (Units.isOfFinOrder_val).mpr hfin

/-- Every `ExponentialPolynomialData` record supplies the checked unit-level nondegeneracy API. -/
theorem rootRatioNondegenerate_of_data {K : Type u} [Field K] {r : ℕ}
    (D : ExponentialPolynomialData K r) :
    RootRatioNondegenerate D :=
  (rootRatioNondegenerate_iff_ratio_nontorsion D).mpr D.ratio_nontorsion

/--
The root-ratio nondegeneracy condition is exactly exclusion from all positive
`rootsOfUnity n K` subgroups.
-/
theorem rootRatioNondegenerate_iff_forall_not_mem_rootsOfUnity
    {K : Type u} [Field K] {r : ℕ} (D : ExponentialPolynomialData K r) :
    RootRatioNondegenerate D ↔
      ∀ i j, i ≠ j → ∀ n : ℕ, 0 < n →
        nonzeroRootRatioUnit D i j ∉ rootsOfUnity n K := by
  constructor
  · intro h i j hij
    exact (unit_not_isOfFinOrder_iff_forall_not_mem_rootsOfUnity
      (nonzeroRootRatioUnit D i j)).mp (h i j hij)
  · intro h i j hij
    exact (unit_not_isOfFinOrder_iff_forall_not_mem_rootsOfUnity
      (nonzeroRootRatioUnit D i j)).mpr (h i j hij)

/-- P04 audit result: root-ratio nondegeneracy now has a checked unit/roots-of-unity bridge. -/
def rootRatioTorsionAPIAuditClosed : Bool := true

/-- Checked P04 gate for the roots-of-unity / torsion API audit. -/
theorem rootRatioTorsionAPIAuditClosed_eq_true :
    rootRatioTorsionAPIAuditClosed = true :=
  rfl

/-- Concrete mathlib APIs selected for the root-ratio torsion audit. -/
def rootRatioTorsionAPIReplacements : List String := [
  "IsOfFinOrder",
  "isOfFinOrder_iff_pow_eq_one",
  "Units.isOfFinOrder_val",
  "rootsOfUnity",
  "mem_rootsOfUnity",
  "rootsOfUnity.mkOfPowEq",
  "IsPrimitiveRoot",
  "IsPrimitiveRoot.isOfFinOrder",
  "isPrimitiveRoot_of_mem_rootsOfUnity"
]

/--
One row of the integration-ready public mathlib anchor table for
`THM-M-0403-P01`.

The table is metadata only.  It records modules and local audit probes; it does
not claim a terminal Schlickewei--Evertse or ESS/S-unit theorem.
-/
structure PublicMathlibAnchorRow where
  moduleName : String
  anchorRole : String
  repoLocalProbe : String
  currentStatus : String
  completionUse : String
  deriving Repr, DecidableEq

/--
Integration-ready mathlib anchor table for the Schlickewei--Evertse slot.

These rows are intentionally stronger than a prose-only public-doc note because
the named modules are imported above and this file is checked by Lean.  Rows
whose status describes support are not terminal proof anchors.
-/
def publicMathlibAnchorTable : List PublicMathlibAnchorRow := [
  {
    moduleName := "Mathlib.Algebra.LinearRecurrence",
    anchorRole := "linear recurrence object model and geometric-sequence bridge",
    repoLocalProbe := "LinearRecurrence; LinearRecurrence.IsSolution; LinearRecurrence.geom_sol_iff_root_charPoly",
    currentStatus := "checked_support",
    completionUse := "state the recurrence wrapper and bridge geometric solutions to characteristic roots"
  },
  {
    moduleName := "Mathlib.RingTheory.DedekindDomain.SInteger",
    anchorRole := "S-integer and S-unit infrastructure over Dedekind domains",
    repoLocalProbe := "Set.integer; Set.unit; Set.unit_valuation_eq_one; Set.unitEquivUnitsInteger",
    currentStatus := "checked_support_import",
    completionUse := "future host for finite-place support and S-unit equation normalization"
  },
  {
    moduleName := "Mathlib.NumberTheory.NumberField.Units.DirichletTheorem",
    anchorRole := "finite-rank unit-group infrastructure for number fields",
    repoLocalProbe := "FiniteRankUnitGroupAPI; Group.FG; Subgroup.FG; Monoid.FG; NumberField.Units.rank_modTorsion; NumberField.Units.closure_fundSystem_sup_torsion_eq_top",
    currentStatus := "checked_support_import",
    completionUse := "replace HasFiniteRankSubgroup placeholder with checked finite-rank unit-group data, not an ESS multiplicative-equation proof"
  },
  {
    moduleName := "Mathlib.NumberTheory.Height.Basic",
    anchorRole := "abstract global height API and product-formula interface",
    repoLocalProbe := "Height.logHeight_nonneg; Height.mulHeight; Height.logHeight",
    currentStatus := "checked_transitive_support",
    completionUse := "height bookkeeping for future Subspace-theorem/ESS formalization"
  },
  {
    moduleName := "Mathlib.NumberTheory.Height.NumberField",
    anchorRole := "number-field height specialization",
    repoLocalProbe := "NumberField.logHeight₁_eq; NumberField.mulHeight₁_eq; NumberField.totalWeight_eq_finrank",
    currentStatus := "checked_support_import",
    completionUse := "connect height expressions to finite and infinite places over number fields"
  },
  {
    moduleName := "Mathlib.NumberTheory.Height.Northcott",
    anchorRole := "Northcott-style finiteness infrastructure for bounded heights",
    repoLocalProbe := "module import checked",
    currentStatus := "checked_support_import",
    completionUse := "possible finiteness extraction support after terminal Diophantine input is available"
  },
  {
    moduleName := "Mathlib.NumberTheory.NumberField.ProductFormula",
    anchorRole := "finite/infinite place product formula over number fields",
    repoLocalProbe := "NumberField.prod_abs_eq_one; NumberField.FinitePlace.prod_eq_inv_abs_norm",
    currentStatus := "checked_support_import",
    completionUse := "product-formula normalization for height and S-unit reductions"
  }
]

/-- The public mathlib anchor table currently has seven rows. -/
theorem publicMathlibAnchorTable_length :
    publicMathlibAnchorTable.length = 7 :=
  rfl

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Algebra.LinearRecurrence",
  "Mathlib.GroupTheory.OrderOfElement",
  "Mathlib.RingTheory.RootsOfUnity.Basic",
  "Mathlib.RingTheory.RootsOfUnity.PrimitiveRoots",
  "Mathlib.RingTheory.DedekindDomain.SInteger",
  "Mathlib.NumberTheory.NumberField.Units.DirichletTheorem",
  "Mathlib.NumberTheory.Height.Basic",
  "Mathlib.NumberTheory.Height.NumberField",
  "Mathlib.NumberTheory.Height.Northcott",
  "Mathlib.NumberTheory.NumberField.ProductFormula"
]

/-- Checked or relevant theorem names found during the local anchor audit. -/
def mathlibAnchorTheorems : List String := [
  "LinearRecurrence.IsSolution",
  "LinearRecurrence.geom_sol_iff_root_charPoly",
  "IsOfFinOrder",
  "isOfFinOrder_iff_pow_eq_one",
  "Units.isOfFinOrder_val",
  "rootsOfUnity",
  "mem_rootsOfUnity",
  "IsPrimitiveRoot",
  "IsPrimitiveRoot.isOfFinOrder",
  "RootRatioNondegenerate",
  "Group.FG",
  "Subgroup.FG",
  "Monoid.FG",
  "NumberField.Units.rank_modTorsion",
  "NumberField.Units.closure_fundSystem_sup_torsion_eq_top",
  "FiniteRankUnitGroupAPI",
  "Set.Finite",
  "Set.finite_empty"
]

/-- Search terms that did not locate a terminal ESS/S-unit proof in mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Schlickewei",
  "Evertse",
  "EvertseSchlickewei",
  "SubspaceTheorem",
  "SUnit",
  "SUnitEquation",
  "SkolemMahlerLech",
  "LinearRecurrenceZero"
]

/-! ## External Lean 4 project search audit for `THM-M-0403-P05` -/

/--
One row of the external Lean 4 search audit for terminal ESS/S-unit or
Schlickewei--Evertse proof anchors.

Rows are negative unless `theoremName` records a real declaration.  They are
metadata only and do not import, pin, or complete any external proof.
-/
structure ExternalLean4SearchRow where
  repositoryURL : String
  commitSHA : String
  moduleOrPath : String
  theoremName : String
  queryOrScope : String
  result : String
  deriving Repr, DecidableEq

/--
External Lean 4 project search results for `THM-M-0403-P05`.

No row supplies a terminal theorem.  The exact pinned Lake dependencies were
searched locally by commit; unauthenticated public repository searches found no
relevant Lean 4 project for the exact theorem-family queries, and GitHub code
search could not be used through `gh` without authentication.
-/
def externalLean4ProjectSearchRows : List ExternalLean4SearchRow := [
  {
    repositoryURL := "https://github.com/leanprover-community/mathlib4",
    commitSHA := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    moduleOrPath := "Mathlib/RingTheory/DedekindDomain/SInteger.lean",
    theoremName := "none-found",
    queryOrScope := "local git grep for Schlickewei, Evertse, SubspaceTheorem, SUnitEquation, S-unit, SkolemMahlerLech, LinearRecurrenceZero",
    result := "support-only hit for S integer/S-unit file comment; no ESS, S-unit equation finiteness, Subspace theorem, Schlickewei-Evertse, or recurrence-zero theorem declaration"
  },
  {
    repositoryURL := "https://github.com/leanprover-community/flt-regular",
    commitSHA := "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27",
    moduleOrPath := "repository-wide *.lean search",
    theoremName := "none-found",
    queryOrScope := "local git grep for Schlickewei, Evertse, SubspaceTheorem, SUnitEquation, S-unit, SkolemMahlerLech, LinearRecurrenceZero",
    result := "no matching terminal theorem-family declaration"
  },
  {
    repositoryURL := "https://api.github.com/search/repositories",
    commitSHA := "not-applicable",
    moduleOrPath := "public repository search API",
    theoremName := "none-found",
    queryOrScope := "Schlickewei Lean; Evertse Lean; \"Subspace theorem\" Lean; \"S-unit equation\" Lean; Skolem Mahler Lech Lean; LinearRecurrence Lean mathlib",
    result := "no relevant Lean 4 theorem project located by unauthenticated repository search"
  },
  {
    repositoryURL := "https://github.com/search",
    commitSHA := "not-applicable",
    moduleOrPath := "public web/code search attempt",
    theoremName := "blocked",
    queryOrScope := "gh search code for exact terms Schlickewei, Evertse, SkolemMahlerLech, SubspaceTheorem in language:Lean",
    result := "GitHub CLI code search requires authentication in this environment; no code-search candidate was accepted as proof evidence"
  }
]

/-- P05 audit result: no external terminal Lean 4 proof anchor was accepted. -/
def externalTerminalLean4ProofFound : Bool := false

/-- Checked P05 gate for the external-project search audit. -/
theorem externalTerminalLean4ProofFound_eq_false :
    externalTerminalLean4ProofFound = false :=
  rfl

/-- The P05 external search table currently records four checked audit rows. -/
theorem externalLean4ProjectSearchRows_length :
    externalLean4ProjectSearchRows.length = 4 :=
  rfl

/-! ## External proof integration gate for `THM-M-0403-P06` -/

/--
Repo-local integration status for a possible external ESS/S-unit proof.

The current status is the first constructor: the P05 audit did not locate a
terminal Lean 4 proof declaration to pin, import, and check.  The other
constructors document the only acceptable future completion routes under the
M0387 no-anchor-only gate.
-/
inductive ExternalProofIntegrationStatus where
  | noExternalTerminalProofFound
  | externalProofPinnedImportedChecked
  | externalProofBlocked
  deriving DecidableEq, Repr

/-- Current P06 integration status after the negative P05 search audit. -/
def externalProofIntegrationStatus : ExternalProofIntegrationStatus :=
  ExternalProofIntegrationStatus.noExternalTerminalProofFound

/--
Checked P06 status gate: there is no external terminal proof currently available
for repo-local integration.
-/
theorem externalProofIntegrationStatus_eq_noExternalTerminalProofFound :
    externalProofIntegrationStatus =
      ExternalProofIntegrationStatus.noExternalTerminalProofFound :=
  rfl

/--
Concrete integration blockers for `THM-M-0403-P06`.

These rows explain why no external proof was pinned/imported/checked in this
child.  They are not completion evidence for the terminal theorem.
-/
def externalProofIntegrationBlockers : List String := [
  "no terminal Lean 4 declaration for ESS, S-unit equation finiteness, the Subspace theorem, Schlickewei-Evertse, Skolem-Mahler-Lech, or recurrence-zero finiteness was found in the pinned Lake dependencies",
  "mathlib currently supplies support modules for LinearRecurrence, S-integers/S-units, units, heights, Northcott, and product formulas, but no terminal ESS/S-unit finiteness theorem to wrap",
  "unauthenticated public repository search found no pin-ready Lean 4 theorem project for the exact theorem-family queries recorded in externalLean4ProjectSearchRows",
  "GitHub code search through gh was unavailable without GH_TOKEN or gh auth login; an authenticated exact-code search is required before any future completed-state claim",
  "if a future audit finds an external proof, completion requires a pinned dependency or vendored proof body plus a repo-local lake env lean validation; anchor-only URL/theorem-name evidence remains non-completing"
]

/-- The P06 blocker table currently records five concrete blocker rows. -/
theorem externalProofIntegrationBlockers_length :
    externalProofIntegrationBlockers.length = 5 :=
  rfl

/--
P06 repo-local integration-debt gate result.

The current artifact makes no completed-state claim and therefore does not keep
`repo_local_integration_debt` as a completion state.  It remains blocked as
formalization debt until a local proof body, a mathlib wrapper, or a pinned
external dependency closes `StatementShape`.
-/
def p06RepoLocalIntegrationDebtGate : List String := [
  "externalTerminalLean4ProofFound = false",
  "externalProofIntegrationStatus = noExternalTerminalProofFound",
  "no external proof was pinned/imported/checked because no terminal external proof declaration was located",
  "no anchor-only external proof evidence is used as completion evidence",
  "parent theorem remains formalization_debt / not_repo_local_closed"
]

/-- The P06 repo-local integration-debt gate currently records five rows. -/
theorem p06RepoLocalIntegrationDebtGate_length :
    p06RepoLocalIntegrationDebtGate.length = 5 :=
  rfl

/-! ## Public theorem-tree backfill gate for `THM-M-0403-P09` -/

/--
Machine-anchor status used by the public theorem-tree backfill gate.

The current settled status is deliberately a non-completion status: the checked
statement boundary and audit metadata are present, but no terminal
Schlickewei--Evertse/ESS proof is locally closed or externally pinned.
-/
inductive PublicBackfillMachineAnchorStatus where
  | settledFormalizationDebtNoExternalProof
  | settledRepoLocalClosed
  | blockedByRepoLocalIntegrationDebt
  deriving DecidableEq, Repr

/--
Current P09 machine-anchor status.

This permits a serial public backfill of the theorem tree and leaf-budget ledger
only as an open formalization-debt record.  It is not a theorem-completion
claim.
-/
def publicBackfillMachineAnchorStatus : PublicBackfillMachineAnchorStatus :=
  PublicBackfillMachineAnchorStatus.settledFormalizationDebtNoExternalProof

/-- Checked P09 status: public backfill is based on formalization-debt closure, not proof closure. -/
theorem publicBackfillMachineAnchorStatus_eq_settledFormalizationDebtNoExternalProof :
    publicBackfillMachineAnchorStatus =
      PublicBackfillMachineAnchorStatus.settledFormalizationDebtNoExternalProof :=
  rfl

/--
P09 gate rows for a serial public-doc integrator.

The gate is positive only for integration-ready public documentation that keeps
the theorem open.  It does not upgrade the parent to a completed theorem state.
-/
def publicBackfillGateRows : List String := [
  "statement-shape artifact exists: Stage1.THMM0403.SimpleNondegenerateZeroFinitenessShape is a checked proposition boundary",
  "machine-anchor status is settled as formalization_debt / not_repo_local_closed: no terminal ESS/S-unit/Subspace theorem proof is locally closed",
  "external-anchor audit found no pin-ready terminal Lean 4 proof; P06 therefore records no external proof to pin/import/check",
  "repo_local_integration_debt is not retained as completion evidence: repoLocalIntegrationDebtRetained = false and no anchor-only proof is accepted",
  "public theorem-tree backfill must keep multiplicative-equation input, exceptional-subsum classification, finite-zero extraction, and recurrence closed-form bridge open",
  "public leaf-budget ledger may be serially merged only with unchecked/open leaves for the terminal proof packages"
]

/-- The P09 public-backfill gate currently records six rows. -/
theorem publicBackfillGateRows_length :
    publicBackfillGateRows.length = 6 :=
  rfl

/--
Integration-ready public theorem-tree package rows for `THM-M-0403-P09`.

These rows are stable planning metadata.  Rows marked open remain formalization
debt and must not be converted into checked public tasks without new
repo-local validation.
-/
def publicTheoremTreeBackfillRows : List (String × String × String) := [
  ("R", "open", "THM-M-0403 simple nondegenerate exponential-polynomial zero-finiteness statement shape"),
  ("R.A", "open", "ESS finite-rank multiplicative-group equation input over characteristic-zero fields"),
  ("R.B", "checked_statement_shape", "Stage1.THMM0403.SimpleNondegenerateZeroFinitenessShape and AwesomeTheorems.Stage1.S1_M_016.StatementShape"),
  ("R.C", "conditional_checked_bridge", "linearRecurrenceShape_of_simpleShape after RecurrenceNondegenerateData supplies a simple exponential-polynomial reduction"),
  ("R.D", "owned_by_S1_M_017", "Skolem-Mahler-Lech periodic / finite-union arithmetic-progression branch is not canonical for this slot"),
  ("R.E", "checked_special_cases", "oneTerm_zeroSet_finite and twoTerm_zeroSet_finite smoke-test wrappers"),
  ("R.F", "open", "public completion gate requiring local_proof_body, local_wrapper_upstream_mathlib, or external_upstream_pinned validation")
]

/-- The P09 theorem-tree backfill currently records seven rows. -/
theorem publicTheoremTreeBackfillRows_length :
    publicTheoremTreeBackfillRows.length = 7 :=
  rfl

/-! ## Audit probes retained in the checked file. -/

#check LinearRecurrence
#check LinearRecurrence.IsSolution
#check LinearRecurrence.geom_sol_iff_root_charPoly
#check IsOfFinOrder
#check isOfFinOrder_iff_pow_eq_one
#check Units.isOfFinOrder_val
#check rootsOfUnity
#check mem_rootsOfUnity
#check rootsOfUnity.mkOfPowEq
#check IsPrimitiveRoot
#check IsPrimitiveRoot.isOfFinOrder
#check isPrimitiveRoot_of_mem_rootsOfUnity
#check nonzeroRootRatioUnit
#check RootRatioNondegenerate
#check unit_isOfFinOrder_iff_exists_mem_rootsOfUnity
#check unit_not_isOfFinOrder_iff_forall_not_mem_rootsOfUnity
#check rootRatioNondegenerate_iff_ratio_nontorsion
#check rootRatioNondegenerate_of_data
#check rootRatioNondegenerate_iff_forall_not_mem_rootsOfUnity
#check rootRatioTorsionAPIAuditClosed_eq_true
#check rootRatioTorsionAPIReplacements
#check Set.Finite
#check Set.integer
#check Set.unit
#check Set.unit_valuation_eq_one
#check Set.unitEquivUnitsInteger
#check Group.FG
#check Subgroup.FG
#check Monoid.FG
#check NumberField.Units.rank
#check NumberField.Units.fundSystem
#check NumberField.Units.rank_modTorsion
#check NumberField.Units.closure_fundSystem_sup_torsion_eq_top
#check UnitsModTorsion
#check FiniteRankUnitGroupAPI
#check finiteRankUnitGroupAPI
#check hasFiniteRankSubgroupPlaceholderRetained_eq_false
#check finiteRankGroupAPIReplacements
#check Height.logHeight_nonneg
#check NumberField.logHeight₁_eq
#check NumberField.mulHeight₁_eq
#check NumberField.prod_abs_eq_one
#check NumberField.FinitePlace.prod_eq_inv_abs_norm
#check PublicTheoremTarget
#check canonicalPublicTheoremTarget
#check skolemMahlerLechPeriodicBranchOwnerSlot
#check skolemMahlerLechPeriodicBranchOwnedHere_eq_false
#check s1m017FiniteUnionAPStatementShapeName
#check s1m017EventuallyPeriodicStatementShapeName
#check skolemMahlerLechPeriodicBranchCoordinationRows
#check skolemMahlerLechPeriodicBranchCoordinationRows_length
#check fullLinearRecurrenceTheoremIsDeferredWrapper_eq_true
#check CanonicalPublicTheoremTargetShape
#check StatementShape
#check SimpleNondegenerateZeroFinitenessShape
#check oneTerm_zeroSet_empty
#check oneTerm_zeroSet_finite
#check twoTermUnitZeroSet
#check twoTermUnitZeroSet_subsingleton
#check twoTermUnitZeroSet_finite
#check twoTerm_eval_zero_iff_unitRatio
#check twoTerm_zeroSet_eq_unitZeroSet
#check twoTerm_zeroSet_finite
#check lowDimensionalSmokeTestWrappersClosed_eq_true
#check lowDimensionalSmokeTestWrappers_length
#check LinearRecurrenceZeroFinitenessShape
#check SchlickeweiEvertseProofPackage
#check schlickeweiEvertseProofPackageSplit
#check schlickeweiEvertseProofPackageSplit_length
#check repoLocalIntegrationDebtRetained_eq_false
#check repoLocalIntegrationDebtGate
#check SchlickeweiEvertseFormalizationDebt
#check PublicMathlibAnchorRow
#check publicMathlibAnchorTable
#check publicMathlibAnchorTable_length
#check ExternalLean4SearchRow
#check externalLean4ProjectSearchRows
#check externalLean4ProjectSearchRows_length
#check externalTerminalLean4ProofFound_eq_false
#check ExternalProofIntegrationStatus
#check externalProofIntegrationStatus
#check externalProofIntegrationStatus_eq_noExternalTerminalProofFound
#check externalProofIntegrationBlockers
#check externalProofIntegrationBlockers_length
#check p06RepoLocalIntegrationDebtGate
#check p06RepoLocalIntegrationDebtGate_length
#check PublicBackfillMachineAnchorStatus
#check publicBackfillMachineAnchorStatus
#check publicBackfillMachineAnchorStatus_eq_settledFormalizationDebtNoExternalProof
#check publicBackfillGateRows
#check publicBackfillGateRows_length
#check publicTheoremTreeBackfillRows
#check publicTheoremTreeBackfillRows_length

end AwesomeTheorems.Stage1.S1_M_016

/-!
## Public Stage1 theorem-name wrapper

The public blueprint asks for the theorem-UID namespace
`Stage1.THMM0403.SimpleNondegenerateZeroFinitenessShape`.  This wrapper keeps
the richer `AwesomeTheorems.Stage1.S1_M_016` artifact as the canonical payload
while exposing the checked statement-shape name requested by the Stage1 queue.
-/

namespace Stage1.THMM0403

universe u

abbrev ExponentialPolynomialData (K : Type u) [Field K] (r : ℕ) :=
  AwesomeTheorems.Stage1.S1_M_016.ExponentialPolynomialData K r

abbrev exponentialPolynomialZeroSet {K : Type u} [Field K] {r : ℕ}
    (D : ExponentialPolynomialData K r) : Set ℕ :=
  AwesomeTheorems.Stage1.S1_M_016.exponentialPolynomialZeroSet D

/--
Statement-only public wrapper for THM-M-0403 / Schlickewei--Evertse.

For every nonempty finite sum of nonzero simple exponential terms over a
characteristic-zero field, if all pairwise root quotients are not torsion, then
the zero-index set is finite.  This is a checked Lean proposition boundary, not
a proof of the Schlickewei--Evertse theorem.
-/
def SimpleNondegenerateZeroFinitenessShape (K : Type u) [Field K] [CharZero K] :
    Prop :=
  AwesomeTheorems.Stage1.S1_M_016.SimpleNondegenerateZeroFinitenessShape K

/-- The public UID wrapper is definitionally the existing `S1_M_016` shape. -/
theorem simpleNondegenerateZeroFinitenessShape_iff_s1_m_016
    (K : Type u) [Field K] [CharZero K] :
    SimpleNondegenerateZeroFinitenessShape K ↔
      AwesomeTheorems.Stage1.S1_M_016.SimpleNondegenerateZeroFinitenessShape K :=
  Iff.rfl

abbrev PublicMathlibAnchorRow :=
  AwesomeTheorems.Stage1.S1_M_016.PublicMathlibAnchorRow

/--
Import-audit rows supporting the public wrapper name.

These rows are metadata only: they record checked local imports and probes, not
a terminal ESS/S-unit or Schlickewei--Evertse proof anchor.
-/
def importAuditAnchorTable : List PublicMathlibAnchorRow :=
  AwesomeTheorems.Stage1.S1_M_016.publicMathlibAnchorTable

/-- The public import-audit table reuses the seven checked internal rows. -/
theorem importAuditAnchorTable_length :
    importAuditAnchorTable.length = 7 :=
  rfl

/-! Audit probes for the public wrapper namespace. -/

#check ExponentialPolynomialData
#check exponentialPolynomialZeroSet
#check SimpleNondegenerateZeroFinitenessShape
#check simpleNondegenerateZeroFinitenessShape_iff_s1_m_016
#check importAuditAnchorTable
#check importAuditAnchorTable_length

end Stage1.THMM0403
