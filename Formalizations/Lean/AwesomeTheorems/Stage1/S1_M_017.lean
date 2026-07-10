import Mathlib.Algebra.LinearRecurrence
import Mathlib.Algebra.CharZero.Defs
import Mathlib.Analysis.Analytic.IsolatedZeros
import Mathlib.LinearAlgebra.Eigenspace.Triangularizable
import Mathlib.LinearAlgebra.JordanChevalley
import Mathlib.NumberTheory.LocalField.Basic
import Mathlib.NumberTheory.Padics.MahlerBasis
import Mathlib.NumberTheory.Padics.PadicNumbers

/-!
# S1-M-017 / THM-M-0404: Skolem-Mahler-Lech theorem

This Stage1 artifact records conservative Lean 4 statement shapes for the
Skolem-Mahler-Lech theorem: over a characteristic-zero field, the zero set of a
linear recurrence sequence is eventually periodic, equivalently a finite union
of arithmetic progressions, up to a finite exceptional set.

The local mathlib dependency provides the `LinearRecurrence` object model and
basic solution API, but this file does not claim a kernel-checked proof of the
Skolem-Mahler-Lech theorem.
-/

noncomputable section

universe u

open Filter ValuativeRel
open scoped Topology WithZero

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_017

/-- A natural-number arithmetic progression, allowing step `0` so singleton
progressions can be represented uniformly when needed. -/
def NatArithmeticProgression (start step n : Nat) : Prop :=
  ∃ k : Nat, n = start + step * k

/-- Membership in one of a finite list of natural-number arithmetic
progressions.  Each pair stores `(start, step)`. -/
def CoveredByProgressions (progressions : List (Nat × Nat)) (n : Nat) : Prop :=
  ∃ p : Nat × Nat, p ∈ progressions ∧ NatArithmeticProgression p.1 p.2 n

/-- Zero-set predicate attached to a sequence. -/
def zeroSetPredicate {K : Type u} [Zero K] (u : Nat → K) : Nat → Prop :=
  fun n : Nat => u n = 0

/--
The finite-union conclusion used by the Skolem-Mahler-Lech statement shape.

`exceptions` records the finite exceptional zero set and `progressions` records
the finitely many arithmetic progressions.  The predicate `S` is written as
`Nat → Prop` to avoid committing to a particular `Set Nat` API in this Stage1
boundary file.
-/
def IsFiniteUnionOfArithmeticProgressions (S : Nat → Prop) : Prop :=
  ∃ exceptions : List Nat,
    ∃ progressions : List (Nat × Nat),
      ∀ n : Nat, S n ↔ n ∈ exceptions ∨ CoveredByProgressions progressions n

/--
Eventual periodicity of a natural-number predicate.

This is the second public statement-normalization variant for
Skolem-Mahler-Lech.  A later package must prove the equivalence between this
predicate and `IsFiniteUnionOfArithmeticProgressions` for subsets of `Nat`; this
Stage1 child only fixes the shape and does not claim that equivalence.
-/
def IsEventuallyPeriodic (S : Nat → Prop) : Prop :=
  ∃ N period : Nat, 0 < period ∧ ∀ n : Nat, N ≤ n → (S (n + period) ↔ S n)

/--
P03 bridge target: eventual periodicity is equivalent to the list-based
finite-union-of-arithmetic-progressions representation for a predicate on
`Nat`.

This definition records the exact theorem statement required by the public
blueprint task.  It is intentionally a `Prop` target, not an axiom or proof
claim.
-/
def EventualPeriodicFiniteUnionAPEquivalence (S : Nat → Prop) : Prop :=
  IsEventuallyPeriodic S ↔ IsFiniteUnionOfArithmeticProgressions S

/--
Repository-wide P03 target for all subsets of `Nat`, expressed with predicates.

Closing this proposition requires a local proof body or a pinned checked
upstream theorem.  Until then it is formalization debt, not repo-local
completion.
-/
def NatSubsetEventualPeriodicFiniteUnionAPBridge : Prop :=
  ∀ S : Nat → Prop, EventualPeriodicFiniteUnionAPEquivalence S

/--
Statement-normalization note for `THM-M-0404-P00`.

The repo-local canonical Lean wrapper remains `StatementShape`, whose
conclusion is the finite-union-of-arithmetic-progressions form.  The paired
eventual-periodic form is recorded as `StatementShapeEventuallyPeriodic`.  The
bridge between the two variants is intentionally left to `THM-M-0404-P03`.
-/
def statementNormalizationNote : String :=
  "Canonical Stage1 SML variants: finite-union arithmetic progressions for the Lean wrapper; eventual periodicity as the paired normalization target; equivalence not yet proved repo-locally."

/--
Normalized Stage1 statement shape for the Skolem-Mahler-Lech theorem.

For every characteristic-zero field `K`, every linear recurrence `E` over `K`,
and every sequence `u` satisfying `E`, the zero set `{n | u n = 0}` is a finite
union of arithmetic progressions, with finitely many exceptional indices.
-/
def StatementShape : Prop :=
  ∀ (K : Type u) [Field K] [CharZero K]
    (E : LinearRecurrence K) (u : Nat → K),
      E.IsSolution u →
        IsFiniteUnionOfArithmeticProgressions (fun n : Nat => u n = 0)

/--
`THM-M-0404-P01` statement-only wrapper around mathlib's
`LinearRecurrence` object model.

This is deliberately just a named statement surface.  It imports and typechecks
the recurrence/solution API required to state Skolem-Mahler-Lech, but it does
not provide or assume a proof of the theorem.
-/
abbrev LinearRecurrenceStatementOnlyWrapper : Prop :=
  StatementShape.{u}

/--
Eventual-periodic companion statement shape for the Skolem-Mahler-Lech theorem.

This is a statement-normalization surface only.  It is not used as a proof of
`StatementShape`, and it carries no claim that the equivalence with the
finite-union arithmetic-progression form has been established in this
repository.
-/
def StatementShapeEventuallyPeriodic : Prop :=
  ∀ (K : Type u) [Field K] [CharZero K]
    (E : LinearRecurrence K) (u : Nat → K),
      E.IsSolution u →
        IsEventuallyPeriodic (fun n : Nat => u n = 0)

/-- A proof package bucket used by the Stage1 recurrence/zero-set audit. -/
inductive RecurrenceZeroSetPackage where
  | recurrenceObjectModel
  | companionMatrixReduction
  | characteristicPolynomialBridge
  | spectralExpansion
  | torsionClassDecomposition
  | nondegenerateZeroFiniteness
  | degeneratePeriodExtraction
  | finiteExceptionalSetAccounting
  | finiteUnionEventualPeriodBridge
  | pAdicAnalyticInterpolation
  | externalClosureGate
  deriving DecidableEq, Repr

/--
Typed metadata for the recurrence/zero-set proof-package queue.

These records are intentionally data rather than theorem assumptions: an entry
being listed here does not assert that its proof has been completed.
-/
structure ProofPackageAudit where
  package : RecurrenceZeroSetPackage
  code : String
  role : String
  currentStatus : String
  completionGate : String
  leafBudgetStatus : String
  deriving Repr

/-- Pinned mathlib revision used by this repository's Lake closure for P02. -/
def mathlibLinearRecurrenceRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Primary source URL for the audited `Mathlib.Algebra.LinearRecurrence` module. -/
def mathlibLinearRecurrenceSourceUrl : String :=
  "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Algebra/LinearRecurrence.lean"

/-- Primary source URL for the audited eigenspace API module. -/
def mathlibEigenspaceBasicSourceUrl : String :=
  "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/LinearAlgebra/Eigenspace/Basic.lean"

/-- Primary source URL for the audited triangularizable/eigenspace-span API module. -/
def mathlibEigenspaceTriangularizableSourceUrl : String :=
  "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/LinearAlgebra/Eigenspace/Triangularizable.lean"

/-- Primary source URL for the audited Jordan-Chevalley API module. -/
def mathlibJordanChevalleySourceUrl : String :=
  "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/LinearAlgebra/JordanChevalley.lean"

/-- Primary source URL for the audited p-adic number API module. -/
def mathlibPadicNumbersSourceUrl : String :=
  "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/NumberTheory/Padics/PadicNumbers.lean"

/-- Primary source URL for the audited p-adic Mahler basis API module. -/
def mathlibPadicMahlerBasisSourceUrl : String :=
  "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/NumberTheory/Padics/MahlerBasis.lean"

/-- Primary source URL for the audited nonarchimedean local-field API module. -/
def mathlibLocalFieldBasicSourceUrl : String :=
  "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/NumberTheory/LocalField/Basic.lean"

/-- Primary source URL for the audited analytic isolated-zeros API module. -/
def mathlibAnalyticIsolatedZerosSourceUrl : String :=
  "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Analysis/Analytic/IsolatedZeros.lean"

/-- Classification for entries in the P02 `Mathlib.Algebra.LinearRecurrence` audit. -/
inductive LinearRecurrenceAnchorKind where
  | objectModel
  | solutionApi
  | uniquenessApi
  | solutionSpaceApi
  | companionOperatorApi
  | characteristicPolynomialApi
  | negativeTerminalTheoremSearch
  deriving DecidableEq, Repr

/-- Classification for P05 spectral/Jordan decomposition audit rows. -/
inductive SpectralJordanAnchorKind where
  | generalizedEigenspaceApi
  | eigenspaceSpanApi
  | eigenvectorOrbitApi
  | jordanChevalleyApi
  | companionBridgeObligation
  | closedFormGap
  deriving DecidableEq, Repr

/-- Classification for P06 p-adic/local-field analytic interpolation audit rows. -/
inductive PadicLocalAnalyticAnchorKind where
  | padicNumberField
  | padicNormValuation
  | padicMahlerInterpolation
  | localFieldObjectModel
  | analyticIsolatedZeros
  | strassmannNegativeSearch
  | smlAnalyticInterpolationGap
  deriving DecidableEq, Repr

/-- Classification for P07 external Lean 4 search audit rows. -/
inductive ExternalLeanSearchAnchorKind where
  | sourcegraphExactSearch
  | githubRepositorySearch
  | githubAuthenticatedCodeSearchBlocked
  | leanCommunityArchiveSearch
  | externalProofCandidate
  | negativeTerminalSearch
  deriving DecidableEq, Repr

/-- Classification for P08 external proof integration rows. -/
inductive ExternalProofIntegrationKind where
  | noCandidateAvailable
  | pinnedDependencyChecked
  | concreteIntegrationBlocker
  deriving DecidableEq, Repr

/-- Classification for P09 public `<=100` leaf-ledger gate rows. -/
inductive PublicLeafLedgerGateKind where
  | blockedMachineAnchorUnstable
  | blockedPackageTreeUnstable
  | readyForSerialPublicBackfill
  deriving DecidableEq, Repr

/--
Typed P02 audit row for exact `Mathlib.Algebra.LinearRecurrence` anchors.

Rows are metadata about checked declarations in the pinned dependency. They do
not assert a proof of Skolem-Mahler-Lech.
-/
structure MathlibLinearRecurrenceAnchorAudit where
  moduleName : String
  sourceRevision : String
  sourceUrl : String
  anchorName : String
  kind : LinearRecurrenceAnchorKind
  mathematicalRole : String
  repoLocalStatus : String
  completionGate : String
  deriving Repr

/--
Typed P05 audit row for spectral/Jordan decomposition APIs relevant to
polynomial-times-geometric closed forms.

Rows record checked API anchors and open bridge obligations; they do not assert
the closed-form expansion theorem needed for Skolem-Mahler-Lech.
-/
structure SpectralJordanAnchorAudit where
  moduleName : String
  sourceRevision : String
  sourceUrl : String
  anchorName : String
  kind : SpectralJordanAnchorKind
  mathematicalRole : String
  repoLocalStatus : String
  completionGate : String
  deriving Repr

/--
Typed P06 audit row for p-adic, local-field, and analytic APIs relevant to the
analytic interpolation branch of Skolem-Mahler-Lech.

Rows record available checked anchors or explicit negative findings.  They do
not assert a Strassmann theorem or a completed SML analytic branch.
-/
structure PadicLocalAnalyticAnchorAudit where
  moduleName : String
  sourceRevision : String
  sourceUrl : String
  anchorName : String
  kind : PadicLocalAnalyticAnchorKind
  mathematicalRole : String
  repoLocalStatus : String
  completionGate : String
  deriving Repr

/--
Typed P07 row for authenticated-primary-source external Lean 4 search.

Rows record the search surface and candidate status.  A negative row is not a
proof of absence; it is an auditable checkpoint saying no importable Lean 4
Skolem-Mahler-Lech proof candidate was found by the listed query.
-/
structure ExternalLeanSearchAudit where
  searchSurface : String
  queryOrRepositoryUrl : String
  repositoryUrl : String
  commitOrRevision : String
  modulePath : String
  theoremName : String
  buildStatus : String
  kind : ExternalLeanSearchAnchorKind
  repoLocalStatus : String
  completionGate : String
  deriving Repr

/--
Typed P08 row for attempting repo-local integration of an external Lean 4
Skolem-Mahler-Lech proof candidate.

Rows in the current artifact are gate metadata only.  They do not assert that a
candidate proof exists or that the theorem has been completed.
-/
structure ExternalProofIntegrationAudit where
  upstreamSearchAudit : String
  repositoryUrl : String
  commitOrRevision : String
  modulePath : String
  theoremName : String
  integrationAction : String
  validationCommand : String
  validationResult : String
  kind : ExternalProofIntegrationKind
  repoLocalStatus : String
  completionGate : String
  deriving Repr

/--
Typed P09 row for the public `<=100` leaf-ledger creation gate.

Rows are process metadata only.  They record whether the machine anchor and
package tree are stable enough for a serial public-doc integrator to create a
public leaf ledger.
-/
structure PublicLeafLedgerGateAudit where
  taskCode : String
  publicMergeTarget : String
  machineAnchorStatus : String
  packageTreeStatus : String
  externalIntegrationStatus : String
  kind : PublicLeafLedgerGateKind
  repoLocalStatus : String
  completionGate : String
  proposedAction : String
  deriving Repr


/--
P02 audit table for `Mathlib.Algebra.LinearRecurrence` at the pinned mathlib
revision.

The positive rows are backed by the `#check` probes below.  The final row records
the negative terminal-theorem finding for this module: it supplies recurrence
infrastructure, not a checked Skolem-Mahler-Lech theorem.
-/
def mathlibLinearRecurrenceAnchorAuditTable :
    List MathlibLinearRecurrenceAnchorAudit := [
  {
    moduleName := "Mathlib.Algebra.LinearRecurrence",
    sourceRevision := mathlibLinearRecurrenceRevision,
    sourceUrl := mathlibLinearRecurrenceSourceUrl,
    anchorName := "LinearRecurrence",
    kind := LinearRecurrenceAnchorKind.objectModel,
    mathematicalRole := "Structure storing the order and coefficients of a linear recurrence over a commutative semiring.",
    repoLocalStatus := "checked_upstream_anchor: available through the pinned mathlib import.",
    completionGate := "Use as the object model for local statement wrappers; not by itself an SML theorem."
  },
  {
    moduleName := "Mathlib.Algebra.LinearRecurrence",
    sourceRevision := mathlibLinearRecurrenceRevision,
    sourceUrl := mathlibLinearRecurrenceSourceUrl,
    anchorName := "LinearRecurrence.IsSolution",
    kind := LinearRecurrenceAnchorKind.solutionApi,
    mathematicalRole := "Predicate that a sequence satisfies the recurrence equation.",
    repoLocalStatus := "checked_upstream_anchor: used by StatementShape and its wrappers.",
    completionGate := "All local SML statements should quantify solutions through this predicate."
  },
  {
    moduleName := "Mathlib.Algebra.LinearRecurrence",
    sourceRevision := mathlibLinearRecurrenceRevision,
    sourceUrl := mathlibLinearRecurrenceSourceUrl,
    anchorName := "LinearRecurrence.mkSol / is_sol_mkSol",
    kind := LinearRecurrenceAnchorKind.solutionApi,
    mathematicalRole := "Constructs the solution determined by initial values and proves it satisfies the recurrence.",
    repoLocalStatus := "checked_upstream_anchor: construction exists in pinned mathlib.",
    completionGate := "Use for initial-condition and finite-prefix arguments when building proof leaves."
  },
  {
    moduleName := "Mathlib.Algebra.LinearRecurrence",
    sourceRevision := mathlibLinearRecurrenceRevision,
    sourceUrl := mathlibLinearRecurrenceSourceUrl,
    anchorName := "LinearRecurrence.eq_mk_of_is_sol_of_eq_init / eq_mk_of_is_sol_of_eq_init'",
    kind := LinearRecurrenceAnchorKind.uniquenessApi,
    mathematicalRole := "Uniqueness of a recurrence solution from its first `order` values.",
    repoLocalStatus := "checked_upstream_anchor: uniqueness API exists in pinned mathlib.",
    completionGate := "Use to justify finite-prefix normalization in later proof packages."
  },
  {
    moduleName := "Mathlib.Algebra.LinearRecurrence",
    sourceRevision := mathlibLinearRecurrenceRevision,
    sourceUrl := mathlibLinearRecurrenceSourceUrl,
    anchorName := "LinearRecurrence.solSpace / toInit / sol_eq_of_eq_init / solSpace_rank",
    kind := LinearRecurrenceAnchorKind.solutionSpaceApi,
    mathematicalRole := "Packages recurrence solutions as a submodule and identifies it with initial values.",
    repoLocalStatus := "checked_upstream_anchor: linear solution-space API exists.",
    completionGate := "Bridge from the sequence formulation to linear-algebraic proof branches."
  },
  {
    moduleName := "Mathlib.Algebra.LinearRecurrence",
    sourceRevision := mathlibLinearRecurrenceRevision,
    sourceUrl := mathlibLinearRecurrenceSourceUrl,
    anchorName := "LinearRecurrence.tupleSucc",
    kind := LinearRecurrenceAnchorKind.companionOperatorApi,
    mathematicalRole := "Linear map sending an initial tuple to its successor tuple, i.e. the companion-operator surface.",
    repoLocalStatus := "checked_upstream_anchor: available for the companion-matrix reduction package.",
    completionGate := "P04 must connect iterates of this operator to sequence values and matrix/spectral APIs."
  },
  {
    moduleName := "Mathlib.Algebra.LinearRecurrence",
    sourceRevision := mathlibLinearRecurrenceRevision,
    sourceUrl := mathlibLinearRecurrenceSourceUrl,
    anchorName := "LinearRecurrence.charPoly / charPoly_monic / geom_sol_iff_root_charPoly",
    kind := LinearRecurrenceAnchorKind.characteristicPolynomialApi,
    mathematicalRole := "Characteristic polynomial and geometric-solution/root equivalence.",
    repoLocalStatus := "checked_upstream_anchor: root/geometric-sequence bridge exists.",
    completionGate := "P05 must extend this to the selected spectral or Jordan decomposition branch."
  },
  {
    moduleName := "Mathlib.Algebra.LinearRecurrence",
    sourceRevision := mathlibLinearRecurrenceRevision,
    sourceUrl := mathlibLinearRecurrenceSourceUrl,
    anchorName := "Skolem-Mahler-Lech zero-set theorem",
    kind := LinearRecurrenceAnchorKind.negativeTerminalTheoremSearch,
    mathematicalRole := "Terminal theorem that the zero set of a characteristic-zero recurrence is eventually periodic or a finite union of arithmetic progressions.",
    repoLocalStatus := "not_repo_local_closed: no such theorem is provided by this pinned module.",
    completionGate := "Provide a local proof body, a pinned mathlib theorem if one later appears, or a pinned external dependency with repo-local validation."
  }
]

/--
P05 audit table for spectral/Jordan decomposition APIs at the pinned mathlib
revision.

The checked positive rows identify reusable local anchors for generalized
eigenspaces, algebraically closed finite-dimensional spectral spanning,
eigenvector orbit evaluation, and Jordan-Chevalley decomposition.  The final
rows record the bridge still missing for Skolem-Mahler-Lech: no checked
repo-local theorem currently converts the companion-operator orbit into a full
polynomial-times-geometric closed-form expansion.
-/
def spectralJordanAnchorAuditTable : List SpectralJordanAnchorAudit := [
  {
    moduleName := "Mathlib.LinearAlgebra.Eigenspace.Basic",
    sourceRevision := mathlibLinearRecurrenceRevision,
    sourceUrl := mathlibEigenspaceBasicSourceUrl,
    anchorName := "Module.End.genEigenspace / Module.End.mem_genEigenspace_nat",
    kind := SpectralJordanAnchorKind.generalizedEigenspaceApi,
    mathematicalRole := "Defines generalized eigenspaces as kernels of powers of `(f - mu • 1)` and exposes finite-exponent membership.",
    repoLocalStatus := "checked_upstream_anchor: imported and wrapped by `genEigenspace_nat_kernel`.",
    completionGate := "Use this as the kernel filtration for Jordan block and nilpotent-part arguments."
  },
  {
    moduleName := "Mathlib.LinearAlgebra.Eigenspace.Triangularizable",
    sourceRevision := mathlibLinearRecurrenceRevision,
    sourceUrl := mathlibEigenspaceTriangularizableSourceUrl,
    anchorName := "Module.End.iSup_maxGenEigenspace_eq_top",
    kind := SpectralJordanAnchorKind.eigenspaceSpanApi,
    mathematicalRole := "Over an algebraically closed field in finite dimension, maximal generalized eigenspaces span the whole module.",
    repoLocalStatus := "checked_upstream_anchor: imported and wrapped by `algClosed_iSup_maxGenEigenspace_eq_top`.",
    completionGate := "Supply the field-extension/base-change bridge from the recurrence companion operator to an algebraically closed finite-dimensional setting."
  },
  {
    moduleName := "Mathlib.LinearAlgebra.Eigenspace.Basic",
    sourceRevision := mathlibLinearRecurrenceRevision,
    sourceUrl := mathlibEigenspaceBasicSourceUrl,
    anchorName := "Module.End.HasUnifEigenvector.pow_apply",
    kind := SpectralJordanAnchorKind.eigenvectorOrbitApi,
    mathematicalRole := "Evaluates iterates of an eigenvector as `mu ^ n • v`, the geometric part of the desired closed form.",
    repoLocalStatus := "checked_upstream_anchor: imported and wrapped by `hasUnifEigenvector_pow_apply`.",
    completionGate := "Extend from eigenvectors to generalized eigenvectors, producing finite polynomial factors from the nilpotent filtration."
  },
  {
    moduleName := "Mathlib.LinearAlgebra.JordanChevalley",
    sourceRevision := mathlibLinearRecurrenceRevision,
    sourceUrl := mathlibJordanChevalleySourceUrl,
    anchorName := "Module.End.exists_isNilpotent_isSemisimple",
    kind := SpectralJordanAnchorKind.jordanChevalleyApi,
    mathematicalRole := "Decomposes a finite-dimensional endomorphism over a perfect field into nilpotent and semisimple summands polynomial in the operator.",
    repoLocalStatus := "checked_upstream_anchor: imported and wrapped by `exists_isNilpotent_isSemisimple_anchor`.",
    completionGate := "Decide whether the SML package uses this decomposition directly or instead works through generalized eigenspaces after algebraic closure."
  },
  {
    moduleName := "AwesomeTheorems.Stage1.S1_M_017",
    sourceRevision := "repo-local",
    sourceUrl := "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_017.lean",
    anchorName := "companionState_solutionWindow / zeroSet_iff_companionState_first",
    kind := SpectralJordanAnchorKind.companionBridgeObligation,
    mathematicalRole := "Connects recurrence solution values to iterates of `LinearRecurrence.tupleSucc`, the operator to which spectral APIs must be applied.",
    repoLocalStatus := "checked_local_support: companion orbit bridge is present for positive order, with a zero-order boundary theorem.",
    completionGate := "Construct the finite-dimensional module equivalence and coordinate functional needed to feed `tupleSucc` into the selected spectral/Jordan route."
  },
  {
    moduleName := "AwesomeTheorems.Stage1.S1_M_017",
    sourceRevision := "repo-local",
    sourceUrl := "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_017.lean",
    anchorName := "polynomial-times-geometric closed-form theorem",
    kind := SpectralJordanAnchorKind.closedFormGap,
    mathematicalRole := "Terminal P05 lemma expanding every companion-coordinate orbit as a finite sum of polynomial functions in `n` times powers of characteristic roots.",
    repoLocalStatus := "formalization_debt: no such repo-local theorem or pinned upstream theorem is integrated.",
    completionGate := "Provide a local proof from generalized eigenspaces/Jordan-Chevalley data or pin/import/check an upstream Lean theorem with this exact statement."
  }
]

/--
P06 audit table for the p-adic/local-field analytic interpolation branch.

The positive rows are backed by imports and `#check` probes below.  The
Strassmann row is a negative audit result for the pinned mathlib revision:
local searches did not locate a theorem named or documented as Strassmann.
The available isolated-zero theorem is useful analytic infrastructure but is
not a substitute for Strassmann's p-adic power-series zero bound.
-/
def padicLocalAnalyticAnchorAuditTable : List PadicLocalAnalyticAnchorAudit := [
  {
    moduleName := "Mathlib.NumberTheory.Padics.PadicNumbers",
    sourceRevision := mathlibLinearRecurrenceRevision,
    sourceUrl := mathlibPadicNumbersSourceUrl,
    anchorName := "Padic / ℚ_[p] / Padic.nonarchimedean / Padic.complete",
    kind := PadicLocalAnalyticAnchorKind.padicNumberField,
    mathematicalRole := "Provides the p-adic field `ℚ_[p]`, its normed-field structure, nonarchimedean triangle inequality, rational density, and completeness.",
    repoLocalStatus := "checked_upstream_anchor: imported and wrapped by p-adic support lemmas in this file.",
    completionGate := "Use as the base field for a first p-adic analytic interpolation prototype before generalizing to arbitrary local fields."
  },
  {
    moduleName := "Mathlib.NumberTheory.Padics.PadicNumbers",
    sourceRevision := mathlibLinearRecurrenceRevision,
    sourceUrl := mathlibPadicNumbersSourceUrl,
    anchorName := "Padic.norm_p / Padic.valuation / Padic.addValuation",
    kind := PadicLocalAnalyticAnchorKind.padicNormValuation,
    mathematicalRole := "Supplies p-adic norm and valuation controls needed for convergence estimates and binomial/power-series arguments.",
    repoLocalStatus := "checked_upstream_anchor: declarations are available from the pinned import.",
    completionGate := "Connect these estimates to the chosen analytic interpolation theorem; no zero-counting theorem is obtained from valuations alone."
  },
  {
    moduleName := "Mathlib.NumberTheory.Padics.MahlerBasis",
    sourceRevision := mathlibLinearRecurrenceRevision,
    sourceUrl := mathlibPadicMahlerBasisSourceUrl,
    anchorName := "PadicInt.continuous_choose / PadicInt.hasSum_mahler / PadicInt.mahlerEquiv_apply",
    kind := PadicLocalAnalyticAnchorKind.padicMahlerInterpolation,
    mathematicalRole := "Provides continuous binomial/Mahler-basis infrastructure on `ℤ_[p]`, a plausible substrate for interpolation of integer-indexed functions.",
    repoLocalStatus := "checked_upstream_anchor: imported and probed, but not connected to recurrence zero sets.",
    completionGate := "Prove or import the specific interpolation lemma for recurrence subsequences, including convergence and coefficient-decay hypotheses."
  },
  {
    moduleName := "Mathlib.NumberTheory.LocalField.Basic",
    sourceRevision := mathlibLinearRecurrenceRevision,
    sourceUrl := mathlibLocalFieldBasicSourceUrl,
    anchorName := "IsNonarchimedeanLocalField / valueGroupWithZeroIsoInt / finite residue field",
    kind := PadicLocalAnalyticAnchorKind.localFieldObjectModel,
    mathematicalRole := "Packages complete locally compact nonarchimedean fields with discrete rank-one value group and finite residue field consequences.",
    repoLocalStatus := "checked_upstream_anchor: imported and wrapped by local-field support lemmas in this file.",
    completionGate := "Decide whether the SML analytic branch is first built over `ℚ_[p]` or over the abstract `IsNonarchimedeanLocalField` interface."
  },
  {
    moduleName := "Mathlib.Analysis.Analytic.IsolatedZeros",
    sourceRevision := mathlibLinearRecurrenceRevision,
    sourceUrl := mathlibAnalyticIsolatedZerosSourceUrl,
    anchorName := "AnalyticAt.eventually_eq_zero_or_eventually_ne_zero / HasFPowerSeriesAt.locally_ne_zero",
    kind := PadicLocalAnalyticAnchorKind.analyticIsolatedZeros,
    mathematicalRole := "Gives a general normed-field isolated-zero principle for analytic functions.",
    repoLocalStatus := "checked_upstream_anchor: imported and wrapped locally; useful but weaker/different from Strassmann's p-adic zero bound.",
    completionGate := "Show that the interpolating function is analytic on the relevant p-adic ball and that the zero-set accumulation argument suffices, or import a Strassmann theorem."
  },
  {
    moduleName := "Pinned mathlib local source search",
    sourceRevision := mathlibLinearRecurrenceRevision,
    sourceUrl := "Formalizations/Lean/.lake/packages/mathlib/Mathlib",
    anchorName := "Strassmann / strassmann",
    kind := PadicLocalAnalyticAnchorKind.strassmannNegativeSearch,
    mathematicalRole := "Expected p-adic theorem bounding zeros of a power series by the dominant coefficient index.",
    repoLocalStatus := "negative_search_result: no Strassmann theorem was located in the pinned local mathlib source during this child audit.",
    completionGate := "Either formalize Strassmann locally, find a differently named equivalent theorem, or record a concrete upstream integration blocker."
  },
  {
    moduleName := "AwesomeTheorems.Stage1.S1_M_017",
    sourceRevision := "repo-local",
    sourceUrl := "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_017.lean",
    anchorName := "SML p-adic analytic interpolation branch",
    kind := PadicLocalAnalyticAnchorKind.smlAnalyticInterpolationGap,
    mathematicalRole := "Terminal branch converting recurrence subsequences into p-adic analytic functions and deriving finite/periodic zero behavior from the p-adic zero theorem.",
    repoLocalStatus := "formalization_debt: no checked local branch or pinned upstream theorem is integrated.",
    completionGate := "Select the base-field interface, prove interpolation/convergence, and close zeros using a checked Strassmann or sufficient isolated-zero replacement."
  }
]

/-- Calendar date of the P07 external Lean 4 search audit. -/
def externalLeanSearchAuditDate : String := "2026-05-01"

/--
P07 external Lean 4 search audit for Skolem-Mahler-Lech.

The pass found no repository/module/theorem candidate that can be pinned and
imported.  The GitHub authenticated code-search lane is recorded as blocked
because the local `gh` client reported no authenticated GitHub host.
-/
def externalLeanSearchAuditTable : List ExternalLeanSearchAudit := [
  {
    searchSurface := "Sourcegraph public code search",
    queryOrRepositoryUrl := "https://sourcegraph.com/search?q=context:global+archived:yes+fork:yes+%22Skolem-Mahler-Lech%22+lang:Lean",
    repositoryUrl := "none",
    commitOrRevision := "not_applicable",
    modulePath := "none",
    theoremName := "none",
    buildStatus := "not_applicable: exact public-code search returned matchCount=0.",
    kind := ExternalLeanSearchAnchorKind.sourcegraphExactSearch,
    repoLocalStatus := "negative_search_result: no Lean source hit for exact `Skolem-Mahler-Lech` spelling.",
    completionGate := "Continue to treat SML as formalization_debt unless a concrete Lean repository, commit, module path, theorem name, and build result are found."
  },
  {
    searchSurface := "Sourcegraph public code search",
    queryOrRepositoryUrl := "https://sourcegraph.com/search?q=context:global+archived:yes+fork:yes+%22Skolem%20Mahler%20Lech%22+lang:Lean",
    repositoryUrl := "none",
    commitOrRevision := "not_applicable",
    modulePath := "none",
    theoremName := "none",
    buildStatus := "not_applicable: exact public-code search returned matchCount=0.",
    kind := ExternalLeanSearchAnchorKind.sourcegraphExactSearch,
    repoLocalStatus := "negative_search_result: no Lean source hit for exact spaced `Skolem Mahler Lech` spelling.",
    completionGate := "Continue to treat SML as formalization_debt unless a concrete Lean repository, commit, module path, theorem name, and build result are found."
  },
  {
    searchSurface := "Sourcegraph public code search",
    queryOrRepositoryUrl := "https://sourcegraph.com/search?q=context:global+archived:yes+fork:yes+SkolemMahlerLech+lang:Lean",
    repositoryUrl := "none",
    commitOrRevision := "not_applicable",
    modulePath := "none",
    theoremName := "none",
    buildStatus := "not_applicable: exact public-code search returned matchCount=0.",
    kind := ExternalLeanSearchAnchorKind.sourcegraphExactSearch,
    repoLocalStatus := "negative_search_result: no Lean source hit for camel-case `SkolemMahlerLech` spelling.",
    completionGate := "Continue to treat SML as formalization_debt unless a concrete Lean repository, commit, module path, theorem name, and build result are found."
  },
  {
    searchSurface := "GitHub REST repository search",
    queryOrRepositoryUrl := "https://api.github.com/search/repositories?q=%22Skolem-Mahler-Lech%22+lean",
    repositoryUrl := "none",
    commitOrRevision := "not_applicable",
    modulePath := "none",
    theoremName := "none",
    buildStatus := "not_applicable: repository search returned total_count=0.",
    kind := ExternalLeanSearchAnchorKind.githubRepositorySearch,
    repoLocalStatus := "negative_search_result: no public GitHub repository candidate was located by repository metadata search.",
    completionGate := "A future candidate must supply repository URL, commit, module path, theorem name, and local build status before P08 integration."
  },
  {
    searchSurface := "GitHub CLI authenticated code search",
    queryOrRepositoryUrl := "gh auth status",
    repositoryUrl := "none",
    commitOrRevision := "not_applicable",
    modulePath := "none",
    theoremName := "none",
    buildStatus := "blocked: local GitHub CLI reported no authenticated GitHub hosts; no authenticated GitHub code-search result is claimed.",
    kind := ExternalLeanSearchAnchorKind.githubAuthenticatedCodeSearchBlocked,
    repoLocalStatus := "integration_blocker: the authenticated GitHub code-search lane needs a configured GitHub login or token before it can count as closed.",
    completionGate := "Run authenticated GitHub code search for exact SML spellings, then record any candidate repository URL, commit, module path, theorem name, and build status."
  },
  {
    searchSurface := "Lean community Zulip archive",
    queryOrRepositoryUrl := "https://leanprover-community.github.io/archive/stream/217875-Is-there-code-for-X%3F/topic/Skolem.E2.80.93Mahler.E2.80.93Lech.20theorem.html",
    repositoryUrl := "none",
    commitOrRevision := "not_applicable",
    modulePath := "none",
    theoremName := "none",
    buildStatus := "not_applicable: community archive discussion is not an importable proof artifact.",
    kind := ExternalLeanSearchAnchorKind.leanCommunityArchiveSearch,
    repoLocalStatus := "negative_context_result: no importable Lean 4 theorem candidate is supplied by the public archive topic.",
    completionGate := "Do not use archive discussion as completion evidence; require source repository, commit, module path, theorem name, and build validation."
  },
  {
    searchSurface := "P07 terminal external proof candidate status",
    queryOrRepositoryUrl := "THM-M-0404-P07",
    repositoryUrl := "none_found",
    commitOrRevision := "none_found",
    modulePath := "none_found",
    theoremName := "none_found",
    buildStatus := "not_applicable: no candidate proof was found to build or import.",
    kind := ExternalLeanSearchAnchorKind.negativeTerminalSearch,
    repoLocalStatus := "not_repo_local_closed: no external Lean 4 SML proof has been pinned, imported, and checked in this repository.",
    completionGate := "Leave THM-M-0404 open as formalization_debt; P08 has no external proof to integrate unless a future authenticated search finds one."
  }
]

/-- Calendar date of the P08 external-proof integration gate audit. -/
def externalProofIntegrationAuditDate : String := "2026-05-01"

/--
P08 external proof integration audit for Skolem-Mahler-Lech.

Because the P07 table currently records no repository/module/theorem candidate,
there is no external proof body available to pin as a Lake dependency, vendor,
or wrap.  This is therefore a conditional gate, not a completion claim.
-/
def externalProofIntegrationAuditTable : List ExternalProofIntegrationAudit := [
  {
    upstreamSearchAudit := "externalLeanSearchAuditTable",
    repositoryUrl := "none_found",
    commitOrRevision := "none_found",
    modulePath := "none_found",
    theoremName := "none_found",
    integrationAction := "not_attempted_no_external_candidate: no repository, commit, module path, or theorem name is available for pin/import/check.",
    validationCommand := "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_017.lean",
    validationResult := "metadata_gate_only: this command validates the repo-local audit artifact, not an external SML proof.",
    kind := ExternalProofIntegrationKind.noCandidateAvailable,
    repoLocalStatus := "not_repo_local_closed: no external Lean 4 Skolem-Mahler-Lech proof has entered this repository's Lake closure.",
    completionGate := "If a future authenticated search finds a candidate, add a pinned dependency or vendored proof body and validate a local wrapper; if that fails, record the exact dependency, toolchain, license, theorem-export, or build blocker."
  }
]

/-- Calendar date of the P09 public leaf-ledger gate audit. -/
def publicLeafLedgerGateAuditDate : String := "2026-05-01"

/--
P09 public `<=100` leaf-ledger gate for Skolem-Mahler-Lech.

The public ledger should be created only after the terminal machine anchor or
the package tree is stable enough to support independent `<=100` leaves.  The
current artifact has checked support leaves and audit tables, but no completed
terminal Skolem-Mahler-Lech proof body or pinned external proof dependency.
-/
def publicLeafLedgerGateAuditTable : List PublicLeafLedgerGateAudit := [
  {
    taskCode := "THM-M-0404-P09",
    publicMergeTarget := "Docs/Stage1_Blueprint.md / Docs/todos_20260430.md serial backfill only",
    machineAnchorStatus := "unstable_terminal_anchor: no repo-local theorem or pinned external dependency proves Skolem-Mahler-Lech.",
    packageTreeStatus := "partial_tree_only: statement, recurrence object model, companion support, spectral/Jordan anchors, p-adic/local-field anchors, P07 search metadata, and P08 gate metadata are present; terminal proof leaves are still open.",
    externalIntegrationStatus := "not_repo_local_closed: P07 found no importable external Lean 4 proof candidate and P08 has no candidate to pin/import/check.",
    kind := PublicLeafLedgerGateKind.blockedMachineAnchorUnstable,
    repoLocalStatus := "formalization_debt: public leaf ledger creation is blocked until the machine anchor and package tree stabilize.",
    completionGate := "Do not create or mark a public <=100 leaf ledger complete until a checked terminal proof path or stable package tree exists, the local Lean command passes, and the serial public-doc integrator merges the authoritative ledger.",
    proposedAction := "Keep P09 open; publish only an integration-ready backfill note saying that no public <=100 leaf ledger is eligible yet."
  }
]

/--
M0387-level package split for a future Skolem-Mahler-Lech proof.

Every unchecked package below must later be replaced by a local proof body,
pinned mathlib wrapper, or pinned external dependency before any terminal
completion claim.  The current file only checks the object-model and zero-set
interfaces used to state those packages.
-/
def recurrenceZeroSetProofPackages : List ProofPackageAudit := [
  {
    package := RecurrenceZeroSetPackage.recurrenceObjectModel,
    code := "THM-M-0404-P01",
    role := "Represent a linear recurrence over a characteristic-zero field and its solution sequence.",
    currentStatus := "checked_local_support: LinearRecurrence and LinearRecurrence.IsSolution are available from mathlib.",
    completionGate := "Keep the local wrapper aligned with Mathlib.Algebra.LinearRecurrence.",
    leafBudgetStatus := "checked support leaf; not a terminal SML proof leaf."
  },
  {
    package := RecurrenceZeroSetPackage.companionMatrixReduction,
    code := "THM-M-0404-P04",
    role := "Reduce a recurrence solution to iterates of the finite-dimensional companion operator `LinearRecurrence.tupleSucc` on solution windows.",
    currentStatus := "checked_local_support: `companionState_solutionWindow` and `zeroSet_iff_companionState_first` connect solution values to iterates of `tupleSucc` for positive order; `solution_eq_zero_of_order_eq_zero` handles the zero-order boundary.",
    completionGate := "Connect this companion-operator surface to the selected matrix/spectral or Jordan API and then to exponential-polynomial closed forms.",
    leafBudgetStatus := "checked support leaf for the companion reduction; downstream spectral decomposition and analytic zero-set leaves remain unchecked."
  },
  {
    package := RecurrenceZeroSetPackage.characteristicPolynomialBridge,
    code := "THM-M-0404-P02",
    role := "Relate geometric solutions to roots of the characteristic polynomial.",
    currentStatus := "checked_local_support: LinearRecurrence.geom_sol_iff_root_charPoly is available.",
    completionGate := "Extend from geometric solutions to the selected splitting-field/Jordan-block decomposition.",
    leafBudgetStatus := "checked support leaf; spectral expansion remains unchecked."
  },
  {
    package := RecurrenceZeroSetPackage.spectralExpansion,
    code := "THM-M-0404-P05",
    role := "Expand recurrence solutions into exponential-polynomial pieces after the chosen field extension.",
    currentStatus := "partial_checked_support: P05 audit records checked mathlib anchors for generalized eigenspaces, algebraically closed generalized-eigenspace spanning, eigenvector iterates, and Jordan-Chevalley decomposition.",
    completionGate := "Provide or import a checked theorem converting companion-coordinate orbits into polynomial-times-geometric closed forms with exact field/base-change hypotheses.",
    leafBudgetStatus := "anchor audit checked; terminal closed-form expansion remains unchecked and must be split into <=100-step leaves."
  },
  {
    package := RecurrenceZeroSetPackage.torsionClassDecomposition,
    code := "THM-M-0404-P04",
    role := "Partition characteristic roots by root-of-unity quotient classes and isolate residue classes.",
    currentStatus := "formalization_debt: torsion-coset partition not formalized here.",
    completionGate := "Pin/import/check roots-of-unity quotient machinery or implement the local branch split.",
    leafBudgetStatus := "unchecked; requires branch ledger."
  },
  {
    package := RecurrenceZeroSetPackage.nondegenerateZeroFiniteness,
    code := "THM-M-0404-P05",
    role := "Prove finiteness of zeros on each nondegenerate exponential-polynomial branch.",
    currentStatus := "formalization_debt: expected deep input is not present as a repo-local Lean theorem.",
    completionGate := "Integrate the required S-unit/Subspace-style theorem or record a concrete blocker.",
    leafBudgetStatus := "unchecked; deep theorem package exceeds one leaf."
  },
  {
    package := RecurrenceZeroSetPackage.degeneratePeriodExtraction,
    code := "THM-M-0404-P06",
    role := "Convert torsion degeneracies into arithmetic progressions of zero indices.",
    currentStatus := "formalization_debt: no checked period-extraction proof body.",
    completionGate := "Discharge residue-class recurrence branch and progression construction.",
    leafBudgetStatus := "unchecked; split by torsion class and residue."
  },
  {
    package := RecurrenceZeroSetPackage.pAdicAnalyticInterpolation,
    code := "THM-M-0404-P06",
    role := "Audit and later build the p-adic analytic interpolation branch, including the zero theorem used in place of or as Strassmann.",
    currentStatus := "partial_checked_support: P06 audit records checked anchors for `ℚ_[p]`, p-adic norm/valuation facts, Mahler-basis interpolation substrate, nonarchimedean local fields, and generic analytic isolated zeros; no Strassmann theorem was found in pinned mathlib.",
    completionGate := "Formalize Strassmann locally, locate a differently named checked equivalent, or integrate a pinned external proof; then connect recurrence subsequences to analytic functions on the selected p-adic domain.",
    leafBudgetStatus := "anchor audit checked; interpolation, convergence, and zero-count leaves remain unchecked and must be split into <=100-step leaves."
  },
  {
    package := RecurrenceZeroSetPackage.finiteExceptionalSetAccounting,
    code := "THM-M-0404-P07",
    role := "Collect the finitely many exceptional indices outside the periodic tail.",
    currentStatus := "partial_checked_support: list-based finite-union target and empty/list smoke tests are local.",
    completionGate := "Connect branch-wise finite sets to the canonical list representation.",
    leafBudgetStatus := "partially checked support; terminal accounting still unchecked."
  },
  {
    package := RecurrenceZeroSetPackage.finiteUnionEventualPeriodBridge,
    code := "THM-M-0404-P03",
    role := "Bridge the finite-union-of-progressions and eventual-periodic statement variants.",
    currentStatus := "recorded_statement_surface: NatSubsetEventualPeriodicFiniteUnionAPBridge names the exact predicate-level equivalence; statement-shape equivalence is locally checked conditional on that bridge.",
    completionGate := "Replace the recorded bridge target with a local proof body or a pinned checked upstream theorem for predicates on Nat.",
    leafBudgetStatus := "unchecked; the two directions must still be split into <=100-step local leaves."
  },
  {
    package := RecurrenceZeroSetPackage.externalClosureGate,
    code := "THM-M-0404-P07/P08/P09",
    role := "Authenticate any external Lean proof and bring it into the repo-local validation closure.",
    currentStatus := "negative_external_search_with_blocker: P07 exact public-code and repository searches found no Lean 4 SML proof candidate; authenticated GitHub code search is blocked by missing local GitHub authentication. P08 has no candidate available for pin/import/check.",
    completionGate := "Configure authenticated GitHub code search; if a candidate appears, record repository URL, commit, module path, theorem name, build status, and then pin/import/check or record a concrete P08 blocker.",
    leafBudgetStatus := "gate leaf; open until authenticated search and any candidate integration are closed."
  }
]

/-- The statement shape unfolds to the explicit field/recurrence formulation. -/
theorem statementShape_iff :
    StatementShape.{u} ↔
      ∀ (K : Type u) [Field K] [CharZero K]
        (E : LinearRecurrence K) (u : Nat → K),
          E.IsSolution u →
            IsFiniteUnionOfArithmeticProgressions (fun n : Nat => u n = 0) :=
  Iff.rfl

/-- The P01 wrapper unfolds to the explicit recurrence/zero-set statement. -/
theorem linearRecurrenceStatementOnlyWrapper_iff :
    LinearRecurrenceStatementOnlyWrapper.{u} ↔
      ∀ (K : Type u) [Field K] [CharZero K]
        (E : LinearRecurrence K) (u : Nat → K),
          E.IsSolution u →
            IsFiniteUnionOfArithmeticProgressions (fun n : Nat => u n = 0) :=
  Iff.rfl

/-- The eventual-periodic companion shape unfolds to its explicit formulation. -/
theorem statementShapeEventuallyPeriodic_iff :
    StatementShapeEventuallyPeriodic.{u} ↔
      ∀ (K : Type u) [Field K] [CharZero K]
        (E : LinearRecurrence K) (u : Nat → K),
          E.IsSolution u →
            IsEventuallyPeriodic (fun n : Nat => u n = 0) :=
  Iff.rfl

/-- The P03 predicate-level bridge target unfolds to the two normalized forms. -/
theorem eventualPeriodicFiniteUnionAPEquivalence_iff (S : Nat → Prop) :
    EventualPeriodicFiniteUnionAPEquivalence S ↔
      (IsEventuallyPeriodic S ↔ IsFiniteUnionOfArithmeticProgressions S) :=
  Iff.rfl

/-- The all-subsets P03 bridge target unfolds to the predicate-level bridge. -/
theorem natSubsetEventualPeriodicFiniteUnionAPBridge_iff :
    NatSubsetEventualPeriodicFiniteUnionAPBridge ↔
      ∀ S : Nat → Prop, IsEventuallyPeriodic S ↔ IsFiniteUnionOfArithmeticProgressions S :=
  Iff.rfl

/--
Checked conditional assembly for P03.

Once the predicate-level eventual-periodic/finite-union bridge is supplied, the
two Skolem-Mahler-Lech statement-normalization surfaces are equivalent.  This
does not prove Skolem-Mahler-Lech; it only verifies the local assembly boundary.
-/
theorem statementShape_iff_statementShapeEventuallyPeriodic_of_natSubsetBridge
    (hbridge : NatSubsetEventualPeriodicFiniteUnionAPBridge) :
    StatementShape.{u} ↔ StatementShapeEventuallyPeriodic.{u} := by
  constructor
  · intro h K _field _charZero E u hu
    exact ((hbridge (fun n : Nat => u n = 0)).2 (h K E u hu))
  · intro h K _field _charZero E u hu
    exact ((hbridge (fun n : Nat => u n = 0)).1 (h K E u hu))

/-- Membership in the zero-set predicate unfolds to the sequence value. -/
theorem zeroSetPredicate_iff {K : Type u} [Zero K] (u : Nat → K) (n : Nat) :
    zeroSetPredicate u n ↔ u n = 0 :=
  Iff.rfl

/-- The empty predicate is represented by empty exception and progression lists. -/
theorem empty_isFiniteUnionOfArithmeticProgressions :
    IsFiniteUnionOfArithmeticProgressions (fun _n : Nat => False) := by
  refine ⟨[], [], ?_⟩
  intro n
  simp [CoveredByProgressions]

/-- Any predicate represented exactly by list membership is a finite-union target. -/
theorem listMembership_isFiniteUnionOfArithmeticProgressions
    (exceptions : List Nat) :
    IsFiniteUnionOfArithmeticProgressions (fun n : Nat => n ∈ exceptions) := by
  refine ⟨exceptions, [], ?_⟩
  intro n
  simp [CoveredByProgressions]

/-- The empty predicate is eventually periodic, with period `1`. -/
theorem empty_isEventuallyPeriodic :
    IsEventuallyPeriodic (fun _n : Nat => False) := by
  refine ⟨0, 1, by decide, ?_⟩
  intro n _hn
  simp

/-- A geometric sequence is a solution exactly when its ratio is a characteristic root. -/
theorem geometric_solution_iff_root_charPoly {K : Type u} [CommRing K]
    (E : LinearRecurrence K) (q : K) :
    (E.IsSolution fun n => q ^ n) ↔ E.charPoly.IsRoot q :=
  E.geom_sol_iff_root_charPoly q

/-! ## P05 spectral/Jordan decomposition API audit wrappers. -/

/--
Finite-exponent generalized eigenspaces are kernels of powers of
`f - mu • 1`.

This is the kernel-filtration anchor needed before a Jordan-block or nilpotent
part argument can produce polynomial factors.
-/
theorem genEigenspace_nat_kernel {K V : Type u} [CommRing K] [AddCommGroup V]
    [Module K V] (f : Module.End K V) (mu : K) (k : Nat) :
    f.genEigenspace mu (k : ℕ∞) = LinearMap.ker ((f - mu • 1) ^ k) :=
  Module.End.genEigenspace_nat

/--
Iterates of a true eigenvector give the geometric part of an exponential
closed form.
-/
theorem hasUnifEigenvector_pow_apply {K V : Type u} [CommRing K] [AddCommGroup V]
    [Module K V] {f : Module.End K V} {mu : K} {v : V}
    (hv : f.HasUnifEigenvector mu 1 v) (n : Nat) :
    (f ^ n) v = mu ^ n • v :=
  hv.pow_apply n

/--
Over an algebraically closed field, finite-dimensional endomorphisms are
spanned by their maximal generalized eigenspaces.

This is an anchor for the future reduction from companion-state orbits to
generalized-eigenspace components.
-/
theorem algClosed_iSup_maxGenEigenspace_eq_top {K V : Type u} [Field K]
    [AddCommGroup V] [Module K V] [IsAlgClosed K] [FiniteDimensional K V]
    (f : Module.End K V) :
    ⨆ mu : K, f.maxGenEigenspace mu = ⊤ :=
  Module.End.iSup_maxGenEigenspace_eq_top f

/--
Jordan-Chevalley decomposition anchor for finite-dimensional endomorphisms over
a perfect field.

This supplies nilpotent and semisimple summands polynomial in the original
operator, but it does not by itself provide the recurrence closed-form
expansion required by Skolem-Mahler-Lech.
-/
theorem exists_isNilpotent_isSemisimple_anchor {K V : Type u} [Field K]
    [AddCommGroup V] [Module K V] [FiniteDimensional K V] [PerfectField K]
    (f : Module.End K V) :
    ∃ᵉ (n ∈ Algebra.adjoin K ({f} : Set (Module.End K V)))
        (s ∈ Algebra.adjoin K ({f} : Set (Module.End K V))),
      IsNilpotent n ∧ s.IsSemisimple ∧ f = n + s :=
  Module.End.exists_isNilpotent_isSemisimple (f := f)

/-! ## P06 p-adic and local-field analytic API audit wrappers. -/

/-- `ℚ_[p]` is complete in the pinned mathlib p-adic-number API. -/
theorem padic_completeSpace_anchor (p : Nat) [Fact p.Prime] : CompleteSpace ℚ_[p] := by
  infer_instance

/-- `ℚ_[p]` satisfies the nonarchimedean norm inequality. -/
theorem padic_nonarchimedean_anchor (p : Nat) [Fact p.Prime] (x y : ℚ_[p]) :
    ‖x + y‖ ≤ max ‖x‖ ‖y‖ :=
  Padic.nonarchimedean x y

/-- The p-adic norm of the uniformizer `p` is strictly less than one. -/
theorem padic_norm_p_lt_one_anchor (p : Nat) [Fact p.Prime] :
    ‖(p : ℚ_[p])‖ < 1 :=
  Padic.norm_p_lt_one

/-- Rational points are dense in `ℚ_[p]`. -/
theorem padic_rat_dense_anchor (p : Nat) [Fact p.Prime] (q : ℚ_[p])
    {ε : ℝ} (hε : 0 < ε) : ∃ r : ℚ, ‖q - r‖ < ε :=
  Padic.rat_dense p q hε

/-- A nonarchimedean local field has value group canonically isomorphic to `ℤᵐ⁰`. -/
theorem localField_valueGroupWithZero_iso_int_anchor
    (K : Type u) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] :
    Nonempty (ValueGroupWithZero K ≃*o ℤᵐ⁰) := by
  exact ⟨IsNonarchimedeanLocalField.valueGroupWithZeroIsoInt K⟩

/-- A nonarchimedean local field has finite residue field in the pinned API. -/
theorem localField_residueField_finite_anchor
    (K : Type u) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] :
    Finite 𝓀[K] := by
  infer_instance

/-- Generic analytic isolated-zero principle available in mathlib. -/
theorem analyticAt_eventually_eq_zero_or_eventually_ne_zero_anchor
    {𝕜 : Type u} [NontriviallyNormedField 𝕜]
    {E : Type u} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {f : 𝕜 → E} {z₀ : 𝕜} (hf : AnalyticAt 𝕜 f z₀) :
    (∀ᶠ z in 𝓝 z₀, f z = 0) ∨ ∀ᶠ z in 𝓝[≠] z₀, f z ≠ 0 :=
  hf.eventually_eq_zero_or_eventually_ne_zero

/-! ## P04 companion-operator reduction package. -/

/--
The length-`E.order` window of a sequence beginning at index `n`.

This is the state vector used by the companion-operator reduction.  It records
`u n, u (n+1), ..., u (n+E.order-1)` as a function on `Fin E.order`.
-/
def solutionWindow {R : Type u} [CommSemiring R]
    (E : LinearRecurrence R) (u : Nat → R) (n : Nat) : Fin E.order → R :=
  fun i : Fin E.order => u (n + i)

/--
The `n`th state obtained by iterating mathlib's companion-style operator
`LinearRecurrence.tupleSucc` from an initial tuple.
-/
def companionState {R : Type u} [CommSemiring R]
    (E : LinearRecurrence R) (init : Fin E.order → R) (n : Nat) :
    Fin E.order → R :=
  (E.tupleSucc^[n]) init

/-- At time zero, the companion state is the initial tuple. -/
theorem companionState_zero {R : Type u} [CommSemiring R]
    (E : LinearRecurrence R) (init : Fin E.order → R) :
    companionState E init 0 = init :=
  rfl

/-- Advancing one state applies `LinearRecurrence.tupleSucc`. -/
theorem companionState_succ {R : Type u} [CommSemiring R]
    (E : LinearRecurrence R) (init : Fin E.order → R) (n : Nat) :
    companionState E init (n + 1) = E.tupleSucc (companionState E init n) := by
  simp [companionState, Function.iterate_succ_apply']

/--
The companion operator sends the window beginning at `n` to the window beginning
at `n+1` for every solution of the recurrence.

This is the checked core of the P04 reduction from recurrence sequences to
iterates of `LinearRecurrence.tupleSucc`.
-/
theorem tupleSucc_solutionWindow {R : Type u} [CommSemiring R]
    (E : LinearRecurrence R) (u : Nat → R) (hu : E.IsSolution u) (n : Nat) :
    E.tupleSucc (solutionWindow E u n) = solutionWindow E u (n + 1) := by
  ext i
  dsimp [solutionWindow, LinearRecurrence.tupleSucc]
  by_cases h : (i : Nat) + 1 < E.order
  · simp [h, Nat.add_comm, Nat.add_left_comm]
  · have hi : (i : Nat) + 1 = E.order := by
      exact le_antisymm (Nat.succ_le_of_lt i.2) (le_of_not_gt h)
    simp [h]
    rw [← hu n]
    congr 1
    omega

/--
Iterating `tupleSucc` from the initial solution window gives the solution window
at time `n`.
-/
theorem companionState_solutionWindow {R : Type u} [CommSemiring R]
    (E : LinearRecurrence R) (u : Nat → R) (hu : E.IsSolution u) (n : Nat) :
    companionState E (solutionWindow E u 0) n = solutionWindow E u n := by
  induction n with
  | zero =>
      ext i
      simp [companionState, solutionWindow]
  | succ n ih =>
      rw [companionState_succ, ih, tupleSucc_solutionWindow E u hu n]

/--
For positive order, the first coordinate of the iterated companion state is the
original sequence value.
-/
theorem companionState_first_eq_solution {R : Type u} [CommSemiring R]
    (E : LinearRecurrence R) (u : Nat → R) (hu : E.IsSolution u)
    (horder : 0 < E.order) (n : Nat) :
    companionState E (solutionWindow E u 0) n ⟨0, horder⟩ = u n := by
  rw [companionState_solutionWindow E u hu n]
  simp [solutionWindow]

/--
For positive order, the zero set of a recurrence solution is the zero set of the
first coordinate of the companion-operator orbit.
-/
theorem zeroSet_iff_companionState_first {R : Type u} [CommSemiring R]
    (E : LinearRecurrence R) (u : Nat → R) (hu : E.IsSolution u)
    (horder : 0 < E.order) (n : Nat) :
    u n = 0 ↔ companionState E (solutionWindow E u 0) n ⟨0, horder⟩ = 0 := by
  rw [companionState_first_eq_solution E u hu horder n]

/--
Zero-order recurrences force every solution value to be zero, so the
companion-window reduction only needs a first-coordinate bridge in the positive
order case.
-/
theorem solution_eq_zero_of_order_eq_zero {R : Type u} [CommSemiring R]
    (E : LinearRecurrence R) (u : Nat → R) (hu : E.IsSolution u)
    (horder : E.order = 0) (n : Nat) : u n = 0 := by
  cases E with
  | mk order coeffs =>
      dsimp at horder hu
      subst order
      simpa [LinearRecurrence.IsSolution] using hu n

/--
Checked local projection wrapper: a future proof of `StatementShape` supplies the
finite-union zero-set conclusion for any fixed recurrence solution.
-/
theorem zeroSet_finiteUnion_of_statementShape
    (h : StatementShape.{u})
    (K : Type u) [Field K] [CharZero K]
    (E : LinearRecurrence K) (u : Nat → K)
    (hu : E.IsSolution u) :
    IsFiniteUnionOfArithmeticProgressions (fun n : Nat => u n = 0) :=
  h K E u hu

/--
Checked local projection wrapper: a future proof of
`StatementShapeEventuallyPeriodic` supplies the eventual-periodic zero-set
conclusion for any fixed recurrence solution.
-/
theorem zeroSet_eventuallyPeriodic_of_statementShapeEventuallyPeriodic
    (h : StatementShapeEventuallyPeriodic.{u})
    (K : Type u) [Field K] [CharZero K]
    (E : LinearRecurrence K) (u : Nat → K)
    (hu : E.IsSolution u) :
    IsEventuallyPeriodic (fun n : Nat => u n = 0) :=
  h K E u hu

/-- Mathlib modules audited as repo-local object-model anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Algebra.LinearRecurrence",
  "Mathlib.Algebra.CharZero.Defs",
  "Mathlib.Analysis.Analytic.IsolatedZeros",
  "Mathlib.Algebra.Field.Defs",
  "Mathlib.Algebra.Polynomial.Degree.Operations",
  "Mathlib.LinearAlgebra.Dimension.Constructions",
  "Mathlib.LinearAlgebra.Eigenspace.Basic",
  "Mathlib.LinearAlgebra.Eigenspace.Triangularizable",
  "Mathlib.LinearAlgebra.JordanChevalley",
  "Mathlib.NumberTheory.LocalField.Basic",
  "Mathlib.NumberTheory.Padics.MahlerBasis",
  "Mathlib.NumberTheory.Padics.PadicNumbers"
]

/--
Local declaration names that this Stage1 module contributes to the repository's
checked Lean surface.
-/
def checkedDeclarationNames : List String := [
  "AwesomeTheorems.Stage1.S1_M_017.NatArithmeticProgression",
  "AwesomeTheorems.Stage1.S1_M_017.CoveredByProgressions",
  "AwesomeTheorems.Stage1.S1_M_017.zeroSetPredicate",
  "AwesomeTheorems.Stage1.S1_M_017.IsFiniteUnionOfArithmeticProgressions",
  "AwesomeTheorems.Stage1.S1_M_017.IsEventuallyPeriodic",
  "AwesomeTheorems.Stage1.S1_M_017.EventualPeriodicFiniteUnionAPEquivalence",
  "AwesomeTheorems.Stage1.S1_M_017.NatSubsetEventualPeriodicFiniteUnionAPBridge",
  "AwesomeTheorems.Stage1.S1_M_017.statementNormalizationNote",
  "AwesomeTheorems.Stage1.S1_M_017.StatementShape",
  "AwesomeTheorems.Stage1.S1_M_017.LinearRecurrenceStatementOnlyWrapper",
  "AwesomeTheorems.Stage1.S1_M_017.StatementShapeEventuallyPeriodic",
  "AwesomeTheorems.Stage1.S1_M_017.RecurrenceZeroSetPackage",
  "AwesomeTheorems.Stage1.S1_M_017.ProofPackageAudit",
  "AwesomeTheorems.Stage1.S1_M_017.mathlibLinearRecurrenceRevision",
  "AwesomeTheorems.Stage1.S1_M_017.mathlibLinearRecurrenceSourceUrl",
  "AwesomeTheorems.Stage1.S1_M_017.mathlibEigenspaceBasicSourceUrl",
  "AwesomeTheorems.Stage1.S1_M_017.mathlibEigenspaceTriangularizableSourceUrl",
  "AwesomeTheorems.Stage1.S1_M_017.mathlibJordanChevalleySourceUrl",
  "AwesomeTheorems.Stage1.S1_M_017.mathlibPadicNumbersSourceUrl",
  "AwesomeTheorems.Stage1.S1_M_017.mathlibPadicMahlerBasisSourceUrl",
  "AwesomeTheorems.Stage1.S1_M_017.mathlibLocalFieldBasicSourceUrl",
  "AwesomeTheorems.Stage1.S1_M_017.mathlibAnalyticIsolatedZerosSourceUrl",
  "AwesomeTheorems.Stage1.S1_M_017.LinearRecurrenceAnchorKind",
  "AwesomeTheorems.Stage1.S1_M_017.SpectralJordanAnchorKind",
  "AwesomeTheorems.Stage1.S1_M_017.PadicLocalAnalyticAnchorKind",
  "AwesomeTheorems.Stage1.S1_M_017.ExternalLeanSearchAnchorKind",
  "AwesomeTheorems.Stage1.S1_M_017.ExternalProofIntegrationKind",
  "AwesomeTheorems.Stage1.S1_M_017.PublicLeafLedgerGateKind",
  "AwesomeTheorems.Stage1.S1_M_017.MathlibLinearRecurrenceAnchorAudit",
  "AwesomeTheorems.Stage1.S1_M_017.SpectralJordanAnchorAudit",
  "AwesomeTheorems.Stage1.S1_M_017.PadicLocalAnalyticAnchorAudit",
  "AwesomeTheorems.Stage1.S1_M_017.ExternalLeanSearchAudit",
  "AwesomeTheorems.Stage1.S1_M_017.ExternalProofIntegrationAudit",
  "AwesomeTheorems.Stage1.S1_M_017.PublicLeafLedgerGateAudit",
  "AwesomeTheorems.Stage1.S1_M_017.mathlibLinearRecurrenceAnchorAuditTable",
  "AwesomeTheorems.Stage1.S1_M_017.spectralJordanAnchorAuditTable",
  "AwesomeTheorems.Stage1.S1_M_017.padicLocalAnalyticAnchorAuditTable",
  "AwesomeTheorems.Stage1.S1_M_017.externalLeanSearchAuditDate",
  "AwesomeTheorems.Stage1.S1_M_017.externalLeanSearchAuditTable",
  "AwesomeTheorems.Stage1.S1_M_017.externalProofIntegrationAuditDate",
  "AwesomeTheorems.Stage1.S1_M_017.externalProofIntegrationAuditTable",
  "AwesomeTheorems.Stage1.S1_M_017.publicLeafLedgerGateAuditDate",
  "AwesomeTheorems.Stage1.S1_M_017.publicLeafLedgerGateAuditTable",
  "AwesomeTheorems.Stage1.S1_M_017.recurrenceZeroSetProofPackages",
  "AwesomeTheorems.Stage1.S1_M_017.statementShape_iff",
  "AwesomeTheorems.Stage1.S1_M_017.linearRecurrenceStatementOnlyWrapper_iff",
  "AwesomeTheorems.Stage1.S1_M_017.statementShapeEventuallyPeriodic_iff",
  "AwesomeTheorems.Stage1.S1_M_017.eventualPeriodicFiniteUnionAPEquivalence_iff",
  "AwesomeTheorems.Stage1.S1_M_017.natSubsetEventualPeriodicFiniteUnionAPBridge_iff",
  "AwesomeTheorems.Stage1.S1_M_017.statementShape_iff_statementShapeEventuallyPeriodic_of_natSubsetBridge",
  "AwesomeTheorems.Stage1.S1_M_017.zeroSetPredicate_iff",
  "AwesomeTheorems.Stage1.S1_M_017.empty_isFiniteUnionOfArithmeticProgressions",
  "AwesomeTheorems.Stage1.S1_M_017.listMembership_isFiniteUnionOfArithmeticProgressions",
  "AwesomeTheorems.Stage1.S1_M_017.empty_isEventuallyPeriodic",
  "AwesomeTheorems.Stage1.S1_M_017.geometric_solution_iff_root_charPoly",
  "AwesomeTheorems.Stage1.S1_M_017.genEigenspace_nat_kernel",
  "AwesomeTheorems.Stage1.S1_M_017.hasUnifEigenvector_pow_apply",
  "AwesomeTheorems.Stage1.S1_M_017.algClosed_iSup_maxGenEigenspace_eq_top",
  "AwesomeTheorems.Stage1.S1_M_017.exists_isNilpotent_isSemisimple_anchor",
  "AwesomeTheorems.Stage1.S1_M_017.padic_completeSpace_anchor",
  "AwesomeTheorems.Stage1.S1_M_017.padic_nonarchimedean_anchor",
  "AwesomeTheorems.Stage1.S1_M_017.padic_norm_p_lt_one_anchor",
  "AwesomeTheorems.Stage1.S1_M_017.padic_rat_dense_anchor",
  "AwesomeTheorems.Stage1.S1_M_017.localField_valueGroupWithZero_iso_int_anchor",
  "AwesomeTheorems.Stage1.S1_M_017.localField_residueField_finite_anchor",
  "AwesomeTheorems.Stage1.S1_M_017.analyticAt_eventually_eq_zero_or_eventually_ne_zero_anchor",
  "AwesomeTheorems.Stage1.S1_M_017.solutionWindow",
  "AwesomeTheorems.Stage1.S1_M_017.companionState",
  "AwesomeTheorems.Stage1.S1_M_017.companionState_zero",
  "AwesomeTheorems.Stage1.S1_M_017.companionState_succ",
  "AwesomeTheorems.Stage1.S1_M_017.tupleSucc_solutionWindow",
  "AwesomeTheorems.Stage1.S1_M_017.companionState_solutionWindow",
  "AwesomeTheorems.Stage1.S1_M_017.companionState_first_eq_solution",
  "AwesomeTheorems.Stage1.S1_M_017.zeroSet_iff_companionState_first",
  "AwesomeTheorems.Stage1.S1_M_017.solution_eq_zero_of_order_eq_zero",
  "AwesomeTheorems.Stage1.S1_M_017.zeroSet_finiteUnion_of_statementShape",
  "AwesomeTheorems.Stage1.S1_M_017.zeroSet_eventuallyPeriodic_of_statementShapeEventuallyPeriodic"
]

/--
Machine-proof debt classification for this Stage1 slot.

The theorem is mathematically known, but no full repo-local Lean proof body or
pinned external Lean dependency has been integrated by this repair pass.
-/
def machineProofDebt : String := "formalization_debt"

/--
Repo-local integration-debt gate.

This remains `False` in the Lean artifact because no external Lean 4 proof of
Skolem-Mahler-Lech has been pinned, imported, and checked in this repository.
The module is therefore not marked completed.
-/
def repoLocalIntegrationDebtClosed : Prop := False

/-! ## Audit probes retained in the checked file. -/

#check LinearRecurrence
#check LinearRecurrence.order
#check LinearRecurrence.coeffs
#check LinearRecurrence.IsSolution
#check LinearRecurrence.mkSol
#check LinearRecurrence.is_sol_mkSol
#check LinearRecurrence.mkSol_eq_init
#check LinearRecurrence.eq_mk_of_is_sol_of_eq_init
#check LinearRecurrence.eq_mk_of_is_sol_of_eq_init'
#check LinearRecurrence.solSpace
#check LinearRecurrence.is_sol_iff_mem_solSpace
#check LinearRecurrence.toInit
#check LinearRecurrence.sol_eq_of_eq_init
#check LinearRecurrence.tupleSucc
#check LinearRecurrence.solSpace_rank
#check LinearRecurrence.charPoly
#check LinearRecurrence.charPoly_degree_eq_order
#check LinearRecurrence.charPoly_monic
#check LinearRecurrence.geom_sol_iff_root_charPoly
#check Module.End.genEigenspace
#check Module.End.mem_genEigenspace_nat
#check Module.End.genEigenspace_nat
#check Module.End.HasUnifEigenvector.pow_apply
#check Module.End.iSup_maxGenEigenspace_eq_top
#check Module.End.exists_isNilpotent_isSemisimple
#check Module.End.isNilpotent_isSemisimple_unique
#check zeroSetPredicate
#check IsEventuallyPeriodic
#check EventualPeriodicFiniteUnionAPEquivalence
#check NatSubsetEventualPeriodicFiniteUnionAPBridge
#check StatementShape
#check LinearRecurrenceStatementOnlyWrapper
#check StatementShapeEventuallyPeriodic
#check RecurrenceZeroSetPackage
#check ProofPackageAudit
#check mathlibLinearRecurrenceRevision
#check mathlibLinearRecurrenceSourceUrl
#check mathlibEigenspaceBasicSourceUrl
#check mathlibEigenspaceTriangularizableSourceUrl
#check mathlibJordanChevalleySourceUrl
#check mathlibPadicNumbersSourceUrl
#check mathlibPadicMahlerBasisSourceUrl
#check mathlibLocalFieldBasicSourceUrl
#check mathlibAnalyticIsolatedZerosSourceUrl
#check LinearRecurrenceAnchorKind
#check SpectralJordanAnchorKind
#check PadicLocalAnalyticAnchorKind
#check ExternalLeanSearchAnchorKind
#check ExternalProofIntegrationKind
#check PublicLeafLedgerGateKind
#check MathlibLinearRecurrenceAnchorAudit
#check SpectralJordanAnchorAudit
#check PadicLocalAnalyticAnchorAudit
#check ExternalLeanSearchAudit
#check ExternalProofIntegrationAudit
#check PublicLeafLedgerGateAudit
#check mathlibLinearRecurrenceAnchorAuditTable
#check spectralJordanAnchorAuditTable
#check padicLocalAnalyticAnchorAuditTable
#check externalLeanSearchAuditDate
#check externalLeanSearchAuditTable
#check externalProofIntegrationAuditDate
#check externalProofIntegrationAuditTable
#check publicLeafLedgerGateAuditDate
#check publicLeafLedgerGateAuditTable
#check recurrenceZeroSetProofPackages
#check zeroSetPredicate_iff
#check linearRecurrenceStatementOnlyWrapper_iff
#check eventualPeriodicFiniteUnionAPEquivalence_iff
#check natSubsetEventualPeriodicFiniteUnionAPBridge_iff
#check statementShape_iff_statementShapeEventuallyPeriodic_of_natSubsetBridge
#check empty_isFiniteUnionOfArithmeticProgressions
#check listMembership_isFiniteUnionOfArithmeticProgressions
#check empty_isEventuallyPeriodic
#check geometric_solution_iff_root_charPoly
#check genEigenspace_nat_kernel
#check hasUnifEigenvector_pow_apply
#check algClosed_iSup_maxGenEigenspace_eq_top
#check exists_isNilpotent_isSemisimple_anchor
#check Padic
#check Padic.norm_p
#check Padic.norm_p_lt_one
#check Padic.nonarchimedean
#check Padic.rat_dense
#check PadicInt.continuous_choose
#check PadicInt.hasSum_mahler
#check PadicInt.mahlerEquiv_apply
#check IsNonarchimedeanLocalField
#check IsNonarchimedeanLocalField.valueGroupWithZeroIsoInt
#check AnalyticAt.eventually_eq_zero_or_eventually_ne_zero
#check HasFPowerSeriesAt.locally_ne_zero
#check padic_completeSpace_anchor
#check padic_nonarchimedean_anchor
#check padic_norm_p_lt_one_anchor
#check padic_rat_dense_anchor
#check localField_valueGroupWithZero_iso_int_anchor
#check localField_residueField_finite_anchor
#check analyticAt_eventually_eq_zero_or_eventually_ne_zero_anchor
#check solutionWindow
#check companionState
#check companionState_zero
#check companionState_succ
#check tupleSucc_solutionWindow
#check companionState_solutionWindow
#check companionState_first_eq_solution
#check zeroSet_iff_companionState_first
#check solution_eq_zero_of_order_eq_zero
#check zeroSet_finiteUnion_of_statementShape
#check zeroSet_eventuallyPeriodic_of_statementShapeEventuallyPeriodic

end S1_M_017
end Stage1
end AwesomeTheorems
