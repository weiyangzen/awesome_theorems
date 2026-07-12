import Mathlib.SetTheory.Cardinal.SchroederBernstein

/-!
# THM-M-0768: exact Cantor-Bernstein-Schroeder statement

This module freezes the statement and its checked encoding transport. It does not invoke the
library proof of the Cantor-Bernstein-Schroeder theorem.
-/

namespace Stage1Instances.THM_M_0768

open Function

universe u v

/-- If arbitrary functions inject two types into one another, a bijection between them exists. -/
def CantorBernsteinSchroederTarget : Prop :=
  forall {alpha : Type u} {beta : Type v} {f : alpha -> beta} {g : beta -> alpha},
    Injective f -> Injective g -> exists h : alpha -> beta, Bijective h

/-- The bundled embedding/equivalence encoding credited as an alternate statement. -/
def BundledTarget : Prop :=
  forall {alpha : Type u} {beta : Type v},
    (alpha ↪ beta) -> (beta ↪ alpha) -> Nonempty (alpha ≃ beta)

/-- The raw-function and bundled encodings are propositionally equivalent without using the
Cantor-Bernstein-Schroeder proof: each direction assumes the corresponding whole statement. -/
theorem target_iff_bundled :
    CantorBernsteinSchroederTarget.{u, v} ↔ BundledTarget.{u, v} := by
  constructor
  · intro raw alpha beta f g
    obtain ⟨h, hh⟩ := @raw alpha beta f g f.injective g.injective
    exact ⟨Equiv.ofBijective h hh⟩
  · intro bundled alpha beta f g hf hg
    obtain ⟨e⟩ := @bundled alpha beta ⟨f, hf⟩ ⟨g, hg⟩
    exact ⟨e, e.bijective⟩

-- Structural mutations: these elaborate, but the statement checker requires distinct expressions.
def mutationRemovedReverseInjectivity : Prop :=
  forall {alpha : Type u} {beta : Type v} {f : alpha -> beta} {_g : beta -> alpha},
    Injective f -> exists h : alpha -> beta, Bijective h

def mutationChangedDomain : Prop :=
  forall {alpha : Type u} {f g : alpha -> alpha},
    Injective f -> Injective g -> exists h : alpha -> alpha, Bijective h

def mutationChangedBinderScope : Prop :=
  forall {alpha : Type u} {beta : Type v},
    (exists h : alpha -> beta, Bijective h) /\
      forall {f : alpha -> beta} {g : beta -> alpha}, Injective f -> Injective g -> True

def mutationExcludesEmptyBoundary : Prop :=
  forall {alpha : Type u} {beta : Type v},
    Nonempty alpha -> Nonempty beta ->
      forall {f : alpha -> beta} {g : beta -> alpha},
        Injective f -> Injective g -> exists h : alpha -> beta, Bijective h

end Stage1Instances.THM_M_0768

set_option pp.explicit true in
#print Stage1Instances.THM_M_0768.CantorBernsteinSchroederTarget
