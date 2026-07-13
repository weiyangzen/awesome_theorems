import Mathlib.Analysis.Complex.Basic

/-!
# THM-M-0276 canonical Lean statement

This module freezes the ordinary same-field real-and-complex form of the Banach open mapping
theorem selected from the immutable lecture-note statement admitted at intake. It contains only
the target, a definitional expansion transport, and statement mutations; it does not prove the
open mapping theorem.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0276

universe u v

/-- The Banach open mapping proposition over the real scalar field. -/
def RealOpenMappingTarget : Prop :=
  forall (E : Type u) (F : Type v)
      [NormedAddCommGroup E] [NormedSpace Real E] [CompleteSpace E]
      [NormedAddCommGroup F] [NormedSpace Real F] [CompleteSpace F]
      (f : E →L[Real] F),
    Function.Surjective f -> IsOpenMap f

/-- The Banach open mapping proposition over the complex scalar field. -/
def ComplexOpenMappingTarget : Prop :=
  forall (E : Type u) (F : Type v)
      [NormedAddCommGroup E] [NormedSpace Complex E] [CompleteSpace E]
      [NormedAddCommGroup F] [NormedSpace Complex F] [CompleteSpace F]
      (f : E →L[Complex] F),
    Function.Surjective f -> IsOpenMap f

/-- Exact source-selected target: the Banach open mapping theorem over both `Real` and `Complex`. -/
def BanachOpenMappingTarget : Prop :=
  RealOpenMappingTarget.{u, v} /\ ComplexOpenMappingTarget.{u, v}

/-- Directly expands the open-map terminology. -/
def ExpandedOpenMappingTarget : Prop :=
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

/-- Checked definitional transport to the source's expanded definition of an open map. -/
theorem banachOpenMappingTarget_iff_expandedOpenMappingTarget :
    BanachOpenMappingTarget.{u, v} <-> ExpandedOpenMappingTarget.{u, v} :=
  Iff.rfl

/-! Structural mutations elaborate but are intentionally distinct from the canonical target. -/

def mutationRemovedSurjectivityHypothesis : Prop :=
  (forall (E : Type u) (F : Type v)
      [NormedAddCommGroup E] [NormedSpace Real E] [CompleteSpace E]
      [NormedAddCommGroup F] [NormedSpace Real F] [CompleteSpace F]
      (f : E →L[Real] F),
    IsOpenMap f) /\
  (forall (E : Type u) (F : Type v)
      [NormedAddCommGroup E] [NormedSpace Complex E] [CompleteSpace E]
      [NormedAddCommGroup F] [NormedSpace Complex F] [CompleteSpace F]
      (f : E →L[Complex] F),
    IsOpenMap f)

def mutationChangedScalarDomain : Prop :=
  RealOpenMappingTarget.{u, v}

def mutationChangedBinderScope : Prop :=
  (forall (E : Type u) (F : Type v)
      [NormedAddCommGroup E] [NormedSpace Real E] [CompleteSpace E]
      [NormedAddCommGroup F] [NormedSpace Real F] [CompleteSpace F],
    exists f : E →L[Real] F, Function.Surjective f -> IsOpenMap f) /\
  (forall (E : Type u) (F : Type v)
      [NormedAddCommGroup E] [NormedSpace Complex E] [CompleteSpace E]
      [NormedAddCommGroup F] [NormedSpace Complex F] [CompleteSpace F],
    exists f : E →L[Complex] F, Function.Surjective f -> IsOpenMap f)

def mutationDroppedDomainCompleteness : Prop :=
  (forall (E : Type u) (F : Type v)
      [NormedAddCommGroup E] [NormedSpace Real E]
      [NormedAddCommGroup F] [NormedSpace Real F] [CompleteSpace F]
      (f : E →L[Real] F),
    Function.Surjective f -> IsOpenMap f) /\
  (forall (E : Type u) (F : Type v)
      [NormedAddCommGroup E] [NormedSpace Complex E]
      [NormedAddCommGroup F] [NormedSpace Complex F] [CompleteSpace F]
      (f : E →L[Complex] F),
    Function.Surjective f -> IsOpenMap f)

def mutationExcludedNoninjectiveBoundary : Prop :=
  (forall (E : Type u) (F : Type v)
      [NormedAddCommGroup E] [NormedSpace Real E] [CompleteSpace E]
      [NormedAddCommGroup F] [NormedSpace Real F] [CompleteSpace F]
      (f : E →L[Real] F),
    Function.Bijective f -> IsOpenMap f) /\
  (forall (E : Type u) (F : Type v)
      [NormedAddCommGroup E] [NormedSpace Complex E] [CompleteSpace E]
      [NormedAddCommGroup F] [NormedSpace Complex F] [CompleteSpace F]
      (f : E →L[Complex] F),
    Function.Bijective f -> IsOpenMap f)

variable
  (hRemoved : mutationRemovedSurjectivityHypothesis.{u, v})
  (hDomain : mutationChangedScalarDomain.{u, v})
  (hScope : mutationChangedBinderScope.{u, v})
  (hCompleteness : mutationDroppedDomainCompleteness.{u, v})
  (hBoundary : mutationExcludedNoninjectiveBoundary.{u, v})

#check_failure (hRemoved : BanachOpenMappingTarget.{u, v})
#check_failure (hDomain : BanachOpenMappingTarget.{u, v})
#check_failure (hScope : BanachOpenMappingTarget.{u, v})
#check_failure (hCompleteness : BanachOpenMappingTarget.{u, v})
#check_failure (hBoundary : BanachOpenMappingTarget.{u, v})

#check banachOpenMappingTarget_iff_expandedOpenMappingTarget
#print axioms banachOpenMappingTarget_iff_expandedOpenMappingTarget

set_option pp.universes true in
set_option pp.explicit true in
#print BanachOpenMappingTarget

end Stage1Instances.THM_M_0276
