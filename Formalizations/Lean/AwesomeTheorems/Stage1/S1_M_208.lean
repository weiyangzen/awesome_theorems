import Mathlib.Algebra.Algebra.Spectrum.Basic
import Mathlib.Algebra.Algebra.Spectrum.Quasispectrum
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Distribution.SchwartzSpace.Fourier
import Mathlib.Analysis.Fourier.FourierTransform
import Mathlib.Analysis.Fourier.Inversion
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.LinearPMap
import Mathlib.Analysis.InnerProductSpace.Spectrum

/-!
# S1-M-208 / THM-M-1549: Inverse scattering transform for KdV

This Stage1 artifact records a conservative Lean 4 statement boundary for the
claim that the inverse scattering transform solves the Korteweg--de Vries
equation.

The repo-local checked content below does not assert a terminal inverse
scattering theorem.  It freezes:

* a derivative-level KdV residual on functions `u : ℝ → ℝ → ℝ`;
* an abstract scattering-data carrier;
* an abstract forward-scattering / spectral-evolution / inverse-scattering
  interface;
* small checked wrappers projecting the KdV and initial-condition conclusions
  from such an interface; and
* a constant-solution sanity check for the residual.

No spectral theory of one-dimensional Schrödinger operators, Marchenko equation,
soliton reconstruction, or full inverse-scattering proof is claimed here.
-/

noncomputable section

namespace AwesomeTheorems.Stage1.S1_M_208

universe u

/-- Spatial first derivative for a KdV field `u x t`. -/
def spatialDeriv (u : ℝ → ℝ → ℝ) (x t : ℝ) : ℝ :=
  deriv (fun y : ℝ => u y t) x

/-- Spatial second derivative for a KdV field `u x t`. -/
def spatialSecondDeriv (u : ℝ → ℝ → ℝ) (x t : ℝ) : ℝ :=
  deriv (fun y : ℝ => spatialDeriv u y t) x

/-- Spatial third derivative for a KdV field `u x t`. -/
def spatialThirdDeriv (u : ℝ → ℝ → ℝ) (x t : ℝ) : ℝ :=
  deriv (fun y : ℝ => spatialSecondDeriv u y t) x

/-- Time derivative for a KdV field `u x t`. -/
def timeDeriv (u : ℝ → ℝ → ℝ) (x t : ℝ) : ℝ :=
  deriv (fun τ : ℝ => u x τ) t

/--
The normalized KdV residual

`u_t + 6 u u_x + u_xxx`.

The sign and coefficient convention is the standard `+ 6 u u_x + u_xxx = 0`
form.  Other KdV conventions should be represented by a separate residual
definition rather than silently reusing this one.
-/
def KdVResidual (u : ℝ → ℝ → ℝ) (x t : ℝ) : ℝ :=
  timeDeriv u x t + 6 * u x t * spatialDeriv u x t + spatialThirdDeriv u x t

/-- A real-valued field solves the normalized KdV equation pointwise. -/
def SolvesKdV (u : ℝ → ℝ → ℝ) : Prop :=
  ∀ x t : ℝ, KdVResidual u x t = 0

/-- The Cauchy initial condition `u(x, 0) = u₀(x)`. -/
def InitialCondition (u : ℝ → ℝ → ℝ) (u₀ : ℝ → ℝ) : Prop :=
  ∀ x : ℝ, u x 0 = u₀ x

/--
Minimal scattering data used by the Stage1 boundary.

This is intentionally not a full analytic definition of scattering data for the
Schrödinger operator.  It records the formal slots normally occupied by the
reflection coefficient, discrete spectrum, and norming constants.
-/
structure ScatteringData where
  reflectionCoefficient : ℝ → ℂ
  discreteSpectrum : Set ℝ
  normingConstant : ℝ → ℂ

/-- Bounded Hilbert-space operators provide a low-risk spectral API anchor. -/
abbrev HilbertOperator
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H] : Type u :=
  H →L[ℂ] H

/-- Spectrum of a bounded Hilbert-space operator, via mathlib's algebra-spectrum API. -/
def OperatorSpectrum
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (T : HilbertOperator H) : Set ℂ :=
  spectrum ℂ T

/--
A Stage1 model of the inverse-scattering pipeline.

The fields `reconstruction_solves_kdv` and `reconstruction_matches_initial`
are the mathematical proof obligations for a later formalization or pinned
dependency.  Keeping them as fields prevents this file from pretending that the
Marchenko/inverse-scattering proof is already available in the repo-local Lean
closure.
-/
structure InverseScatteringModel where
  AdmissiblePotential : (ℝ → ℝ) → Prop
  ScatteringDataWellFormed : ScatteringData → Prop
  ForwardScattering : (ℝ → ℝ) → ScatteringData
  ScatteringEvolution : ScatteringData → ℝ → ScatteringData
  InverseScattering : ScatteringData → ℝ → ℝ
  forwardScattering_wellFormed :
    ∀ u₀ : ℝ → ℝ, AdmissiblePotential u₀ →
      ScatteringDataWellFormed (ForwardScattering u₀)
  scatteringEvolution_wellFormed :
    ∀ (S : ScatteringData) (t : ℝ), ScatteringDataWellFormed S →
      ScatteringDataWellFormed (ScatteringEvolution S t)
  reconstruction_solves_kdv :
    ∀ u₀ : ℝ → ℝ, AdmissiblePotential u₀ →
      SolvesKdV (fun x t : ℝ =>
        InverseScattering (ScatteringEvolution (ForwardScattering u₀) t) x)
  reconstruction_matches_initial :
    ∀ u₀ : ℝ → ℝ, AdmissiblePotential u₀ →
      InitialCondition
        (fun x t : ℝ => InverseScattering (ScatteringEvolution (ForwardScattering u₀) t) x)
        u₀

/-- The solution reconstructed by a declared inverse-scattering model. -/
def ReconstructedSolution (M : InverseScatteringModel) (u₀ : ℝ → ℝ) :
    ℝ → ℝ → ℝ :=
  fun x t : ℝ => M.InverseScattering (M.ScatteringEvolution (M.ForwardScattering u₀) t) x

/-- The formal conclusion expected from the inverse-scattering solution method. -/
def InverseScatteringConclusion (M : InverseScatteringModel) (u₀ : ℝ → ℝ) : Prop :=
  SolvesKdV (ReconstructedSolution M u₀) ∧
    InitialCondition (ReconstructedSolution M u₀) u₀

/--
Stage1 normalized statement shape.

For any declared inverse-scattering model and any admissible initial potential,
the reconstructed solution solves KdV and has the prescribed initial condition.
This is a precise formalization boundary, not a proof that such a model has
been constructed from mathlib's current analysis and spectral APIs.
-/
def StatementShape : Prop :=
  ∀ (M : InverseScatteringModel) (u₀ : ℝ → ℝ),
    M.AdmissiblePotential u₀ → InverseScatteringConclusion M u₀

/-- The statement shape unfolds to the expected quantified implication. -/
theorem statementShape_iff_forall_model :
    StatementShape ↔
      ∀ (M : InverseScatteringModel) (u₀ : ℝ → ℝ),
        M.AdmissiblePotential u₀ → InverseScatteringConclusion M u₀ :=
  Iff.rfl

/--
If a future package supplies the inverse-scattering model fields, the repo-local
wrapper can project the KdV and initial-condition conclusions.
-/
theorem statementShape_from_model_fields : StatementShape := by
  intro M u₀ hAdmissible
  exact ⟨M.reconstruction_solves_kdv u₀ hAdmissible,
    M.reconstruction_matches_initial u₀ hAdmissible⟩

/-- Project the KdV branch from the normalized conclusion. -/
theorem InverseScatteringConclusion.solvesKdV
    {M : InverseScatteringModel} {u₀ : ℝ → ℝ}
    (h : InverseScatteringConclusion M u₀) :
    SolvesKdV (ReconstructedSolution M u₀) :=
  h.1

/-- Project the initial-condition branch from the normalized conclusion. -/
theorem InverseScatteringConclusion.initialCondition
    {M : InverseScatteringModel} {u₀ : ℝ → ℝ}
    (h : InverseScatteringConclusion M u₀) :
    InitialCondition (ReconstructedSolution M u₀) u₀ :=
  h.2

/-- The operator spectrum definition is exactly mathlib's `spectrum` for endomorphisms. -/
theorem operatorSpectrum_eq_spectrum
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (T : HilbertOperator H) :
    OperatorSpectrum T = spectrum ℂ T :=
  rfl

/-- Constant fields solve the normalized KdV residual. -/
theorem constant_solvesKdV (c : ℝ) :
    SolvesKdV (fun _ _ : ℝ => c) := by
  intro x t
  simp [KdVResidual, timeDeriv, spatialDeriv, spatialSecondDeriv, spatialThirdDeriv]

/-- The zero field has zero initial condition. -/
theorem zero_initialCondition :
    InitialCondition (fun _ _ : ℝ => 0) (fun _ : ℝ => 0) := by
  intro x
  rfl

/-- The zero field is a checked special solution of the normalized KdV equation. -/
theorem zero_solvesKdV :
    SolvesKdV (fun _ _ : ℝ => 0) := by
  simpa using constant_solvesKdV 0

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Calculus.Deriv.Basic",
  "Mathlib.Algebra.Algebra.Spectrum.Basic",
  "Mathlib.Algebra.Algebra.Spectrum.Quasispectrum",
  "Mathlib.Analysis.InnerProductSpace.Basic",
  "Mathlib.Analysis.InnerProductSpace.Spectrum",
  "Mathlib.Analysis.Fourier.FourierTransform",
  "Mathlib.Analysis.Fourier.Inversion",
  "Mathlib.Analysis.Distribution.SchwartzSpace.Fourier"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "deriv",
  "KdVResidual",
  "SolvesKdV",
  "InitialCondition",
  "spectrum",
  "OperatorSpectrum",
  "HilbertOperator"
]

/-- Primary-source anchors recorded for this Stage1 audit. -/
def primarySourceAnchors : List String := [
  "mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Analysis/Calculus/Deriv/Basic.lean",
  "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Algebra/Algebra/Spectrum/Basic.lean",
  "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Analysis/Fourier/FourierTransform.lean",
  "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Analysis/Distribution/SchwartzSpace/Fourier.lean"
]

/-- Machine-proof debt classification for the full inverse-scattering claim. -/
def machineProofDebtClass : String := "formalization_debt"

/--
Repo-local integration gate for this slot.

No external Lean 4 proof of the full KdV inverse-scattering theorem is imported
or pinned here, so this module remains a statement-shape/wrapper artifact and is
not a completed theorem.
-/
def repoLocalIntegrationGate : String :=
  "no completed state; no external full Lean 4 proof pinned in this repo"

/--
Search terms used to separate available generic mathlib infrastructure from a
terminal inverse-scattering formalization.
-/
def boundarySearchTerms : List String := [
  "KdV",
  "Korteweg",
  "de Vries",
  "inverse scattering",
  "scattering transform",
  "Schrodinger",
  "Schrödinger",
  "Marchenko",
  "Gel'fand-Levitan",
  "Lax pair",
  "soliton"
]

/-! ## C002 public mathlib-audit record -/

/-- Pinned mathlib revision audited for the C002 public mathlib note. -/
def c002MathlibAuditRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Infrastructure areas present in the pinned mathlib revision and relevant to a
future KdV inverse-scattering formalization.
-/
def c002MathlibInfrastructureAreas : List String := [
  "calculus",
  "Fourier",
  "Schwartz/distribution",
  "Hilbert-space",
  "spectrum"
]

/-- Imported mathlib modules witnessing the C002 infrastructure buckets. -/
def c002MathlibInfrastructureModulePaths : List String := [
  "Mathlib.Analysis.Calculus.Deriv.Basic",
  "Mathlib.Analysis.Fourier.FourierTransform",
  "Mathlib.Analysis.Fourier.Inversion",
  "Mathlib.Analysis.Distribution.SchwartzSpace.Fourier",
  "Mathlib.Analysis.InnerProductSpace.Basic",
  "Mathlib.Analysis.InnerProductSpace.Spectrum",
  "Mathlib.Algebra.Algebra.Spectrum.Basic",
  "Mathlib.Algebra.Algebra.Spectrum.Quasispectrum"
]

/--
Exact local mathlib search terms requested by C002 with no terminal KdV
inverse-scattering matches in the repo-local pinned mathlib audit.
-/
def c002NoLocalMathlibMatchTerms : List String := [
  "KdV",
  "Korteweg",
  "inverse scattering",
  "Marchenko",
  "Schrodinger",
  "soliton"
]

/-- Checked record of the C002 pinned mathlib revision. -/
theorem c002MathlibAuditRevision_eq :
    c002MathlibAuditRevision =
      "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- Checked record of the C002 positive infrastructure audit buckets. -/
theorem c002MathlibInfrastructureAreas_eq :
    c002MathlibInfrastructureAreas =
      ["calculus", "Fourier", "Schwartz/distribution", "Hilbert-space", "spectrum"] :=
  rfl

/-- Checked record of the C002 negative local-match audit terms. -/
theorem c002NoLocalMathlibMatchTerms_eq :
    c002NoLocalMathlibMatchTerms =
      ["KdV", "Korteweg", "inverse scattering", "Marchenko", "Schrodinger", "soliton"] :=
  rfl

/-! ## C003 first concrete formal target decision -/

/--
Concrete first-target options considered by child task `S1-M-208-C003`.

The choice below is a formalization-route decision, not a completion claim for
the inverse-scattering theorem.
-/
inductive C003FormalTargetOption where
  | schwartzPotentialStatement
  | weakDistributionalKdVStatement
  | oneSolitonSpecialCase
  | reflectionlessFiniteSolitonPackage
  deriving DecidableEq, Repr

/--
C003 target selection: first stabilize the Schwartz-potential statement.

This is the narrowest target aligned with the imported `SchwartzMap` /
Fourier/distribution infrastructure and with the classical IST domain of
rapidly decaying real-line potentials.  It avoids pretending that the current
repo-local closure already supplies distributional KdV, explicit soliton
calculus, Marchenko reconstruction, or reflectionless finite-soliton spectral
data.
-/
def c003FirstConcreteFormalTarget : C003FormalTargetOption :=
  .schwartzPotentialStatement

/-- Real-line Schwartz potentials for the selected first formal target. -/
abbrev KdVSchwartzPotential : Type :=
  SchwartzMap ℝ ℝ

/-- Coerce a Schwartz potential to the pointwise initial profile used by `InitialCondition`. -/
def SchwartzPotentialInitialProfile (q : KdVSchwartzPotential) : ℝ → ℝ :=
  fun x : ℝ => q x

/--
Selected C003 statement boundary.

For a declared inverse-scattering model, Schwartz initial potentials should
lead to the same KdV and initial-trace conclusion as the abstract Stage1 model.
This definition intentionally leaves admissibility, forward scattering,
spectral evolution, and inverse reconstruction as model obligations.
-/
def SchwartzPotentialStatementTarget : Prop :=
  ∀ (M : InverseScatteringModel) (q : KdVSchwartzPotential),
    M.AdmissiblePotential (SchwartzPotentialInitialProfile q) →
      InverseScatteringConclusion M (SchwartzPotentialInitialProfile q)

/-- C003 rationale intended for public backfill after serialized integration. -/
def c003FirstTargetRationale : String :=
  "Choose the Schwartz-potential statement first: it aligns with the imported " ++
  "Schwartz/Fourier/distribution anchors and with the classical IST domain, " ++
  "while weak distributional KdV, nonzero one-soliton calculus, and " ++
  "reflectionless finite-soliton reconstruction need larger missing APIs."

/-- C003 non-selected target blockers. -/
def c003DeferredTargetBlockers : List (C003FormalTargetOption × String) := [
  (.weakDistributionalKdVStatement,
    "requires a concrete distributional KdV residual and product/derivative APIs for the selected function or distribution class"),
  (.oneSolitonSpecialCase,
    "requires checked hyperbolic-function calculus for the nonzero sech-squared soliton and its third spatial derivative"),
  (.reflectionlessFiniteSolitonPackage,
    "requires finite scattering data, Marchenko/reconstruction formulas, determinant identities, and reflectionless spectral packages")
]

/-- The C003 selected target is definitionally the Schwartz-potential statement. -/
theorem c003FirstConcreteFormalTarget_eq :
    c003FirstConcreteFormalTarget =
      C003FormalTargetOption.schwartzPotentialStatement :=
  rfl

/-- The selected Schwartz potential profile is the pointwise coercion of the Schwartz map. -/
theorem SchwartzPotentialInitialProfile_apply
    (q : KdVSchwartzPotential) (x : ℝ) :
    SchwartzPotentialInitialProfile q x = q x :=
  rfl

/--
The existing abstract statement shape specializes to the selected
Schwartz-potential target.
-/
theorem statementShape_implies_schwartzPotentialTarget
    (h : StatementShape) : SchwartzPotentialStatementTarget := by
  intro M q hAdmissible
  exact h M (SchwartzPotentialInitialProfile q) hAdmissible

/--
The current model-field wrapper also specializes to the selected
Schwartz-potential target.  This remains a wrapper around model obligations,
not a construction of inverse scattering from mathlib.
-/
theorem schwartzPotentialTarget_from_model_fields :
    SchwartzPotentialStatementTarget :=
  statementShape_implies_schwartzPotentialTarget statementShape_from_model_fields

/-! ## C004 unbounded Schrödinger-operator API audit -/

/-- Generic partially defined Hilbert-space operators exposed by mathlib's `LinearPMap` API. -/
abbrev UnboundedHilbertOperator
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H] : Type u :=
  H →ₗ.[ℂ] H

/--
Checked generic self-adjoint unbounded-operator package.

This is only a mathlib API anchor for partially defined Hilbert-space
operators.  It is not yet a one-dimensional Schrödinger operator
`-d²/dx² + q`.
-/
structure SelfAdjointUnboundedHilbertOperator
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] where
  op : UnboundedHilbertOperator H
  selfAdjoint : IsSelfAdjoint op

/-- A self-adjoint `LinearPMap` has dense domain in the ambient Hilbert space. -/
theorem SelfAdjointUnboundedHilbertOperator.dense_domain
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A : SelfAdjointUnboundedHilbertOperator H) :
    Dense (A.op.domain : Set H) :=
  A.selfAdjoint.dense_domain

/-- A self-adjoint `LinearPMap` is closed. -/
theorem SelfAdjointUnboundedHilbertOperator.isClosed
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A : SelfAdjointUnboundedHilbertOperator H) :
    A.op.IsClosed :=
  A.selfAdjoint.isClosed

/--
C004 result: mathlib has a generic unbounded-operator layer, but the
Schrödinger-specific scattering stack is absent from the repo-local closure.
-/
inductive C004UnboundedSchrodingerAuditResult where
  | genericLinearPMapPresent_schrodingerSpecificStackAbsent
  deriving DecidableEq, Repr

/-- Final C004 audit classification. -/
def c004UnboundedSchrodingerAuditResult : C004UnboundedSchrodingerAuditResult :=
  .genericLinearPMapPresent_schrodingerSpecificStackAbsent

/-- Positive generic unbounded-operator anchors found in pinned mathlib. -/
def c004AvailableUnboundedOperatorAnchors : List String := [
  "Mathlib.Analysis.InnerProductSpace.LinearPMap",
  "Mathlib.Topology.Algebra.Module.LinearPMap",
  "LinearPMap",
  "LinearPMap.IsClosed",
  "LinearPMap.IsClosable",
  "LinearPMap.HasCore",
  "LinearPMap.adjoint",
  "LinearPMap.IsFormalAdjoint",
  "ContinuousLinearMap.toPMap_adjoint_eq_adjoint_toPMap_of_dense",
  "IsSelfAdjoint for LinearPMap self-adjointness",
  "IsSelfAdjoint.dense_domain",
  "IsSelfAdjoint.isClosed"
]

/--
Exact missing APIs before attempting direct scattering for a one-dimensional
Schrödinger operator.
-/
def c004MissingSchrodingerAPIs : List String := [
  "constructor for the one-dimensional L2(R) Schrodinger operator H_q = -d^2/dx^2 + multiplication by q as a LinearPMap",
  "domain package for H^2(R), Schwartz, or another dense core embedded in L2(R) and stable under the differential expression",
  "proof that the selected second-derivative plus potential-multiplication expression is symmetric and self-adjoint on that domain",
  "unbounded LinearPMap resolvent and spectrum API suitable for self-adjoint differential operators, not only bounded algebra spectrum",
  "direct-scattering API: Jost solutions, Weyl-Titchmarsh data, reflection/transmission coefficients, and discrete spectrum/norming constants",
  "inverse-scattering API: Marchenko or Gelfand-Levitan equation, reconstruction, and proof that reconstructed potentials solve KdV"
]

/-- C004 route decision for public backfill. -/
def c004SchrodingerAuditConclusion : String :=
  "Do not attempt direct scattering yet: use mathlib's generic LinearPMap " ++
  "self-adjoint API as the unbounded-operator anchor, but record the missing " ++
  "Schrodinger-domain, self-adjointness, unbounded spectrum/resolvent, direct " ++
  "scattering, and Marchenko/Gelfand-Levitan reconstruction APIs."

/-- Checked record of the C004 audit classification. -/
theorem c004UnboundedSchrodingerAuditResult_eq :
    c004UnboundedSchrodingerAuditResult =
      C004UnboundedSchrodingerAuditResult.genericLinearPMapPresent_schrodingerSpecificStackAbsent :=
  rfl

/-- The C004 missing-API list records six concrete blockers. -/
theorem c004MissingSchrodingerAPIs_length :
    c004MissingSchrodingerAPIs.length = 6 :=
  rfl

/-! ## C005 external GitHub Lean 4 code-search audit -/

/--
C005 authenticated GitHub code-search status.

The worker environment had no usable GitHub authentication (`gh auth status`
reported no logged-in hosts and `GH_TOKEN`/`GITHUB_TOKEN` were absent), so the
requested authenticated code search could not be completed in this pass.
-/
inductive C005GitHubCodeSearchStatus where
  | authenticationUnavailable
  deriving DecidableEq, Repr

/-- Final C005 authenticated-search status for this pass. -/
def c005GitHubCodeSearchStatus : C005GitHubCodeSearchStatus :=
  .authenticationUnavailable

/-- Exact C005 GitHub Lean 4 code-search terms requested by the child task. -/
def c005RequestedGitHubSearchTerms : List String := [
  "KdV",
  "Korteweg",
  "inverse scattering",
  "Marchenko",
  "Gel'fand-Levitan",
  "Schrodinger scattering",
  "Lax pair",
  "soliton"
]

/--
External Lean 4 candidates verified by an authenticated GitHub code search.

This list is empty because authentication was unavailable, not because the
authenticated search proved that no such candidate exists.
-/
def c005AuthenticatedGitHubCandidates : List String := []

/--
C005 repo-local gate: no external Lean 4 inverse-scattering proof was verified,
pinned, imported, or wrapped locally in this pass.
-/
def c005RepoLocalIntegrationGate : String :=
  "not completed: authenticated GitHub code search blocked by missing credentials; no external candidate pinned or imported"

/-- Checked record of the C005 authenticated-search blocker. -/
theorem c005GitHubCodeSearchStatus_eq :
    c005GitHubCodeSearchStatus =
      C005GitHubCodeSearchStatus.authenticationUnavailable :=
  rfl

/-- C005 has no authenticated candidate commit hashes recorded in this pass. -/
theorem c005AuthenticatedGitHubCandidates_eq_nil :
    c005AuthenticatedGitHubCandidates = [] :=
  rfl

/-! ## C006 external IST-proof integration gate -/

/--
C006 integration status for the conditional external-proof task.

No placeholder-free Lean 4 proof of the full KdV inverse-scattering theorem was
verified in this pass.  Therefore this module cannot add a pinned Lake
dependency, vendored proof body, or wrapper theorem for a terminal IST proof.
-/
inductive C006ExternalISTProofIntegrationStatus where
  | noPlaceholderFreeExternalProofVerified
  deriving DecidableEq, Repr

/-- Final C006 conditional-integration status. -/
def c006ExternalISTProofIntegrationStatus : C006ExternalISTProofIntegrationStatus :=
  .noPlaceholderFreeExternalProofVerified

/--
External Lean 4 IST proof candidates eligible for pin/import/wrapper work.

This list is empty because no placeholder-free candidate with a concrete
repository, commit, module, and theorem name was verified in this pass.
-/
def c006VerifiedPlaceholderFreeISTProofCandidates : List String := []

/--
Required local action if a future pass verifies a placeholder-free external
Lean 4 IST proof.
-/
def c006RequiredActionIfProofFound : List String := [
  "record the upstream repository URL, exact commit hash, module path, theorem name, Lean toolchain, and placeholder audit",
  "add a pinned Lake dependency or vendor the proof body inside the repo-local validation closure",
  "add a local wrapper theorem in S1_M_208.lean or a serialized Stage1 module that imports the pinned proof",
  "rerun cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_208.lean before any completion claim"
]

/-- Concrete blockers preventing a C006 completion claim in this pass. -/
def c006CurrentIntegrationBlockers : List String := [
  "no placeholder-free Lean 4 proof candidate for the full KdV inverse-scattering theorem was verified",
  "authenticated GitHub code search remains blocked by missing gh/GH_TOKEN/GITHUB_TOKEN credentials",
  "there is no external commit, module path, theorem name, or proof body to pin, vendor, import, and wrap"
]

/--
C006 repo-local integration-debt gate.

The gate is acceptable only as a non-completed formalization-debt state: this
file makes no `external_upstream_anchor_only` completion claim and records that
pin/import/check or a concrete integration blocker is mandatory if an external
proof is later found.
-/
def c006RepoLocalIntegrationDebtGate : String :=
  "not completed; no repo-local integration debt is being treated as completed evidence"

/-- C006 keeps the full terminal theorem in formalization debt. -/
def c006MachineProofDebtClass : String :=
  "formalization_debt"

/-- Checked record of the C006 conditional-integration status. -/
theorem c006ExternalISTProofIntegrationStatus_eq :
    c006ExternalISTProofIntegrationStatus =
      C006ExternalISTProofIntegrationStatus.noPlaceholderFreeExternalProofVerified :=
  rfl

/-- No C006 external candidate is available for dependency pinning in this pass. -/
theorem c006VerifiedPlaceholderFreeISTProofCandidates_eq_nil :
    c006VerifiedPlaceholderFreeISTProofCandidates = [] :=
  rfl

/-- C006 records three concrete blockers before any completion claim. -/
theorem c006CurrentIntegrationBlockers_length :
    c006CurrentIntegrationBlockers.length = 3 :=
  rfl

/-! ## C007 terminal formalization-debt gate -/

/--
C007 terminal closure status for THM-M-1549.

The checked declarations in this module do not contain a proof body for the
full inverse-scattering theorem, do not wrap a mathlib theorem proving it, and
do not import a pinned external proof closure.
-/
inductive C007TerminalClosureStatus where
  | terminalClosureNotRepoLocal
  deriving DecidableEq, Repr

/-- Final C007 status: the terminal theorem is not closed repo-locally. -/
def c007TerminalClosureStatus : C007TerminalClosureStatus :=
  .terminalClosureNotRepoLocal

/-- C007 machine-proof debt classification for THM-M-1549. -/
def c007MachineProofDebtClass : String :=
  "formalization_debt"

/--
Artifacts that would be sufficient to leave formalization debt for the terminal
inverse-scattering theorem.
-/
def c007CompletionPrerequisites : List String := [
  "repo-local proof body for the full KdV inverse-scattering theorem",
  "repo-local wrapper around a pinned mathlib theorem proving the full terminal theorem",
  "pinned or vendored external Lean 4 proof closure with a repo-local wrapper theorem"
]

/-- Current C007 blockers for any completed theorem-state claim. -/
def c007CurrentTerminalBlockers : List String := [
  "no repo-local proof body for the full inverse-scattering transform theorem is present",
  "no mathlib theorem for the full KdV inverse-scattering result is imported and wrapped",
  "no external Lean 4 proof closure is pinned, vendored, imported, and locally wrapped"
]

/--
C007 repo-local integration-debt gate.

The gate passes only as a non-completed status: there is no completed claim and
there is no anchor-only external proof evidence being counted as completed.
-/
def c007RepoLocalIntegrationDebtGate : String :=
  "non-completed gate passed: no repo-local integration debt is retained in a completed state"

/-- Checked record of the C007 terminal closure status. -/
theorem c007TerminalClosureStatus_eq :
    c007TerminalClosureStatus =
      C007TerminalClosureStatus.terminalClosureNotRepoLocal :=
  rfl

/-- C007 keeps THM-M-1549 classified as formalization debt. -/
theorem c007MachineProofDebtClass_eq :
    c007MachineProofDebtClass = "formalization_debt" :=
  rfl

/-- C007 records exactly the three allowed completion routes. -/
theorem c007CompletionPrerequisites_length :
    c007CompletionPrerequisites.length = 3 :=
  rfl

/-- C007 records exactly the three current blockers matching those routes. -/
theorem c007CurrentTerminalBlockers_length :
    c007CurrentTerminalBlockers.length = 3 :=
  rfl

/-! ## Audit probes -/

#check spatialDeriv
#check spatialThirdDeriv
#check KdVResidual
#check SolvesKdV
#check ScatteringData
#check InverseScatteringModel
#check ReconstructedSolution
#check StatementShape
#check statementShape_from_model_fields
#check constant_solvesKdV
#check zero_solvesKdV
#check spectrum
#check c002MathlibAuditRevision
#check c002MathlibInfrastructureAreas
#check c002MathlibInfrastructureModulePaths
#check c002NoLocalMathlibMatchTerms
#check c002MathlibAuditRevision_eq
#check c002MathlibInfrastructureAreas_eq
#check c002NoLocalMathlibMatchTerms_eq
#check C003FormalTargetOption
#check c003FirstConcreteFormalTarget
#check KdVSchwartzPotential
#check SchwartzPotentialInitialProfile
#check SchwartzPotentialStatementTarget
#check c003FirstTargetRationale
#check c003DeferredTargetBlockers
#check c003FirstConcreteFormalTarget_eq
#check SchwartzPotentialInitialProfile_apply
#check statementShape_implies_schwartzPotentialTarget
#check schwartzPotentialTarget_from_model_fields
#check LinearPMap
#check LinearPMap.IsClosed
#check LinearPMap.IsClosable
#check LinearPMap.HasCore
#check LinearPMap.adjoint
#check LinearPMap.IsFormalAdjoint
#check IsSelfAdjoint.dense_domain
#check IsSelfAdjoint.isClosed
#check UnboundedHilbertOperator
#check SelfAdjointUnboundedHilbertOperator
#check SelfAdjointUnboundedHilbertOperator.dense_domain
#check SelfAdjointUnboundedHilbertOperator.isClosed
#check C004UnboundedSchrodingerAuditResult
#check c004UnboundedSchrodingerAuditResult
#check c004AvailableUnboundedOperatorAnchors
#check c004MissingSchrodingerAPIs
#check c004SchrodingerAuditConclusion
#check c004UnboundedSchrodingerAuditResult_eq
#check c004MissingSchrodingerAPIs_length
#check C005GitHubCodeSearchStatus
#check c005GitHubCodeSearchStatus
#check c005RequestedGitHubSearchTerms
#check c005AuthenticatedGitHubCandidates
#check c005RepoLocalIntegrationGate
#check c005GitHubCodeSearchStatus_eq
#check c005AuthenticatedGitHubCandidates_eq_nil
#check C006ExternalISTProofIntegrationStatus
#check c006ExternalISTProofIntegrationStatus
#check c006VerifiedPlaceholderFreeISTProofCandidates
#check c006RequiredActionIfProofFound
#check c006CurrentIntegrationBlockers
#check c006RepoLocalIntegrationDebtGate
#check c006MachineProofDebtClass
#check c006ExternalISTProofIntegrationStatus_eq
#check c006VerifiedPlaceholderFreeISTProofCandidates_eq_nil
#check c006CurrentIntegrationBlockers_length
#check C007TerminalClosureStatus
#check c007TerminalClosureStatus
#check c007MachineProofDebtClass
#check c007CompletionPrerequisites
#check c007CurrentTerminalBlockers
#check c007RepoLocalIntegrationDebtGate
#check c007TerminalClosureStatus_eq
#check c007MachineProofDebtClass_eq
#check c007CompletionPrerequisites_length
#check c007CurrentTerminalBlockers_length

end AwesomeTheorems.Stage1.S1_M_208
