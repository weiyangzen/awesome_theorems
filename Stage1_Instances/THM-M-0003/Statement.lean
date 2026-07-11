import Mathlib.Algebra.Homology.ShortComplex.SnakeLemma

/-!
# THM-M-0003: snake lemma

This module freezes the six-term kernel/cokernel exactness statement for a
snake input in an arbitrary abelian category. It does not prove that target.
-/

universe v u

namespace Stage1Instances.THM_M_0003

open CategoryTheory

/-- The canonical category-level snake-lemma target. `SnakeInput` packages the
four-row diagram, kernel/cokernel witnesses, exact middle rows, and the endpoint
epi/mono assumptions needed for the six-term sequence. -/
def SnakeLemmaTarget : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C]
    (S : ShortComplex.SnakeInput C),
    S.composableArrows.Exact

/-- A pointwise grouping of the same target, used to check the binder
transport rather than relying on prose to identify the canonical statement. -/
def PointwiseSnakeLemmaTarget
    (C : Type u) [Category.{v} C] [Abelian C] : Prop :=
  ∀ S : ShortComplex.SnakeInput C, S.composableArrows.Exact

/-- Checked transport between the canonical closed proposition and its
pointwise encoding. -/
theorem snakeLemmaTarget_iff_pointwise :
    SnakeLemmaTarget.{v, u} ↔
      ∀ (C : Type u) [Category.{v} C] [Abelian C],
        PointwiseSnakeLemmaTarget C := by
  rfl

-- Structural mutations are elaborated and compared by `check_statement.py`.
def mutationRemovedSnakeInput : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C], Nonempty C

def mutationChangedCategoryUniverse : Prop :=
  ∀ (C : Type (u + 1)) [Category.{v} C] [Abelian C]
    (S : ShortComplex.SnakeInput C),
    S.composableArrows.Exact

def mutationChangedBinderScope : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C],
    Nonempty (ShortComplex.SnakeInput C)

def mutationShortExactEndpoints : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C]
    (S : ShortComplex.SnakeInput C) [Mono S.L₁.f] [Epi S.L₂.g],
    S.composableArrows.Exact

end Stage1Instances.THM_M_0003

set_option pp.explicit true in
#print Stage1Instances.THM_M_0003.SnakeLemmaTarget
