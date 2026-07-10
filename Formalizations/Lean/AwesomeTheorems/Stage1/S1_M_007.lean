import Mathlib.AlgebraicGeometry.Morphisms.FiniteType
import Mathlib.AlgebraicGeometry.Geometrically.Integral
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Separated
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.QuasiAffine
import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point
import Mathlib.AlgebraicGeometry.EllipticCurve.Reduction
import Mathlib.NumberTheory.Height.Northcott
import Mathlib.NumberTheory.NumberField.Basic
import Mathlib.NumberTheory.SiegelsLemma
import Mathlib.RingTheory.DedekindDomain.SInteger

/-!
# S1-M-007 / THM-M-0394: Siegel theorem

This Stage1 artifact records a repo-local Lean 4 statement boundary for
Siegel's theorem on finiteness of integral points on curves.  It is not a proof
of Siegel's theorem.  The pinned mathlib dependency currently supplies useful
substrates for number fields, schemes, finite-type and separated morphisms,
Northcott predicates, and `S`-integers/`S`-units, but this audit did not find a
terminal theorem for integral points on curves.
-/

noncomputable section

open CategoryTheory
open AlgebraicGeometry
open scoped WeierstrassCurve.Affine

attribute [local instance] Matrix.seminormedAddCommGroup

universe u v w

namespace AwesomeTheorems.Stage1.S1_M_007

/-- Audit identifier for the source theorem. -/
def theoremUID : String := "THM-M-0394"

/-- Current machine-proof debt classification for this Stage1 artifact. -/
def machineProofDebt : String := "formalization_debt"

/--
This artifact does not retain repo-local integration debt: no external Lean 4
closure has been found and imported, so the remaining debt is formalization
debt.
-/
def repoLocalIntegrationDebtRetained : Bool := false

/--
Child gate for `S1-M-007-A03-lean-statement`.

The exact curve, divisor, genus, affine-open, boundary-support, and
`S`-integral point APIs have not yet been selected.  Therefore this module keeps
only the internal `AwesomeTheorems.Stage1.S1_M_007` statement boundary and must
not be treated as the final public `Stage1.THMM0394` statement namespace.
-/
def exactObjectAPIsSelectedForA03 : Bool := false

/-- Machine-checkable status string for the A03 statement-only namespace gate. -/
def a03LeanStatementNamespaceStatus : String :=
  "blocked: exact object APIs are not yet selected; current StatementShape uses explicit predicate fields"

/-- The A03 exact-object API gate is currently closed. -/
theorem exactObjectAPIsSelectedForA03_eq_false :
    exactObjectAPIsSelectedForA03 = false :=
  rfl

/-- Data needed to state a Siegel-type finiteness theorem over a number field.

The fields `smoothCurve`, `geometricallyIntegralCurve`, `affineCurveModel`, and
`siegelBoundaryCondition` deliberately remain explicit predicates.  They mark
the APIs that a later integrator must replace by concrete curve, divisor,
genus, affine-open, and boundary-support definitions or by a checked upstream
Lean 4 theorem wrapper.
-/
structure SiegelCurveInput (K : Type u) [Field K] [NumberField K] where
  X : Scheme.{u}
  structureMap : X ⟶ Spec (CommRingCat.of K)
  locallyOfFiniteType : LocallyOfFiniteType structureMap
  separated : IsSeparated structureMap
  smoothCurve : Prop
  geometricallyIntegralCurve : Prop
  affineCurveModel : Prop
  siegelBoundaryCondition : Prop
  integralPoint : Type v
  isIntegralPoint : integralPoint → Prop

/-- Statement shape for Siegel's theorem on integral points on curves.

For each number field and each curve package satisfying the geometric and
boundary hypotheses, the set of integral points is finite.  The theorem is kept
as a `def ... : Prop` because no repo-local or pinned upstream Lean 4 terminal
proof has been identified for this Stage1 slot.
-/
def StatementShape : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K),
    D.smoothCurve →
      D.geometricallyIntegralCurve →
        D.affineCurveModel →
          D.siegelBoundaryCondition →
            {P : D.integralPoint | D.isIntegralPoint P}.Finite

/--
Candidate A public-root alias: an affine curve package with a projective
compactification and an explicit Siegel boundary condition.

Candidate B, the log-hyperbolic divisor inequality form, is useful for later
branch splitting but is not selected as the public root in this Stage1 child.
-/
def StatementShapeCandidateA : Prop :=
  StatementShape.{u, v}

/-- Machine-readable record of the chosen public root candidate. -/
def selectedPublicRootCandidate : String :=
  "Candidate A: affine curve with projective compactification"

/-- The selected public root for later blueprint backfill. -/
def SelectedPublicRoot : Prop :=
  StatementShapeCandidateA.{u, v}

/-- The selected public root is definitionally the local statement shape. -/
theorem selectedPublicRoot_iff_statementShape :
    SelectedPublicRoot.{u, v} ↔ StatementShape.{u, v} :=
  Iff.rfl

/-- Packaging lemma for a future terminal proof or checked upstream wrapper. -/
theorem statementShape_of_forall
    (h : ∀ (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K),
      D.smoothCurve →
        D.geometricallyIntegralCurve →
          D.affineCurveModel →
            D.siegelBoundaryCondition →
              {P : D.integralPoint | D.isIntegralPoint P}.Finite) :
    StatementShape.{u, v} :=
  h

/-- The statement-shape definition unfolds to the explicit finiteness target. -/
theorem statementShape_iff :
    StatementShape.{u, v} ↔
      ∀ (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K),
        D.smoothCurve →
          D.geometricallyIntegralCurve →
            D.affineCurveModel →
              D.siegelBoundaryCondition →
                {P : D.integralPoint | D.isIntegralPoint P}.Finite :=
  Iff.rfl

/-- A reduced finite-domain branch: if the selected point type is already
finite, the integral-point subset is finite.  This is only a local sanity check
for the conclusion shape, not a Siegel proof branch.
-/
theorem finite_integralPoints_of_finite_type
    (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K)
    [Finite D.integralPoint] :
    {P : D.integralPoint | D.isIntegralPoint P}.Finite :=
  Set.finite_univ.subset (fun _ _ => Set.mem_univ _)

/--
Terminal conclusion package expected from a completed Siegel formalization for
one fixed arithmetic curve input.

Supplying this package for every admissible input is exactly the missing
machine proof obligation.  The structure only records the target conclusion and
does not manufacture any instance of it.
-/
structure SiegelIntegralPointsPackage
    (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K) where
  finiteIntegralPoints : {P : D.integralPoint | D.isIntegralPoint P}.Finite

/-- A terminal package exposes the integral-point finiteness conclusion. -/
theorem SiegelIntegralPointsPackage.finite
    (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K)
    (P : SiegelIntegralPointsPackage K D) :
    {Q : D.integralPoint | D.isIntegralPoint Q}.Finite :=
  P.finiteIntegralPoints

/--
If a later proof or pinned upstream wrapper supplies a terminal package for
every admissible input, the normalized `StatementShape` follows.
-/
theorem statementShape_of_integralPointsPackage
    (h : ∀ (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K),
      D.smoothCurve →
        D.geometricallyIntegralCurve →
          D.affineCurveModel →
            D.siegelBoundaryCondition →
              SiegelIntegralPointsPackage K D) :
    StatementShape.{u, v} :=
  fun K _ _ D hSmooth hGeom hAffine hBoundary =>
    (h K D hSmooth hGeom hAffine hBoundary).finiteIntegralPoints

/--
Canonical arithmetic-geometry proof packages for the Siegel integral-points
slot.  These are theorem-tree nodes for later formalization work, not proof
claims.
-/
inductive ArithmeticGeometryPackage where
  | curveObjectModel
  | sIntegerAndModelLayer
  | integralPointPredicate
  | compactificationBoundary
  | genusZeroSUnitBranch
  | ellipticWeierstrassBranch
  | higherGenusHeightNorthcottBranch
  | branchAssembly
  | terminalIntegrationGate
  deriving DecidableEq, Repr

/-- Canonical package order for the Siegel arithmetic-geometry split. -/
def arithmeticGeometryPackageSplit : List ArithmeticGeometryPackage := [
  ArithmeticGeometryPackage.curveObjectModel,
  ArithmeticGeometryPackage.sIntegerAndModelLayer,
  ArithmeticGeometryPackage.integralPointPredicate,
  ArithmeticGeometryPackage.compactificationBoundary,
  ArithmeticGeometryPackage.genusZeroSUnitBranch,
  ArithmeticGeometryPackage.ellipticWeierstrassBranch,
  ArithmeticGeometryPackage.higherGenusHeightNorthcottBranch,
  ArithmeticGeometryPackage.branchAssembly,
  ArithmeticGeometryPackage.terminalIntegrationGate
]

/-- The arithmetic-geometry split currently has nine named packages. -/
theorem arithmeticGeometryPackageSplit_length :
    arithmeticGeometryPackageSplit.length = 9 :=
  rfl

/-- Machine-checkable status labels for the current arithmetic-geometry packages. -/
def arithmeticGeometryPackageStatus : List String := [
  "curveObjectModel: statement-shape only; concrete curve and divisor APIs still need selection",
  "sIntegerAndModelLayer: anchors for S.integer and S.unit are typed below, but no integral model is built",
  "integralPointPredicate: predicate field exists; model-independence is not proved",
  "compactificationBoundary: boundary condition is explicit Prop data, not a divisor/genus theorem",
  "genusZeroSUnitBranch: A08 branch leaves and package interface recorded; no local P1-minus-boundary or S-unit proof body",
  "ellipticWeierstrassBranch: A09 Weierstrass object, affine-point, integral-model, and branch-interface wrappers recorded; no local integral-points finiteness proof body",
  "higherGenusHeightNorthcottBranch: A10 route selected as height/Northcott; branch interface recorded below; no local height boundedness proof",
  "branchAssembly: package named; no exhaustive genus/boundary case split is proved",
  "terminalIntegrationGate: no external Lean proof is pinned, imported, or checked here"
]

/--
M0387-level unchecked child leaves for the Siegel proof-package frontier.

Each entry is intentionally a future proof or audit task.  The current artifact
only makes the leaf frontier stable and machine-checkable as data.
-/
def m0387LeafBudgetLedger : List String := [
  "M0394.L001 curve API: choose concrete smooth curve object over a number field; unchecked <=100",
  "M0394.L002 curve API: encode geometric integrality for the selected object; unchecked <=100",
  "M0394.L003 curve API: connect locally finite type and separated morphism anchors; unchecked <=100",
  "M0394.L004 curve API: select projective compactification data; unchecked <=100",
  "M0394.L005 boundary API: represent affine open as complement of boundary support; unchecked <=100",
  "M0394.L006 boundary API: define Siegel boundary condition in genus and support terms; unchecked <=100",
  "M0394.L007 S-integers: choose finite-place set object for a number field; unchecked <=100",
  "M0394.L008 S-integers: connect the place set to mathlib S.integer; unchecked <=100",
  "M0394.L009 S-units: connect boundary equations to mathlib S.unit; unchecked <=100",
  "M0394.L010 integral points: define model-dependent integral point predicate; unchecked <=100",
  "M0394.L011 integral points: prove model-change invariance target; unchecked <=100",
  "M0394.L012 integral points: bridge affine K-points to the predicate field; unchecked <=100",
  "M0394.L013 non-target audit: record that NumberTheory.SiegelsLemma is not this theorem; unchecked <=100",
  "M0394.L014 terminal mathlib audit: search pinned mathlib theorem names; unchecked <=100",
  "M0394.L015 external audit: search primary Lean 4 repositories; unchecked <=100",
  "M0394.L016 genus zero: classify compactification as P1 under genus-zero hypotheses; unchecked <=100",
  "M0394.L017 genus zero: normalize three boundary points by automorphism; unchecked <=100",
  "M0394.L018 genus zero: reduce integral points to S-unit equation data; unchecked <=100",
  "M0394.L019 genus zero: prove finite S-unit equation solution set or import closure; unchecked <=100",
  "M0394.L020 genus zero: package finiteness for the affine curve branch; unchecked <=100",
  "M0394.L021 elliptic branch: select Weierstrass curve API; unchecked <=100",
  "M0394.L022 elliptic branch: bridge affine model to elliptic curve points; unchecked <=100",
  "M0394.L023 elliptic branch: state integral x-coordinate finiteness target; unchecked <=100",
  "M0394.L024 elliptic branch: audit Mordell-Weil or height inputs needed; unchecked <=100",
  "M0394.L025 elliptic branch: package finiteness for genus-one affine curves; unchecked <=100",
  "M0394.L026 higher genus: choose height function on rational points; unchecked <=100",
  "M0394.L027 higher genus: prove or import height boundedness for integral points; unchecked <=100",
  "M0394.L028 higher genus: connect bounded height to Northcott finiteness; unchecked <=100",
  "M0394.L029 higher genus: audit Faltings-style dependency option; unchecked <=100",
  "M0394.L030 higher genus: package finiteness for genus at least two; unchecked <=100",
  "M0394.L031 Diophantine approximation: identify Roth/Subspace inputs if used; unchecked <=100",
  "M0394.L032 Diophantine approximation: bridge divisor support to approximation inequalities; unchecked <=100",
  "M0394.L033 height package: define local heights or select upstream API; unchecked <=100",
  "M0394.L034 height package: prove decomposition of global height into local terms; unchecked <=100",
  "M0394.L035 height package: isolate constants depending on K, S, and model; unchecked <=100",
  "M0394.L036 branch assembly: prove genus and boundary cases cover Candidate A; unchecked <=100",
  "M0394.L037 branch assembly: route genus-zero branch to terminal package; unchecked <=100",
  "M0394.L038 branch assembly: route elliptic branch to terminal package; unchecked <=100",
  "M0394.L039 branch assembly: route higher-genus branch to terminal package; unchecked <=100",
  "M0394.L040 branch assembly: expose StatementShape from terminal packages; unchecked <=100",
  "M0394.L041 corollary wrapper: delay Mordell equation wrapper until root branch is checked; unchecked <=100",
  "M0394.L042 corollary wrapper: delay Thue equation wrapper until root branch is checked; unchecked <=100",
  "M0394.L043 corollary wrapper: delay plane-equation wrapper until root branch is checked; unchecked <=100",
  "M0394.L044 integration gate: if external Lean closure is found, pin dependency; unchecked <=100",
  "M0394.L045 integration gate: import external theorem under local namespace; unchecked <=100",
  "M0394.L046 integration gate: prove local wrapper against SelectedPublicRoot; unchecked <=100",
  "M0394.L047 validation gate: run repo-local Lean command for this module; unchecked <=100",
  "M0394.L048 public sync gate: update blueprint, todo, README, and meta only after checked closure; unchecked <=100"
]

/-- The current unchecked Siegel leaf frontier contains forty-eight entries. -/
theorem m0387LeafBudgetLedger_length :
    m0387LeafBudgetLedger.length = 48 :=
  rfl

/-- A13 child-task scope for preserving the unchecked 48-leaf ledger. -/
def a13LeafLedgerChildScope : String :=
  "S1-M-007-A13-leaf-ledgers: preserve the 48-leaf unchecked M0387 ledger before any public checked status"

/--
A13 ledger-preservation gate.

This child records the leaf frontier as stable bookkeeping only.  It does not
close any Siegel proof branch, does not add a terminal external anchor, and
does not justify a public checked status.
-/
def a13LeafLedgerGate : List String := [
  "leaf_frontier_preserved: m0387LeafBudgetLedger has exactly 48 entries",
  "unchecked_frontier: M0394.L001 through M0394.L040 remain unchecked proof or audit leaves",
  "blocked_frontier: M0394.L041 through M0394.L048 remain blocked behind a terminal proof engine or pinned dependency",
  "no_leaf_completed_by_a13: this child adds no proof completion claim for any Siegel branch",
  "public_checked_status_blocked: blueprint/todo/README surfaces must stay open until a checked root or branch wrapper validates locally",
  "repo_local_integration_debt_gate: no external anchor is used as completion evidence in this artifact"
]

/-- The A13 ledger-preservation gate records six conclusions. -/
theorem a13LeafLedgerGate_length :
    a13LeafLedgerGate.length = 6 :=
  rfl

/-- A13 does not close the public checked-status gate. -/
def a13PublicCheckedStatusAllowed : Bool :=
  false

/-- The A13 public checked-status gate is definitionally closed. -/
theorem a13PublicCheckedStatusAllowed_eq_false :
    a13PublicCheckedStatusAllowed = false :=
  rfl

/-- Repo-local integration-debt gate for the current package-split scope. -/
def repoLocalIntegrationDebtGate : List String := [
  "no terminal Siegel integral-points proof is claimed by this artifact",
  "pinned local mathlib search found S-integer, S-unit, scheme, finite-type, separated, and Northcott anchors",
  "pinned local mathlib search found NumberTheory.SiegelsLemma only as a false-positive linear-algebra lemma",
  "upstream mathlib search found no terminal Siegel integral-points theorem name as of 2026-05-01 snapshot 49f10344339f99fda2d3bb0aa1455bfa6801fd93",
  "external Lean 4 primary-source audit found no pin-ready Siegel integral-points proof on 2026-05-01; authenticated GitHub code search remains credential-blocked",
  "no external Lean 4 Siegel integral-points proof has been pinned, imported, or checked here",
  "current status is not_repo_local_closed with formalization_debt, not completed repo-local integration debt"
]

/--
A06 terminal-mathlib-anchor audit result.

The pinned repository mathlib commit is
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.  A fresh upstream mathlib snapshot
checked on 2026-05-01 was
`49f10344339f99fda2d3bb0aa1455bfa6801fd93`.  Searches over the relevant
`Mathlib/AlgebraicGeometry`, `Mathlib/NumberTheory`, and `Mathlib/RingTheory`
subtrees found support modules but no terminal theorem name for Siegel's
finiteness theorem for integral points on curves.
-/
def terminalMathlibAnchorAudit : List String := [
  "scope: S1-M-007-A06-terminal-mathlib-anchor",
  "pinned_mathlib_rev: 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "upstream_mathlib_rev_checked_2026-05-01: 49f10344339f99fda2d3bb0aa1455bfa6801fd93",
  "searched_terms: Siegel, Siegels, IntegralPoint, integral point, integral-points, integer point, SInteger, S-unit, SUnit, unit equation, UnitEquation",
  "searched_subtrees: Mathlib/AlgebraicGeometry, Mathlib/NumberTheory, Mathlib/RingTheory",
  "support_anchor_found: Mathlib.NumberTheory.SiegelsLemma with Int.Matrix.exists_ne_zero_int_vec_norm_le and Int.Matrix.exists_ne_zero_int_vec_norm_le'",
  "support_anchor_found: Mathlib.RingTheory.DedekindDomain.SInteger with Set.integer, Set.unit, and Set.unitEquivUnitsInteger",
  "terminal_siegel_integral_points_theorem_names_found: none",
  "a06_result: formalization_debt remains; no repo-local wrapper or upstream mathlib theorem can close StatementShape"
]

/-- The A06 terminal-mathlib-anchor audit records nine conclusions. -/
theorem terminalMathlibAnchorAudit_length :
    terminalMathlibAnchorAudit.length = 9 :=
  rfl

/-- A06 machine-readable child status. -/
def a06TerminalMathlibAnchorStatus : String :=
  "repo-local and upstream mathlib audit complete: no terminal Siegel integral-points theorem name found"

/-! ## A07 external Lean 4 primary-source audit -/

/--
One row in the A07 external Lean 4 source-repository audit.

Rows are discovery metadata only.  A row can close the parent theorem only if it
records a real terminal theorem name and a later integration pass pins, imports,
and checks that proof inside this repository.
-/
structure ExternalLean4PrimarySourceAuditRow where
  sourceSurface : String
  repositoryURL : String
  commitOrSnapshot : String
  searchedSurface : String
  candidateModuleOrPath : String
  theoremName : String
  result : String
  integrationAction : String
  deriving Repr, DecidableEq

/--
A07 external-anchor audit rows for Siegel's theorem on integral points.

This table deliberately excludes the A06 pinned/upstream mathlib terminal-name
search except where needed to record already-pinned non-mathlib Lake
dependencies.  No row supplies a terminal theorem for integral points on
curves.
-/
def externalLean4PrimarySourceAuditRows : List ExternalLean4PrimarySourceAuditRow := [
  {
    sourceSurface := "repo-local pinned non-mathlib Lake dependencies",
    repositoryURL := "https://github.com/leanprover-community/flt-regular and local Lake utility dependencies",
    commitOrSnapshot := "flt-regular 56161b6eb5281fbfe9c38f2bcec0f429ebc11a27; other utility packages as pinned in lake-manifest.json",
    searchedSurface :=
      "rg over pinned flt-regular, plausible, proofwidgets, batteries, Cli, checkdecls, aesop, importGraph, LeanSearchClient, and Qq sources for Siegel, IntegralPoint, integral point, SInteger, S-unit, SUnit, and UnitEquation",
    candidateModuleOrPath := "repository-wide *.lean and *.md search",
    theoremName := "none-found",
    result :=
      "no terminal Siegel integral-points theorem, integral-points-on-curves proof body, or relevant external arithmetic-geometry closure was found outside mathlib",
    integrationAction := "no pin/import/check target"
  },
  {
    sourceSurface := "Loogle public declaration search",
    repositoryURL := "https://loogle.lean-lang.org/json",
    commitOrSnapshot := "queried on 2026-05-01; endpoint exposes no repository commit hash",
    searchedSurface :=
      "declaration-name queries for quoted strings Siegel, IntegralPoint, and integral points",
    candidateModuleOrPath := "public mathlib declaration index",
    theoremName := "none-found",
    result :=
      "0 declarations whose name contains Siegel; 0 declarations whose name contains IntegralPoint; 0 declarations whose name contains integral points",
    integrationAction := "negative public declaration discovery only; no external proof to integrate"
  },
  {
    sourceSurface := "GitHub REST repository search API",
    repositoryURL := "https://api.github.com/search/repositories",
    commitOrSnapshot := "queried on 2026-05-01",
    searchedSurface :=
      "repository queries: Lean Siegel integral points; \"Siegel\" \"integral points\" Lean; \"arithmetic geometry\" Lean; \"algebraic geometry\" Lean theorem; Faltings Lean theorem",
    candidateModuleOrPath := "public repository metadata",
    theoremName := "none-found",
    result := "all recorded repository queries returned total_count 0",
    integrationAction := "no candidate repository identified by repository search"
  },
  {
    sourceSurface := "GitHub CLI and REST code-search gate",
    repositoryURL := "https://github.com/search and https://api.github.com/search/code",
    commitOrSnapshot := "queried on 2026-05-01",
    searchedSurface :=
      "gh auth status plus REST code-search attempts for \"Siegel\" \"integral points\" language:Lean and IntegralPoint language:Lean",
    candidateModuleOrPath := "GitHub code search",
    theoremName := "blocked",
    result :=
      "gh reported no logged-in GitHub host and no GH_TOKEN/GITHUB_TOKEN was present; unauthenticated REST code search returned rate-limit failure for IntegralPoint and did not return proof source files",
    integrationAction :=
      "concrete blocker: rerun authenticated GitHub code search before any future public completion claim"
  },
  {
    sourceSurface := "Reservoir package registry probes",
    repositoryURL := "https://reservoir.lean-lang.org/packages",
    commitOrSnapshot := "queried on 2026-05-01",
    searchedSurface :=
      "package-registry probes for Siegel via /api/packages?search=Siegel and /packages search query variants",
    candidateModuleOrPath := "Reservoir package listing",
    theoremName := "none-found",
    result :=
      "the /api/packages?search=Siegel path returned 404 and package-page query variants exposed only the generic packages listing, not a Siegel integral-points source package",
    integrationAction := "no Reservoir package candidate to pin"
  },
  {
    sourceSurface := "known arithmetic-geometry-adjacent Lean 4 project anchors",
    repositoryURL :=
      "https://github.com/MichaelStollBayreuth/Heights; https://github.com/smmercuri/adele-ring_locally-compact; https://github.com/ImperialCollegeLondon/FLT",
    commitOrSnapshot := "reused from sibling THM-M-0395 audit rows on 2026-05-01",
    searchedSurface :=
      "project metadata for height/Northcott/descent, adeles/local compactness, and FLT statement infrastructure",
    candidateModuleOrPath :=
      "Heights.Rat; Heights.Descent; AdeleRingLocallyCompact.NumberTheory.NumberField.AdeleRing; Mathlib.NumberTheory.FLT.Basic",
    theoremName :=
      "Projectivization.Rat.finite_of_mulHeight_le; NumberField.AdeleRing.locallyCompactSpace; FermatLastTheorem",
    result :=
      "arithmetic-geometry infrastructure or adjacent statement projects only; no terminal Siegel integral-points theorem for curves was identified",
    integrationAction :=
      "partial infrastructure anchors are not completion evidence; do not pin as a Siegel closure without a terminal theorem name"
  }
]

/-- The A07 external-primary-source audit table currently records six rows. -/
theorem externalLean4PrimarySourceAuditRows_length :
    externalLean4PrimarySourceAuditRows.length = 6 :=
  rfl

/-- This A07 pass found no terminal external Lean 4 proof body for Siegel. -/
def externalLean4PrimarySourceAuditFoundTerminalSiegelProof : Bool :=
  false

/-- The A07 terminal external-proof gate is definitionally negative. -/
theorem externalLean4PrimarySourceAuditFoundTerminalSiegelProof_eq_false :
    externalLean4PrimarySourceAuditFoundTerminalSiegelProof = false :=
  rfl

/-- Authenticated GitHub code search was unavailable in this worker environment. -/
def externalLean4AuthenticatedGitHubCodeSearchAvailable : Bool :=
  false

/-- The authenticated GitHub code-search gate remains closed for A07. -/
theorem externalLean4AuthenticatedGitHubCodeSearchAvailable_eq_false :
    externalLean4AuthenticatedGitHubCodeSearchAvailable = false :=
  rfl

/-- A07 machine-readable child status. -/
def a07ExternalAnchorStatus : String :=
  "external Lean 4 primary-source audit found no terminal Siegel integral-points proof; authenticated GitHub code search remains a concrete blocker before any future completion claim"

/--
Public non-target caution for the Stage1 blueprint backfill: the mathlib module
`Mathlib.NumberTheory.SiegelsLemma` proves Siegel's lemma about small nonzero
integer kernel vectors of underdetermined integer matrices.  It is not Siegel's
theorem on finiteness of integral points on curves, and it cannot close
`StatementShape`.
-/
def siegelsLemmaNonTargetCaution : String :=
  "Mathlib.NumberTheory.SiegelsLemma is a linear-algebra Siegel's lemma module for small nonzero integer kernel vectors of underdetermined integer matrices; it is not Siegel's integral-points theorem for curves."

/--
The actual conclusion shape supplied by the main pinned mathlib theorem
`Int.Matrix.exists_ne_zero_int_vec_norm_le`.

This typed anchor is intentionally matrix-linear algebra, not a curve or
integral-point finiteness statement.
-/
abbrev MathlibSiegelsLemmaMainConclusion
    {α : Type u} {β : Type v} [Fintype α] [Fintype β] (A : Matrix α β ℤ) : Prop :=
  ∃ t : β → ℤ,
    t ≠ 0 ∧
      A.mulVec t = 0 ∧
        ‖t‖ ≤ ((Fintype.card β : ℝ) * max 1 ‖A‖) ^
          ((Fintype.card α : ℝ) / ((Fintype.card β : ℝ) - (Fintype.card α : ℝ)))

/--
Pinned mathlib's `SiegelsLemma` main theorem checks against the local non-target
anchor.  This records the false-positive anchor without claiming any
integral-points theorem.
-/
theorem mathlib_siegelsLemma_main_nonTargetAnchor
    {α : Type u} {β : Type v} [Fintype α] [Fintype β]
    (A : Matrix α β ℤ)
    (hn : Fintype.card α < Fintype.card β) (hm : 0 < Fintype.card α) :
    MathlibSiegelsLemmaMainConclusion A := by
  simpa [MathlibSiegelsLemmaMainConclusion] using
    Int.Matrix.exists_ne_zero_int_vec_norm_le A hn hm

/-- M0387 machine-proof debt classification for this Stage1 artifact. -/
def machineProofDebtClassification : List String := [
  "mathematical_debt: inactive for the classical Siegel integral-points theorem",
  "formalization_debt: active; terminal proof body or checked wrapper is absent",
  "repo_local_integration_debt: not retained as a completed-state claim; no external proof is used as completion evidence"
]

/--
A05 audit result for curve, divisor, genus, affine-open, and boundary-support
APIs in the pinned repo-local mathlib.

The checked anchors below are sufficient for a future object-model layer to
name smooth relative dimension-one scheme morphisms, geometric integrality,
proper compactification morphisms, open immersions, affine opens, quasi-affine
schemes, and a set-theoretic boundary complement.  They are not yet sufficient
to freeze the final public Siegel statement, because this audit did not find a
repo-local algebraic curve divisor-support API, curve genus invariant/case
split API, or terminal integral-points theorem.
-/
def curveDivisorGenusAffineBoundaryAuditDecision : List String := [
  "curve_layer_available: Scheme morphisms can carry Smooth, SmoothOfRelativeDimension 1, and GeometricallyIntegral anchors",
  "compactification_layer_available: IsProper can type a proper compactification morphism anchor",
  "affine_open_layer_available: IsOpenImmersion, IsAffineOpen, and Scheme.IsQuasiAffine are typed anchors",
  "boundary_set_layer_available: an affine open boundary can be typed as the complement of an open-immersion range",
  "divisor_api_gap: no selected algebraic curve divisor-support API is checked in this artifact",
  "genus_api_gap: no selected curve genus invariant or genus case-split API is checked in this artifact",
  "statement_gate_result: exact curve/divisor/genus/affine-open/boundary APIs remain unselected for A03",
  "insufficient_for_siegel_closure: these anchors do not supply an integral-points finiteness theorem"
]

/-- The A05 curve/divisor/genus/affine-boundary audit records eight conclusions. -/
theorem curveDivisorGenusAffineBoundaryAuditDecision_length :
    curveDivisorGenusAffineBoundaryAuditDecision.length = 8 :=
  rfl

/-- A05 machine-readable child status. -/
def a05CurveApiStatus : String :=
  "repo-local audit complete: scheme-side curve/open anchors exist, but divisor support and genus APIs are not selected; no Siegel proof is closed"

/-- The A05 exact-object API gate remains closed. -/
def a05ExactObjectAPIsSelected : Bool := false

/-- A05 did not select enough object APIs to unblock the final public A03 namespace. -/
theorem a05ExactObjectAPIsSelected_eq_false :
    a05ExactObjectAPIsSelected = false :=
  rfl

/-- Audited mathlib anchor: schemes are available as the ambient curve object. -/
abbrev SchemeAnchor : Type (u + 1) :=
  Scheme.{u}

/-- Audited mathlib anchor: number fields are available as base fields. -/
abbrev NumberFieldAnchor (K : Type u) [Field K] : Prop :=
  NumberField K

/-- Audited mathlib anchor: finite-type morphisms are available for the curve
structure map.
-/
abbrev LocallyFiniteTypeAnchor {X Y : Scheme.{u}} (f : X ⟶ Y) : Prop :=
  LocallyOfFiniteType f

/-- Audited mathlib anchor: separated morphisms are available for the curve
structure map.
-/
abbrev SeparatedMorphismAnchor {X Y : Scheme.{u}} (f : X ⟶ Y) : Prop :=
  IsSeparated f

/-- Audited mathlib anchor: smooth morphisms are available for the curve map. -/
abbrev SmoothMorphismAnchor {X Y : Scheme.{u}} (f : X ⟶ Y) : Prop :=
  Smooth f

/-- Audited mathlib anchor: smooth morphisms of relative dimension one can type
the scheme-side curve condition.
-/
abbrev SmoothRelativeCurveAnchor {X Y : Scheme.{u}} (f : X ⟶ Y) : Prop :=
  SmoothOfRelativeDimension 1 f

/-- Audited mathlib anchor: geometric integrality is available as a morphism
property.
-/
abbrev GeometricallyIntegralMorphismAnchor {X Y : Scheme.{u}} (f : X ⟶ Y) : Prop :=
  GeometricallyIntegral f

/-- Audited mathlib anchor: proper morphisms can type the compactification side
of the selected public root candidate.
-/
abbrev ProperCompactificationMorphismAnchor {X Y : Scheme.{u}} (f : X ⟶ Y) : Prop :=
  IsProper f

/-- Audited mathlib anchor: open immersions are available for affine-open
inclusions into compactifications.
-/
abbrev OpenImmersionAnchor {U X : Scheme.{u}} (j : U ⟶ X) : Prop :=
  IsOpenImmersion j

/-- Audited mathlib anchor: affine opens are available inside a scheme. -/
abbrev AffineOpenAnchor (X : Scheme.{u}) (U : X.Opens) : Prop :=
  IsAffineOpen U

/-- Audited mathlib anchor: quasi-affine schemes are available for affine-curve
model bookkeeping.
-/
abbrev QuasiAffineSchemeAnchor (X : Scheme.{u}) : Prop :=
  X.IsQuasiAffine

/-- Audited boundary-support fallback: a boundary can at least be typed as a
set of points of a compactifying scheme.
-/
abbrev BoundarySupportSetAnchor (Xbar : Scheme.{u}) : Type u :=
  Set Xbar

/-- Set-theoretic boundary condition for an affine open immersion into a
compactifying scheme.

This is a typed fallback for A05, not a divisor-support API and not a genus
condition.
-/
abbrev BoundarySupportIsComplement {U Xbar : Scheme.{u}}
    (j : U ⟶ Xbar) (B : Set Xbar) : Prop :=
  B = (Set.range j)ᶜ

/-- The complement of an open-immersion range satisfies the local boundary
fallback by definition.
-/
theorem boundarySupportIsComplement_self {U Xbar : Scheme.{u}} (j : U ⟶ Xbar) :
    BoundarySupportIsComplement j ((Set.range j)ᶜ) :=
  rfl

/-- Minimal typed package for the A05 affine-open boundary audit.

The package records only an open immersion and its set-theoretic complement in
a compactifying scheme.  It deliberately does not claim a divisor support,
genus computation, or Siegel boundary theorem.
-/
structure AffineOpenBoundaryPackage where
  compactification : Scheme.{u}
  affineOpen : Scheme.{u}
  openImmersion : affineOpen ⟶ compactification
  openImmersion_isOpen : IsOpenImmersion openImmersion
  boundarySupport : Set compactification
  boundarySupport_eq_complement : boundarySupport = (Set.range openImmersion)ᶜ

/-- An A05 boundary package exposes the set-theoretic complement condition. -/
theorem AffineOpenBoundaryPackage.boundarySupport_isComplement
    (B : AffineOpenBoundaryPackage.{u}) :
    BoundarySupportIsComplement B.openImmersion B.boundarySupport :=
  B.boundarySupport_eq_complement

/-- Audited mathlib anchor: `S`-integers are available for fraction fields of
Dedekind domains.
-/
abbrev SIntegerSubalgebraAnchor
    (R : Type u) [CommRing R] [IsDedekindDomain R]
    (S : Set (IsDedekindDomain.HeightOneSpectrum R))
    (K : Type v) [Field K] [Algebra R K] [IsFractionRing R K] :
    Subalgebra R K :=
  S.integer K

/-- Audited mathlib anchor: `S`-units are available for fraction fields of
Dedekind domains.
-/
abbrev SUnitGroupAnchor
    (R : Type u) [CommRing R] [IsDedekindDomain R]
    (S : Set (IsDedekindDomain.HeightOneSpectrum R))
    (K : Type v) [Field K] [Algebra R K] [IsFractionRing R K] :
    Subgroup Kˣ :=
  S.unit K

/--
A04 audit result for `Mathlib.RingTheory.DedekindDomain.SInteger`.

`Set.integer` and `Set.unit` are sufficient as the local algebraic object layer:
they give the `S`-integer subalgebra and `S`-unit subgroup of the fraction field
of a Dedekind domain, with valuation characterizations outside `S`.  They are
not sufficient by themselves as a Siegel integral-points theorem closure:
the curve model, boundary support, integral-point predicate, S-unit equation
finiteness, and branch assembly remain separate proof/API obligations.
-/
def sIntegerSUnitAuditDecision : List String := [
  "sufficient_for_object_layer: Set.integer is a typed Subalgebra of the fraction field",
  "sufficient_for_object_layer: Set.unit is a typed Subgroup of field units with valuation-equals-one outside S",
  "sufficient_for_unit_bridge: Set.unitEquivUnitsInteger identifies S-units with units of S-integers",
  "insufficient_for_siegel_closure: no curve integral-point theorem, S-unit equation finiteness theorem, or branch assembly is supplied by this module"
]

/-- The A04 S-integer/S-unit audit records four local conclusions. -/
theorem sIntegerSUnitAuditDecision_length :
    sIntegerSUnitAuditDecision.length = 4 :=
  rfl

/-- A04 machine-readable child status. -/
def a04SIntegersStatus : String :=
  "repo-local audit complete: Set.integer/Set.unit are adequate object-layer anchors, not a terminal Siegel proof"

/-- Typed A04 anchor: membership in `S.integer` gives valuation at most one
outside `S`.
-/
theorem sIntegerAnchor_valuation_le_one
    (R : Type u) [CommRing R] [IsDedekindDomain R]
    (S : Set (IsDedekindDomain.HeightOneSpectrum R))
    (K : Type v) [Field K] [Algebra R K] [IsFractionRing R K]
    (x : SIntegerSubalgebraAnchor R S K)
    {v : IsDedekindDomain.HeightOneSpectrum R} (hv : v ∉ S) :
    v.valuation K (x : K) ≤ 1 :=
  Set.integer_valuation_le_one S K x hv

/-- Typed A04 anchor: membership in `S.unit` gives valuation exactly one
outside `S`.
-/
theorem sUnitAnchor_valuation_eq_one
    (R : Type u) [CommRing R] [IsDedekindDomain R]
    (S : Set (IsDedekindDomain.HeightOneSpectrum R))
    (K : Type v) [Field K] [Algebra R K] [IsFractionRing R K]
    (x : SUnitGroupAnchor R S K)
    {v : IsDedekindDomain.HeightOneSpectrum R} (hv : v ∉ S) :
    v.valuation K ((x : Kˣ) : K) = 1 :=
  Set.unit_valuation_eq_one S K x hv

/-- Typed A04 anchor: mathlib identifies `S`-units with units of the
`S`-integer subalgebra.
-/
abbrev SUnitUnitsOfSIntegerAnchor
    (R : Type u) [CommRing R] [IsDedekindDomain R]
    (S : Set (IsDedekindDomain.HeightOneSpectrum R))
    (K : Type v) [Field K] [Algebra R K] [IsFractionRing R K] :
    SUnitGroupAnchor R S K ≃* (SIntegerSubalgebraAnchor R S K)ˣ :=
  Set.unitEquivUnitsInteger S K

/-- Typed A04 anchor: with no inverted primes, `S.integer` is the base
subalgebra.
-/
theorem sIntegerAnchor_empty_eq_bot
    (R : Type u) [CommRing R] [IsDedekindDomain R]
    (K : Type v) [Field K] [Algebra R K] [IsFractionRing R K] :
    SIntegerSubalgebraAnchor R (∅ : Set (IsDedekindDomain.HeightOneSpectrum R)) K = ⊥ :=
  IsDedekindDomain.integer_empty R K

/-- Typed A04 anchor: inverting every height-one prime gives the whole
fraction field.
-/
theorem sIntegerAnchor_univ_eq_top
    (R : Type u) [CommRing R] [IsDedekindDomain R]
    (K : Type v) [Field K] [Algebra R K] [IsFractionRing R K] :
    SIntegerSubalgebraAnchor R (Set.univ : Set (IsDedekindDomain.HeightOneSpectrum R)) K = ⊤ :=
  IsDedekindDomain.integer_univ R K

/-! ## A08 genus-zero branch through S-unit equations -/

/--
Leaf split for the genus-zero branch of Siegel's theorem.

The leaves deliberately separate the geometric normalization of a genus-zero
compactification from the arithmetic `S`-unit equation finiteness input.  This
is checked bookkeeping for the future proof branch, not a proof of any leaf.
-/
inductive GenusZeroSUnitLeaf where
  | classifyCompactificationAsP1
  | chooseThreeBoundaryPoints
  | normalizeBoundaryToZeroOneInfinity
  | reduceIntegralPointsToSUnitEquation
  | closeFiniteSUnitEquationSolutions
  | packageAffineCurveFiniteness
  deriving DecidableEq, Repr

/-- Canonical A08 leaf order for the genus-zero/S-unit branch. -/
def genusZeroSUnitLeafSplit : List GenusZeroSUnitLeaf := [
  GenusZeroSUnitLeaf.classifyCompactificationAsP1,
  GenusZeroSUnitLeaf.chooseThreeBoundaryPoints,
  GenusZeroSUnitLeaf.normalizeBoundaryToZeroOneInfinity,
  GenusZeroSUnitLeaf.reduceIntegralPointsToSUnitEquation,
  GenusZeroSUnitLeaf.closeFiniteSUnitEquationSolutions,
  GenusZeroSUnitLeaf.packageAffineCurveFiniteness
]

/-- The A08 genus-zero/S-unit branch split has six leaves. -/
theorem genusZeroSUnitLeafSplit_length :
    genusZeroSUnitLeafSplit.length = 6 :=
  rfl

/-- M0387-level A08 leaf ledger for the genus-zero branch. -/
def genusZeroSUnitLeafBudgetLedger : List String := [
  "M0394.A08.L01 genus zero: classify the smooth projective compactification as P1; unchecked <=100",
  "M0394.A08.L02 boundary: extract at least three distinct points in the boundary support; unchecked <=100",
  "M0394.A08.L03 normalization: send three boundary points to 0, 1, and infinity by a PGL2 automorphism; unchecked <=100",
  "M0394.A08.L04 reduction: show integral points on P1 minus the normalized boundary give S-unit equation solutions; unchecked <=100",
  "M0394.A08.L05 arithmetic: prove or import finiteness for the relevant S-unit equation solution set; unchecked <=100",
  "M0394.A08.L06 packaging: transport S-unit equation finiteness back to the affine genus-zero curve; unchecked <=100"
]

/-- The A08 M0387 leaf ledger records six unchecked leaves. -/
theorem genusZeroSUnitLeafBudgetLedger_length :
    genusZeroSUnitLeafBudgetLedger.length = 6 :=
  rfl

/--
Typed branch-interface data for the genus-zero route.

The fields are explicit predicates because A05 has not yet selected concrete
curve-genus, divisor-support, boundary-cardinality, projective-line, or
automorphism APIs.  A completed branch must replace these predicates by real
object-level data and prove `finiteIntegralPoints`.
-/
structure GenusZeroSUnitBranchPackage
    (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K) where
  compactificationIsP1 : Prop
  boundaryCardAtLeastThree : Prop
  normalizedToZeroOneInfinity : Prop
  integralPointsReduceToSUnitEquation : Prop
  finiteSUnitEquationSolutions : Prop
  compactificationIsP1_proof : compactificationIsP1
  boundaryCardAtLeastThree_proof : boundaryCardAtLeastThree
  normalizedToZeroOneInfinity_proof : normalizedToZeroOneInfinity
  integralPointsReduceToSUnitEquation_proof : integralPointsReduceToSUnitEquation
  finiteSUnitEquationSolutions_proof : finiteSUnitEquationSolutions
  finiteIntegralPoints : {P : D.integralPoint | D.isIntegralPoint P}.Finite

/-- A completed A08 branch package exposes the integral-point finiteness target. -/
theorem GenusZeroSUnitBranchPackage.finite
    (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K)
    (P : GenusZeroSUnitBranchPackage K D) :
    {Q : D.integralPoint | D.isIntegralPoint Q}.Finite :=
  P.finiteIntegralPoints

/-- A completed A08 genus-zero package is a terminal package for that input. -/
def GenusZeroSUnitBranchPackage.toIntegralPointsPackage
    (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K)
    (P : GenusZeroSUnitBranchPackage K D) :
    SiegelIntegralPointsPackage K D where
  finiteIntegralPoints := P.finite

/--
If a future proof supplies an A08 package for every admissible genus-zero
input, then the selected `StatementShape` follows for the inputs routed through
that branch.  This theorem is only a transport lemma; all mathematical content
is in the hypothesis `h`.
-/
theorem statementShape_of_genusZeroSUnitBranchPackage
    (h : ∀ (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K),
      D.smoothCurve →
        D.geometricallyIntegralCurve →
          D.affineCurveModel →
            D.siegelBoundaryCondition →
              GenusZeroSUnitBranchPackage K D) :
    StatementShape.{u, v} :=
  fun K _ _ D hSmooth hGeom hAffine hBoundary =>
    (h K D hSmooth hGeom hAffine hBoundary).finite

/-- A08 machine-readable child status. -/
def a08GenusZeroSUnitStatus : String :=
  "branch interface recorded: P1 minus at least three boundary points is split through S-unit equation finiteness; no terminal S-unit equation proof or P1 normalization proof is claimed"

/-- A08 does not close the parent Siegel theorem in this artifact. -/
def a08GenusZeroSUnitBranchClosed : Bool := false

/-- The A08 branch closure gate is definitionally negative. -/
theorem a08GenusZeroSUnitBranchClosed_eq_false :
    a08GenusZeroSUnitBranchClosed = false :=
  rfl

/-! ## A09 genus-one / elliptic Weierstrass branch -/

/--
Leaf split for the genus-one/elliptic branch of Siegel's theorem.

The checked part of this child is the Weierstrass object layer and branch
interface.  The arithmetic finiteness theorem for integral affine points is
still a separate formalization obligation.
-/
inductive EllipticWeierstrassLeaf where
  | selectWeierstrassCurveAPI
  | exposeAffinePointType
  | exposeIntegralWeierstrassModel
  | defineSIntegralAffinePredicate
  | bridgeGenericIntegralPointsToAffinePoints
  | proveFiniteAffineIntegralPoints
  | packageGenusOneBranchFiniteness
  deriving DecidableEq, Repr

/-- Canonical A09 leaf order for the genus-one/elliptic Weierstrass branch. -/
def ellipticWeierstrassLeafSplit : List EllipticWeierstrassLeaf := [
  EllipticWeierstrassLeaf.selectWeierstrassCurveAPI,
  EllipticWeierstrassLeaf.exposeAffinePointType,
  EllipticWeierstrassLeaf.exposeIntegralWeierstrassModel,
  EllipticWeierstrassLeaf.defineSIntegralAffinePredicate,
  EllipticWeierstrassLeaf.bridgeGenericIntegralPointsToAffinePoints,
  EllipticWeierstrassLeaf.proveFiniteAffineIntegralPoints,
  EllipticWeierstrassLeaf.packageGenusOneBranchFiniteness
]

/-- The A09 elliptic/Weierstrass branch split has seven leaves. -/
theorem ellipticWeierstrassLeafSplit_length :
    ellipticWeierstrassLeafSplit.length = 7 :=
  rfl

/-- M0387-level A09 leaf ledger for the elliptic Weierstrass branch. -/
def ellipticWeierstrassLeafBudgetLedger : List String := [
  "M0394.A09.L01 Weierstrass API: use mathlib WeierstrassCurve K and WeierstrassCurve.IsElliptic; checked wrapper <=100",
  "M0394.A09.L02 affine points: use mathlib affine point type E⟮K⟯ for nonsingular K-points; checked wrapper <=100",
  "M0394.A09.L03 integral model: use WeierstrassCurve.IsIntegral and integralModel/baseChange anchors; checked wrapper <=100",
  "M0394.A09.L04 S-integrality: choose a concrete coordinate-level S-integral predicate on E⟮K⟯; unchecked <=100",
  "M0394.A09.L05 bridge: prove the generic integral-point predicate injects into the chosen affine Weierstrass S-integral predicate; unchecked <=100",
  "M0394.A09.L06 arithmetic finiteness: prove or import finiteness of S-integral affine points on the selected elliptic Weierstrass model; unchecked <=100",
  "M0394.A09.L07 packaging: transport affine finiteness back to the genus-one affine branch package; checked transport wrapper <=100 once L04-L06 are supplied"
]

/-- The A09 M0387 leaf ledger records seven leaves. -/
theorem ellipticWeierstrassLeafBudgetLedger_length :
    ellipticWeierstrassLeafBudgetLedger.length = 7 :=
  rfl

/-- Typed A09 anchor: mathlib's affine point type for a Weierstrass curve. -/
abbrev EllipticAffinePoint
    (K : Type u) [Field K] (E : WeierstrassCurve K) : Type u :=
  E⟮K⟯

/-- Checked A09 anchor: an elliptic Weierstrass curve has unit discriminant. -/
theorem ellipticWeierstrass_discriminant_isUnit
    (K : Type u) [Field K] (E : WeierstrassCurve K) [E.IsElliptic] :
    IsUnit E.Δ :=
  E.isUnit_Δ

/-- Typed A09 anchor: integral Weierstrass models over a base ring. -/
abbrev WeierstrassIntegralModelAnchor
    (R : Type v) [CommRing R] (K : Type u) [Field K] [Algebra R K]
    (E : WeierstrassCurve K) : Prop :=
  WeierstrassCurve.IsIntegral R E

/-- Checked A09 anchor: the selected integral model base-changes back to the curve. -/
theorem weierstrass_integralModel_baseChange_eq
    (R : Type v) [CommRing R] (K : Type u) [Field K] [Algebra R K]
    (E : WeierstrassCurve K) [WeierstrassIntegralModelAnchor R K E] :
    (WeierstrassCurve.integralModel R E).baseChange K = E :=
  WeierstrassCurve.baseChange_integralModel_eq R E

/--
Typed branch-interface data for the genus-one/elliptic route.

The curve and affine point model are concrete mathlib Weierstrass APIs.  The
`sIntegralAffinePoint` predicate is intentionally explicit because this Stage1
pass has not selected a coordinate-level `S`-integrality API or proved the
elliptic integral-points finiteness theorem.
-/
structure EllipticWeierstrassBranchPackage
    (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K) where
  curve : WeierstrassCurve K
  elliptic : curve.IsElliptic
  sIntegralAffinePoint : EllipticAffinePoint K curve → Prop
  fromIntegralPoint : D.integralPoint → EllipticAffinePoint K curve
  bridgeInjective : Function.Injective fromIntegralPoint
  bridgeMapsIntegralPoints :
    ∀ P : D.integralPoint, D.isIntegralPoint P → sIntegralAffinePoint (fromIntegralPoint P)
  finiteAffineSIntegralPoints :
    {P : EllipticAffinePoint K curve | sIntegralAffinePoint P}.Finite

/--
An A09 branch package exposes the integral-point finiteness target by injecting
the generic integral-point subtype into the finite affine Weierstrass
`S`-integral subtype.
-/
theorem EllipticWeierstrassBranchPackage.finite
    (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K)
    (P : EllipticWeierstrassBranchPackage K D) :
    {Q : D.integralPoint | D.isIntegralPoint Q}.Finite := by
  let f : D.integralPoint → EllipticAffinePoint K P.curve := P.fromIntegralPoint
  let T : Set (EllipticAffinePoint K P.curve) := {Q | P.sIntegralAffinePoint Q}
  have hImage : (f '' {Q : D.integralPoint | D.isIntegralPoint Q}).Finite := by
    refine P.finiteAffineSIntegralPoints.subset ?_
    intro Q hQ
    rcases hQ with ⟨Q0, hQ0, rfl⟩
    exact P.bridgeMapsIntegralPoints Q0 hQ0
  refine hImage.of_finite_image ?_
  exact P.bridgeInjective.injOn

/-- A completed A09 elliptic package is a terminal package for that input. -/
def EllipticWeierstrassBranchPackage.toIntegralPointsPackage
    (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K)
    (P : EllipticWeierstrassBranchPackage K D) :
    SiegelIntegralPointsPackage K D where
  finiteIntegralPoints := P.finite K D

/--
If a future proof supplies an A09 package for every admissible genus-one input,
then the selected `StatementShape` follows for inputs routed through that
branch.  The theorem is a transport lemma only; all arithmetic content is in
the hypothesis `h`.
-/
theorem statementShape_of_ellipticWeierstrassBranchPackage
    (h : ∀ (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K),
      D.smoothCurve →
        D.geometricallyIntegralCurve →
          D.affineCurveModel →
            D.siegelBoundaryCondition →
              EllipticWeierstrassBranchPackage K D) :
    StatementShape.{u, v} :=
  fun K _ _ D hSmooth hGeom hAffine hBoundary =>
    (h K D hSmooth hGeom hAffine hBoundary).finite K D

/-- A09 machine-readable child status. -/
def a09EllipticWeierstrassStatus : String :=
  "branch interface recorded with concrete WeierstrassCurve, E⟮K⟯, IsElliptic, and IsIntegral/integralModel anchors; S-integral coordinate predicate and arithmetic finiteness remain formalization debt"

/-- A09 does not close the parent Siegel theorem in this artifact. -/
def a09EllipticWeierstrassBranchClosed : Bool := false

/-- The A09 branch closure gate is definitionally negative. -/
theorem a09EllipticWeierstrassBranchClosed_eq_false :
    a09EllipticWeierstrassBranchClosed = false :=
  rfl

/-- Audited mathlib anchor: Northcott-style finiteness predicates are available
for height-like functions.
-/
abbrev NorthcottAnchor (α : Type v) (β : Type w) [LE β] (height : α → β) : Prop :=
  Northcott height

/-! ## A10 higher-genus branch through height/Northcott -/

/--
Route options for the higher-genus branch of Siegel's theorem.

The selected route in this artifact is the height/Northcott route because
pinned mathlib has a typed `Northcott` finiteness predicate.  The other
constructors remain recorded as audit alternatives, not completion evidence.
-/
inductive HigherGenusRoute where
  | heightNorthcott
  | diophantineApproximation
  | faltingsStyleInput
  | externalClosure
  deriving DecidableEq, Repr

/-- A10 route selected for the higher-genus branch. -/
def selectedHigherGenusRoute : HigherGenusRoute :=
  HigherGenusRoute.heightNorthcott

/-- The A10 selected route is height/Northcott. -/
theorem selectedHigherGenusRoute_eq_heightNorthcott :
    selectedHigherGenusRoute = HigherGenusRoute.heightNorthcott :=
  rfl

/--
Leaf split for the higher-genus branch.

The leaves separate curve-genus routing, height selection, bounded-height
input, Northcott finiteness, and the integration gate.  This is checked
bookkeeping for future proof work, not a proof of Siegel's theorem.
-/
inductive HigherGenusHeightNorthcottLeaf where
  | routeGenusAtLeastTwoInput
  | chooseHeightFunction
  | proveIntegralPointsHeightBounded
  | applyNorthcottFiniteness
  | auditDiophantineApproximationAlternative
  | auditFaltingsStyleAlternative
  | auditExternalClosureAlternative
  | packageHigherGenusBranchFiniteness
  deriving DecidableEq, Repr

/-- Canonical A10 leaf order for the higher-genus height/Northcott branch. -/
def higherGenusHeightNorthcottLeafSplit : List HigherGenusHeightNorthcottLeaf := [
  HigherGenusHeightNorthcottLeaf.routeGenusAtLeastTwoInput,
  HigherGenusHeightNorthcottLeaf.chooseHeightFunction,
  HigherGenusHeightNorthcottLeaf.proveIntegralPointsHeightBounded,
  HigherGenusHeightNorthcottLeaf.applyNorthcottFiniteness,
  HigherGenusHeightNorthcottLeaf.auditDiophantineApproximationAlternative,
  HigherGenusHeightNorthcottLeaf.auditFaltingsStyleAlternative,
  HigherGenusHeightNorthcottLeaf.auditExternalClosureAlternative,
  HigherGenusHeightNorthcottLeaf.packageHigherGenusBranchFiniteness
]

/-- The A10 higher-genus height/Northcott split has eight leaves. -/
theorem higherGenusHeightNorthcottLeafSplit_length :
    higherGenusHeightNorthcottLeafSplit.length = 8 :=
  rfl

/-- M0387-level A10 leaf ledger for the higher-genus branch. -/
def higherGenusHeightNorthcottLeafBudgetLedger : List String := [
  "M0394.A10.L01 routing: isolate genus at least two from the selected curve/genus API; unchecked <=100",
  "M0394.A10.L02 height: choose a concrete height function on rational or integral points of the selected curve model; unchecked <=100",
  "M0394.A10.L03 height bound: prove or import bounded height for integral points on the higher-genus affine curve; unchecked <=100",
  "M0394.A10.L04 Northcott: apply mathlib Northcott.finite_le to the bounded-height subset; checked transport wrapper <=100 once L02-L03 are supplied",
  "M0394.A10.L05 Diophantine approximation audit: identify Roth/Subspace-style inputs only if the height route is abandoned; unchecked <=100",
  "M0394.A10.L06 Faltings-style audit: identify a checked Faltings/Mordell input only as a dependency option, not as anchor-only closure; unchecked <=100",
  "M0394.A10.L07 external closure audit: if a terminal external Lean proof is found, pin/import/check before any completion claim; unchecked <=100",
  "M0394.A10.L08 packaging: transport the height/Northcott finiteness result back to the higher-genus branch package; checked transport wrapper <=100 once L01-L04 are supplied"
]

/-- The A10 M0387 leaf ledger records eight leaves. -/
theorem higherGenusHeightNorthcottLeafBudgetLedger_length :
    higherGenusHeightNorthcottLeafBudgetLedger.length = 8 :=
  rfl

/--
Typed branch-interface data for the higher-genus route.

The `genusAtLeastTwo` and `higherGenusRouteHypothesis` fields are explicit
predicates because A05 has not selected a concrete genus API.  The proof-bearing
part is deliberately narrow: if a future formalization supplies a Northcott
height and a bound for all integral points, mathlib's `Northcott.finite_le`
gives the finite integral-point subset.
-/
structure HigherGenusHeightNorthcottBranchPackage
    (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K) where
  genusAtLeastTwo : Prop
  genusAtLeastTwo_proof : genusAtLeastTwo
  higherGenusRouteHypothesis : Prop
  higherGenusRouteHypothesis_proof : higherGenusRouteHypothesis
  heightValue : Type w
  heightValueLE : LE heightValue
  height : D.integralPoint → heightValue
  northcottHeight : @Northcott D.integralPoint heightValue height heightValueLE
  heightBound : heightValue
  integralPointsHeightBounded :
    ∀ P : D.integralPoint, D.isIntegralPoint P → height P ≤ heightBound

/--
An A10 branch package exposes the integral-point finiteness target by applying
Northcott finiteness to the height-bounded subset.
-/
theorem HigherGenusHeightNorthcottBranchPackage.finite
    (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K)
    (P : HigherGenusHeightNorthcottBranchPackage K D) :
    {Q : D.integralPoint | D.isIntegralPoint Q}.Finite := by
  letI : LE P.heightValue := P.heightValueLE
  haveI : Northcott P.height := P.northcottHeight
  exact (Northcott.finite_le P.heightBound).subset
    (fun Q hQ => P.integralPointsHeightBounded Q hQ)

/-- A completed A10 higher-genus package is a terminal package for that input. -/
def HigherGenusHeightNorthcottBranchPackage.toIntegralPointsPackage
    (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K)
    (P : HigherGenusHeightNorthcottBranchPackage K D) :
    SiegelIntegralPointsPackage K D where
  finiteIntegralPoints := P.finite K D

/--
If a future proof supplies an A10 package for every admissible higher-genus
input, then the selected `StatementShape` follows for inputs routed through
that branch.  The theorem is a transport lemma only; the height bound and
genus routing are in the hypothesis `h`.
-/
theorem statementShape_of_higherGenusHeightNorthcottBranchPackage
    (h : ∀ (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K),
      D.smoothCurve →
        D.geometricallyIntegralCurve →
          D.affineCurveModel →
            D.siegelBoundaryCondition →
              HigherGenusHeightNorthcottBranchPackage K D) :
    StatementShape.{u, v} :=
  fun K _ _ D hSmooth hGeom hAffine hBoundary =>
    (h K D hSmooth hGeom hAffine hBoundary).finite K D

/-- A10 machine-readable child status. -/
def a10HigherGenusHeightNorthcottStatus : String :=
  "route selected: height/Northcott; checked transport applies Northcott.finite_le once a concrete height and integral-point height bound are supplied; Diophantine approximation, Faltings-style, and external-closure alternatives remain audit branches only"

/-- A10 does not close the parent Siegel theorem in this artifact. -/
def a10HigherGenusBranchClosed : Bool := false

/-- The A10 branch closure gate is definitionally negative. -/
theorem a10HigherGenusBranchClosed_eq_false :
    a10HigherGenusBranchClosed = false :=
  rfl

/-! ## A11 dedicated height/Northcott inequality audit ledger -/

/--
One row in the A11 height/Northcott audit ledger.

Rows are proof-planning data for the required inequalities.  A row may mention
a checked local transport wrapper, but no row claims a Siegel height inequality
unless the `repoLocalStatus` field says so explicitly.
-/
structure HeightNorthcottInequalityAuditRow where
  leafId : String
  requiredInput : String
  requiredInequalityOrFact : String
  checkedAnchorOrCandidate : String
  repoLocalStatus : String
  blockerOrNextStep : String
  m0387Gate : String
  deriving Repr, DecidableEq

/--
A11 dedicated ledger for the height/Northcott package required by the
higher-genus route.

The checked part is intentionally limited to the abstract Northcott extraction
from a bounded-height predicate.  The actual Siegel inequalities remain
unchecked until concrete curve, divisor, local height, and integrality APIs are
selected and proved or imported.
-/
def heightNorthcottInequalityAuditLedger : List HeightNorthcottInequalityAuditRow := [
  {
    leafId := "M0394.A11.H01",
    requiredInput := "concrete height object on the selected integral-point or rational-point type",
    requiredInequalityOrFact := "choose `height : D.integralPoint -> beta` with `[LE beta]` and `[Northcott height]`",
    checkedAnchorOrCandidate := "Northcott; AwesomeTheorems.Stage1.S1_M_007.northcottFiniteOfHeightBoundedSet",
    repoLocalStatus := "local_wrapper_upstream_mathlib for abstract Northcott only",
    blockerOrNextStep := "select a curve-compatible height API after A05 chooses the object model",
    m0387Gate := "unchecked concrete height selection; abstract wrapper checked <=100"
  },
  {
    leafId := "M0394.A11.H02",
    requiredInput := "comparison between the selected curve height and an ambient projective or coordinate height",
    requiredInequalityOrFact := "prove `height_curve P <= c1 * height_ambient P + c2` or a monotone equivalent usable by Northcott",
    checkedAnchorOrCandidate := "no checked curve-height comparison anchor in this artifact",
    repoLocalStatus := "formalization_debt",
    blockerOrNextStep := "audit projectivization/coordinate height APIs once the compactification map is fixed",
    m0387Gate := "unchecked <=100"
  },
  {
    leafId := "M0394.A11.H03",
    requiredInput := "local height decomposition at finite and infinite places",
    requiredInequalityOrFact := "decompose the global height into local contributions with constants depending only on `K`, `S`, and the model",
    checkedAnchorOrCandidate := "Mathlib.NumberTheory.Height.Basic and NumberField height modules are substrate only",
    repoLocalStatus := "formalization_debt",
    blockerOrNextStep := "select local absolute-value/place APIs and prove the decomposition for the chosen height",
    m0387Gate := "unchecked <=100"
  },
  {
    leafId := "M0394.A11.H04",
    requiredInput := "S-integrality outside the finite set of places",
    requiredInequalityOrFact := "show outside-`S` local contributions are controlled or vanish for integral points",
    checkedAnchorOrCandidate := "Set.integer_valuation_le_one; Set.unit_valuation_eq_one",
    repoLocalStatus := "local_wrapper_upstream_mathlib for S-integer/S-unit valuation anchors only",
    blockerOrNextStep := "bridge the generic integral-point predicate to these valuation statements",
    m0387Gate := "unchecked bridge <=100"
  },
  {
    leafId := "M0394.A11.H05",
    requiredInput := "boundary divisor or affine-open complement data",
    requiredInequalityOrFact := "turn boundary support into the local-height inequalities used by Siegel's argument",
    checkedAnchorOrCandidate := "AffineOpenBoundaryPackage is set-theoretic only",
    repoLocalStatus := "formalization_debt",
    blockerOrNextStep := "replace the set-theoretic boundary fallback by divisor/support APIs",
    m0387Gate := "unchecked <=100"
  },
  {
    leafId := "M0394.A11.H06",
    requiredInput := "global bounded-height theorem for integral points in the selected branch",
    requiredInequalityOrFact := "prove `forall P, D.isIntegralPoint P -> height P <= bound`",
    checkedAnchorOrCandidate := "finiteIntegralPointsOfNorthcottHeightBound supplies only the downstream transport",
    repoLocalStatus := "formalization_debt",
    blockerOrNextStep := "derive the bound from H02-H05 or import a terminal checked inequality package",
    m0387Gate := "unchecked <=100"
  },
  {
    leafId := "M0394.A11.H07",
    requiredInput := "abstract Northcott extraction",
    requiredInequalityOrFact := "from `[Northcott height]` and `T subset {x | height x <= bound}`, infer `T.Finite`",
    checkedAnchorOrCandidate := "Northcott.finite_le; northcottFiniteOfHeightBoundedSet",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    blockerOrNextStep := "none for the abstract extraction wrapper",
    m0387Gate := "checked <=100 for abstract extraction only"
  },
  {
    leafId := "M0394.A11.H08",
    requiredInput := "integral-point subset specialization",
    requiredInequalityOrFact := "apply H07 to `{P : D.integralPoint | D.isIntegralPoint P}`",
    checkedAnchorOrCandidate := "finiteIntegralPointsOfNorthcottHeightBound",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    blockerOrNextStep := "needs H01 and H06 for any concrete Siegel branch",
    m0387Gate := "checked <=100 for transport only"
  },
  {
    leafId := "M0394.A11.H09",
    requiredInput := "constant bookkeeping",
    requiredInequalityOrFact := "isolate all constants and prove they depend only on fixed `K`, `S`, compactification, divisor, and model data",
    checkedAnchorOrCandidate := "no checked constant bookkeeping API selected",
    repoLocalStatus := "formalization_debt",
    blockerOrNextStep := "create explicit constant records after the height and local-place APIs are selected",
    m0387Gate := "unchecked <=100"
  },
  {
    leafId := "M0394.A11.H10",
    requiredInput := "integration gate for any external height package",
    requiredInequalityOrFact := "if an external Lean height/Siegel package is found, pin/import/check it before using it as completion evidence",
    checkedAnchorOrCandidate := "repoLocalIntegrationDebtGate records no terminal external proof currently used",
    repoLocalStatus := "not_repo_local_closed; no repo_local_integration_debt retained as completed state",
    blockerOrNextStep := "authenticated external code search and Lake-pin feasibility remain future audit work",
    m0387Gate := "unchecked external-search follow-up; no completion claim"
  }
]

/-- The A11 height/Northcott inequality ledger records ten rows. -/
theorem heightNorthcottInequalityAuditLedger_length :
    heightNorthcottInequalityAuditLedger.length = 10 :=
  rfl

/--
Checked A11 Northcott extraction wrapper.

This is only the abstract finite-sublevel argument.  It does not construct the
height, prove an integrality height bound, or close any Siegel branch.
-/
theorem northcottFiniteOfHeightBoundedSet
    {α : Type v} {β : Type w} [LE β] (height : α → β) [Northcott height]
    (bound : β) (T : Set α)
    (hT : ∀ a, a ∈ T → height a ≤ bound) :
    T.Finite :=
  (Northcott.finite_le bound).subset hT

/--
Checked A11 specialization to the current integral-point predicate shape.

The mathematical content is entirely in the hypotheses selecting a Northcott
height and proving a bound for every integral point.
-/
theorem finiteIntegralPointsOfNorthcottHeightBound
    (K : Type u) [Field K] [NumberField K] (D : SiegelCurveInput.{u, v} K)
    {β : Type w} [LE β] (height : D.integralPoint → β) [Northcott height]
    (bound : β)
    (hBound : ∀ P : D.integralPoint, D.isIntegralPoint P → height P ≤ bound) :
    {P : D.integralPoint | D.isIntegralPoint P}.Finite :=
  northcottFiniteOfHeightBoundedSet height bound {P | D.isIntegralPoint P} hBound

/-- A11 machine-readable child status. -/
def a11HeightNorthcottAuditStatus : String :=
  "dedicated height/Northcott ledger created: abstract Northcott finite-sublevel extraction is locally checked; concrete Siegel height inequalities remain formalization debt"

/-- A11 records an audit ledger and checked transport wrappers, not a completed Siegel proof. -/
def a11HeightNorthcottPackageClosed : Bool :=
  false

/-- The A11 package closure gate is definitionally negative. -/
theorem a11HeightNorthcottPackageClosed_eq_false :
    a11HeightNorthcottPackageClosed = false :=
  rfl

/-! ## A12 corollary-wrapper gate -/

/--
Gate for `S1-M-007-A12-corollaries`.

The parent task permits Mordell, Thue, and plane-equation wrappers only after a
root theorem or a branch theorem is checked.  The current artifact has checked
transport wrappers and audit ledgers, but no checked root theorem and no closed
genus-zero, elliptic, or higher-genus branch theorem.  Therefore A12 records a
negative gate instead of adding corollary theorem statements.
-/
def a12RootOrBranchTheoremChecked : Bool :=
  false

/-- The A12 root-or-branch theorem gate is currently closed. -/
theorem a12RootOrBranchTheoremChecked_eq_false :
    a12RootOrBranchTheoremChecked = false :=
  rfl

/-- Machine-readable A12 status for the delayed corollary wrappers. -/
def a12CorollaryWrapperStatus : List String := [
  "A12 gate: no checked root theorem for SelectedPublicRoot is available",
  "A12 gate: no checked genus-zero, elliptic, or higher-genus branch theorem is closed",
  "Mordell wrapper: delayed until a root or relevant branch theorem is checked",
  "Thue wrapper: delayed until a root or relevant branch theorem is checked",
  "plane-equation wrapper: delayed until a root or relevant branch theorem is checked",
  "repo-local integration debt: none retained as completed-state debt; no external proof is used as wrapper evidence"
]

/-- The A12 corollary-wrapper status records six gate conclusions. -/
theorem a12CorollaryWrapperStatus_length :
    a12CorollaryWrapperStatus.length = 6 :=
  rfl

/-- A12 machine-readable child status. -/
def a12CorollaryWrapperGateStatus : String :=
  "blocked-negative: Mordell, Thue, and plane-equation wrappers are not added because no root or branch theorem is checked"

/-! ## A14 external-proof integration gate -/

/--
Candidate record for the A14 external-proof integration gate.

If `foundTerminalProof` is true, M0387 requires either
`pinnedImportedChecked` or `concreteBlockerRecorded` before any completion
claim.  Anchor-only evidence is deliberately separated so it cannot discharge
the gate.
-/
structure ExternalSiegelClosureCandidate where
  foundTerminalProof : Bool
  pinnedImportedChecked : Bool
  concreteBlockerRecorded : Bool
  anchorOnlyEvidenceOnly : Bool
  deriving Repr, DecidableEq

/--
A14 gate predicate: either no terminal external proof is currently accepted as
found, or a found proof has been pinned/imported/checked locally, or a concrete
integration blocker has been recorded.
-/
def A14IntegrationGate (C : ExternalSiegelClosureCandidate) : Prop :=
  C.foundTerminalProof = false ∨
    C.pinnedImportedChecked = true ∨
      C.concreteBlockerRecorded = true

/-- A14 gate closes in the current negative-search state. -/
theorem A14IntegrationGate.of_no_terminal_external_proof
    (C : ExternalSiegelClosureCandidate) (h : C.foundTerminalProof = false) :
    A14IntegrationGate C :=
  Or.inl h

/-- A14 gate closes for a found proof only after repo-local pin/import/check. -/
theorem A14IntegrationGate.of_pinned_imported_checked
    (C : ExternalSiegelClosureCandidate) (h : C.pinnedImportedChecked = true) :
    A14IntegrationGate C :=
  Or.inr (Or.inl h)

/-- A14 gate closes for a found proof only if a concrete blocker is recorded. -/
theorem A14IntegrationGate.of_concrete_blocker
    (C : ExternalSiegelClosureCandidate) (h : C.concreteBlockerRecorded = true) :
    A14IntegrationGate C :=
  Or.inr (Or.inr h)

/--
Current A14 candidate status.

The previous A06/A07 audits found support infrastructure and false positives,
but no terminal external Lean 4 proof of Siegel's integral-points theorem that
can be pinned, imported, and checked.  Therefore the current gate is the
negative-search branch, not an anchor-only completion claim.
-/
def currentA14ExternalSiegelClosureCandidate : ExternalSiegelClosureCandidate where
  foundTerminalProof := false
  pinnedImportedChecked := false
  concreteBlockerRecorded := false
  anchorOnlyEvidenceOnly := false

/-- The current A14 candidate satisfies the integration gate by negative search. -/
theorem currentA14IntegrationGate :
    A14IntegrationGate currentA14ExternalSiegelClosureCandidate :=
  A14IntegrationGate.of_no_terminal_external_proof _ rfl

/-- A14 does not authorize theorem completion in this artifact. -/
def a14CompletionAllowed : Bool :=
  false

/-- The A14 completion gate is definitionally closed. -/
theorem a14CompletionAllowed_eq_false :
    a14CompletionAllowed = false :=
  rfl

/-- A14 retains no completed-state repo-local integration debt. -/
def a14RepoLocalIntegrationDebtRetainedInCompletedState : Bool :=
  false

/-- The A14 repo-local integration-debt residue gate is definitionally clear. -/
theorem a14RepoLocalIntegrationDebtRetainedInCompletedState_eq_false :
    a14RepoLocalIntegrationDebtRetainedInCompletedState = false :=
  rfl

/-- Machine-readable A14 gate status for serial public backfill. -/
def a14IntegrationGateStatus : List String := [
  "scope: S1-M-007-A14-integration-gate",
  "current_external_terminal_siegel_proof_found: false",
  "current_pin_import_check_target: none",
  "current_concrete_integration_blocker: authenticated GitHub code search remains unavailable; no named terminal external proof is accepted as found",
  "anchor_only_completion_allowed: false",
  "repo_local_integration_debt_retained_in_completed_state: false",
  "parent_completion_effect: none; THM-M-0394 remains not_repo_local_closed with formalization_debt"
]

/-- The A14 integration-gate status records seven conclusions. -/
theorem a14IntegrationGateStatus_length :
    a14IntegrationGateStatus.length = 7 :=
  rfl

/-- Public integrator task text for the external-proof-found branch of A14. -/
def a14PublicBackfillProposal : String :=
  "If a terminal external Lean 4 proof of Siegel's integral-points theorem is found, record repository URL, commit SHA, license, Lean/Lake toolchain, module path, theorem names, and exact match to SelectedPublicRoot; then pin or vendor the dependency, import the terminal theorem under AwesomeTheorems.Stage1.S1_M_007, prove/check a local wrapper, and run `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_007.lean`. If pin/import/check is blocked, record the concrete blocker. Do not mark THM-M-0394 completed from anchor-only evidence."

/-! ## A15 public-surface synchronization gate -/

/--
Gate for `S1-M-007-A15-public-sync`.

Public README, metadata, blueprint, todo, and build-validation surfaces may be
synchronized only after a checked local root wrapper exists.  The current
artifact has statement shapes, audit ledgers, and transport wrappers, but no
checked wrapper for `SelectedPublicRoot`.
-/
def a15CheckedRootWrapperExists : Bool :=
  false

/-- The A15 checked-root-wrapper prerequisite is currently absent. -/
theorem a15CheckedRootWrapperExists_eq_false :
    a15CheckedRootWrapperExists = false :=
  rfl

/-- Public surfaces that must be updated together once A15 is unblocked. -/
def a15PublicSyncSurfaces : List String := [
  "README theorem-status entry for THM-M-0394",
  "machine-readable theorem metadata/status surface",
  "Docs/Stage1_Blueprint.md S1-M-007 checklist line",
  "Docs/todos_20260430.md follow-up task surface",
  "build-validation record for the checked local Lean command"
]

/-- A15 tracks five public sync surfaces. -/
theorem a15PublicSyncSurfaces_length :
    a15PublicSyncSurfaces.length = 5 :=
  rfl

/-- Machine-readable A15 status for serial public backfill. -/
def a15PublicSyncStatus : List String := [
  "scope: S1-M-007-A15-public-sync",
  "checked_root_wrapper_exists: false",
  "public_sync_allowed_now: false",
  "reason: no local proof body, pinned mathlib wrapper, or pinned external dependency wrapper proves SelectedPublicRoot",
  "repo_local_integration_debt_retained_in_completed_state: false",
  "parent_completion_effect: none; THM-M-0394 remains not_repo_local_closed with formalization_debt"
]

/-- The A15 public-sync status records six gate conclusions. -/
theorem a15PublicSyncStatus_length :
    a15PublicSyncStatus.length = 6 :=
  rfl

/-- A15 does not authorize public documentation edits in this child artifact. -/
def a15PublicSyncAllowedNow : Bool :=
  false

/-- The A15 public-sync gate is definitionally closed. -/
theorem a15PublicSyncAllowedNow_eq_false :
    a15PublicSyncAllowedNow = false :=
  rfl

/-- Public integrator task text for A15 once a checked wrapper exists. -/
def a15PublicBackfillProposal : String :=
  "Keep S1-M-007-A15 unchecked until a repo-local checked wrapper for SelectedPublicRoot exists and `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_007.lean` passes. Once that prerequisite is met, update README, theorem metadata, Docs/Stage1_Blueprint.md, Docs/todos_20260430.md, and the build-validation record in the same serial integration patch. The public status must say whether the proof body is local, from pinned mathlib, or from a pinned external dependency, and it must not retain repo_local_integration_debt as a completed-state residue."

end AwesomeTheorems.Stage1.S1_M_007
