import Mathlib.Algebra.BrauerGroup.Defs
import Mathlib.Algebra.Azumaya.Basic
import Mathlib.Algebra.Azumaya.Matrix
import Mathlib.Algebra.Group.Defs
import Mathlib.RingTheory.SimpleModule.WedderburnArtin
import Mathlib.RingTheory.Artinian.Module
import Mathlib.RingTheory.TensorProduct.Basic
import Mathlib.RingTheory.Morita.Matrix

/-!
# S1-M-078 / THM-M-0424: Brauer group statement boundary

This file records the part of the central-simple-algebra classification boundary
that is already available in the local mathlib closure:

* `CSA K`, `IsBrauerEquivalent`, and `BrauerGroup K` as a quotient by Brauer
  equivalence.
* a checked quotient wrapper saying equality of normalized Brauer classes is
  exactly Brauer equivalence.
* a checked Wedderburn-Artin wrapper: every finite-dimensional central simple
  algebra over a field is isomorphic to a matrix algebra over a finite
  division algebra.
* a checked audit boundary for `Mathlib.Algebra.Azumaya.*`: mathlib has the
  Azumaya predicate and basic base/matrix/equivalence-transfer anchors, but not
  a commutative-ring Brauer quotient/group.

It deliberately does not claim a full Brauer-group classification theorem:
mathlib's Brauer-group file currently leaves the group law, functoriality, and
Morita-equivalence characterization as TODOs.  The Azumaya generalization is
therefore recorded as a separate target interface rather than as part of the
field-CSA terminal theorem in this slot.
-/

noncomputable section

universe u v

namespace AwesomeTheorems.Stage1.S1_M_078

variable {K : Type u} [Field K]

/-- The canonical Brauer class of a central simple algebra in mathlib's quotient model. -/
abbrev BrauerClass (A : CSA.{u, v} K) : BrauerGroup K :=
  Quotient.mk (Brauer.CSA_Setoid K) A

/-- Brauer-equivalent central simple algebras define the same quotient class. -/
theorem brauerClass_eq_of_isBrauerEquivalent {A B : CSA.{u, v} K}
    (h : IsBrauerEquivalent A B) : BrauerClass A = BrauerClass B :=
  Quotient.sound h

/-- Equality in mathlib's Brauer quotient recovers Brauer equivalence. -/
theorem isBrauerEquivalent_of_brauerClass_eq {A B : CSA.{u, v} K}
    (h : BrauerClass A = BrauerClass B) : IsBrauerEquivalent A B :=
  Quotient.exact h

/-- The quotient statement of Brauer classification available directly from mathlib's setoid. -/
theorem brauerClass_eq_iff_isBrauerEquivalent (A B : CSA.{u, v} K) :
    BrauerClass A = BrauerClass B ↔ IsBrauerEquivalent A B :=
  ⟨isBrauerEquivalent_of_brauerClass_eq, brauerClass_eq_of_isBrauerEquivalent⟩

/--
The narrow Stage1 terminal target that is currently repo-locally checkable:
classification by equality in mathlib's quotient of central simple algebras by
Brauer equivalence.

This deliberately excludes the future tensor-product group law, Morita bridge,
and arithmetic/cohomological classifications.
-/
def QuotientClassificationTarget : Prop :=
  ∀ (K : Type u) [Field K], ∀ A B : CSA.{u, v} K,
    BrauerClass A = BrauerClass B ↔ IsBrauerEquivalent A B

/-- The quotient-classification target is validated by the local quotient wrappers. -/
theorem checked_quotient_classification_target : QuotientClassificationTarget := by
  intro K hK A B
  letI : Field K := hK
  exact brauerClass_eq_iff_isBrauerEquivalent A B

/--
Checked Wedderburn-Artin normal form for a finite-dimensional central simple algebra.

The `IsArtinianRing` instance is obtained locally from finite-dimensionality over
the base field; the proof body is mathlib's finite Artin-Wedderburn theorem.
-/
theorem csa_wedderburn_artin_finite (A : CSA.{u, v} K) :
    ∃ (n : ℕ) (_ : NeZero n) (D : Type v) (_ : DivisionRing D) (_ : Algebra K D)
      (_ : Module.Finite K D), Nonempty (A ≃ₐ[K] Matrix (Fin n) (Fin n) D) := by
  letI : IsArtinianRing A := IsArtinianRing.of_finite K A
  exact IsSimpleRing.exists_algEquiv_matrix_divisionRing_finite K A

/--
The mathlib-compatible data still missing for the tensor-product part of the
Brauer-group TODO.

The `mul` field is the intended tensor product operation on `CSA K`.  The
`mul_equiv_tensor` field records that the selected central simple algebra has
the expected underlying `K`-algebra, namely `A ⊗[K] B`.  The `congr` field is
the well-definedness theorem needed to descend this operation to the quotient
`BrauerGroup K`.

This structure is deliberately data, not an instance or an assumption: the current
local mathlib closure does not yet prove that `A ⊗[K] B` is again central
simple for arbitrary `CSA K` objects.
-/
structure CSATensorProductData where
  /-- The intended tensor-product operation on central simple algebras. -/
  mul : CSA.{u, v} K → CSA.{u, v} K → CSA.{u, v} K
  /-- The operation is represented by the ordinary algebra tensor product. -/
  mul_equiv_tensor :
    ∀ A B : CSA.{u, v} K, Nonempty ((mul A B : Type v) ≃ₐ[K] TensorProduct K A B)
  /-- The operation respects Brauer equivalence in both inputs. -/
  congr : ∀ {A A' B B' : CSA.{u, v} K},
    IsBrauerEquivalent A A' → IsBrauerEquivalent B B' →
      IsBrauerEquivalent (mul A B) (mul A' B')

namespace CSATensorProductData

/-- A packaged tensor product operation respects Brauer equivalence in the left input. -/
theorem congr_left (data : CSATensorProductData (K := K)) {A A' B : CSA.{u, v} K}
    (hA : IsBrauerEquivalent A A') :
    IsBrauerEquivalent (data.mul A B) (data.mul A' B) :=
  data.congr hA (IsBrauerEquivalent.refl B)

/-- A packaged tensor product operation respects Brauer equivalence in the right input. -/
theorem congr_right (data : CSATensorProductData (K := K)) {A B B' : CSA.{u, v} K}
    (hB : IsBrauerEquivalent B B') :
    IsBrauerEquivalent (data.mul A B) (data.mul A B') :=
  data.congr (IsBrauerEquivalent.refl A) hB

/--
Any completed tensor-product package descends to a binary operation on the
Brauer quotient.
-/
def brauerMul (data : CSATensorProductData (K := K)) :
    BrauerGroup K → BrauerGroup K → BrauerGroup K :=
  Quotient.lift₂ (fun A B => BrauerClass (data.mul A B)) (by
    intro A A' B B' hA hB
    exact brauerClass_eq_of_isBrauerEquivalent (data.congr hA hB))

/-- The descended quotient operation is represented by `data.mul` on quotient representatives. -/
theorem brauerMul_mk (data : CSATensorProductData (K := K)) (A B : CSA.{u, v} K) :
    data.brauerMul (BrauerClass A) (BrauerClass B) = BrauerClass (data.mul A B) :=
  rfl

end CSATensorProductData

/--
The complete data needed to turn mathlib's quotient `BrauerGroup K` into the
classical abelian Brauer group.

This extends the tensor-product descent interface with the group structure and
the representative-level compatibility expected of the classical construction:

* multiplication is represented by tensor product of central simple algebras;
* the unit is represented by the base field;
* inversion is represented by the opposite algebra;
* associativity, unit laws, inverse laws, and commutativity are supplied by the
  `CommGroup (BrauerGroup K)` field.

The structure is intentionally a target interface rather than an inhabitant.
The local mathlib closure only defines `BrauerGroup K` as a quotient and marks
the abelian group law as a TODO.
-/
structure BrauerGroupAbelianLawData extends CSATensorProductData.{u, v} (K := K) where
  /-- A representative for the unit class.  Classically this is the base field `K`. -/
  oneRep : CSA.{u, v} K
  /-- The selected unit representative is algebra-equivalent to the base field. -/
  oneRep_equiv_base : Nonempty ((oneRep : Type v) ≃ₐ[K] K)
  /-- A representative for the inverse of a Brauer class.  Classically this is `Aᵐᵒᵖ`. -/
  invRep : CSA.{u, v} K → CSA.{u, v} K
  /-- The selected inverse representative is algebra-equivalent to the opposite algebra. -/
  invRep_equiv_opposite :
    ∀ A : CSA.{u, v} K, Nonempty ((invRep A : Type v) ≃ₐ[K] MulOpposite A)
  /-- The intended abelian group structure on the Brauer quotient. -/
  [commGroup : CommGroup (BrauerGroup K)]
  /-- The group multiplication agrees with the descended tensor-product operation on classes. -/
  mul_mk :
    ∀ A B : CSA.{u, v} K, BrauerClass A * BrauerClass B = BrauerClass (mul A B)
  /-- The group unit is represented by `oneRep`. -/
  one_mk : (1 : BrauerGroup K) = BrauerClass oneRep
  /-- The group inverse is represented by `invRep`. -/
  inv_mk : ∀ A : CSA.{u, v} K, (BrauerClass A)⁻¹ = BrauerClass (invRep A)

namespace BrauerGroupAbelianLawData

attribute [instance] commGroup

/-- A completed abelian-law package supplies a checked `CommGroup` instance on `BrauerGroup K`. -/
@[reducible]
def toCommGroup (data : BrauerGroupAbelianLawData (K := K)) : CommGroup (BrauerGroup K) :=
  data.commGroup

/-- The packaged group multiplication agrees with the quotient descent from tensor data. -/
theorem mul_eq_brauerMul (data : BrauerGroupAbelianLawData (K := K))
    (A B : CSA.{u, v} K) :
    (letI := data.commGroup;
      BrauerClass A * BrauerClass B = data.toCSATensorProductData.brauerMul
        (BrauerClass A) (BrauerClass B)) := by
  letI := data.commGroup
  rw [CSATensorProductData.brauerMul_mk, data.mul_mk]

/-- The packaged group operation is commutative on representative classes. -/
theorem mul_comm_mk (data : BrauerGroupAbelianLawData (K := K))
    (A B : CSA.{u, v} K) :
    (letI := data.commGroup;
      BrauerClass A * BrauerClass B = BrauerClass B * BrauerClass A) := by
  letI := data.commGroup
  simpa using mul_comm (BrauerClass A) (BrauerClass B)

/-- The packaged group operation is associative on representative classes. -/
theorem mul_assoc_mk (data : BrauerGroupAbelianLawData (K := K))
    (A B C : CSA.{u, v} K) :
    (letI := data.commGroup;
      (BrauerClass A * BrauerClass B) * BrauerClass C =
        BrauerClass A * (BrauerClass B * BrauerClass C)) := by
  letI := data.commGroup
  simpa using mul_assoc (BrauerClass A) (BrauerClass B) (BrauerClass C)

/-- The packaged unit law holds on representative classes. -/
theorem one_mul_mk (data : BrauerGroupAbelianLawData (K := K))
    (A : CSA.{u, v} K) :
    (letI := data.commGroup;
      (1 : BrauerGroup K) * BrauerClass A = BrauerClass A) := by
  letI := data.commGroup
  simp

/-- The packaged inverse law holds on representative classes. -/
theorem inv_mul_cancel_mk (data : BrauerGroupAbelianLawData (K := K))
    (A : CSA.{u, v} K) :
    (letI := data.commGroup;
      (BrauerClass A)⁻¹ * BrauerClass A = 1) := by
  letI := data.commGroup
  simp

end BrauerGroupAbelianLawData

/-- Morita equivalence for the underlying `K`-algebras of two central simple algebras. -/
abbrev IsCSAMoritaEquivalent (A B : CSA.{u, v} K) : Prop :=
  IsMoritaEquivalent K A B

namespace IsCSAMoritaEquivalent

/--
One checked half of the Morita bridge promised by mathlib's Brauer-group TODO:
Brauer equivalence of central simple algebras implies Morita equivalence of the
underlying `K`-algebras.

The proof uses mathlib's Morita equivalence between an algebra and a full matrix
algebra, plus the algebra equivalence supplied by `IsBrauerEquivalent`.
-/
theorem of_isBrauerEquivalent {A B : CSA.{u, v} K}
    (h : IsBrauerEquivalent A B) : IsCSAMoritaEquivalent A B := by
  obtain ⟨n, m, hn, hm, ⟨e⟩⟩ := h
  haveI : Nonempty (Fin n) := Fin.pos_iff_nonempty.mp (Nat.pos_of_ne_zero hn)
  haveI : Nonempty (Fin m) := Fin.pos_iff_nonempty.mp (Nat.pos_of_ne_zero hm)
  have hA : IsMoritaEquivalent K A (Matrix (Fin n) (Fin n) A) :=
    IsMoritaEquivalent.matrix K (R := A)
  have hAB :
      IsMoritaEquivalent K (Matrix (Fin n) (Fin n) A) (Matrix (Fin m) (Fin m) B) :=
    IsMoritaEquivalent.of_algEquiv (R := K) e
  have hB : IsMoritaEquivalent K (Matrix (Fin m) (Fin m) B) B :=
    (IsMoritaEquivalent.matrix K (R := B)).symm
  exact IsMoritaEquivalent.trans K (IsMoritaEquivalent.trans K hA hAB) hB

end IsCSAMoritaEquivalent

/--
The complete Morita-equivalence characterization still missing from mathlib's
Brauer-group TODO.

The forward implication is locally checked as
`IsCSAMoritaEquivalent.of_isBrauerEquivalent`.  The reverse implication is the
remaining formalization target: over a field, Morita-equivalent finite
central-simple algebras should be Brauer equivalent in the matrix-algebra sense
used by `IsBrauerEquivalent`.
-/
structure BrauerMoritaEquivalenceData where
  /-- Brauer-equivalent central simple algebras are Morita equivalent. -/
  toMorita :
    ∀ {A B : CSA.{u, v} K}, IsBrauerEquivalent A B → IsCSAMoritaEquivalent A B
  /-- Morita-equivalent central simple algebras are Brauer equivalent. -/
  toBrauer :
    ∀ {A B : CSA.{u, v} K}, IsCSAMoritaEquivalent A B → IsBrauerEquivalent A B

namespace BrauerMoritaEquivalenceData

/-- A completed Morita bridge gives the promised iff characterization. -/
theorem iff (data : BrauerMoritaEquivalenceData.{u, v} (K := K)) (A B : CSA.{u, v} K) :
    IsBrauerEquivalent A B ↔ IsCSAMoritaEquivalent A B :=
  ⟨fun h => data.toMorita h, fun h => data.toBrauer h⟩

/-- The locally checked forward implication can fill the forward field of the target data. -/
theorem checked_toMorita {A B : CSA.{u, v} K} (h : IsBrauerEquivalent A B) :
    IsCSAMoritaEquivalent A B :=
  IsCSAMoritaEquivalent.of_isBrauerEquivalent h

end BrauerMoritaEquivalenceData

/--
The precise local formalization gap for the tensor-product backfill task.

Producing an inhabitant of this proposition requires a repo-local proof that
the tensor product of two `CSA K` objects can be packaged as a `CSA K` object
and that this packaging respects `IsBrauerEquivalent`.
-/
def CSATensorProductOperationExists : Prop :=
  Nonempty (CSATensorProductData.{u, v} (K := K))

/--
The precise local formalization gap for the abelian-group backfill task.

Producing an inhabitant of this proposition requires first closing the tensor
product `CSA K` package and then proving that the descended operation has the
base-field unit, opposite-algebra inverse, associativity, and commutativity
needed for `CommGroup (BrauerGroup K)`.
-/
def BrauerGroupAbelianLawExists : Prop :=
  Nonempty (BrauerGroupAbelianLawData.{u, v} (K := K))

/--
The precise local formalization gap for the Morita-characterization backfill
task.

Producing an inhabitant requires the reverse implication from
`IsCSAMoritaEquivalent A B` to `IsBrauerEquivalent A B`; the forward implication
is already checked by `IsCSAMoritaEquivalent.of_isBrauerEquivalent`.
-/
def BrauerMoritaEquivalenceExists : Prop :=
  Nonempty (BrauerMoritaEquivalenceData.{u, v} (K := K))

section AzumayaAudit

variable (R : Type u) [CommRing R]

/--
The repo-local anchors currently available from `Mathlib.Algebra.Azumaya.*`.

They cover the defining Azumaya predicate, the base algebra, matrix algebras, and
transport across algebra equivalence.  They do not define a quotient relation or
a group of Azumaya classes over a commutative ring.
-/
def ExistingAzumayaAnchors : Prop :=
  IsAzumaya R R ∧
    (∀ (n : Type v) [Fintype n] [DecidableEq n] [Nonempty n],
      IsAzumaya R (Matrix n n R)) ∧
    (∀ (A B : Type v) [Ring A] [Ring B] [Algebra R A] [Algebra R B],
      IsAzumaya R A → (A ≃ₐ[R] B) → IsAzumaya R B)

/-- The audited Azumaya anchors from mathlib compile in the local closure. -/
theorem checked_existing_azumaya_anchors : ExistingAzumayaAnchors.{u, v} R := by
  refine ⟨IsAzumaya.id R, ?_, ?_⟩
  · intro n _ _ _
    exact IsAzumaya.matrix R n
  · intro A B _ _ _ _ hA e
    letI : IsAzumaya R A := hA
    exact IsAzumaya.of_AlgEquiv R A B e

/--
Target interface for a future commutative-ring Brauer group built from Azumaya
algebras.

This is intentionally separate from `BrauerGroup K`, which mathlib defines only
for fields as a quotient of central simple algebras.  An inhabitant would need
to choose the quotient/group object, its class map for Azumaya algebras, the
tensor product law, the base class, and the theorem that matrix Azumaya algebras
represent the neutral class.
-/
structure AzumayaBrauerGroupGeneralizationData where
  /-- The intended Brauer group of Azumaya algebras over `R`. -/
  BrAz : Type u
  /-- The class of an Azumaya `R`-algebra. -/
  classOf : (A : Type u) → [Ring A] → [Algebra R A] → IsAzumaya R A → BrAz
  /-- The group law should be induced by tensor product over `R`. -/
  [commGroup : CommGroup BrAz]
  /-- The neutral class is represented by the base algebra `R`. -/
  one_eq_base : (1 : BrAz) = classOf R (IsAzumaya.id R)
  /-- Matrix Azumaya algebras should represent the neutral Brauer class. -/
  matrix_eq_one :
    ∀ (n : Type u) [Fintype n] [DecidableEq n] [Nonempty n],
      classOf (Matrix n n R) (IsAzumaya.matrix R n) = 1

/--
The formalization gap for the commutative-ring Azumaya generalization.

This belongs in a separate child theorem from the field-level `BrauerGroup K`
slot unless the public terminal target is explicitly broadened beyond central
simple algebras over fields.
-/
def AzumayaBrauerGroupGeneralizationExists : Prop :=
  Nonempty (AzumayaBrauerGroupGeneralizationData.{u} R)

end AzumayaAudit

/--
External Lean 4 Brauer-proof audit for `S1-M-078-C008`.

This audit records only integration-relevant evidence.  It is not a proof of the
terminal Brauer-group theorem and it does not treat anchor-only search hits as a
completed machine-checked dependency.
-/
def c008ExternalLean4BrauerProofAudit_2026_05_01 : List String := [
  "pinned local mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95 provides Mathlib.Algebra.BrauerGroup.Defs with CSA, IsBrauerEquivalent, Brauer.CSA_Setoid, and BrauerGroup",
  "pinned local mathlib BrauerGroup is a quotient-definition anchor only for the full theorem; the audited file still leaves group law, functoriality, and Morita characterization as TODO-level work",
  "repo-local wrapper theorems brauerClass_eq_iff_isBrauerEquivalent, csa_wedderburn_artin_finite, IsCSAMoritaEquivalent.of_isBrauerEquivalent, and checked_existing_azumaya_anchors compile in this file",
  "GitHub CLI authentication is unavailable in this worker environment, so authenticated GitHub code search could not be rerun here",
  "web/source search for Lean 4 BrauerGroup, IsBrauerEquivalent, central simple algebra, and Mathlib.Algebra.BrauerGroup.Defs found no external non-mathlib Lean 4 proof body with repository URL, commit, module path, and theorem name",
  "no external Lean 4 Brauer-group proof candidate is currently available to pin, import, and check in this repository"
]

/--
`S1-M-078-C008` pin/import/check gate.

If a future audit finds an external Lean 4 Brauer-group proof, this gate must be
replaced by a concrete Lake dependency/import/check attempt, or by a blocker
that names the exact dependency, theorem, license, toolchain, or API conflict.
-/
def c008ExternalProofIntegrationGate : List String := [
  "C008 status on 2026-05-01: no external non-mathlib Lean 4 Brauer-group proof body was found",
  "no pin/import/check task is created because there is no candidate project URL, commit, module path, theorem name, license, and proof body to integrate",
  "if a candidate is later found, record repository URL, license, commit hash, module path, theorem name, lean-toolchain, lakefile, dependency compatibility with mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95, and proof-placeholder audit",
  "then either pin/import/check the candidate in this repository or record a concrete blocker such as toolchain mismatch, dependency conflict, license incompatibility, missing theorem endpoint, or untrusted constants in the closure",
  "anchor-only evidence is not completion evidence; keep S1-M-078 open until repo-local validation passes for the selected terminal theorem target",
  "current machine status remains not_repo_local_closed for the terminal theorem, with formalization_debt rather than completed repo_local_integration_debt"
]

/-- No external proof was available in this child pass, so no C008 dependency task was opened. -/
def c008PinImportCheckTaskCreated : Bool := false

/-- This child does not retain repo-local integration debt in any completed theorem state. -/
def c008RepoLocalIntegrationDebtRetainedInCompletedState : Bool := false

theorem c008_no_completed_repoLocalIntegrationDebt :
    c008RepoLocalIntegrationDebtRetainedInCompletedState = false := rfl

/--
Stage1 statement-shape candidate for the currently checkable mathlib boundary of
"classification of central simple algebras by the Brauer group".

The first conjunct is the quotient classification by Brauer equivalence.  The
second conjunct is the Wedderburn-Artin matrix-over-division-algebra normal form.
The terminal theorem still needs the Brauer group law, inverse/tensor-product
classification, Morita-equivalence bridge, and any desired cohomological
classification layer.
-/
def StatementShape : Prop :=
  ∀ (K : Type u) [Field K],
    (∀ A B : CSA.{u, v} K, BrauerClass A = BrauerClass B ↔ IsBrauerEquivalent A B) ∧
      (∀ A : CSA.{u, v} K,
        ∃ (n : ℕ) (_ : NeZero n) (D : Type v) (_ : DivisionRing D) (_ : Algebra K D)
          (_ : Module.Finite K D), Nonempty (A ≃ₐ[K] Matrix (Fin n) (Fin n) D))

/--
The locally checked part of the statement-shape boundary.

This is not a proof of the full Brauer-group theorem advertised by the Stage1
slot; it packages only the quotient and Wedderburn-Artin facts audited above.
-/
theorem checked_mathlib_classification_boundary : StatementShape := by
  intro K hK
  letI : Field K := hK
  exact ⟨brauerClass_eq_iff_isBrauerEquivalent, csa_wedderburn_artin_finite⟩

end AwesomeTheorems.Stage1.S1_M_078
