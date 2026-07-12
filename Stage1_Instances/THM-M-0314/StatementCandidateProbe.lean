import Mathlib.Analysis.InnerProductSpace.Spectrum

/-!
# THM-M-0314 statement candidate probe

This module checks two nonidentical propositions compatible with the repository's
phrase "spectral decomposition of compact self-adjoint operators". It is blocker
evidence, not a canonical-target selection and not a proof of either proposition.
-/

namespace Stage1Instances.THM_M_0314

universe u v

/-- The pinned mathlib formulation saying that the closed eigenspace span is complete. -/
def CompleteEigenspaceSpanTarget : Prop :=
  forall (𝕜 : Type u) [RCLike 𝕜]
    (E : Type v) [NormedAddCommGroup E] [InnerProductSpace 𝕜 E] [CompleteSpace E]
    (T : E →L[𝕜] E),
      IsCompactOperator T ->
      T.toLinearMap.IsSymmetric ->
      (⨆ mu, Module.End.eigenspace T.toLinearMap mu)ᗮ = ⊥

/-- A stronger package that also includes finite multiplicity of every nonzero eigenvalue. -/
def CompleteEigenspaceSpanWithFiniteMultiplicityTarget : Prop :=
  forall (𝕜 : Type u) [RCLike 𝕜]
    (E : Type v) [NormedAddCommGroup E] [InnerProductSpace 𝕜 E] [CompleteSpace E]
    (T : E →L[𝕜] E),
      IsCompactOperator T ->
      T.toLinearMap.IsSymmetric ->
      (⨆ mu, Module.End.eigenspace T.toLinearMap mu)ᗮ = ⊥ ∧
        forall mu, mu ≠ 0 ->
          FiniteDimensional 𝕜 (Module.End.eigenspace T.toLinearMap mu)

-- Exact pinned declaration types relevant to the two candidates.
#check ContinuousLinearMap.orthogonalComplement_iSup_eigenspaces_eq_bot
#check ContinuousLinearMap.finite_dimensional_eigenspace

end Stage1Instances.THM_M_0314

#check Stage1Instances.THM_M_0314.CompleteEigenspaceSpanTarget
#check Stage1Instances.THM_M_0314.CompleteEigenspaceSpanWithFiniteMultiplicityTarget
