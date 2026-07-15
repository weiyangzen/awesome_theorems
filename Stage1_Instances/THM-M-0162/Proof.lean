import «Stage1_Instances».«THM-M-0162».ObligationTree
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Comp
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Prod
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.LinearAlgebra.Matrix.DotProduct

/-!
# THM-M-0162 proof

This module proves the exact frozen Frenet-Serret target. The proof derives the
orthonormal moving frame, differentiates its scalar products, and reconstructs
the normal and binormal derivatives from their three frame coefficients.
-/

namespace Stage1Instances.THM_M_0162

open Matrix

private lemma dot_self_nonneg (v : Vec3) : 0 <= dotProduct v v := by
  rw [dotProduct]
  exact Finset.sum_nonneg (fun i _ => mul_self_nonneg (v i))

private lemma dot_deriv_eq_zero_of_const_one {U : Set Real} {f g : Real -> Vec3}
    {f' g' : Vec3} {s : Real} (hU : IsOpen U) (hs : s ∈ U)
    (hf : HasDerivAt f f' s) (hg : HasDerivAt g g' s)
    (hconst : forall t, t ∈ U -> dotProduct (f t) (g t) = 1) :
    dotProduct (f s) g' + dotProduct f' (g s) = 0 := by
  let fE : Real -> EuclideanSpace Real (Fin 3) := fun t => WithLp.toLp 2 (f t)
  let gE : Real -> EuclideanSpace Real (Fin 3) := fun t => WithLp.toLp 2 (g t)
  let e : (Fin 3 -> Real) ≃L[Real] EuclideanSpace Real (Fin 3) :=
    (WithLp.linearEquiv 2 Real (Fin 3 -> Real)).symm.toContinuousLinearEquiv
  have hfE : HasDerivAt fE (WithLp.toLp 2 f') s := by
    simpa [fE, e] using (e.toContinuousLinearMap.hasFDerivAt.comp_hasDerivAt s hf)
  have hgE : HasDerivAt gE (WithLp.toLp 2 g') s := by
    simpa [gE, e] using (e.toContinuousLinearMap.hasFDerivAt.comp_hasDerivAt s hg)
  have hi := hfE.inner Real hgE
  have heq : (fun t => inner Real (fE t) (gE t)) =ᶠ[nhds s]
      fun _ => (1 : Real) := by
    filter_upwards [hU.mem_nhds hs] with t ht
    change dotProduct (g t) (f t) = 1
    rw [dotProduct_comm]
    exact hconst t ht
  have hone : HasDerivAt (fun _ : Real => (1 : Real)) 0 s := hasDerivAt_const s 1
  have hz : inner Real (fE s) (WithLp.toLp 2 g') +
      inner Real (WithLp.toLp 2 f') (gE s) = 0 :=
    (hi.congr_of_eventuallyEq heq.symm).unique hone
  change dotProduct g' (f s) + dotProduct (g s) f' = 0 at hz
  simpa [dotProduct_comm] using hz

private lemma dot_deriv_eq_zero_of_const_zero {U : Set Real} {f g : Real -> Vec3}
    {f' g' : Vec3} {s : Real} (hU : IsOpen U) (hs : s ∈ U)
    (hf : HasDerivAt f f' s) (hg : HasDerivAt g g' s)
    (hconst : forall t, t ∈ U -> dotProduct (f t) (g t) = 0) :
    dotProduct (f s) g' + dotProduct f' (g s) = 0 := by
  let fE : Real -> EuclideanSpace Real (Fin 3) := fun t => WithLp.toLp 2 (f t)
  let gE : Real -> EuclideanSpace Real (Fin 3) := fun t => WithLp.toLp 2 (g t)
  let e : (Fin 3 -> Real) ≃L[Real] EuclideanSpace Real (Fin 3) :=
    (WithLp.linearEquiv 2 Real (Fin 3 -> Real)).symm.toContinuousLinearEquiv
  have hfE : HasDerivAt fE (WithLp.toLp 2 f') s := by
    simpa [fE, e] using (e.toContinuousLinearMap.hasFDerivAt.comp_hasDerivAt s hf)
  have hgE : HasDerivAt gE (WithLp.toLp 2 g') s := by
    simpa [gE, e] using (e.toContinuousLinearMap.hasFDerivAt.comp_hasDerivAt s hg)
  have hi := hfE.inner Real hgE
  have heq : (fun t => inner Real (fE t) (gE t)) =ᶠ[nhds s]
      fun _ => (0 : Real) := by
    filter_upwards [hU.mem_nhds hs] with t ht
    change dotProduct (g t) (f t) = 0
    rw [dotProduct_comm]
    exact hconst t ht
  have hzero : HasDerivAt (fun _ : Real => (0 : Real)) 0 s := hasDerivAt_const s 0
  have hz : inner Real (fE s) (WithLp.toLp 2 g') +
      inner Real (WithLp.toLp 2 f') (gE s) = 0 :=
    (hi.congr_of_eventuallyEq heq.symm).unique hzero
  change dotProduct g' (f s) + dotProduct (g s) f' = 0 at hz
  simpa [dotProduct_comm] using hz

private lemma self_dot_deriv_eq_zero {U : Set Real} {f : Real -> Vec3}
    {f' : Vec3} {s : Real} (hU : IsOpen U) (hs : s ∈ U)
    (hf : HasDerivAt f f' s)
    (hconst : forall t, t ∈ U -> euclideanNorm (f t) = 1) :
    dotProduct f' (f s) = 0 := by
  have hsq : forall t, t ∈ U -> dotProduct (f t) (f t) = 1 := by
    intro t ht
    have h := congrArg (fun x : Real => x ^ 2) (hconst t ht)
    simpa [euclideanNorm, Real.sq_sqrt (dot_self_nonneg (f t))] using h
  have hzero := dot_deriv_eq_zero_of_const_one hU hs hf hf hsq
  rw [dotProduct_comm] at hzero
  linarith

private lemma self_dot_eq_one_of_norm {v : Vec3} (h : euclideanNorm v = 1) :
    dotProduct v v = 1 := by
  have hsq := congrArg (fun x : Real => x ^ 2) h
  simpa [euclideanNorm, Real.sq_sqrt (dot_self_nonneg v)] using hsq

private lemma tangent_normal_orthogonal {U : Set Real} {T T' N : Real -> Vec3}
    {kappa : Real -> Real} {s : Real} (hU : IsOpen U) (hs : s ∈ U)
    (hT : forall t, t ∈ U -> HasDerivAt T (T' t) t)
    (hUnit : forall t, t ∈ U -> euclideanNorm (T t) = 1)
    (hNormal : forall t, t ∈ U -> N t = (kappa t)⁻¹ • T' t) :
    dotProduct (T s) (N s) = 0 := by
  have horth : dotProduct (T' s) (T s) = 0 :=
    self_dot_deriv_eq_zero hU hs (hT s hs) hUnit
  rw [hNormal s hs, dotProduct_smul, dotProduct_comm]
  simp [horth]

private lemma normal_is_unit {U : Set Real} {T' N : Real -> Vec3}
    {kappa : Real -> Real} {s : Real} (hs : s ∈ U)
    (hKappa : forall t, t ∈ U -> kappa t = euclideanNorm (T' t))
    (hPos : forall t, t ∈ U -> 0 < kappa t)
    (hNormal : forall t, t ∈ U -> N t = (kappa t)⁻¹ • T' t) :
    dotProduct (N s) (N s) = 1 := by
  have hk0 : kappa s ≠ 0 := ne_of_gt (hPos s hs)
  have hTnorm : dotProduct (T' s) (T' s) = (kappa s) ^ 2 := by
    have hsq := congrArg (fun x : Real => x ^ 2) (hKappa s hs)
    simpa [euclideanNorm, Real.sq_sqrt (dot_self_nonneg (T' s))] using hsq.symm
  rw [hNormal s hs, dotProduct_smul, smul_dotProduct]
  simp only [smul_eq_mul]
  rw [hTnorm]
  field_simp

private lemma self_dot_deriv_eq_zero_of_dot_one {U : Set Real} {f : Real -> Vec3}
    {f' : Vec3} {s : Real} (hU : IsOpen U) (hs : s ∈ U)
    (hf : HasDerivAt f f' s)
    (hconst : forall t, t ∈ U -> dotProduct (f t) (f t) = 1) :
    dotProduct f' (f s) = 0 := by
  have hzero := dot_deriv_eq_zero_of_const_one hU hs hf hf hconst
  rw [dotProduct_comm] at hzero
  linarith

private lemma cross_derivative {T N T' N' : Real -> Vec3} {s : Real}
    (hT : HasDerivAt T (T' s) s) (hN : HasDerivAt N (N' s) s) :
    HasDerivAt (fun t => T t ⨯₃ N t) (T' s ⨯₃ N s + T s ⨯₃ N' s) s := by
  apply hasDerivAt_pi.mpr
  intro i
  have hTcoord (j : Fin 3) : HasDerivAt (fun t => T t j) (T' s j) s := by
    simpa using (hasFDerivAt_apply j (T s)).comp s hT.hasFDerivAt
  have hNcoord (j : Fin 3) : HasDerivAt (fun t => N t j) (N' s j) s := by
    simpa using (hasFDerivAt_apply j (N s)).comp s hN.hasFDerivAt
  fin_cases i
  · change HasDerivAt
      (fun t => T t 1 * N t 2 - T t 2 * N t 1)
      ((T' s 1 * N s 2 - T' s 2 * N s 1) +
        (T s 1 * N' s 2 - T s 2 * N' s 1)) s
    have hd : HasDerivAt (fun t => T t 1 * N t 2 - T t 2 * N t 1)
        ((T' s 1 * N s 2 + T s 1 * N' s 2) -
          (T' s 2 * N s 1 + T s 2 * N' s 1)) s := by
      change HasDerivAt ((fun t => T t 1 * N t 2) - (fun t => T t 2 * N t 1)) _ s
      exact HasDerivAt.sub ((hTcoord 1).mul (hNcoord 2)) ((hTcoord 2).mul (hNcoord 1))
    exact hd.congr_deriv (by ring)
  · change HasDerivAt
      (fun t => T t 2 * N t 0 - T t 0 * N t 2)
      ((T' s 2 * N s 0 - T' s 0 * N s 2) +
        (T s 2 * N' s 0 - T s 0 * N' s 2)) s
    have hd : HasDerivAt (fun t => T t 2 * N t 0 - T t 0 * N t 2)
        ((T' s 2 * N s 0 + T s 2 * N' s 0) -
          (T' s 0 * N s 2 + T s 0 * N' s 2)) s := by
      change HasDerivAt ((fun t => T t 2 * N t 0) - (fun t => T t 0 * N t 2)) _ s
      exact HasDerivAt.sub ((hTcoord 2).mul (hNcoord 0)) ((hTcoord 0).mul (hNcoord 2))
    exact hd.congr_deriv (by ring)
  · change HasDerivAt
      (fun t => T t 0 * N t 1 - T t 1 * N t 0)
      ((T' s 0 * N s 1 - T' s 1 * N s 0) +
        (T s 0 * N' s 1 - T s 1 * N' s 0)) s
    have hd : HasDerivAt (fun t => T t 0 * N t 1 - T t 1 * N t 0)
        ((T' s 0 * N s 1 + T s 0 * N' s 1) -
          (T' s 1 * N s 0 + T s 1 * N' s 0)) s := by
      change HasDerivAt ((fun t => T t 0 * N t 1) - (fun t => T t 1 * N t 0)) _ s
      exact HasDerivAt.sub ((hTcoord 0).mul (hNcoord 1)) ((hTcoord 1).mul (hNcoord 0))
    exact hd.congr_deriv (by ring)

private lemma derivative_of_local_cross_identity {U : Set Real}
    {T N B T' N' B' : Real -> Vec3} {s : Real} (hU : IsOpen U) (hs : s ∈ U)
    (hT : HasDerivAt T (T' s) s) (hN : HasDerivAt N (N' s) s)
    (hB : HasDerivAt B (B' s) s)
    (hcross : forall t, t ∈ U -> B t = T t ⨯₃ N t) :
    B' s = T' s ⨯₃ N s + T s ⨯₃ N' s := by
  have hcrossD := cross_derivative hT hN
  have heq : B =ᶠ[nhds s] fun t => T t ⨯₃ N t := by
    filter_upwards [hU.mem_nhds hs] with t ht
    exact hcross t ht
  exact hB.unique (hcrossD.congr_of_eventuallyEq heq)

private lemma vector_reconstruct (T N : Vec3)
    (hTT : dotProduct T T = 1) (hNN : dotProduct N N = 1)
    (hTN : dotProduct T N = 0) (v : Vec3) :
    v = dotProduct v T • T + dotProduct v N • N +
      dotProduct v (T ⨯₃ N) • (T ⨯₃ N) := by
  have hNT : dotProduct N T = 0 := by simpa [dotProduct_comm] using hTN
  have hBnorm : dotProduct (T ⨯₃ N) (T ⨯₃ N) = 1 := by
    rw [cross_dot_cross, hTT, hNN, hTN, hNT]
    norm_num
  have hTB : dotProduct T (T ⨯₃ N) = 0 := dot_self_cross T N
  have hNB : dotProduct N (T ⨯₃ N) = 0 := dot_cross_self T N
  let w := v - dotProduct v T • T - dotProduct v N • N -
    dotProduct v (T ⨯₃ N) • (T ⨯₃ N)
  have hwT : dotProduct w T = 0 := by
    dsimp [w]
    rw [sub_dotProduct, sub_dotProduct, sub_dotProduct,
      smul_dotProduct, smul_dotProduct, smul_dotProduct, hTT, hNT]
    have hBT : dotProduct (T ⨯₃ N) T = 0 := by
      rw [dotProduct_comm]
      exact hTB
    rw [hBT]
    simp
  have hwN : dotProduct w N = 0 := by
    dsimp [w]
    rw [sub_dotProduct, sub_dotProduct, sub_dotProduct,
      smul_dotProduct, smul_dotProduct, smul_dotProduct, hTN, hNN]
    have hBN : dotProduct (T ⨯₃ N) N = 0 := by
      rw [dotProduct_comm]
      exact hNB
    rw [hBN]
    simp
  have hwB : dotProduct w (T ⨯₃ N) = 0 := by
    dsimp [w]
    simp [sub_dotProduct, smul_dotProduct, hTB, hNB, hBnorm]
  have hTw : dotProduct T w = 0 := by
    rw [dotProduct_comm]
    exact hwT
  have hNw : dotProduct N w = 0 := by
    rw [dotProduct_comm]
    exact hwN
  have hBw : dotProduct (T ⨯₃ N) w = 0 := by simpa [dotProduct_comm] using hwB
  have hcross : (T ⨯₃ N) ⨯₃ w = 0 := by
    rw [cross_cross_eq_smul_sub_smul]
    simp [hTw, hNw]
  have hw : w = 0 := by
    apply (dotProduct_self_eq_zero (R := Real)).mp
    have hquad := cross_dot_cross (T ⨯₃ N) w (T ⨯₃ N) w
    rw [hcross, zero_dotProduct, hBnorm, hBw, hwB] at hquad
    linarith
  dsimp [w] at hw
  have := congrArg (fun z => z + dotProduct v (T ⨯₃ N) • (T ⨯₃ N) +
    dotProduct v N • N + dotProduct v T • T) hw
  simpa [sub_eq_add_neg, add_assoc, add_left_comm, add_comm] using this

/-- Direct closure of the three Frenet-Serret equations before routing the
result through the frozen package interfaces. -/
private theorem frenetSerretDirect : FrenetSerretTarget := by
  intro U alpha T T' N N' B B' kappa tau hU _hAlpha hT hN hB
    hUnit hKappa hKappaPos hNormal hBinormal hTau s hs
  have hTangent : T' s = kappa s • N s := by
    rw [hNormal s hs]
    simp only [smul_smul]
    rw [mul_inv_cancel₀ (ne_of_gt (hKappaPos s hs))]
    simp
  constructor
  · exact hTangent
  constructor
  · have hTT : dotProduct (T s) (T s) = 1 := self_dot_eq_one_of_norm (hUnit s hs)
    have hNN : dotProduct (N s) (N s) = 1 :=
      normal_is_unit hs hKappa hKappaPos hNormal
    have hTN : dotProduct (T s) (N s) = 0 :=
      tangent_normal_orthogonal hU hs hT hUnit hNormal
    have hNNT : dotProduct (N' s) (N s) = 0 := by
      apply self_dot_deriv_eq_zero_of_dot_one hU hs (hN s hs)
      intro t ht
      exact normal_is_unit ht hKappa hKappaPos hNormal
    have hNprimeT : dotProduct (N' s) (T s) = -kappa s := by
      have hd := dot_deriv_eq_zero_of_const_zero hU hs (hN s hs) (hT s hs)
        (fun t ht => by
          rw [dotProduct_comm]
          exact tangent_normal_orthogonal hU ht hT hUnit hNormal)
      rw [hTangent, dotProduct_smul, hNN] at hd
      simp at hd
      linarith
    have hNprimeB : dotProduct (N' s) (B s) = tau s := by
      have hBprimeN : dotProduct (B' s) (N s) = -tau s := by linarith [hTau s hs]
      have hd := dot_deriv_eq_zero_of_const_zero hU hs (hB s hs) (hN s hs)
        (fun t ht => by
          rw [hBinormal t ht, dotProduct_comm]
          exact dot_cross_self (T t) (N t))
      rw [dotProduct_comm (B s) (N' s)] at hd
      linarith
    have hrecon := vector_reconstruct (T s) (N s) hTT hNN hTN (N' s)
    rw [← hBinormal s hs, hNprimeT, hNNT, hNprimeB] at hrecon
    simpa [add_assoc] using hrecon
  · have hTT : dotProduct (T s) (T s) = 1 := self_dot_eq_one_of_norm (hUnit s hs)
    have hNN : dotProduct (N s) (N s) = 1 :=
      normal_is_unit hs hKappa hKappaPos hNormal
    have hTN : dotProduct (T s) (N s) = 0 :=
      tangent_normal_orthogonal hU hs hT hUnit hNormal
    have hBT : dotProduct (B' s) (T s) = 0 := by
      have hd := dot_deriv_eq_zero_of_const_zero hU hs (hB s hs) (hT s hs)
        (fun t ht => by
          rw [hBinormal t ht, dotProduct_comm]
          exact dot_self_cross (T t) (N t))
      rw [hTangent, dotProduct_smul] at hd
      rw [dotProduct_comm (B s) (N s), hBinormal s hs, dot_cross_self] at hd
      simp at hd
      simpa using hd
    have hBN : dotProduct (B' s) (N s) = -tau s := by linarith [hTau s hs]
    have hBcross := derivative_of_local_cross_identity hU hs (hT s hs) (hN s hs)
      (hB s hs) hBinormal
    have hBB : dotProduct (B' s) (B s) = 0 := by
      rw [hBcross, hBinormal s hs]
      simp only [add_dotProduct]
      have h1 : dotProduct (T' s ⨯₃ N s) (T s ⨯₃ N s) = 0 := by
        rw [hTangent, map_smul]
        simp
      have h2 : dotProduct (T s ⨯₃ N' s) (T s ⨯₃ N s) = 0 := by
        rw [cross_dot_cross, hTT, hTN]
        have hn := self_dot_deriv_eq_zero_of_dot_one hU hs (hN s hs)
          (fun t ht => normal_is_unit ht hKappa hKappaPos hNormal)
        simpa [dotProduct_comm] using hn
      rw [h1, h2, add_zero]
    have hrecon := vector_reconstruct (T s) (N s) hTT hNN hTN (B' s)
    rw [← hBinormal s hs, hBT, hBN, hBB] at hrecon
    simpa using hrecon

private theorem equations_of_premises
    (U : Set Real) (alpha T T' N N' B B' : Real -> Vec3)
    (kappa tau : Real -> Real)
    (hPremises : FrenetPremises U alpha T T' N N' B B' kappa tau)
    (s : Real) (hs : s ∈ U) :
    T' s = kappa s • N s /\
      N' s = -(kappa s) • T s + tau s • B s /\
      B' s = -(tau s) • N s := by
  rcases hPremises with
    ⟨hU, hAlpha, hT, hN, hB, hUnit, hKappa, hKappaPos, hNormal, hBinormal, hTau⟩
  exact frenetSerretDirect U alpha T T' N N' B B' kappa tau hU hAlpha hT hN hB
    hUnit hKappa hKappaPos hNormal hBinormal hTau s hs

/-- Closed proof body for the frozen tangent-equation package. -/
theorem tangentEquation : TangentEquationPackage := by
  intro U alpha T T' N N' B B' kappa tau hPremises s hs
  exact (equations_of_premises U alpha T T' N N' B B' kappa tau hPremises s hs).1

/-- Closed proof body for the frozen normal-equation package. -/
theorem normalEquation : NormalEquationPackage := by
  intro U alpha T T' N N' B B' kappa tau hPremises s hs
  exact (equations_of_premises U alpha T T' N N' B B' kappa tau hPremises s hs).2.1

/-- Closed proof body for the frozen binormal-equation package. -/
theorem binormalEquation : BinormalEquationPackage := by
  intro U alpha T T' N N' B B' kappa tau hPremises s hs
  exact (equations_of_premises U alpha T T' N N' B B' kappa tau hPremises s hs).2.2

/-- Exact root proof composed through the interfaces frozen in
`ObligationTree.lean`. -/
theorem frenetSerret : FrenetSerretTarget :=
  root_of_equation_packages tangentEquation normalEquation binormalEquation

#print axioms tangentEquation
#print axioms normalEquation
#print axioms binormalEquation
#print axioms frenetSerret

end Stage1Instances.THM_M_0162
