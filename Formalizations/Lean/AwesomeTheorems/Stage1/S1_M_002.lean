import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Basic
import Mathlib.AlgebraicGeometry.EllipticCurve.NormalForms
import Mathlib.Algebra.QuadraticAlgebra.Basic
import Mathlib.Data.Set.Finite.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.RingTheory.ClassGroup
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# S1-M-002 / THM-M-0392: Mordell equation

This Stage1 artifact records the repo-local Lean 4 statement shape for the
Mordell equation finiteness target: for each nonzero integer parameter `k`, the
integer solutions of `y^2 = x^3 + k` should form a finite set.

The full finiteness theorem is not proved here.  The file deliberately exposes a
precise `Prop` target plus small checked equation-normalization wrappers, so the
module remains compilable without proof placeholders or new trust declarations.
-/

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_002

universe u

/-- The affine Mordell equation `y^2 = x^3 + k` over the integers. -/
def MordellEquation (k x y : Int) : Prop :=
  y ^ 2 = x ^ 3 + k

/-- Integration-ready public spelling for the affine Mordell equation. -/
def MordellEq (k x y : Int) : Prop :=
  MordellEquation k x y

/-- The public spelling is definitionally the normalized cubic equation. -/
theorem mordellEq_iff (k x y : Int) :
    MordellEq k x y ↔ y ^ 2 = x ^ 3 + k :=
  Iff.rfl

/-- The integer solution set for a fixed Mordell parameter `k`. -/
def IntegralSolutions (k : Int) : Set (Int × Int) :=
  {p | MordellEquation k p.1 p.2}

/-- Integration-ready public spelling for the integer Mordell solution set. -/
def MordellSolutions (k : Int) : Set (Int × Int) :=
  {p | MordellEq k p.1 p.2}

/-- The public solution-set spelling is definitionally the Stage1 solution set. -/
theorem mordellSolutions_eq_integralSolutions (k : Int) :
    MordellSolutions k = IntegralSolutions k :=
  rfl

/-- Membership in the public solution-set spelling unfolds to the equation. -/
theorem mem_mordellSolutions_iff (k x y : Int) :
    (x, y) ∈ MordellSolutions k ↔ MordellEq k x y :=
  Iff.rfl

/--
Stage1 normalized statement shape.

The nonzero-parameter hypothesis is essential: when `k = 0`, the parametrized
family `(x, y) = (t^2, t^3)` supplies infinitely many integer solutions.
-/
def StatementShape : Prop :=
  ∀ k : Int, k ≠ 0 → Set.Finite (IntegralSolutions k)

/-- Statement-shape wrapper using the integration-ready public names. -/
def MordellStatementShape : Prop :=
  ∀ k : Int, k ≠ 0 → Set.Finite (MordellSolutions k)

/-- The existing Stage1 shape and the public-name wrapper are definitionally equal. -/
theorem statementShape_iff_mordellStatementShape :
    StatementShape ↔ MordellStatementShape :=
  Iff.rfl

/-- Projection from the public-name wrapper back to the canonical Stage1 shape. -/
theorem statementShape_of_mordellStatementShape
    (h : MordellStatementShape) : StatementShape :=
  statementShape_iff_mordellStatementShape.mpr h

/-- Projection from the canonical Stage1 shape to the public-name wrapper. -/
theorem mordellStatementShape_of_statementShape
    (h : StatementShape) : MordellStatementShape :=
  statementShape_iff_mordellStatementShape.mp h

/-! ## Fixed-parameter enumeration surface audit -/

/--
Preferred public statement surface for a fixed parameter.

The theorem should assert finiteness of the semantic solution set; any concrete
`Finset` enumeration is then a derived witness rather than the main statement.
-/
def FixedKFiniteSurface (k : Int) : Prop :=
  Set.Finite (MordellSolutions k)

/-- Downstream enumeration witness for a fixed parameter. -/
def FixedKFinsetEnumeration (k : Int) : Prop :=
  ∃ s : Finset (Int × Int), (s : Set (Int × Int)) = MordellSolutions k

/-- A finite solution set gives a canonical noncomputable `Finset` enumeration. -/
noncomputable def mordellSolutionsFinset
    (k : Int) (h : FixedKFiniteSurface k) : Finset (Int × Int) :=
  h.toFinset

/-- The derived enumeration has exactly the same members as the solution set. -/
theorem mem_mordellSolutionsFinset_iff
    (k : Int) (h : FixedKFiniteSurface k) (p : Int × Int) :
    p ∈ mordellSolutionsFinset k h ↔ p ∈ MordellSolutions k :=
  h.mem_toFinset

/--
Checked bridge between the preferred `Set.Finite` theorem surface and an
existential `Finset` enumeration witness.
-/
theorem fixedKFiniteSurface_iff_finsetEnumeration (k : Int) :
    FixedKFiniteSurface k ↔ FixedKFinsetEnumeration k := by
  constructor
  · intro h
    exact ⟨h.toFinset, h.coe_toFinset⟩
  · rintro ⟨s, hs⟩
    unfold FixedKFiniteSurface
    rw [← hs]
    exact s.finite_toSet

/-- Checked normalization witness for the zero-parameter family. -/
theorem zeroParameterFamily (t : Int) :
    MordellEquation 0 (t ^ 2) (t ^ 3) := by
  unfold MordellEquation
  ring

/-- A checked point constructor for any explicit integer solution proof. -/
theorem mem_integralSolutions_iff (k x y : Int) :
    (x, y) ∈ IntegralSolutions k ↔ MordellEquation k x y :=
  Iff.rfl

/-! ## Congruence-only local obstruction leaves -/

/--
Finite `ZMod 8` check behind the Lean 3 local obstruction
`x_odd_two_three_aux`.
-/
theorem zmod8_mordell_evenCube_obstruction
    (D Y X : ZMod 8)
    (hD : D ∈ ({2, 3, 5, 6, 7} : Finset (ZMod 8))) :
    Y ^ 2 - D ≠ (X + X) ^ 3 := by
  revert D Y X
  native_decide

/-- Residues `d % 4 = 2` land in the obstructing `ZMod 8` residue set. -/
theorem zmod8_mordell_obstruction_of_emod_four_eq_two
    {d : Int} (hd : d % 4 = 2) :
    (d : ZMod 8) ∈ ({2, 3, 5, 6, 7} : Finset (ZMod 8)) := by
  have hmul_add_two
      (q : ZMod 8) :
      q * 4 + 2 ∈ ({2, 3, 5, 6, 7} : Finset (ZMod 8)) := by
    revert q
    native_decide
  have hdcast : (d : ZMod 8) = ((d / (4 : Int) : ZMod 8) * 4 + 2) := by
    calc
      (d : ZMod 8) = ((d / (4 : Int) * 4 + d % 4 : Int) : ZMod 8) := by
        rw [Int.ediv_mul_add_emod]
      _ = ((d / (4 : Int) : ZMod 8) * 4 + 2) := by
        rw [hd]
        norm_num
  rw [hdcast]
  exact hmul_add_two (d / (4 : Int) : ZMod 8)

/-- Residues `d % 4 = 3` land in the obstructing `ZMod 8` residue set. -/
theorem zmod8_mordell_obstruction_of_emod_four_eq_three
    {d : Int} (hd : d % 4 = 3) :
    (d : ZMod 8) ∈ ({2, 3, 5, 6, 7} : Finset (ZMod 8)) := by
  have hmul_add_three
      (q : ZMod 8) :
      q * 4 + 3 ∈ ({2, 3, 5, 6, 7} : Finset (ZMod 8)) := by
    revert q
    native_decide
  have hdcast : (d : ZMod 8) = ((d / (4 : Int) : ZMod 8) * 4 + 3) := by
    calc
      (d : ZMod 8) = ((d / (4 : Int) * 4 + d % 4 : Int) : ZMod 8) := by
        rw [Int.ediv_mul_add_emod]
      _ = ((d / (4 : Int) : ZMod 8) * 4 + 3) := by
        rw [hd]
        norm_num
  rw [hdcast]
  exact hmul_add_three (d / (4 : Int) : ZMod 8)

/-- Residues `d % 8 = 5` land in the obstructing `ZMod 8` residue set. -/
theorem zmod8_mordell_obstruction_of_emod_eight_eq_five
    {d : Int} (hd : d % 8 = 5) :
    (d : ZMod 8) ∈ ({2, 3, 5, 6, 7} : Finset (ZMod 8)) := by
  have hmul_add_five
      (q : ZMod 8) :
      q * 8 + 5 ∈ ({2, 3, 5, 6, 7} : Finset (ZMod 8)) := by
    revert q
    native_decide
  have hdcast : (d : ZMod 8) = ((d / (8 : Int) : ZMod 8) * 8 + 5) := by
    calc
      (d : ZMod 8) = ((d / (8 : Int) * 8 + d % 8 : Int) : ZMod 8) := by
        rw [Int.ediv_mul_add_emod]
      _ = ((d / (8 : Int) : ZMod 8) * 8 + 5) := by
        rw [hd]
        norm_num
  rw [hdcast]
  exact hmul_add_five (d / (8 : Int) : ZMod 8)

/--
Port of the Lean 3 congruence-only leaf `x_odd_two_three_aux`.

There is no even `x` in an integer equation `y^2 - d = x^3` when `d` has one
of the obstructing residues modulo `8`.
-/
theorem x_odd_two_three_aux
    {x y d : Int}
    (hd : (d : ZMod 8) ∈ ({2, 3, 5, 6, 7} : Finset (ZMod 8)))
    (h_eqn : y ^ 2 - d = x ^ 3) :
    ¬ Even x := by
  rintro ⟨X, rfl⟩
  have hmod :
      (y : ZMod 8) ^ 2 - (d : ZMod 8) = ((X : ZMod 8) + X) ^ 3 := by
    calc
      (y : ZMod 8) ^ 2 - (d : ZMod 8) = ((y ^ 2 - d : Int) : ZMod 8) := by
        norm_num
      _ = (((X + X) ^ 3 : Int) : ZMod 8) := by
        rw [h_eqn]
      _ = ((X : ZMod 8) + X) ^ 3 := by
        norm_num
  exact zmod8_mordell_evenCube_obstruction
    (d : ZMod 8) (y : ZMod 8) (X : ZMod 8) hd hmod

/--
Port of the Lean 3 local obstruction `x_odd_two_three`.

If `d % 4` is `2` or `3`, then every integer solution of `y^2 - d = x^3` has
odd `x`.
-/
theorem x_odd_two_three
    {x y d : Int}
    (hd : d % 4 = 2 ∨ d % 4 = 3)
    (h_eqn : y ^ 2 - d = x ^ 3) :
    ¬ Even x := by
  refine x_odd_two_three_aux ?_ h_eqn
  rcases hd with hd | hd
  · exact zmod8_mordell_obstruction_of_emod_four_eq_two hd
  · exact zmod8_mordell_obstruction_of_emod_four_eq_three hd

/-- Port of the Lean 3 local obstruction for `d % 4 = 3`. -/
theorem x_odd_three
    {x y d : Int}
    (hd : d % 4 = 3)
    (h_eqn : y ^ 2 - d = x ^ 3) :
    ¬ Even x :=
  x_odd_two_three (Or.inr hd) h_eqn

/-- Port of the Lean 3 local obstruction for `d % 4 = 2`. -/
theorem x_odd_two
    {x y d : Int}
    (hd : d % 4 = 2)
    (h_eqn : y ^ 2 - d = x ^ 3) :
    ¬ Even x :=
  x_odd_two_three (Or.inl hd) h_eqn

/-- Port of the Lean 3 local obstruction for `d % 8 = 5`. -/
theorem x_odd_five
    {x y d : Int}
    (hd : d % 8 = 5)
    (h_eqn : y ^ 2 - d = x ^ 3) :
    ¬ Even x :=
  x_odd_two_three_aux
    (zmod8_mordell_obstruction_of_emod_eight_eq_five hd) h_eqn

/--
Mordell-equation spelling of the modulo-`8` obstruction leaf.

This is a local obstruction only: it proves parity of `x` under residue
hypotheses, not finiteness of all integer solutions.
-/
theorem mordell_no_even_x_of_zmod8_obstruction
    {k x y : Int}
    (hk : (k : ZMod 8) ∈ ({2, 3, 5, 6, 7} : Finset (ZMod 8)))
    (h_eqn : MordellEquation k x y) :
    ¬ Even x := by
  refine x_odd_two_three_aux (x := x) (y := y) (d := k) hk ?_
  unfold MordellEquation at h_eqn
  rw [h_eqn]
  ring

/-! ## mathlib elliptic-curve object model -/

/--
The short Weierstrass curve `Y^2 = X^3 + k` over an arbitrary commutative ring.

This is only an object-model bridge.  It does not assert finiteness of integral
points.
-/
def mordellCurve (R : Type u) [CommRing R] (k : R) : WeierstrassCurve R :=
  { a₁ := 0, a₂ := 0, a₃ := 0, a₄ := 0, a₆ := k }

/-- The Mordell curve is definitionally in short Weierstrass normal form. -/
instance mordellCurve_isShortNF (R : Type u) [CommRing R] (k : R) :
    (mordellCurve R k).IsShortNF where
  a₁ := rfl
  a₂ := rfl
  a₃ := rfl

/-- The mathlib affine equation for `mordellCurve R k` unfolds to `y^2 = x^3 + k`. -/
theorem mordellCurve_affineEquation_iff
    (R : Type u) [CommRing R] (k x y : R) :
    (mordellCurve R k).toAffine.Equation x y ↔ y ^ 2 = x ^ 3 + k := by
  rw [WeierstrassCurve.Affine.equation_iff]
  simp [mordellCurve]

/--
Task-surface spelling of the mathlib wrapper for
`Wk = {a₁ := 0, a₂ := 0, a₃ := 0, a₄ := 0, a₆ := k}`.
-/
theorem Wk_toAffine_Equation_iff
    (R : Type u) [CommRing R] (k x y : R) :
    (let Wk : WeierstrassCurve R :=
      { a₁ := 0, a₂ := 0, a₃ := 0, a₄ := 0, a₆ := k }
     Wk.toAffine.Equation x y) ↔ y ^ 2 = x ^ 3 + k := by
  simpa [mordellCurve] using mordellCurve_affineEquation_iff R k x y

/-- Integer specialization of the affine-equation bridge. -/
theorem mordellCurveInt_affineEquation_iff (k x y : Int) :
    (mordellCurve Int k).toAffine.Equation x y ↔ MordellEquation k x y := by
  simpa [MordellEquation] using mordellCurve_affineEquation_iff Int k x y

/-- Discriminant computation for the short Mordell curve. -/
theorem mordellCurve_discriminant (R : Type u) [CommRing R] (k : R) :
    (mordellCurve R k).Δ = -432 * k ^ 2 := by
  rw [WeierstrassCurve.Δ_of_isShortNF]
  simp [mordellCurve]
  ring

/--
Over `Rat`, a nonzero integer parameter gives a mathlib `IsElliptic` object.

This proves the discriminant is a unit after coercing `k` to `Rat`; it is still
only the nonsingularity gate, not an integral-points theorem.
-/
theorem mordellCurveRat_isElliptic_of_ne_zero (k : Int) (hk : k ≠ 0) :
    (mordellCurve Rat (k : Rat)).IsElliptic := by
  refine ⟨?_⟩
  rw [mordellCurve_discriminant]
  refine isUnit_iff_ne_zero.mpr ?_
  have hkRat : (k : Rat) ≠ 0 := by
    exact_mod_cast hk
  exact mul_ne_zero (by norm_num) (pow_ne_zero 2 hkRat)

/-! ## Lean 4 replacement for the Lean 3 `quad_ring` branch -/

/--
Lean 4 replacement object for the Lean 3 `quad_ring` used in the historical
class-group descent branch.

The replacement is mathlib's `QuadraticAlgebra R D 0`, whose generator `ω`
satisfies `ω^2 = D`.  This is only the quadratic-algebra substrate; the descent
still needs a separate number-field/order/class-group bridge before it can be
attempted as a proof of Mordell finiteness.
-/
abbrev QuadraticDescentAlgebra (R : Type u) [Zero R] (D : R) : Type u :=
  QuadraticAlgebra R D (0 : R)

/-- The canonical square-root generator in the chosen quadratic algebra. -/
abbrev quadraticDescentGenerator
    (R : Type u) [Zero R] [One R] (D : R) :
    QuadraticDescentAlgebra R D :=
  (QuadraticAlgebra.omega : QuadraticAlgebra R D 0)

/-- In the replacement algebra, the distinguished generator squares to `D`. -/
theorem quadraticDescentGenerator_sq
    (R : Type u) [CommRing R] (D : R) :
    quadraticDescentGenerator R D * quadraticDescentGenerator R D =
      algebraMap R (QuadraticDescentAlgebra R D) D := by
  ext <;> simp [QuadraticDescentAlgebra, quadraticDescentGenerator]

/-- The replacement algebra has the expected conjugation on the generator. -/
theorem star_quadraticDescentGenerator
    (R : Type u) [CommRing R] (D : R) :
    star (quadraticDescentGenerator R D) =
      -quadraticDescentGenerator R D := by
  ext <;> simp [QuadraticDescentAlgebra, quadraticDescentGenerator]

/-- The norm of the replacement generator is `-D`. -/
theorem norm_quadraticDescentGenerator
    (R : Type u) [CommRing R] (D : R) :
    (quadraticDescentGenerator R D).norm = -D := by
  simp [quadraticDescentGenerator, QuadraticAlgebra.norm_def]

/-- Coordinates in the replacement algebra have the usual norm `x^2 - D*y^2`. -/
theorem quadraticDescentAlgebra_norm_mk
    (R : Type u) [CommRing R] (D x y : R) :
    (⟨x, y⟩ : QuadraticDescentAlgebra R D).norm = x ^ 2 - D * y ^ 2 := by
  simp [QuadraticAlgebra.norm_def, pow_two]
  ring

/--
Checked decision record for the `quad_ring` replacement.

Use `Mathlib.Algebra.QuadraticAlgebra.Basic`, specifically
`QuadraticAlgebra R D 0`, for the quadratic algebra substrate.  Do not start
the class-group descent branch from a bespoke port of Lean 3 `quad_ring`.
-/
def quadRingReplacementDecision : String :=
  "use mathlib QuadraticAlgebra R D 0 as the Lean 4 replacement for Lean 3 quad_ring"

/--
Boundary for the later class-group descent branch.

`QuadraticAlgebra R D 0` settles only the quadratic-algebra object model.  The
descent branch remains blocked until a concrete number-field/order/integrality
surface and the corresponding `ClassGroup` bridge are selected and checked.
-/
def classGroupDescentReplacementBlocker : String :=
  "quadratic algebra chosen; number-field/order/ClassGroup bridge still open"

/-! ## Historical Lean 3 reference boundary -/

/--
Historical source repository for the Lean 3 Mordell-equation formalization.

This is recorded only as audit metadata for later public backfill.  It is not a
Lean 4 dependency of this Stage1 module.
-/
def historicalLean3MordellReferenceRepository : String :=
  "https://github.com/lean-forward/class-group-and-mordell-equation, main/HEAD baba2049f3bfe4d2cc184f8205997333e7c58638"

/--
Toolchain metadata observed from the historical project's `leanpkg.toml`.

The project targets the community fork of Lean 3, so it cannot close a Lean 4
Stage1 theorem slot without a port or an explicitly pinned/vendored integration
that validates in this repository.
-/
def historicalLean3MordellReferenceToolchain : String :=
  "leanprover-community/lean:3.49.1 with Lean 3 mathlib rev cf9386b56953fb40904843af98b7a80757bbe7f9"

/--
Completion boundary for citing the historical Lean 3 project.

The source may guide future theorem-tree and porting work, but it is not a
Lean 4 / Lake dependency and is not evidence of repo-local completion for the
Mordell finiteness theorem.
-/
def historicalLean3MordellReferenceBoundary : String :=
  "historical/formalization reference only; not a Lean 4 dependency; not repo-local completion evidence"

/-! ## Audit probes -/

#check MordellEq
#check MordellSolutions
#check MordellStatementShape
#check statementShape_iff_mordellStatementShape
#check FixedKFiniteSurface
#check FixedKFinsetEnumeration
#check mordellSolutionsFinset
#check mem_mordellSolutionsFinset_iff
#check fixedKFiniteSurface_iff_finsetEnumeration
#check zmod8_mordell_evenCube_obstruction
#check zmod8_mordell_obstruction_of_emod_four_eq_two
#check zmod8_mordell_obstruction_of_emod_four_eq_three
#check zmod8_mordell_obstruction_of_emod_eight_eq_five
#check x_odd_two_three_aux
#check x_odd_two_three
#check x_odd_three
#check x_odd_two
#check x_odd_five
#check mordell_no_even_x_of_zmod8_obstruction
#check mordellCurve
#check mordellCurve_affineEquation_iff
#check Wk_toAffine_Equation_iff
#check mordellCurveInt_affineEquation_iff
#check mordellCurve_discriminant
#check mordellCurveRat_isElliptic_of_ne_zero
#check QuadraticAlgebra
#check QuadraticAlgebra.omega
#check QuadraticAlgebra.norm
#check ClassGroup
#check QuadraticDescentAlgebra
#check quadraticDescentGenerator
#check quadraticDescentGenerator_sq
#check star_quadraticDescentGenerator
#check norm_quadraticDescentGenerator
#check quadraticDescentAlgebra_norm_mk
#check quadRingReplacementDecision
#check classGroupDescentReplacementBlocker
#check historicalLean3MordellReferenceRepository
#check historicalLean3MordellReferenceToolchain
#check historicalLean3MordellReferenceBoundary

/-- mathlib modules audited for repo-local Lean 4 anchors in this repair pass. -/
def mathlibAnchorModules : List String := [
  "Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Basic",
  "Mathlib.AlgebraicGeometry.EllipticCurve.NormalForms",
  "Mathlib.Algebra.QuadraticAlgebra.Basic",
  "Mathlib.Data.Set.Finite.Basic",
  "Mathlib.Tactic.NormNum",
  "Mathlib.Tactic.Ring",
  "Mathlib.RingTheory.ClassGroup",
  "Mathlib.NumberTheory.Dioph",
  "Mathlib.NumberTheory.Height.Basic",
  "Mathlib.NumberTheory.Height.Northcott",
  "Mathlib.NumberTheory.ClassNumber.Finite",
  "Mathlib.NumberTheory.Padics.Hensel",
  "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass",
  "Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point",
  "Mathlib.AlgebraicGeometry.EllipticCurve.Jacobian.Point"
]

/-- Search terms used for the local and external anchor audit. -/
def anchorSearchTerms : List String := [
  "Mordell",
  "mordell",
  "Bachet",
  "IntegralSolutions",
  "integral points",
  "EllipticCurve",
  "y^2 = x^3 + k",
  "class group Mordell equation Lean"
]

/-- Date of the renewed external Lean 4 port audit for this Stage1 child. -/
def externalLean4PortAuditDate : String := "2026-05-01"

/--
External source classes checked in the renewed Lean 4 port audit.

The audit is deliberately recorded as data, not as completion evidence.
-/
def externalLean4PortAuditScope : List String := [
  "repo-local mathlib checkout under Formalizations/Lean/.lake/packages/mathlib",
  "web search for Lean 4 Mordell equation and y^2 = x^3 + k source anchors",
  "GitHub source search pages for Mordell plus lakefile.lean or import Mathlib",
  "known lean-forward/class-group-and-mordell-equation repository"
]

/--
Renewed Lean 4 port audit result.

No Lean 4 / Lake port of the full nonzero-parameter Mordell-equation finiteness
theorem was identified.  The repo-local closure therefore remains a checked
statement-shape and infrastructure artifact, not an external-upstream proof.
-/
def externalLean4PortAuditResult : String :=
  "no Lean 4/Lake port of Mordell-equation finiteness identified on 2026-05-01"

/--
Concrete integration blocker for the only located formal Mordell-equation
project.

The public `lean-forward/class-group-and-mordell-equation` code is Lean 3
`leanpkg.toml` code targeting `leanprover-community/lean:3.49.1`; it cannot be
imported by this Lean 4 Lake project without a port or a compatibility bridge.
-/
def externalLean4PortIntegrationBlocker : String :=
  "located formal Mordell-equation project is Lean 3 leanpkg code, not a Lean 4 Lake dependency"

/--
Machine proof debt classification for this Stage1 module.

The current repo-local Lean 4 closure is a statement-shape artifact with checked
equation-normalization and mathlib Weierstrass-curve object-model wrappers.  No
Lean 4 proof of the full nonzero-parameter finiteness theorem has been
integrated.
-/
def machineProofDebt : String := "formalization_debt"

/--
Repo-local integration-debt gate.

The public `lean-forward/class-group-and-mordell-equation` project formalizes
several Mordell-equation instances in Lean 3, not Lean 4 / Lake.  It is therefore
recorded as an integration blocker, not as a completed Lean 4 anchor.
-/
def repoLocalIntegrationDebtGate : String :=
  "completion upgrade blocked: no Lean 4 port found; Lean 3 anchor remains an explicit blocker, not completed evidence"

/--
Public status-surface gate for this Stage1 slot.

README, metadata, and blueprint checkboxes must stay unchecked until the local
Lean validation record and the serial public merge-back both exist.  This data
record is checked locally, but it is not itself a public-doc update.
-/
def publicStatusSurfaceGate : String :=
  "keep README/meta/blueprint unchecked until repo-local validation and public merge-back exist"

/-- Evidence required before any public completion checkbox can be checked. -/
def publicStatusSurfaceCompletionRequirements : List String := [
  "repo-local Lean validation command passes for the relevant checked artifact",
  "public serial merge-back records the validated artifact and exact theorem boundary",
  "the parent Mordell finiteness theorem is not represented as completed from anchor-only evidence",
  "no completed state retains repo_local_integration_debt"
]

/--
Machine-readable child result for the public status surfaces.

`false` means this child deliberately leaves README/meta/blueprint completion
unchecked; the serial integrator may change public surfaces only after the
requirements above are met.
-/
def publicStatusSurfaceCompletionAllowed : Bool := false

/-- Checked Boolean witness for the current public status-surface gate. -/
theorem publicStatusSurfaceCompletionAllowed_eq_false :
    publicStatusSurfaceCompletionAllowed = false :=
  rfl

#check externalLean4PortAuditDate
#check externalLean4PortAuditScope
#check externalLean4PortAuditResult
#check externalLean4PortIntegrationBlocker
#check publicStatusSurfaceGate
#check publicStatusSurfaceCompletionRequirements
#check publicStatusSurfaceCompletionAllowed
#check publicStatusSurfaceCompletionAllowed_eq_false

end S1_M_002
end Stage1
end AwesomeTheorems
