import ObligationTree

/-!
# THM-M-0626: proof installation

This module installs the exact theorem from pinned mathlib at the frozen local-continuity interface
and also reconstructs its visible open-set proof through every frozen component package. Both
routes consume the registered global-to-local transport and terminal assembly to prove the same
canonical target. Duplicate wrappers receive no additional proof-body credit.
-/

namespace Stage1Instances.THM_M_0626.Proof

open Stage1Instances.THM_M_0626
open Stage1Instances.THM_M_0626.ObligationTree

universe u v

/-- Construct the two source-open representatives supplied by relative continuity. -/
theorem relativePreimages : RelativePreimagePackage.{u, v} := by
  intro alpha beta _ _ s f hf u v hu hv
  obtain ⟨u', hu', hpreU⟩ := (continuousOn_iff'.mp hf) u hu
  obtain ⟨v', hv', hpreV⟩ := (continuousOn_iff'.mp hf) v hv
  exact ⟨u', v', hu', hv', hpreU, hpreV⟩

/-- Pull a cover of the image back through the two relative-preimage identities. -/
theorem imageCoverPullback : ImageCoverPullbackPackage.{u, v} := by
  intro alpha beta _ _ s f u v u' v' hpreU hpreV huv x hx
  rcases huv ⟨x, hx, rfl⟩ with hfu | hfv
  · left
    have hxu' : x ∈ u' ∩ s := by
      rw [← hpreU]
      exact ⟨hfu, hx⟩
    exact hxu'.1
  · right
    have hxv' : x ∈ v' ∩ s := by
      rw [← hpreV]
      exact ⟨hfv, hx⟩
    exact hxv'.1

/-- Pull witnesses meeting each image open back to the corresponding source opens. -/
theorem imageHitPullback : ImageHitPullbackPackage.{u, v} := by
  intro alpha beta _ _ s f u v u' v' hpreU hpreV
  rintro ⟨_, ⟨x, hx, rfl⟩, hfu⟩ ⟨_, ⟨y, hy, rfl⟩, hfv⟩
  constructor
  · refine ⟨x, hx, ?_⟩
    have hxu' : x ∈ u' ∩ s := by
      rw [← hpreU]
      exact ⟨hfu, hx⟩
    exact hxu'.1
  · refine ⟨y, hy, ?_⟩
    have hyv' : y ∈ v' ∩ s := by
      rw [← hpreV]
      exact ⟨hfv, hy⟩
    exact hyv'.1

/-- Apply source preconnectedness after the cover and endpoint witnesses are pulled back. -/
theorem sourceIntersection : SourceIntersectionPackage.{u} := by
  intro alpha _ s u' v' hs hu' hv' hcover hsu' hsv'
  exact hs u' v' hu' hv' hcover hsu' hsv'

/-- Send a source intersection witness into the required image intersection. -/
theorem intersectionPushforward : IntersectionPushforwardPackage.{u, v} := by
  intro alpha beta _ _ s f u v u' v' hpreU hpreV
  rintro ⟨z, hzs, hzu', hzv'⟩
  have hfu : f z ∈ u := by
    have hz : z ∈ f ⁻¹' u ∩ s := by
      rw [hpreU]
      exact ⟨hzu', hzs⟩
    exact hz.1
  have hfv : f z ∈ v := by
    have hz : z ∈ f ⁻¹' v ∩ s := by
      rw [hpreV]
      exact ⟨hzv', hzs⟩
    exact hz.1
  exact ⟨f z, ⟨z, hzs, rfl⟩, hfu, hfv⟩

/-- Compose the five explicit leaves into the arbitrary-open separation engine. -/
theorem separationEngine : SeparationEngine.{u, v} :=
  separationEngine_of_components relativePreimages imageCoverPullback imageHitPullback
    sourceIntersection intersectionPushforward

/-- Repackage the separation engine as image preconnectedness. -/
theorem imagePreconnected : ImagePreconnectedPackage.{u, v} :=
  imagePreconnected_of_separationEngine separationEngine

/-- Map a source witness through the function to make the direct image nonempty. -/
theorem imageNonempty : ImageNonemptyPackage.{u, v} := by
  intro alpha beta _ _ s hs f
  exact Set.image_nonempty.mpr hs

/-- Reassemble nonemptiness and preconnectedness into local image connectedness. -/
theorem localConnectedImage_components : LocalConnectedImagePackage.{u, v} :=
  localConnectedImage_of_components imageNonempty imagePreconnected

/-- The pinned `IsConnected.image` theorem installed at the exact frozen local interface. -/
theorem localConnectedImage_mathlib : LocalConnectedImagePackage.{u, v} := by
  intro alpha beta _ _ s hs f hf
  exact hs.image f hf

/-- The exact canonical root, obtained through every required edge of the frozen proof graph. -/
theorem connectedImage : ConnectedImageTarget.{u, v} :=
  root_of_localConnectedImage globalToLocalContinuity localConnectedImage_mathlib

/-- An exact root independently reconstructed through every internal component package. -/
theorem connectedImage_via_components : ConnectedImageTarget.{u, v} :=
  root_of_localConnectedImage globalToLocalContinuity localConnectedImage_components

/-- The same root exposed through the frozen terminal-assembly interface. -/
theorem connectedImage_via_exactAssembly : ConnectedImageTarget.{u, v} :=
  root_of_exactAssembly
    (exactAssembly_of_packages globalToLocalContinuity localConnectedImage_mathlib)

#print axioms IsPreconnected.image
#print axioms IsConnected.image
#print axioms relativePreimages
#print axioms imageCoverPullback
#print axioms imageHitPullback
#print axioms sourceIntersection
#print axioms intersectionPushforward
#print axioms separationEngine
#print axioms imagePreconnected
#print axioms imageNonempty
#print axioms localConnectedImage_components
#print axioms localConnectedImage_mathlib
#print axioms connectedImage
#print axioms connectedImage_via_components
#print axioms connectedImage_via_exactAssembly
#print sorries IsPreconnected.image
#print sorries IsConnected.image
#print sorries relativePreimages
#print sorries imageCoverPullback
#print sorries imageHitPullback
#print sorries sourceIntersection
#print sorries intersectionPushforward
#print sorries separationEngine
#print sorries imagePreconnected
#print sorries imageNonempty
#print sorries localConnectedImage_components
#print sorries localConnectedImage_mathlib
#print sorries connectedImage
#print sorries connectedImage_via_components
#print sorries connectedImage_via_exactAssembly

end Stage1Instances.THM_M_0626.Proof
