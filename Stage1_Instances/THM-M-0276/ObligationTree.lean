import Mathlib.Analysis.Complex.Basic
import Mathlib.Analysis.Normed.Operator.Banach
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0276 conditional obligation composition

This module repeats the frozen statement literally so it can be elaborated by the narrow worker
recipe without manufacturing a local `Statement.olean`. It checks only the exact adapter and root
composition. The audited mathlib theorem is inspected as a candidate, not installed as the proof.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0276_Obligations

universe u v k l

/-- Literal real branch of the frozen statement. -/
def RealOpenMappingTarget : Prop :=
  forall (E : Type u) (F : Type v)
      [NormedAddCommGroup E] [NormedSpace Real E] [CompleteSpace E]
      [NormedAddCommGroup F] [NormedSpace Real F] [CompleteSpace F]
      (f : E →L[Real] F),
    Function.Surjective f -> IsOpenMap f

/-- Literal complex branch of the frozen statement. -/
def ComplexOpenMappingTarget : Prop :=
  forall (E : Type u) (F : Type v)
      [NormedAddCommGroup E] [NormedSpace Complex E] [CompleteSpace E]
      [NormedAddCommGroup F] [NormedSpace Complex F] [CompleteSpace F]
      (f : E →L[Complex] F),
    Function.Surjective f -> IsOpenMap f

/-- Literal copy of `Stage1Instances.THM_M_0276.BanachOpenMappingTarget`. -/
def ExactRoot : Prop :=
  RealOpenMappingTarget.{u, v} /\ ComplexOpenMappingTarget.{u, v}

/-- Literal copy of the statement phase's fully expanded expression serialization. -/
def CanonicalStatementCopy : Prop :=
  (forall (E : Type u) (F : Type v)
      [NormedAddCommGroup E] [NormedSpace Real E] [CompleteSpace E]
      [NormedAddCommGroup F] [NormedSpace Real F] [CompleteSpace F]
      (f : E →L[Real] F),
    Function.Surjective f ->
      forall U : Set E, IsOpen U -> IsOpen (f '' U)) /\
  (forall (E : Type u) (F : Type v)
      [NormedAddCommGroup E] [NormedSpace Complex E] [CompleteSpace E]
      [NormedAddCommGroup F] [NormedSpace Complex F] [CompleteSpace F]
      (f : E →L[Complex] F),
    Function.Surjective f ->
      forall U : Set E, IsOpen U -> IsOpen (f '' U))

theorem exactRoot_iff_canonicalStatementCopy :
    ExactRoot.{u, v} <-> CanonicalStatementCopy.{u, v} :=
  Iff.rfl

/-- Literal polymorphic proposition delivered by the pinned semilinear terminal theorem. -/
def MathlibTerminal : Prop :=
  forall {𝕜 : Type k} {𝕜' : Type l}
      [NontriviallyNormedField 𝕜] [NontriviallyNormedField 𝕜']
      {σ : 𝕜 →+* 𝕜'} {σ' : 𝕜' →+* 𝕜}
      [RingHomInvPair σ σ'] [RingHomIsometric σ] [RingHomIsometric σ']
      {E : Type u} [NormedAddCommGroup E] [NormedSpace 𝕜 E] [CompleteSpace E]
      {F : Type v} [NormedAddCommGroup F] [NormedSpace 𝕜' F] [CompleteSpace F]
      (f : E →SL[σ] F),
    Function.Surjective f -> IsOpenMap f

/-- Checked specialization of the semilinear terminal to both exact same-field branches. -/
theorem terminal_adapter : MathlibTerminal.{u, v, 0, 0} -> ExactRoot.{u, v} := by
  intro terminal
  constructor
  · intro E F _ _ _ _ _ _ f hf
    exact terminal (𝕜 := Real) (𝕜' := Real) (σ := RingHom.id Real)
      (σ' := RingHom.id Real) f hf
  · intro E F _ _ _ _ _ _ f hf
    exact terminal (𝕜 := Complex) (𝕜' := Complex) (σ := RingHom.id Complex)
      (σ' := RingHom.id Complex) f hf

/-- The actual pinned candidate; its proof-body identity remains at the upstream declaration. -/
theorem pinned_mathlib_terminal : MathlibTerminal.{u, v, k, l} := by
  intro 𝕜 𝕜' _ _ σ σ' _ _ _ E _ _ _ F _ _ _ f hf
  exact ContinuousLinearMap.isOpenMap f hf

/-- Root composition certificate. Both exact typed children are explicit and consumed. -/
theorem compose_root
    (adapter : MathlibTerminal.{u, v, 0, 0} -> ExactRoot.{u, v})
    (terminal : MathlibTerminal.{u, v, 0, 0}) : ExactRoot.{u, v} :=
  adapter terminal

#check ContinuousLinearMap.exists_approx_preimage_norm_le
#check ContinuousLinearMap.exists_preimage_norm_le
#check ContinuousLinearMap.isOpenMap
#check terminal_adapter
#check pinned_mathlib_terminal
#check compose_root

assert_no_sorry terminal_adapter
assert_no_sorry pinned_mathlib_terminal
assert_no_sorry compose_root
assert_no_sorry exactRoot_iff_canonicalStatementCopy

#print sorries terminal_adapter
#print sorries pinned_mathlib_terminal
#print sorries compose_root
#print sorries exactRoot_iff_canonicalStatementCopy
#print sorries ContinuousLinearMap.exists_approx_preimage_norm_le
#print sorries ContinuousLinearMap.exists_preimage_norm_le
#print sorries ContinuousLinearMap.isOpenMap

#print axioms terminal_adapter
#print axioms pinned_mathlib_terminal
#print axioms compose_root
#print axioms exactRoot_iff_canonicalStatementCopy
#print axioms ContinuousLinearMap.exists_approx_preimage_norm_le
#print axioms ContinuousLinearMap.exists_preimage_norm_le
#print axioms ContinuousLinearMap.isOpenMap

set_option pp.universes true in
set_option pp.explicit true in
#print ExactRoot

set_option pp.universes true in
set_option pp.explicit true in
#print CanonicalStatementCopy

end Stage1Instances.THM_M_0276_Obligations
