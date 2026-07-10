import Mathlib.NumberTheory.DiophantineApproximation.ContinuedFractions
import Mathlib.FieldTheory.AlgebraicClosure
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.NumberTheory.Transcendental.Liouville.LiouvilleWith
import Mathlib.NumberTheory.Height.Basic
import Mathlib.NumberTheory.Height.NumberField
import Mathlib.Combinatorics.Additive.Corner.Roth

/-!
# S1-M-012 / THM-M-0399: Roth's theorem

This Stage1 repair artifact records a conservative Lean 4 boundary for Roth's
theorem on rational approximation to algebraic irrational real numbers.

The pinned mathlib snapshot has foundational Diophantine-approximation results:
Dirichlet's theorem, infinitude of irrational approximants at exponent `2`,
finiteness for rational targets at exponent `2`, and Legendre's continued
fraction criterion.  It does not expose a terminal Roth theorem for algebraic
irrational real numbers and exponent `2 + ε`.

The terminal theorem is therefore represented only as a precise `Prop`
statement-shape.  Candidate A is the canonical Stage1 target: a direct
finite-rational-approximants statement with algebraic irrational real target,
arbitrary exponent `p > 2`, arbitrary positive constant `C`, and reduced
denominator `Rat.den`.  Lean uses `Real.rpow` for the real exponent.

The checked declarations below are wrappers around existing mathlib anchors,
an explicit anchor-audit table, and a proof-package split.  They contain no
proof placeholders or new kernel assumptions.
-/

noncomputable section

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_012

open Set

/-- Algebraic irrational real target in the usual Roth theorem over `ℚ`. -/
def AlgebraicIrrationalReal (ξ : ℝ) : Prop :=
  IsAlgebraic ℚ ξ ∧ Irrational ξ

/--
The rational approximants that would violate Roth's exponent `2 + ε`
finiteness conclusion for a fixed real target `ξ`.
-/
def RothApproximationSetEpsilon (ξ ε : ℝ) : Set ℚ :=
  {q : ℚ | |ξ - (q : ℝ)| < 1 / Real.rpow (q.den : ℝ) (2 + ε)}

/--
Candidate A approximation set for the canonical Stage1 target.

This is the direct finite-rational-approximants surface selected by the public
backfill task.  It avoids choosing integer representatives for `q` and follows
mathlib's denominator convention via `Rat.den`.
-/
def RothApproximationSetA (ξ p C : ℝ) : Set ℚ :=
  {q : ℚ | |ξ - (q : ℝ)| < C / Real.rpow (q.den : ℝ) p}

/--
Candidate A, the canonical Stage1 Lean 4 target for Roth's theorem.

For every algebraic irrational real `ξ`, every exponent `p > 2`, and every
positive real constant `C`, only finitely many rationals `q` approximate `ξ`
within `C / q.den ^ p`, encoded with `Real.rpow` for the real exponent.
-/
def RothStatementShapeA : Prop :=
  ∀ ξ : ℝ,
    AlgebraicIrrationalReal ξ →
      ∀ p : ℝ,
        2 < p →
          ∀ C : ℝ,
            0 < C →
              (RothApproximationSetA ξ p C).Finite

/--
The older `ε`-increment, constant-`1` spelling kept as a bridge target.

For every algebraic irrational real `ξ` and every positive real `ε`, only
finitely many rationals `q` approximate `ξ` within denominator exponent
`2 + ε`.
-/
def RothStatementShapeEpsilon : Prop :=
  ∀ ξ ε : ℝ,
    AlgebraicIrrationalReal ξ →
      0 < ε →
        (RothApproximationSetEpsilon ξ ε).Finite

/--
Candidate C, the `LiouvilleWith` corollary surface.

This is not the canonical public root for `THM-M-0399`.  It records the
standard irrationality-exponent corollary expected from Candidate A: an
algebraic irrational real is not `LiouvilleWith p` for any exponent `p > 2`.
-/
def RothStatementShapeC : Prop :=
  ∀ ξ : ℝ,
    AlgebraicIrrationalReal ξ →
      ∀ p : ℝ,
        2 < p →
          ¬ LiouvilleWith p ξ

/--
Normalized Stage1 statement-shape for Roth's theorem.

This is definitionally Candidate A.  The `ε`-increment spelling is retained as
`RothStatementShapeEpsilon` for later bridge lemmas, but it is not the
canonical public target for `THM-M-0399`.
-/
def StatementShape : Prop :=
  RothStatementShapeA

/-- Checked definitional witness that `StatementShape` is Candidate A. -/
theorem statementShape_is_candidateA : StatementShape = RothStatementShapeA :=
  rfl

/--
Checked bridge from Candidate A to the older `ε`-increment, constant-`1`
surface.

This is a genuine local proof about the parsed statement shapes.  It does not
prove Candidate A; it only records that the canonical finite-approximants target
specializes to the legacy epsilon spelling once Candidate A is supplied.
-/
theorem candidateA_implies_epsilon
    (hA : RothStatementShapeA) : RothStatementShapeEpsilon := by
  intro ξ ε hξ hε
  have hp : (2 : ℝ) < 2 + ε := by
    linarith
  simpa [RothApproximationSetA, RothApproximationSetEpsilon] using
    hA ξ hξ (2 + ε) hp 1 zero_lt_one

/--
Candidate A-to-C bridge obligation.

The proof of this proposition is the next nontrivial statement-bridge leaf: it
must extract a `LiouvilleWith` contradiction from finite rational
approximants.  It is a named obligation, not assumed evidence.
-/
def CandidateAToCBridge : Prop :=
  RothStatementShapeA → RothStatementShapeC

/--
Candidate C-to-A bridge obligation.

This reverse direction is not expected to be the primary public route, but it is
kept as a named target in case an upstream theorem is only exposed through
`LiouvilleWith` and a finite-approximant wrapper is later required.
-/
def CandidateCToABridge : Prop :=
  RothStatementShapeC → RothStatementShapeA

/-- Conditional assembly of Candidate C from Candidate A and the named bridge. -/
theorem candidateC_of_candidateA_of_bridge
    (hA : RothStatementShapeA) (hAC : CandidateAToCBridge) :
    RothStatementShapeC :=
  hAC hA

/--
Conditional assembly of the `LiouvilleWith` corollary from the canonical
`StatementShape` and the named Candidate A-to-C bridge.
-/
theorem candidateC_of_statementShape_of_bridge
    (hS : StatementShape) (hAC : CandidateAToCBridge) :
    RothStatementShapeC :=
  candidateC_of_candidateA_of_bridge (by simpa [StatementShape] using hS) hAC

/--
P0-P5 theorem-tree packages for a future Roth proof.

These constructors are planning nodes, not proof claims.  They keep the
statement/audit/proof-package split stable inside the checked Lean artifact so
the public blueprint can later be backfilled by a serial integrator.
-/
inductive RothProofPackage where
  | P0_statementNormalization
  | P1_mathlibObjectModel
  | P2_liouvilleBridge
  | P3_heightAndNumberFieldBridge
  | P4_coreRothLemmaFamily
  | P5_terminalWrapperOrDependencyGate
  deriving DecidableEq, Repr

/-- Canonical P0-P5 package order for the Roth theorem-tree split. -/
def rothProofPackageSplit : List RothProofPackage := [
  RothProofPackage.P0_statementNormalization,
  RothProofPackage.P1_mathlibObjectModel,
  RothProofPackage.P2_liouvilleBridge,
  RothProofPackage.P3_heightAndNumberFieldBridge,
  RothProofPackage.P4_coreRothLemmaFamily,
  RothProofPackage.P5_terminalWrapperOrDependencyGate
]

/-- Checked package count for the public P0-P5 split. -/
theorem rothProofPackageSplit_length :
    rothProofPackageSplit.length = 6 :=
  rfl

/-- A structured theorem-tree package row for the public P0-P5 split. -/
structure RothPackageRow where
  packageId : String
  packageName : String
  responsibility : String
  upstreamInput : String
  downstreamOutput : String
  status : String
  deriving Repr

/--
Integration-ready theorem-tree package split for THM-M-0399.

The rows are checked data, not proof claims.  They match the parent public
backfill packages P0 through P5 and preserve the M0387-level distinction
between checked statement/audit scaffolding and the missing terminal Roth proof.
-/
def rothTheoremTreePackageRows : List RothPackageRow := [
  {
    packageId := "M0399.P0",
    packageName := "statement_normalization",
    responsibility := "freeze Candidate A as the canonical Lean 4 target; keep epsilon, integer-pair, and LiouvilleWith spellings as bridge targets",
    upstreamInput := "human Roth statement for algebraic irrational real numbers and mathlib rational denominator conventions",
    downstreamOutput := "StatementShape definitionally equal to RothStatementShapeA, Candidate C parsed as the LiouvilleWith corollary surface, and bridge obligations named",
    status := "partially checked: Candidate A, Candidate C, StatementShape, and A-to-epsilon specialization parse locally; A-to-C proof remains unchecked"
  },
  {
    packageId := "M0399.P1",
    packageName := "mathlib_object_model",
    responsibility := "audit imports and object models for Rat.den, Set.Finite, filters, Irrational, IsAlgebraic, LiouvilleWith, heights, and the Roth name collision",
    upstreamInput := "pinned mathlib modules and local import/elaboration probes",
    downstreamOutput := "anchor table separating usable infrastructure from non-terminal and false-positive Roth evidence",
    status := "partially checked: infrastructure anchors elaborate locally; no terminal mathlib Roth theorem was found"
  },
  {
    packageId := "M0399.P2",
    packageName := "liouville_bridge",
    responsibility := "relate finite rational-approximant statements to non-LiouvilleWith exponent statements, including constants and denominator normalization",
    upstreamInput := "P0 statement shapes and P1 LiouvilleWith / rational-approximation APIs",
    downstreamOutput := "named CandidateAToCBridge / CandidateCToABridge obligations plus checked conditional assembly lemmas",
    status := "partially checked bridge surface: Candidate C and conditional assembly lemmas elaborate; the actual A-to-C and C-to-A proofs remain formalization debt"
  },
  {
    packageId := "M0399.P3",
    packageName := "height_and_number_field_bridge",
    responsibility := "move from a real algebraic target to number-field height and product-formula inequalities tied to rational denominators",
    upstreamInput := "P1 height and number-field APIs plus P2 denominator-normalized approximants",
    downstreamOutput := "height/product-formula estimates usable by the Roth auxiliary-polynomial contradiction",
    status := "unchecked formalization debt: no local Rat.den-to-height or product-formula bridge is proved"
  },
  {
    packageId := "M0399.P4",
    packageName := "core_roth_lemma_family",
    responsibility := "cover the auxiliary-polynomial, Siegel-lemma, multiplicity, zero-estimate, gap-principle, and upper/lower bound contradiction branch",
    upstreamInput := "P3 height/product-formula estimates and a chosen formal auxiliary-polynomial interface",
    downstreamOutput := "contradiction to infinitely many too-good approximants for exponent p > 2",
    status := "unchecked deep formalization debt: the core Roth lemma family is not available locally"
  },
  {
    packageId := "M0399.P5",
    packageName := "terminal_wrapper_or_dependency_gate",
    responsibility := "close the theorem only through a local proof body, checked mathlib wrapper, or pinned/imported external Lean proof; otherwise keep formalization debt",
    upstreamInput := "validated P0-P4 proof chain or a validated terminal upstream theorem",
    downstreamOutput := "repo-local proof/dependency closure plus public metadata/checklist synchronization",
    status := "open gate: no terminal proof body or pinned external dependency is checked in this repository"
  }
]

/-- Checked package-row count for the public theorem-tree split. -/
theorem rothTheoremTreePackageRows_length :
    rothTheoremTreePackageRows.length = 6 :=
  rfl

/-- Current status of each P0-P5 package under M0387-level accounting. -/
def rothProofPackageStatus : List String := [
  "P0 statement normalization: locally checked as RothStatementShapeA / StatementShape, with Candidate C parsed as the LiouvilleWith corollary surface",
  "P1 mathlib object model: checked anchors exist for exponent-2 Diophantine approximation, LiouvilleWith, Height, and a non-number-theoretic combinatorial Roth collision",
  "P2 liouville bridge: Candidate A-to-epsilon specialization and conditional A-to-C assembly are checked; the substantive A-to-C proof remains open",
  "P3 height and number-field bridge: package named; no local bridge from Rat.den to absolute/logarithmic height or product-formula estimates is proved here",
  "P4 core Roth lemma family: package named; no local auxiliary-polynomial, Siegel-lemma, zero-estimate, or gap-principle proof body is present",
  "P5 terminal wrapper or dependency gate: terminal theorem remains not_repo_local_closed until a local proof body or pinned/imported external proof validates StatementShape"
]

/-- mathlib modules audited for the Roth statement/audit split. -/
def mathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.DiophantineApproximation.Basic",
  "Mathlib.NumberTheory.DiophantineApproximation.ContinuedFractions",
  "Mathlib.NumberTheory.Transcendental.Liouville.LiouvilleWith",
  "Mathlib.NumberTheory.Height.Basic",
  "Mathlib.NumberTheory.Height.NumberField",
  "Mathlib.Combinatorics.Additive.Corner.Roth"
]

/-- A structured row for the public mathlib anchor table. -/
structure MathlibAnchorRow where
  moduleName : String
  anchorNames : String
  roleForRoth : String
  closureStatus : String
  deriving Repr

/--
Child C002 anchor table for the public THM-M-0399 backfill.

The table intentionally includes the combinatorial `Roth` module as a name
collision warning rather than as number-theoretic evidence.
-/
def mathlibAnchorTable : List MathlibAnchorRow := [
  {
    moduleName := "Mathlib.NumberTheory.DiophantineApproximation.Basic",
    anchorNames := "Real.infinite_rat_abs_sub_lt_one_div_den_sq_of_irrational; Rat.finite_rat_abs_sub_lt_one_div_den_sq",
    roleForRoth := "exponent-2 rational-approximation anchors for irrational and rational targets",
    closureStatus := "checked anchor only; not algebraic irrational Roth at exponent p > 2"
  },
  {
    moduleName := "Mathlib.NumberTheory.Transcendental.Liouville.LiouvilleWith",
    anchorNames := "LiouvilleWith; LiouvilleWith.exists_pos; LiouvilleWith.irrational",
    roleForRoth := "candidate bridge surface for irrationality-exponent formulations",
    closureStatus := "checked anchor only; no local theorem proves algebraic irrational reals are not LiouvilleWith p for p > 2"
  },
  {
    moduleName := "Mathlib.NumberTheory.Height.Basic",
    anchorNames := "Height.mulHeight₁; Height.logHeight₁",
    roleForRoth := "height object-model API needed before denominator-height bridge work",
    closureStatus := "checked anchor only; no local Rat.den-to-height bridge is proved here"
  },
  {
    moduleName := "Mathlib.NumberTheory.Height.NumberField",
    anchorNames := "Height.mulHeight; Height.logHeight",
    roleForRoth := "number-field height API relevant to algebraic target estimates",
    closureStatus := "checked anchor only; no local Roth height estimate is proved here"
  },
  {
    moduleName := "Mathlib.Combinatorics.Additive.Corner.Roth",
    anchorNames := "roth_3ap_theorem; roth_3ap_theorem_nat",
    roleForRoth := "irrelevant name collision for arithmetic-progression Roth theorem",
    closureStatus := "false-positive warning; not THM-M-0399 and not evidence for number-theoretic Roth"
  }
]

/-- Checked row count for the C002 public anchor table. -/
theorem mathlibAnchorTable_length :
    mathlibAnchorTable.length = 5 :=
  rfl

/--
Audit table for checked mathlib anchors.

The final row is intentionally a false-positive warning: mathlib's theorem
named `roth_3ap_theorem` proves Roth's theorem on three-term arithmetic
progression-free finite sets, not Roth's Diophantine approximation theorem.
-/
def mathlibAnchorAudit : List String := [
  "DiophantineApproximation.Basic: Real.infinite_rat_abs_sub_lt_one_div_den_sq_of_irrational; exponent-2 infinitude anchor, not terminal Roth",
  "DiophantineApproximation.Basic: Rat.finite_rat_abs_sub_lt_one_div_den_sq; rational-target exponent-2 finiteness anchor, not algebraic irrational Roth",
  "DiophantineApproximation.ContinuedFractions: Real.exists_convs_eq_rat; Legendre continued-fraction anchor",
  "Transcendental.Liouville.LiouvilleWith: LiouvilleWith and basic lemmas; useful bridge surface but no algebraic irrational Roth theorem",
  "Height.Basic / Height.NumberField: Height.mulHeight₁, Height.logHeight₁, Height.mulHeight, Height.logHeight object-model anchors; no denominator-height bridge proved here",
  "Combinatorics.Additive.Corner.Roth: roth_3ap_theorem and roth_3ap_theorem_nat are additive-combinatorics theorems, not THM-M-0399"
]

/--
Public caution for the Roth name collision in mathlib.

This is checked data for the later serial blueprint backfill.  It deliberately
does not use the combinatorial Roth module as evidence for the
number-theoretic Roth theorem.
-/
def publicCombinatorialRothCaution : List String := [
  "Public caution for THM-M-0399: Mathlib.Combinatorics.Additive.Corner.Roth is not the number-theoretic Roth theorem.",
  "That module proves additive-combinatorics results about three-term arithmetic progressions in finite sets, including roth_3ap_theorem and roth_3ap_theorem_nat.",
  "It should be recorded only as an irrelevant Roth-name collision / false-positive audit row, not as a terminal proof, bridge theorem, or completion signal for Diophantine approximation of algebraic irrational real numbers."
]

/-- Checked row count for the public Roth name-collision caution. -/
theorem publicCombinatorialRothCaution_length :
    publicCombinatorialRothCaution.length = 3 :=
  rfl

/-- A structured row for external Lean 4 primary-source audit results. -/
structure ExternalLeanAuditRow where
  sourceKind : String
  repositoryUrl : String
  commitOrStatus : String
  theoremNames : String
  buildStatus : String
  notes : String
  deriving Repr

/--
Child C005 external Lean 4 primary-source audit rows.

These rows record source-level evidence, authentication/build status, and the
absence of a terminal Roth proof candidate.  They are audit data only; none is
a completed theorem wrapper for `StatementShape`.
-/
def externalLeanPrimarySourceAuditRows : List ExternalLeanAuditRow := [
  {
    sourceKind := "pinned mathlib dependency",
    repositoryUrl := "https://github.com/leanprover-community/mathlib4.git",
    commitOrStatus := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    theoremNames := "Real.infinite_rat_abs_sub_lt_one_div_den_sq_of_irrational; Rat.finite_rat_abs_sub_lt_one_div_den_sq; Real.infinite_rat_abs_sub_lt_one_div_den_sq_iff_irrational; Real.exists_convs_eq_rat; LiouvilleWith; LiouvilleWith.exists_pos; Height.mulHeight₁; Height.logHeight₁; Height.mulHeight; Height.logHeight; roth_3ap_theorem; roth_3ap_theorem_nat",
    buildStatus := "repo-local file validation passes via lake env lean AwesomeTheorems/Stage1/S1_M_012.lean; no terminal Roth theorem found",
    notes := "mathlib provides infrastructure and an irrelevant additive-combinatorics Roth name collision, not the Diophantine-approximation Roth theorem"
  },
  {
    sourceKind := "GitHub CLI authenticated search gate",
    repositoryUrl := "not available",
    commitOrStatus := "blocked on 2026-05-01: gh auth status reports no logged-in GitHub host and no GH_TOKEN",
    theoremNames := "none",
    buildStatus := "not applicable: authenticated search could not be executed in this environment",
    notes := "do not treat unauthenticated fallback searches as an authenticated primary-source audit"
  },
  {
    sourceKind := "GitHub REST repository-search fallback",
    repositoryUrl := "https://api.github.com/search/repositories",
    commitOrStatus := "queries on 2026-05-01 returned total_count = 0 and incomplete_results = false",
    theoremNames := "none",
    buildStatus := "no candidate repository to clone or build",
    notes := "fallback queries: \"Roth's theorem\" Lean; \"Thue-Siegel-Roth\" Lean; DiophantineApproximation Roth Lean; LiouvilleWith IsAlgebraic Lean"
  },
  {
    sourceKind := "GitHub REST code-search fallback",
    repositoryUrl := "https://api.github.com/search/code",
    commitOrStatus := "blocked on 2026-05-01 by unauthenticated API rate limit for code search",
    theoremNames := "none verified",
    buildStatus := "not applicable: no source file or repository commit was returned",
    notes := "exact attempted queries: \"Thue-Siegel-Roth\" language:Lean; \"Roth's theorem\" language:Lean; LiouvilleWith IsAlgebraic language:Lean; DiophantineApproximation Roth language:Lean"
  }
]

/-- Checked row count for the C005 external Lean 4 primary-source audit table. -/
theorem externalLeanPrimarySourceAuditRows_length :
    externalLeanPrimarySourceAuditRows.length = 4 :=
  rfl

/-- Search/audit status for external Lean 4 Roth proof evidence in this child. -/
def externalAnchorAuditStatus : List String := [
  "GitHub CLI authenticated search unavailable on 2026-05-01: gh auth status reports no logged-in host and no GH_TOKEN",
  "GitHub REST repository-search fallback returned no candidate repositories for Roth/Thue-Siegel-Roth/DiophantineApproximation/LiouvilleWith query families",
  "GitHub REST code-search fallback was rate-limited before returning source files, so the authenticated-audit requirement remains an integration blocker",
  "pinned mathlib source is https://github.com/leanprover-community/mathlib4.git at 8a178386ffc0f5fef0b77738bb5449d50efeea95; checked theorem names are infrastructure only, not terminal Roth",
  "no external Lean 4 Roth Diophantine-approximation proof has been pinned, imported, or checked by this repository in this child",
  "completion remains blocked unless an external proof is later pinned/imported/checked or a local proof body is added"
]

/--
The terminal Roth proof obligation for this Stage1 slot.

This is intentionally definitionally the same as `StatementShape`; it records
the missing theorem family without introducing a proof placeholder.
-/
def RothFormalizationDebt : Prop :=
  StatementShape

/-- Checked mathlib anchor: irrational real numbers have infinitely many
Dirichlet-good rational approximations at exponent `2`. -/
theorem irrational_has_infinite_exponent_two_approximants {ξ : ℝ}
    (hξ : Irrational ξ) :
    {q : ℚ | |ξ - (q : ℝ)| < 1 / (q.den : ℝ) ^ 2}.Infinite :=
  Real.infinite_rat_abs_sub_lt_one_div_den_sq_of_irrational hξ

/-- Checked mathlib anchor: rational targets have only finitely many
exponent-`2` good rational approximants. -/
theorem rational_has_finite_exponent_two_approximants (ξ : ℚ) :
    {q : ℚ | |ξ - q| < 1 / (q.den : ℚ) ^ 2}.Finite :=
  Rat.finite_rat_abs_sub_lt_one_div_den_sq ξ

/-- Checked mathlib anchor: infinitude of exponent-`2` approximants is
equivalent to irrationality of the target. -/
theorem infinite_exponent_two_approximants_iff_irrational (ξ : ℝ) :
    {q : ℚ | |ξ - (q : ℝ)| < 1 / (q.den : ℝ) ^ 2}.Infinite ↔ Irrational ξ :=
  Real.infinite_rat_abs_sub_lt_one_div_den_sq_iff_irrational ξ

/-- Checked mathlib anchor: Legendre's theorem in continued-fraction form. -/
theorem legendre_continued_fraction_anchor {ξ : ℝ} {q : ℚ}
    (h : |ξ - (q : ℝ)| < 1 / (2 * (q.den : ℝ) ^ 2)) :
    ∃ n, (GenContFract.of ξ).convs n = q :=
  Real.exists_convs_eq_rat h

/--
Repo-local integration-debt gate for this Stage1 slot.

No external Lean 4 Roth proof has been imported or pinned into this repository
by this module.  The current artifact is therefore not a completed theorem
closure and carries `formalization_debt`, not a completed state with lingering
`repo_local_integration_debt`.
-/
def repoLocalIntegrationDebtGate : List String := [
  "mathlib anchors checked locally: DiophantineApproximation.Basic and ContinuedFractions",
  "additional mathlib audit anchors checked locally: LiouvilleWith, Height.Basic, Height.NumberField, and the non-number-theoretic Combinatorics.Additive.Corner.Roth collision",
  "no terminal Roth theorem found in the pinned mathlib snapshot",
  "no external Lean 4 Roth proof has been pinned/imported/checked in this repository",
  "completion is blocked until a local proof body or pinned external dependency proves StatementShape"
]

/--
Child C006 integration gate for external Lean 4 Roth proof evidence.

This records the public-doc synchronization rule as checked data inside the
owned Lean artifact: finding an external proof is not itself completion.  It
must first become a repo-local validation dependency, or a concrete integration
blocker must be recorded before any public checkbox can change.
-/
def externalProofIntegrationGateC006 : List String := [
  "C006 scope: contingent external-proof integration gate, not a terminal Roth proof body",
  "current evidence from C005: no external Lean 4 Diophantine-approximation Roth proof was found or authenticated",
  "if a terminal external proof is later found, record repository URL, commit, source path, theorem name, license, Lean toolchain, and build command/result",
  "before any completion checkbox changes, either pin/import/check the external proof in this repository or record a concrete blocker such as toolchain mismatch, license conflict, or dependency incompatibility",
  "anchor-only evidence remains external_upstream_anchor_only and cannot count as repo-local completed",
  "current repo-local theorem state remains not_repo_local_closed / formalization_debt"
]

/-- Checked row count for the C006 external-proof integration gate. -/
theorem externalProofIntegrationGateC006_length :
    externalProofIntegrationGateC006.length = 6 :=
  rfl

/--
Child C008 Lake/mathlib vendor reconciliation gate.

This records dependency-state evidence for the later serial public-doc
backfill.  It is not a proof of Roth's theorem and does not mutate the shared
Lake manifest, shared Lake file, or vendor directory.
-/
def lakeMathlibVendorReconciliationC008 : List String := [
  "C008 scope: reconcile local mathlib source state before any public lake build record for THM-M-0399",
  "Lake manifest and lakefile pin mathlib to https://github.com/leanprover-community/mathlib4.git at 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "active Lake package Formalizations/Lean/.lake/packages/mathlib is an independent git checkout detached at 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "lake exe cache get reported: No files to download; Already decompressed 8232 file(s)",
  "Formalizations/Lean/.vendor/mathlib4 exists but is not an independent git checkout: git -C that path resolves to the parent awesome_theorems repository at dc7664a302ed42b3acb861ceeacdb5e866358313",
  "therefore .vendor/mathlib4 cannot be used as manifest-synchronized mathlib evidence until a serial integrator replaces it with a pinned checkout or removes it from the audit path",
  "repo-local validation for this module should rely on Lake's active .lake/packages/mathlib dependency, not on .vendor/mathlib4",
  "full lake build should not be published as a .vendor reconciliation closure until the vendor path blocker is resolved"
]

/-- Checked row count for the C008 Lake/mathlib vendor reconciliation gate. -/
theorem lakeMathlibVendorReconciliationC008_length :
    lakeMathlibVendorReconciliationC008.length = 8 :=
  rfl

/-- Machine proof debt classification for S1-M-012. -/
def machineProofDebtClassification : List String := [
  "formalization_debt: Roth's theorem is mathematically known but not repo-local kernel-checked here",
  "repo_local_integration_debt is not claimed closed by anchor-only evidence",
  "mathematical_debt: none for the classical theorem statement"
]

/-- Canonical theorem-internal leaves for later M0387-level splitting. -/
def canonicalChildLeaves : List String := [
  "P0 statement normalization / Candidate A finite rational approximants / p > 2 exponent freeze",
  "P1 mathlib object model / DiophantineApproximation / LiouvilleWith / Height / false-positive Roth collision",
  "P2 LiouvilleWith bridge for finite rational approximants and irrationality-exponent statements",
  "P3 height and number-field bridge for denominator, height, place, and product-formula estimates",
  "P4 core Roth lemma family covering auxiliary polynomials, Siegel lemma, zero estimates, multiplicity, and gap principle",
  "P5 terminal wrapper or dependency gate for local proof body, mathlib wrapper, or pinned external Roth theorem closure"
]

/-- Public backfill note content for the later serial integrator. -/
def publicStatementNormalizationNote : List String := [
  "THM-M-0399 statement normalization: choose Candidate A as the canonical Lean 4 target.",
  "Canonical target: RothStatementShapeA / StatementShape in AwesomeTheorems.Stage1.S1_M_012.",
  "Surface: for every algebraic irrational real ξ, every real p with 2 < p, and every C > 0, the set of q : ℚ with |ξ - q| < C / Real.rpow (q.den : ℝ) p is finite.",
  "Candidate C is parsed locally as the LiouvilleWith corollary surface: algebraic irrational real ξ is not LiouvilleWith p ξ for p > 2.",
  "Candidate B integer-pair and Candidate C LiouvilleWith surfaces are bridge targets only, not the public root unless an upstream proof forces that interface.",
  "This note is statement normalization only; it is not a proof of Roth's theorem."
]

/-- Public backfill content for the later anchor-audit and P0-P5 split. -/
def publicAuditAndPackageBackfillNote : List String := [
  "Add a mathlib anchor table for THM-M-0399 with DiophantineApproximation.Basic, DiophantineApproximation.ContinuedFractions, Transcendental.Liouville.LiouvilleWith, Height.Basic, Height.NumberField, and Combinatorics.Additive.Corner.Roth.",
  "Record that DiophantineApproximation.Basic supplies exponent-2 irrational/rational approximation anchors, not terminal Roth.",
  "Record that LiouvilleWith is a bridge surface for irrationality-exponent statements, not a proof that algebraic irrational reals fail LiouvilleWith p for p > 2.",
  "Record that Height.Basic and Height.NumberField supply height object-model APIs; the Rat.den to height bridge remains open.",
  "Record that Combinatorics.Additive.Corner.Roth proves roth_3ap_theorem for arithmetic-progressions, not the number-theoretic Roth theorem.",
  "Add a public caution: Mathlib.Combinatorics.Additive.Corner.Roth is an additive-combinatorics module about three-term arithmetic progressions and must not be cited as the number-theoretic Roth theorem for Diophantine approximation.",
  "Use P0-P5 package names from RothProofPackage: P0 statement_normalization; P1 mathlib_object_model; P2 liouville_bridge; P3 height_and_number_field_bridge; P4 core_roth_lemma_family; P5 terminal_wrapper_or_dependency_gate.",
  "Add the C008 Lake reconciliation note: the active Lake mathlib package is detached at manifest revision 8a178386ffc0f5fef0b77738bb5449d50efeea95, but Formalizations/Lean/.vendor/mathlib4 is not an independent git checkout and must not be cited as synchronized source evidence until fixed by a serial integrator."
]

/-- A reader-facing proof-flow outline row for the public C009 backfill. -/
structure HumanReadableProofFlowRow where
  packageId : String
  readerTask : String
  inputInterface : String
  outputInterface : String
  proofFlow : String
  closureBoundary : String
  deriving Repr

/--
Child C009 human-readable proof-flow outline for the public Roth backfill.

This is checked data for a later serial public-doc merge.  It deliberately
avoids runtime-worker wording and records proof-flow responsibilities without
claiming that the terminal Roth proof has been machine checked.
-/
def humanReadableProofFlowOutlineC009 : List HumanReadableProofFlowRow := [
  {
    packageId := "M0399.P0",
    readerTask := "normalize the theorem statement before any proof search",
    inputInterface := "classical Roth statement for algebraic irrational real numbers",
    outputInterface := "Candidate A / StatementShape with finite rational approximants using Rat.den and Real.rpow",
    proofFlow := "The public root should say that for an algebraic irrational real target, every exponent p > 2 and every positive constant C leave only finitely many rational approximants q satisfying the denominator-height inequality.  The epsilon and LiouvilleWith spellings are retained only as bridge surfaces.",
    closureBoundary := "partially checked locally: Candidate A parses, StatementShape is definitionally Candidate A, and Candidate A specializes to the epsilon constant-1 surface; no terminal Roth proof is supplied"
  },
  {
    packageId := "M0399.P1",
    readerTask := "separate usable mathlib infrastructure from false-positive names",
    inputInterface := "pinned mathlib rational approximation, LiouvilleWith, height, number-field, and combinatorial Roth modules",
    outputInterface := "anchor table distinguishing infrastructure from terminal evidence",
    proofFlow := "The proof plan may use exponent-2 Diophantine approximation lemmas, LiouvilleWith terminology, and height APIs as object models.  The additive-combinatorics Roth module is only a name-collision warning and does not contribute to the number-theoretic proof.",
    closureBoundary := "anchor audit only: no mathlib theorem in the inspected snapshot proves Roth's algebraic irrational approximation bound for p > 2"
  },
  {
    packageId := "M0399.P2",
    readerTask := "connect finite approximants to irrationality-exponent language",
    inputInterface := "Candidate A plus LiouvilleWith and denominator-normalized rational approximants",
    outputInterface := "bridge obligations CandidateAToCBridge and CandidateCToABridge",
    proofFlow := "This package must show that infinitely many too-good rational approximations would produce the corresponding LiouvilleWith behavior, while a non-LiouvilleWith conclusion should recover the finite-approximant surface after constants and reduced denominators are normalized.",
    closureBoundary := "unchecked substantive bridge: only the bridge names and conditional assembly lemmas are checked locally"
  },
  {
    packageId := "M0399.P3",
    readerTask := "translate rational approximation into height and product-formula estimates",
    inputInterface := "an algebraic real target, rational approximants, Rat.den, and mathlib height or number-field APIs",
    outputInterface := "height bounds for the approximation difference and denominator contributions",
    proofFlow := "A full proof must place the algebraic target in a number-field context, compare the distinguished real absolute value with other places, and express finite-place contributions in terms of the rational denominator.  These estimates feed the contradiction step.",
    closureBoundary := "unchecked formalization debt: no local Rat.den-to-height, place, or product-formula bridge is proved"
  },
  {
    packageId := "M0399.P4",
    readerTask := "supply the core Roth contradiction",
    inputInterface := "height/product-formula estimates and a long sequence of assumed too-good approximants",
    outputInterface := "contradiction to infinitely many approximants beyond exponent 2",
    proofFlow := "The core branch constructs an auxiliary polynomial with controlled height, forces high multiplicity at approximation points, proves a nonvanishing evaluation, and compares an upper bound from the assumed approximations with a lower bound from height/product-formula estimates.",
    closureBoundary := "deep unchecked formalization debt: no local auxiliary-polynomial, Siegel-lemma, zero-estimate, or gap-principle proof body is present"
  },
  {
    packageId := "M0399.P5",
    readerTask := "close only through repo-local validation",
    inputInterface := "a completed P0-P4 proof chain, a future mathlib theorem, or a concrete external Lean proof candidate",
    outputInterface := "local proof body, local mathlib wrapper, or pinned/imported external dependency proving StatementShape",
    proofFlow := "The public status may change only after the terminal theorem is validated in this repository.  If an external proof appears, it must be pinned, imported, and checked, or a concrete integration blocker must be recorded.",
    closureBoundary := "open gate: current state is not_repo_local_closed / formalization_debt, with no completed state carrying repo_local_integration_debt"
  }
]

/-- Checked row count for the C009 human-readable proof-flow outline. -/
theorem humanReadableProofFlowOutlineC009_length :
    humanReadableProofFlowOutlineC009.length = 6 :=
  rfl

/-- Public backfill text for merging the C009 proof-flow outline later. -/
def publicHumanReadableProofFlowBackfillC009 : List String := [
  "Add a human-readable proof-flow subsection for THM-M-0399 after the machine audit and before any completion checkbox changes.",
  "Use the canonical package names M0399.P0 through M0399.P5; do not introduce a competing proof-tree naming system.",
  "P0: explain that Candidate A / StatementShape is the public root and that epsilon or LiouvilleWith formulations are bridge surfaces only.",
  "P1: explain that mathlib provides rational-approximation, LiouvilleWith, height, and number-field infrastructure, while Combinatorics.Additive.Corner.Roth is a false-positive name collision.",
  "P2: explain the required bridge between finite rational approximants and LiouvilleWith-style irrationality-exponent statements, with constants and denominators normalized.",
  "P3: explain the height and number-field bridge from rational denominators and approximation differences to product-formula estimates.",
  "P4: explain the core Roth proof obligation through auxiliary polynomials, Siegel-lemma input, multiplicity, nonvanishing, and upper/lower bound contradiction.",
  "P5: explain that terminal closure requires a local proof body, checked mathlib wrapper, or pinned/imported external Lean proof; anchor-only evidence is not completion.",
  "Mark P2-P5 substantive proof content as unchecked/formalization_debt unless and until repo-local Lean validation proves the corresponding obligations."
]

/-- Checked row count for the C009 public proof-flow backfill text. -/
theorem publicHumanReadableProofFlowBackfillC009_length :
    publicHumanReadableProofFlowBackfillC009.length = 9 :=
  rfl

/-! ## Audit probes -/

#check IsAlgebraic
#check Irrational
#check Real.rpow
#check Real.infinite_rat_abs_sub_lt_one_div_den_sq_of_irrational
#check Rat.finite_rat_abs_sub_lt_one_div_den_sq
#check Real.infinite_rat_abs_sub_lt_one_div_den_sq_iff_irrational
#check Real.exists_convs_eq_rat
#check LiouvilleWith
#check LiouvilleWith.exists_pos
#check Height.mulHeight₁
#check Height.logHeight₁
#check Height.mulHeight
#check Height.logHeight
#check cornersTheoremBound
#check roth_3ap_theorem
#check roth_3ap_theorem_nat
#check RothApproximationSetA
#check RothStatementShapeA
#check RothStatementShapeEpsilon
#check RothStatementShapeC
#check StatementShape
#check statementShape_is_candidateA
#check candidateA_implies_epsilon
#check CandidateAToCBridge
#check CandidateCToABridge
#check candidateC_of_candidateA_of_bridge
#check candidateC_of_statementShape_of_bridge
#check RothProofPackage
#check rothProofPackageSplit
#check rothProofPackageSplit_length
#check RothPackageRow
#check rothTheoremTreePackageRows
#check rothTheoremTreePackageRows_length
#check rothProofPackageStatus
#check mathlibAnchorModules
#check MathlibAnchorRow
#check mathlibAnchorTable
#check mathlibAnchorTable_length
#check mathlibAnchorAudit
#check publicCombinatorialRothCaution
#check publicCombinatorialRothCaution_length
#check ExternalLeanAuditRow
#check externalLeanPrimarySourceAuditRows
#check externalLeanPrimarySourceAuditRows_length
#check externalAnchorAuditStatus
#check RothFormalizationDebt
#check repoLocalIntegrationDebtGate
#check externalProofIntegrationGateC006
#check externalProofIntegrationGateC006_length
#check lakeMathlibVendorReconciliationC008
#check lakeMathlibVendorReconciliationC008_length
#check HumanReadableProofFlowRow
#check humanReadableProofFlowOutlineC009
#check humanReadableProofFlowOutlineC009_length
#check publicHumanReadableProofFlowBackfillC009
#check publicHumanReadableProofFlowBackfillC009_length

end S1_M_012
end Stage1
end AwesomeTheorems
