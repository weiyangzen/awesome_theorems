import Mathlib.Tactic

/-!
# S1-M-005 / THM-M-0391: Mihailescu's theorem, Stage1 statement shape

This module records a Lean 4 statement-shape boundary for Mihailescu's theorem
(Catalan's conjecture): the only pair of consecutive nontrivial perfect powers
is `8` and `9`.

The file intentionally does not claim a proof of the theorem.  The local mathlib
audit found nearby elementary number-theory and Fermat-Catalan polynomial
infrastructure, but no terminal theorem for Mihailescu/Catalan in the local
dependency closure.
-/

namespace AwesomeTheorems.Stage1.S1_M_005

/-- The Catalan equation in the orientation `x ^ a = y ^ b + 1`, avoiding
truncated subtraction on natural numbers. -/
def CatalanEquation (x a y b : ℕ) : Prop :=
  x ^ a = y ^ b + 1

/-- Nontrivial bases and exponents for the Catalan/Mihailescu statement. -/
def NontrivialPerfectPowerPair (x a y b : ℕ) : Prop :=
  1 < x ∧ 1 < a ∧ 1 < y ∧ 1 < b

/-- The unique exceptional solution, written in the same variable order as
`CatalanEquation`: `3 ^ 2 = 2 ^ 3 + 1`. -/
def ExceptionalSolution (x a y b : ℕ) : Prop :=
  x = 3 ∧ a = 2 ∧ y = 2 ∧ b = 3

/--
Candidate A, the canonical Stage1 normalized statement shape for Mihailescu's
theorem / Catalan's conjecture.

Every nontrivial natural-number solution of `x ^ a = y ^ b + 1` is the
exceptional consecutive-perfect-power pair `3 ^ 2` and `2 ^ 3`.
-/
def StatementShape : Prop :=
  ∀ x a y b : ℕ,
    NontrivialPerfectPowerPair x a y b →
      CatalanEquation x a y b →
        ExceptionalSolution x a y b

/-- Explicit Candidate A alias retained for public blueprint backfill text. -/
def StatementShapeNat : Prop :=
  StatementShape

/-- A natural number is a nontrivial perfect power if it has a base and exponent
both greater than `1`. -/
def IsNontrivialNatPower (z : ℕ) : Prop :=
  ∃ a k : ℕ, 1 < a ∧ 1 < k ∧ z = a ^ k

/--
Candidate B wrapper shape: the only consecutive nontrivial perfect-power values
are `8` and `9`.

This is kept as a wrapper target rather than the canonical Stage1 statement
because it hides the bases and exponents behind witnesses.
-/
def StatementShapeConsecutiveValues : Prop :=
  ∀ u v : ℕ,
    IsNontrivialNatPower u →
      IsNontrivialNatPower v →
        u + 1 = v →
          u = 8 ∧ v = 9

/--
Candidate C wrapper shape over integers.

This is kept as a bridge target for number-field-oriented proofs; Candidate A is
canonical because it avoids extra `Int`/`Nat` transfer decisions.
-/
def StatementShapeIntPositive : Prop :=
  ∀ (x y : ℤ) (a b : ℕ),
    1 < x →
      1 < y →
        1 < a →
          1 < b →
            x ^ a - y ^ b = 1 →
              x = 3 ∧ a = 2 ∧ y = 2 ∧ b = 3

/--
Checked repo-local wrapper target for the canonical natural-number statement.

This theorem is intentionally conditional: a future terminal proof of
`StatementShape` would immediately close the explicit `StatementShapeNat`
wrapper without changing the public statement shape.
-/
theorem statementShapeNat_of_statementShape
    (h : StatementShape) : StatementShapeNat :=
  h

/--
Checked repo-local bridge target from Candidate A to Candidate B.

This is closure plumbing only.  It proves that a future proof of the canonical
base/exponent statement would discharge the consecutive-value wrapper, but it
does not provide the missing proof of `StatementShape` itself.
-/
theorem statementShapeConsecutiveValues_of_statementShape
    (h : StatementShape) : StatementShapeConsecutiveValues := by
  intro u v hu hv huv
  rcases hu with ⟨y, b, hy, hb, rfl⟩
  rcases hv with ⟨x, a, hx, ha, rfl⟩
  have hsol : ExceptionalSolution x a y b :=
    h x a y b ⟨hx, ha, hy, hb⟩ (by
      unfold CatalanEquation
      exact huv.symm)
  rcases hsol with ⟨rfl, rfl, rfl, rfl⟩
  norm_num

/-- Locally checked sanity lemma for the exceptional solution used in the
statement shape.  This is not a proof of the universal theorem. -/
theorem exceptionalSolution_satisfies_equation :
    CatalanEquation 3 2 2 3 := by
  norm_num [CatalanEquation]

/-- Locally checked sanity lemma that the exceptional solution is nontrivial. -/
theorem exceptionalSolution_nontrivial :
    NontrivialPerfectPowerPair 3 2 2 3 := by
  norm_num [NontrivialPerfectPowerPair]

/-- Locally checked sanity lemma for the Candidate B exceptional values. -/
theorem exceptionalValues_are_nontrivial_powers :
    IsNontrivialNatPower 8 ∧ IsNontrivialNatPower 9 := by
  constructor
  · refine ⟨2, 3, ?_, ?_, ?_⟩ <;> norm_num
  · refine ⟨3, 2, ?_, ?_, ?_⟩ <;> norm_num

/-- Locally checked terminal arithmetic for the Candidate B exceptional values. -/
theorem exceptionalValues_are_consecutive :
    8 + 1 = 9 := by
  norm_num

/-- Locally checked sanity lemma for the Candidate C exceptional solution. -/
theorem exceptionalSolution_satisfies_int_equation :
    (3 : ℤ) ^ (2 : ℕ) - (2 : ℤ) ^ (3 : ℕ) = 1 := by
  norm_num

/--
Finite low-dimensional check over the base/exponent grid `{2, 3}`.

Within this small grid, the Catalan equation already forces the exceptional
solution.  This is a terminal arithmetic leaf only; it does not cover arbitrary
bases or exponents.
-/
theorem two_three_grid_catalanEquation_classifies
    {x a y b : ℕ}
    (hx : x = 2 ∨ x = 3)
    (ha : a = 2 ∨ a = 3)
    (hy : y = 2 ∨ y = 3)
    (hb : b = 2 ∨ b = 3)
    (h : CatalanEquation x a y b) :
    ExceptionalSolution x a y b := by
  rcases hx with rfl | rfl <;>
    rcases ha with rfl | rfl <;>
    rcases hy with rfl | rfl <;>
    rcases hb with rfl | rfl <;>
    norm_num [CatalanEquation, ExceptionalSolution] at *

/--
The same finite `{2, 3}` check packaged with the nontriviality hypotheses used
by the canonical statement shape.
-/
theorem two_three_grid_statementShape_leaf
    {x a y b : ℕ}
    (hx : x = 2 ∨ x = 3)
    (ha : a = 2 ∨ a = 3)
    (hy : y = 2 ∨ y = 3)
    (hb : b = 2 ∨ b = 3)
    (_hnontrivial : NontrivialPerfectPowerPair x a y b)
    (h : CatalanEquation x a y b) :
    ExceptionalSolution x a y b :=
  two_three_grid_catalanEquation_classifies hx ha hy hb h

/-- Names of local declarations that define this Stage1 statement boundary. -/
def checkedDeclarationNames : List String :=
  [ "AwesomeTheorems.Stage1.S1_M_005.CatalanEquation",
    "AwesomeTheorems.Stage1.S1_M_005.NontrivialPerfectPowerPair",
    "AwesomeTheorems.Stage1.S1_M_005.ExceptionalSolution",
    "AwesomeTheorems.Stage1.S1_M_005.StatementShape",
    "AwesomeTheorems.Stage1.S1_M_005.StatementShapeNat",
    "AwesomeTheorems.Stage1.S1_M_005.IsNontrivialNatPower",
    "AwesomeTheorems.Stage1.S1_M_005.StatementShapeConsecutiveValues",
    "AwesomeTheorems.Stage1.S1_M_005.StatementShapeIntPositive",
    "AwesomeTheorems.Stage1.S1_M_005.statementShapeNat_of_statementShape",
    "AwesomeTheorems.Stage1.S1_M_005.statementShapeConsecutiveValues_of_statementShape",
    "AwesomeTheorems.Stage1.S1_M_005.exceptionalSolution_satisfies_equation",
    "AwesomeTheorems.Stage1.S1_M_005.exceptionalSolution_nontrivial",
    "AwesomeTheorems.Stage1.S1_M_005.exceptionalValues_are_nontrivial_powers",
    "AwesomeTheorems.Stage1.S1_M_005.exceptionalValues_are_consecutive",
    "AwesomeTheorems.Stage1.S1_M_005.exceptionalSolution_satisfies_int_equation",
    "AwesomeTheorems.Stage1.S1_M_005.two_three_grid_catalanEquation_classifies",
    "AwesomeTheorems.Stage1.S1_M_005.two_three_grid_statementShape_leaf",
    "AwesomeTheorems.Stage1.S1_M_005.theoremTreeSurfacePackages",
    "AwesomeTheorems.Stage1.S1_M_005.uncheckedLeafLedger",
    "AwesomeTheorems.Stage1.S1_M_005.publicTheoremTreeBackfillTargets",
    "AwesomeTheorems.Stage1.S1_M_005.completionGateNote" ]

/-- Checked finite special-case leaves for `THM-M-0391-SPECIAL-CASES`. -/
def checkedSpecialCaseLeaves : List String :=
  [ "exceptionalSolution_satisfies_equation: checks 3^2 = 2^3 + 1",
    "exceptionalSolution_nontrivial: checks bases/exponents 3,2,2,3 are all > 1",
    "exceptionalValues_are_nontrivial_powers: checks 8 and 9 have nontrivial power witnesses",
    "exceptionalValues_are_consecutive: checks 8 + 1 = 9",
    "exceptionalSolution_satisfies_int_equation: checks the Int equation 3^2 - 2^3 = 1",
    "two_three_grid_catalanEquation_classifies: classifies the finite base/exponent grid {2,3}",
    "two_three_grid_statementShape_leaf: packages the {2,3} grid check in StatementShape hypothesis form" ]

/-- Dependency split for the next Mihailescu proof-package pass. -/
def dependencySplit : List String :=
  [ "P00 statement normalization: CatalanEquation, NontrivialPerfectPowerPair, ExceptionalSolution, StatementShape",
    "P01 wrapper targets: StatementShapeNat and StatementShapeConsecutiveValues are conditionally discharged from StatementShape",
    "P02 elementary reductions: Nat/Int transfer, zero-one elimination, coprimality, parity, shared-prime split",
    "P03 exponent reductions: composite exponent to prime divisor branches and square/cube special cases",
    "P04 arithmetic support APIs: Nat.factorization, Nat.Prime.pow_inj', IsPrimePow, Pell/FLT-adjacent lemmas",
    "P05 algebraic-number-theory frontier: cyclotomic fields, units, ideals, class groups, local obstructions",
    "P06 terminal closure gate: local_proof_body, local_wrapper_upstream_mathlib, or external_upstream_pinned only" ]

/-- Repo-local wrapper targets that may be closed once a terminal proof exists. -/
def repoLocalWrapperTargets : List String :=
  [ "StatementShapeNat from StatementShape via statementShapeNat_of_statementShape",
    "StatementShapeConsecutiveValues from StatementShape via statementShapeConsecutiveValues_of_statementShape",
    "StatementShapeIntPositive remains a bridge target pending explicit Int/Nat transfer lemmas",
    "No wrapper target is a proof of Mihailescu's theorem until StatementShape has a checked proof body or pinned upstream theorem" ]

/--
Public theorem-tree package surface prepared for serial blueprint merge.

Items marked `checked` are repo-local Lean declarations in this file.  Items
marked `unchecked` are package nodes only; they are not proof-complete leaves.
-/
def theoremTreeSurfacePackages : List String :=
  [ "P00 statement normalization: checked; CatalanEquation, NontrivialPerfectPowerPair, ExceptionalSolution, StatementShape, and StatementShapeNat validate repo-locally",
    "P01 wrapper targets: partially checked; statementShapeNat_of_statementShape and statementShapeConsecutiveValues_of_statementShape validate conditionally from StatementShape; StatementShapeIntPositive remains unchecked",
    "P02 elementary reductions: unchecked; Nat/Int transfer, zero-one elimination, coprimality, parity normalization, and shared-prime split still need local lemma nodes",
    "P03 exponent reductions: unchecked; composite-exponent descent to prime exponents and square/cube branches still need local theorem nodes",
    "P04 arithmetic support APIs: unchecked; Nat.factorization, Nat.Prime.pow_inj', prime-power support, Pell-style support, and FLT-adjacent imports need theorem-level audit against the local pin",
    "P05 algebraic-number-theory frontier: unchecked; cyclotomic fields, units, ideals, class groups, and local obstruction packages are not represented by repo-local proof nodes",
    "P06 terminal closure gate: open; completion requires local_proof_body, local_wrapper_upstream_mathlib, or external_upstream_pinned with repo-local validation" ]

/--
Unchecked leaf ledger for the Mihailescu theorem-tree surface.

Every item here is intentionally open and must remain unchecked in public
surfaces until it has either a local proof body or a pinned/imported checked
upstream theorem plus an independent `<=100` step local ledger.
-/
def uncheckedLeafLedger : List String :=
  [ "U-P01-C: StatementShapeIntPositive bridge from Candidate A is unchecked; needs explicit positivity, coercion, subtraction, and Nat/Int power-transfer lemmas",
    "U-P02-0: zero/one and nontriviality eliminations are unchecked outside the current hypotheses",
    "U-P02-coprime: coprimality of a primitive Catalan solution is unchecked as a reusable local lemma",
    "U-P02-parity: parity normalization and even/odd branch coverage are unchecked",
    "U-P02-shared-prime: shared-prime exclusion for the two consecutive powers is unchecked as a tree node",
    "U-P03-composite-exponent: reduction from composite exponents to prime-divisor exponent branches is unchecked",
    "U-P03-square-cube: square/cube and low-dimensional infinite-family branches are unchecked beyond the finite {2,3} grid leaf",
    "U-P04-factorization-api: factorization and prime-power API bridge lemmas are unchecked against the pinned mathlib revision",
    "U-P04-pell-flt: Pell-style or FLT-adjacent support lemmas are unchecked for this theorem statement",
    "U-P05-cyclotomic: cyclotomic unit and ideal/class-group packages are unchecked and have no repo-local Lean proof nodes",
    "U-P05-local-obstruction: local obstruction/descent terminal contradiction is unchecked",
    "U-P06-terminal: no checked terminal theorem for StatementShape is present in the repo-local closure" ]

/-- Public merge targets prepared by the C006 theorem-tree child pass. -/
def publicTheoremTreeBackfillTargets : List String :=
  [ "Merge theoremTreeSurfacePackages into the public THM-M-0391 theorem-tree surface",
    "Merge uncheckedLeafLedger with literal unchecked/open wording; do not mark package nodes completed",
    "Keep THM-M-0391-TREE open until serial public-doc integration lands",
    "Keep the parent theorem open until P06 is closed by local_proof_body, local_wrapper_upstream_mathlib, or external_upstream_pinned" ]

/--
Completion gate note for `THM-M-0391-GATE`.

No public checkbox for Mihailescu/Catalan proof completion may be promoted from
open until one of these repo-local closure modes is present and validated:
`local_proof_body`, `local_wrapper_upstream_mathlib`, or
`external_upstream_pinned`.  External anchors, statement-only files, conditional
wrappers, and finite sanity leaves are insufficient for completion.
-/
def completionGateNote : List String :=
  [ "Before any THM-M-0391 checkbox promotion, require one of: local_proof_body, local_wrapper_upstream_mathlib, external_upstream_pinned",
    "external_upstream_anchor_only is not completion evidence unless the dependency is pinned/imported and repo-locally checked",
    "StatementShape, conditional wrappers, and finite sanity leaves do not close Mihailescu's theorem",
    "No completed state may retain repo_local_integration_debt; unresolved integration blockers must keep the public checklist open" ]

/--
Repo-local integration-debt gate for this Stage1 artifact.

The current value is `False` because this module has only statement shapes,
sanity leaves, dependency split metadata, and conditional wrapper targets.  It
does not pin, import, or prove a terminal Mihailescu theorem.
-/
def repoLocalIntegrationDebtClosed : Prop := False

/-- Local mathlib search terms used for the negative terminal-theorem audit. -/
def negativeAuditSearchTerms : List String :=
  [ "Mihailescu",
    "Mihăilescu",
    "Catalan conjecture",
    "consecutive perfect powers",
    "PerfectPower" ]

/-- Pinned mathlib revision used for the Stage1 Mihailescu audit. -/
def mathlibAuditPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Repo-local mathlib audit findings for the pinned revision. -/
def mathlibAuditFindings : List String :=
  [ "Formalizations/Lean/lakefile.lean and lake-manifest.json pin mathlib4 at 8a178386ffc0f5fef0b77738bb5449d50efeea95",
    "Mathlib/docs/1000.yaml has Q174955 with title Mihăilescu's theorem and no decl or decls field",
    "Searches for Mihailescu, Mihăilescu, Catalan's conjecture, consecutive perfect powers, and perfect powers found no terminal integer theorem",
    "Catalan-number modules and Polynomial.flt_catalan are non-terminal adjacent material for THM-M-0391",
    "The pinned mathlib role for THM-M-0391 is support substrate only, not local_wrapper_upstream_mathlib closure" ]

/-- External Lean 4 audit status for the Stage1 Mihailescu child audit. -/
def externalLeanAuditFindings : List String :=
  [ "GitHub CLI authenticated code search was blocked on 2026-05-01 because gh auth status reported no logged-in GitHub hosts and no GH_TOKEN/GITHUB_TOKEN was present",
    "Project-specific search of pinned Lake dependencies found no Mihailescu/Catalan terminal theorem in mathlib4 or flt-regular",
    "DeepMind formal-conjectures commit 7871d8fc7a8164a1ac16c3765b40c25ce015b681 contains theorem Catalan.catalans_conjecture in FormalConjectures/Wikipedia/Catalan.lean",
    "formal-conjectures Catalan.catalans_conjecture is a statement-only Lean anchor ending in sorry, not a machine-checked proof of Mihailescu's theorem",
    "formal-conjectures at that commit uses leanprover/lean4:v4.27.0 and mathlib inputRev v4.27.0 with mathlib rev a3a10db0e9d66acbebf76c5e6a135066525ac900; this repo uses Lean v4.29.0 and mathlib rev 8a178386ffc0f5fef0b77738bb5449d50efeea95",
    "No external_upstream_pinned closure is available from this audit; current machine status remains not_repo_local_closed/formalization_debt" ]

/-- Exact external URLs captured for the Stage1 Mihailescu external-anchor audit. -/
def externalLeanAuditUrls : List String :=
  [ "https://github.com/google-deepmind/formal-conjectures/tree/7871d8fc7a8164a1ac16c3765b40c25ce015b681",
    "https://github.com/google-deepmind/formal-conjectures/blob/7871d8fc7a8164a1ac16c3765b40c25ce015b681/FormalConjectures/Wikipedia/Catalan.lean#L34-L36",
    "https://github.com/google-deepmind/formal-conjectures/blob/7871d8fc7a8164a1ac16c3765b40c25ce015b681/FormalConjecturesForMathlib/Data/Nat/PerfectPower.lean#L35-L39",
    "https://github.com/google-deepmind/formal-conjectures/blob/7871d8fc7a8164a1ac16c3765b40c25ce015b681/lakefile.toml#L21-L39",
    "https://github.com/google-deepmind/formal-conjectures/blob/7871d8fc7a8164a1ac16c3765b40c25ce015b681/lean-toolchain#L1" ]

end AwesomeTheorems.Stage1.S1_M_005

#check AwesomeTheorems.Stage1.S1_M_005.CatalanEquation
#check AwesomeTheorems.Stage1.S1_M_005.NontrivialPerfectPowerPair
#check AwesomeTheorems.Stage1.S1_M_005.ExceptionalSolution
#check AwesomeTheorems.Stage1.S1_M_005.StatementShape
#check AwesomeTheorems.Stage1.S1_M_005.StatementShapeNat
#check AwesomeTheorems.Stage1.S1_M_005.IsNontrivialNatPower
#check AwesomeTheorems.Stage1.S1_M_005.StatementShapeConsecutiveValues
#check AwesomeTheorems.Stage1.S1_M_005.StatementShapeIntPositive
#check AwesomeTheorems.Stage1.S1_M_005.statementShapeNat_of_statementShape
#check AwesomeTheorems.Stage1.S1_M_005.statementShapeConsecutiveValues_of_statementShape
#check AwesomeTheorems.Stage1.S1_M_005.exceptionalSolution_satisfies_equation
#check AwesomeTheorems.Stage1.S1_M_005.exceptionalSolution_nontrivial
#check AwesomeTheorems.Stage1.S1_M_005.exceptionalValues_are_nontrivial_powers
#check AwesomeTheorems.Stage1.S1_M_005.exceptionalValues_are_consecutive
#check AwesomeTheorems.Stage1.S1_M_005.exceptionalSolution_satisfies_int_equation
#check AwesomeTheorems.Stage1.S1_M_005.two_three_grid_catalanEquation_classifies
#check AwesomeTheorems.Stage1.S1_M_005.two_three_grid_statementShape_leaf
#check AwesomeTheorems.Stage1.S1_M_005.dependencySplit
#check AwesomeTheorems.Stage1.S1_M_005.repoLocalWrapperTargets
#check AwesomeTheorems.Stage1.S1_M_005.checkedSpecialCaseLeaves
#check AwesomeTheorems.Stage1.S1_M_005.theoremTreeSurfacePackages
#check AwesomeTheorems.Stage1.S1_M_005.uncheckedLeafLedger
#check AwesomeTheorems.Stage1.S1_M_005.publicTheoremTreeBackfillTargets
#check AwesomeTheorems.Stage1.S1_M_005.completionGateNote
#check AwesomeTheorems.Stage1.S1_M_005.repoLocalIntegrationDebtClosed
#check AwesomeTheorems.Stage1.S1_M_005.negativeAuditSearchTerms
#check AwesomeTheorems.Stage1.S1_M_005.mathlibAuditPinnedRevision
#check AwesomeTheorems.Stage1.S1_M_005.mathlibAuditFindings
#check AwesomeTheorems.Stage1.S1_M_005.externalLeanAuditFindings
#check AwesomeTheorems.Stage1.S1_M_005.externalLeanAuditUrls
