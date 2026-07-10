import Mathlib.AlgebraicGeometry.RationalMap
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Noetherian
import Mathlib.AlgebraicGeometry.Sites.BigZariski
import Mathlib.AlgebraicGeometry.Sites.Small
import Mathlib.AlgebraicGeometry.Modules.Tilde

/-!
# S1-M-028 / THM-M-0148: Mori minimal model program

This Stage1 artifact records a conservative Lean 4 statement shape for the
Mori minimal model program as a birational-classification theorem for
higher-dimensional algebraic varieties.

The current repo-local Lean surface checks the scheme/rational-map object
boundary supplied by mathlib.  It does not claim a proof of the MMP, and it
does not introduce placeholder axioms for terminal singularities,
`Q`-factoriality, canonical divisors, nefness, flips, or Mori fiber spaces.
Those still-missing notions are explicit predicate parameters in the statement
shape below.
-/

noncomputable section

open CategoryTheory
open AlgebraicGeometry

universe u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_028

/--
Mathlib-backed lower-bound hypotheses for the scheme object that an MMP input
must refine.  This is intentionally not a definition of a projective
`Q`-factorial terminal variety; those conditions remain explicit parameters in
`StatementShape`.
-/
def SchemeMMPInput {B X : Scheme.{u}} (π : X ⟶ B) : Prop :=
  IsProper π ∧ LocallyOfFiniteType π ∧ IsIntegral X

/--
Stage1 birational witness shape using mathlib rational maps.

This only records the two rational maps needed at the object-model boundary.
The future proof package must replace or refine this with the exact mathlib
birational-equivalence API once the relevant algebraic-geometry branch exists.
-/
def RationalMapBirationalWitness (X Y : Scheme.{u}) : Prop :=
  Nonempty (X ⤏ Y) ∧ Nonempty (Y ⤏ X)

/--
Explicit-field Stage1 data for the MMP statement-normalization child task.

The universe is the Lean universe parameter `u`.  The base, source, and
structure morphism are concrete mathlib `Scheme` fields.  The remaining
MMP-specific assumptions and outputs are deliberately `Prop`-valued placeholder
fields until mathlib supplies terminal APIs for projectivity, terminal
singularities, `Q`-factoriality, canonical divisor nefness, minimal models, and
Mori fiber spaces.
-/
structure MMPStatementData : Type (u + 1) where
  base : Scheme.{u}
  source : Scheme.{u}
  structureMap : source ⟶ base
  projectiveOverBase : Prop
  normalVariety : Prop
  terminalSingularities : Prop
  qFactorial : Prop
  canonicalDivisorExists : Prop
  minimalModelOutput : (Y : Scheme.{u}) → (Y ⟶ base) → Prop
  moriFiberSpaceOutput : (Z : Scheme.{u}) → (Z ⟶ base) → Prop

/-- Mathlib-backed hypotheses currently available around the explicit MMP input. -/
def MMPMathlibHypotheses (D : MMPStatementData.{u}) : Prop :=
  IsProper D.structureMap ∧
    LocallyOfFiniteType D.structureMap ∧
    IsIntegral D.source ∧
    IsLocallyNoetherian D.base ∧
    IsLocallyNoetherian D.source

/-- MMP-specific input placeholders that must be replaced by real definitions later. -/
def MMPPlaceholderHypotheses (D : MMPStatementData.{u}) : Prop :=
  D.projectiveOverBase ∧
    D.normalVariety ∧
    D.terminalSingularities ∧
    D.qFactorial ∧
    D.canonicalDivisorExists

/-- The normalized minimal-model-or-Mori-fiber-space output alternative. -/
def MMPOutputAlternative (D : MMPStatementData.{u}) : Prop :=
  (∃ (Y : Scheme.{u}) (μ : Y ⟶ D.base),
    RationalMapBirationalWitness D.source Y ∧ D.minimalModelOutput Y μ) ∨
  (∃ (Z : Scheme.{u}) (ρ : Z ⟶ D.base),
    RationalMapBirationalWitness D.source Z ∧ D.moriFiberSpaceOutput Z ρ)

/--
Normalized statement shape with explicit universe/base/hypothesis/output fields.

This is the integration-ready child artifact for `S1-M-028-C001`.  It is a
formal target only: no proof of this proposition is provided or claimed here.
-/
def ExplicitFieldStatementShape : Prop :=
  ∀ D : MMPStatementData.{u},
    MMPMathlibHypotheses D →
    MMPPlaceholderHypotheses D →
      MMPOutputAlternative D

/-- The explicit-field statement unfolds to its normalized input/output form. -/
theorem explicitFieldStatementShape_iff :
    ExplicitFieldStatementShape.{u} ↔
      ∀ D : MMPStatementData.{u},
        MMPMathlibHypotheses D →
        MMPPlaceholderHypotheses D →
          MMPOutputAlternative D :=
  Iff.rfl

/-- Projection wrapper for the explicit-field normalized statement. -/
theorem mmpOutputAlternative_of_explicitFieldStatementShape
    (h : ExplicitFieldStatementShape.{u})
    (D : MMPStatementData.{u})
    (hMathlib : MMPMathlibHypotheses D)
    (hMMP : MMPPlaceholderHypotheses D) :
      MMPOutputAlternative D :=
  h D hMathlib hMMP

/--
Normalized statement shape for the Mori minimal model program.

`ProjectiveTerminalQFactorial π` packages the source-side assumptions beyond
the currently audited mathlib lower bound, including projectivity, normality,
terminal singularities, and `Q`-factoriality.  `MinimalModelOutput π μ` and
`MoriFiberSpaceOutput π ρ` are the two possible outcomes: a birational minimal
model with nef canonical class, or a birational Mori fiber space.
-/
def StatementShape
    (ProjectiveTerminalQFactorial :
      {B X : Scheme.{u}} → (X ⟶ B) → Prop)
    (MinimalModelOutput :
      {B X Y : Scheme.{u}} → (X ⟶ B) → (Y ⟶ B) → Prop)
    (MoriFiberSpaceOutput :
      {B X Z : Scheme.{u}} → (X ⟶ B) → (Z ⟶ B) → Prop) : Prop :=
  ∀ ⦃B X : Scheme.{u}⦄ (π : X ⟶ B),
    SchemeMMPInput π →
    ProjectiveTerminalQFactorial π →
      (∃ (Y : Scheme.{u}) (μ : Y ⟶ B),
        RationalMapBirationalWitness X Y ∧ MinimalModelOutput π μ) ∨
      (∃ (Z : Scheme.{u}) (ρ : Z ⟶ B),
        RationalMapBirationalWitness X Z ∧ MoriFiberSpaceOutput π ρ)

/-- The statement shape unfolds to the explicit MMP alternative. -/
theorem statementShape_iff
    (ProjectiveTerminalQFactorial :
      {B X : Scheme.{u}} → (X ⟶ B) → Prop)
    (MinimalModelOutput :
      {B X Y : Scheme.{u}} → (X ⟶ B) → (Y ⟶ B) → Prop)
    (MoriFiberSpaceOutput :
      {B X Z : Scheme.{u}} → (X ⟶ B) → (Z ⟶ B) → Prop) :
    StatementShape ProjectiveTerminalQFactorial
        MinimalModelOutput MoriFiberSpaceOutput ↔
      ∀ ⦃B X : Scheme.{u}⦄ (π : X ⟶ B),
        SchemeMMPInput π →
        ProjectiveTerminalQFactorial π →
          (∃ (Y : Scheme.{u}) (μ : Y ⟶ B),
            RationalMapBirationalWitness X Y ∧ MinimalModelOutput π μ) ∨
          (∃ (Z : Scheme.{u}) (ρ : Z ⟶ B),
            RationalMapBirationalWitness X Z ∧ MoriFiberSpaceOutput π ρ) :=
  Iff.rfl

/--
Checked local projection wrapper: a future proof of `StatementShape` supplies
the minimal-model-or-Mori-fiber-space alternative for each fixed input.
-/
theorem mmpAlternative_of_statementShape
    {ProjectiveTerminalQFactorial :
      {B X : Scheme.{u}} → (X ⟶ B) → Prop}
    {MinimalModelOutput :
      {B X Y : Scheme.{u}} → (X ⟶ B) → (Y ⟶ B) → Prop}
    {MoriFiberSpaceOutput :
      {B X Z : Scheme.{u}} → (X ⟶ B) → (Z ⟶ B) → Prop}
    (h : StatementShape ProjectiveTerminalQFactorial
        MinimalModelOutput MoriFiberSpaceOutput)
    {B X : Scheme.{u}} (π : X ⟶ B)
    (hπ : SchemeMMPInput π)
    (hterm : ProjectiveTerminalQFactorial π) :
      (∃ (Y : Scheme.{u}) (μ : Y ⟶ B),
        RationalMapBirationalWitness X Y ∧ MinimalModelOutput π μ) ∨
      (∃ (Z : Scheme.{u}) (ρ : Z ⟶ B),
        RationalMapBirationalWitness X Z ∧ MoriFiberSpaceOutput π ρ) :=
  h π hπ hterm

/-! ## Partial-branch scope for the MMP frontier -/

/--
Top-level proof branches for a future Mori minimal model program
formalization.

These are branch labels, not assumptions.  They make the partial-branch scope
visible to Stage1 audit tooling while the terminal MMP APIs remain unavailable
in the repo-local Lean closure.
-/
inductive MMPPartialBranch where
  | inputModelAndBirationalBoundary
  | coneTheoremAndExtremalRays
  | contractionTheorem
  | divisorialContractionBranch
  | flipExistenceBranch
  | flipTerminationBranch
  | minimalModelOutputBranch
  | moriFiberSpaceOutputBranch
  | repoLocalClosureGate
  deriving DecidableEq, Repr

/--
Typed metadata for one MMP branch.

`repoLocalClosed` is intentionally `false` for every current row.  The ledger
records formalization work packages and their M0387 gates; it does not assert a
proof of the MMP or of any unimported Mori-program theorem.
-/
structure MMPPartialBranchAudit where
  branch : MMPPartialBranch
  code : String
  title : String
  statementBoundary : String
  mathlibSupport : String
  missingMMPApi : String
  currentStatus : String
  nextGate : String
  leafBudgetStatus : String
  repoLocalClosed : Bool
  deriving DecidableEq, Repr

/--
M0387-level partial-branch ledger for `THM-M-0148`.

The split isolates the mathlib-backed scheme/rational-map boundary from the
deep MMP packages: cone theorem, contraction theorem, divisorial contractions,
flips, termination, and the two terminal output alternatives.
-/
def mmpPartialBranchLedger : List MMPPartialBranchAudit := [
  {
    branch := MMPPartialBranch.inputModelAndBirationalBoundary
    code := "MMP-PB-01"
    title := "input model and birational boundary"
    statementBoundary :=
      "Base scheme, source scheme, structure morphism, proper finite-type integral input, and rational-map birational witness."
    mathlibSupport :=
      "Scheme, morphisms, IsProper, LocallyOfFiniteType, IsIntegral, IsLocallyNoetherian, and Scheme.RationalMap validate locally."
    missingMMPApi :=
      "Projectivity over the base, normality, terminal singularities, Q-factoriality, and canonical divisor data are still placeholder fields."
    currentStatus :=
      "partial_checked_support: object-level and rational-map boundary is repo-local Lean checked."
    nextGate :=
      "Replace placeholder input predicates by selected mathlib or pinned external definitions when available."
    leafBudgetStatus :=
      "support leaf checked; MMP-specific input leaves remain unchecked."
    repoLocalClosed := false
  },
  {
    branch := MMPPartialBranch.coneTheoremAndExtremalRays
    code := "MMP-PB-02"
    title := "cone theorem and extremal-ray decomposition"
    statementBoundary :=
      "Relative cone of curves, K-negative extremal rays, local finiteness, and decomposition of the negative part."
    mathlibSupport :=
      "Adjacent Stage1 artifact S1_M_039 records a Mori-cone statement shape, but no terminal cone theorem."
    missingMMPApi :=
      "Numerical curve classes, Mori cone, klt or terminal pair package, extremal rays, and K-negative intersection theory."
    currentStatus :=
      "formalization_debt: cone-theorem branch has only statement-shape support, not a proof body."
    nextGate :=
      "Pin or implement a cone-theorem API and connect its output to the chosen MMP step construction."
    leafBudgetStatus :=
      "unchecked; split cone construction, extremal-ray extraction, and local-finiteness proof into <=100-step leaves."
    repoLocalClosed := false
  },
  {
    branch := MMPPartialBranch.contractionTheorem
    code := "MMP-PB-03"
    title := "contraction theorem for negative extremal rays"
    statementBoundary :=
      "For each K-negative extremal ray, produce the associated contraction morphism over the base."
    mathlibSupport :=
      "Proper morphism and categorical composition substrate is available, but no Mori contraction theorem is imported."
    missingMMPApi :=
      "Extremal contraction existence, relative Picard and numerical equivalence infrastructure, and contraction-morphism properties."
    currentStatus :=
      "formalization_debt: contraction theorem is not repo-local closed."
    nextGate :=
      "Validate the contraction theorem as a local proof body, mathlib wrapper, or pinned external dependency."
    leafBudgetStatus :=
      "unchecked; ray-to-morphism construction and contraction properties require separate leaves."
    repoLocalClosed := false
  },
  {
    branch := MMPPartialBranch.divisorialContractionBranch
    code := "MMP-PB-04"
    title := "divisorial contraction step"
    statementBoundary :=
      "When an extremal contraction is divisorial, update the model over the base and preserve the admissible MMP input conditions."
    mathlibSupport :=
      "Scheme morphisms and rational maps provide only the ambient object boundary."
    missingMMPApi :=
      "Exceptional divisors, discrepancy control, preservation of terminal Q-factorial conditions, and canonical divisor transform."
    currentStatus :=
      "formalization_debt: divisorial-step preservation is not formalized in this repo."
    nextGate :=
      "Choose the divisorial-contraction API and prove the input-preservation bridge used by the MMP iteration."
    leafBudgetStatus :=
      "unchecked; exceptional locus, discrepancy, and update-map preservation must be split."
    repoLocalClosed := false
  },
  {
    branch := MMPPartialBranch.flipExistenceBranch
    code := "MMP-PB-05"
    title := "flip existence step"
    statementBoundary :=
      "When the contraction is small, produce the flipped model and the compatible birational correspondence."
    mathlibSupport :=
      "Current repo-local support stops at generic scheme and rational-map objects."
    missingMMPApi :=
      "Small contractions, flips, relative Proj construction for canonical algebras, and preservation of terminal Q-factoriality."
    currentStatus :=
      "formalization_debt: flip existence is a deep missing MMP package."
    nextGate :=
      "Import or formalize the selected flip-existence theorem and expose the exact branch interface."
    leafBudgetStatus :=
      "unchecked; construction, compatibility, and preservation leaves exceed one local budget."
    repoLocalClosed := false
  },
  {
    branch := MMPPartialBranch.flipTerminationBranch
    code := "MMP-PB-06"
    title := "termination or partial-run stopping gate"
    statementBoundary :=
      "Either prove termination of the MMP run in the chosen dimension/singularity scope, or record a bounded partial-run frontier."
    mathlibSupport :=
      "No ordinal, measure, discrepancy, or dimension-specific MMP termination package is connected to this statement."
    missingMMPApi :=
      "Termination of flips, special termination, scaling variants, and dimension-specific hypotheses."
    currentStatus :=
      "formalization_debt: no repo-local termination proof or checked partial-run theorem is present."
    nextGate :=
      "Select the intended scope: full termination, dimension-bounded termination, or explicit partial-run statement."
    leafBudgetStatus :=
      "unchecked; termination measure, monotonicity, and no-infinite-chain branches must be separated."
    repoLocalClosed := false
  },
  {
    branch := MMPPartialBranch.minimalModelOutputBranch
    code := "MMP-PB-07"
    title := "minimal-model output branch"
    statementBoundary :=
      "If the run reaches a nef canonical divisor model, produce a birational minimal model over the base."
    mathlibSupport :=
      "RationalMapBirationalWitness gives only the current birational witness boundary."
    missingMMPApi :=
      "Canonical divisor, nefness, minimal-model definition, and proof that the final model satisfies those properties."
    currentStatus :=
      "formalization_debt: output predicate remains a placeholder field."
    nextGate :=
      "Replace MinimalModelOutput by concrete definitions and prove the final-model branch from the iteration package."
    leafBudgetStatus :=
      "unchecked; nefness, birationality, and base-compatibility leaves remain open."
    repoLocalClosed := false
  },
  {
    branch := MMPPartialBranch.moriFiberSpaceOutputBranch
    code := "MMP-PB-08"
    title := "Mori-fiber-space output branch"
    statementBoundary :=
      "If the run exits through negative canonical class, produce a birational Mori fiber space over the base."
    mathlibSupport :=
      "Rational-map witnesses and scheme morphisms are available as object-level support only."
    missingMMPApi :=
      "Relative Picard rank, Fano-type fiber condition, contraction to lower-dimensional base, and Mori-fiber-space definition."
    currentStatus :=
      "formalization_debt: Mori fiber space output is still abstract."
    nextGate :=
      "Define or import Mori fiber spaces and connect the terminal contraction branch to that definition."
    leafBudgetStatus :=
      "unchecked; contraction, dimension drop, relative rank, and positivity branches need separate leaves."
    repoLocalClosed := false
  },
  {
    branch := MMPPartialBranch.repoLocalClosureGate
    code := "MMP-PB-09"
    title := "repo-local proof closure gate"
    statementBoundary :=
      "A completion claim requires a local proof body, mathlib wrapper theorem, or pinned external dependency proving StatementShape or ExplicitFieldStatementShape."
    mathlibSupport :=
      "Current validation checks this metadata and the statement boundary only."
    missingMMPApi :=
      "All terminal MMP proof packages remain outside the repo-local Lean closure."
    currentStatus :=
      "not_repo_local_closed: no theorem completion is claimed and no anchor-only proof is accepted."
    nextGate :=
      "After any external proof discovery, pin/import/check it or record a concrete integration blocker before completion."
    leafBudgetStatus :=
      "gate leaf open; no completed-state repo_local_integration_debt is retained."
    repoLocalClosed := false
  }
]

/-- The partial-branch ledger currently has nine MMP frontier rows. -/
theorem mmpPartialBranchLedger_length : mmpPartialBranchLedger.length = 9 :=
  rfl

/-- No row in the partial-branch ledger is claimed as repo-local MMP closure. -/
theorem mmpPartialBranchLedger_no_repoLocalClosed_claim :
    mmpPartialBranchLedger.map MMPPartialBranchAudit.repoLocalClosed =
      [false, false, false, false, false, false, false, false, false] :=
  rfl

/-- The branch codes are the public `MMP-PB-01` through `MMP-PB-09` queue. -/
theorem mmpPartialBranchLedger_codes :
    mmpPartialBranchLedger.map MMPPartialBranchAudit.code =
      ["MMP-PB-01", "MMP-PB-02", "MMP-PB-03", "MMP-PB-04", "MMP-PB-05",
        "MMP-PB-06", "MMP-PB-07", "MMP-PB-08", "MMP-PB-09"] :=
  rfl

/-! ## Mathlib object-model audit for the MMP boundary -/

/--
One row of the public object-model audit requested for the Mori minimal model
program slot.

`repoLocalCheckedSupport` means only that the named mathlib object/API is
available in this repo-local Lean closure.  It is not a proof-completion flag
for the MMP branch itself.
-/
structure MMPObjectModelAudit where
  code : String
  requestedObject : String
  mathlibAnchor : String
  importModule : String
  roleForMMPBoundary : String
  repoLocalCheck : String
  remainingMMPGap : String
  repoLocalCheckedSupport : Bool
  deriving DecidableEq, Repr

/--
Repo-local checked object-model audit for the public `S1-M-028-C002` task.

The table deliberately distinguishes mathlib substrate from MMP-specific
definitions.  `Scheme`, affine `Spec`, integral/noetherian hypotheses,
morphism-property predicates, rational maps, sheaves, sites, and module sheaves
are available as anchors.  Terminal singularities, `Q`-factoriality, canonical
divisors, nefness, flips, contractions, minimal models, and Mori fiber spaces
remain future formalization packages.
-/
def mmpObjectModelAudit : List MMPObjectModelAudit := [
  {
    code := "MMP-OM-01"
    requestedObject := "Scheme"
    mathlibAnchor := "AlgebraicGeometry.Scheme"
    importModule := "Mathlib.AlgebraicGeometry.Scheme"
    roleForMMPBoundary :=
      "Ambient category for bases, models, and structure morphisms in the normalized statement."
    repoLocalCheck :=
      "#check Scheme; used by MMPStatementData, SchemeMMPInput, and StatementShape."
    remainingMMPGap :=
      "No bundled projective normal terminal Q-factorial variety object is present here."
    repoLocalCheckedSupport := true
  },
  {
    code := "MMP-OM-02"
    requestedObject := "Spec"
    mathlibAnchor := "AlgebraicGeometry.Spec and Scheme.Spec.map"
    importModule := "Mathlib.AlgebraicGeometry.Scheme"
    roleForMMPBoundary :=
      "Affine charts, affine cover reductions, and spectrum maps available for local algebraic-geometry infrastructure."
    repoLocalCheck :=
      "#check Spec; #check Scheme.Spec.map."
    remainingMMPGap :=
      "Affine spectrum support does not by itself define projectivity, canonical divisors, or MMP steps."
    repoLocalCheckedSupport := true
  },
  {
    code := "MMP-OM-03"
    requestedObject := "Scheme.IsIntegral / IsIntegral"
    mathlibAnchor := "AlgebraicGeometry.IsIntegral"
    importModule := "Mathlib.AlgebraicGeometry.Properties"
    roleForMMPBoundary :=
      "Integral source hypothesis used in the current mathlib-backed lower-bound input predicate."
    repoLocalCheck :=
      "#check IsIntegral; used by SchemeMMPInput and MMPMathlibHypotheses."
    remainingMMPGap :=
      "Integral is only a substrate condition; normality and terminal singularities are still placeholders."
    repoLocalCheckedSupport := true
  },
  {
    code := "MMP-OM-04"
    requestedObject := "IsLocallyNoetherian"
    mathlibAnchor := "AlgebraicGeometry.IsLocallyNoetherian"
    importModule := "Mathlib.AlgebraicGeometry.Noetherian"
    roleForMMPBoundary :=
      "Noetherian base/source hypotheses for finite-type algebraic-geometry arguments."
    repoLocalCheck :=
      "#check IsLocallyNoetherian; used by MMPMathlibHypotheses."
    remainingMMPGap :=
      "Noetherianity alone does not supply dimension-bounded MMP termination or singularity packages."
    repoLocalCheckedSupport := true
  },
  {
    code := "MMP-OM-05"
    requestedObject := "morphism properties"
    mathlibAnchor := "MorphismProperty, IsProper, LocallyOfFiniteType"
    importModule := "Mathlib.AlgebraicGeometry.Morphisms.Proper"
    roleForMMPBoundary :=
      "Proper and locally finite-type structure morphisms are checked inputs; the general morphism-property API supplies locality and stability infrastructure."
    repoLocalCheck :=
      "#check MorphismProperty; #check IsProper; #check LocallyOfFiniteType."
    remainingMMPGap :=
      "Projective morphisms, extremal contractions, flips, and Mori-fiber-space morphism predicates are not connected."
    repoLocalCheckedSupport := true
  },
  {
    code := "MMP-OM-06"
    requestedObject := "RationalMap"
    mathlibAnchor := "Scheme.RationalMap"
    importModule := "Mathlib.AlgebraicGeometry.RationalMap"
    roleForMMPBoundary :=
      "Birational witness boundary for the source model versus either output model."
    repoLocalCheck :=
      "#check Scheme.RationalMap; notation X ⤏ Y is used in RationalMapBirationalWitness."
    remainingMMPGap :=
      "A pair of rational maps is not yet the selected birational-equivalence theorem/API for the final MMP statement."
    repoLocalCheckedSupport := true
  },
  {
    code := "MMP-OM-07"
    requestedObject := "sheaves"
    mathlibAnchor := "TopCat.Sheaf, SheafedSpace, PresheafedSpace, Scheme.ringCatSheaf"
    importModule := "Mathlib.AlgebraicGeometry.Spec"
    roleForMMPBoundary :=
      "Structure-sheaf substrate for schemes and for future divisor, ideal-sheaf, and module-sheaf constructions."
    repoLocalCheck :=
      "#check TopCat.Sheaf; #check SheafedSpace; #check PresheafedSpace; #check Scheme.ringCatSheaf."
    remainingMMPGap :=
      "No canonical-divisor, discrepancy, or terminal-pair sheaf package is selected here."
    repoLocalCheckedSupport := true
  },
  {
    code := "MMP-OM-08"
    requestedObject := "sites"
    mathlibAnchor := "Scheme.zariskiTopology, Scheme.overGrothendieckTopology, Scheme.smallGrothendieckTopology"
    importModule := "Mathlib.AlgebraicGeometry.Sites.BigZariski and Mathlib.AlgebraicGeometry.Sites.Small"
    roleForMMPBoundary :=
      "Big Zariski and over/small site infrastructure for sheaf-local and relative arguments."
    repoLocalCheck :=
      "#check Scheme.zariskiTopology; #check Scheme.overGrothendieckTopology; #check Scheme.smallGrothendieckTopology."
    remainingMMPGap :=
      "Site infrastructure is not a replacement for checked descent statements for MMP constructions."
    repoLocalCheckedSupport := true
  },
  {
    code := "MMP-OM-09"
    requestedObject := "module sheaves"
    mathlibAnchor := "Scheme.Modules, Scheme.PresheafOfModules, modulesSpecToSheaf, tilde"
    importModule := "Mathlib.AlgebraicGeometry.Modules.Tilde"
    roleForMMPBoundary :=
      "Sheaves of modules over schemes and affine tilde construction provide the expected substrate for future line-bundle and divisor APIs."
    repoLocalCheck :=
      "#check Scheme.Modules; #check Scheme.PresheafOfModules; #check modulesSpecToSheaf; #check tilde."
    remainingMMPGap :=
      "No selected canonical sheaf, relative canonical divisor, nefness, or Q-Cartier divisor interface is proved here."
    repoLocalCheckedSupport := true
  }
]

/-- The object-model audit has the nine rows requested by `S1-M-028-C002`. -/
theorem mmpObjectModelAudit_length : mmpObjectModelAudit.length = 9 :=
  rfl

/-- Each object-model row records checked substrate support, not MMP proof closure. -/
theorem mmpObjectModelAudit_all_checked_support :
    mmpObjectModelAudit.map MMPObjectModelAudit.repoLocalCheckedSupport =
      [true, true, true, true, true, true, true, true, true] :=
  rfl

/-- Stable row codes for public backfill of the object-model audit table. -/
theorem mmpObjectModelAudit_codes :
    mmpObjectModelAudit.map MMPObjectModelAudit.code =
      ["MMP-OM-01", "MMP-OM-02", "MMP-OM-03", "MMP-OM-04", "MMP-OM-05",
        "MMP-OM-06", "MMP-OM-07", "MMP-OM-08", "MMP-OM-09"] :=
  rfl

/-- Mathlib modules audited as repo-local object-model anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.AlgebraicGeometry.RationalMap",
  "Mathlib.AlgebraicGeometry.Morphisms.Proper",
  "Mathlib.AlgebraicGeometry.Scheme",
  "Mathlib.AlgebraicGeometry.Properties",
  "Mathlib.AlgebraicGeometry.Noetherian",
  "Mathlib.AlgebraicGeometry.Sites.BigZariski",
  "Mathlib.AlgebraicGeometry.Sites.Small",
  "Mathlib.AlgebraicGeometry.Modules.Tilde"
]

/-- Search terms retained for the local and external Lean 4 anchor audit. -/
def anchorSearchTerms : List String := [
  "Mori minimal model program Lean 4",
  "minimal model program mathlib",
  "Mori fiber space Lean",
  "terminal Q-factorial variety Lean",
  "canonical divisor nef algebraic geometry Lean"
]

/-! ## External Lean 4 anchor audit for the MMP boundary -/

/--
One row of the public external-anchor audit requested for the Mori minimal
model program slot.

`lakeClosureFeasible` is `true` only for an identified external theorem that
can plausibly be pinned, imported, and checked in this repository.  Search
rows, blocked code-search rows, and local-dependency negative rows are not
proof anchors.
-/
structure MMPExternalAnchorAudit where
  code : String
  sourceKind : String
  exactUrl : String
  exactRevisionOrResult : String
  theoremNames : String
  lakeClosureFeasibility : String
  auditStatus : String
  lakeClosureFeasible : Bool
  deriving DecidableEq, Repr

/--
External Lean 4 anchor audit for `S1-M-028-C003`.

The checked data records exact search URLs and the current local Lake closure.
It found no public Lean 4 theorem proving the Mori minimal model program or a
terminal MMP branch.  GitHub code search remains an authentication-blocked
follow-up, so this table is not a global absence proof.
-/
def mmpExternalAnchorAudit : List MMPExternalAnchorAudit := [
  {
    code := "MMP-EA-01"
    sourceKind := "GitHub repository search"
    exactUrl :=
      "https://api.github.com/search/repositories?q=%22minimal%20model%20program%22%20lean&per_page=10"
    exactRevisionOrResult :=
      "2026-05-01 unauthenticated REST repository search: total_count = 0; incomplete_results = false."
    theoremNames := "none identified"
    lakeClosureFeasibility :=
      "No repository candidate was returned, so there is no URL, revision, theorem name, or Lake dependency to pin."
    auditStatus := "negative_repository_search"
    lakeClosureFeasible := false
  },
  {
    code := "MMP-EA-02"
    sourceKind := "GitHub repository search"
    exactUrl :=
      "https://api.github.com/search/repositories?q=Mori%20Lean%20algebraic%20geometry&per_page=10"
    exactRevisionOrResult :=
      "2026-05-01 unauthenticated REST repository search: total_count = 0; incomplete_results = false."
    theoremNames := "none identified"
    lakeClosureFeasibility :=
      "No Mori algebraic-geometry Lean repository candidate was returned for dependency integration."
    auditStatus := "negative_repository_search"
    lakeClosureFeasible := false
  },
  {
    code := "MMP-EA-03"
    sourceKind := "GitHub repository search"
    exactUrl :=
      "https://api.github.com/search/repositories?q=%22Mori%20fiber%20space%22%20Lean&per_page=10"
    exactRevisionOrResult :=
      "2026-05-01 unauthenticated REST repository search: total_count = 0; incomplete_results = false."
    theoremNames := "none identified"
    lakeClosureFeasibility :=
      "No Mori-fiber-space Lean repository candidate was returned for dependency integration."
    auditStatus := "negative_repository_search"
    lakeClosureFeasible := false
  },
  {
    code := "MMP-EA-04"
    sourceKind := "GitHub repository search"
    exactUrl :=
      "https://api.github.com/search/repositories?q=%22terminal%20singularities%22%20Lean&per_page=10"
    exactRevisionOrResult :=
      "2026-05-01 unauthenticated REST repository search: total_count = 0; incomplete_results = false."
    theoremNames := "none identified"
    lakeClosureFeasibility :=
      "No terminal-singularities Lean repository candidate was returned for dependency integration."
    auditStatus := "negative_repository_search"
    lakeClosureFeasible := false
  },
  {
    code := "MMP-EA-05"
    sourceKind := "GitHub repository search"
    exactUrl :=
      "https://api.github.com/search/repositories?q=%22canonical%20divisor%22%20Lean%204&per_page=10"
    exactRevisionOrResult :=
      "2026-05-01 unauthenticated REST repository search: total_count = 0; incomplete_results = false."
    theoremNames := "none identified"
    lakeClosureFeasibility :=
      "No canonical-divisor Lean 4 repository candidate was returned for dependency integration."
    auditStatus := "negative_repository_search"
    lakeClosureFeasible := false
  },
  {
    code := "MMP-EA-06"
    sourceKind := "GitHub repository search"
    exactUrl :=
      "https://api.github.com/search/repositories?q=%22Q-factorial%22%20Lean&per_page=10"
    exactRevisionOrResult :=
      "2026-05-01 unauthenticated REST repository search: total_count = 0; incomplete_results = false."
    theoremNames := "none identified"
    lakeClosureFeasibility :=
      "No Q-factorial Lean repository candidate was returned for dependency integration."
    auditStatus := "negative_repository_search"
    lakeClosureFeasible := false
  },
  {
    code := "MMP-EA-07"
    sourceKind := "GitHub code search"
    exactUrl :=
      "https://api.github.com/search/code?q=%22minimal%20model%20program%22+language:Lean&per_page=10"
    exactRevisionOrResult :=
      "2026-05-01 unauthenticated REST code search returned 401 Requires authentication."
    theoremNames := "blocked; no theorem names available from this unauthenticated pass"
    lakeClosureFeasibility :=
      "Blocked until authenticated code search records candidate repository URL, commit, module, and theorem names."
    auditStatus := "authentication_blocker"
    lakeClosureFeasible := false
  },
  {
    code := "MMP-EA-08"
    sourceKind := "GitHub code search"
    exactUrl :=
      "https://api.github.com/search/code?q=%22Mori%22+%22RationalMap%22+language:Lean&per_page=10"
    exactRevisionOrResult :=
      "2026-05-01 unauthenticated REST code search returned 401 Requires authentication."
    theoremNames := "blocked; no theorem names available from this unauthenticated pass"
    lakeClosureFeasibility :=
      "Blocked until authenticated code search records candidate repository URL, commit, module, and theorem names."
    auditStatus := "authentication_blocker"
    lakeClosureFeasible := false
  },
  {
    code := "MMP-EA-09"
    sourceKind := "Reservoir package registry"
    exactUrl := "https://reservoir.lean-lang.org/?q=mori"
    exactRevisionOrResult :=
      "2026-05-01 direct curl to the query URL timed out after 30 seconds; no package candidate was extracted."
    theoremNames := "none identified"
    lakeClosureFeasibility :=
      "No Reservoir package URL, release, commit, module, or theorem name was available to add as a Lake dependency."
    auditStatus := "registry_search_blocker"
    lakeClosureFeasible := false
  },
  {
    code := "MMP-EA-10"
    sourceKind := "repo-local Lake closure"
    exactUrl := "Formalizations/Lean/lakefile.lean and Formalizations/Lean/lake-manifest.json"
    exactRevisionOrResult :=
      "mathlib pinned at 8a178386ffc0f5fef0b77738bb5449d50efeea95; flt-regular pinned at 56161b6eb5281fbfe9c38f2bcec0f429ebc11a27; no MMP external dependency is present."
    theoremNames := "no imported MMP theorem names in the current Lake closure"
    lakeClosureFeasibility :=
      "Current closure supports scheme/rational-map substrate only; it does not prove StatementShape or ExplicitFieldStatementShape."
    auditStatus := "not_repo_local_closed"
    lakeClosureFeasible := false
  }
]

/-- The C003 external-anchor audit records ten exact search or closure rows. -/
theorem mmpExternalAnchorAudit_length : mmpExternalAnchorAudit.length = 10 :=
  rfl

/--
No row in the C003 external-anchor audit is currently a feasible pinned proof
closure for the MMP statement.
-/
theorem mmpExternalAnchorAudit_no_lakeClosureFeasible :
    mmpExternalAnchorAudit.map MMPExternalAnchorAudit.lakeClosureFeasible =
      [false, false, false, false, false, false, false, false, false, false] :=
  rfl

/-- Stable row codes for public backfill of the C003 external-anchor audit. -/
theorem mmpExternalAnchorAudit_codes :
    mmpExternalAnchorAudit.map MMPExternalAnchorAudit.code =
      ["MMP-EA-01", "MMP-EA-02", "MMP-EA-03", "MMP-EA-04", "MMP-EA-05",
        "MMP-EA-06", "MMP-EA-07", "MMP-EA-08", "MMP-EA-09", "MMP-EA-10"] :=
  rfl

/-! ## Theorem-tree package split for the MMP statement -/

/--
Package labels for the public theorem-tree split requested by `S1-M-028-C004`.

The labels are bookkeeping nodes for the future proof tree.  They are not
theorem constructors and do not assert that any MMP proof branch has been
closed in this repository.
-/
inductive MMPTheoremPackage where
  | P0_statementAndScopeNormalization
  | P1_inputObjectAndSingularityPackage
  | P2_coneTheoremAndExtremalRayPackage
  | P3_contractionAndStepClassificationPackage
  | P4_divisorialContractionPreservationPackage
  | P5_flipExistenceAndPreservationPackage
  | P6_terminationOrBoundedRunPackage
  | P7_outputAlternativeAndClosureGatePackage
  deriving DecidableEq, Repr

/--
One theorem-tree package row.

`leafStatus` is intentionally a string so the public ledger can preserve the
exact M0387 status word `unchecked` while no concrete MMP proof leaves exist in
the repo-local Lean closure.
-/
structure MMPTheoremTreePackageAudit where
  package : MMPTheoremPackage
  code : String
  title : String
  proofTreeRole : String
  currentLeaves : List String
  leafStatus : String
  nextGate : String
  repoLocalClosed : Bool
  deriving DecidableEq, Repr

/--
Public theorem-tree split for `THM-M-0148` with packages `P0` through `P7`.

Every current leaf is explicitly marked `unchecked`.  The checked declarations
below validate only this metadata split and the absence of a repo-local closure
claim; they do not prove the Mori minimal model program.
-/
def mmpTheoremTreePackageSplit : List MMPTheoremTreePackageAudit := [
  {
    package := MMPTheoremPackage.P0_statementAndScopeNormalization
    code := "P0"
    title := "statement and scope normalization"
    proofTreeRole :=
      "Choose the exact theorem branch, base universe, input hypotheses, and output alternative before proving anything."
    currentLeaves := [
      "[unchecked] fix the dimension and characteristic scope",
      "[unchecked] replace slogan-level MMP wording by a theorem branch",
      "[unchecked] align ExplicitFieldStatementShape with the chosen branch"
    ]
    leafStatus := "unchecked"
    nextGate :=
      "Select a known MMP theorem branch and rewrite the statement with non-placeholder definitions where available."
    repoLocalClosed := false
  },
  {
    package := MMPTheoremPackage.P1_inputObjectAndSingularityPackage
    code := "P1"
    title := "input object and singularity package"
    proofTreeRole :=
      "Build the projective normal terminal Q-factorial input object over the base from mathlib or pinned APIs."
    currentLeaves := [
      "[unchecked] projective-over-base predicate",
      "[unchecked] normal variety predicate",
      "[unchecked] terminal singularity predicate",
      "[unchecked] Q-factorial and canonical divisor interfaces"
    ]
    leafStatus := "unchecked"
    nextGate :=
      "Replace placeholder input fields by checked definitions and prove they imply the mathlib substrate hypotheses."
    repoLocalClosed := false
  },
  {
    package := MMPTheoremPackage.P2_coneTheoremAndExtremalRayPackage
    code := "P2"
    title := "cone theorem and extremal rays"
    proofTreeRole :=
      "Supply the cone theorem, K-negative extremal rays, decomposition, and local-finiteness branch used to choose an MMP step."
    currentLeaves := [
      "[unchecked] numerical curve classes and Mori cone",
      "[unchecked] K-negative extremal-ray extraction",
      "[unchecked] cone decomposition and local finiteness"
    ]
    leafStatus := "unchecked"
    nextGate :=
      "Pin or implement a cone-theorem API and split its proof graph into independently budgeted leaves."
    repoLocalClosed := false
  },
  {
    package := MMPTheoremPackage.P3_contractionAndStepClassificationPackage
    code := "P3"
    title := "contraction theorem and step classification"
    proofTreeRole :=
      "Turn a selected extremal ray into a contraction morphism and classify the step as divisorial, flipping, or fiber type."
    currentLeaves := [
      "[unchecked] ray-to-contraction existence",
      "[unchecked] contraction properties over the base",
      "[unchecked] divisorial, small, and fiber-type case split"
    ]
    leafStatus := "unchecked"
    nextGate :=
      "Connect the contraction theorem to the concrete morphism predicates needed by the iteration."
    repoLocalClosed := false
  },
  {
    package := MMPTheoremPackage.P4_divisorialContractionPreservationPackage
    code := "P4"
    title := "divisorial contraction preservation"
    proofTreeRole :=
      "For divisorial contractions, update the model and preserve the admissible MMP input conditions."
    currentLeaves := [
      "[unchecked] exceptional divisor and discrepancy control",
      "[unchecked] transform of canonical divisor data",
      "[unchecked] preservation of terminal Q-factorial input"
    ]
    leafStatus := "unchecked"
    nextGate :=
      "Choose the divisorial-contraction interface and prove the preservation bridge for the next iteration state."
    repoLocalClosed := false
  },
  {
    package := MMPTheoremPackage.P5_flipExistenceAndPreservationPackage
    code := "P5"
    title := "flip existence and preservation"
    proofTreeRole :=
      "For small contractions, construct the flip and preserve the admissible MMP input conditions."
    currentLeaves := [
      "[unchecked] small contraction hypothesis",
      "[unchecked] flip construction or pinned existence theorem",
      "[unchecked] birational compatibility",
      "[unchecked] preservation of terminal Q-factorial input"
    ]
    leafStatus := "unchecked"
    nextGate :=
      "Import or formalize the selected flip-existence theorem and its preservation corollaries."
    repoLocalClosed := false
  },
  {
    package := MMPTheoremPackage.P6_terminationOrBoundedRunPackage
    code := "P6"
    title := "termination or bounded-run gate"
    proofTreeRole :=
      "Close the iteration by termination, by a dimension-specific stopping theorem, or by narrowing the statement to a bounded partial-run result."
    currentLeaves := [
      "[unchecked] termination measure or invariant",
      "[unchecked] monotonicity across divisorial steps and flips",
      "[unchecked] no-infinite-chain or bounded-run closure"
    ]
    leafStatus := "unchecked"
    nextGate :=
      "Decide between full termination, dimension-bounded termination, or a weaker checked partial-run theorem."
    repoLocalClosed := false
  },
  {
    package := MMPTheoremPackage.P7_outputAlternativeAndClosureGatePackage
    code := "P7"
    title := "output alternative and repo-local closure gate"
    proofTreeRole :=
      "Assemble either the minimal-model output or the Mori-fiber-space output and enforce the pin/import/check completion gate."
    currentLeaves := [
      "[unchecked] minimal-model output predicate and nef canonical class",
      "[unchecked] Mori-fiber-space output predicate",
      "[unchecked] birational witness compatibility",
      "[unchecked] local proof body, mathlib wrapper, or pinned external dependency check"
    ]
    leafStatus := "unchecked"
    nextGate :=
      "Prove StatementShape or ExplicitFieldStatementShape through a repo-local proof body, mathlib wrapper, or pinned external dependency."
    repoLocalClosed := false
  }
]

/-- The C004 theorem-tree split has exactly packages `P0` through `P7`. -/
theorem mmpTheoremTreePackageSplit_length : mmpTheoremTreePackageSplit.length = 8 :=
  rfl

/-- Stable package codes for public backfill of the C004 theorem-tree split. -/
theorem mmpTheoremTreePackageSplit_codes :
    mmpTheoremTreePackageSplit.map MMPTheoremTreePackageAudit.code =
      ["P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7"] :=
  rfl

/-- Every current package row has public leaf status `unchecked`. -/
theorem mmpTheoremTreePackageSplit_all_unchecked :
    mmpTheoremTreePackageSplit.map MMPTheoremTreePackageAudit.leafStatus =
      ["unchecked", "unchecked", "unchecked", "unchecked",
        "unchecked", "unchecked", "unchecked", "unchecked"] :=
  rfl

/-- No package in the C004 split is claimed as repo-local MMP closure. -/
theorem mmpTheoremTreePackageSplit_no_repoLocalClosed_claim :
    mmpTheoremTreePackageSplit.map MMPTheoremTreePackageAudit.repoLocalClosed =
      [false, false, false, false, false, false, false, false] :=
  rfl

/--
Machine-proof debt classification for this Stage1 slot.

The theorem is mathematically known in the intended higher-dimensional MMP
scope, but this repair pass found no repo-local Lean proof body or pinned
external Lean 4 proof of the full MMP statement.
-/
def machineProofDebt : String := "formalization_debt"

/--
Repo-local integration-debt gate.

No exact external Lean 4 proof anchor was identified or imported by this repair
pass, so the file records no completed-state `repo_local_integration_debt`.
Completion remains blocked on a local proof body, a mathlib theorem wrapper, or
a pinned external dependency that actually proves `StatementShape`.
-/
def repoLocalIntegrationDebtGate : String :=
  "closed_vacuously_for_open_item: no exact external Lean 4 proof anchor identified"

/--
Public integration-gate note for `S1-M-028-C005`.

This is checked metadata for the serial public-doc backfill.  It forbids a
completion claim from an anchor-only external Lean proof: any future external
MMP proof must either enter this repository's pinned/imported validation
closure or be recorded as a concrete blocker while the parent remains open.
-/
def externalProofCompletionGateNote : List String := [
  "No S1-M-028 / THM-M-0148 completion checkbox may be promoted from an external Lean proof unless that proof is pinned, imported, and checked in this repository.",
  "Accepted closure modes are local_proof_body, local_wrapper_upstream_mathlib, or external_upstream_pinned.",
  "external_upstream_anchor_only, URLs, theorem names, repository names, and source notes are not completion evidence.",
  "If an external Lean proof is found but cannot be integrated, record a concrete blocker with URL, revision, theorem or module names, toolchain or license issue, and failed command.",
  "A blocked external proof keeps the parent open as not_repo_local_closed; it does not discharge repo_local_integration_debt.",
  "No completed state may retain repo_local_integration_debt under the M0387 gate."
]

/-- The C005 integration-gate note has six public backfill clauses. -/
theorem externalProofCompletionGateNote_length :
    externalProofCompletionGateNote.length = 6 :=
  rfl

/-! ## Known-theorem-branch blocker for replacing the MMP slogan -/

/--
One checked blocker row for the public `S1-M-028-C006` backfill.

The row is documentation metadata, not theorem evidence.  It records that the
parent cannot be promoted while the target remains the whole minimal model
program slogan instead of a named, scoped theorem branch with explicit
hypotheses, output, proof package, and repo-local validation target.
-/
structure MMPKnownTheoremBranchBlocker where
  code : String
  publicTask : String
  blockerReason : String
  acceptableBranchShape : String
  requiredNormalizationFields : List String
  candidateBranchExamples : List String
  completionGate : String
  currentStatus : String
  repoLocalClosed : Bool
  deriving DecidableEq, Repr

/--
Public blocker metadata for `S1-M-028-C006`.

This deliberately blocks the slogan-level theorem target.  Future work must
choose one known branch, such as a fixed cone-theorem branch, contraction
theorem branch, flip-existence branch, dimension-scoped termination theorem,
minimal-model existence branch, or Mori-fiber-space output branch, and then
replace the placeholder fields above by the definitions and theorem statement
for that branch.
-/
def mmpKnownTheoremBranchBlocker : MMPKnownTheoremBranchBlocker := {
  code := "MMP-BLOCKER-KNOWN-BRANCH"
  publicTask :=
    "Narrow THM-M-0148 from the slogan-level Mori minimal model program to one named known theorem branch before any completion claim."
  blockerReason :=
    "The current StatementShape still represents the full MMP alternative with placeholder predicates, so it is too broad to be a checkable Lean target."
  acceptableBranchShape :=
    "A valid branch names a theorem family, fixes dimension/characteristic/singularity/base hypotheses, states the exact output, and identifies the local proof body, mathlib wrapper, or pinned external dependency expected to close it."
  requiredNormalizationFields := [
    "branch theorem family",
    "dimension and characteristic scope",
    "base and morphism hypotheses",
    "singularity and divisor hypotheses",
    "exact output object or alternative",
    "required proof packages",
    "machine theorem target name",
    "repo-local validation command"
  ]
  candidateBranchExamples := [
    "cone theorem for the selected singularity scope",
    "contraction theorem for K-negative extremal rays",
    "flip existence for the selected contraction class",
    "dimension-scoped flip termination or bounded-run theorem",
    "minimal-model existence branch with fixed hypotheses",
    "Mori-fiber-space output branch with fixed hypotheses"
  ]
  completionGate :=
    "Until a branch is selected and repo-local Lean validation passes for that branch target, S1-M-028 remains not_repo_local_closed and no anchor-only evidence is a completion state."
  currentStatus :=
    "public-doc integration pending; checked Lean metadata only, with no MMP proof claim."
  repoLocalClosed := false
}

/-- The C006 blocker has eight required normalization fields. -/
theorem mmpKnownTheoremBranchBlocker_requiredFields_length :
    mmpKnownTheoremBranchBlocker.requiredNormalizationFields.length = 8 :=
  rfl

/-- The C006 blocker explicitly remains outside repo-local theorem closure. -/
theorem mmpKnownTheoremBranchBlocker_no_repoLocalClosed_claim :
    mmpKnownTheoremBranchBlocker.repoLocalClosed = false :=
  rfl

/-! ## Low-risk import-check wrapper task -/

/--
One row for the public `S1-M-028-C007` wrapper task.

The row records a low-risk import/probe target only.  `proofCompletionClaim`
must stay `false`: these imports check the scheme/rational-map substrate used
by the statement boundary, not any Mori minimal model program theorem.
-/
structure MMPLowRiskImportCheckTask where
  code : String
  requestedSurface : String
  mathlibDeclaration : String
  importModule : String
  wrapperProbe : String
  completionBoundary : String
  proofCompletionClaim : Bool
  deriving DecidableEq, Repr

/--
Public-wrapper metadata for `S1-M-028-C007`.

Each row is intentionally narrow enough to validate by importing this file and
checking declaration names.  The wrapper task is suitable for serial backfill
into the public blueprint/todo, while the actual public documents remain
untouched by this worker.
-/
def mmpLowRiskImportCheckTasks : List MMPLowRiskImportCheckTask := [
  {
    code := "MMP-IMPORT-01"
    requestedSurface := "RationalMap"
    mathlibDeclaration := "Scheme.RationalMap and notation X ⤏ Y"
    importModule := "Mathlib.AlgebraicGeometry.RationalMap"
    wrapperProbe := "RationalMapBirationalWitness uses Nonempty (X ⤏ Y) and Nonempty (Y ⤏ X)."
    completionBoundary :=
      "Checks the rational-map object boundary only; it does not choose or prove a birational-equivalence theorem for the MMP."
    proofCompletionClaim := false
  },
  {
    code := "MMP-IMPORT-02"
    requestedSurface := "Scheme.IsIntegral / IsIntegral"
    mathlibDeclaration := "AlgebraicGeometry.IsIntegral"
    importModule := "Mathlib.AlgebraicGeometry.Properties"
    wrapperProbe := "SchemeMMPInput and MMPMathlibHypotheses use IsIntegral X."
    completionBoundary :=
      "Checks the integral source predicate only; it does not define normality, terminal singularities, or Q-factoriality."
    proofCompletionClaim := false
  },
  {
    code := "MMP-IMPORT-03"
    requestedSurface := "IsLocallyNoetherian"
    mathlibDeclaration := "AlgebraicGeometry.IsLocallyNoetherian"
    importModule := "Mathlib.AlgebraicGeometry.Noetherian"
    wrapperProbe := "MMPMathlibHypotheses uses IsLocallyNoetherian on the base and source."
    completionBoundary :=
      "Checks noetherian substrate predicates only; it does not supply dimension bounds or termination of flips."
    proofCompletionClaim := false
  },
  {
    code := "MMP-IMPORT-04"
    requestedSurface := "proper morphism predicate"
    mathlibDeclaration := "AlgebraicGeometry.IsProper"
    importModule := "Mathlib.AlgebraicGeometry.Morphisms.Proper"
    wrapperProbe := "SchemeMMPInput and MMPMathlibHypotheses use IsProper π."
    completionBoundary :=
      "Checks properness as a morphism property only; it does not prove projectivity or extremal contraction existence."
    proofCompletionClaim := false
  },
  {
    code := "MMP-IMPORT-05"
    requestedSurface := "finite-type morphism predicate"
    mathlibDeclaration := "AlgebraicGeometry.LocallyOfFiniteType"
    importModule := "Mathlib.AlgebraicGeometry.Morphisms.FiniteType"
    wrapperProbe := "SchemeMMPInput and MMPMathlibHypotheses use LocallyOfFiniteType π."
    completionBoundary :=
      "Checks locally finite-type substrate only; it does not supply MMP step construction or output alternatives."
    proofCompletionClaim := false
  }
]

/--
Minimal checked wrapper showing the C007 import surfaces can coexist in one
repo-local Lean target.

This proposition is deliberately trivial after the imported declarations type:
its role is import/probe validation, not proof of any MMP theorem.
-/
def LowRiskImportCheckWrapper : Prop :=
  ∀ {B X Y : Scheme.{u}} (π : X ⟶ B),
    Nonempty (X ⤏ Y) →
    IsIntegral X →
    IsLocallyNoetherian B →
    IsLocallyNoetherian X →
    IsProper π →
    LocallyOfFiniteType π →
      True

/-- The C007 low-risk wrapper checks once the imported predicates type. -/
theorem lowRiskImportCheckWrapper : LowRiskImportCheckWrapper.{u} := by
  intro B X Y π hRationalMap hIntegral hNoetherianBase hNoetherianSource hProper hFiniteType
  trivial

/-- The C007 import-check wrapper has exactly five public probe rows. -/
theorem mmpLowRiskImportCheckTasks_length :
    mmpLowRiskImportCheckTasks.length = 5 :=
  rfl

/-- Stable row codes for public backfill of the C007 wrapper task. -/
theorem mmpLowRiskImportCheckTasks_codes :
    mmpLowRiskImportCheckTasks.map MMPLowRiskImportCheckTask.code =
      ["MMP-IMPORT-01", "MMP-IMPORT-02", "MMP-IMPORT-03", "MMP-IMPORT-04",
        "MMP-IMPORT-05"] :=
  rfl

/-- The C007 import checks are not proof-completion claims. -/
theorem mmpLowRiskImportCheckTasks_no_proofCompletionClaim :
    mmpLowRiskImportCheckTasks.map MMPLowRiskImportCheckTask.proofCompletionClaim =
      [false, false, false, false, false] :=
  rfl

/-- Local declaration names contributed by this checked Stage1 artifact. -/
def checkedDeclarationNames : List String := [
  "AwesomeTheorems.Stage1.S1_M_028.SchemeMMPInput",
  "AwesomeTheorems.Stage1.S1_M_028.RationalMapBirationalWitness",
  "AwesomeTheorems.Stage1.S1_M_028.MMPStatementData",
  "AwesomeTheorems.Stage1.S1_M_028.MMPMathlibHypotheses",
  "AwesomeTheorems.Stage1.S1_M_028.MMPPlaceholderHypotheses",
  "AwesomeTheorems.Stage1.S1_M_028.MMPOutputAlternative",
  "AwesomeTheorems.Stage1.S1_M_028.ExplicitFieldStatementShape",
  "AwesomeTheorems.Stage1.S1_M_028.explicitFieldStatementShape_iff",
  "AwesomeTheorems.Stage1.S1_M_028.mmpOutputAlternative_of_explicitFieldStatementShape",
  "AwesomeTheorems.Stage1.S1_M_028.StatementShape",
  "AwesomeTheorems.Stage1.S1_M_028.statementShape_iff",
  "AwesomeTheorems.Stage1.S1_M_028.mmpAlternative_of_statementShape",
  "AwesomeTheorems.Stage1.S1_M_028.MMPPartialBranch",
  "AwesomeTheorems.Stage1.S1_M_028.MMPPartialBranchAudit",
  "AwesomeTheorems.Stage1.S1_M_028.mmpPartialBranchLedger",
  "AwesomeTheorems.Stage1.S1_M_028.mmpPartialBranchLedger_length",
  "AwesomeTheorems.Stage1.S1_M_028.mmpPartialBranchLedger_no_repoLocalClosed_claim",
  "AwesomeTheorems.Stage1.S1_M_028.mmpPartialBranchLedger_codes",
  "AwesomeTheorems.Stage1.S1_M_028.MMPObjectModelAudit",
  "AwesomeTheorems.Stage1.S1_M_028.mmpObjectModelAudit",
  "AwesomeTheorems.Stage1.S1_M_028.mmpObjectModelAudit_length",
  "AwesomeTheorems.Stage1.S1_M_028.mmpObjectModelAudit_all_checked_support",
  "AwesomeTheorems.Stage1.S1_M_028.mmpObjectModelAudit_codes",
  "AwesomeTheorems.Stage1.S1_M_028.MMPExternalAnchorAudit",
  "AwesomeTheorems.Stage1.S1_M_028.mmpExternalAnchorAudit",
  "AwesomeTheorems.Stage1.S1_M_028.mmpExternalAnchorAudit_length",
  "AwesomeTheorems.Stage1.S1_M_028.mmpExternalAnchorAudit_no_lakeClosureFeasible",
  "AwesomeTheorems.Stage1.S1_M_028.mmpExternalAnchorAudit_codes",
  "AwesomeTheorems.Stage1.S1_M_028.MMPTheoremPackage",
  "AwesomeTheorems.Stage1.S1_M_028.MMPTheoremTreePackageAudit",
  "AwesomeTheorems.Stage1.S1_M_028.mmpTheoremTreePackageSplit",
  "AwesomeTheorems.Stage1.S1_M_028.mmpTheoremTreePackageSplit_length",
  "AwesomeTheorems.Stage1.S1_M_028.mmpTheoremTreePackageSplit_codes",
  "AwesomeTheorems.Stage1.S1_M_028.mmpTheoremTreePackageSplit_all_unchecked",
  "AwesomeTheorems.Stage1.S1_M_028.mmpTheoremTreePackageSplit_no_repoLocalClosed_claim",
  "AwesomeTheorems.Stage1.S1_M_028.externalProofCompletionGateNote",
  "AwesomeTheorems.Stage1.S1_M_028.externalProofCompletionGateNote_length",
  "AwesomeTheorems.Stage1.S1_M_028.MMPKnownTheoremBranchBlocker",
  "AwesomeTheorems.Stage1.S1_M_028.mmpKnownTheoremBranchBlocker",
  "AwesomeTheorems.Stage1.S1_M_028.mmpKnownTheoremBranchBlocker_requiredFields_length",
  "AwesomeTheorems.Stage1.S1_M_028.mmpKnownTheoremBranchBlocker_no_repoLocalClosed_claim",
  "AwesomeTheorems.Stage1.S1_M_028.MMPLowRiskImportCheckTask",
  "AwesomeTheorems.Stage1.S1_M_028.mmpLowRiskImportCheckTasks",
  "AwesomeTheorems.Stage1.S1_M_028.LowRiskImportCheckWrapper",
  "AwesomeTheorems.Stage1.S1_M_028.lowRiskImportCheckWrapper",
  "AwesomeTheorems.Stage1.S1_M_028.mmpLowRiskImportCheckTasks_length",
  "AwesomeTheorems.Stage1.S1_M_028.mmpLowRiskImportCheckTasks_codes",
  "AwesomeTheorems.Stage1.S1_M_028.mmpLowRiskImportCheckTasks_no_proofCompletionClaim"
]

/-! ## Audit probes retained in the checked file. -/

#check Scheme
#check Spec
#check Scheme.Spec.map
#check Scheme.RationalMap
#check IsProper
#check LocallyOfFiniteType
#check MorphismProperty
#check IsIntegral
#check IsLocallyNoetherian
#check TopCat.Sheaf
#check SheafedSpace
#check PresheafedSpace
#check Scheme.ringCatSheaf
#check Scheme.zariskiTopology
#check Scheme.overGrothendieckTopology
#check Scheme.smallGrothendieckTopology
#check Scheme.Modules
#check Scheme.PresheafOfModules
#check modulesSpecToSheaf
#check tilde
#check MMPStatementData
#check ExplicitFieldStatementShape
#check mmpOutputAlternative_of_explicitFieldStatementShape
#check StatementShape
#check mmpAlternative_of_statementShape
#check MMPPartialBranch
#check mmpPartialBranchLedger
#check mmpPartialBranchLedger_length
#check mmpPartialBranchLedger_no_repoLocalClosed_claim
#check mmpPartialBranchLedger_codes
#check MMPObjectModelAudit
#check mmpObjectModelAudit
#check mmpObjectModelAudit_length
#check mmpObjectModelAudit_all_checked_support
#check mmpObjectModelAudit_codes
#check MMPExternalAnchorAudit
#check mmpExternalAnchorAudit
#check mmpExternalAnchorAudit_length
#check mmpExternalAnchorAudit_no_lakeClosureFeasible
#check mmpExternalAnchorAudit_codes
#check MMPTheoremPackage
#check MMPTheoremTreePackageAudit
#check mmpTheoremTreePackageSplit
#check mmpTheoremTreePackageSplit_length
#check mmpTheoremTreePackageSplit_codes
#check mmpTheoremTreePackageSplit_all_unchecked
#check mmpTheoremTreePackageSplit_no_repoLocalClosed_claim
#check externalProofCompletionGateNote
#check externalProofCompletionGateNote_length
#check MMPKnownTheoremBranchBlocker
#check mmpKnownTheoremBranchBlocker
#check mmpKnownTheoremBranchBlocker_requiredFields_length
#check mmpKnownTheoremBranchBlocker_no_repoLocalClosed_claim
#check MMPLowRiskImportCheckTask
#check mmpLowRiskImportCheckTasks
#check LowRiskImportCheckWrapper
#check lowRiskImportCheckWrapper
#check mmpLowRiskImportCheckTasks_length
#check mmpLowRiskImportCheckTasks_codes
#check mmpLowRiskImportCheckTasks_no_proofCompletionClaim

end S1_M_028
end Stage1
end AwesomeTheorems
