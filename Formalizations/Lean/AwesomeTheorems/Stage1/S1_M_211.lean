import Mathlib.Analysis.Analytic.Constructions
import Mathlib.Analysis.Complex.CauchyIntegral
import Mathlib.Analysis.Normed.Operator.FredholmAlternative
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.SchurComplement

/-!
# S1-M-211 / THM-M-1552: tau functions

This Stage1 artifact records a conservative Lean 4 statement boundary for
tau functions in integrable systems.

The mathematical phrase "the tau function of an integrable system" is not a
single theorem until a hierarchy, time variables, wave/flow data, regularity,
and Hirota or equivalent spectral/variational characterization have been fixed.
The declarations below isolate that boundary.  The repo-local checked content
is limited to small wrappers around mathlib's analytic-function, finite
determinant, and Fredholm-alternative APIs; no terminal KP/Toda/Hirota tau
function theorem is claimed.
-/

noncomputable section

open scoped Topology

universe uTime uPhase uIndex uE uN

namespace AwesomeTheorems.Stage1.S1_M_211

/-- A tau function is represented as a complex-valued function of hierarchy times. -/
abbrev TauFunction (Time : Type uTime) : Type uTime :=
  Time → ℂ

/-- Analyticity predicate for tau functions once the time space is a complex normed space. -/
def TauAnalyticOn
    {Time : Type uTime} [NormedAddCommGroup Time] [NormedSpace ℂ Time]
    (tau : TauFunction Time) (domain : Set Time) : Prop :=
  AnalyticOn ℂ tau domain

/--
Abstract Hirota-side data for an integrable hierarchy.

The bilinear identity is intentionally proposition-valued: a later formalization
must choose concrete differential operators, shifts, residues, or Plucker
coordinates before this can become a terminal theorem.
-/
structure HirotaBilinearDatum (Time : Type uTime) : Type uTime where
  equationLabel : String
  bilinearIdentity : TauFunction Time → Prop
  compatibilityWithHierarchy : TauFunction Time → Prop

/--
An axiomatized integrable-hierarchy model before a tau witness is supplied.

`Time` is the hierarchy-time space, `Phase` is the solution/field phase space,
`Index` indexes flows in the hierarchy, and `E` is an operator space used for
spectral or Fredholm-type anchors.  The proposition fields mark the exact
formalization debt: they should later be replaced by concrete KP/Toda/KdV,
Sato-Grassmannian, Riemann-Hilbert, or Fredholm-determinant interfaces.
-/
structure IntegrableHierarchyModel
    (Time : Type uTime) (Phase : Type uPhase) (Index : Type uIndex) (E : Type uE)
    [TopologicalSpace Time] [NormedAddCommGroup E] [NormedSpace ℂ E] :
    Type (max (max uTime uPhase) (max uIndex uE)) where
  timeDomain : Set Time
  phaseSpaceSet : Set Phase
  flow : Index → Phase → Phase
  spectralOperator : E →L[ℂ] E
  hirotaDatum : HirotaBilinearDatum Time
  hierarchyEquationsWellFormed : Prop
  commutingFlows : Prop
  spectralOrVariationalEncoding : Prop
  tauNormalizationCondition : TauFunction Time → Prop
  solutionReconstruction : TauFunction Time → Phase → Prop

/--
A tau-function witness for an axiomatized integrable hierarchy.

The fields record the expected properties of the tau function: regularity,
Hirota identity, hierarchy compatibility, normalization, and reconstruction of
some solution/phase point.  This is a data boundary, not a proof that every
integrable hierarchy admits such data.
-/
structure TauFunctionWitness
    {Time : Type uTime} {Phase : Type uPhase} {Index : Type uIndex} {E : Type uE}
    [TopologicalSpace Time] [NormedAddCommGroup E] [NormedSpace ℂ E]
    (M : IntegrableHierarchyModel Time Phase Index E) :
    Type (max (max uTime uPhase) (max uIndex uE)) where
  tau : TauFunction Time
  reconstructedPhase : Phase
  tau_continuousOn : ContinuousOn tau M.timeDomain
  hirota_identity : M.hirotaDatum.bilinearIdentity tau
  hierarchy_compatibility : M.hirotaDatum.compatibilityWithHierarchy tau
  normalization : M.tauNormalizationCondition tau
  reconstructs_solution : M.solutionReconstruction tau reconstructedPhase

/-- The model-level proposition that a tau function exists for the hierarchy. -/
def HasTauFunction
    {Time : Type uTime} {Phase : Type uPhase} {Index : Type uIndex} {E : Type uE}
    [TopologicalSpace Time] [NormedAddCommGroup E] [NormedSpace ℂ E]
    (M : IntegrableHierarchyModel Time Phase Index E) : Prop :=
  Nonempty (TauFunctionWitness M)

/--
Concrete tau-function branches considered for the next proof package.

Child task `S1-M-211-C003` selects the KdV finite-soliton determinant branch,
because it can start from finite matrix determinants already present in mathlib.
The other branches remain possible later targets but need more missing
infrastructure before they are good first local proof packages.
-/
inductive TauFunctionBranch where
  | kp
  | toda
  | kdvFiniteSolitonDeterminant
  | satoGrassmannian
  | fredholmDeterminant
  | isomonodromic
  deriving DecidableEq, Repr

/-- Canonical branch choice for the next `S1-M-211` proof package. -/
def chosenTauFunctionBranch : TauFunctionBranch :=
  .kdvFiniteSolitonDeterminant

/-- Checked branch-selection gate for child task `S1-M-211-C003`. -/
theorem chosenTauFunctionBranch_eq_kdvFiniteSolitonDeterminant :
    chosenTauFunctionBranch = TauFunctionBranch.kdvFiniteSolitonDeterminant :=
  rfl

/--
Normalized Stage1 statement shape for THM-M-1552.

For every axiomatized integrable hierarchy with well-formed equations,
commuting flows, and a selected spectral or variational encoding, the intended
theorem asserts the existence of a tau-function witness satisfying the chosen
Hirota, normalization, and reconstruction interfaces.

This statement is deliberately not proved here.  A terminal proof must replace
the abstract proposition fields with concrete formalized KP/Toda/KdV,
Riemann-Hilbert, Sato-Grassmannian, or Fredholm-determinant machinery.
-/
def StatementShape : Prop :=
  ∀ (Time : Type uTime) (Phase : Type uPhase) (Index : Type uIndex) (E : Type uE)
    [TopologicalSpace Time] [NormedAddCommGroup E] [NormedSpace ℂ E],
      ∀ M : IntegrableHierarchyModel Time Phase Index E,
        M.hierarchyEquationsWellFormed →
          M.commutingFlows →
            M.spectralOrVariationalEncoding →
              HasTauFunction M

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (Time : Type uTime) (Phase : Type uPhase) (Index : Type uIndex) (E : Type uE)
      [TopologicalSpace Time] [NormedAddCommGroup E] [NormedSpace ℂ E],
        ∀ M : IntegrableHierarchyModel Time Phase Index E,
          M.hierarchyEquationsWellFormed →
            M.commutingFlows →
              M.spectralOrVariationalEncoding →
                HasTauFunction M) :
    StatementShape.{uTime, uPhase, uIndex, uE} :=
  h

/-- Projection wrapper: a tau witness exposes a continuous tau function on the time domain. -/
theorem TauFunctionWitness.continuousOn_tau
    {Time : Type uTime} {Phase : Type uPhase} {Index : Type uIndex} {E : Type uE}
    [TopologicalSpace Time] [NormedAddCommGroup E] [NormedSpace ℂ E]
    {M : IntegrableHierarchyModel Time Phase Index E} (W : TauFunctionWitness M) :
    ContinuousOn W.tau M.timeDomain :=
  W.tau_continuousOn

/-- Projection wrapper: a tau witness satisfies the selected Hirota bilinear identity. -/
theorem TauFunctionWitness.satisfies_hirota
    {Time : Type uTime} {Phase : Type uPhase} {Index : Type uIndex} {E : Type uE}
    [TopologicalSpace Time] [NormedAddCommGroup E] [NormedSpace ℂ E]
    {M : IntegrableHierarchyModel Time Phase Index E} (W : TauFunctionWitness M) :
    M.hirotaDatum.bilinearIdentity W.tau :=
  W.hirota_identity

/-- Projection wrapper: a tau witness is compatible with the hierarchy interface. -/
theorem TauFunctionWitness.compatible_with_hierarchy
    {Time : Type uTime} {Phase : Type uPhase} {Index : Type uIndex} {E : Type uE}
    [TopologicalSpace Time] [NormedAddCommGroup E] [NormedSpace ℂ E]
    {M : IntegrableHierarchyModel Time Phase Index E} (W : TauFunctionWitness M) :
    M.hirotaDatum.compatibilityWithHierarchy W.tau :=
  W.hierarchy_compatibility

/-- Projection wrapper: a tau witness reconstructs its selected phase point. -/
theorem TauFunctionWitness.reconstructs
    {Time : Type uTime} {Phase : Type uPhase} {Index : Type uIndex} {E : Type uE}
    [TopologicalSpace Time] [NormedAddCommGroup E] [NormedSpace ℂ E]
    {M : IntegrableHierarchyModel Time Phase Index E} (W : TauFunctionWitness M) :
    M.solutionReconstruction W.tau W.reconstructedPhase :=
  W.reconstructs_solution

/-- A finite determinant tau candidate attached to a matrix-valued function. -/
def finiteDeterminantTau
    (Time : Type uTime) (n : Type uN) [Fintype n] [DecidableEq n]
    (A : Time → Matrix n n ℂ) : TauFunction Time :=
  fun t => (A t).det

/--
Concrete time space for the selected KdV finite-soliton determinant branch.

This first branch uses the two visible KdV variables, spatial position and
evolution time.  Higher hierarchy times are deliberately left for a later KP or
full KdV-hierarchy package.
-/
abbrev KdVFiniteSolitonTime : Type :=
  ℂ × ℂ

/--
Finite determinant tau candidate for the selected KdV finite-soliton branch.

The real soliton package must later specialize `A` to the standard finite-rank
matrix built from soliton parameters and prove the Hirota/KdV identities.  This
definition only fixes the concrete branch and determinant-shaped candidate.
-/
def kdvFiniteSolitonDeterminantTau
    (n : Type uN) [Fintype n] [DecidableEq n]
    (A : KdVFiniteSolitonTime → Matrix n n ℂ) :
    TauFunction KdVFiniteSolitonTime :=
  finiteDeterminantTau KdVFiniteSolitonTime n A

/-- Checked KdV-branch determinant anchor: the identity-matrix candidate is constantly one. -/
theorem kdvFiniteSolitonDeterminantTau_one
    (n : Type uN) [Fintype n] [DecidableEq n] (t : KdVFiniteSolitonTime) :
    kdvFiniteSolitonDeterminantTau n (fun _ => (1 : Matrix n n ℂ)) t = 1 :=
  by
    simp [kdvFiniteSolitonDeterminantTau, finiteDeterminantTau]

/-- Spatial direction for the selected KdV finite-soliton branch. -/
def kdvSpaceDirection : KdVFiniteSolitonTime :=
  (1, 0)

/-- Evolution-time direction for the selected KdV finite-soliton branch. -/
def kdvEvolutionDirection : KdVFiniteSolitonTime :=
  (0, 1)

/--
Directional derivative used to spell concrete Hirota operators for the
selected KdV finite-soliton determinant branch.
-/
def kdvDirectionalDerivative
    (v : KdVFiniteSolitonTime) (tau : TauFunction KdVFiniteSolitonTime) :
    TauFunction KdVFiniteSolitonTime :=
  fun z => fderiv ℂ tau z v

/-- Iterated directional derivative along a fixed KdV time direction. -/
def kdvIteratedDirectionalDerivative
    (order : ℕ) (v : KdVFiniteSolitonTime) (tau : TauFunction KdVFiniteSolitonTime) :
    TauFunction KdVFiniteSolitonTime :=
  Nat.rec tau (fun _ prev => kdvDirectionalDerivative v prev) order

/-- Mixed `x`/`t` directional derivative used in the KdV Hirota operator. -/
def kdvMixedDirectionalDerivative
    (xOrder tOrder : ℕ) (tau : TauFunction KdVFiniteSolitonTime) :
    TauFunction KdVFiniteSolitonTime :=
  kdvIteratedDirectionalDerivative tOrder kdvEvolutionDirection
    (kdvIteratedDirectionalDerivative xOrder kdvSpaceDirection tau)

/--
Concrete Hirota bilinear differential operator
`D_x^xOrder D_t^tOrder f · g` for the selected KdV branch.

This is a definition only.  Later proof packages must add differentiability
and finite-soliton determinant lemmas strong enough to prove the KdV bilinear
identity.
-/
def kdvHirotaD
    (xOrder tOrder : ℕ)
    (f g : TauFunction KdVFiniteSolitonTime) :
    TauFunction KdVFiniteSolitonTime :=
  fun z =>
    ∑ i ∈ Finset.range (xOrder + 1),
      ∑ j ∈ Finset.range (tOrder + 1),
        (((-1 : ℂ) ^ (i + j)) * (Nat.choose xOrder i : ℂ) *
            (Nat.choose tOrder j : ℂ)) *
          kdvMixedDirectionalDerivative (xOrder - i) (tOrder - j) f z *
            kdvMixedDirectionalDerivative i j g z

/-- The standard KdV finite-soliton Hirota combination `(D_x^4 + D_x D_t) τ · τ`. -/
def kdvFiniteSolitonHirotaCombination
    (tau : TauFunction KdVFiniteSolitonTime) :
    TauFunction KdVFiniteSolitonTime :=
  fun z => kdvHirotaD 4 0 tau tau z + kdvHirotaD 1 1 tau tau z

/-- Concrete proposition for the selected branch's KdV Hirota identity. -/
def KdVFiniteSolitonHirotaIdentity
    (tau : TauFunction KdVFiniteSolitonTime) : Prop :=
  ∀ z, kdvFiniteSolitonHirotaCombination tau z = 0

/-- Zero-order iterated directional derivative is the original tau function. -/
theorem kdvIteratedDirectionalDerivative_zero
    (v : KdVFiniteSolitonTime) (tau : TauFunction KdVFiniteSolitonTime) :
    kdvIteratedDirectionalDerivative 0 v tau = tau :=
  rfl

/-- Mixed derivative of order `(0, 0)` is the original tau function. -/
theorem kdvMixedDirectionalDerivative_zero_zero
    (tau : TauFunction KdVFiniteSolitonTime) :
    kdvMixedDirectionalDerivative 0 0 tau = tau :=
  rfl

/-- The zero-order Hirota operator is ordinary pointwise multiplication. -/
theorem kdvHirotaD_zero_zero
    (f g : TauFunction KdVFiniteSolitonTime) (z : KdVFiniteSolitonTime) :
    kdvHirotaD 0 0 f g z = f z * g z := by
  simp [kdvHirotaD, kdvMixedDirectionalDerivative, kdvIteratedDirectionalDerivative]

/-- Apply-form wrapper for the finite determinant tau candidate. -/
theorem kdvFiniteSolitonDeterminantTau_apply
    (n : Type uN) [Fintype n] [DecidableEq n]
    (A : KdVFiniteSolitonTime → Matrix n n ℂ) (z : KdVFiniteSolitonTime) :
    kdvFiniteSolitonDeterminantTau n A z = (A z).det :=
  rfl

/-- Determinant tau candidates are extensionally equal when their matrices agree. -/
theorem kdvFiniteSolitonDeterminantTau_congr
    (n : Type uN) [Fintype n] [DecidableEq n]
    {A B : KdVFiniteSolitonTime → Matrix n n ℂ}
    (h : ∀ z, A z = B z) :
    kdvFiniteSolitonDeterminantTau n A = kdvFiniteSolitonDeterminantTau n B := by
  funext z
  simp [kdvFiniteSolitonDeterminantTau, finiteDeterminantTau, h z]

/-- Analytic KdV-branch tau functions are continuous on the same domain. -/
theorem kdvTau_continuousOn_of_analyticOn
    (tau : TauFunction KdVFiniteSolitonTime) (domain : Set KdVFiniteSolitonTime)
    (h : TauAnalyticOn tau domain) :
    ContinuousOn tau domain := by
  simpa [TauAnalyticOn] using h.continuousOn

/--
Regularity wrapper for determinant-shaped KdV finite-soliton tau candidates:
once the determinant candidate has been proved analytic on a domain, continuity
is available immediately from mathlib's analytic substrate.
-/
theorem kdvFiniteSolitonDeterminantTau_continuousOn_of_analyticOn
    (n : Type uN) [Fintype n] [DecidableEq n]
    (A : KdVFiniteSolitonTime → Matrix n n ℂ) (domain : Set KdVFiniteSolitonTime)
    (h : TauAnalyticOn (kdvFiniteSolitonDeterminantTau n A) domain) :
    ContinuousOn (kdvFiniteSolitonDeterminantTau n A) domain :=
  kdvTau_continuousOn_of_analyticOn (kdvFiniteSolitonDeterminantTau n A) domain h

/--
Integration-ready local proof-leaf split for `S1-M-211/P5`.

These are proof obligations for the selected KdV finite-soliton determinant
branch.  They are deliberately recorded as open leaves; only the definitional,
determinant-congruence, and analytic-to-continuity wrappers above are locally
checked in this file.
-/
def kdvFiniteSolitonLocalProofLeaves : List String := [
  "P5.L01 checked: define KdVFiniteSolitonTime as C x C for the selected branch.",
  "P5.L02 checked: define kdvSpaceDirection and kdvEvolutionDirection.",
  "P5.L03 checked: define kdvDirectionalDerivative using fderiv over C.",
  "P5.L04 checked: define kdvIteratedDirectionalDerivative.",
  "P5.L05 checked: define kdvMixedDirectionalDerivative for x/t orders.",
  "P5.L06 checked: define kdvHirotaD by the finite binomial Hirota sum.",
  "P5.L07 checked: define kdvFiniteSolitonHirotaCombination as D_x^4 + D_x D_t.",
  "P5.L08 checked: define KdVFiniteSolitonHirotaIdentity.",
  "P5.L09 checked: prove kdvIteratedDirectionalDerivative_zero.",
  "P5.L10 checked: prove kdvMixedDirectionalDerivative_zero_zero.",
  "P5.L11 checked: prove kdvHirotaD_zero_zero.",
  "P5.L12 checked: prove kdvFiniteSolitonDeterminantTau_apply.",
  "P5.L13 checked: prove kdvFiniteSolitonDeterminantTau_congr.",
  "P5.L14 checked: prove kdvTau_continuousOn_of_analyticOn.",
  "P5.L15 checked: prove kdvFiniteSolitonDeterminantTau_continuousOn_of_analyticOn.",
  "P5.L16 open: choose finite-soliton parameter type and nondegeneracy assumptions.",
  "P5.L17 open: define the concrete finite-soliton matrix entries.",
  "P5.L18 open: prove entrywise analyticity of the finite-soliton matrix.",
  "P5.L19 open: prove analyticity of the determinant tau candidate.",
  "P5.L20 open: prove closed forms for the directional derivatives of entries.",
  "P5.L21 open: prove determinant derivative/Jacobi-formula lemmas required by Hirota.",
  "P5.L22 open: prove the finite determinant algebra identity implying D_x^4 + D_x D_t.",
  "P5.L23 open: prove KdVFiniteSolitonHirotaIdentity for the determinant candidate.",
  "P5.L24 open: define the KdV field reconstructed from tau.",
  "P5.L25 open: prove reconstruction satisfies the selected KdV equation.",
  "P5.L26 open: split any leaf above that exceeds 100 local Lean proof steps."
]

/-- Integration-ready rationale for the selected branch. -/
def chosenTauFunctionBranchRationale : String :=
  "Choose the KdV finite-soliton determinant branch: it is the narrowest " ++
  "tau-function package that can start from repo-local checked finite " ++
  "matrix determinant anchors, while Fredholm determinant, Sato " ++
  "Grassmannian, full KP/Toda, and isomonodromic branches still need " ++
  "larger missing APIs before a local proof package can close."

/-- Checked finite determinant anchor: the identity-matrix tau is constantly one. -/
theorem finiteDeterminantTau_one
    (Time : Type uTime) (n : Type uN) [Fintype n] [DecidableEq n] (t : Time) :
    finiteDeterminantTau Time n (fun _ => (1 : Matrix n n ℂ)) t = 1 := by
  simp [finiteDeterminantTau]

/--
Checked finite determinant anchor: the Weinstein-Aronszajn identity available
as `Matrix.det_one_add_mul_comm` in mathlib's Schur-complement module.
-/
theorem determinant_one_add_mul_comm_anchor
    (m : Type uIndex) (n : Type uN) [Fintype m] [DecidableEq m] [Fintype n] [DecidableEq n]
    (A : Matrix m n ℂ) (B : Matrix n m ℂ) :
    (1 + A * B).det = (1 + B * A).det :=
  Matrix.det_one_add_mul_comm A B

/-- Checked analytic anchor: constant tau functions are analytic on every domain. -/
theorem constant_tau_analyticOn
    {Time : Type uTime} [NormedAddCommGroup Time] [NormedSpace ℂ Time]
    (c : ℂ) (domain : Set Time) :
    TauAnalyticOn (fun _ : Time => c) domain := by
  simpa [TauAnalyticOn] using
    (analyticOn_const (𝕜 := ℂ) (E := Time) (F := ℂ) (v := c) (s := domain))

/--
Checked operator-theoretic anchor: mathlib's Fredholm alternative for compact
operators.  This is adjacent to Fredholm-determinant tau constructions but is
not itself a tau-function theorem.
-/
theorem compactOperator_fredholmAlternative_anchor
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℂ E] [CompleteSpace E]
    {T : E →L[ℂ] E} (hT : IsCompactOperator T) {μ : ℂ} (hμ : μ ≠ 0) :
    Module.End.HasEigenvalue (T : Module.End ℂ E) μ ∨ μ ∈ resolventSet ℂ T :=
  IsCompactOperator.hasEigenvalue_or_mem_resolventSet hT hμ

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Analytic.Basic",
  "Mathlib.Analysis.Analytic.Constructions",
  "Mathlib.Analysis.Complex.CauchyIntegral",
  "Mathlib.Analysis.Normed.Operator.FredholmAlternative",
  "Mathlib.Analysis.Normed.Operator.Compact",
  "Mathlib.Analysis.Fourier.AddCircle",
  "Mathlib.Analysis.Fourier.Convolution",
  "Mathlib.Analysis.Distribution.FourierMultiplier",
  "Mathlib.LinearAlgebra.Matrix.Determinant.Basic",
  "Mathlib.LinearAlgebra.Matrix.SchurComplement"
]

/-- Checked declaration names used or audited for the Stage1 tau-function boundary. -/
def mathlibAnchorNames : List String := [
  "AnalyticOn",
  "analyticOn_const",
  "ContinuousOn",
  "Matrix.det",
  "Matrix.det_one",
  "Matrix.det_mul",
  "Matrix.det_one_add_mul_comm",
  "IsCompactOperator",
  "IsCompactOperator.hasEigenvalue_or_mem_resolventSet",
  "resolventSet",
  "spectrum",
  "fourierBasis"
]

/-- Integration-ready public anchor-audit rows for child task `S1-M-211-C002`. -/
def requiredMathlibAnchorAuditRows : List String := [
  "AnalyticOn | Mathlib.Analysis.Analytic.Basic | def AnalyticOn (f : E -> F) (s : Set E) : Prop | pinned mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95 | checked by local TauAnalyticOn boundary",
  "analyticOn_const | Mathlib.Analysis.Analytic.Constructions | theorem analyticOn_const {v : F} {s : Set E} : AnalyticOn k (fun _ => v) s | pinned mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95 | checked by constant_tau_analyticOn",
  "Matrix.det_one | Mathlib.LinearAlgebra.Matrix.Determinant.Basic | theorem Matrix.det_one : det (1 : Matrix n n R) = 1 | pinned mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95 | checked by finiteDeterminantTau_one",
  "Matrix.det_one_add_mul_comm | Mathlib.LinearAlgebra.Matrix.SchurComplement | theorem Matrix.det_one_add_mul_comm (A : Matrix m n alpha) (B : Matrix n m alpha) : det (1 + A * B) = det (1 + B * A) | pinned mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95 | checked by determinant_one_add_mul_comm_anchor",
  "IsCompactOperator.hasEigenvalue_or_mem_resolventSet | Mathlib.Analysis.Normed.Operator.FredholmAlternative | theorem IsCompactOperator.hasEigenvalue_or_mem_resolventSet (hT : IsCompactOperator T) (hmu : mu != 0) : Module.End.HasEigenvalue (T : Module.End k X) mu or mu in resolventSet k T | pinned mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95 | checked by compactOperator_fredholmAlternative_anchor"
]

/-- Search terms that did not locate a terminal tau-function theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "tau function",
  "TauFunction",
  "Hirota",
  "KP hierarchy",
  "KdV tau",
  "Toda tau",
  "Sato Grassmannian",
  "Fredholm determinant tau",
  "isomonodromic tau",
  "integrable systems tau"
]

/-- Primary-source anchors and external-audit notes for this Stage1 slot. -/
def primarySourceAnchors : List String := [
  "mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "https://raw.githubusercontent.com/leanprover-community/mathlib4/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Analysis/Analytic/Basic.lean",
  "https://raw.githubusercontent.com/leanprover-community/mathlib4/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Analysis/Analytic/Constructions.lean",
  "https://raw.githubusercontent.com/leanprover-community/mathlib4/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Analysis/Normed/Operator/FredholmAlternative.lean",
  "https://raw.githubusercontent.com/leanprover-community/mathlib4/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/LinearAlgebra/Matrix/Determinant/Basic.lean",
  "GitHub primary-source repository search on 2026-04-30 for \"tau function\" \"Lean 4\" returned no matching repositories before rate limiting; no external Lean 4 tau-function proof was added to this repo-local closure."
]

/-- P4 integration gate: no closed external tau-function proof is currently established. -/
def externalLeanProofIntegrationGate : List String := [
  "P4 status: no closed external Lean 4 proof target for the tau-function theorem is established in this repository.",
  "Authenticated GitHub code search remains blocked until a GitHub session or token is supplied to the local process.",
  "Because no external proof target is established, there is no dependency to pin, import, and check in Lake in this child.",
  "The terminal theorem must remain not_repo_local_closed / formalization_debt; it must not be marked completed from anchor-only evidence.",
  "If a later authenticated audit finds a closed external proof, the next step is a pinned dependency, vendored proof body, or a concrete Lake/toolchain/license/API blocker before any completion claim."
]

/-- P6 public-doc synchronization gate: private ledgers are not public completion surfaces. -/
def publicDocumentationSynchronizationGate : List String := [
  "P6 status: public planning docs must be synchronized only by the serial integrator.",
  "Private child ledgers under .cron/results are runtime evidence, not public completion surfaces.",
  "Docs/Stage1_Blueprint.md, Docs/todos_20260430.md, and README.md must not point completion status at this private worker ledger.",
  "An integrator may merge the backfill proposals from child ledgers into the public blueprint/todo surface after checking consistency.",
  "The terminal tau-function theorem remains open unless the repo-local Lean validation and every M0387 completion gate are explicitly satisfied."
]

/-! ## Audit probes -/

#check TauFunction
#check TauAnalyticOn
#check HirotaBilinearDatum
#check IntegrableHierarchyModel
#check TauFunctionWitness
#check HasTauFunction
#check TauFunctionBranch
#check chosenTauFunctionBranch
#check chosenTauFunctionBranch_eq_kdvFiniteSolitonDeterminant
#check StatementShape
#check StatementShape.intro
#check TauFunctionWitness.satisfies_hirota
#check KdVFiniteSolitonTime
#check kdvFiniteSolitonDeterminantTau
#check kdvFiniteSolitonDeterminantTau_one
#check kdvDirectionalDerivative
#check kdvMixedDirectionalDerivative
#check kdvHirotaD
#check kdvFiniteSolitonHirotaCombination
#check KdVFiniteSolitonHirotaIdentity
#check kdvHirotaD_zero_zero
#check kdvFiniteSolitonDeterminantTau_congr
#check kdvFiniteSolitonDeterminantTau_continuousOn_of_analyticOn
#check kdvFiniteSolitonLocalProofLeaves
#check finiteDeterminantTau_one
#check determinant_one_add_mul_comm_anchor
#check constant_tau_analyticOn
#check compactOperator_fredholmAlternative_anchor
#check IsCompactOperator.hasEigenvalue_or_mem_resolventSet
#check Matrix.det_one
#check Matrix.det_one_add_mul_comm
#check analyticOn_const
#check externalLeanProofIntegrationGate
#check publicDocumentationSynchronizationGate

end AwesomeTheorems.Stage1.S1_M_211
