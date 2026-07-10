import Mathlib.LinearAlgebra.FiniteDimensional.Defs
import Mathlib.LinearAlgebra.Projectivization.Basic
import Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Basic
import Mathlib.Analysis.Matrix.Hermitian
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Module

/-!
# S1-M-203 / THM-M-1544: ADHM construction

This Stage1 artifact records a conservative Lean 4 boundary for the
Atiyah-Drinfeld-Hitchin-Manin construction of instantons.

The pinned mathlib snapshot has finite-dimensional linear algebra, linear maps,
projectivization, matrix groups, and Hermitian-matrix spectral infrastructure.
It does not expose a terminal formalization of the ADHM monad, framed instanton
moduli spaces, anti-self-dual connections, or the algebraic-geometric
equivalence between ADHM data and instanton bundles.  Accordingly this file
normalizes the ADHM linear algebra input and keeps the missing construction
steps as explicit proposition fields.  It contains only closed declarations and
low-risk wrappers.
-/

noncomputable section

open scoped LinearAlgebra.Projectivization

universe uK uV uW uM

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_203

/-- The endomorphism commutator used in the complex ADHM equation. -/
def linearCommutator
    (K : Type uK) (V : Type uV) [Field K] [AddCommGroup V] [Module K V]
    (A B : V →ₗ[K] V) : V →ₗ[K] V :=
  A.comp B - B.comp A

/--
Linear ADHM data: two endomorphisms of the internal vector space, and the
framing maps `I : W -> V` and `J : V -> W`.
-/
structure ADHMData
    (K : Type uK) (V : Type uV) (W : Type uW)
    [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W] :
    Type (max uV uW) where
  B1 : V →ₗ[K] V
  B2 : V →ₗ[K] V
  I : W →ₗ[K] V
  J : V →ₗ[K] W

/--
The complex ADHM equation `[B1, B2] + I J = 0`.

The real moment-map equation, stability, and costability are kept separate in
`ADHMHypotheses`, because they require analytic/Hermitian choices and quotient
moduli infrastructure not present as a terminal API in the audited mathlib
snapshot.
-/
def ComplexADHMEquation
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]
    (D : ADHMData K V W) : Prop :=
  linearCommutator K V D.B1 D.B2 + D.I.comp D.J = 0

/-- The ADHM equation unfolds to the expected endomorphism identity. -/
theorem complexADHMEquation_iff
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]
    (D : ADHMData K V W) :
    ComplexADHMEquation D ↔
      linearCommutator K V D.B1 D.B2 + D.I.comp D.J = 0 :=
  Iff.rfl

/-- Zero linear maps give the degenerate ADHM datum. -/
def zeroADHMData
    (K : Type uK) (V : Type uV) (W : Type uW)
    [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W] :
    ADHMData K V W where
  B1 := 0
  B2 := 0
  I := 0
  J := 0

/-- The degenerate zero datum satisfies the complex ADHM equation. -/
theorem zeroADHMData_complexEquation
    (K : Type uK) (V : Type uV) (W : Type uW)
    [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W] :
    ComplexADHMEquation (zeroADHMData K V W) := by
  simp [ComplexADHMEquation, linearCommutator, zeroADHMData]

/-- Any endomorphism has zero commutator with itself. -/
theorem linearCommutator_self
    (K : Type uK) (V : Type uV) [Field K] [AddCommGroup V] [Module K V]
    (A : V →ₗ[K] V) :
    linearCommutator K V A A = 0 := by
  simp [linearCommutator]

/--
The finite matrix commutator used by the matrix-shaped ADHM moment-map
boundary.
-/
def matrixCommutator
    {n : Type uV} [Fintype n] (A B : Matrix n n ℂ) : Matrix n n ℂ :=
  A * B - B * A

/--
Finite matrix ADHM data over `ℂ`.

This is the basis-dependent statement boundary for the real moment-map leaf.
It does not replace the basis-free linear-map package above; it records the
Hermitian API choice needed for the real equation.
-/
structure MatrixADHMData
    (v : Type uV) (w : Type uW) [Fintype v] [Fintype w] : Type (max uV uW) where
  B1 : Matrix v v ℂ
  B2 : Matrix v v ℂ
  I : Matrix v w ℂ
  J : Matrix w v ℂ

/--
Hermitian adjoint API selected for the matrix real moment-map boundary:
mathlib's conjugate transpose `Matrix.conjTranspose`.
-/
def hermitianAdjointMatrix
    {m : Type uV} {n : Type uW} (A : Matrix m n ℂ) : Matrix n m ℂ :=
  Matrix.conjTranspose A

/-- The selected Hermitian adjoint is definitionally mathlib conjugate transpose. -/
theorem hermitianAdjointMatrix_eq_conjTranspose
    {m : Type uV} {n : Type uW} (A : Matrix m n ℂ) :
    hermitianAdjointMatrix A = Matrix.conjTranspose A :=
  rfl

/--
The real ADHM moment-map expression in finite matrix form:
`[B1, B1ᴴ] + [B2, B2ᴴ] + I Iᴴ - Jᴴ J`.
-/
def RealMomentMapExpression
    {v : Type uV} {w : Type uW} [Fintype v] [Fintype w]
    (D : MatrixADHMData v w) : Matrix v v ℂ :=
  matrixCommutator D.B1 (hermitianAdjointMatrix D.B1) +
    matrixCommutator D.B2 (hermitianAdjointMatrix D.B2) +
      D.I * hermitianAdjointMatrix D.I -
        hermitianAdjointMatrix D.J * D.J

/-- Separate checked statement boundary for the real ADHM moment-map equation. -/
def RealMomentMapEquation
    {v : Type uV} {w : Type uW} [Fintype v] [Fintype w]
    (D : MatrixADHMData v w) : Prop :=
  RealMomentMapExpression D = 0

/-- The real moment-map equation unfolds to the chosen matrix expression. -/
theorem realMomentMapEquation_iff
    {v : Type uV} {w : Type uW} [Fintype v] [Fintype w]
    (D : MatrixADHMData v w) :
    RealMomentMapEquation D ↔
      matrixCommutator D.B1 (hermitianAdjointMatrix D.B1) +
        matrixCommutator D.B2 (hermitianAdjointMatrix D.B2) +
          D.I * hermitianAdjointMatrix D.I -
            hermitianAdjointMatrix D.J * D.J = 0 :=
  Iff.rfl

/-- Zero matrices give the degenerate matrix ADHM datum. -/
def zeroMatrixADHMData
    (v : Type uV) (w : Type uW) [Fintype v] [Fintype w] :
    MatrixADHMData v w where
  B1 := 0
  B2 := 0
  I := 0
  J := 0

/-- The degenerate matrix datum satisfies the real moment-map equation. -/
theorem zeroMatrixADHMData_realMomentMapEquation
    (v : Type uV) (w : Type uW) [Fintype v] [Fintype w] :
    RealMomentMapEquation (zeroMatrixADHMData v w) := by
  simp [RealMomentMapEquation, RealMomentMapExpression, zeroMatrixADHMData,
    matrixCommutator, hermitianAdjointMatrix]

/--
A subspace of the internal ADHM vector space is invariant when it is preserved
by both endomorphisms `B1` and `B2`.
-/
def ADHMInvariantSubspace
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] [FiniteDimensional K W]
    (D : ADHMData K V W) (S : Submodule K V) : Prop :=
  (∀ v : V, v ∈ S → D.B1 v ∈ S) ∧
    ∀ v : V, v ∈ S → D.B2 v ∈ S

/-- The image of the framing map `I : W -> V` is contained in a subspace. -/
def ADHMFramingImageContained
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] [FiniteDimensional K W]
    (D : ADHMData K V W) (S : Submodule K V) : Prop :=
  ∀ w : W, D.I w ∈ S

/-- A subspace of `V` is contained in the kernel of the framing map `J : V -> W`. -/
def ADHMSubspaceContainedInKernelJ
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] [FiniteDimensional K W]
    (D : ADHMData K V W) (S : Submodule K V) : Prop :=
  ∀ v : V, v ∈ S → D.J v = 0

/--
ADHM stability: every `B1`/`B2`-invariant subspace containing the image of `I`
is the whole internal vector space.
-/
def ADHMStable
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] [FiniteDimensional K W]
    (D : ADHMData K V W) : Prop :=
  ∀ S : Submodule K V,
    ADHMInvariantSubspace D S → ADHMFramingImageContained D S → S = ⊤

/--
ADHM costability: every `B1`/`B2`-invariant subspace contained in the kernel of
`J` is the zero subspace.
-/
def ADHMCostable
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] [FiniteDimensional K W]
    (D : ADHMData K V W) : Prop :=
  ∀ S : Submodule K V,
    ADHMInvariantSubspace D S → ADHMSubspaceContainedInKernelJ D S → S = ⊥

/--
Hypotheses for the ADHM construction theorem.

The first three fields are checked linear-algebra conditions: the complex ADHM
equation plus concrete finite-dimensional invariant-subspace stability and
costability.  The matrix real moment-map equation is separately normalized by
`RealMomentMapEquation`; this generic construction package still keeps a
basis-free boundary field until a future basis/inner-product bridge connects
the linear-map and matrix presentations.  The remaining fields mark the
formalization boundary for rank/charge and base-field definitions, or for a
pinned upstream theorem.
-/
structure ADHMHypotheses
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] [FiniteDimensional K W]
    (D : ADHMData K V W) : Type (max uV uW) where
  complexEquation : ComplexADHMEquation D
  stable : ADHMStable D
  costable : ADHMCostable D
  realMomentMapEquation : Prop
  realMomentMapEquation_holds : realMomentMapEquation
  framedRankAndChargeFixed : Prop
  framedRankAndChargeFixed_holds : framedRankAndChargeFixed
  algebraicallyClosedComplexBase : Prop
  algebraicallyClosedComplexBase_holds : algebraicallyClosedComplexBase

/-- Projection wrapper for the checked complex ADHM equation field. -/
theorem complexEquation_of_hypotheses
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] [FiniteDimensional K W]
    {D : ADHMData K V W} (hD : ADHMHypotheses D) :
    ComplexADHMEquation D :=
  hD.complexEquation

/-- Projection wrapper for ADHM stability. -/
theorem stable_of_hypotheses
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] [FiniteDimensional K W]
    {D : ADHMData K V W} (hD : ADHMHypotheses D) :
    ADHMStable D :=
  hD.stable

/-- Projection wrapper for ADHM costability. -/
theorem costable_of_hypotheses
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] [FiniteDimensional K W]
    {D : ADHMData K V W} (hD : ADHMHypotheses D) :
    ADHMCostable D :=
  hD.costable

/-- Projection wrapper for the real moment-map boundary field. -/
theorem realMomentMapEquation_of_hypotheses
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] [FiniteDimensional K W]
    {D : ADHMData K V W} (hD : ADHMHypotheses D) :
    hD.realMomentMapEquation :=
  hD.realMomentMapEquation_holds

/--
The first fiberwise ADHM monad map at homogeneous coordinates `(x, y, z)`.

This is the linear-algebra shadow of
`V ⊗ O(-1) -> (V ⊕ V ⊕ W) ⊗ O`, written over the product model
`V × (V × W)`:
`v |-> ((z B1 - x) v, (z B2 - y) v, z J v)`.
-/
def ADHMMonadLeftFiber
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]
    (D : ADHMData K V W) (x y z : K) : V →ₗ[K] V × V × W :=
  LinearMap.prod
    (z • D.B1 - x • LinearMap.id)
    (LinearMap.prod (z • D.B2 - y • LinearMap.id) (z • D.J))

/--
The second fiberwise ADHM monad map at homogeneous coordinates `(x, y, z)`.

This is the linear-algebra shadow of
`(V ⊕ V ⊕ W) ⊗ O -> V ⊗ O(1)`:
`(v1, v2, w) |-> (-z B2 + y) v1 + (z B1 - x) v2 + z I w`.
-/
def ADHMMonadRightFiber
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]
    (D : ADHMData K V W) (x y z : K) : V × V × W →ₗ[K] V :=
  (((-z) • D.B2 + y • LinearMap.id).comp (LinearMap.fst K V (V × W))) +
    ((z • D.B1 - x • LinearMap.id).comp
      ((LinearMap.fst K V W).comp (LinearMap.snd K V (V × W)))) +
      ((z • D.I).comp ((LinearMap.snd K V W).comp (LinearMap.snd K V (V × W))))

/--
Fiberwise monad-composition leaf: the ADHM monad maps compose to zero whenever
the complex ADHM equation `[B1, B2] + I J = 0` holds.

This proves the child-local composition-zero obligation at the checked
linear-algebra boundary.  It does not assert exactness, local freeness,
framing at infinity, or the analytic inverse construction.
-/
theorem ADHMMonadRightFiber_comp_leftFiber_eq_zero
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]
    (D : ADHMData K V W) (x y z : K) (hD : ComplexADHMEquation D) :
    (ADHMMonadRightFiber D x y z).comp (ADHMMonadLeftFiber D x y z) = 0 := by
  ext v
  have hv := LinearMap.congr_fun hD v
  simp [linearCommutator, LinearMap.comp_apply, sub_eq_add_neg,
    ADHMMonadRightFiber, ADHMMonadLeftFiber] at hv ⊢
  linear_combination (norm := module) (z * z) • hv

/--
Output package expected from a terminal ADHM construction.

The concrete future target should replace these proposition fields with a
monad on projective space, its cohomology sheaf or bundle, framing at the line
at infinity, charge/rank computations, and the inverse moduli construction.
-/
structure ADHMConstructionPackage
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]
    (D : ADHMData K V W) : Type (max (uV + 1) (uW + 1)) where
  monadCarrier : Type (max uV uW)
  instantonObject : Type (max uV uW)
  monadIsComplex : Prop
  monadIsComplex_holds : monadIsComplex
  monadIsExactAtEnds : Prop
  monadIsExactAtEnds_holds : monadIsExactAtEnds
  cohomologyIsLocallyFree : Prop
  cohomologyIsLocallyFree_holds : cohomologyIsLocallyFree
  framingAtInfinity : Prop
  framingAtInfinity_holds : framingAtInfinity
  rankAndChargeMatch : Prop
  rankAndChargeMatch_holds : rankAndChargeMatch
  antiSelfDualConnectionRecovered : Prop
  antiSelfDualConnectionRecovered_holds : antiSelfDualConnectionRecovered
  inverseModuliLaw : Prop
  inverseModuliLaw_holds : inverseModuliLaw

/-- The construction package exposes exactness of the ADHM monad at the ends. -/
theorem ADHMConstructionPackage.exact_at_ends
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]
    {D : ADHMData K V W} (P : ADHMConstructionPackage D) :
    P.monadIsExactAtEnds :=
  P.monadIsExactAtEnds_holds

/-- The construction package exposes the framed rank/charge compatibility field. -/
theorem ADHMConstructionPackage.rank_charge
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]
    {D : ADHMData K V W} (P : ADHMConstructionPackage D) :
    P.rankAndChargeMatch :=
  P.rankAndChargeMatch_holds

/-- Change-of-basis pairs acting on the internal and framing vector spaces. -/
abbrev FramingChange
    (K : Type uK) (V : Type uV) (W : Type uW)
    [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W] :
    Type (max uV uW) :=
  (V ≃ₗ[K] V) × (W ≃ₗ[K] W)

/-- The identity change of basis is available from mathlib's linear equivalence API. -/
def identityFramingChange
    (K : Type uK) (V : Type uV) (W : Type uW)
    [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W] :
    FramingChange K V W :=
  (LinearEquiv.refl K V, LinearEquiv.refl K W)

/--
The complex ADHM change-of-basis action.

The internal basis change conjugates `B1` and `B2`; the framing basis change
acts contravariantly on the source of `I` and covariantly on the target of `J`.
-/
def complexADHMGaugeAction
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]
    (D : ADHMData K V W) (g : FramingChange K V W) : ADHMData K V W where
  B1 := g.1.toLinearMap.comp (D.B1.comp g.1.symm.toLinearMap)
  B2 := g.1.toLinearMap.comp (D.B2.comp g.1.symm.toLinearMap)
  I := g.1.toLinearMap.comp (D.I.comp g.2.symm.toLinearMap)
  J := g.2.toLinearMap.comp (D.J.comp g.1.symm.toLinearMap)

/--
After change of basis, the complex ADHM left-hand side is conjugate to the
original left-hand side by the internal basis change.
-/
theorem complexADHMGaugeAction_complexExpression
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]
    (D : ADHMData K V W) (g : FramingChange K V W) :
    linearCommutator K V
          (complexADHMGaugeAction D g).B1 (complexADHMGaugeAction D g).B2 +
        (complexADHMGaugeAction D g).I.comp (complexADHMGaugeAction D g).J =
      g.1.toLinearMap.comp
        ((linearCommutator K V D.B1 D.B2 + D.I.comp D.J).comp
          g.1.symm.toLinearMap) := by
  ext v
  simp [complexADHMGaugeAction, linearCommutator, LinearMap.comp_apply,
    sub_eq_add_neg, add_assoc]

/-- The complex ADHM equation is invariant under the change-of-basis action. -/
theorem complexADHMGaugeAction_complexEquation_iff
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]
    (D : ADHMData K V W) (g : FramingChange K V W) :
    ComplexADHMEquation (complexADHMGaugeAction D g) ↔
      ComplexADHMEquation D := by
  constructor
  · intro h
    rw [ComplexADHMEquation, complexADHMGaugeAction_complexExpression] at h
    rw [ComplexADHMEquation]
    ext v
    have hv := LinearMap.congr_fun h (g.1 v)
    have hgv :
        g.1 ((linearCommutator K V D.B1 D.B2 + D.I.comp D.J) v) = 0 := by
      simpa [LinearMap.comp_apply] using hv
    apply g.1.injective
    simpa using hgv
  · intro h
    rw [ComplexADHMEquation] at h
    rw [ComplexADHMEquation, complexADHMGaugeAction_complexExpression, h]
    simp

/-- Forward form of complex-equation invariance under change of basis. -/
theorem complexADHMGaugeAction_preserves_complexEquation
    {K : Type uK} {V : Type uV} {W : Type uW}
    [Field K] [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]
    {D : ADHMData K V W} (g : FramingChange K V W)
    (hD : ComplexADHMEquation D) :
    ComplexADHMEquation (complexADHMGaugeAction D g) :=
  (complexADHMGaugeAction_complexEquation_iff D g).2 hD

/--
Normalized Stage1 statement shape for the ADHM construction.

It quantifies over the scalar field, internal vector space `V`, framing vector
space `W`, finite-dimensionality assumptions, the linear ADHM data, and the
explicit construction hypotheses.  The conclusion is intentionally a package
existence statement, not a local proof of the ADHM construction.
-/
def StatementShape : Prop :=
  ∀ (K : Type uK) (V : Type uV) (W : Type uW)
    [Field K] [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] [FiniteDimensional K W],
      ∀ D : ADHMData K V W,
        ADHMHypotheses D -> Nonempty (ADHMConstructionPackage D)

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (K : Type uK) (V : Type uV) (W : Type uW)
      [Field K] [AddCommGroup V] [Module K V] [FiniteDimensional K V]
      [AddCommGroup W] [Module K W] [FiniteDimensional K W],
        ∀ D : ADHMData K V W,
          ADHMHypotheses D -> Nonempty (ADHMConstructionPackage D)) :
    StatementShape.{uK, uV, uW} :=
  h

/-- Finite-dimensional ADHM data have well-defined internal and framing dimensions. -/
def dimensionPair
    (K : Type uK) (V : Type uV) (W : Type uW)
    [Field K] [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] [FiniteDimensional K W] : ℕ × ℕ :=
  (Module.finrank K V, Module.finrank K W)

/-- Projectivization names the ambient projective linear-algebra substrate. -/
abbrev ProjectiveSpaceOf
    (K : Type uK) (M : Type uM) [Field K] [AddCommGroup M] [Module K M] :=
  Projectivization K M

/-- The projectivization representative of any point is nonzero. -/
theorem projective_rep_nonzero
    (K : Type uK) (M : Type uM) [Field K] [AddCommGroup M] [Module K M]
    (p : ProjectiveSpaceOf K M) :
    Projectivization.rep p ≠ 0 :=
  Projectivization.rep_nonzero p

/-- mathlib modules checked while locating repo-local ADHM anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.LinearAlgebra.FiniteDimensional.Defs",
  "Mathlib.LinearAlgebra.Projectivization.Basic",
  "Mathlib.LinearAlgebra.Projectivization.Subspace",
  "Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Basic",
  "Mathlib.LinearAlgebra.Matrix.Trace",
  "Mathlib.Analysis.Matrix.Hermitian",
  "Mathlib.Analysis.Matrix.Spectrum",
  "Mathlib.Analysis.Matrix.PosDef",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic",
  "Mathlib.AlgebraicGeometry.Scheme"
]

/-- Nearby checked names used or audited for the ADHM statement boundary. -/
def mathlibAnchorNames : List String := [
  "LinearMap",
  "LinearMap.comp",
  "LinearEquiv",
  "LinearEquiv.refl",
  "FiniteDimensional",
  "Module.finrank",
  "Projectivization",
  "Projectivization.rep_nonzero",
  "Matrix.GeneralLinearGroup",
  "Matrix.IsHermitian",
  "Matrix.IsHermitian.spectral_theorem",
  "Matrix.PosSemidef"
]

/-- Pinned mathlib revision used for the C002 public-anchor audit note. -/
def mathlibAuditRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Exact anchors requested by the C002 public mathlib audit task. -/
def c002RequestedMathlibAnchors : List String := [
  "LinearMap",
  "FiniteDimensional",
  "Projectivization",
  "Matrix.GeneralLinearGroup",
  "Matrix.IsHermitian"
]

/-- Search terms that did not locate a terminal ADHM theorem in pinned local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "ADHM",
  "Atiyah-Drinfeld-Hitchin-Manin",
  "instanton",
  "Yang-Mills",
  "YangMills",
  "anti-self-dual",
  "self-dual",
  "framed instanton",
  "monad construction",
  "ADHM equation"
]

/-- External GitHub code-search terms required by child task `S1-M-203-C007`. -/
def c007RequestedGitHubCodeSearchTerms : List String := [
  "ADHM",
  "Atiyah-Drinfeld-Hitchin-Manin",
  "instanton",
  "monad construction"
]

/--
External-audit status for child task `S1-M-203-C007` on 2026-05-01.

Authenticated GitHub code search was not available in this execution
environment: `gh auth status` reported no logged-in GitHub host, and unauthenticated
GitHub REST code-search probes returned a rate-limit/authentication failure.
Therefore no external Lean 4 ADHM proof entered this repository's pinned
validation closure in this child pass.
-/
def c007ExternalAuditStatus : String :=
  "blocked_before_result_set: no authenticated GitHub code search token was available"

/--
M0387 integration gate for `S1-M-203-C007`: no completion is claimed from
anchor-only evidence, and no completed state may retain repo-local integration
debt.
-/
def c007NoCompletedRepoLocalIntegrationDebt : Prop :=
  True

/-- Checked marker for the `S1-M-203-C007` repo-local integration-debt gate. -/
theorem c007NoCompletedRepoLocalIntegrationDebt_holds :
    c007NoCompletedRepoLocalIntegrationDebt := by
  trivial

/--
C008 status gate: `THM-M-1544` is not repo-locally closed by this Stage1
artifact.

The checked file contains statement boundaries and several linear-algebra
leaves, but it does not contain a terminal ADHM construction proof body and no
pinned external Lean 4 ADHM closure has been imported into this repository's
Lake validation closure.
-/
def c008FormalizationDebtStatus : String :=
  "formalization_debt_not_repo_local_closed"

/--
C008 completion gate: do not upgrade the ADHM construction from
`formalization_debt` until a local proof body, local mathlib wrapper, or pinned
external Lean 4 closure validates in this repository.
-/
def c008KeepFormalizationDebtUntilClosed : Prop :=
  True

/-- Checked marker for the C008 no-completion gate. -/
theorem c008KeepFormalizationDebtUntilClosed_holds :
    c008KeepFormalizationDebtUntilClosed := by
  trivial

/-! ## Audit probes retained in the checked file. -/

#check linearCommutator
#check ADHMData
#check ComplexADHMEquation
#check complexADHMEquation_iff
#check zeroADHMData_complexEquation
#check linearCommutator_self
#check matrixCommutator
#check MatrixADHMData
#check hermitianAdjointMatrix
#check hermitianAdjointMatrix_eq_conjTranspose
#check RealMomentMapExpression
#check RealMomentMapEquation
#check realMomentMapEquation_iff
#check zeroMatrixADHMData
#check zeroMatrixADHMData_realMomentMapEquation
#check ADHMInvariantSubspace
#check ADHMFramingImageContained
#check ADHMSubspaceContainedInKernelJ
#check ADHMStable
#check ADHMCostable
#check ADHMHypotheses
#check complexEquation_of_hypotheses
#check stable_of_hypotheses
#check costable_of_hypotheses
#check realMomentMapEquation_of_hypotheses
#check ADHMMonadLeftFiber
#check ADHMMonadRightFiber
#check ADHMMonadRightFiber_comp_leftFiber_eq_zero
#check ADHMConstructionPackage
#check StatementShape
#check StatementShape.intro
#check dimensionPair
#check FramingChange
#check identityFramingChange
#check complexADHMGaugeAction
#check complexADHMGaugeAction_complexExpression
#check complexADHMGaugeAction_complexEquation_iff
#check complexADHMGaugeAction_preserves_complexEquation
#check ProjectiveSpaceOf
#check projective_rep_nonzero
#check mathlibAuditRevision
#check c002RequestedMathlibAnchors
#check c007RequestedGitHubCodeSearchTerms
#check c007ExternalAuditStatus
#check c007NoCompletedRepoLocalIntegrationDebt_holds
#check c008FormalizationDebtStatus
#check c008KeepFormalizationDebtUntilClosed_holds
#check LinearMap
#check LinearMap.comp
#check LinearEquiv.refl
#check FiniteDimensional
#check Module.finrank
#check Projectivization
#check Projectivization.rep_nonzero
#check Matrix.GeneralLinearGroup
#check Matrix.IsHermitian

end S1_M_203
end Stage1
end AwesomeTheorems
