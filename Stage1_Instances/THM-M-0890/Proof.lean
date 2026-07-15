import ObligationTree
import Mathlib.Analysis.Matrix.PosDef
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0890 proof bodies

This module implements the frozen Hoffman ratio-bound obligations.  The proof uses the ordered
Hermitian spectrum of the real adjacency matrix and keeps the positive-denominator boundary
explicit.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0890_Proof

open Matrix
open Stage1Instances.THM_M_0890
open Stage1Instances.THM_M_0890_Obligations

universe u

/-- The final entry of the descending Hermitian enumeration is below every adjacency
eigenvalue in the vertex-indexed enumeration. -/
theorem leastAdjacencyEigenvalue_le_eigenvalue
    {V : Type u} [Fintype V] [Nonempty V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (i : V) :
    leastAdjacencyEigenvalue G <= (G.isHermitian_adjMatrix Real).eigenvalues i := by
  let hA := G.isHermitian_adjMatrix Real
  let e : Fin (Fintype.card V) ≃ V := Fintype.equivOfCardEq (Fintype.card_fin _)
  change hA.eigenvalues₀
      ⟨Fintype.card V - 1, Nat.sub_lt Fintype.card_pos Nat.zero_lt_one⟩ <=
    hA.eigenvalues₀ (e.symm i)
  apply hA.eigenvalues₀_antitone
  simp only [Fin.le_iff_val_le_val]
  omega

/-- Positive regular degree forces the least adjacency eigenvalue to be strictly negative. -/
theorem leastAdjacencyEigenvalue_neg
    {V : Type u} [Fintype V] [Nonempty V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (k : Nat)
    (hRegular : G.IsRegularOfDegree k) (hPositive : 0 < k) :
    leastAdjacencyEigenvalue G < 0 := by
  let hA := G.isHermitian_adjMatrix Real
  by_contra hNotNegative
  have hLeastNonnegative : 0 <= leastAdjacencyEigenvalue G := le_of_not_gt hNotNegative
  have hAdjacencyPSD : (G.adjMatrix Real).PosSemidef :=
    hA.posSemidef_iff_eigenvalues_nonneg.mpr fun i =>
      hLeastNonnegative.trans (leastAdjacencyEigenvalue_le_eigenvalue G i)
  have hAdjacencyZero : G.adjMatrix Real = 0 :=
    hAdjacencyPSD.trace_eq_zero_iff.mp (G.trace_adjMatrix Real)
  let v : V := Classical.choice inferInstance
  have hRegularAction :=
    SimpleGraph.adjMatrix_mulVec_const_apply_of_regular
      (G := G) (a := (1 : Real)) hRegular (v := v)
  have hkReal : (k : Real) = 0 := by
    simpa [hAdjacencyZero] using hRegularAction.symm
  have hk : k = 0 := by exact_mod_cast hkReal
  omega

/-- The exact denominator consumed by the frozen final division is positive. -/
theorem denominatorPositive_proof : DenominatorPositiveTarget.{u} := by
  intro V _ _ _ G _ k hRegular hPositive
  have hLeast := leastAdjacencyEigenvalue_neg G k hRegular hPositive
  have hk : (0 : Real) < k := by exact_mod_cast hPositive
  linarith

/-- Subtracting the least eigenvalue from the adjacency matrix gives a positive-semidefinite
matrix.  This is the spectral lower-bound form used by the scalar estimate. -/
theorem shiftedAdjacency_posSemidef
    {V : Type u} [Fintype V] [Nonempty V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] :
    (G.adjMatrix Real -
      leastAdjacencyEigenvalue G • (1 : Matrix V V Real)).PosSemidef := by
  let hA := G.isHermitian_adjMatrix Real
  let lambda := leastAdjacencyEigenvalue G
  let U : Matrix V V Real := hA.eigenvectorUnitary
  let D : Matrix V V Real :=
    Matrix.diagonal fun i : V => hA.eigenvalues i - lambda
  have hDiagonal :
      D.PosSemidef :=
    Matrix.PosSemidef.diagonal fun i =>
      sub_nonneg.mpr (leastAdjacencyEigenvalue_le_eigenvalue G i)
  have hConjugated : (U * D * star U).PosSemidef :=
    hDiagonal.mul_mul_conjTranspose_same U
  have hId : U * (1 : Matrix V V Real) * star U = 1 := by
    dsimp only [U]
    rw [mul_one]
    exact Unitary.coe_mul_star_self hA.eigenvectorUnitary
  have hScalar :
      U * (lambda • (1 : Matrix V V Real)) * star U =
        lambda • (1 : Matrix V V Real) := by
    rw [Matrix.mul_smul, Matrix.smul_mul, hId]
  have hEq :
      G.adjMatrix Real - lambda • (1 : Matrix V V Real) = U * D * star U := by
    rw [hA.spectral_theorem]
    simp only [Unitary.conjStarAlgAut_apply]
    rw [← hScalar]
    change U * Matrix.diagonal (RCLike.ofReal ∘ hA.eigenvalues) * star U -
      U * (lambda • (1 : Matrix V V Real)) * star U = U * D * star U
    rw [← Matrix.sub_mul, ← Matrix.mul_sub]
    congr 2
    ext i j
    simp only [D, Matrix.diagonal_apply, Matrix.sub_apply]
    split_ifs with hij
    · subst j
      simp
    · simp [hij]
  rw [hEq]
  exact hConjugated

/-- The characteristic vector of an independent set has zero adjacency quadratic form. -/
theorem independentSet_adjacency_quadratic_zero
    {V : Type u} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (s : Finset V)
    (hIndependent : G.IsIndepSet s) :
    let x : V → Real := fun v => if v ∈ s then 1 else 0
    x ⬝ᵥ (G.adjMatrix Real *ᵥ x) = 0 := by
  dsimp
  rw [SimpleGraph.dotProduct_mulVec_adjMatrix]
  apply Finset.sum_eq_zero
  intro i _
  apply Finset.sum_eq_zero
  intro j _
  by_cases hAdj : G.Adj i j
  · have hNotBoth : ¬ (i ∈ s ∧ j ∈ s) := by
      rintro ⟨hi, hj⟩
      exact hIndependent hi hj hAdj.ne hAdj
    by_cases hi : i ∈ s <;> by_cases hj : j ∈ s <;> simp_all
  · simp [hAdj]

/-- The characteristic vector has squared norm equal to the independent-set cardinality. -/
theorem independentSet_characteristic_norm
    {V : Type u} [Fintype V] [DecidableEq V] (s : Finset V) :
    let x : V → Real := fun v => if v ∈ s then 1 else 0
    x ⬝ᵥ x = s.card := by
  dsimp
  simp [dotProduct]

/-- The regular adjacency matrix sends the constant vector to the degree times that vector. -/
theorem regular_adjacency_mulVec_one
    {V : Type u} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (k : Nat)
    (hRegular : G.IsRegularOfDegree k) :
    G.adjMatrix Real *ᵥ (1 : V → Real) = (k : Real) • (1 : V → Real) := by
  ext v
  simpa using
    (SimpleGraph.adjMatrix_mulVec_const_apply_of_regular
      (G := G) (a := (1 : Real)) hRegular (v := v))

/-- The independent-set characteristic vector has adjacency cross term `k * |s|` against the
constant vector in a `k`-regular graph. -/
theorem independentSet_adjacency_one
    {V : Type u} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (k : Nat)
    (hRegular : G.IsRegularOfDegree k) (s : Finset V) :
    let x : V → Real := fun v => if v ∈ s then 1 else 0
    x ⬝ᵥ (G.adjMatrix Real *ᵥ (1 : V → Real)) = (k : Real) * s.card := by
  dsimp
  rw [regular_adjacency_mulVec_one G k hRegular]
  rw [dotProduct_smul]
  simp [dotProduct]

/-- The all-ones vector has squared norm equal to the vertex count. -/
theorem one_dotProduct_one_real
    {V : Type u} [Fintype V] :
    (1 : V → Real) ⬝ᵥ (1 : V → Real) = Fintype.card V := by
  simp [dotProduct]

/-- Centering an independent-set characteristic vector against the constant vector evaluates the
shifted-adjacency quadratic form to the scalar expression used in Hoffman's bound. -/
theorem centered_shifted_quadratic
    {V : Type u} [Fintype V] [Nonempty V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (k : Nat)
    (hRegular : G.IsRegularOfDegree k) (s : Finset V)
    (hIndependent : G.IsIndepSet s) :
    let n : Real := Fintype.card V
    let alpha : Real := s.card
    let lambda := leastAdjacencyEigenvalue G
    let x : V → Real := fun v => if v ∈ s then 1 else 0
    let y := x - (alpha / n) • (1 : V → Real)
    y ⬝ᵥ ((G.adjMatrix Real - lambda • (1 : Matrix V V Real)) *ᵥ y) =
      alpha * (-lambda - alpha * ((k : Real) - lambda) / n) := by
  dsimp
  have hn : (Fintype.card V : Real) ≠ 0 := by
    exact_mod_cast (ne_of_gt Fintype.card_pos)
  have hAx := independentSet_adjacency_quadratic_zero G s hIndependent
  have hxx := independentSet_characteristic_norm s
  have hAone := regular_adjacency_mulVec_one G k hRegular
  have hxAone := independentSet_adjacency_one G k hRegular s
  have hone := one_dotProduct_one_real (V := V)
  have hOneX :
      (1 : V → Real) ⬝ᵥ (fun v => if v ∈ s then 1 else 0) = s.card := by
    simp [dotProduct]
  have hOneAx :
      (1 : V → Real) ⬝ᵥ
          (G.adjMatrix Real *ᵥ (fun v => if v ∈ s then 1 else 0)) =
        (k : Real) * s.card := by
    rw [Matrix.dotProduct_mulVec]
    have hVecMul :
        (1 : V → Real) ᵥ* G.adjMatrix Real = (k : Real) • (1 : V → Real) := by
      ext v
      simpa [hRegular v] using
        (SimpleGraph.adjMatrix_vecMul_apply (G := G) (v := v) (1 : V → Real))
    rw [hVecMul, smul_dotProduct]
    simp [dotProduct]
  have hXOne :
      (fun v => if v ∈ s then (1 : Real) else 0) ⬝ᵥ (1 : V → Real) = s.card := by
    simp [dotProduct]
  have hXKOne :
      (fun v => if v ∈ s then (1 : Real) else 0) ⬝ᵥ
          ((k : Real) • (1 : V → Real)) = (k : Real) * s.card := by
    rw [dotProduct_smul, hXOne]
    simp
  have hOneKOne :
      (1 : V → Real) ⬝ᵥ ((k : Real) • (1 : V → Real)) =
        (k : Real) * Fintype.card V := by
    rw [dotProduct_smul, hone]
    simp
  simp only [sub_mulVec, smul_mulVec, one_mulVec, mulVec_sub, mulVec_smul]
  simp only [sub_dotProduct, dotProduct_sub, smul_dotProduct, dotProduct_smul]
  rw [hAone, hAx, hxx, hOneAx, hOneX, hXOne, hXKOne, hOneKOne, hone]
  simp only [smul_eq_mul]
  field_simp
  ring

/-- The positive-semidefinite shifted adjacency matrix yields the exact scalar inequality for any
independent set. -/
theorem independentSet_scalar_nonnegative
    {V : Type u} [Fintype V] [Nonempty V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (k : Nat) (s : Finset V)
    (hRegular : G.IsRegularOfDegree k) (hIndependent : G.IsIndepSet s) :
    0 <= (s.card : Real) *
      (-leastAdjacencyEigenvalue G -
        (s.card : Real) * ((k : Real) - leastAdjacencyEigenvalue G) /
          Fintype.card V) := by
  let n : Real := Fintype.card V
  let alpha : Real := s.card
  let lambda := leastAdjacencyEigenvalue G
  let x : V → Real := fun v => if v ∈ s then 1 else 0
  let y := x - (alpha / n) • (1 : V → Real)
  have hNonnegative := (shiftedAdjacency_posSemidef G).dotProduct_mulVec_nonneg y
  rw [star_trivial, centered_shifted_quadratic G k hRegular s hIndependent] at hNonnegative
  exact hNonnegative

/-- A nonempty finite graph has a nonempty maximum independent set. -/
theorem indepNum_pos
    {V : Type u} [Fintype V] [Nonempty V]
    (G : SimpleGraph V) : 0 < G.indepNum := by
  let v : V := Classical.choice inferInstance
  have hSingleton : G.IsIndepSet ({v} : Finset V) := by
    simp [SimpleGraph.isIndepSet_iff]
  have hCard := hSingleton.card_le_indepNum
  simpa using hCard

/-- The arbitrary independent-set scalar estimate at the exact frozen maximum-estimate
interface. -/
theorem maximumIndependentSetEstimate_proof : MaximumIndependentSetEstimateTarget.{u} := by
  intro V _ _ _ G _ k s hRegular hPositive hIndependent _
  have hScalar := independentSet_scalar_nonnegative G k s hRegular hIndependent
  have hVertices : (0 : Real) < Fintype.card V := by
    exact_mod_cast Fintype.card_pos
  by_cases hCardZero : s.card = 0
  · have hLeast := leastAdjacencyEigenvalue_neg G k hRegular hPositive
    rw [hCardZero]
    simp
    exact mul_nonpos_of_nonneg_of_nonpos (by positivity) hLeast.le
  · have hAlpha : (0 : Real) < s.card := by
      exact_mod_cast Nat.pos_of_ne_zero hCardZero
    field_simp at hScalar
    nlinarith

/-- The scalar positive-semidefinite estimate rearranges to the frozen division-free inequality. -/
theorem divisionFreeInequality_proof : DivisionFreeInequalityTarget.{u} :=
  divisionFree_of_maximumEstimate maximumIndependentSetWitness_checked
    maximumIndependentSetEstimate_proof

/-- The exact frozen terminal pair. -/
theorem ratioAssembly_proof : RatioAssemblyTarget.{u} :=
  assembly_of_children denominatorPositive_proof divisionFreeInequality_proof

/-- Exact closed root proof assembled from the two locally proved terminal obligations. -/
theorem hoffmanRatioBound_proof : HoffmanRatioBoundTarget.{u} :=
  root_of_ratio_assembly ratioAssembly_proof

#check leastAdjacencyEigenvalue_le_eigenvalue
#check leastAdjacencyEigenvalue_neg
#check denominatorPositive_proof
#check shiftedAdjacency_posSemidef
#check independentSet_adjacency_quadratic_zero
#check independentSet_characteristic_norm
#check regular_adjacency_mulVec_one
#check independentSet_adjacency_one
#check one_dotProduct_one_real
#check centered_shifted_quadratic
#check independentSet_scalar_nonnegative
#check indepNum_pos
#check maximumIndependentSetEstimate_proof
#check divisionFreeInequality_proof
#check ratioAssembly_proof
#check hoffmanRatioBound_proof

assert_no_sorry leastAdjacencyEigenvalue_le_eigenvalue
assert_no_sorry leastAdjacencyEigenvalue_neg
assert_no_sorry denominatorPositive_proof
assert_no_sorry shiftedAdjacency_posSemidef
assert_no_sorry independentSet_adjacency_quadratic_zero
assert_no_sorry independentSet_characteristic_norm
assert_no_sorry regular_adjacency_mulVec_one
assert_no_sorry independentSet_adjacency_one
assert_no_sorry one_dotProduct_one_real
assert_no_sorry centered_shifted_quadratic
assert_no_sorry independentSet_scalar_nonnegative
assert_no_sorry indepNum_pos
assert_no_sorry maximumIndependentSetEstimate_proof
assert_no_sorry divisionFreeInequality_proof
assert_no_sorry ratioAssembly_proof
assert_no_sorry hoffmanRatioBound_proof

#print sorries leastAdjacencyEigenvalue_le_eigenvalue leastAdjacencyEigenvalue_neg
  denominatorPositive_proof
  shiftedAdjacency_posSemidef
  independentSet_adjacency_quadratic_zero independentSet_characteristic_norm
  regular_adjacency_mulVec_one independentSet_adjacency_one one_dotProduct_one_real
  centered_shifted_quadratic
  independentSet_scalar_nonnegative indepNum_pos maximumIndependentSetEstimate_proof
  divisionFreeInequality_proof ratioAssembly_proof hoffmanRatioBound_proof
#print axioms leastAdjacencyEigenvalue_le_eigenvalue
#print axioms leastAdjacencyEigenvalue_neg
#print axioms denominatorPositive_proof
#print axioms shiftedAdjacency_posSemidef
#print axioms independentSet_adjacency_quadratic_zero
#print axioms independentSet_characteristic_norm
#print axioms regular_adjacency_mulVec_one
#print axioms independentSet_adjacency_one
#print axioms one_dotProduct_one_real
#print axioms centered_shifted_quadratic
#print axioms independentSet_scalar_nonnegative
#print axioms indepNum_pos
#print axioms maximumIndependentSetEstimate_proof
#print axioms divisionFreeInequality_proof
#print axioms ratioAssembly_proof
#print axioms hoffmanRatioBound_proof

end Stage1Instances.THM_M_0890_Proof
