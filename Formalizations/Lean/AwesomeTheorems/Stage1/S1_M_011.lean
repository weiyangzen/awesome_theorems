import Mathlib.NumberTheory.DiophantineApproximation.Basic
import Mathlib.NumberTheory.DiophantineApproximation.ContinuedFractions
import Mathlib.NumberTheory.Transcendental.Liouville.LiouvilleWith
import Mathlib.NumberTheory.Height.Basic
import Mathlib.NumberTheory.Height.MvPolynomial
import Mathlib.NumberTheory.Height.Northcott
import Mathlib.NumberTheory.Height.NumberField
import Mathlib.NumberTheory.Height.Projectivization
import Mathlib.NumberTheory.SiegelsLemma
import Mathlib.NumberTheory.Real.Irrational
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Combinatorics.Additive.Corner.Roth
import Mathlib.RingTheory.Polynomial.Basic

/-!
# S1-M-011 / THM-M-0398: Thue-Siegel-Roth theorem

This Stage1 artifact records a Lean 4 statement-shape boundary for Roth's
theorem on rational approximation of algebraic numbers.  The terminal theorem
is not claimed here: the current repo-local closure only fixes the typed
statement, the approximation inequality, and the audit anchors needed by later
proof or dependency-integration work.
-/

namespace AwesomeTheorems.Stage1.S1_M_011

noncomputable section

open Filter

/--
An explicit predicate for real algebraic numbers, phrased as being a real root
of a nonzero polynomial with integer coefficients.

This avoids committing this Stage1 slot to a particular future algebraic-number
object model while still exposing all fields needed by Roth's theorem.
-/
def AlgebraicReal (α : ℝ) : Prop :=
  ∃ P : Polynomial ℤ, P ≠ 0 ∧ Polynomial.eval₂ (Int.castRingHom ℝ) α P = 0

/-- The source-side object in Roth's theorem: an irrational algebraic real. -/
def IrrationalAlgebraicReal (α : ℝ) : Prop :=
  AlgebraicReal α ∧ Irrational α

/-- Error term for approximating `α` by the rational number `p / q`. -/
def RationalApproximationError (α : ℝ) (p q : ℤ) : ℝ :=
  |α - ((p : ℝ) / (q : ℝ))|

/--
Absolute denominator height used in the normalized Stage1 inequality.

The statement quantifies over nonzero integer denominators, so `|q|` is the
height of the rational approximation after allowing either sign for `q`.
-/
def DenominatorHeight (q : ℤ) : ℝ :=
  |(q : ℝ)|

/--
The Roth lower-bound conclusion for a fixed irrational algebraic real `α`, an
exponent slack `ε`, and a positive constant `C`.

For every nonzero denominator `q`, the rational approximation error is bounded
below by `C / |q|^(2 + ε)`.
-/
def RothLowerBoundFor (α ε C : ℝ) : Prop :=
  0 < ε ∧
    0 < C ∧
      ∀ p q : ℤ,
        q ≠ 0 →
          C / (DenominatorHeight q) ^ ((2 : ℝ) + ε) ≤
            RationalApproximationError α p q

/--
Normalized Stage1 statement shape for the Thue-Siegel-Roth theorem.

Every irrational algebraic real `α` admits, for each `ε > 0`, a positive
constant `C = C(α, ε)` such that all rational approximations `p / q` satisfy
the Roth lower bound with exponent `2 + ε`.
-/
def StatementShape : Prop :=
  ∀ α : ℝ,
    IrrationalAlgebraicReal α →
      ∀ ε : ℝ, 0 < ε → ∃ C : ℝ, RothLowerBoundFor α ε C

/--
Candidate public surfaces for normalizing the Thue-Siegel-Roth statement.

This records the Stage1 statement-shape decision boundary without claiming any
terminal Roth proof.  The current repo-local theorem artifact chooses the
integer-pair lower-bound surface because it avoids premature commitments to a
future rational finite-set API, finite-exception wrapper, or `LiouvilleWith`
bridge.
-/
inductive StatementSurface where
  | rationalSet
  | integerPair
  | finiteException
  | liouvilleWith
  deriving DecidableEq, Repr

/-- The four public statement-normalization surfaces that must stay in scope. -/
def statementSurfaceCandidates : List StatementSurface := [
  StatementSurface.rationalSet,
  StatementSurface.integerPair,
  StatementSurface.finiteException,
  StatementSurface.liouvilleWith
]

/--
Repo-local Stage1 normalization choice for this artifact.

The selected surface is exactly the integer-pair statement `StatementShape`
below: all integer numerators and nonzero integer denominators satisfy a
uniform lower bound.
-/
def chosenStatementSurface : StatementSurface :=
  StatementSurface.integerPair

/-- The selected statement-normalization surface is the integer-pair surface. -/
theorem chosenStatementSurface_eq_integerPair :
    chosenStatementSurface = StatementSurface.integerPair :=
  rfl

/-- The chosen integer-pair surface unfolds to the normalized `StatementShape`. -/
def ChosenIntegerPairSurface : Prop :=
  StatementShape

/-- The chosen surface is definitionally the existing normalized statement. -/
theorem chosenIntegerPairSurface_iff_statementShape :
    ChosenIntegerPairSurface ↔ StatementShape :=
  Iff.rfl

/-- Projection wrapper for the algebraicity half of the normalized input. -/
theorem irrationalAlgebraicReal_algebraic {α : ℝ}
    (h : IrrationalAlgebraicReal α) : AlgebraicReal α :=
  h.1

/-- Projection wrapper for the irrationality half of the normalized input. -/
theorem irrationalAlgebraicReal_irrational {α : ℝ}
    (h : IrrationalAlgebraicReal α) : Irrational α :=
  h.2

/-- Projection wrapper for the exponent-slack positivity in the Roth bound. -/
theorem rothLowerBoundFor_epsilon_pos {α ε C : ℝ}
    (h : RothLowerBoundFor α ε C) : 0 < ε :=
  h.1

/-- Projection wrapper for the positivity of the Roth constant. -/
theorem rothLowerBoundFor_constant_pos {α ε C : ℝ}
    (h : RothLowerBoundFor α ε C) : 0 < C :=
  h.2.1

/-- Projection wrapper for the denominator-uniform approximation inequality. -/
theorem rothLowerBoundFor_bound {α ε C : ℝ}
    (h : RothLowerBoundFor α ε C) :
    ∀ p q : ℤ,
      q ≠ 0 →
        C / (DenominatorHeight q) ^ ((2 : ℝ) + ε) ≤
          RationalApproximationError α p q :=
  h.2.2

/-- The canonical statement unfolds to the explicit normalized quantifier shape. -/
theorem statementShape_unfold :
    StatementShape ↔
      ∀ α : ℝ,
        IrrationalAlgebraicReal α →
          ∀ ε : ℝ, 0 < ε → ∃ C : ℝ, RothLowerBoundFor α ε C :=
  Iff.rfl

/--
Pairs whose rational approximation is better than the normalized Roth
exponent for the fixed constant `C`.

This is a bridge target for the finite-exception formulation.  It is not used
to claim finiteness here.
-/
def BetterThanRothBound (α ε C : ℝ) (p q : ℤ) : Prop :=
  q ≠ 0 ∧
    RationalApproximationError α p q <
      C / (DenominatorHeight q) ^ ((2 : ℝ) + ε)

/-- Finite-exception bridge surface for a fixed `α`, `ε`, and trial constant. -/
def FiniteExceptionSurfaceFor (α ε C : ℝ) : Prop :=
  {pq : ℤ × ℤ | BetterThanRothBound α ε C pq.1 pq.2}.Finite

/--
Canonical normalized integer pair attached to a rational approximant.

The denominator is `Rat.den`, hence positive as a natural number before it is
cast to `ℤ`.  This gives the bridge direction from rational approximants to the
integer-pair surface without adding a separate reduced-pair API.
-/
def NormalizedRatPair (r : ℚ) : ℤ × ℤ :=
  (r.num, (r.den : ℤ))

/-- Error term for approximating `α` by a rational number `r`. -/
def RationalApproximationErrorRat (α : ℝ) (r : ℚ) : ℝ :=
  |α - (r : ℝ)|

/-- Denominator height of a rational approximant in its normalized `Rat` form. -/
def DenominatorHeightRat (r : ℚ) : ℝ :=
  (r.den : ℝ)

/-- Rational-approximant version of the strict "better than Roth" predicate. -/
def BetterThanRothBoundRat (α ε C : ℝ) (r : ℚ) : Prop :=
  RationalApproximationErrorRat α r <
    C / (DenominatorHeightRat r) ^ ((2 : ℝ) + ε)

/-- Finite-exception surface over normalized rational approximants. -/
def FiniteRationalExceptionSurfaceFor (α ε C : ℝ) : Prop :=
  {r : ℚ | BetterThanRothBoundRat α ε C r}.Finite

/-- Projection from the finite-exception bridge predicate to `q ≠ 0`. -/
theorem betterThanRothBound_denominator_ne {α ε C : ℝ} {p q : ℤ}
    (h : BetterThanRothBound α ε C p q) : q ≠ 0 :=
  h.1

/-- Projection from the finite-exception bridge predicate to the strict error bound. -/
theorem betterThanRothBound_error_lt {α ε C : ℝ} {p q : ℤ}
    (h : BetterThanRothBound α ε C p q) :
    RationalApproximationError α p q <
      C / (DenominatorHeight q) ^ ((2 : ℝ) + ε) :=
  h.2

/-- The normalized rational-to-pair map is injective. -/
theorem normalizedRatPair_injective : Function.Injective NormalizedRatPair := by
  intro r s h
  apply Rat.ext
  · exact congrArg Prod.fst h
  · have hden : ((r.den : ℤ) = (s.den : ℤ)) := by
      simpa [NormalizedRatPair] using congrArg Prod.snd h
    exact_mod_cast hden

/-- The integer denominator extracted from a normalized rational is nonzero. -/
theorem normalizedRatPair_denominator_ne (r : ℚ) :
    (NormalizedRatPair r).2 ≠ 0 := by
  dsimp [NormalizedRatPair]
  exact_mod_cast Rat.den_nz r

/-- The integer denominator height is always nonnegative. -/
theorem denominatorHeight_nonneg (q : ℤ) : 0 ≤ DenominatorHeight q := by
  dsimp [DenominatorHeight]
  positivity

/-- The integer denominator height is positive for nonzero denominators. -/
theorem denominatorHeight_pos {q : ℤ} (hq : q ≠ 0) :
    0 < DenominatorHeight q := by
  dsimp [DenominatorHeight]
  exact abs_pos.mpr (by exact_mod_cast hq)

/-- Nonzero integer denominators have height at least one. -/
theorem one_le_denominatorHeight {q : ℤ} (hq : q ≠ 0) :
    1 ≤ DenominatorHeight q := by
  have hnat : 1 ≤ q.natAbs := Nat.succ_le_iff.mpr (Int.natAbs_pos.mpr hq)
  have hreal : (1 : ℝ) ≤ (q.natAbs : ℝ) := by
    exact_mod_cast hnat
  simpa [DenominatorHeight, Nat.cast_natAbs (α := ℝ) q] using hreal

/-- Rational denominator height is positive in canonical `Rat` form. -/
theorem denominatorHeightRat_pos (r : ℚ) :
    0 < DenominatorHeightRat r := by
  dsimp [DenominatorHeightRat]
  exact_mod_cast r.den_pos

/-- Rational denominator height is nonzero in canonical `Rat` form. -/
theorem denominatorHeightRat_ne_zero (r : ℚ) :
    DenominatorHeightRat r ≠ 0 :=
  (denominatorHeightRat_pos r).ne'

/-- Rational denominator height is at least one in canonical `Rat` form. -/
theorem one_le_denominatorHeightRat (r : ℚ) :
    1 ≤ DenominatorHeightRat r := by
  dsimp [DenominatorHeightRat]
  exact_mod_cast r.den_pos

/-- Rational denominator height agrees with the integer-pair denominator height. -/
theorem denominatorHeightRat_eq_pair (r : ℚ) :
    DenominatorHeightRat r = DenominatorHeight (NormalizedRatPair r).2 := by
  dsimp [DenominatorHeightRat, DenominatorHeight, NormalizedRatPair]
  have hnonneg : 0 ≤ (((r.den : ℤ) : ℝ)) := by
    exact_mod_cast Nat.zero_le r.den
  rw [abs_of_nonneg hnonneg]
  simp

/--
The canonical numerator and denominator of a rational approximant are coprime
after taking the integer absolute value of the denominator component.
-/
theorem normalizedRatPair_coprime_natAbs_den (r : ℚ) :
    (NormalizedRatPair r).1.natAbs.Coprime (NormalizedRatPair r).2.natAbs := by
  dsimp [NormalizedRatPair]
  simpa using r.reduced

/-- The normalized pair represents the original rational number over `ℚ`. -/
theorem normalizedRatPair_rational_value (r : ℚ) :
    ((NormalizedRatPair r).1 : ℚ) / ((NormalizedRatPair r).2 : ℚ) = r := by
  simpa [NormalizedRatPair] using r.num_div_den

/-- Rational approximation error agrees with the error of the normalized pair. -/
theorem rationalApproximationErrorRat_eq_pair (α : ℝ) (r : ℚ) :
    RationalApproximationErrorRat α r =
      RationalApproximationError α (NormalizedRatPair r).1 (NormalizedRatPair r).2 := by
  dsimp [RationalApproximationErrorRat, RationalApproximationError, NormalizedRatPair]
  rw [Rat.cast_def]
  simp

/--
A rational approximant that beats the rational surface also beats the
integer-pair surface after normalization.
-/
theorem betterThanRothBound_of_rat {α ε C : ℝ} {r : ℚ}
    (h : BetterThanRothBoundRat α ε C r) :
    BetterThanRothBound α ε C (NormalizedRatPair r).1 (NormalizedRatPair r).2 := by
  constructor
  · exact normalizedRatPair_denominator_ne r
  · simpa [BetterThanRothBoundRat, rationalApproximationErrorRat_eq_pair,
      denominatorHeightRat_eq_pair] using h

/--
Finite bad normalized integer pairs imply finite bad rational approximants.

This is the checked repo-local bridge for `S1-M-011-A04-rat-pair-bridge`.
It does not prove the finite-exception Roth theorem itself.
-/
theorem finiteRationalExceptionSurfaceFor_of_finiteExceptionSurfaceFor {α ε C : ℝ}
    (h : FiniteExceptionSurfaceFor α ε C) :
    FiniteRationalExceptionSurfaceFor α ε C := by
  unfold FiniteRationalExceptionSurfaceFor
  refine (h.preimage normalizedRatPair_injective.injOn).subset ?_
  intro r hr
  exact betterThanRothBound_of_rat hr

/--
A checked bridge from a uniform Roth lower bound at exponent `2 + ε` to the
negation of mathlib's `LiouvilleWith` predicate at any strictly larger
exponent.

This is the local core of `S1-M-011-A05-liouvillewith-bridge`: it does not
prove Roth's theorem, but it verifies the exponent and denominator conversion
needed once a Roth lower-bound or finite-exception package supplies the local
bound.
-/
theorem not_liouvilleWith_of_rothLowerBoundFor {α P ε C : ℝ}
    (hR : RothLowerBoundFor α ε C) (hP : (2 : ℝ) + ε < P) :
    ¬ LiouvilleWith P α := by
  intro hL
  let β : ℝ := (((2 : ℝ) + ε) + P) / 2
  have hbaseβ : (2 : ℝ) + ε < β := by
    dsimp [β]
    linarith
  have hβP : β < P := by
    dsimp [β]
    linarith
  have hfreq := hL.frequently_lt_rpow_neg hβP
  have hCpos : 0 < C := rothLowerBoundFor_constant_pos hR
  have heventually : ∀ᶠ n : ℕ in atTop,
      1 ≤ n ∧ (n : ℝ) ^ (-β) < C / (n : ℝ) ^ ((2 : ℝ) + ε) := by
    have hpow : ∀ᶠ n : ℕ in atTop,
        C⁻¹ < (n : ℝ) ^ (β - ((2 : ℝ) + ε)) := by
      simpa only [(· ∘ ·)] using
        ((tendsto_rpow_atTop (sub_pos.2 hbaseβ)).comp
            tendsto_natCast_atTop_atTop).eventually
          (eventually_gt_atTop C⁻¹)
    refine ((eventually_ge_atTop 1).and hpow).mono ?_
    intro n hn
    rcases hn with ⟨hn_ge, hn_pow⟩
    have hnpos_nat : 0 < n := Nat.succ_le_iff.mp hn_ge
    have hnpos : (0 : ℝ) < n := by
      exact_mod_cast hnpos_nat
    have hmul : 1 < C * (n : ℝ) ^ (β - ((2 : ℝ) + ε)) := by
      rw [inv_lt_iff_one_lt_mul₀ hCpos] at hn_pow
      simpa [mul_comm] using hn_pow
    have hdenpos : 0 < (n : ℝ) ^ ((2 : ℝ) + ε) :=
      Real.rpow_pos_of_pos hnpos _
    have hnpowpos : 0 < (n : ℝ) ^ β :=
      Real.rpow_pos_of_pos hnpos _
    constructor
    · exact hn_ge
    · calc
        (n : ℝ) ^ (-β) = 1 / (n : ℝ) ^ β := by
          rw [Real.rpow_neg hnpos.le, one_div]
        _ < (C * (n : ℝ) ^ (β - ((2 : ℝ) + ε))) / (n : ℝ) ^ β := by
          exact div_lt_div_of_pos_right hmul hnpowpos
        _ = C / (n : ℝ) ^ ((2 : ℝ) + ε) := by
          rw [div_eq_div_iff hnpowpos.ne' hdenpos.ne']
          rw [mul_assoc, ← Real.rpow_add hnpos, sub_add_cancel]
  exact (heventually.and_frequently hfreq).exists.elim fun n hn => by
    rcases hn with ⟨⟨hn_ge, hn_lt_bound⟩, m, _hne, hm_lt⟩
    have hnpos_nat : 0 < n := Nat.succ_le_iff.mp hn_ge
    have hnz : (n : ℤ) ≠ 0 := by
      exact_mod_cast hnpos_nat.ne'
    have hpair := rothLowerBoundFor_bound hR m (n : ℤ) hnz
    have hheight : DenominatorHeight (n : ℤ) = (n : ℝ) := by
      dsimp [DenominatorHeight]
      have hnonneg : (0 : ℝ) ≤ (n : ℤ) := by
        exact_mod_cast Nat.zero_le n
      rw [abs_of_nonneg hnonneg]
      simp
    have herror :
        RationalApproximationError α m (n : ℤ) = |α - (m : ℝ) / (n : ℝ)| := by
      dsimp [RationalApproximationError]
      norm_num
    have hpair' :
        C / (n : ℝ) ^ ((2 : ℝ) + ε) ≤ |α - (m : ℝ) / (n : ℝ)| := by
      simpa [hheight, herror] using hpair
    linarith

/--
If the normalized Roth `StatementShape` is later proved or imported, it
immediately yields the public `LiouvilleWith` corollary for every exponent
strictly above `2`.
-/
theorem not_liouvilleWith_of_statementShape
    (hS : StatementShape) {α P : ℝ}
    (hα : IrrationalAlgebraicReal α) (hP : (2 : ℝ) < P) :
    ¬ LiouvilleWith P α := by
  let ε : ℝ := (P - 2) / 2
  have hε : 0 < ε := by
    dsimp [ε]
    linarith
  rcases hS α hα ε hε with ⟨C, hR⟩
  exact not_liouvilleWith_of_rothLowerBoundFor hR (by
    dsimp [ε]
    linarith)

/--
Approximation-theory proof packages that a future formal Roth proof must close.

The constructors are proof-planning nodes, not theorem claims.  They make the
package split explicit inside the checked artifact so public backfill can refer
to stable names.
-/
inductive ApproximationTheoryPackage where
  | algebraicInputAndHeight
  | rationalApproximationNormalization
  | liouvilleBaseline
  | siegelLemmaAuxiliaryPolynomial
  | zeroMultiplicityEstimate
  | gapPrinciple
  | finiteExceptionExtraction
  | publicSurfaceBridge
  deriving DecidableEq, Repr

/-- Canonical package order for the Thue-Siegel-Roth approximation split. -/
def approximationTheoryPackageSplit : List ApproximationTheoryPackage := [
  ApproximationTheoryPackage.algebraicInputAndHeight,
  ApproximationTheoryPackage.rationalApproximationNormalization,
  ApproximationTheoryPackage.liouvilleBaseline,
  ApproximationTheoryPackage.siegelLemmaAuxiliaryPolynomial,
  ApproximationTheoryPackage.zeroMultiplicityEstimate,
  ApproximationTheoryPackage.gapPrinciple,
  ApproximationTheoryPackage.finiteExceptionExtraction,
  ApproximationTheoryPackage.publicSurfaceBridge
]

/-- The approximation-theory split currently has eight named packages. -/
theorem approximationTheoryPackageSplit_length :
    approximationTheoryPackageSplit.length = 8 :=
  rfl

/--
Leaf split for the auxiliary-polynomial package around
`Mathlib.NumberTheory.SiegelsLemma`.

The first three leaves are checked mathlib/input-output anchors for the
integer-matrix Siegel lemma.  The remaining leaves are the unclosed Roth-specific
work needed to turn a small integer kernel vector into a useful auxiliary
polynomial with height and vanishing-order control.
-/
inductive SiegelLemmaAuxiliaryPolynomialLeaf where
  | integerMatrixKernelStatement
  | underdeterminedRankInput
  | smallNonzeroVectorOutput
  | monomialIndexingAndCoefficientMatrix
  | coefficientHeightTransfer
  | auxiliaryPolynomialNonzero
  | vanishingJetConstraints
  | evaluationHeightBound
  deriving DecidableEq, Repr

/-- Canonical leaf order for `S1-M-011-A07-siegel-lemma-package`. -/
def siegelLemmaAuxiliaryPolynomialLeaves :
    List SiegelLemmaAuxiliaryPolynomialLeaf := [
  SiegelLemmaAuxiliaryPolynomialLeaf.integerMatrixKernelStatement,
  SiegelLemmaAuxiliaryPolynomialLeaf.underdeterminedRankInput,
  SiegelLemmaAuxiliaryPolynomialLeaf.smallNonzeroVectorOutput,
  SiegelLemmaAuxiliaryPolynomialLeaf.monomialIndexingAndCoefficientMatrix,
  SiegelLemmaAuxiliaryPolynomialLeaf.coefficientHeightTransfer,
  SiegelLemmaAuxiliaryPolynomialLeaf.auxiliaryPolynomialNonzero,
  SiegelLemmaAuxiliaryPolynomialLeaf.vanishingJetConstraints,
  SiegelLemmaAuxiliaryPolynomialLeaf.evaluationHeightBound
]

/-- The auxiliary-polynomial package split currently has eight named leaves. -/
theorem siegelLemmaAuxiliaryPolynomialLeaves_length :
    siegelLemmaAuxiliaryPolynomialLeaves.length = 8 :=
  rfl

/-- The checked mathlib Siegel-lemma anchors available to this artifact. -/
def siegelLemmaCheckedAnchors : List String := [
  "Int.Matrix.exists_ne_zero_int_vec_norm_le: underdetermined integer matrix -> nonzero integer kernel vector with sup-norm bound using max 1 ||A||",
  "Int.Matrix.exists_ne_zero_int_vec_norm_le': nonzero underdetermined integer matrix -> nonzero integer kernel vector with sup-norm bound using ||A||",
  "Int.Matrix.one_le_norm_A_of_ne_zero: nonzero integer matrix has sup norm at least one"
]

/--
Checked input obligations of the mathlib Siegel-lemma theorem family that a
future Roth auxiliary-polynomial construction must supply.
-/
def siegelLemmaInputObligations : List String := [
  "choose finite row and column index types alpha beta for the linear system",
  "construct an integer matrix A : Matrix alpha beta Int encoding vanishing or jet constraints",
  "prove Fintype.card alpha < Fintype.card beta for the chosen degree/multiplicity parameters",
  "prove 0 < Fintype.card alpha",
  "for the sharpened bound, prove A != 0"
]

/--
Checked output facts available after applying mathlib's Siegel lemma.

These are package interfaces, not a claim that the Roth auxiliary polynomial has
already been constructed in this repository.
-/
def siegelLemmaOutputInterface : List String := [
  "a coefficient vector t : beta -> Int",
  "t != 0",
  "A *ᵥ t = 0, giving the encoded homogeneous linear constraints",
  "||t|| <= (card beta * max 1 ||A||) ^ (card alpha / (card beta - card alpha))",
  "under A != 0, ||t|| <= (card beta * ||A||) ^ (card alpha / (card beta - card alpha))"
]

/-- Roth-specific blockers beyond the checked integer-matrix Siegel lemma. -/
def siegelLemmaAuxiliaryPolynomialBlockers : List String := [
  "no checked monomial-index equivalence beta -> polynomial coefficients is present in this artifact",
  "no checked construction maps the kernel vector t to a nonzero univariate or multivariate auxiliary polynomial",
  "no checked proof transfers A *ᵥ t = 0 into the required vanishing or high-multiplicity conditions",
  "no checked height estimate bounds the resulting auxiliary-polynomial coefficients in the selected algebraic-height model",
  "no checked parameter ledger proves the row/column inequality and final exponent budget for the Roth proof",
  "therefore NumberTheory.SiegelsLemma is a checked package anchor, not completion evidence for StatementShape"
]

/-- Machine-checkable status labels for the Siegel-lemma auxiliary package. -/
def siegelLemmaAuxiliaryPolynomialStatus : List String := [
  "checked_anchor: Mathlib.NumberTheory.SiegelsLemma imports and the core Int.Matrix theorem names are available",
  "checked_interface: the package input obligations and output facts are named in this repo-local artifact",
  "formalization_debt: the Roth-specific auxiliary-polynomial construction, height transfer, and vanishing translation are not proved here",
  "not_repo_local_closed: no terminal Thue-Siegel-Roth theorem or auxiliary-polynomial theorem is claimed"
]

/--
Audited denominator-height leaves for `S1-M-011-A06`.

The checked leaves cover the canonical rational denominator and integer-pair
height conversions available in this repo-local artifact.  The remaining
algebraic-number height comparisons are deliberately kept as audit blockers,
because no terminal Roth proof or algebraic-height object model is closed here.
-/
inductive DenominatorHeightAuditLeaf where
  | integerHeightNonzero
  | rationalCanonicalDenominatorPositive
  | rationalPairHeightAgreement
  | rationalPairReduced
  | rationalPairValue
  | algebraicHeightObjectModel
  deriving DecidableEq, Repr

/-- Canonical leaf order for the denominator-height bridge audit. -/
def denominatorHeightAuditLeaves : List DenominatorHeightAuditLeaf := [
  DenominatorHeightAuditLeaf.integerHeightNonzero,
  DenominatorHeightAuditLeaf.rationalCanonicalDenominatorPositive,
  DenominatorHeightAuditLeaf.rationalPairHeightAgreement,
  DenominatorHeightAuditLeaf.rationalPairReduced,
  DenominatorHeightAuditLeaf.rationalPairValue,
  DenominatorHeightAuditLeaf.algebraicHeightObjectModel
]

/-- The denominator-height audit currently has six named leaves. -/
theorem denominatorHeightAuditLeaves_length :
    denominatorHeightAuditLeaves.length = 6 :=
  rfl

/-- Checked repo-local denominator-height anchors for reduced rationals. -/
def denominatorHeightCheckedAnchors : List String := [
  "denominatorHeight_nonneg: 0 <= DenominatorHeight q",
  "denominatorHeight_pos: q != 0 -> 0 < DenominatorHeight q",
  "one_le_denominatorHeight: q != 0 -> 1 <= DenominatorHeight q",
  "denominatorHeightRat_pos: 0 < DenominatorHeightRat r",
  "denominatorHeightRat_ne_zero: DenominatorHeightRat r != 0",
  "one_le_denominatorHeightRat: 1 <= DenominatorHeightRat r",
  "denominatorHeightRat_eq_pair: DenominatorHeightRat r = DenominatorHeight (NormalizedRatPair r).2",
  "normalizedRatPair_coprime_natAbs_den: canonical numerator and denominator are coprime",
  "normalizedRatPair_rational_value: the canonical pair represents r over Rat"
]

/-- mathlib height APIs audited but not converted into a Roth height proof here. -/
def algebraicHeightAuditAnchors : List String := [
  "Height.mulHeight₁ / Height.logHeight₁: field-element height APIs over fields with Height.AdmissibleAbsValues",
  "Height.mulHeight / Height.logHeight: projective tuple height APIs over finite index types",
  "Height.one_le_mulHeight₁ / Height.mulHeight₁_pos / Height.zero_le_logHeight₁: basic positivity anchors",
  "Height.one_le_mulHeight / Height.mulHeight_pos / Height.logHeight_nonneg: projective positivity anchors",
  "Height.mulHeight_smul_eq_mulHeight: projective scaling invariance anchor",
  "Height.mulHeight_eval_le and Height.mulHeight_eval_ge families: homogeneous polynomial height estimate anchors",
  "Height.NumberField and Height.Projectivization imports: audited modules for future algebraic-number height integration"
]

/-- Concrete blockers before denominator-height work can support a terminal Roth proof. -/
def heightBridgeIntegrationBlockers : List String := [
  "no checked theorem in this artifact identifies DenominatorHeightRat r with a mathlib Height.mulHeight or Height.mulHeight₁ expression",
  "the current AlgebraicReal predicate is an integer-polynomial-root statement, not a bundled algebraic-number object with a selected number-field height",
  "future Roth packages must choose whether rational approximants are measured by DenominatorHeightRat, projective Height.mulHeight ![num, den], or a number-field height specialization",
  "algebraic-number height estimates needed by auxiliary-polynomial and zero-estimate packages remain formalization_debt, not repo-local completion evidence"
]

/--
Leaf split for `S1-M-011-A08-zero-estimate-package`.

These leaves isolate the zero-estimate and product-formula dependencies that a
future formal Roth proof must close after the auxiliary polynomial has been
constructed.  The list is a checked package ledger, not a proof of the zero
estimate.
-/
inductive ZeroEstimateProductFormulaLeaf where
  | auxiliaryPolynomialNonzeroInput
  | multiplicityAndJetModel
  | archimedeanLocalUpperBounds
  | nonarchimedeanLocalUpperBounds
  | productFormulaNormalization
  | heightEvaluationLowerBound
  | denominatorExponentLedger
  | nonzeroEvaluationWitness
  deriving DecidableEq, Repr

/-- Canonical leaf order for the zero-estimate/product-formula package. -/
def zeroEstimateProductFormulaLeaves :
    List ZeroEstimateProductFormulaLeaf := [
  ZeroEstimateProductFormulaLeaf.auxiliaryPolynomialNonzeroInput,
  ZeroEstimateProductFormulaLeaf.multiplicityAndJetModel,
  ZeroEstimateProductFormulaLeaf.archimedeanLocalUpperBounds,
  ZeroEstimateProductFormulaLeaf.nonarchimedeanLocalUpperBounds,
  ZeroEstimateProductFormulaLeaf.productFormulaNormalization,
  ZeroEstimateProductFormulaLeaf.heightEvaluationLowerBound,
  ZeroEstimateProductFormulaLeaf.denominatorExponentLedger,
  ZeroEstimateProductFormulaLeaf.nonzeroEvaluationWitness
]

/-- The zero-estimate/product-formula package split currently has eight leaves. -/
theorem zeroEstimateProductFormulaLeaves_length :
    zeroEstimateProductFormulaLeaves.length = 8 :=
  rfl

/-- mathlib anchors available for the zero-estimate/product-formula audit. -/
def zeroEstimateProductFormulaCheckedAnchors : List String := [
  "Height.AdmissibleAbsValues.product_formula: abstract product-formula field-class axiom used by mathlib heights",
  "NumberField.prod_abs_eq_one: number-field product formula over infinite and finite places",
  "NumberField.FinitePlace.prod_eq_inv_abs_norm: finite-place product equals inverse norm factor",
  "Height.mulHeight_eval_le / Height.logHeight_eval_le: upper height estimates for homogeneous polynomial evaluation",
  "Height.mulHeight_eval_ge / Height.logHeight_eval_ge: lower height estimates from auxiliary homogeneous systems",
  "Height.NumberField imports ProductFormula and provides number-field admissible absolute values"
]

/--
Missing APIs before the zero-estimate package can support a terminal Roth proof.

These are concrete formalization blockers, not repo-local integration debt:
the current repository has no external Lean Roth proof pinned as completion
evidence for this package.
-/
def zeroEstimateProductFormulaMissingAPIs : List String := [
  "a bundled Roth auxiliary-polynomial object with coefficients, degree bounds, and a proved nonzero evaluation target",
  "a multiplicity or jet API connecting encoded vanishing constraints to order-of-vanishing statements at algebraic approximation tuples",
  "local archimedean estimates converting small approximation errors into bounds for all relevant derivatives/evaluations",
  "local nonarchimedean estimates controlling denominators and integrality factors at finite places",
  "a bridge from the selected local absolute values to Height.AdmissibleAbsValues.product_formula or NumberField.prod_abs_eq_one",
  "a lower-bound theorem for a nonzero algebraic evaluation in the chosen height model",
  "an exponent ledger showing the product-formula lower bound contradicts the assumed better-than-Roth approximation rate",
  "a proof that the selected evaluation is nonzero after the zero-estimate/multiplicity argument"
]

/-- Machine-checkable status labels for the A08 zero-estimate package. -/
def zeroEstimateProductFormulaStatus : List String := [
  "checked_anchor: product-formula and height-evaluation theorem names are available through current imports",
  "checked_package_split: eight leaves name the zero-estimate/product-formula proof obligations",
  "formalization_debt: no zero-estimate proof body, local absolute-value bound, or exponent contradiction is present",
  "not_repo_local_closed: this package does not prove StatementShape or any terminal Thue-Siegel-Roth theorem"
]

/--
Leaf split for `S1-M-011-A09-gap-principle-package`.

These leaves separate the denominator-growth argument from the final finite-set
assembly.  The checked lemmas below close only the elementary bounded-box
assembly: if a future gap principle supplies explicit numerator and denominator
`natAbs` bounds for all bad pairs, the bad-pair surface is finite.
-/
inductive GapPrincipleFinitenessLeaf where
  | badApproximantOrdering
  | denominatorUnboundedness
  | consecutiveDenominatorGap
  | supergrowthIteration
  | exponentBudgetContradiction
  | denominatorBoundExtraction
  | numeratorBoundExtraction
  | boundedBoxFiniteness
  deriving DecidableEq, Repr

/-- Canonical leaf order for the gap-principle and finiteness-assembly package. -/
def gapPrincipleFinitenessLeaves : List GapPrincipleFinitenessLeaf := [
  GapPrincipleFinitenessLeaf.badApproximantOrdering,
  GapPrincipleFinitenessLeaf.denominatorUnboundedness,
  GapPrincipleFinitenessLeaf.consecutiveDenominatorGap,
  GapPrincipleFinitenessLeaf.supergrowthIteration,
  GapPrincipleFinitenessLeaf.exponentBudgetContradiction,
  GapPrincipleFinitenessLeaf.denominatorBoundExtraction,
  GapPrincipleFinitenessLeaf.numeratorBoundExtraction,
  GapPrincipleFinitenessLeaf.boundedBoxFiniteness
]

/-- The A09 gap-principle package split currently has eight leaves. -/
theorem gapPrincipleFinitenessLeaves_length :
    gapPrincipleFinitenessLeaves.length = 8 :=
  rfl

/-- Explicit numerator/denominator `natAbs` bounds for all bad integer pairs. -/
def BadPairNatAbsBounds (α ε C : ℝ) (M N : ℕ) : Prop :=
  ∀ ⦃p q : ℤ⦄,
    BetterThanRothBound α ε C p q →
      p.natAbs ≤ M ∧ q.natAbs ≤ N

/-- The set of integers with bounded `natAbs` is finite. -/
theorem finite_int_natAbs_le (N : ℕ) :
    ({z : ℤ | z.natAbs ≤ N} : Set ℤ).Finite := by
  refine (Set.finite_Icc (-(N : ℤ)) (N : ℤ)).subset ?_
  intro z hz
  have hcast : (z.natAbs : ℤ) ≤ (N : ℤ) := by
    exact_mod_cast hz
  constructor
  · have hneg : -z ≤ (z.natAbs : ℤ) := by
      simpa [Int.natCast_natAbs] using neg_le_abs z
    linarith
  · have hle : z ≤ (z.natAbs : ℤ) := by
      simpa [Int.natCast_natAbs] using le_abs_self z
    linarith

/-- Integer pairs in a fixed numerator/denominator `natAbs` box form a finite set. -/
theorem finite_pair_natAbs_le (M N : ℕ) :
    ({pq : ℤ × ℤ | pq.1.natAbs ≤ M ∧ pq.2.natAbs ≤ N} : Set (ℤ × ℤ)).Finite := by
  let s : Set ℤ := {p : ℤ | p.natAbs ≤ M}
  let t : Set ℤ := {q : ℤ | q.natAbs ≤ N}
  have hs : s.Finite := finite_int_natAbs_le M
  have ht : t.Finite := finite_int_natAbs_le N
  simpa [s, t, Set.prod] using hs.prod ht

/--
Bounded numerator and denominator ranges assemble the finite-exception surface.

This is a checked local A09 endpoint, but its input bounds are still future
gap-principle output obligations rather than proved Roth estimates.
-/
theorem finiteExceptionSurfaceFor_of_badPairNatAbsBounds {α ε C : ℝ} {M N : ℕ}
    (h : BadPairNatAbsBounds α ε C M N) :
    FiniteExceptionSurfaceFor α ε C := by
  unfold FiniteExceptionSurfaceFor
  exact (finite_pair_natAbs_le M N).subset fun pq hpq => h hpq

/-- The same bounded-box assembly transported to normalized rational approximants. -/
theorem finiteRationalExceptionSurfaceFor_of_badPairNatAbsBounds {α ε C : ℝ} {M N : ℕ}
    (h : BadPairNatAbsBounds α ε C M N) :
    FiniteRationalExceptionSurfaceFor α ε C :=
  finiteRationalExceptionSurfaceFor_of_finiteExceptionSurfaceFor
    (finiteExceptionSurfaceFor_of_badPairNatAbsBounds h)

/-- Checked repo-local anchors for the A09 bounded-box finiteness endpoint. -/
def gapPrincipleFinitenessCheckedAnchors : List String := [
  "GapPrincipleFinitenessLeaf / gapPrincipleFinitenessLeaves: checked eight-leaf split for denominator growth and finiteness assembly",
  "BadPairNatAbsBounds: explicit numerator and denominator natAbs bounds for every bad integer pair",
  "finite_int_natAbs_le: integers with z.natAbs <= N form a finite set",
  "finite_pair_natAbs_le: integer pairs in a fixed numerator/denominator natAbs box form a finite set",
  "finiteExceptionSurfaceFor_of_badPairNatAbsBounds: bounded bad-pair boxes imply FiniteExceptionSurfaceFor",
  "finiteRationalExceptionSurfaceFor_of_badPairNatAbsBounds: bounded bad-pair boxes imply the normalized rational finite-exception surface"
]

/-- Missing proof APIs before the A09 package can support a terminal Roth proof. -/
def gapPrincipleFinitenessMissingAPIs : List String := [
  "a checked construction that orders an assumed infinite family of too-good approximants by strictly increasing denominator height",
  "a proof that denominators tend to infinity for an infinite bad-approximant family after quotienting duplicate rational values",
  "the Roth gap inequality relating consecutive denominator heights from the auxiliary-polynomial and zero-estimate packages",
  "an iteration theorem showing the gap inequality forces supergrowth incompatible with the earlier exponent ledger",
  "a bound-extraction theorem turning the contradiction into a concrete denominator natAbs bound N",
  "a numerator-bound theorem deriving p.natAbs <= M from q.natAbs <= N and the selected approximation-error inequality",
  "a bridge from the finite rational-exception surface to a positive uniform Roth constant when the public statement is phrased as RothLowerBoundFor"
]

/-- Machine-checkable status labels for the A09 gap-principle package. -/
def gapPrincipleFinitenessStatus : List String := [
  "checked_package_split: eight leaves name the denominator-growth and finite-assembly obligations",
  "checked_endpoint: explicit numerator/denominator natAbs bounds imply finite integer-pair and rational-exception surfaces",
  "formalization_debt: the gap principle itself, denominator supergrowth contradiction, and bound extraction are not proved here",
  "not_repo_local_closed: this package does not prove StatementShape or any terminal Thue-Siegel-Roth theorem"
]

/-- Machine-checkable status labels for the current approximation packages. -/
def approximationTheoryPackageStatus : List String := [
  "algebraicInputAndHeight: denominator positivity/reduced-rational leaves checked; algebraic-number height object model remains open",
  "rationalApproximationNormalization: checked rational-to-normalized-integer-pair bridge via NormalizedRatPair, including denominator-height agreement",
  "liouvilleBaseline: checked conditional bridge from RothLowerBoundFor/StatementShape to Not (LiouvilleWith P alpha) for P > 2",
  "siegelLemmaAuxiliaryPolynomial: checked mathlib Siegel-lemma anchors and input/output interface split; Roth-specific polynomial construction remains formalization_debt",
  "zeroMultiplicityEstimate: checked A08 package split and product-formula anchors; no local zero-estimate proof body",
  "gapPrinciple: checked A09 package split and bounded-box finiteness endpoint; no local denominator-growth proof body",
  "finiteExceptionExtraction: FiniteExceptionSurfaceFor transports to FiniteRationalExceptionSurfaceFor; bounded bad-pair boxes give both finite surfaces",
  "publicSurfaceBridge: bridge target only; public docs require serial integrator backfill"
]

/--
The terminal proof obligation remains the normalized `StatementShape`.

Keeping this as a definition records formalization debt without adding a proof
placeholder or new kernel assumption.
-/
def ThueSiegelRothFormalizationDebt : Prop :=
  StatementShape

/-- Repo-local integration-debt gate for the current child scope. -/
def repoLocalIntegrationDebtGate : List String := [
  "no terminal Thue-Siegel-Roth proof is claimed by this artifact",
  "pinned mathlib search found Diophantine-approximation and Liouville anchors, not a terminal Roth theorem",
  "no external Lean 4 Roth proof has been pinned, imported, or checked by this repository in this child",
  "current completed scope is package-split metadata plus statement bridges only; terminal status is not_repo_local_closed"
]

/-- A11 integration-gate state for a possible external Lean 4 proof. -/
inductive IntegrationGateState where
  | noTerminalExternalProofFound
  | terminalExternalProofRequiresPinImportCheck
  | terminalExternalProofBlocked
  | terminalExternalProofPinnedChecked
  deriving DecidableEq, Repr

/--
Repo-local integration-gate row for `S1-M-011-A11`.

This is gate metadata only: no row may be used as completion evidence unless
`state = terminalExternalProofPinnedChecked` and the cited validation command
has passed in this repository.
-/
structure ExternalIntegrationGateRow where
  candidate : String
  state : IntegrationGateState
  requiredAction : String
  completionGate : String

/-- Checked A11 integration-gate rows for the current child scope. -/
def s1m011A11IntegrationGateRows : List ExternalIntegrationGateRow := [
  {
    candidate := "pinned local mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95"
    state := IntegrationGateState.noTerminalExternalProofFound
    requiredAction := "do not promote completion from LiouvilleWith, Height, SiegelLemma, or additive-combinatorics Roth support anchors"
    completionGate := "not_repo_local_closed; no terminal theorem was found in the pinned local dependency"
  },
  {
    candidate := "upstream mathlib master 49f10344339f99fda2d3bb0aa1455bfa6801fd93 recorded for follow-up"
    state := IntegrationGateState.terminalExternalProofRequiresPinImportCheck
    requiredAction := "before any completion claim, a serial integrator must pin/import/check an upstream terminal theorem or record the concrete incompatibility"
    completionGate := "anchor-only revision recording is not external_upstream_pinned"
  },
  {
    candidate := "future external Lean 4 Thue-Siegel-Roth or number-theoretic Roth project"
    state := IntegrationGateState.terminalExternalProofRequiresPinImportCheck
    requiredAction := "record URL, commit, Lean/Lake versions, module, theorem name, license, and run a repo-local import or wrapper validation"
    completionGate := "if validation fails, keep the public item open with an explicit repo_local_integration_debt blocker"
  }
]

/-- The A11 integration gate currently records exactly three candidate rows. -/
theorem s1m011A11IntegrationGateRows_length :
    s1m011A11IntegrationGateRows.length = 3 :=
  rfl

/-- Machine-checkable status labels for the A11 integration gate. -/
def s1m011A11IntegrationGateStatus : List String := [
  "A11 is an integration gate, not a terminal proof of StatementShape",
  "no external Lean 4 terminal Thue-Siegel-Roth proof is currently pinned/imported/checked in this repository",
  "no completed state retains repo_local_integration_debt because no anchor-only external proof is used as completion evidence",
  "any future terminal external proof must become external_upstream_pinned or local_wrapper_upstream_* through repo-local validation, or remain an explicit blocker"
]

/-- Public surfaces that A12 may synchronize only through a serial integrator. -/
inductive PublicSyncSurface where
  | stage1Blueprint
  | stage1Todo
  | repositoryReadmeOrMeta
  | theoremResearchCatalog
  deriving DecidableEq, Repr

/--
Serial public-sync row for `S1-M-011-A12`.

These rows are integration instructions, not proof evidence. They record the
public surfaces that must be kept consistent after the checked Lean artifact
and private child ledgers are reviewed by an integrator.
-/
structure PublicSyncTargetRow where
  surface : PublicSyncSurface
  targetPath : String
  requiredUpdate : String
  completionBoundary : String

/-- Checked A12 public-sync targets for the current Stage1 artifact. -/
def s1m011A12PublicSyncTargets : List PublicSyncTargetRow := [
  {
    surface := PublicSyncSurface.stage1Blueprint
    targetPath := "Docs/Stage1_Blueprint.md"
    requiredUpdate := "replace the generic S1-M-011 backfill checklist with the validated Lean artifact summary, including A04-A11 child ledger anchors and this A12 public-sync ledger"
    completionBoundary := "keep Stage1 status open/not completed; the artifact validates statement bridges and package ledgers, not StatementShape"
  },
  {
    surface := PublicSyncSurface.stage1Todo
    targetPath := "Docs/todos_20260430.md"
    requiredUpdate := "mirror the same checked/non-completion boundary as the Stage1 blueprint and avoid marking A12 done before the serial public patch is merged"
    completionBoundary := "todo checkboxes are public merge gates, not private worker completion claims"
  },
  {
    surface := PublicSyncSurface.repositoryReadmeOrMeta
    targetPath := "README.md or the authoritative theorem meta surface if one is introduced for THM-M-0398"
    requiredUpdate := "record Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_011.lean as a validated Stage1 statement/package artifact only"
    completionBoundary := "do not describe THM-M-0398 as repo-local completed unless a terminal proof/dependency validates and all M0387 gates close"
  },
  {
    surface := PublicSyncSurface.theoremResearchCatalog
    targetPath := "Docs/researches/math_theorems.md"
    requiredUpdate := "if status wording is refreshed, distinguish source mathematical status from repo-local Lean completion status"
    completionBoundary := "the source catalog may say the theorem is mathematically verified, but public Stage1 must say formalization_debt/not_repo_local_closed"
  }
]

/-- The A12 public-sync plan currently records exactly four public surfaces. -/
theorem s1m011A12PublicSyncTargets_length :
    s1m011A12PublicSyncTargets.length = 4 :=
  rfl

/-- Machine-checkable status labels for the A12 public-sync gate. -/
def s1m011A12PublicSyncStatus : List String := [
  "A12 is public-doc integration work, not terminal code/proof work for StatementShape",
  "this child may only write the owned private ledger and checked Lean metadata; shared public docs require a serial integrator patch",
  "the public patch must preserve formalization_debt/not_repo_local_closed until a terminal proof body or pinned external dependency validates repo-locally",
  "no completed state may retain repo_local_integration_debt; if a future external terminal proof is found, A11 must pin/import/check it or publish a concrete blocker first"
]

/-- Checklist a serial integrator must satisfy before marking A12 complete. -/
def publicSyncIntegratorChecklist : List String := [
  "Stage1 blueprint line and detailed S1-M-011 section name S1_M_011.lean and the validation command",
  "todo surface mirrors the blueprint boundary and does not mark terminal theorem completion",
  "README/meta surface, if updated, says validated Stage1 statement/package artifact rather than proved Thue-Siegel-Roth theorem",
  "theorem research catalog, if updated, separates source mathematical verification from repo-local Lean completion",
  "public wording removes runtime-worker phrasing and keeps private .cron ledgers as evidence anchors only",
  "all public surfaces agree on formalization_debt/not_repo_local_closed unless a future terminal proof/dependency closes every M0387 gate"
]

/-- M0387 machine-proof debt classification for this Stage1 artifact. -/
def machineProofDebtClassification : List String := [
  "mathematical_debt: none for the classical Thue-Siegel-Roth theorem",
  "formalization_debt: terminal proof body is not present in this repository",
  "repo_local_integration_debt: not retained as a completed-state claim; no external proof is used as completion evidence"
]

/--
Primary-source row for `S1-M-011-A10-external-primary-audit`.

The row is audit metadata only.  A URL/commit anchor recorded here is not a
completion certificate unless a later child pins/imports/checks a terminal
Lean proof in the repo-local validation closure.
-/
structure ExternalPrimaryAuditRow where
  sourceUrl : String
  commit : String
  query : String
  outcome : String
  repoLocalGate : String

/-- Primary-source Lean 4 anchors checked or recorded for the external audit. -/
def externalPrimaryAuditRows : List ExternalPrimaryAuditRow := [
  {
    sourceUrl := "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/NumberTheory/Transcendental/Liouville/LiouvilleWith.lean"
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    query := "pinned local mathlib search for Thue-Siegel-Roth, Roth, LiouvilleWith, and DiophantineApproximation"
    outcome := "supporting infrastructure only: LiouvilleWith defines the exponent predicate and cites Thue-Siegel-Roth as mathematical context, but does not prove StatementShape"
    repoLocalGate := "external_upstream_anchor_only; not repo-local completed"
  },
  {
    sourceUrl := "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Combinatorics/Additive/Corner/Roth.lean"
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    query := "pinned local mathlib search for Roth theorem name collisions"
    outcome := "false positive only: additive-combinatorics Roth on three-term arithmetic progressions, not Diophantine approximation of algebraic irrational reals"
    repoLocalGate := "false-positive anchor; not repo-local completed"
  },
  {
    sourceUrl := "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/NumberTheory/SiegelsLemma.lean"
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    query := "pinned local mathlib search for Siegel-lemma substrate used by Roth auxiliary-polynomial proofs"
    outcome := "supporting infrastructure only: integer-matrix Siegel lemma anchors are present, but no Roth auxiliary-polynomial package or terminal theorem is present"
    repoLocalGate := "external_upstream_anchor_only; not repo-local completed"
  },
  {
    sourceUrl := "https://github.com/leanprover-community/mathlib4/tree/49f10344339f99fda2d3bb0aa1455bfa6801fd93"
    commit := "49f10344339f99fda2d3bb0aa1455bfa6801fd93"
    query := "upstream mathlib master revision recorded on 2026-05-01 for current-primary-source follow-up"
    outcome := "current upstream revision recorded; no terminal Thue-Siegel-Roth theorem has been pinned/imported/checked from it in this repository"
    repoLocalGate := "integration required before any completion claim"
  }
]

/-- External-primary audit status for this child task. -/
def externalPrimaryAuditStatus : List String := [
  "A10 is an external-anchor audit, not code/proof completion for StatementShape",
  "pinned local mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95 contains LiouvilleWith, DiophantineApproximation, Height, SiegelLemma, and combinatorial Roth anchors, but no terminal Thue-Siegel-Roth theorem",
  "upstream mathlib master was recorded at 49f10344339f99fda2d3bb0aa1455bfa6801fd93 for serial follow-up; this child does not import or pin that revision",
  "GitHub code search through the unauthenticated REST API returned authentication/rate-limit blockers in this environment, so no external proof is used as completion evidence",
  "repo_local_integration_debt is not retained as a completed state: if a terminal external Lean 4 proof is later found, S1-M-011-A11 must pin/import/check it or record a concrete blocker"
]

/-- Remaining theorem-internal child leaves after this package-split child. -/
def m0387RemainingChildLeaves : List String := [
  "prove or import a checked algebraic-height object model connecting DenominatorHeightRat to the selected mathlib height API",
  "prove the reverse quotient/setoid direction from arbitrary integer pairs to canonical rational finite sets if the public surface requires it",
  "derive RothLowerBoundFor from the finite-exception rational surface by extracting a positive minimum over the finite exceptional set",
  "audit any external Lean 4 Roth/Thue-Siegel-Roth proof before using it as completion evidence",
  "close the auxiliary-polynomial, zero-estimate, denominator-growth, numerator-bound, and Roth-constant extraction packages with <=100-step leaf ledgers",
  "serially merge public blueprint/todo backfill after integrator review"
]

/-- mathlib modules audited while fixing the local statement boundary. -/
def mathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.DiophantineApproximation.Basic",
  "Mathlib.NumberTheory.DiophantineApproximation.ContinuedFractions",
  "Mathlib.NumberTheory.Transcendental.Liouville.LiouvilleWith",
  "Mathlib.NumberTheory.Height.Basic",
  "Mathlib.NumberTheory.Height.MvPolynomial",
  "Mathlib.NumberTheory.Height.Northcott",
  "Mathlib.NumberTheory.Height.NumberField",
  "Mathlib.NumberTheory.Height.Projectivization",
  "Mathlib.NumberTheory.SiegelsLemma",
  "Mathlib.NumberTheory.Real.Irrational",
  "Mathlib.Analysis.SpecialFunctions.Pow.Real",
  "Mathlib.RingTheory.Polynomial.Basic"
]

/--
Import-probe manifest for `S1-M-011-A02`.

The entries name the exact mathlib modules imported in this file for the
Diophantine-approximation, continued-fraction, `LiouvilleWith`, height, and
Siegel-lemma dependency surfaces.  This is a checked import/dependency probe,
not a terminal Thue-Siegel-Roth proof claim.
-/
def importProbeModules : List String := [
  "DiophantineApproximation.Basic -> Mathlib.NumberTheory.DiophantineApproximation.Basic",
  "ContinuedFractions -> Mathlib.NumberTheory.DiophantineApproximation.ContinuedFractions",
  "LiouvilleWith -> Mathlib.NumberTheory.Transcendental.Liouville.LiouvilleWith",
  "Height.Basic -> Mathlib.NumberTheory.Height.Basic",
  "Height.MvPolynomial -> Mathlib.NumberTheory.Height.MvPolynomial",
  "Height.Northcott -> Mathlib.NumberTheory.Height.Northcott",
  "Height.NumberField -> Mathlib.NumberTheory.Height.NumberField",
  "Height.Projectivization -> Mathlib.NumberTheory.Height.Projectivization",
  "SiegelsLemma -> Mathlib.NumberTheory.SiegelsLemma"
]

/--
Name-collision warning for `S1-M-011-A03`.

`Mathlib.Combinatorics.Additive.Corner.Roth` is imported and checked here only
as a false-positive audit anchor.  It proves the additive-combinatorics Roth
theorem on 3-term arithmetic progressions, together with the corners theorem;
it is not the Thue-Siegel-Roth theorem on Diophantine approximation of
irrational algebraic real numbers.
-/
inductive RothFalsePositiveAnchor where
  | additiveCornerRoth
  deriving DecidableEq, Repr

/-- The exact mathlib module whose name can be mistaken for this theorem. -/
def falsePositiveRothModules : List String := [
  "Mathlib.Combinatorics.Additive.Corner.Roth"
]

/-- Checked declaration names from the additive-combinatorics Roth module. -/
def additiveCornerRothDeclarationNames : List String := [
  "corners_theorem",
  "corners_theorem_nat",
  "roth_3ap_theorem",
  "roth_3ap_theorem_nat",
  "rothNumberNat_isLittleO_id"
]

/-- Why the additive-combinatorics Roth module is not completion evidence here. -/
def falsePositiveRothWarning : List String := [
  "Mathlib.Combinatorics.Additive.Corner.Roth is about corner-free sets and 3-term arithmetic progressions",
  "its declarations are additive-combinatorics results over finite abelian groups and natural-number intervals",
  "it does not state a lower bound for rational approximation of irrational algebraic real numbers",
  "it does not close StatementShape, RothLowerBoundFor, or any Thue-Siegel-Roth finite-exception bridge",
  "therefore it is a checked false-positive anchor, not repo-local completion evidence for THM-M-0398"
]

/-- The only false-positive anchor recorded by this child task. -/
def rothFalsePositiveAnchors : List RothFalsePositiveAnchor := [
  RothFalsePositiveAnchor.additiveCornerRoth
]

/-- The false-positive warning list is intentionally nonempty. -/
theorem rothFalsePositiveAnchors_ne_nil :
    rothFalsePositiveAnchors ≠ [] := by
  decide

/-- Checked declarations used by this statement-shape artifact. -/
def checkedLocalAnchors : List String := [
  "Irrational",
  "Polynomial",
  "Polynomial.eval₂",
  "Int.castRingHom",
  "Real.rpow",
  "AlgebraicReal",
  "RothLowerBoundFor",
  "StatementShape",
  "StatementSurface",
  "chosenStatementSurface",
  "ChosenIntegerPairSurface",
  "BetterThanRothBound",
  "FiniteExceptionSurfaceFor",
  "NormalizedRatPair",
  "RationalApproximationErrorRat",
  "DenominatorHeightRat",
  "BetterThanRothBoundRat",
  "FiniteRationalExceptionSurfaceFor",
  "normalizedRatPair_injective",
  "normalizedRatPair_denominator_ne",
  "denominatorHeight_nonneg",
  "denominatorHeight_pos",
  "one_le_denominatorHeight",
  "denominatorHeightRat_pos",
  "denominatorHeightRat_ne_zero",
  "one_le_denominatorHeightRat",
  "denominatorHeightRat_eq_pair",
  "normalizedRatPair_coprime_natAbs_den",
  "normalizedRatPair_rational_value",
  "rationalApproximationErrorRat_eq_pair",
  "betterThanRothBound_of_rat",
  "finiteRationalExceptionSurfaceFor_of_finiteExceptionSurfaceFor",
  "not_liouvilleWith_of_rothLowerBoundFor",
  "not_liouvilleWith_of_statementShape",
  "ApproximationTheoryPackage",
  "approximationTheoryPackageSplit",
  "SiegelLemmaAuxiliaryPolynomialLeaf",
  "siegelLemmaAuxiliaryPolynomialLeaves",
  "siegelLemmaAuxiliaryPolynomialLeaves_length",
  "siegelLemmaCheckedAnchors",
  "siegelLemmaInputObligations",
  "siegelLemmaOutputInterface",
  "siegelLemmaAuxiliaryPolynomialBlockers",
  "siegelLemmaAuxiliaryPolynomialStatus",
  "DenominatorHeightAuditLeaf",
  "denominatorHeightAuditLeaves",
  "denominatorHeightCheckedAnchors",
  "algebraicHeightAuditAnchors",
  "heightBridgeIntegrationBlockers",
  "ZeroEstimateProductFormulaLeaf",
  "zeroEstimateProductFormulaLeaves",
  "zeroEstimateProductFormulaLeaves_length",
  "zeroEstimateProductFormulaCheckedAnchors",
  "zeroEstimateProductFormulaMissingAPIs",
  "zeroEstimateProductFormulaStatus",
  "GapPrincipleFinitenessLeaf",
  "gapPrincipleFinitenessLeaves",
  "gapPrincipleFinitenessLeaves_length",
  "BadPairNatAbsBounds",
  "finite_int_natAbs_le",
  "finite_pair_natAbs_le",
  "finiteExceptionSurfaceFor_of_badPairNatAbsBounds",
  "finiteRationalExceptionSurfaceFor_of_badPairNatAbsBounds",
  "gapPrincipleFinitenessCheckedAnchors",
  "gapPrincipleFinitenessMissingAPIs",
  "gapPrincipleFinitenessStatus",
  "ThueSiegelRothFormalizationDebt",
  "PublicSyncSurface",
  "PublicSyncTargetRow",
  "s1m011A12PublicSyncTargets",
  "s1m011A12PublicSyncTargets_length",
  "s1m011A12PublicSyncStatus",
  "publicSyncIntegratorChecklist",
  "RothFalsePositiveAnchor",
  "falsePositiveRothWarning"
]

/--
Search terms that did not locate a terminal repo-local Lean theorem for the
Thue-Siegel-Roth theorem in this repair pass.
-/
def absentTerminalSearchTerms : List String := [
  "Roth",
  "Thue",
  "Siegel",
  "Diophantine approximation",
  "irrationality exponent",
  "algebraic approximation",
  "Thue-Siegel-Roth"
]

#check AlgebraicReal
#check IrrationalAlgebraicReal
#check RothLowerBoundFor
#check StatementShape
#check StatementSurface
#check chosenStatementSurface
#check chosenStatementSurface_eq_integerPair
#check ChosenIntegerPairSurface
#check chosenIntegerPairSurface_iff_statementShape
#check statementShape_unfold
#check BetterThanRothBound
#check FiniteExceptionSurfaceFor
#check betterThanRothBound_denominator_ne
#check betterThanRothBound_error_lt
#check NormalizedRatPair
#check RationalApproximationErrorRat
#check DenominatorHeightRat
#check BetterThanRothBoundRat
#check FiniteRationalExceptionSurfaceFor
#check normalizedRatPair_injective
#check normalizedRatPair_denominator_ne
#check denominatorHeight_nonneg
#check denominatorHeight_pos
#check one_le_denominatorHeight
#check denominatorHeightRat_pos
#check denominatorHeightRat_ne_zero
#check one_le_denominatorHeightRat
#check denominatorHeightRat_eq_pair
#check normalizedRatPair_coprime_natAbs_den
#check normalizedRatPair_rational_value
#check rationalApproximationErrorRat_eq_pair
#check betterThanRothBound_of_rat
#check finiteRationalExceptionSurfaceFor_of_finiteExceptionSurfaceFor
#check not_liouvilleWith_of_rothLowerBoundFor
#check not_liouvilleWith_of_statementShape
#check ApproximationTheoryPackage
#check approximationTheoryPackageSplit
#check approximationTheoryPackageSplit_length
#check Int.Matrix.exists_ne_zero_int_vec_norm_le
#check Int.Matrix.exists_ne_zero_int_vec_norm_le'
#check Int.Matrix.one_le_norm_A_of_ne_zero
#check SiegelLemmaAuxiliaryPolynomialLeaf
#check siegelLemmaAuxiliaryPolynomialLeaves
#check siegelLemmaAuxiliaryPolynomialLeaves_length
#check siegelLemmaCheckedAnchors
#check siegelLemmaInputObligations
#check siegelLemmaOutputInterface
#check siegelLemmaAuxiliaryPolynomialBlockers
#check siegelLemmaAuxiliaryPolynomialStatus
#check DenominatorHeightAuditLeaf
#check denominatorHeightAuditLeaves
#check denominatorHeightAuditLeaves_length
#check denominatorHeightCheckedAnchors
#check algebraicHeightAuditAnchors
#check heightBridgeIntegrationBlockers
#check Height.AdmissibleAbsValues.product_formula
#check NumberField.prod_abs_eq_one
#check NumberField.FinitePlace.prod_eq_inv_abs_norm
#check Height.mulHeight_eval_le
#check Height.logHeight_eval_le
#check Height.mulHeight_eval_ge
#check Height.logHeight_eval_ge
#check ZeroEstimateProductFormulaLeaf
#check zeroEstimateProductFormulaLeaves
#check zeroEstimateProductFormulaLeaves_length
#check zeroEstimateProductFormulaCheckedAnchors
#check zeroEstimateProductFormulaMissingAPIs
#check zeroEstimateProductFormulaStatus
#check GapPrincipleFinitenessLeaf
#check gapPrincipleFinitenessLeaves
#check gapPrincipleFinitenessLeaves_length
#check BadPairNatAbsBounds
#check finite_int_natAbs_le
#check finite_pair_natAbs_le
#check finiteExceptionSurfaceFor_of_badPairNatAbsBounds
#check finiteRationalExceptionSurfaceFor_of_badPairNatAbsBounds
#check gapPrincipleFinitenessCheckedAnchors
#check gapPrincipleFinitenessMissingAPIs
#check gapPrincipleFinitenessStatus
#check ThueSiegelRothFormalizationDebt
#check repoLocalIntegrationDebtGate
#check IntegrationGateState
#check ExternalIntegrationGateRow
#check s1m011A11IntegrationGateRows
#check s1m011A11IntegrationGateRows_length
#check s1m011A11IntegrationGateStatus
#check PublicSyncSurface
#check PublicSyncTargetRow
#check s1m011A12PublicSyncTargets
#check s1m011A12PublicSyncTargets_length
#check s1m011A12PublicSyncStatus
#check publicSyncIntegratorChecklist
#check machineProofDebtClassification
#check ExternalPrimaryAuditRow
#check externalPrimaryAuditRows
#check externalPrimaryAuditStatus
#check importProbeModules
#check _root_.corners_theorem
#check _root_.corners_theorem_nat
#check _root_.roth_3ap_theorem
#check _root_.roth_3ap_theorem_nat
#check _root_.rothNumberNat_isLittleO_id
#check RothFalsePositiveAnchor
#check falsePositiveRothModules
#check additiveCornerRothDeclarationNames
#check falsePositiveRothWarning
#check rothFalsePositiveAnchors
#check rothFalsePositiveAnchors_ne_nil

end

end AwesomeTheorems.Stage1.S1_M_011
