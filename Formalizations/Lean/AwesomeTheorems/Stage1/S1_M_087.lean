import Mathlib.Data.Rat.Defs
import Mathlib.Data.Rat.Cast.Defs
import Mathlib.Data.Set.Finite.Basic
import Mathlib.ModelTheory.Algebra.Field.Basic
import Mathlib.ModelTheory.Arithmetic.Presburger.Basic
import Mathlib.ModelTheory.Definability
import Mathlib.ModelTheory.Order

/-!
# S1-M-087 / THM-M-0441: Pila-Wilkie theorem, Stage1 statement shape

This file records a conservative Lean 4 boundary for the Pila-Wilkie rational
point counting theorem in o-minimal structures.  The local mathlib snapshot has
first-order languages, ordered structures, definable sets, rational casts, and
finite-set/cardinality infrastructure.  It does not expose an o-minimality API,
the algebraic/transcendental part of a definable set, or the Pila-Wilkie
subpolynomial counting theorem.
-/

noncomputable section

open FirstOrder

universe u v w

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_087

/--
Pinned mathlib revision audited for the `THM-M-0441.mathlib-audit` child task.

The import list above checks the repo-local availability of the requested
mathlib surface.  In this snapshot, `Data.Rat` and
`ModelTheory.Arithmetic.Presburger` are source-family names; the importable Lean
leaves used here are `Mathlib.Data.Rat.Defs` and
`Mathlib.ModelTheory.Arithmetic.Presburger.Basic`.
-/
def auditedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Public names requested for the Pila-Wilkie Stage1 mathlib audit. -/
def auditedMathlibModuleNames : List String :=
  [ "ModelTheory.Definability"
  , "ModelTheory.Order"
  , "ModelTheory.Algebra.Field.Basic"
  , "ModelTheory.Arithmetic.Presburger"
  , "Data.Rat"
  , "Data.Set.Finite.Basic"
  ]

/-- The audited revision string is intentionally fixed, not inferred. -/
theorem auditedMathlibRevision_eq :
    auditedMathlibRevision = "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- The audit records exactly the six requested mathlib module families. -/
theorem auditedMathlibModuleNames_length :
    auditedMathlibModuleNames.length = 6 :=
  rfl

/-- `ModelTheory.Arithmetic.Presburger.Basic` supplies the Presburger language. -/
def presburgerLanguageAuditAnchor : FirstOrder.Language :=
  FirstOrder.Language.presburger

/-- `ModelTheory.Algebra.Field.Basic` supplies the first-order field theory. -/
def fieldTheoryAuditAnchor : FirstOrder.Language.ring.Theory :=
  FirstOrder.Language.Theory.field

/-- `ModelTheory.Order` supplies the first-order language of orders. -/
def orderLanguageAuditAnchor : FirstOrder.Language :=
  FirstOrder.Language.order

/-- `Data.Rat.Defs` supplies the rational-number type used for rational points. -/
def rationalTypeAuditAnchor : Type :=
  ℚ

/-- `Data.Set.Finite.Basic` supplies finite-set facts needed for counting wrappers. -/
theorem finiteEmptyAuditAnchor (α : Type u) :
    (∅ : Set α).Finite :=
  Set.finite_empty

/-- Rational points in affine `n`-space, represented by rational coordinate functions. -/
abbrev RationalPoint (n : ℕ) : Type :=
  Fin n -> ℚ

/-- Interpret a rational point as a point of an ambient linear ordered field. -/
def rationalPointMap (M : Type u) [Field M] (n : ℕ) (q : RationalPoint n) : Fin n -> M :=
  fun i => (q i : M)

/--
Stage1 data slots for an o-minimal expansion of an ordered field.

`isOMinimal` is intentionally a predicate slot: the audited mathlib revision has
ordered first-order structures and definability, but not a ready-made o-minimality
class or cell-decomposition API.
-/
structure OMinimalExpansionData
    (L : FirstOrder.Language.{u, v}) (M : Type w)
    [Field M] [LinearOrder M] [IsStrictOrderedRing M] [L.Structure M] where
  parameterSet : Set M
  isOMinimal : Prop

/-- A definable subset of affine `n`-space over the chosen o-minimal expansion. -/
def DefinableSet
    {L : FirstOrder.Language.{u, v}} {M : Type w}
    [Field M] [LinearOrder M] [IsStrictOrderedRing M] [L.Structure M]
    (D : OMinimalExpansionData L M) (n : ℕ) : Type w :=
  { X : Set (Fin n -> M) // D.parameterSet.Definable L X }

/--
Additional slots needed to state the Pila-Wilkie theorem for one arity.

The fields isolate the current formalization boundary:
* `height` is the rational height convention;
* `algebraicPart` is the union of positive-dimensional semialgebraic pieces of `X`;
* `subpolynomialBound` is the asymptotic `O(T^epsilon)` conclusion.
-/
structure PilaWilkieArityBoundary
    {L : FirstOrder.Language.{u, v}} {M : Type w}
    [Field M] [LinearOrder M] [IsStrictOrderedRing M] [L.Structure M]
    (D : OMinimalExpansionData L M) (n : ℕ) where
  height : RationalPoint n -> ℕ
  algebraicPart : DefinableSet D n -> Set (Fin n -> M)
  subpolynomialBound : (ℕ -> Set (RationalPoint n)) -> Prop

/-- Missing formal API families for the Stage1 Pila-Wilkie boundary. -/
inductive PilaWilkieMissingFormalApi where
  | oMinimality
  | cellDecomposition
  | definableDimension
  | algebraicPart
  | rationalHeight
  | boundedHeightFiniteness
  | subpolynomialAsymptoticCounting
  deriving DecidableEq, Repr

/-- Stable public code for each missing Pila-Wilkie API family. -/
def PilaWilkieMissingFormalApi.code : PilaWilkieMissingFormalApi -> String
  | PilaWilkieMissingFormalApi.oMinimality =>
      "M0441-API-01-o-minimality"
  | PilaWilkieMissingFormalApi.cellDecomposition =>
      "M0441-API-02-cell-decomposition"
  | PilaWilkieMissingFormalApi.definableDimension =>
      "M0441-API-03-definable-dimension"
  | PilaWilkieMissingFormalApi.algebraicPart =>
      "M0441-API-04-algebraic-part"
  | PilaWilkieMissingFormalApi.rationalHeight =>
      "M0441-API-05-rational-height"
  | PilaWilkieMissingFormalApi.boundedHeightFiniteness =>
      "M0441-API-06-bounded-height-finiteness"
  | PilaWilkieMissingFormalApi.subpolynomialAsymptoticCounting =>
      "M0441-API-07-subpolynomial-asymptotic-counting"

/-- Human-readable description for each missing Pila-Wilkie API family. -/
def PilaWilkieMissingFormalApi.description : PilaWilkieMissingFormalApi -> String
  | PilaWilkieMissingFormalApi.oMinimality =>
      "define or import an o-minimality predicate or class for ordered-field expansions"
  | PilaWilkieMissingFormalApi.cellDecomposition =>
      "define or import cell decomposition for definable subsets of affine space"
  | PilaWilkieMissingFormalApi.definableDimension =>
      "define or import definable dimension and positive-dimensionality tests"
  | PilaWilkieMissingFormalApi.algebraicPart =>
      "define the algebraic part as the union of positive-dimensional semialgebraic pieces"
  | PilaWilkieMissingFormalApi.rationalHeight =>
      "fix the rational height convention on rational points in affine space"
  | PilaWilkieMissingFormalApi.boundedHeightFiniteness =>
      "prove finiteness of rational points with height at most a fixed bound"
  | PilaWilkieMissingFormalApi.subpolynomialAsymptoticCounting =>
      "state and prove the Pila-Wilkie subpolynomial counting bound"

/-- Complete split requested by `THM-M-0441.missing-api`. -/
def pilaWilkieMissingFormalApiSplit : List PilaWilkieMissingFormalApi := [
  PilaWilkieMissingFormalApi.oMinimality,
  PilaWilkieMissingFormalApi.cellDecomposition,
  PilaWilkieMissingFormalApi.definableDimension,
  PilaWilkieMissingFormalApi.algebraicPart,
  PilaWilkieMissingFormalApi.rationalHeight,
  PilaWilkieMissingFormalApi.boundedHeightFiniteness,
  PilaWilkieMissingFormalApi.subpolynomialAsymptoticCounting
]

/-- The checked split contains exactly the seven public child families requested. -/
theorem pilaWilkieMissingFormalApiSplit_length :
    pilaWilkieMissingFormalApiSplit.length = 7 :=
  rfl

/-- The checked split exposes stable public codes in the intended order. -/
theorem pilaWilkieMissingFormalApiSplit_codes :
    pilaWilkieMissingFormalApiSplit.map PilaWilkieMissingFormalApi.code =
      [ "M0441-API-01-o-minimality"
      , "M0441-API-02-cell-decomposition"
      , "M0441-API-03-definable-dimension"
      , "M0441-API-04-algebraic-part"
      , "M0441-API-05-rational-height"
      , "M0441-API-06-bounded-height-finiteness"
      , "M0441-API-07-subpolynomial-asymptotic-counting"
      ] :=
  rfl

/--
Abstract interface showing how the seven missing API families feed one arity.

This structure is intentionally uninstantiated here.  It records the concrete
slots that must be supplied by future local development or by a pinned external
Lean 4 dependency before `StatementShape` can become a terminal Pila-Wilkie
formalization.
-/
structure PilaWilkieMissingApiBoundary
    {L : FirstOrder.Language.{u, v}} {M : Type w}
    [Field M] [LinearOrder M] [IsStrictOrderedRing M] [L.Structure M]
    (D : OMinimalExpansionData L M) (n : ℕ) where
  isOMinimalStructure : Prop
  cellDecomposition : DefinableSet D n -> Type w
  definableDimension : DefinableSet D n -> ℕ
  algebraicPart : DefinableSet D n -> Set (Fin n -> M)
  rationalHeight : RationalPoint n -> ℕ
  boundedHeightFinite : ∀ B : ℕ, { q : RationalPoint n | rationalHeight q ≤ B }.Finite
  subpolynomialAsymptoticCounting : (ℕ -> Set (RationalPoint n)) -> Prop

/--
The missing-API boundary specializes to the existing arity boundary by forgetting
the o-minimality, cell-decomposition, dimension, and finiteness slots.
-/
def PilaWilkieMissingApiBoundary.toArityBoundary
    {L : FirstOrder.Language.{u, v}} {M : Type w}
    [Field M] [LinearOrder M] [IsStrictOrderedRing M] [L.Structure M]
    {D : OMinimalExpansionData L M} {n : ℕ}
    (Pkg : PilaWilkieMissingApiBoundary D n) : PilaWilkieArityBoundary D n where
  height := Pkg.rationalHeight
  algebraicPart := Pkg.algebraicPart
  subpolynomialBound := Pkg.subpolynomialAsymptoticCounting

/-- The missing-API boundary is only an interface; no terminal theorem is claimed. -/
def pilaWilkieMissingApiBoundaryIsTerminalTheorem : Bool :=
  false

/-- Machine-proof debt classification after the missing-API split child. -/
def pilaWilkieMachineProofDebt : String :=
  "formalization_debt"

/-- Current machine status after the missing-API split child. -/
def pilaWilkieCurrentMachineStatus : String :=
  "not_repo_local_closed"

/-- M0387 gate: this child leaves no completed state with repo-local integration debt. -/
def pilaWilkieRepoLocalIntegrationDebtRetainedInCompletedState : Bool :=
  false

/-- Public backfill notes for the `THM-M-0441.missing-api` child. -/
def pilaWilkieMissingApiPublicBackfillNotes : List String := [
  "The checked Lean artifact splits the missing Pila-Wilkie APIs into seven families: o-minimality, cell decomposition, definable dimension, algebraic part, rational height, bounded-height finiteness, and subpolynomial asymptotic counting.",
  "The split is recorded by AwesomeTheorems.Stage1.S1_M_087.PilaWilkieMissingFormalApi and pilaWilkieMissingFormalApiSplit_length.",
  "PilaWilkieMissingApiBoundary records how these APIs would feed one arity of the existing StatementShape boundary, but it is intentionally uninstantiated and is not a terminal Pila-Wilkie theorem.",
  "Current machine status remains not_repo_local_closed / formalization_debt; no completed-state repo_local_integration_debt is claimed."
]

/-- External Lean 4 search terms requested by `THM-M-0441.external-audit`. -/
def pilaWilkieExternalAuditSearchTerms : List String := [
  "PilaWilkie",
  "Pila-Wilkie",
  "Pila Wilkie",
  "OMinimal",
  "oMinimal",
  "o-minimal",
  "cell decomposition",
  "algebraicPart",
  "subpolynomial"
]

/-- The external audit records exactly the nine requested search terms. -/
theorem pilaWilkieExternalAuditSearchTerms_length :
    pilaWilkieExternalAuditSearchTerms.length = 9 :=
  rfl

/--
Machine-readable summary for the external audit child.

No checked Lean 4 Pila-Wilkie theorem, o-minimality API, algebraic-part API, or
subpolynomial counting theorem was found in the repo-local dependency closure.
The authenticated GitHub code-search step was blocked by a missing local GitHub
login, so the runtime ledger records this as a concrete audit limitation rather
than as positive evidence of absence from all public Lean 4 repositories.
-/
def pilaWilkieExternalAuditLean4ClosureFound : Bool :=
  false

/-- No external upstream closure is pinned or imported by this child. -/
def pilaWilkieExternalAuditDependencyFeasibleNow : Bool :=
  false

/-- Current machine status after the external-audit child. -/
def pilaWilkieExternalAuditCurrentMachineStatus : String :=
  "not_repo_local_closed"

/-- Current machine-proof debt after the external-audit child. -/
def pilaWilkieExternalAuditMachineProofDebt : String :=
  "formalization_debt"

/-- M0387 gate: the external audit makes no completed-state integration claim. -/
def pilaWilkieExternalAuditRepoLocalIntegrationDebtRetainedInCompletedState : Bool :=
  false

/--
Wrapper-gate diagnosis for `THM-M-0441.wrapper-gate`.

The prior external audit did not verify a Lean 4 upstream closure for
Pila-Wilkie.  Consequently this file records the gate decision instead of adding
a new Lake dependency or pretending that the statement boundary is a theorem.
-/
def pilaWilkieWrapperGateUpstreamClosureFound : Bool :=
  pilaWilkieExternalAuditLean4ClosureFound

/-- No pinned dependency was added for Pila-Wilkie by the wrapper gate. -/
def pilaWilkieWrapperGatePinnedDependencyAdded : Bool :=
  false

/-- No local theorem wrapper was added because no upstream closure was verified. -/
def pilaWilkieWrapperGateLocalWrapperAdded : Bool :=
  false

/-- Current machine status after the wrapper-gate child. -/
def pilaWilkieWrapperGateCurrentMachineStatus : String :=
  "not_repo_local_closed"

/-- Current machine-proof debt after the wrapper-gate child. -/
def pilaWilkieWrapperGateMachineProofDebt : String :=
  "formalization_debt"

/-- M0387 gate: the wrapper gate makes no completed-state integration claim. -/
def pilaWilkieWrapperGateRepoLocalIntegrationDebtRetainedInCompletedState : Bool :=
  false

/-- Checked wrapper-gate outcome: no verified upstream closure was available to wrap. -/
theorem pilaWilkieWrapperGate_noVerifiedClosure :
    [ pilaWilkieWrapperGateUpstreamClosureFound
    , pilaWilkieWrapperGatePinnedDependencyAdded
    , pilaWilkieWrapperGateLocalWrapperAdded
    , pilaWilkieWrapperGateRepoLocalIntegrationDebtRetainedInCompletedState
    ] = [false, false, false, false] :=
  rfl

/-- Public backfill notes for the `THM-M-0441.wrapper-gate` child. -/
def pilaWilkieWrapperGatePublicBackfillNotes : List String := [
  "No Lean 4 upstream closure for Pila-Wilkie was verified by the available external audit, so this child did not add a pinned dependency.",
  "No local wrapper theorem was added: StatementShape remains a statement-normalization boundary, not a terminal theorem.",
  "The parent theorem remains not_repo_local_closed / formalization_debt.",
  "No completed-state repo_local_integration_debt is claimed or retained."
]

/-- Special-case branches audited by `THM-M-0441.special-cases`. -/
inductive PilaWilkieSpecialCaseCandidate where
  | semialgebraic
  | oneDimensional
  deriving DecidableEq, Repr

/-- Stable public code for each audited Pila-Wilkie special-case branch. -/
def PilaWilkieSpecialCaseCandidate.code : PilaWilkieSpecialCaseCandidate -> String
  | PilaWilkieSpecialCaseCandidate.semialgebraic =>
      "M0441-SC-01-semialgebraic"
  | PilaWilkieSpecialCaseCandidate.oneDimensional =>
      "M0441-SC-02-one-dimensional"

/--
Current mathlib-readiness diagnosis for each special-case branch.

`false` here is not a mathematical impossibility claim.  It records that the
audited repo-local mathlib closure does not currently expose enough named API to
close the semialgebraic or one-dimensional Pila-Wilkie special cases as Lean
theorems without adding new substantial formalization infrastructure.
-/
def PilaWilkieSpecialCaseCandidate.currentMathlibCanClose :
    PilaWilkieSpecialCaseCandidate -> Bool
  | PilaWilkieSpecialCaseCandidate.semialgebraic =>
      false
  | PilaWilkieSpecialCaseCandidate.oneDimensional =>
      false

/-- Concrete missing API names blocking each audited special-case branch. -/
def PilaWilkieSpecialCaseCandidate.mathlibApiGaps :
    PilaWilkieSpecialCaseCandidate -> List String
  | PilaWilkieSpecialCaseCandidate.semialgebraic =>
      [ "semialgebraic-set predicate and closure API"
      , "semialgebraic dimension or finite-component theorem"
      , "algebraic-part construction for positive-dimensional semialgebraic pieces"
      , "standard affine rational-height convention"
      , "bounded-height finiteness for rational points"
      , "subpolynomial asymptotic counting interface"
      ]
  | PilaWilkieSpecialCaseCandidate.oneDimensional =>
      [ "o-minimality predicate or class for ordered-field expansions"
      , "one-dimensional definable-set finite-union-of-points-and-intervals theorem"
      , "cell-decomposition or definable-dimension bridge"
      , "algebraic-part construction for positive-dimensional definable pieces"
      , "standard affine rational-height convention"
      , "bounded-height finiteness for rational points"
      , "subpolynomial asymptotic counting interface"
      ]

/-- The special-case child audits exactly the two requested branches. -/
def pilaWilkieSpecialCaseCandidates : List PilaWilkieSpecialCaseCandidate := [
  PilaWilkieSpecialCaseCandidate.semialgebraic,
  PilaWilkieSpecialCaseCandidate.oneDimensional
]

/-- The checked special-case audit contains exactly two candidate branches. -/
theorem pilaWilkieSpecialCaseCandidates_length :
    pilaWilkieSpecialCaseCandidates.length = 2 :=
  rfl

/-- Stable public codes for the checked special-case audit, in order. -/
theorem pilaWilkieSpecialCaseCandidates_codes :
    pilaWilkieSpecialCaseCandidates.map PilaWilkieSpecialCaseCandidate.code =
      [ "M0441-SC-01-semialgebraic"
      , "M0441-SC-02-one-dimensional"
      ] :=
  rfl

/--
Checked diagnosis: neither audited special-case branch closes with only the
current mathlib surface.
-/
theorem pilaWilkieSpecialCaseCandidates_currentMathlibCanClose :
    pilaWilkieSpecialCaseCandidates.map
        PilaWilkieSpecialCaseCandidate.currentMathlibCanClose =
      [false, false] :=
  rfl

/-- The semialgebraic branch has six concrete missing API groups in this audit. -/
theorem semialgebraicSpecialCaseApiGapCount :
    (PilaWilkieSpecialCaseCandidate.mathlibApiGaps
      PilaWilkieSpecialCaseCandidate.semialgebraic).length = 6 :=
  rfl

/-- The one-dimensional branch has seven concrete missing API groups in this audit. -/
theorem oneDimensionalSpecialCaseApiGapCount :
    (PilaWilkieSpecialCaseCandidate.mathlibApiGaps
      PilaWilkieSpecialCaseCandidate.oneDimensional).length = 7 :=
  rfl

/-- Current machine status after the special-case audit child. -/
def pilaWilkieSpecialCasesCurrentMachineStatus : String :=
  "not_repo_local_closed"

/-- Current machine-proof debt after the special-case audit child. -/
def pilaWilkieSpecialCasesMachineProofDebt : String :=
  "formalization_debt"

/-- M0387 gate: the special-case audit makes no completed-state integration claim. -/
def pilaWilkieSpecialCasesRepoLocalIntegrationDebtRetainedInCompletedState : Bool :=
  false

/-- Public backfill notes for the `THM-M-0441.special-cases` child. -/
def pilaWilkieSpecialCasesPublicBackfillNotes : List String := [
  "The checked Lean artifact audits two possible early special cases: semialgebraic sets and one-dimensional definable sets.",
  "For the pinned mathlib closure, both candidates are recorded as not currently closable by mathlib alone: no named semialgebraic-set API, o-minimality API, one-dimensional finite-union theorem, definable dimension/cell-decomposition bridge, algebraic-part construction, rational-height package, or subpolynomial counting theorem is available in the local imports.",
  "A finite-remainder conditional boundary is recorded by FiniteRemainderSpecialCaseBoundary, but it is only a boundary: future work must prove that the chosen semialgebraic or one-dimensional case supplies that finite remainder and connects it to a concrete asymptotic bound.",
  "Current machine status remains not_repo_local_closed / formalization_debt; no completed-state repo_local_integration_debt is claimed."
]

/-- Rational points of height at most `B` lying in `X` but outside its algebraic part. -/
def rationalPointsInTranscendentalPart
    {L : FirstOrder.Language.{u, v}} {M : Type w}
    [Field M] [LinearOrder M] [IsStrictOrderedRing M] [L.Structure M]
    {D : OMinimalExpansionData L M} {n : ℕ}
    (Bnd : PilaWilkieArityBoundary D n) (X : DefinableSet D n) (B : ℕ) :
    Set (RationalPoint n) :=
  { q | rationalPointMap M n q ∈ X.1 ∧
      rationalPointMap M n q ∉ Bnd.algebraicPart X ∧
      Bnd.height q ≤ B }

/--
Conditional finite-remainder boundary for future special-case work.

For semialgebraic or one-dimensional branches, the expected mathematical route is
to show that the transcendental remainder is finite, or at least finite in every
height slice, after the algebraic part is removed.  The current mathlib snapshot
does not prove that route, so this structure records only the checked interface
that such a future special-case theorem would have to fill.
-/
structure FiniteRemainderSpecialCaseBoundary
    {L : FirstOrder.Language.{u, v}} {M : Type w}
    [Field M] [LinearOrder M] [IsStrictOrderedRing M] [L.Structure M]
    {D : OMinimalExpansionData L M} {n : ℕ}
    (Bnd : PilaWilkieArityBoundary D n) where
  X : DefinableSet D n
  finiteTranscendentalRationalPoints :
    ∀ B : ℕ, (rationalPointsInTranscendentalPart Bnd X B).Finite

/-- The finite-remainder boundary exposes finite bounded-height slices. -/
theorem FiniteRemainderSpecialCaseBoundary.finite_slice
    {L : FirstOrder.Language.{u, v}} {M : Type w}
    [Field M] [LinearOrder M] [IsStrictOrderedRing M] [L.Structure M]
    {D : OMinimalExpansionData L M} {n : ℕ}
    {Bnd : PilaWilkieArityBoundary D n}
    (Pkg : FiniteRemainderSpecialCaseBoundary Bnd) (B : ℕ) :
    (rationalPointsInTranscendentalPart Bnd Pkg.X B).Finite :=
  Pkg.finiteTranscendentalRationalPoints B

/--
Stage1 normalized statement-shape for the Pila-Wilkie theorem.

For every o-minimal expansion and arity, once the missing height convention,
algebraic-part construction, and subpolynomial bound predicate are supplied, every
definable set has subpolynomially many rational points of bounded height outside
its algebraic part.

This is the public Stage1 statement-normalization boundary for `THM-M-0441`.
It is intentionally not a terminal formalization of the classical Pila-Wilkie
theorem: the o-minimality API, algebraic-part construction, height convention,
and asymptotic counting theorem remain supplied as boundary data.
-/
def StatementShape : Prop :=
  ∀ {L : FirstOrder.Language.{u, v}} {M : Type w}
    [Field M] [LinearOrder M] [IsStrictOrderedRing M] [L.Structure M]
    (D : OMinimalExpansionData L M), D.isOMinimal ->
    ∀ (n : ℕ), ∃ Bnd : PilaWilkieArityBoundary D n,
      ∀ X : DefinableSet D n,
        Bnd.subpolynomialBound (rationalPointsInTranscendentalPart Bnd X)

/--
Checked public-normalization hook for `THM-M-0441.statement`.

Integrators should cite `StatementShape` as the repo-local Lean boundary.  This
alias exists only to make the public backfill target explicit inside the Lean
artifact; it adds no proof of Pila-Wilkie beyond the normalized statement shape.
-/
def StatementNormalizationBoundary : Prop :=
  StatementShape.{u, v, w}

/-- The public-normalization hook is exactly the existing `StatementShape`. -/
theorem statementNormalizationBoundary_iff :
    StatementNormalizationBoundary.{u, v, w} ↔ StatementShape.{u, v, w} :=
  Iff.rfl

/-- The rational point map is definitionally coordinatewise rational casting. -/
theorem rationalPointMap_apply
    (M : Type u) [Field M] (n : ℕ) (q : RationalPoint n) (i : Fin n) :
    rationalPointMap M n q i = (q i : M) :=
  rfl

/-- Mathlib definability supplies a checked empty definable set wrapper. -/
theorem definable_empty
    {L : FirstOrder.Language.{u, v}} {M : Type w} [L.Structure M] (A : Set M) (n : ℕ) :
    A.Definable L (∅ : Set (Fin n -> M)) :=
  Set.definable_empty

/-- Mathlib definability supplies a checked universal definable set wrapper. -/
theorem definable_univ
    {L : FirstOrder.Language.{u, v}} {M : Type w} [L.Structure M] (A : Set M) (n : ℕ) :
    A.Definable L (Set.univ : Set (Fin n -> M)) :=
  Set.definable_univ

/-- The rational-point slice definition unfolds to its three intended conditions. -/
theorem mem_rationalPointsInTranscendentalPart_iff
    {L : FirstOrder.Language.{u, v}} {M : Type w}
    [Field M] [LinearOrder M] [IsStrictOrderedRing M] [L.Structure M]
    {D : OMinimalExpansionData L M} {n : ℕ}
    (Bnd : PilaWilkieArityBoundary D n) (X : DefinableSet D n) (B : ℕ) (q : RationalPoint n) :
    q ∈ rationalPointsInTranscendentalPart Bnd X B <->
      rationalPointMap M n q ∈ X.1 ∧
        rationalPointMap M n q ∉ Bnd.algebraicPart X ∧
        Bnd.height q ≤ B :=
  Iff.rfl

end S1_M_087
end Stage1
end AwesomeTheorems
