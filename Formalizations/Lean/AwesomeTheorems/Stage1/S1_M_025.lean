import Mathlib.Analysis.Calculus.DifferentialForm.Basic
import Mathlib.Analysis.InnerProductSpace.Harmonic.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Geometry.Manifold.Complex
import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.LinearAlgebra.DFinsupp
import Mathlib.RingTheory.Kaehler.Basic

/-!
# S1-M-025 / THM-M-0113: Hodge decomposition theorem

This Stage1 module records a conservative Lean 4 statement boundary for the
analytic cohomological Hodge decomposition of compact Kahler manifolds.  That
target is the direct-sum decomposition of complex cohomology into `(p,q)` pieces
for compact Kahler manifolds, mediated by harmonic representatives.  It is not
the algebraic theory of `KaehlerDifferential` for commutative algebras, even
though that algebraic API is useful as nearby differential infrastructure.

The current mathlib pin has complex-manifold, Riemannian, differential-form,
harmonic function, direct-sum, and algebraic Kaehler-differential infrastructure,
but the local audit did not locate a terminal compact-Kahler Hodge-decomposition
theorem.

The file therefore defines a parameterized `StatementShape : Prop` and a few
small checked wrappers around available supporting APIs.  It is intentionally
not a proof of the classical theorem.

## Theorem-level mathlib audit for `S1-M-025-public-004`

Pinned local mathlib checkout: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
under Lean `v4.29.0`.

| Area | Exact module(s) checked | Present anchor(s) | Absent terminal theorem names/search terms |
|---|---|---|---|
| Complex/Riemannian manifolds | `Mathlib.Geometry.Manifold.Complex`, `Mathlib.Geometry.Manifold.Riemannian.Basic`, `Mathlib.Geometry.Manifold.VectorBundle.Riemannian` | `ModelWithCorners`, `ChartedSpace`, `IsManifold`, Riemannian vector-bundle infrastructure | `KaehlerManifold`, `KahlerManifold`, `KählerManifold`, `compact Kahler`, `compact Kähler`, `compact Kaehler` |
| Differential forms/de Rham support | `Mathlib.Analysis.Calculus.DifferentialForm.Basic`, `Mathlib.Analysis.Calculus.DifferentialForm.VectorField` | `extDeriv`, `extDeriv_extDeriv` | `deRhamCohomology`, `DeRhamCohomology`, `HodgeDecomposition`, `Hodge theorem` |
| Harmonic analysis | `Mathlib.Analysis.InnerProductSpace.Harmonic.Basic`, `Harmonic.Constructions`, `Harmonic.Analytic`, `Mathlib.Analysis.Complex.Harmonic.*` | `HarmonicAt`, `HarmonicOnNhd`, `harmonicOnNhd_const`, complex harmonic-function facts | `HarmonicForm`, `HodgeLaplacian`, `harmonic representative`, `harmonic differential form` |
| Sheaf/cohomology infrastructure | `Mathlib.CategoryTheory.Sites.SheafCohomology.Basic`, `Cech`, `MayerVietoris`; `Mathlib.AlgebraicGeometry.Sites.ElladicCohomology` | `Sheaf.H`, Cech/Mayer-Vietoris scaffolding, `Scheme.EllAdicCohomology` | `Dolbeault`, `DolbeaultCohomology`, `Hodge filtration`, `Hodge-to-de Rham` |
| Algebraic Kaehler differentials | `Mathlib.RingTheory.Kaehler.Basic`, `TensorProduct`, `JacobiZariski`; `Mathlib.RingTheory.Smooth.Kaehler`; `Mathlib.RingTheory.Etale.Kaehler` | `KaehlerDifferential`, `KaehlerDifferential.D`, base-change/Jacobi-Zariski and smooth/etale differential APIs | analytic compact-Kahler `H^{p,q}` direct-sum theorem; Kähler identities; Hodge decomposition theorem |

Conclusion: this child found import-checkable supporting infrastructure only.
The exact absent theorem-name audit does not justify a completion claim for
THM-M-0113, and it does not create `repo_local_integration_debt` because no
completed external Lean theorem is being used as anchor-only evidence here.

## External primary-source audit for `S1-M-025-public-005`

Re-run date: 2026-05-01.

Primary sources checked:

| Repository | Revision | Lean version | mathlib version | Module / names checked | Result |
|---|---|---|---|---|---|
| `https://github.com/lean-dojo/LeanMillenniumPrizeProblems` | `540da94826f70f3edf4d4fc66ce6cda20e903f61` | `leanprover/lean4:v4.26.0` | `2df2f0150c275ad53cb3c90f7c98ec15a56a1a67` | `Problems.Hodge.Millennium`: `MillenniumHodge.HodgeConjecture`; `Problems.Hodge.Variety`: `VarietyDefinition.HodgeData.hodgeSubspace`, `hodgeClass`, `hodgeClassFiltration` | Not a Hodge-decomposition theorem. The repository states Millennium problem statements and parameterizes the missing Hodge decomposition interface. |
| `https://github.com/leanprover-community/mathlib4` | `49f10344339f99fda2d3bb0aa1455bfa6801fd93` | `leanprover/lean4:v4.30.0-rc2` | repository itself, no dependent mathlib package | `Mathlib.Analysis.Calculus.DifferentialForm.Basic`: `extDeriv_extDeriv`; `Mathlib.Analysis.InnerProductSpace.Harmonic.Basic`: `HarmonicAt`, `HarmonicOnNhd`, `harmonicOnNhd_const` | Supporting differential-form and harmonic-function infrastructure only; no compact-Kahler Hodge decomposition theorem found. |

External audit conclusion: no real Lean 4 theorem for compact-Kahler Hodge
decomposition was located.  Therefore there is no external proof to leave as
anchor-only completion evidence, and no `repo_local_integration_debt` is
created by this child.  The parent remains `formalization_debt` /
`not_repo_local_closed`.
-/

noncomputable section

open scoped Manifold Topology

namespace AwesomeTheorems.Stage1.S1_M_025

universe uM uE uH uC uF u𝕜 uV uW

/-- Bidegrees `(p,q)` contributing to total cohomological degree `n`. -/
abbrev HodgeBidegree (n : Nat) : Type :=
  {pq : Nat × Nat // pq.1 + pq.2 = n}

/--
Stage1 input package for the compact-Kahler Hodge decomposition theorem.

The manifold side uses concrete mathlib complex-manifold hypotheses where they
are available.  The Kahler metric, cohomology groups, Hodge summands, harmonic
forms, and comparison theorems remain explicit fields because the audited
mathlib snapshot does not provide a bundled terminal theorem for them.
-/
structure CompactKahlerHodgePackage
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℂ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M] : Type
      (max (uM + 1) (uC + 1) (uF + 1)) where
  isComplexManifold : IsManifold I ω M
  compactSpace : CompactSpace M
  t2Space : T2Space M
  isKahler : Prop
  Cohomology : Nat → Type uC
  [cohomologyAdd : ∀ n, AddCommGroup (Cohomology n)]
  [cohomologyModule : ∀ n, Module ℂ (Cohomology n)]
  hodgeSummand : ∀ n _p _q : Nat, Submodule ℂ (Cohomology n)
  HarmonicForm : Nat → Type uF
  harmonicClass : ∀ n, HarmonicForm n → Cohomology n
  isHarmonic : ∀ n, HarmonicForm n → Prop
  isClosedForm : ∀ n, HarmonicForm n → Prop
  isExactForm : ∀ n, HarmonicForm n → Prop
  hodgeTypeOfHarmonic : ∀ n, HarmonicForm n → Nat → Nat → Prop

attribute [instance] CompactKahlerHodgePackage.cohomologyAdd
attribute [instance] CompactKahlerHodgePackage.cohomologyModule

namespace CompactKahlerHodgePackage

variable
  {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℂ E]
  {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℂ E H}
  {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]

variable (D : CompactKahlerHodgePackage E H I M)

/-- The Hodge summand selected by a total-degree-indexed bidegree. -/
def piece (n : Nat) (pq : HodgeBidegree n) : Submodule ℂ (D.Cohomology n) :=
  D.hodgeSummand n pq.1.1 pq.1.2

/-- Fixed-degree internal direct-sum conclusion for `H^n = ⨆_{p+q=n} H^{p,q}`. -/
def DirectSumConclusion : Prop :=
  ∀ n : Nat,
    iSupIndep (fun pq : HodgeBidegree n => D.piece n pq) ∧
      (iSup (fun pq : HodgeBidegree n => D.piece n pq) = ⊤)

/--
Analytic Hodge-theory boundary: each cohomology class has a closed harmonic
representative, and exact harmonic representatives map to zero.
-/
def HarmonicRepresentativeConclusion : Prop :=
  ∀ n : Nat,
    (∀ x : D.Cohomology n,
      ∃ η : D.HarmonicForm n,
        D.isHarmonic n η ∧ D.isClosedForm n η ∧ D.harmonicClass n η = x) ∧
      (∀ η : D.HarmonicForm n,
        D.isHarmonic n η → D.isExactForm n η → D.harmonicClass n η = 0)

/--
Type-decomposition boundary: harmonic representatives decompose into bidegrees
whose total degree is the ambient cohomological degree.
-/
def HarmonicTypeConclusion : Prop :=
  ∀ n : Nat, ∀ η : D.HarmonicForm n,
    D.isHarmonic n η →
      ∃ pq : HodgeBidegree n, D.hodgeTypeOfHarmonic n η pq.1.1 pq.1.2

/-- The compact-Kahler Hodge statement packaged as analytic plus direct-sum data. -/
def StatementShape : Prop :=
  D.isKahler →
    D.HarmonicRepresentativeConclusion ∧
      D.HarmonicTypeConclusion ∧
        D.DirectSumConclusion

/-- The bidegree proof stored in a `HodgeBidegree`. -/
theorem bidegree_total (n : Nat) (pq : HodgeBidegree n) :
    pq.1.1 + pq.1.2 = n :=
  pq.2

/-- A supplied analytic/type/direct-sum package closes the local statement shape. -/
theorem statementShape_of_conclusions
    (hHarmonic : D.HarmonicRepresentativeConclusion)
    (hType : D.HarmonicTypeConclusion)
    (hDirect : D.DirectSumConclusion) :
    D.StatementShape :=
  fun _ => ⟨hHarmonic, hType, hDirect⟩

/-- Projection of the analytic harmonic-representative package from a supplied theorem shape. -/
theorem statementShape_harmonicRepresentative
    (h : D.StatementShape) (hKahler : D.isKahler) :
    D.HarmonicRepresentativeConclusion :=
  (h hKahler).1

/-- Projection of the harmonic bidegree/type package from a supplied theorem shape. -/
theorem statementShape_harmonicType
    (h : D.StatementShape) (hKahler : D.isKahler) :
    D.HarmonicTypeConclusion :=
  (h hKahler).2.1

/-- Projection of the cohomological direct-sum package from a supplied theorem shape. -/
theorem statementShape_directSum
    (h : D.StatementShape) (hKahler : D.isKahler) :
    D.DirectSumConclusion :=
  (h hKahler).2.2

end CompactKahlerHodgePackage

/-- Repo-local Stage1 statement shape for THM-M-0113. -/
def StatementShape : Prop :=
  ∀ (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℂ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    (D : CompactKahlerHodgePackage.{uM, uE, uH, uC, uF} E H I M),
      D.StatementShape

/-- Low-risk introduction theorem for the normalized statement boundary. -/
theorem StatementShape.intro
    (h : ∀ (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℂ E]
      (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℂ E H)
      (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
      (D : CompactKahlerHodgePackage.{uM, uE, uH, uC, uF} E H I M),
        D.StatementShape) :
    StatementShape.{uM, uE, uH, uC, uF} :=
  h

/--
Checked supporting anchor: on normed vector spaces, the exterior derivative
composes with itself to zero for sufficiently smooth differential forms.

This is de Rham-complex infrastructure only, not Hodge decomposition.
-/
theorem extDeriv_extDeriv_mathlib_anchor
    (𝕜 : Type u𝕜) [NontriviallyNormedField 𝕜]
    (V : Type uV) [NormedAddCommGroup V] [NormedSpace 𝕜 V]
    (W : Type uW) [NormedAddCommGroup W] [NormedSpace 𝕜 W]
    {n : ℕ} {r : WithTop ℕ∞}
    (ω : V → V [⋀^Fin n]→L[𝕜] W)
    (hω : ContDiff 𝕜 r ω) (hr : minSmoothness 𝕜 2 ≤ r) :
    extDeriv (extDeriv ω) = 0 :=
  extDeriv_extDeriv hω hr

/--
Child `S1-M-025-C002` wrapper around the lowest-level available mathlib anchor.

This is checked de Rham-complex support (`d ∘ d = 0`) only; it does not assert
compact-Kahler Hodge decomposition, harmonic representatives, Hodge summands, or
any Dolbeault/cohomology comparison theorem.
-/
theorem c002_supporting_extDeriv_extDeriv_anchor
    (𝕜 : Type u𝕜) [NontriviallyNormedField 𝕜]
    (V : Type uV) [NormedAddCommGroup V] [NormedSpace 𝕜 V]
    (W : Type uW) [NormedAddCommGroup W] [NormedSpace 𝕜 W]
    {n : ℕ} {r : WithTop ℕ∞}
    (ω : V → V [⋀^Fin n]→L[𝕜] W)
    (hω : ContDiff 𝕜 r ω) (hr : minSmoothness 𝕜 2 ≤ r) :
    extDeriv (extDeriv ω) = 0 :=
  extDeriv_extDeriv_mathlib_anchor 𝕜 V W ω hω hr

/-- Checked supporting anchor: constant functions are harmonic on finite-dimensional real spaces. -/
theorem harmonicOnNhd_const_mathlib_anchor
    (V : Type uV) [NormedAddCommGroup V] [InnerProductSpace ℝ V]
    [FiniteDimensional ℝ V]
    (W : Type uW) [NormedAddCommGroup W] [NormedSpace ℝ W]
    (s : Set V) (c : W) :
    InnerProductSpace.HarmonicOnNhd (fun _ : V => c) s :=
  InnerProductSpace.harmonicOnNhd_const (E := V) (F := W) (s := s) (c := c)

/-- Stage1 theorem identifier for audit tooling. -/
def theoremUID : String := "THM-M-0113"

/-- Local machine-proof debt classification for the current artifact. -/
def machineProofDebt : String := "formalization_debt"

/-- Completion-gate flag: this open statement-shape artifact retains no completed integration debt. -/
def repoLocalIntegrationDebtRetained : Bool := false

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.Complex",
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Analysis.Calculus.DifferentialForm.Basic",
  "Mathlib.Analysis.InnerProductSpace.Harmonic.Basic",
  "Mathlib.LinearAlgebra.DFinsupp",
  "Mathlib.CategoryTheory.Sites.SheafCohomology.Basic",
  "Mathlib.RingTheory.Kaehler.Basic"
]

/-- Search terms that did not locate a terminal theorem in the pinned local mathlib tree. -/
def absentTerminalSearchTerms : List String := [
  "HodgeDecomposition",
  "hodgeDecomposition",
  "Hodge.decomposition",
  "Hodge decomposition",
  "Hodge theorem",
  "HarmonicForm",
  "HodgeLaplacian",
  "harmonic representative",
  "harmonic differential form",
  "Dolbeault",
  "DolbeaultCohomology",
  "deRhamCohomology",
  "DeRhamCohomology",
  "KahlerManifold",
  "KaehlerManifold",
  "Kaehler decomposition",
  "compact Kahler",
  "compact Kaehler",
  "Hodge filtration",
  "Hodge-to-de Rham"
]

/--
Integration-ready theorem-level mathlib audit rows for `S1-M-025-public-004`.

Each row records an exact local module family checked, a positive supporting API
if present, and the absent terminal theorem names/search terms relevant to the
compact-Kahler Hodge decomposition target.
-/
def theoremLevelMathlibAuditRows : List String := [
  "Complex/Riemannian manifolds | Mathlib.Geometry.Manifold.Complex; Mathlib.Geometry.Manifold.Riemannian.Basic; Mathlib.Geometry.Manifold.VectorBundle.Riemannian | ModelWithCorners/ChartedSpace/IsManifold and Riemannian vector-bundle infrastructure present | absent: KaehlerManifold, KahlerManifold, KählerManifold, compact Kahler, compact Kähler, compact Kaehler",
  "Differential forms/de Rham support | Mathlib.Analysis.Calculus.DifferentialForm.Basic; Mathlib.Analysis.Calculus.DifferentialForm.VectorField | extDeriv and extDeriv_extDeriv present | absent: deRhamCohomology, DeRhamCohomology, HodgeDecomposition, Hodge theorem",
  "Harmonic analysis | Mathlib.Analysis.InnerProductSpace.Harmonic.Basic; Harmonic.Constructions; Harmonic.Analytic; Mathlib.Analysis.Complex.Harmonic.* | HarmonicAt, HarmonicOnNhd, harmonicOnNhd_const, complex harmonic-function facts present | absent: HarmonicForm, HodgeLaplacian, harmonic representative, harmonic differential form",
  "Sheaf/cohomology infrastructure | Mathlib.CategoryTheory.Sites.SheafCohomology.Basic; Cech; MayerVietoris; Mathlib.AlgebraicGeometry.Sites.ElladicCohomology | Sheaf.H, Cech/Mayer-Vietoris scaffolding, Scheme.EllAdicCohomology present | absent: Dolbeault, DolbeaultCohomology, Hodge filtration, Hodge-to-de Rham",
  "Algebraic Kaehler differentials | Mathlib.RingTheory.Kaehler.Basic; TensorProduct; JacobiZariski; Mathlib.RingTheory.Smooth.Kaehler; Mathlib.RingTheory.Etale.Kaehler | KaehlerDifferential, KaehlerDifferential.D, base-change/Jacobi-Zariski and smooth/etale differential APIs present | absent: analytic compact-Kahler H^{p,q} direct-sum theorem, Kähler identities, Hodge decomposition theorem"
]

/--
Integration-ready external-primary-source audit rows for `S1-M-025-public-005`.

Each row records an exact external repository, revision, Lean toolchain, mathlib
revision when applicable, module/name candidates checked, and the completion
verdict.  None is a real compact-Kahler Hodge-decomposition theorem.
-/
def externalPrimarySourceAuditRows : List String := [
  "lean-dojo/LeanMillenniumPrizeProblems | rev 540da94826f70f3edf4d4fc66ce6cda20e903f61 | Lean leanprover/lean4:v4.26.0 | mathlib 2df2f0150c275ad53cb3c90f7c98ec15a56a1a67 | modules Problems.Hodge.Millennium and Problems.Hodge.Variety | names MillenniumHodge.HodgeConjecture; VarietyDefinition.HodgeData.hodgeSubspace; VarietyDefinition.HodgeData.hodgeClass; VarietyDefinition.HodgeData.hodgeClassFiltration | verdict: parameterized Hodge-conjecture statement scaffold, not a Hodge-decomposition theorem",
  "leanprover-community/mathlib4 | rev 49f10344339f99fda2d3bb0aa1455bfa6801fd93 | Lean leanprover/lean4:v4.30.0-rc2 | mathlib repository itself, no dependent mathlib package | modules Mathlib.Analysis.Calculus.DifferentialForm.Basic and Mathlib.Analysis.InnerProductSpace.Harmonic.Basic | names extDeriv_extDeriv; InnerProductSpace.HarmonicAt; InnerProductSpace.HarmonicOnNhd; InnerProductSpace.harmonicOnNhd_const | verdict: supporting differential-form and harmonic-function infrastructure only, not compact-Kahler Hodge decomposition"
]

/--
Child `S1-M-025-C006` integration-gate verdict.

The checked Stage1 artifact records that the current audit has no real external
Lean 4 compact-Kahler Hodge-decomposition theorem to pin, import, or wrap.
Consequently this file does not claim theorem completion from an anchor-only
reference; the remaining state is formalization debt, not a completed external
upstream integration.
-/
def c006IntegrationGateVerdict : List String := [
  "No real external Lean 4 compact-Kahler Hodge-decomposition theorem is currently pinned in this repository.",
  "No anchor-only external reference is being counted as completion for THM-M-0113.",
  "If a future primary-source audit finds a real external theorem, it must be pinned/imported/checked locally or recorded with a concrete integration blocker.",
  "Current C006 result: no repo-local integration debt is retained in a completed state because no completed external proof is being used."
]

/--
Child `S1-M-025-C007` public-tree backfill gate.

This records that public theorem-tree backfill is an integrator-owned public-doc
operation.  The machine-anchor side has only supporting, import-checkable
infrastructure in this file, and the parent leaf-budget ledger still has open
unchecked leaves.  Therefore this child supplies integration-ready leaf IDs but
does not mark the public theorem tree complete.
-/
def c007PublicTreeBackfillGate : List String := [
  "Public-doc backfill is serial integrator work; child workers must not edit Docs/Stage1_Blueprint.md or shared todo surfaces directly.",
  "Machine-anchor status checked: supporting anchors extDeriv_extDeriv and harmonicOnNhd_const are repo-local wrappers only; no terminal compact-Kahler Hodge-decomposition theorem is present.",
  "Local-budget status checked: parent ledger leaf IDs S1-M-025-L001 through S1-M-025-L028 remain unchecked/open until a later proof-package audit closes them independently.",
  "Backfill proposal may list the leaf IDs as open M0387 work, but must not mark S1-M-025-public-007 completed or THM-M-0113 repo-local closed."
]

/-- Integration-ready leaf IDs from the private S1-M-025 ledger for later public backfill. -/
def c007PublicBackfillLeafIds : List String := [
  "S1-M-025-L001 statement-domain normalization",
  "S1-M-025-L002 coefficient and cohomological-degree convention",
  "S1-M-025-L003 p+q=n bidegree index type",
  "S1-M-025-L004 finite/bounded bidegree-index equivalence",
  "S1-M-025-L005 complex-manifold import check",
  "S1-M-025-L006 Riemannian-manifold import check",
  "S1-M-025-L007 exterior-derivative API import check",
  "S1-M-025-L008 extDeriv_extDeriv supporting wrapper",
  "S1-M-025-L009 harmonic-function predicate import check",
  "S1-M-025-L010 sheaf-cohomology API import check",
  "S1-M-025-L011 algebraic Kaehler-differential API import check",
  "S1-M-025-L012 parameterized complex cohomology groups",
  "S1-M-025-L013 parameterized Hodge subspaces",
  "S1-M-025-L014 pure-degree condition for off-degree Hodge pieces",
  "S1-M-025-L015 Hodge-filtration construction from subspaces",
  "S1-M-025-L016 Hodge-piece-to-filtration inclusion",
  "S1-M-025-L017 Kahler metric compatibility data",
  "S1-M-025-L018 Hodge star data",
  "S1-M-025-L019 formal adjoint of exterior derivative",
  "S1-M-025-L020 Laplacian and harmonic-form predicate",
  "S1-M-025-L021 Hodge theorem harmonic-representative statement",
  "S1-M-025-L022 Kahler identities for type preservation",
  "S1-M-025-L023 pairwise disjointness of distinct Hodge pieces",
  "S1-M-025-L024 supremum/top coverage of fixed-degree cohomology",
  "S1-M-025-L025 conversion of disjointness plus coverage to StatementShape",
  "S1-M-025-L026 future external-proof pin or vendored proof body",
  "S1-M-025-L027 future repo-local wrapper around exact imported theorem",
  "S1-M-025-L028 reproducible local build validation"
]

/--
Child `S1-M-025-C008` local build-validation record.

This child ran the required repo-local command after the checked Stage1 wrapper
and audit constants existed.  The command validates this file only; it does not
upgrade THM-M-0113 to a completed compact-Kahler Hodge-decomposition proof.
-/
def c008BuildValidationRecord : List String := [
  "Command: cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_025.lean",
  "Result on 2026-05-01: passed with exit code 0.",
  "Validated surface: repo-local Stage1 statement-shape wrapper, supporting mathlib anchors, and audit constants.",
  "Completion boundary: supporting infrastructure only; THM-M-0113 remains formalization_debt / not_repo_local_closed."
]

/--
Statement-normalization note for the public THM-M-0113 surface.

The theorem target here is analytic Hodge decomposition on compact Kahler
manifolds: complex cohomology in degree `n` decomposes as an internal direct sum
of bidegree pieces `H^{p,q}` with `p + q = n`, and harmonic representatives are
part of the analytic bridge.  The `Mathlib.RingTheory.Kaehler.Basic` import and
`KaehlerDifferential` check are supporting algebraic infrastructure only: they
refer to algebraic Kahler differentials for commutative algebras and do not
state the compact-Kahler manifold Hodge decomposition theorem.
-/
def statementNormalizationNote : List String := [
  "Target: analytic compact-Kahler-manifold Hodge decomposition.",
  "Shape: degree-n complex cohomology is the internal direct sum of H^{p,q} for p + q = n.",
  "Analytic bridge: harmonic representatives and type decomposition carry the Hodge-theory content.",
  "Non-target: algebraic Kaehler differentials for commutative algebras.",
  "The KaehlerDifferential API is checked only as supporting nearby infrastructure."
]

/-- M0387-level package split for the current child pass. -/
def packageSplit : List String := [
  "S1-M-025-E001-L01 statement-normalization: compact Kahler analytic/cohomological Hodge decomposition, not algebraic KaehlerDifferential.",
  "S1-M-025-E001-L02 analytic package: harmonic representatives for every cohomology class and zero class for exact harmonic representatives.",
  "S1-M-025-E001-L03 type package: harmonic representatives carry some bidegree (p,q) with p + q = n.",
  "S1-M-025-E001-L04 cohomological package: degree-n cohomology is the internal direct sum of Hodge summands indexed by p + q = n.",
  "S1-M-025-E001-L05 integration package: no terminal compact-Kahler Hodge theorem is imported or pinned in this repository."
]

/-! ## Audit probes -/

#check HodgeBidegree
#check CompactKahlerHodgePackage.DirectSumConclusion
#check CompactKahlerHodgePackage.HarmonicRepresentativeConclusion
#check CompactKahlerHodgePackage.HarmonicTypeConclusion
#check CompactKahlerHodgePackage.StatementShape
#check CompactKahlerHodgePackage.statementShape_harmonicRepresentative
#check CompactKahlerHodgePackage.statementShape_harmonicType
#check CompactKahlerHodgePackage.statementShape_directSum
#check StatementShape
#check extDeriv_extDeriv_mathlib_anchor
#check c002_supporting_extDeriv_extDeriv_anchor
#check harmonicOnNhd_const_mathlib_anchor
#check statementNormalizationNote
#check packageSplit
#check theoremLevelMathlibAuditRows
#check externalPrimarySourceAuditRows
#check c006IntegrationGateVerdict
#check c007PublicTreeBackfillGate
#check c007PublicBackfillLeafIds
#check c008BuildValidationRecord
#check iSupIndep
#check KaehlerDifferential

end AwesomeTheorems.Stage1.S1_M_025
