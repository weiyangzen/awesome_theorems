import Mathlib.Data.Complex.Basic
import Mathlib.Algebra.Algebra.Spectrum.Basic
import Mathlib.Algebra.Lie.Classical
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Matrix.Normed
import Mathlib.LinearAlgebra.Matrix.Charpoly.Basic
import Mathlib.RingTheory.Derivation.Basic

/-!
# S1-M-209 / THM-M-1550: Lax pairs

This Stage1 artifact records a conservative Lean 4 boundary for the statement
that integrable systems have a Lax-pair representation.  The physical/source
phrase "representation of integrable systems" is not a kernel-checkable theorem
until the class of systems, phase space, Hamiltonian structure, and spectral
invariants are fixed.

The checked part below uses finite complex matrices as the first object model:
a Lax equation `dL/dt = [P,L]`, algebra spectra of matrices, and the standard
conjugation bridge showing that unit-conjugate matrix flows are isospectral.
The proof that a concrete integrable system produces the conjugating evolution
remains formalization debt.
-/

noncomputable section

open Matrix
open scoped Matrix.Norms.Elementwise

universe u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_209

/-- Finite complex matrix operators used for the Stage1 Lax-pair boundary. -/
abbrev LaxMatrix (n : Type u) : Type u :=
  Matrix n n ℂ

variable {n : Type u} [DecidableEq n] [Fintype n]

/-- Matrix commutator `[A,B] = A * B - B * A`. -/
def matrixCommutator (A B : LaxMatrix n) : LaxMatrix n :=
  A * B - B * A

/-- The commutator agrees with mathlib's associative-ring Lie bracket. -/
theorem matrixCommutator_eq_lie (A B : LaxMatrix n) :
    matrixCommutator A B = ⁅A, B⁆ := by
  simp [matrixCommutator, Ring.lie_def]

/-- Lax equation on a chosen real-time domain: `dL/dt = [P,L]`. -/
def LaxEquationOn
    (L P : ℝ → LaxMatrix n) (timeDomain : Set ℝ) : Prop :=
  ∀ t ∈ timeDomain,
    HasDerivWithinAt L (matrixCommutator (P t) (L t)) timeDomain t

/-- Algebra spectrum of a finite Lax matrix. -/
def MatrixSpectrum (A : LaxMatrix n) : Set ℂ :=
  spectrum ℂ A

/-- Isospectrality over a time domain. -/
def IsospectralOn (L : ℝ → LaxMatrix n) (timeDomain : Set ℝ) : Prop :=
  ∀ t₀ ∈ timeDomain, ∀ t ∈ timeDomain,
    MatrixSpectrum (L t) = MatrixSpectrum (L t₀)

/-- At two times, the Lax matrices are related by conjugation by a matrix unit. -/
def ConjugatesAt (L : ℝ → LaxMatrix n) (t₀ t : ℝ) : Prop :=
  ∃ U : (LaxMatrix n)ˣ,
    L t = (U : LaxMatrix n) * L t₀ * (↑U⁻¹ : LaxMatrix n)

/-- Conjugating evolution package over a time domain. -/
def IsospectralByConjugationOn
    (L : ℝ → LaxMatrix n) (timeDomain : Set ℝ) : Prop :=
  ∀ t₀ ∈ timeDomain, ∀ t ∈ timeDomain, ConjugatesAt L t₀ t

/--
The Leibniz compatibility expected of a Poisson bracket on an algebra of
observables.  The Lie-ring and scalar-linearity laws are supplied by mathlib
typeclasses; this local predicate records the Poisson-specific multiplication
law.
-/
def PoissonLeibniz (A : Type u)
    [CommRing A] [Algebra ℂ A] [LieRing A] [LieAlgebra ℂ A] : Prop :=
  ∀ f g h : A, ⁅f, g * h⁆ = ⁅f, g⁆ * h + g * ⁅f, h⁆

/--
Concrete algebraic Hamiltonian/Poisson interface used by the finite-matrix Lax
boundary.

This is still an abstract observable algebra, but it is no longer a bare
placeholder proposition: the observables carry mathlib algebra and Lie-algebra
instances, the bracket satisfies the Poisson Leibniz rule, and the Hamiltonian
vector field is a mathlib derivation.
-/
structure AlgebraicHamiltonianPoissonModel (A : Type u)
    [CommRing A] [Algebra ℂ A] [LieRing A] [LieAlgebra ℂ A] : Type u where
  hamiltonian : A
  poissonLeibniz : PoissonLeibniz A
  hamiltonianVectorField : Derivation ℂ A A
  vectorField_eq_poissonBracket :
    ∀ f : A, hamiltonianVectorField f = ⁅hamiltonian, f⁆

/-- The finite-matrix spectral invariants exposed by the Stage1 boundary. -/
structure FiniteMatrixSpectralInvariants
    (L : ℝ → LaxMatrix n) : Type u where
  spectrumAt : ℝ → Set ℂ
  traceAt : ℝ → ℂ
  tracePowerAt : ℝ → ℕ → ℂ
  charpolyAt : ℝ → Polynomial ℂ
  spectrumAt_eq : ∀ t : ℝ, spectrumAt t = MatrixSpectrum (L t)
  traceAt_eq : ∀ t : ℝ, traceAt t = Matrix.trace (L t)
  tracePowerAt_eq : ∀ (t : ℝ) (k : ℕ),
    tracePowerAt t k = Matrix.trace ((L t) ^ k)
  charpolyAt_eq : ∀ t : ℝ, charpolyAt t = Matrix.charpoly (L t)

/-- Canonical finite-matrix spectral invariant package for a Lax matrix path. -/
def canonicalFiniteMatrixSpectralInvariants
    (L : ℝ → LaxMatrix n) : FiniteMatrixSpectralInvariants L where
  spectrumAt := fun t => MatrixSpectrum (L t)
  traceAt := fun t => Matrix.trace (L t)
  tracePowerAt := fun t k => Matrix.trace ((L t) ^ k)
  charpolyAt := fun t => Matrix.charpoly (L t)
  spectrumAt_eq := by intro t; rfl
  traceAt_eq := by intro t; rfl
  tracePowerAt_eq := by intro t k; rfl
  charpolyAt_eq := by intro t; rfl

/-- Characteristic-polynomial conservation over a time domain. -/
def CharacteristicPolynomialInvariantOn
    (L : ℝ → LaxMatrix n) (timeDomain : Set ℝ) : Prop :=
  ∀ t₀ ∈ timeDomain, ∀ t ∈ timeDomain,
    Matrix.charpoly (L t) = Matrix.charpoly (L t₀)

/-- Conservation of all trace powers `trace (L(t)^k)` over a time domain. -/
def TracePowersInvariantOn
    (L : ℝ → LaxMatrix n) (timeDomain : Set ℝ) : Prop :=
  ∀ t₀ ∈ timeDomain, ∀ t ∈ timeDomain, ∀ k : ℕ,
    Matrix.trace ((L t) ^ k) = Matrix.trace ((L t₀) ^ k)

/--
Finite-matrix spectral conservation currently derivable from a supplied
conjugating evolution.
-/
structure FiniteMatrixSpectralConservation
    (L : ℝ → LaxMatrix n) (timeDomain : Set ℝ) : Prop where
  spectrumOn : IsospectralOn L timeDomain
  characteristicPolynomialOn : CharacteristicPolynomialInvariantOn L timeDomain
  tracePowersOn : TracePowersInvariantOn L timeDomain

/--
Concrete evolution package replacing the earlier proposition field saying a
conjugating evolution is available.
-/
structure ConjugatingEvolutionPackage
    (L : ℝ → LaxMatrix n) (timeDomain : Set ℝ) : Type u where
  conjugatesOn : IsospectralByConjugationOn L timeDomain

/--
Explicit regularity and evolution hypotheses for the finite-matrix bridge from
a Lax equation to conjugation-based isospectrality.

The `conjugatesOn` field is the still-nontrivial ODE/evolution input: this
package records the local theorem boundary without claiming that mathlib
currently derives the conjugating fundamental solution from `equationOn`.
-/
structure LaxEquationConjugationBridgeHypotheses
    (L P : ℝ → LaxMatrix n) (timeDomain : Set ℝ) : Prop where
  equationOn : LaxEquationOn L P timeDomain
  L_differentiableOn : DifferentiableOn ℝ L timeDomain
  P_continuousOn : ContinuousOn P timeDomain
  conjugatesOn : IsospectralByConjugationOn L timeDomain

/--
Data for a finite-matrix Lax-pair statement with concrete local APIs.

Concrete mathlib data:
* `L` and `P` are time-indexed finite complex matrices;
* `equationOn` states the Lax equation using `HasDerivWithinAt`;
* `MatrixSpectrum` is mathlib's algebra spectrum.

The Hamiltonian/Poisson side is represented by an observable algebra with
mathlib `CommRing`, `Algebra`, `LieRing`, `LieAlgebra`, and `Derivation` APIs.
The spectral side is represented by concrete spectrum, trace, and
characteristic-polynomial functions.  The remaining unproved mathematical
bridge is explicit in `evolution`: this data assumes a conjugating evolution
rather than deriving it from the Lax ODE.
-/
structure LaxPairData (n : Type u) [DecidableEq n] [Fintype n] : Type (u + 1) where
  L : ℝ → LaxMatrix n
  P : ℝ → LaxMatrix n
  timeDomain : Set ℝ
  equationOn : LaxEquationOn L P timeDomain
  ObservableAlgebra : Type u
  observableCommRing : CommRing ObservableAlgebra
  observableAlgebra : Algebra ℂ ObservableAlgebra
  observableLieRing : LieRing ObservableAlgebra
  observableLieAlgebra : LieAlgebra ℂ ObservableAlgebra
  hamiltonianPoissonModel :
    @AlgebraicHamiltonianPoissonModel ObservableAlgebra observableCommRing
      observableAlgebra observableLieRing observableLieAlgebra
  spectralInvariants : FiniteMatrixSpectralInvariants L
  evolution : ConjugatingEvolutionPackage L timeDomain

/-- Hypotheses retained by the normalized Stage1 statement boundary. -/
def LaxPairHypotheses {n : Type u} [DecidableEq n] [Fintype n]
    (_D : LaxPairData n) : Prop :=
  True

/-- Expected output of the finite-matrix Lax theorem: isospectrality of `L(t)`. -/
def LaxPairConclusion {n : Type u} [DecidableEq n] [Fintype n]
    (D : LaxPairData n) : Prop :=
  IsospectralOn D.L D.timeDomain

/--
Stage1 normalized statement shape for THM-M-1550.

For every finite-dimensional complex matrix model, if the Lax equation
represents a chosen integrable system and the Hamiltonian/Poisson and
spectral-invariant interfaces are supplied, the Lax matrix is expected to be
isospectral on the time domain.

This is a statement boundary, not a terminal proof that every integrable system
has such a representation.
-/
def StatementShape : Prop :=
  ∀ (n : Type u) [DecidableEq n] [Fintype n],
    ∀ D : LaxPairData n,
      LaxPairHypotheses D → LaxPairConclusion D

/-- The normalized statement shape unfolds to the quantified implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u} ↔
      ∀ (n : Type u) [DecidableEq n] [Fintype n],
        ∀ D : LaxPairData n,
          LaxPairHypotheses D → LaxPairConclusion D :=
  Iff.rfl

/-- The trace of a finite matrix commutator is zero. -/
theorem trace_matrixCommutator_zero (A B : LaxMatrix n) :
    Matrix.trace (matrixCommutator A B) = 0 := by
  simpa [matrixCommutator, Ring.lie_def] using
    (LieAlgebra.matrix_trace_commutator_zero n ℂ A B)

/-- Unit conjugation preserves the finite matrix spectrum. -/
theorem spectrum_eq_of_units_conjugate (A B : LaxMatrix n)
    (U : (LaxMatrix n)ˣ)
    (hB : B = (U : LaxMatrix n) * A * (↑U⁻¹ : LaxMatrix n)) :
    MatrixSpectrum B = MatrixSpectrum A := by
  rw [hB, MatrixSpectrum]
  exact spectrum.units_conjugate

/-- A `ConjugatesAt` witness gives equality of spectra at the two times. -/
theorem spectrum_eq_of_conjugatesAt {L : ℝ → LaxMatrix n} {t₀ t : ℝ}
    (h : ConjugatesAt L t₀ t) :
    MatrixSpectrum (L t) = MatrixSpectrum (L t₀) := by
  rcases h with ⟨U, hU⟩
  exact spectrum_eq_of_units_conjugate (L t₀) (L t) U hU

/--
If the flow is already known to be implemented by unit conjugation, then it is
isospectral.  This is the checked bridge lemma available in the current local
closure; proving the conjugating evolution from the Lax ODE is left open here.
-/
theorem isospectralOn_of_conjugates {L : ℝ → LaxMatrix n} {timeDomain : Set ℝ}
    (h : IsospectralByConjugationOn L timeDomain) :
    IsospectralOn L timeDomain := by
  intro t₀ ht₀ t ht
  exact spectrum_eq_of_conjugatesAt (h t₀ ht₀ t ht)

/--
Bridge from a checked Lax equation package to conjugation-based isospectrality,
under explicit regularity and evolution hypotheses.

This is the strongest repo-local bridge available here: the Lax ODE and
regularity hypotheses are kernel-visible, while the construction of the
conjugating evolution remains an explicit input rather than an unproved claim.
-/
theorem isospectralByConjugationOn_of_laxEquationOn
    {L P : ℝ → LaxMatrix n} {timeDomain : Set ℝ}
    (h : LaxEquationConjugationBridgeHypotheses L P timeDomain) :
    IsospectralByConjugationOn L timeDomain :=
  h.conjugatesOn

/--
Combining the explicit Lax-equation/conjugating-evolution bridge with the
checked spectrum-conjugation lemma gives finite-matrix isospectrality.
-/
theorem isospectralOn_of_laxEquationOn_with_conjugatingEvolution
    {L P : ℝ → LaxMatrix n} {timeDomain : Set ℝ}
    (h : LaxEquationConjugationBridgeHypotheses L P timeDomain) :
    IsospectralOn L timeDomain :=
  isospectralOn_of_conjugates
    (isospectralByConjugationOn_of_laxEquationOn h)

/-- Matrix trace is invariant under unit conjugation. -/
theorem trace_eq_of_units_conjugate (A : LaxMatrix n) (U : (LaxMatrix n)ˣ) :
    Matrix.trace ((U : LaxMatrix n) * A * (↑U⁻¹ : LaxMatrix n)) =
      Matrix.trace A :=
  Matrix.trace_units_conj U A

/-- Powers of a unit conjugate are unit conjugates of powers. -/
theorem pow_units_conjugate (A : LaxMatrix n) (U : (LaxMatrix n)ˣ) (k : ℕ) :
    ((U : LaxMatrix n) * A * (↑U⁻¹ : LaxMatrix n)) ^ k =
      (U : LaxMatrix n) * A ^ k * (↑U⁻¹ : LaxMatrix n) := by
  simpa using Units.conj_pow U A k

/-- Trace powers are invariant under unit conjugation. -/
theorem trace_pow_eq_of_units_conjugate
    (A : LaxMatrix n) (U : (LaxMatrix n)ˣ) (k : ℕ) :
    Matrix.trace (((U : LaxMatrix n) * A * (↑U⁻¹ : LaxMatrix n)) ^ k) =
      Matrix.trace (A ^ k) := by
  rw [pow_units_conjugate A U k]
  exact Matrix.trace_units_conj U (A ^ k)

/-- The characteristic polynomials of `A * B` and `B * A` agree. -/
theorem charpoly_mul_comm_anchor (A B : LaxMatrix n) :
    Matrix.charpoly (A * B) = Matrix.charpoly (B * A) :=
  Matrix.charpoly_mul_comm A B

/-- Characteristic polynomials are invariant under unit conjugation. -/
theorem charpoly_eq_of_units_conjugate
    (A : LaxMatrix n) (U : (LaxMatrix n)ˣ) :
    Matrix.charpoly ((U : LaxMatrix n) * A * (↑U⁻¹ : LaxMatrix n)) =
      Matrix.charpoly A := by
  calc
    Matrix.charpoly ((U : LaxMatrix n) * A * (↑U⁻¹ : LaxMatrix n))
        = Matrix.charpoly ((↑U⁻¹ : LaxMatrix n) * ((U : LaxMatrix n) * A)) := by
          simpa [Matrix.mul_assoc] using
            (Matrix.charpoly_mul_comm ((U : LaxMatrix n) * A)
              (↑U⁻¹ : LaxMatrix n))
    _ = Matrix.charpoly A := by
          simp

/-- A `ConjugatesAt` witness gives equality of characteristic polynomials. -/
theorem charpoly_eq_of_conjugatesAt {L : ℝ → LaxMatrix n} {t₀ t : ℝ}
    (h : ConjugatesAt L t₀ t) :
    Matrix.charpoly (L t) = Matrix.charpoly (L t₀) := by
  rcases h with ⟨U, hU⟩
  rw [hU]
  exact charpoly_eq_of_units_conjugate (L t₀) U

/-- A `ConjugatesAt` witness gives equality of all trace powers. -/
theorem trace_pow_eq_of_conjugatesAt
    {L : ℝ → LaxMatrix n} {t₀ t : ℝ}
    (h : ConjugatesAt L t₀ t) (k : ℕ) :
    Matrix.trace ((L t) ^ k) = Matrix.trace ((L t₀) ^ k) := by
  rcases h with ⟨U, hU⟩
  rw [hU]
  exact trace_pow_eq_of_units_conjugate (L t₀) U k

/--
Unit-conjugating evolution preserves characteristic polynomials across the
time domain.
-/
theorem characteristicPolynomialInvariantOn_of_conjugates
    {L : ℝ → LaxMatrix n} {timeDomain : Set ℝ}
    (h : IsospectralByConjugationOn L timeDomain) :
    CharacteristicPolynomialInvariantOn L timeDomain := by
  intro t₀ ht₀ t ht
  exact charpoly_eq_of_conjugatesAt (h t₀ ht₀ t ht)

/--
Unit-conjugating evolution preserves all trace powers across the time domain.
-/
theorem tracePowersInvariantOn_of_conjugates
    {L : ℝ → LaxMatrix n} {timeDomain : Set ℝ}
    (h : IsospectralByConjugationOn L timeDomain) :
    TracePowersInvariantOn L timeDomain := by
  intro t₀ ht₀ t ht k
  exact trace_pow_eq_of_conjugatesAt (h t₀ ht₀ t ht) k

/--
The currently checked finite-matrix spectral package: a supplied conjugating
evolution preserves algebra spectrum, characteristic polynomial, and all trace
powers.
-/
theorem finiteMatrixSpectralConservation_of_conjugates
    {L : ℝ → LaxMatrix n} {timeDomain : Set ℝ}
    (h : IsospectralByConjugationOn L timeDomain) :
    FiniteMatrixSpectralConservation L timeDomain where
  spectrumOn := isospectralOn_of_conjugates h
  characteristicPolynomialOn :=
    characteristicPolynomialInvariantOn_of_conjugates h
  tracePowersOn := tracePowersInvariantOn_of_conjugates h

/-- The concrete Hamiltonian/Poisson model carried by the data package. -/
def LaxPairHypotheses.HamiltonianOrPoissonModel
    {D : LaxPairData n} (_h : LaxPairHypotheses D) :
    @AlgebraicHamiltonianPoissonModel D.ObservableAlgebra
      D.observableCommRing D.observableAlgebra D.observableLieRing
        D.observableLieAlgebra :=
  D.hamiltonianPoissonModel

/-- The concrete finite-matrix spectral invariant package carried by the data. -/
def LaxPairHypotheses.spectralInvariantsWellFormed
    {D : LaxPairData n} (_h : LaxPairHypotheses D) :
    FiniteMatrixSpectralInvariants D.L :=
  D.spectralInvariants

/-- The concrete conjugating-evolution witness carried by the data package. -/
theorem LaxPairHypotheses.conjugatingEvolutionAvailable
    {D : LaxPairData n} (_h : LaxPairHypotheses D) :
    IsospectralByConjugationOn D.L D.timeDomain :=
  D.evolution.conjugatesOn

/-- A finite-matrix Lax data package with conjugating evolution is isospectral. -/
theorem conclusion_of_laxPairData (D : LaxPairData n) :
    LaxPairConclusion D :=
  isospectralOn_of_conjugates D.evolution.conjugatesOn

/--
A finite-matrix Lax data package with conjugating evolution preserves the
checked spectral invariants: algebra spectrum, characteristic polynomial, and
all trace powers.
-/
theorem spectralConservation_of_laxPairData (D : LaxPairData n) :
    FiniteMatrixSpectralConservation D.L D.timeDomain :=
  finiteMatrixSpectralConservation_of_conjugates D.evolution.conjugatesOn

/--
Checked closure of the finite-matrix statement boundary.

This closes only the normalized finite-matrix theorem with a supplied
conjugating evolution package.  It does not prove that a Hamiltonian or Poisson
system produces such an evolution from the Lax ODE.
-/
theorem statementShape_from_laxPairData : StatementShape.{u} := by
  intro n _ _ D _h
  exact conclusion_of_laxPairData D

/-- mathlib modules checked while locating repo-local Lax-pair anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Algebra.Algebra.Spectrum.Basic",
  "Mathlib.Algebra.Lie.Classical",
  "Mathlib.Algebra.Lie.OfAssociative",
  "Mathlib.Analysis.Calculus.Deriv.Basic",
  "Mathlib.Analysis.ODE.Basic",
  "Mathlib.Analysis.ODE.PicardLindelof",
  "Mathlib.LinearAlgebra.Matrix.Trace",
  "Mathlib.LinearAlgebra.Matrix.Charpoly.Basic",
  "Mathlib.Analysis.Matrix.Spectrum",
  "Mathlib.Algebra.Group.Semiconj.Units",
  "Mathlib.RingTheory.Derivation.Basic"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "spectrum",
  "spectrum.units_conjugate",
  "LieAlgebra.matrix_trace_commutator_zero",
  "Matrix.trace",
  "Matrix.trace_units_conj",
  "Matrix.trace_mul_comm",
  "Matrix.charpoly",
  "Matrix.charpoly_mul_comm",
  "Units.conj_pow",
  "HasDerivWithinAt",
  "Derivation"
]

/--
Search terms that did not locate a terminal Lax-pair or integrable-systems
theorem in the pinned local mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "Lax pair",
  "LaxPair",
  "lax_pair",
  "integrable system",
  "isospectral flow",
  "Toda lattice",
  "KdV Lax",
  "inverse scattering"
]

/-! ## Public target selection -/

/-- Candidate public theorem targets considered for this Stage1 Lax-pair slot. -/
inductive PublicTheoremTarget where
  /-- Finite-dimensional complex matrix Lax flows. -/
  | finiteMatrixLaxFlows
  /-- Bounded Hilbert-space operator Lax flows. -/
  | boundedHilbertSpaceOperators
  /-- Unbounded operator or PDE Lax pairs. -/
  | unboundedOperatorPDELaxPairs
  /-- A Toda-lattice-specific Lax-pair theorem. -/
  | todaLattice
  /-- A KdV-specific Lax-pair theorem. -/
  | kdv
  /-- A broad root theorem plus a checked example theorem. -/
  | twoLevelRootPlusExample
  deriving DecidableEq, Repr

/--
Canonical public target selected by this child: finite matrix Lax flows.

This matches the repo-local statement boundary already checked in this file.
The broader Hilbert-space, unbounded/PDE, Toda, KdV, and two-level variants are
left as deferred targets until concrete mathlib/local APIs and proof bridges
are available.
-/
def selectedPublicTheoremTarget : PublicTheoremTarget :=
  PublicTheoremTarget.finiteMatrixLaxFlows

/-- Deferred public target alternatives after selecting finite matrix Lax flows. -/
def deferredPublicTheoremTargets : List PublicTheoremTarget := [
  PublicTheoremTarget.boundedHilbertSpaceOperators,
  PublicTheoremTarget.unboundedOperatorPDELaxPairs,
  PublicTheoremTarget.todaLattice,
  PublicTheoremTarget.kdv,
  PublicTheoremTarget.twoLevelRootPlusExample
]

/-- Checked witness for the selected public theorem target. -/
theorem selectedPublicTheoremTarget_eq :
    selectedPublicTheoremTarget =
      PublicTheoremTarget.finiteMatrixLaxFlows :=
  rfl

/-- Public target-selection note for serialized Stage1 backfill. -/
def selectedPublicTheoremTargetNote : String :=
  "Canonical public target selected for S1-M-209 / THM-M-1550: finite " ++
    "complex matrix Lax flows, represented repo-locally by StatementShape " ++
      "and the LaxMatrix/LaxEquationOn/IsospectralOn boundary in " ++
        "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_209.lean. " ++
          "Bounded Hilbert-space, unbounded/PDE, Toda, KdV, and two-level " ++
            "root-plus-example formulations remain deferred formalization targets."

/-- Completion status for the current repo-local Stage1 Lax-pair artifact. -/
inductive Stage1BoundaryStatus where
  /-- The file validates a finite-matrix statement boundary and bridge lemmas. -/
  | finiteMatrixStatementBoundary
  /-- A terminal theorem for THM-M-1550 is locally proved or pinned and checked. -/
  | terminalTheoremClosed
  deriving DecidableEq, Repr

/--
Current checked status: finite-matrix statement boundary only.

This is intentionally not `terminalTheoremClosed`; the file does not prove that
every chosen integrable-system class admits a Lax-pair representation.
-/
def currentStage1BoundaryStatus : Stage1BoundaryStatus :=
  Stage1BoundaryStatus.finiteMatrixStatementBoundary

/-- Checked guard preventing the artifact status from being read as closed. -/
theorem currentStage1BoundaryStatus_eq :
    currentStage1BoundaryStatus =
      Stage1BoundaryStatus.finiteMatrixStatementBoundary :=
  rfl

/-- Public note text for serialized Stage1 backfill. -/
def publicStage1BoundaryNote : String :=
  "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_209.lean validates a " ++
    "finite-matrix Lax-pair statement boundary and conjugation-to-isospectral " ++
      "bridge lemmas, including characteristic-polynomial and trace-power " ++
        "invariance under a supplied conjugating evolution; it is not a " ++
          "proof of THM-M-1550."

/-- Validation command for this Stage1 artifact. -/
def stage1ValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_209.lean"

/-- Historical parent-worker validation date requested for public backfill. -/
def parentWorkerValidationDate : String :=
  "2026-04-30"

/-- Historical parent-worker validation result requested for public backfill. -/
def parentWorkerValidationResult : String :=
  "pass"

/-- Current child-worker validation date for the refreshed artifact. -/
def childWorkerValidationDate : String :=
  "2026-05-01"

/--
Repo-local integration-debt gate note.

No external Lean 4 terminal Lax-pair proof is currently pinned/imported/checked
for this slot, and no completion claim is made from anchor-only evidence.
-/
def repoLocalIntegrationDebtGateNote : String :=
  "pass for the finite-matrix boundary; full THM-M-1550 remains not_repo_local_closed"

/-! ## C008 external Lean proof integration gate -/

/--
Disposition for the C008 child task:
if a terminal external Lean 4 Lax-pair proof is found, it must be
pin/import/check integrated or blocked by a concrete integration reason.
-/
inductive C008ExternalLeanProofDisposition where
  /-- No terminal external Lean 4 proof has been located by this child. -/
  | noTerminalExternalProofFound
  /-- A terminal external proof has entered the repo-local validation closure. -/
  | pinnedImportedChecked
  /-- A located terminal proof is blocked by an explicit integration issue. -/
  | concreteIntegrationBlocker
  deriving DecidableEq, Repr

/-- Search terms owned by C008 for the external-proof integration gate. -/
def c008ExternalLeanProofSearchTerms : List String := [
  "LaxPair",
  "LaxEquation",
  "isospectral",
  "Toda",
  "KdV",
  "integrable system"
]

/--
Current C008 external-proof disposition.

This is intentionally not `pinnedImportedChecked`: the child did not locate a
terminal external Lean 4 proof suitable for Lake integration.
-/
def c008ExternalLeanProofDisposition : C008ExternalLeanProofDisposition :=
  C008ExternalLeanProofDisposition.noTerminalExternalProofFound

/-- Checked witness for the current C008 external-proof disposition. -/
theorem c008ExternalLeanProofDisposition_eq :
    c008ExternalLeanProofDisposition =
      C008ExternalLeanProofDisposition.noTerminalExternalProofFound :=
  rfl

/--
C008 completion gate: this child only passes as an open, not-completed gate.

The finite-matrix boundary is validated, but THM-M-1550 is not terminally
closed by a local proof body, mathlib wrapper, or pinned external dependency.
-/
def C008RepoLocalIntegrationDebtGate : Prop :=
  c008ExternalLeanProofDisposition =
      C008ExternalLeanProofDisposition.noTerminalExternalProofFound ∧
    currentStage1BoundaryStatus =
      Stage1BoundaryStatus.finiteMatrixStatementBoundary

/-- No C008 completed state is claimed from anchor-only external evidence. -/
theorem c008RepoLocalIntegrationDebtGate :
    C008RepoLocalIntegrationDebtGate := by
  constructor <;> rfl

/-- C008 ledger note for serialized public backfill. -/
def c008PublicBackfillNote : String :=
  "S1-M-209-C008 found no terminal external Lean 4 Lax-pair proof to " ++
    "pin/import/check in this child pass.  The repo-local Lean file validates " ++
      "a finite-matrix boundary only; THM-M-1550 remains open under " ++
        "formalization_debt, and no completed state may retain " ++
          "repo_local_integration_debt.  If a later authenticated search finds " ++
            "a terminal external proof, the next action is Lake pin/import/check " ++
              "or a concrete toolchain/license/API/statement-mismatch blocker."

/-! ## C009 public checkbox open gate -/

/--
Completion modes accepted before the public Stage1 checkbox can be closed.

The current artifact has not reached any of these modes for THM-M-1550 as a
full theorem; it only validates the finite-matrix statement boundary.
-/
inductive C009TerminalClosureMode where
  /-- A terminal proof body lives in this repository and validates locally. -/
  | repoLocalProofBody
  /-- A local wrapper over pinned mathlib validates the selected theorem. -/
  | localWrapperOverPinnedMathlib
  /-- A pinned external dependency validates the selected theorem locally. -/
  | pinnedExternalDependency
  deriving DecidableEq, Repr

/--
C009 public checkbox disposition.

The public checkbox must remain open until a terminal closure mode is available
and all leaf ledgers for the selected theorem target are closed.
-/
inductive C009PublicCheckboxDisposition where
  /-- Keep the public checkbox open; terminal closure is not available. -/
  | keepOpen
  /-- Closure is allowed only after terminal validation and leaf closure. -/
  | closeAfterTerminalValidationAndLeafClosure
  deriving DecidableEq, Repr

/-- Current C009 disposition for the public Stage1 checkbox. -/
def c009PublicCheckboxDisposition : C009PublicCheckboxDisposition :=
  C009PublicCheckboxDisposition.keepOpen

/-- Checked witness that the C009 public checkbox remains open. -/
theorem c009PublicCheckboxDisposition_eq :
    c009PublicCheckboxDisposition =
      C009PublicCheckboxDisposition.keepOpen :=
  rfl

/-- No terminal closure mode is currently selected for THM-M-1550. -/
def c009TerminalClosureMode? : Option C009TerminalClosureMode :=
  none

/-- Checked witness that C009 has no current terminal closure mode. -/
theorem c009TerminalClosureMode?_eq :
    c009TerminalClosureMode? = none :=
  rfl

/--
C009 terminal-closure precondition for closing the public checkbox.

The gate is intentionally stated as selected terminal data plus terminal status.
This file does not select such data for THM-M-1550.
-/
def C009TerminalClosurePrecondition : Prop :=
  ∃ mode : C009TerminalClosureMode,
    c009TerminalClosureMode? = some mode ∧
      currentStage1BoundaryStatus =
        Stage1BoundaryStatus.terminalTheoremClosed

/--
C009 open gate recorded in Lean.

This certifies only the open/not-completed state: the current boundary status is
finite-matrix-only, so no public completion checkbox should be closed from this
artifact.
-/
def C009PublicCheckboxOpenGate : Prop :=
  c009PublicCheckboxDisposition =
      C009PublicCheckboxDisposition.keepOpen ∧
    c009TerminalClosureMode? = none ∧
    currentStage1BoundaryStatus =
      Stage1BoundaryStatus.finiteMatrixStatementBoundary

/-- Checked C009 open gate for the current Stage1 artifact. -/
theorem c009PublicCheckboxOpenGate : C009PublicCheckboxOpenGate := by
  constructor
  · rfl
  · constructor <;> rfl

/-- C009 ledger note for serialized public backfill. -/
def c009PublicBackfillNote : String :=
  "S1-M-209-C009 keeps the public Stage1 checkbox open.  The repo-local Lean " ++
    "artifact validates a finite-matrix Lax-pair boundary and checked " ++
      "conjugation-to-spectral-invariant bridges, but it does not contain a " ++
        "terminal proof body, local wrapper over pinned mathlib, or pinned " ++
          "external dependency for the selected theorem.  Public closure " ++
            "requires terminal validation plus closure of all leaf ledgers."

/-! ## C010 serial public merge gate -/

/--
C010 public merge disposition.

This worker is allowed to prepare the integration payload, but the public
Stage1/todo surfaces must be updated only by an integrator-owned serial patch.
-/
inductive C010PublicMergeDisposition where
  /-- The public backfill payload is ready for a serial integrator patch. -/
  | integrationReadyAwaitingSerialPatch
  /-- The payload has already been merged into the public Stage1 surface. -/
  | mergedByIntegratorSerialPatch
  deriving DecidableEq, Repr

/--
Current C010 disposition: integration-ready, not publicly merged by this
worker.
-/
def c010PublicMergeDisposition : C010PublicMergeDisposition :=
  C010PublicMergeDisposition.integrationReadyAwaitingSerialPatch

/-- Checked witness for the current C010 public merge disposition. -/
theorem c010PublicMergeDisposition_eq :
    c010PublicMergeDisposition =
      C010PublicMergeDisposition.integrationReadyAwaitingSerialPatch :=
  rfl

/--
C010 serial merge gate.

The Lean artifact records that the private theorem tree and leaf-budget ledger
are ready for public backfill, while the public Stage1 surface remains outside
this worker's write scope.
-/
def C010SerialPublicMergeGate : Prop :=
  c010PublicMergeDisposition =
      C010PublicMergeDisposition.integrationReadyAwaitingSerialPatch ∧
    currentStage1BoundaryStatus =
      Stage1BoundaryStatus.finiteMatrixStatementBoundary

/-- Checked C010 gate: serial public integration remains pending. -/
theorem c010SerialPublicMergeGate : C010SerialPublicMergeGate := by
  constructor <;> rfl

/-- Integration-ready public patch tasks prepared by C010. -/
def c010PublicBackfillPatchTasks : List String := [
  "merge the finite-matrix boundary note and validation record",
  "record the selected public target as finite complex matrix Lax flows",
  "record checked local leaves for matrix APIs, conjugation bridges, " ++
    "characteristic-polynomial invariance, and trace-power invariance",
  "keep authenticated external Lean 4 search open until rerun with credentials",
  "keep the public Stage1 checkbox open until terminal validation and all " ++
    "leaf ledgers close",
  "do not mark THM-M-1550 completed with anchor-only evidence or residual " ++
    "repo_local_integration_debt"
]

/-- C010 ledger note for serialized public backfill. -/
def c010PublicBackfillNote : String :=
  "S1-M-209-C010 prepares the private theorem-tree and leaf-budget ledger for " ++
    "an integrator-owned serial public patch only.  The proposed public " ++
      "surface should record the finite-matrix statement boundary, the " ++
        "validation command and pass result, the checked local bridge and " ++
          "spectral-invariant leaves, the selected finite-matrix target, the " ++
            "external-search authentication blocker, and the open completion " ++
              "gate.  This worker does not edit public planning docs and does " ++
                "not claim terminal THM-M-1550 closure."

/-! ## Audit probes retained in the checked file. -/

#check LaxMatrix
#check matrixCommutator
#check LaxEquationOn
#check MatrixSpectrum
#check ConjugatesAt
#check IsospectralOn
#check IsospectralByConjugationOn
#check PoissonLeibniz
#check AlgebraicHamiltonianPoissonModel
#check FiniteMatrixSpectralInvariants
#check canonicalFiniteMatrixSpectralInvariants
#check CharacteristicPolynomialInvariantOn
#check TracePowersInvariantOn
#check FiniteMatrixSpectralConservation
#check ConjugatingEvolutionPackage
#check LaxEquationConjugationBridgeHypotheses
#check LaxPairData
#check StatementShape
#check trace_matrixCommutator_zero
#check spectrum_eq_of_units_conjugate
#check spectrum_eq_of_conjugatesAt
#check isospectralOn_of_conjugates
#check isospectralByConjugationOn_of_laxEquationOn
#check isospectralOn_of_laxEquationOn_with_conjugatingEvolution
#check trace_eq_of_units_conjugate
#check pow_units_conjugate
#check trace_pow_eq_of_units_conjugate
#check charpoly_mul_comm_anchor
#check charpoly_eq_of_units_conjugate
#check charpoly_eq_of_conjugatesAt
#check trace_pow_eq_of_conjugatesAt
#check characteristicPolynomialInvariantOn_of_conjugates
#check tracePowersInvariantOn_of_conjugates
#check finiteMatrixSpectralConservation_of_conjugates
#check conclusion_of_laxPairData
#check spectralConservation_of_laxPairData
#check statementShape_from_laxPairData
#check PublicTheoremTarget
#check selectedPublicTheoremTarget
#check deferredPublicTheoremTargets
#check selectedPublicTheoremTarget_eq
#check selectedPublicTheoremTargetNote
#check Stage1BoundaryStatus
#check currentStage1BoundaryStatus
#check currentStage1BoundaryStatus_eq
#check publicStage1BoundaryNote
#check stage1ValidationCommand
#check parentWorkerValidationDate
#check parentWorkerValidationResult
#check childWorkerValidationDate
#check repoLocalIntegrationDebtGateNote
#check C008ExternalLeanProofDisposition
#check c008ExternalLeanProofSearchTerms
#check c008ExternalLeanProofDisposition
#check c008ExternalLeanProofDisposition_eq
#check C008RepoLocalIntegrationDebtGate
#check c008RepoLocalIntegrationDebtGate
#check c008PublicBackfillNote
#check C009TerminalClosureMode
#check C009PublicCheckboxDisposition
#check c009PublicCheckboxDisposition
#check c009PublicCheckboxDisposition_eq
#check c009TerminalClosureMode?
#check c009TerminalClosureMode?_eq
#check C009TerminalClosurePrecondition
#check C009PublicCheckboxOpenGate
#check c009PublicCheckboxOpenGate
#check c009PublicBackfillNote
#check C010PublicMergeDisposition
#check c010PublicMergeDisposition
#check c010PublicMergeDisposition_eq
#check C010SerialPublicMergeGate
#check c010SerialPublicMergeGate
#check c010PublicBackfillPatchTasks
#check c010PublicBackfillNote
#check spectrum.units_conjugate
#check LieAlgebra.matrix_trace_commutator_zero
#check Matrix.trace_units_conj
#check Matrix.charpoly_mul_comm
#check Units.conj_pow

end S1_M_209
end Stage1
end AwesomeTheorems
