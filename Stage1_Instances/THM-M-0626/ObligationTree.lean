import Statement

/-!
# THM-M-0626 conditional obligation composition

This module checks the child-to-parent interfaces frozen for the connected-image theorem.  The
nonempty-image and preconnected-image packages remain explicit hypotheses, so these declarations
do not install the audited mathlib theorem or close the canonical root.
-/

namespace Stage1Instances.THM_M_0626.ObligationTree

universe u v

/-- The nonempty half of the image-connectedness terminal body. -/
def ImageNonemptyPackage : Prop :=
  forall {alpha : Type u} {beta : Type v} [TopologicalSpace alpha] [TopologicalSpace beta]
    {s : Set alpha}, s.Nonempty -> forall f : alpha -> beta, (f '' s).Nonempty

/-- The substantive preconnected-image package exported by the audited mathlib body. -/
def ImagePreconnectedPackage : Prop :=
  forall {alpha : Type u} {beta : Type v} [TopologicalSpace alpha] [TopologicalSpace beta]
    {s : Set alpha}, IsPreconnected s ->
      forall f : alpha -> beta, ContinuousOn f s -> IsPreconnected (f '' s)

/-- Choose source-open representatives for two relative preimages. -/
def RelativePreimagePackage : Prop :=
  forall {alpha : Type u} {beta : Type v} [TopologicalSpace alpha] [TopologicalSpace beta]
    {s : Set alpha} (f : alpha -> beta), ContinuousOn f s ->
      forall u v : Set beta, IsOpen u -> IsOpen v ->
        exists u' v' : Set alpha,
          IsOpen u' /\ IsOpen v' /\
          f ⁻¹' u ∩ s = u' ∩ s /\ f ⁻¹' v ∩ s = v' ∩ s

/-- Convert an image cover to a source cover once relative-preimage identities are supplied. -/
def ImageCoverPullbackPackage : Prop :=
  forall {alpha : Type u} {beta : Type v} [TopologicalSpace alpha] [TopologicalSpace beta]
    {s : Set alpha} (f : alpha -> beta) (u v : Set beta) (u' v' : Set alpha),
      f ⁻¹' u ∩ s = u' ∩ s -> f ⁻¹' v ∩ s = v' ∩ s ->
      f '' s ⊆ u ∪ v -> s ⊆ u' ∪ v'

/-- Pull image hits in `u` and `v` back to hits in the relative source opens. -/
def ImageHitPullbackPackage : Prop :=
  forall {alpha : Type u} {beta : Type v} [TopologicalSpace alpha] [TopologicalSpace beta]
    {s : Set alpha} (f : alpha -> beta) (u v : Set beta) (u' v' : Set alpha),
      f ⁻¹' u ∩ s = u' ∩ s -> f ⁻¹' v ∩ s = v' ∩ s ->
      (f '' s ∩ u).Nonempty -> (f '' s ∩ v).Nonempty ->
      (s ∩ u').Nonempty /\ (s ∩ v').Nonempty

/-- The source preconnectedness eliminator used after cover and witness pullback. -/
def SourceIntersectionPackage : Prop :=
  forall {alpha : Type u} [TopologicalSpace alpha] {s u' v' : Set alpha},
    IsPreconnected s -> IsOpen u' -> IsOpen v' -> s ⊆ u' ∪ v' ->
      (s ∩ u').Nonempty -> (s ∩ v').Nonempty ->
      (s ∩ (u' ∩ v')).Nonempty

/-- Push a relative source intersection witness into the image intersection. -/
def IntersectionPushforwardPackage : Prop :=
  forall {alpha : Type u} {beta : Type v} [TopologicalSpace alpha] [TopologicalSpace beta]
    {s : Set alpha} (f : alpha -> beta) (u v : Set beta) (u' v' : Set alpha),
      f ⁻¹' u ∩ s = u' ∩ s -> f ⁻¹' v ∩ s = v' ∩ s ->
      (s ∩ (u' ∩ v')).Nonempty -> (f '' s ∩ (u ∩ v)).Nonempty

/-- The arbitrary-open separation engine definitionally underlying image preconnectedness. -/
def SeparationEngine : Prop :=
  forall {alpha : Type u} {beta : Type v} [TopologicalSpace alpha] [TopologicalSpace beta]
    {s : Set alpha}, IsPreconnected s ->
      forall (f : alpha -> beta), ContinuousOn f s ->
        forall u v : Set beta, IsOpen u -> IsOpen v -> f '' s ⊆ u ∪ v ->
          (f '' s ∩ u).Nonempty -> (f '' s ∩ v).Nonempty ->
          (f '' s ∩ (u ∩ v)).Nonempty

/-- The exact local-continuity interface supplied by `IsConnected.image`. -/
def LocalConnectedImagePackage : Prop :=
  forall {alpha : Type u} {beta : Type v} [TopologicalSpace alpha] [TopologicalSpace beta]
    {s : Set alpha}, IsConnected s ->
      forall f : alpha -> beta, ContinuousOn f s -> IsConnected (f '' s)

/-- The narrow global-to-local continuity premise used by root composition. -/
def GlobalToLocalContinuityPackage : Prop :=
  forall {alpha : Type u} {beta : Type v} [TopologicalSpace alpha] [TopologicalSpace beta]
    {s : Set alpha}, forall f : alpha -> beta, Continuous f -> ContinuousOn f s

/-- Checked construction of the narrow continuity transport package. -/
theorem globalToLocalContinuity : GlobalToLocalContinuityPackage.{u, v} := by
  intro alpha beta _ _ s f hf
  exact hf.continuousOn

/-- Checked assembly of the complete arbitrary-open separation engine. -/
theorem separationEngine_of_components
    (relativePreimages : RelativePreimagePackage.{u, v})
    (coverPullback : ImageCoverPullbackPackage.{u, v})
    (hitPullback : ImageHitPullbackPackage.{u, v})
    (sourceIntersection : SourceIntersectionPackage.{u})
    (intersectionPushforward : IntersectionPushforwardPackage.{u, v}) :
    SeparationEngine.{u, v} := by
  intro alpha beta _ _ s hs f hf u v hu hv huv hsu hsv
  obtain ⟨u', v', hu', hv', hpreU, hpreV⟩ := relativePreimages f hf u v hu hv
  have hsourceCover : s ⊆ u' ∪ v' := coverPullback f u v u' v' hpreU hpreV huv
  obtain ⟨hsu', hsv'⟩ := hitPullback f u v u' v' hpreU hpreV hsu hsv
  have hintersection : (s ∩ (u' ∩ v')).Nonempty :=
    sourceIntersection hs hu' hv' hsourceCover hsu' hsv'
  exact intersectionPushforward f u v u' v' hpreU hpreV hintersection

/-- Checked re-abstraction of the separation engine as the preconnected-image package. -/
theorem imagePreconnected_of_separationEngine
    (separation : SeparationEngine.{u, v}) :
    ImagePreconnectedPackage.{u, v} := by
  intro alpha beta _ _ s hs f hf
  exact separation hs f hf

/-- Checked recomposition of the two terminal-body branches. Both packages are consumed. -/
theorem localConnectedImage_of_components
    (nonemptyImage : ImageNonemptyPackage.{u, v})
    (preconnectedImage : ImagePreconnectedPackage.{u, v}) :
    LocalConnectedImagePackage.{u, v} := by
  intro alpha beta _ _ s hs f hf
  exact ⟨nonemptyImage hs.nonempty f, preconnectedImage hs.isPreconnected f hf⟩

/-- Checked identity from the reconstructed terminal body to the imported anchor interface. -/
theorem localAnchor_of_bodyComposition
    (bodyComposition : LocalConnectedImagePackage.{u, v}) :
    LocalConnectedImagePackage.{u, v} :=
  bodyComposition

/-- Checked global-to-local transport from the exact local package to the canonical root. -/
theorem root_of_localConnectedImage
    (globalToLocal : GlobalToLocalContinuityPackage.{u, v})
    (localImage : LocalConnectedImagePackage.{u, v}) :
    Stage1Instances.THM_M_0626.ConnectedImageTarget.{u, v} := by
  intro alpha beta _ _ s hs f hf
  exact localImage hs f (globalToLocal f hf)

/-- The exact result type produced by the terminal assembly node. -/
abbrev ExactAssembly : Prop :=
  Stage1Instances.THM_M_0626.ConnectedImageTarget.{u, v}

/-- Checked terminal assembly from the two exact child packages. -/
theorem exactAssembly_of_packages
    (globalToLocal : GlobalToLocalContinuityPackage.{u, v})
    (localImage : LocalConnectedImagePackage.{u, v}) :
    ExactAssembly.{u, v} :=
  root_of_localConnectedImage globalToLocal localImage

/-- Checked identity from the terminal assembly output to the canonical root. -/
theorem root_of_exactAssembly
    (assembly : ExactAssembly.{u, v}) :
    Stage1Instances.THM_M_0626.ConnectedImageTarget.{u, v} :=
  assembly

#check Set.image_nonempty
#check continuousOn_iff'
#check IsPreconnected.image
#check IsConnected.image
#check Continuous.continuousOn
#print axioms globalToLocalContinuity
#print axioms separationEngine_of_components
#print axioms imagePreconnected_of_separationEngine
#print axioms localConnectedImage_of_components
#print axioms localAnchor_of_bodyComposition
#print axioms exactAssembly_of_packages
#print axioms root_of_exactAssembly

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0626.ConnectedImageTarget

end Stage1Instances.THM_M_0626.ObligationTree
