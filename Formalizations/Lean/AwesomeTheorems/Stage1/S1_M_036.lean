import Mathlib.AlgebraicGeometry.Noetherian
import Mathlib.AlgebraicGeometry.Morphisms.FiniteType
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.GroupTheory.Finiteness
import Mathlib.RingTheory.PicardGroup

/-!
Stage1 statement-shape artifact for `S1-M-036 / THM-M-0116`.

The Neron-Severi group itself is not yet a mathlib object in the audited
environment.  This file therefore records the formal boundary: schemes over a
field, finite-type/proper/smooth-relative-dimension-two/noetherian surface
hypotheses, and the target `AddGroup.FG` conclusion for an externally supplied
Neron-Severi group model.
-/

open CategoryTheory
open AlgebraicGeometry

universe u w

namespace AwesomeTheorems.Stage1.S1_M_036

/--
A local package for the geometric hypotheses normally hidden in the phrase
"algebraic surface over a field".

Decision for this slot: an algebraic surface is a scheme equipped with a
structure morphism to `Spec k` that is locally of finite type, proper, smooth of
relative dimension two, and whose source scheme is noetherian.  This is the
strong smooth/proper surface boundary used for the statement-shape artifact.

Projectivity is deliberately not a field of this structure.  The audited
mathlib snapshot has `Proj` and properness results for projective spectra, but
this worker did not find a general scheme-morphism predicate named
`IsProjective`/`Projective` suitable for arbitrary `X ⟶ Spec k`.  If a later
integrator chooses a projective version, it should add a concrete mathlib-backed
closed-immersion-into-projective-space predicate or record that API as a blocker
before changing the theorem target.
-/
structure AlgebraicSurfaceOver (k : Type u) [Field k] (X : Scheme.{u}) where
  structureMap : X ⟶ Spec (CommRingCat.of k)
  locallyOfFiniteType : LocallyOfFiniteType structureMap
  proper : IsProper structureMap
  smoothRelativeDimensionTwo : SmoothOfRelativeDimension 2 structureMap
  noetherian : IsNoetherian X

/-- Alias documenting the exact surface predicate chosen for this Stage1 slot. -/
abbrev SmoothProperSurfaceOver (k : Type u) [Field k] (X : Scheme.{u}) :=
  AlgebraicSurfaceOver k X

/-- The selected surface dimension condition is mathlib's smooth relative dimension `2`. -/
abbrev SurfaceDimensionTwoAnchor {k : Type u} [Field k] {X : Scheme.{u}}
    (f : X ⟶ Spec (CommRingCat.of k)) : Prop :=
  SmoothOfRelativeDimension 2 f

/-- The mathlib predicate used for "the underlying additive group is finitely generated". -/
abbrev FinitelyGeneratedAddGroup (G : Type w) [AddGroup G] : Prop :=
  AddGroup.FG G

/--
Statement shape for the Neron-Severi finite-generation theorem.

`NeronSeveriGroup` is a parameter rather than a definition because the audited
mathlib sources do not yet expose a scheme-level Neron-Severi group API.  Any
future terminal theorem should replace this parameter by the concrete quotient
of divisors/line bundles by numerical or algebraic equivalence selected by the
integrator.
-/
def StatementShape (NeronSeveriGroup : Scheme.{u} → Type w)
    [∀ X, AddGroup (NeronSeveriGroup X)] : Prop :=
  ∀ (k : Type u) [Field k] (X : Scheme.{u}),
    AlgebraicSurfaceOver k X → FinitelyGeneratedAddGroup (NeronSeveriGroup X)

/--
Trivial packaging lemma for downstream wrappers: once an integrator supplies a
machine-checked proof for every algebraic surface and the selected concrete
Neron-Severi model, it exactly inhabits `StatementShape`.
-/
theorem statementShape_of_forall (NeronSeveriGroup : Scheme.{u} → Type w)
    [∀ X, AddGroup (NeronSeveriGroup X)]
    (h : ∀ (k : Type u) [Field k] (X : Scheme.{u}),
      AlgebraicSurfaceOver k X → FinitelyGeneratedAddGroup (NeronSeveriGroup X)) :
    StatementShape NeronSeveriGroup :=
  h

/-- Audited mathlib anchor: schemes are available as the ambient object type. -/
abbrev SchemeAnchor : Type (u + 1) :=
  Scheme.{u}

/-- Audited mathlib anchor: proper morphisms are available for the surface hypotheses. -/
abbrev ProperMorphismAnchor {X Y : Scheme.{u}} (f : X ⟶ Y) : Prop :=
  IsProper f

/-- Audited mathlib anchor: locally finite-type morphisms are available. -/
abbrev LocallyFiniteTypeMorphismAnchor {X Y : Scheme.{u}} (f : X ⟶ Y) : Prop :=
  LocallyOfFiniteType f

/-- Audited mathlib anchor: smooth morphisms of fixed relative dimension are available. -/
abbrev SmoothRelativeDimensionTwoAnchor {X Y : Scheme.{u}} (f : X ⟶ Y) : Prop :=
  SmoothOfRelativeDimension 2 f

/-- Audited mathlib anchor: noetherian schemes are available. -/
abbrev NoetherianSchemeAnchor (X : Scheme.{u}) : Prop :=
  IsNoetherian X

/-- Pinned mathlib revision used by this repository during the repair pass. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Imported declaration families checked for the current statement-shape boundary. -/
def mathlibAnchorNames : List String :=
  [ "Mathlib.AlgebraicGeometry.Noetherian.IsNoetherian",
    "Mathlib.AlgebraicGeometry.Morphisms.FiniteType.LocallyOfFiniteType",
    "Mathlib.AlgebraicGeometry.Morphisms.Proper.IsProper",
    "Mathlib.AlgebraicGeometry.Morphisms.Smooth.SmoothOfRelativeDimension",
    "Mathlib.GroupTheory.Finiteness.AddGroup.FG",
    "AlgebraicGeometry.Scheme",
    "AlgebraicGeometry.Spec" ]

/--
Ring-level Picard/class-group declarations found during the C003 anchor audit.

These are useful bridge targets, but they are not a scheme-level Neron-Severi
group and do not prove finite generation for surfaces.
-/
def mathlibPicardQuotientAuditNames : List String :=
  [ "Mathlib.RingTheory.PicardGroup.CommRing.Pic",
    "Mathlib.RingTheory.PicardGroup.CommRing.Pic.mk",
    "Mathlib.RingTheory.PicardGroup.CommRing.Pic.functor",
    "Mathlib.RingTheory.PicardGroup.CommRing.relPic",
    "Mathlib.RingTheory.PicardGroup.Submodule.unitsQuotEquivRelPic",
    "Mathlib.RingTheory.PicardGroup.ClassGroup.equivPic" ]

/--
C003 external-anchor audit summary.

At the audited local mathlib revision, no declaration named
`NeronSeveriGroup`, `NeronSeveri`, or `Severi` was present.  The current public
declaration search likewise returned no Lean declaration for Neron-Severi; it
did return the ring-level `CommRing.Pic` family in
`Mathlib.RingTheory.PicardGroup`.  Therefore the terminal theorem remains
formalization debt rather than repo-local integration debt.
-/
def externalNeronSeveriAuditSummary : String :=
  "No concrete scheme-level NeronSeveriGroup or equivalent Picard/divisor quotient was found in the audited Lean 4 primary sources. mathlib has ring-level CommRing.Pic, CommRing.relPic, Submodule.unitsQuotEquivRelPic, and ClassGroup.equivPic in Mathlib.RingTheory.PicardGroup, but no scheme-level NS(X) or finite-generation theorem for algebraic surfaces."

/--
C004 integration decision.

No terminal external Lean 4 proof of the Neron-Severi finite-generation
theorem was identified by the C003/C004 audits.  Therefore this module does not
add a Lake dependency or vendor a proof body.  If a later authenticated search
finds such a proof, the next acceptable state is to pin/import/check it or to
record a concrete blocker such as toolchain incompatibility, license mismatch,
or a missing upstream theorem name.
-/
def terminalExternalProofIntegrationDecision : String :=
  "not_applicable_no_terminal_external_lean4_proof_found"

/--
Wrapper status for the child task that asked for a repo-local wrapper around a
terminal external proof.

The only checked wrapper currently available is the parameterized
`StatementShape` boundary above; it is not a wrapper around a terminal external
Neron-Severi proof.
-/
def terminalExternalProofWrapperStatus : String :=
  "no_terminal_external_proof_to_wrap; StatementShape remains statement_shape_only"

/-- Exact human-readable definition selected for "algebraic surface" in this slot. -/
def algebraicSurfaceDefinitionDecision : String :=
  "For S1-M-036, AlgebraicSurfaceOver k X means X -> Spec k is locally of finite type, proper, smooth of relative dimension 2, and X is noetherian. Projectivity is not encoded because the audited mathlib snapshot does not expose a general projective morphism predicate for arbitrary schemes."

/--
Machine proof debt classification for this Stage1 slot.

The theorem is mathematically known, but this module does not contain a
repo-local proof of finite generation for the concrete Neron-Severi group.
-/
def machineProofDebtClassification : String :=
  "formalization_debt"

/--
Repo-local integration gate status.

No completed state is claimed here.  If a later audit finds an external Lean 4
proof of the terminal Neron-Severi finite-generation theorem, the integrator
must pin/import/check it or record a concrete integration blocker.
-/
def repoLocalIntegrationDebtGate : String :=
  "no completed-state repo_local_integration_debt; current status not_repo_local_closed"

/--
Integration-ready Stage1 public note.

This is a checked string anchor only: the module validates the boundary and
does not prove the terminal Neron-Severi finite-generation theorem.
-/
def publicStage1Note : String :=
  "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_036.lean validates a statement-shape boundary only; it does not prove the terminal Neron-Severi finite-generation theorem."

/-- Canonical theorem-internal child leaves for later M0387-level backfill. -/
def theoremInternalChildLeaves : List String :=
  [ "S1-M-036.1 statement normalization: choose final surface and Neron-Severi group model",
    "S1-M-036.2 mathlib anchor audit: schemes, proper morphisms, finite type, noetherianity, and smooth relative dimension two",
    "S1-M-036.3 divisor/Picard bridge: define or import the quotient model for NS(X)",
    "S1-M-036.4 projectivity branch: add a concrete projective morphism predicate only if the public target is upgraded from proper to projective",
    "S1-M-036.5 finiteness theorem branch: prove, wrap mathlib, or pin external Lean proof",
    "S1-M-036.6 local leaf ledgers: split every nontrivial branch into <=100-step leaves",
    "S1-M-036.7 closure gate: validate local wrapper and merge public status without stale debt" ]

/--
Checked task-record shape for the no-terminal-proof branch.

These records are not mathematical assumptions and do not close the theorem.
They are repo-local, machine-checked planning anchors for the child pass that
must split the missing Neron-Severi formalization into concrete work packages.
-/
structure ChildFormalizationTask where
  id : String
  package : String
  title : String
  objective : String
  localBlocker : String
  completionGate : String

/--
C005 diagnosis: no terminal proof is available in this repository state, so the
safe repo-local output is an integration-ready formalization task split rather
than a completed theorem or an anchor-only completion claim.
-/
def noTerminalProofChildTaskDiagnosis : String :=
  "formalization_debt_child_split; no terminal Lean 4 Neron-Severi finite-generation proof is imported, pinned, vendored, or locally proved"

/--
Integration-ready child tasks for the missing Neron-Severi formalization branch.

The requested branches are represented explicitly: Picard/line-bundle API,
divisor/cycle API, algebraic or numerical equivalence, quotient group
construction, and finite-generation proof.
-/
def noTerminalProofChildTasks : List ChildFormalizationTask :=
  [ { id := "NSFG-C005-PicardLineBundleAPI",
      package := "NSFG-P02",
      title := "Picard and line-bundle API",
      objective := "Locate, import, or define the scheme-level Picard group or line-bundle group for a smooth proper surface X, and prove the bridge from available ring-level CommRing.Pic anchors only when the scheme-level hypotheses justify it.",
      localBlocker := "The audited mathlib surface exposes ring-level CommRing.Pic/relPic anchors but no checked scheme-level Picard group object suitable for NS(X).",
      completionGate := "A concrete Lean declaration for the scheme-level Picard or line-bundle group is available, has an AddGroup instance where needed, and validates by lake env lean in this repository." },
    { id := "NSFG-C005-DivisorCycleAPI",
      package := "NSFG-P02",
      title := "Divisor and cycle API",
      objective := "Audit or build Cartier divisor, Weil divisor, and codimension-one cycle APIs on the selected class of algebraic surfaces, including maps to line bundles or divisor classes.",
      localBlocker := "Name-level divisor files are not enough; no checked scheme-level divisor/cycle package has been connected to a Neron-Severi quotient in this artifact.",
      completionGate := "The chosen divisor/cycle objects, group operations, and comparison maps to Picard or line bundles are declared and locally checked without placeholders." },
    { id := "NSFG-C005-EquivalenceRelationAPI",
      package := "NSFG-P03",
      title := "Algebraic or numerical equivalence",
      objective := "Select algebraic equivalence or numerical equivalence for the formal NS model, define the relation on line bundles/divisors/cycles, and prove compatibility with the relevant group law.",
      localBlocker := "The current repository artifact has no concrete equivalence relation on divisors, cycles, or line bundles.",
      completionGate := "The selected equivalence relation is proved to be an additive congruence or quotient-compatible setoid in Lean and its mathematical choice is documented." },
    { id := "NSFG-C005-QuotientGroupConstruction",
      package := "NSFG-P04",
      title := "Neron-Severi quotient group construction",
      objective := "Define NeronSeveriGroup X as the chosen Picard/divisor/cycle quotient and provide the additive group structure expected by StatementShape.",
      localBlocker := "StatementShape still takes NeronSeveriGroup as a parameter, so no concrete quotient inhabits the theorem target.",
      completionGate := "A concrete NeronSeveriGroup declaration replaces the abstract parameter in a repo-local wrapper and exposes the required AddGroup instance." },
    { id := "NSFG-C005-FiniteGenerationBranch",
      package := "NSFG-P05-P06",
      title := "Finite-generation proof branch",
      objective := "Formalize or import the cohomological, Picard-scheme, descent, and finite-rank inputs needed to prove AddGroup.FG for the selected NeronSeveriGroup of a smooth proper surface.",
      localBlocker := "No finite-generation theorem for the concrete NS group has been found or proved in the audited Lean 4 environment.",
      completionGate := "A terminal theorem proves AddGroup.FG (NeronSeveriGroup X) under AlgebraicSurfaceOver hypotheses and the wrapper validates locally." } ]

/-- Public status boundary for the C005 child split. -/
def noTerminalProofChildTaskStatus : String :=
  "task_split_checked_not_theorem_completed"

/--
C006 package-level theorem-tree rows for the public backfill.

These rows are checked planning metadata only.  They do not introduce a
Neron-Severi group definition and do not prove finite generation.
-/
structure NSFGPackageRow where
  code : String
  title : String
  theoremTreeRole : String
  repoLocalStatus : String
  completionGate : String
  repoLocalClosed : Bool

/--
The `NSFG-P00` through `NSFG-P08` package split requested for the public
theorem-tree table.

Every row remains open or unchecked until a concrete NS group, a finite
generation proof, and repo-local validation are available.
-/
def nsfgPackageSplit : List NSFGPackageRow :=
  [ { code := "NSFG-P00",
      title := "Status boundary and canonical target",
      theoremTreeRole := "State that this slot currently validates only StatementShape for a supplied NeronSeveriGroup, not the terminal theorem.",
      repoLocalStatus := "statement_shape_only_not_repo_local_closed",
      completionGate := "Public status remains open until a concrete NS group and finite-generation theorem validate locally.",
      repoLocalClosed := false },
    { code := "NSFG-P01",
      title := "Algebraic surface hypothesis package",
      theoremTreeRole := "Freeze the surface predicate: X -> Spec k locally finite type, proper, smooth relative dimension two, and noetherian.",
      repoLocalStatus := "checked_statement_boundary",
      completionGate := "Any projective upgrade must add a concrete checked projective-morphism API before changing the target.",
      repoLocalClosed := false },
    { code := "NSFG-P02",
      title := "Picard, line-bundle, divisor, and cycle APIs",
      theoremTreeRole := "Locate or build the scheme-level objects from which the Neron-Severi quotient will be formed.",
      repoLocalStatus := "formalization_debt",
      completionGate := "Concrete scheme-level Picard/divisor/cycle declarations and comparison maps validate without placeholders.",
      repoLocalClosed := false },
    { code := "NSFG-P03",
      title := "Algebraic or numerical equivalence",
      theoremTreeRole := "Choose and formalize the equivalence relation used in NS(X), including compatibility with group operations.",
      repoLocalStatus := "formalization_debt",
      completionGate := "The selected equivalence relation is a checked additive congruence or quotient-compatible setoid.",
      repoLocalClosed := false },
    { code := "NSFG-P04",
      title := "Neron-Severi quotient group",
      theoremTreeRole := "Replace the StatementShape parameter by the concrete quotient group and its AddGroup instance.",
      repoLocalStatus := "formalization_debt",
      completionGate := "A concrete NeronSeveriGroup declaration inhabits the theorem target and validates locally.",
      repoLocalClosed := false },
    { code := "NSFG-P05",
      title := "Picard-scheme and cohomological finiteness inputs",
      theoremTreeRole := "Provide the geometric inputs normally used to control the connected component and rank of NS(X).",
      repoLocalStatus := "formalization_debt",
      completionGate := "Representability, connected-component, cohomology, and finiteness lemmas are proved or pinned and checked.",
      repoLocalClosed := false },
    { code := "NSFG-P06",
      title := "Finite-generation theorem branch",
      theoremTreeRole := "Prove AddGroup.FG for the selected NS group under the frozen algebraic-surface hypotheses.",
      repoLocalStatus := "formalization_debt",
      completionGate := "A terminal theorem proves AddGroup.FG (NeronSeveriGroup X) and the wrapper validates by lake env lean.",
      repoLocalClosed := false },
    { code := "NSFG-P07",
      title := "External proof or dependency integration gate",
      theoremTreeRole := "If an external Lean proof is found, pin/import/check it or record a concrete integration blocker.",
      repoLocalStatus := "no_terminal_external_lean4_proof_found",
      completionGate := "No completed state may retain anchor-only external evidence or repo_local_integration_debt.",
      repoLocalClosed := false },
    { code := "NSFG-P08",
      title := "Public merge and status synchronization",
      theoremTreeRole := "Merge the theorem-tree table and leaf ledger into public docs without changing completion status prematurely.",
      repoLocalStatus := "serial_public_doc_integration_required",
      completionGate := "Blueprint, todo, README, and any status surface agree on open or partial statement-shape only.",
      repoLocalClosed := false } ]

/-- The public package table has exactly the requested nine package rows. -/
theorem nsfgPackageSplit_length : nsfgPackageSplit.length = 9 :=
  rfl

/-- The public package table uses exactly `NSFG-P00` through `NSFG-P08`. -/
theorem nsfgPackageSplit_codes :
    nsfgPackageSplit.map NSFGPackageRow.code =
      [ "NSFG-P00", "NSFG-P01", "NSFG-P02", "NSFG-P03", "NSFG-P04",
        "NSFG-P05", "NSFG-P06", "NSFG-P07", "NSFG-P08" ] :=
  rfl

/-- No package row is claimed as repo-local theorem closure. -/
theorem nsfgPackageSplit_no_repoLocalClosed_claim :
    nsfgPackageSplit.map NSFGPackageRow.repoLocalClosed =
      [ false, false, false, false, false, false, false, false, false ] :=
  rfl

/--
C006 independent local leaf ledger rows.

`maxLocalProofSteps` is a budget cap for the future local proof or audit leaf.
All rows are currently unchecked planning leaves; none is a completed proof.
-/
structure NSFGLeafLedgerRow where
  leafId : String
  package : String
  localLeafTarget : String
  maxLocalProofSteps : Nat
  status : String
  independentLocalLedger : Bool

/--
Independent `<=100` leaf ledger for the public backfill.

The rows are intentionally narrower than package rows.  A later owner can close
one leaf without claiming any sibling package complete.
-/
def nsfgIndependentLeafLedger : List NSFGLeafLedgerRow :=
  [ { leafId := "NSFG-L00-01",
      package := "NSFG-P00",
      localLeafTarget := "Record the statement-shape-only boundary and forbid terminal theorem wording.",
      maxLocalProofSteps := 100,
      status := "unchecked_public_doc_leaf",
      independentLocalLedger := true },
    { leafId := "NSFG-L00-02",
      package := "NSFG-P00",
      localLeafTarget := "Define the canonical theorem target in terms of a concrete future NeronSeveriGroup and AddGroup.FG.",
      maxLocalProofSteps := 100,
      status := "unchecked_public_doc_leaf",
      independentLocalLedger := true },
    { leafId := "NSFG-L01-01",
      package := "NSFG-P01",
      localLeafTarget := "Freeze the proper, smooth relative dimension two, finite-type, noetherian surface predicate.",
      maxLocalProofSteps := 100,
      status := "checked_statement_boundary_but_not_terminal_theorem",
      independentLocalLedger := true },
    { leafId := "NSFG-L01-02",
      package := "NSFG-P01",
      localLeafTarget := "Record the projectivity API blocker before any public target upgrade from proper to projective.",
      maxLocalProofSteps := 100,
      status := "unchecked_blocker_leaf",
      independentLocalLedger := true },
    { leafId := "NSFG-L02-01",
      package := "NSFG-P02",
      localLeafTarget := "Locate or define a scheme-level Picard or line-bundle group and its additive structure.",
      maxLocalProofSteps := 100,
      status := "unchecked_formalization_debt",
      independentLocalLedger := true },
    { leafId := "NSFG-L02-02",
      package := "NSFG-P02",
      localLeafTarget := "Locate or define Cartier/Weil divisor or codimension-one cycle APIs and comparison maps.",
      maxLocalProofSteps := 100,
      status := "unchecked_formalization_debt",
      independentLocalLedger := true },
    { leafId := "NSFG-L03-01",
      package := "NSFG-P03",
      localLeafTarget := "Choose algebraic equivalence or numerical equivalence for the formal NS model.",
      maxLocalProofSteps := 100,
      status := "unchecked_formalization_debt",
      independentLocalLedger := true },
    { leafId := "NSFG-L03-02",
      package := "NSFG-P03",
      localLeafTarget := "Prove the chosen equivalence relation is quotient-compatible with the group law.",
      maxLocalProofSteps := 100,
      status := "unchecked_formalization_debt",
      independentLocalLedger := true },
    { leafId := "NSFG-L04-01",
      package := "NSFG-P04",
      localLeafTarget := "Construct the concrete NeronSeveriGroup quotient object for a surface.",
      maxLocalProofSteps := 100,
      status := "unchecked_formalization_debt",
      independentLocalLedger := true },
    { leafId := "NSFG-L04-02",
      package := "NSFG-P04",
      localLeafTarget := "Provide the AddGroup instance and rewrite StatementShape to the concrete quotient target.",
      maxLocalProofSteps := 100,
      status := "unchecked_formalization_debt",
      independentLocalLedger := true },
    { leafId := "NSFG-L05-01",
      package := "NSFG-P05",
      localLeafTarget := "Audit or formalize Picard-scheme representability and identity-component inputs.",
      maxLocalProofSteps := 100,
      status := "unchecked_formalization_debt",
      independentLocalLedger := true },
    { leafId := "NSFG-L05-02",
      package := "NSFG-P05",
      localLeafTarget := "Audit or formalize the cohomological finiteness inputs used to bound the NS rank.",
      maxLocalProofSteps := 100,
      status := "unchecked_formalization_debt",
      independentLocalLedger := true },
    { leafId := "NSFG-L06-01",
      package := "NSFG-P06",
      localLeafTarget := "Prove finite generation for the selected quotient using the checked geometric inputs.",
      maxLocalProofSteps := 100,
      status := "unchecked_formalization_debt",
      independentLocalLedger := true },
    { leafId := "NSFG-L06-02",
      package := "NSFG-P06",
      localLeafTarget := "Expose the terminal repo-local wrapper theorem under AlgebraicSurfaceOver hypotheses.",
      maxLocalProofSteps := 100,
      status := "unchecked_formalization_debt",
      independentLocalLedger := true },
    { leafId := "NSFG-L07-01",
      package := "NSFG-P07",
      localLeafTarget := "Repeat authenticated Lean 4 source search and record repository, module, theorem names, and commit hash.",
      maxLocalProofSteps := 100,
      status := "unchecked_external_anchor_leaf",
      independentLocalLedger := true },
    { leafId := "NSFG-L07-02",
      package := "NSFG-P07",
      localLeafTarget := "If a terminal external proof exists, pin/import/check it; otherwise record a concrete blocker.",
      maxLocalProofSteps := 100,
      status := "unchecked_external_integration_gate",
      independentLocalLedger := true },
    { leafId := "NSFG-L08-01",
      package := "NSFG-P08",
      localLeafTarget := "Serially merge the public theorem-tree table without changing public completion wording.",
      maxLocalProofSteps := 100,
      status := "unchecked_public_doc_leaf",
      independentLocalLedger := true },
    { leafId := "NSFG-L08-02",
      package := "NSFG-P08",
      localLeafTarget := "Synchronize blueprint, todo, README, and status surfaces only after repo-local closure gates pass.",
      maxLocalProofSteps := 100,
      status := "unchecked_public_doc_leaf",
      independentLocalLedger := true } ]

/-- The C006 public backfill ledger has two independent leaves for each package. -/
theorem nsfgIndependentLeafLedger_length : nsfgIndependentLeafLedger.length = 18 :=
  rfl

/-- Every C006 leaf budget is within the M0387 `<=100` local-step limit. -/
theorem nsfgIndependentLeafLedger_all_budgets_le_100 :
    (nsfgIndependentLeafLedger.all (fun row => row.maxLocalProofSteps <= 100)) = true :=
  rfl

/-- Every C006 row is marked as an independent local ledger leaf. -/
theorem nsfgIndependentLeafLedger_all_independent :
    (nsfgIndependentLeafLedger.all NSFGLeafLedgerRow.independentLocalLedger) = true :=
  rfl

/-- C006 diagnosis for the public theorem-tree backfill child. -/
def c006PublicBackfillDiagnosis : String :=
  "public_doc_integration_work_with_checked_repo_local_metadata; not theorem completion"

/-- C006 repo-local gate status: no completed theorem state is claimed. -/
def c006RepoLocalIntegrationDebtGate : String :=
  "passes_for_noncompletion_state: no completed claim and no anchor-only external proof completion"

/--
C007 public status guard rows.

These rows are checked synchronization metadata only.  They do not edit public
documents and do not close any proof branch.
-/
structure PublicStatusSurfaceGuard where
  surface : String
  requiredWording : String
  currentAudit : String
  mayClaimCompletionBeforeRepoLocalGate : Bool

/--
C007 guard for the three public surfaces named by the child task.

The required wording remains `open` or `partial statement-shape only` until a
concrete Neron-Severi group, a terminal finite-generation proof or pinned
checked upstream dependency, and repo-local validation all exist.
-/
def c007PublicStatusSurfaceGuards : List PublicStatusSurfaceGuard :=
  [ { surface := "Docs/Stage1_Blueprint.md",
      requiredWording := "open or partial statement-shape only",
      currentAudit := "S1-M-036 row is open/not completed; public backfill remains serial integration work",
      mayClaimCompletionBeforeRepoLocalGate := false },
    { surface := "Docs/todos_20260430.md",
      requiredWording := "open or partial statement-shape only",
      currentAudit := "S1-M-036 backfill checklist remains unchecked and must not be marked complete by a child worker",
      mayClaimCompletionBeforeRepoLocalGate := false },
    { surface := "README.md",
      requiredWording := "open or partial statement-shape only",
      currentAudit := "no S1-M-036 completion wording was found during this child audit; future README wording must stay nonterminal",
      mayClaimCompletionBeforeRepoLocalGate := false } ]

/-- C007 covers exactly the three public surfaces named by the child task. -/
theorem c007PublicStatusSurfaceGuards_length :
    c007PublicStatusSurfaceGuards.length = 3 :=
  rfl

/-- C007 public surfaces must not claim completion before the repo-local gate closes. -/
theorem c007PublicStatusSurfaceGuards_no_premature_completion :
    c007PublicStatusSurfaceGuards.map
      PublicStatusSurfaceGuard.mayClaimCompletionBeforeRepoLocalGate =
      [ false, false, false ] :=
  rfl

/-- C007 diagnosis for this child task. -/
def c007PublicStatusDiagnosis : String :=
  "public_doc_integration_guard; documentation-only status synchronization, not theorem proof completion"

/-- C007 repo-local integration-debt gate result for this noncompletion state. -/
def c007RepoLocalIntegrationDebtGate : String :=
  "passes_for_noncompletion_state: public status remains open/partial_statement_shape_only until repo-local proof_or_dependency gate closes"

#check StatementShape
#check statementShape_of_forall
#check SmoothProperSurfaceOver
#check SurfaceDimensionTwoAnchor
#check SchemeAnchor
#check ProperMorphismAnchor
#check LocallyFiniteTypeMorphismAnchor
#check SmoothRelativeDimensionTwoAnchor
#check NoetherianSchemeAnchor
#check machineProofDebtClassification
#check repoLocalIntegrationDebtGate
#check algebraicSurfaceDefinitionDecision
#check publicStage1Note
#check theoremInternalChildLeaves
#check ChildFormalizationTask
#check noTerminalProofChildTaskDiagnosis
#check noTerminalProofChildTasks
#check noTerminalProofChildTaskStatus
#check NSFGPackageRow
#check nsfgPackageSplit
#check nsfgPackageSplit_length
#check nsfgPackageSplit_codes
#check nsfgPackageSplit_no_repoLocalClosed_claim
#check NSFGLeafLedgerRow
#check nsfgIndependentLeafLedger
#check nsfgIndependentLeafLedger_length
#check nsfgIndependentLeafLedger_all_budgets_le_100
#check nsfgIndependentLeafLedger_all_independent
#check c006PublicBackfillDiagnosis
#check c006RepoLocalIntegrationDebtGate
#check PublicStatusSurfaceGuard
#check c007PublicStatusSurfaceGuards
#check c007PublicStatusSurfaceGuards_length
#check c007PublicStatusSurfaceGuards_no_premature_completion
#check c007PublicStatusDiagnosis
#check c007RepoLocalIntegrationDebtGate
#check CommRing.Pic
#check CommRing.Pic.mk
#check CommRing.Pic.functor
#check CommRing.relPic
#check Submodule.unitsQuotEquivRelPic
#check ClassGroup.equivPic
#check mathlibPicardQuotientAuditNames
#check externalNeronSeveriAuditSummary
#check terminalExternalProofIntegrationDecision
#check terminalExternalProofWrapperStatus

end AwesomeTheorems.Stage1.S1_M_036
