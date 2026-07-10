import Mathlib.NumberTheory.Pell

/-!
# S1-M-003 / THM-M-0388: Pell's equation

This Stage1 artifact records a repo-local Lean 4 wrapper for the classical
Pell equation `x^2 - D * y^2 = 1`.

The pinned mathlib dependency already contains the terminal theorem family for
positive nonsquare integer parameters:

* `Pell.exists_of_not_isSquare` gives a nontrivial integer solution.
* `Pell.existsUnique_pos_generator` gives the unique positive generator of the
  solution group up to sign.

The declarations below expose that theorem family under this repository's
Stage1 namespace.  They introduce no proof placeholders and no new axioms.
-/

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_003

/-- Normalized Pell parameter hypothesis: `D` is positive and not an integer square. -/
def IsNonsquarePositivePellParameter (D : ℤ) : Prop :=
  0 < D ∧ ¬ IsSquare D

/-- The integer Pell equation attached to the parameter `D`. -/
def PellEquation (D x y : ℤ) : Prop :=
  x ^ 2 - D * y ^ 2 = 1

/-- Nontrivial solvability of the Pell equation over the integers. -/
def NontrivialIntegerSolutionExists (D : ℤ) : Prop :=
  ∃ x y : ℤ, PellEquation D x y ∧ y ≠ 0

/-- Positive solution existence in mathlib's structured Pell-solution type. -/
def PositiveStructuredSolutionExists (D : ℤ) : Prop :=
  ∃ a : Pell.Solution₁ D, 1 < a.x ∧ 0 < a.y

/--
The generator/classification form of Pell's equation:
there is a unique positive solution whose integer powers generate every
solution up to the common sign.
-/
def PositiveGeneratorClassifiesAllSolutions (D : ℤ) : Prop :=
  ∃! a₁ : Pell.Solution₁ D,
    1 < a₁.x ∧
      0 < a₁.y ∧
        ∀ a : Pell.Solution₁ D, ∃ n : ℤ, a = a₁ ^ n ∨ a = -a₁ ^ n

/--
Stage1 normalized statement shape for THM-M-0388.

For every positive nonsquare integer parameter, the Pell equation has a
nontrivial integer solution and the full mathlib solution group has a unique
positive generator up to sign.
-/
def StatementShape : Prop :=
  ∀ D : ℤ,
    IsNonsquarePositivePellParameter D →
      NontrivialIntegerSolutionExists D ∧ PositiveGeneratorClassifiesAllSolutions D

/-- The statement-shape predicate unfolds to the imported Pell theorem family. -/
theorem statementShape_iff :
    StatementShape ↔
      ∀ D : ℤ,
        IsNonsquarePositivePellParameter D →
          NontrivialIntegerSolutionExists D ∧ PositiveGeneratorClassifiesAllSolutions D :=
  Iff.rfl

/-- Checked mathlib wrapper: every positive nonsquare `D` has a nontrivial integer solution. -/
theorem exists_nontrivial_integer_solution_mathlib_wrapper
    {D : ℤ} (hD : IsNonsquarePositivePellParameter D) :
    NontrivialIntegerSolutionExists D := by
  simpa [NontrivialIntegerSolutionExists, PellEquation] using
    Pell.exists_of_not_isSquare hD.1 hD.2

/-- Checked mathlib wrapper: every positive nonsquare `D` has a positive structured solution. -/
theorem exists_positive_structured_solution_mathlib_wrapper
    {D : ℤ} (hD : IsNonsquarePositivePellParameter D) :
    PositiveStructuredSolutionExists D := by
  simpa [PositiveStructuredSolutionExists] using
    Pell.Solution₁.exists_pos_of_not_isSquare hD.1 hD.2

/--
Checked mathlib wrapper: the unique positive generator classifies all Pell
solutions up to powers and sign.
-/
theorem existsUnique_positive_generator_mathlib_wrapper
    {D : ℤ} (hD : IsNonsquarePositivePellParameter D) :
    PositiveGeneratorClassifiesAllSolutions D := by
  simpa [PositiveGeneratorClassifiesAllSolutions] using
    Pell.existsUnique_pos_generator hD.1 hD.2

/-- Repo-local terminal wrapper for the normalized Stage1 statement shape. -/
theorem statementShape_mathlib_wrapper : StatementShape := by
  intro D hD
  exact
    ⟨exists_nontrivial_integer_solution_mathlib_wrapper hD,
      existsUnique_positive_generator_mathlib_wrapper hD⟩

/-- Checked substrate: a structured Pell solution exposes integer coordinates satisfying the equation. -/
theorem structured_solution_coordinates_satisfy_equation
    {D : ℤ} (a : Pell.Solution₁ D) :
    PellEquation D a.x a.y := by
  simpa [PellEquation] using Pell.Solution₁.prop a

/-- Checked substrate: an equation proof constructs a structured Pell solution with the given `x`. -/
theorem mk_solution_x {D x y : ℤ} (h : PellEquation D x y) :
    (Pell.Solution₁.mk x y (by simpa [PellEquation] using h)).x = x := by
  simp

/-- Checked substrate: an equation proof constructs a structured Pell solution with the given `y`. -/
theorem mk_solution_y {D x y : ℤ} (h : PellEquation D x y) :
    (Pell.Solution₁.mk x y (by simpa [PellEquation] using h)).y = y := by
  simp

/-- mathlib modules checked for this Stage1 Pell wrapper. -/
def mathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.Pell",
  "Mathlib.NumberTheory.Zsqrtd.Basic",
  "Mathlib.NumberTheory.DiophantineApproximation.Basic",
  "Mathlib.Algebra.ContinuedFractions.Basic"
]

/-- Pinned theorem and definition names used by this repo-local wrapper. -/
def mathlibAnchorNames : List String := [
  "Pell.exists_of_not_isSquare",
  "Pell.exists_iff_not_isSquare",
  "Pell.Solution₁",
  "Pell.Solution₁.prop",
  "Pell.Solution₁.mk",
  "Pell.Solution₁.exists_nontrivial_of_not_isSquare",
  "Pell.Solution₁.exists_pos_of_not_isSquare",
  "Pell.IsFundamental.exists_of_not_isSquare",
  "Pell.IsFundamental.eq_zpow_or_neg_zpow",
  "Pell.existsUnique_pos_generator",
  "Pell.pos_generator_iff_fundamental"
]

/-- Machine proof debt classification for this module. -/
def machineProofDebtClassification : String :=
  "local_wrapper_upstream_mathlib: terminal Pell existence and generator theorems are imported from pinned mathlib and checked by this repo-local wrapper."

/-! ## Audit probes -/

#check Pell.exists_of_not_isSquare
#check Pell.existsUnique_pos_generator
#check Pell.Solution₁.exists_pos_of_not_isSquare
#check structured_solution_coordinates_satisfy_equation
#check statementShape_mathlib_wrapper

end S1_M_003
end Stage1
end AwesomeTheorems

namespace AwesomeTheorems.NumberTheory.THM_M_0388.PellPath

abbrev IsNonsquarePositivePellParameter :=
  AwesomeTheorems.Stage1.S1_M_003.IsNonsquarePositivePellParameter

abbrev PellEquation :=
  AwesomeTheorems.Stage1.S1_M_003.PellEquation

abbrev NontrivialIntegerSolutionExists :=
  AwesomeTheorems.Stage1.S1_M_003.NontrivialIntegerSolutionExists

abbrev PositiveStructuredSolutionExists :=
  AwesomeTheorems.Stage1.S1_M_003.PositiveStructuredSolutionExists

abbrev PositiveGeneratorClassifiesAllSolutions :=
  AwesomeTheorems.Stage1.S1_M_003.PositiveGeneratorClassifiesAllSolutions

abbrev StatementShape :=
  AwesomeTheorems.Stage1.S1_M_003.StatementShape

/-- Public root wrapper for the normalized THM-M-0388 statement shape. -/
theorem statementShape_mathlib_closure :
    StatementShape :=
  AwesomeTheorems.Stage1.S1_M_003.statementShape_mathlib_wrapper

/-- Candidate A wrapper: raw nontrivial integer solution existence. -/
theorem candidateA_nontrivial_integer_solution
    {D : ℤ} (hD : IsNonsquarePositivePellParameter D) :
    NontrivialIntegerSolutionExists D :=
  AwesomeTheorems.Stage1.S1_M_003.exists_nontrivial_integer_solution_mathlib_wrapper hD

/-- Candidate B wrapper: mathlib's positive structured Pell solution existence theorem. -/
theorem candidateB_positive_structured_solution
    {D : ℤ} (hD : IsNonsquarePositivePellParameter D) :
    PositiveStructuredSolutionExists D :=
  AwesomeTheorems.Stage1.S1_M_003.exists_positive_structured_solution_mathlib_wrapper hD

/-- Candidate C wrapper: mathlib's unique positive generator and classification theorem. -/
theorem candidateC_positive_generator_classification
    {D : ℤ} (hD : IsNonsquarePositivePellParameter D) :
    PositiveGeneratorClassifiesAllSolutions D :=
  AwesomeTheorems.Stage1.S1_M_003.existsUnique_positive_generator_mathlib_wrapper hD

/-- Source-facing raw integer existence alias, directly backed by `Pell.exists_of_not_isSquare`. -/
theorem raw_integer_existence_of_positive_nonsquare
    {D : ℤ} (hD : IsNonsquarePositivePellParameter D) :
    ∃ x y : ℤ, x ^ 2 - D * y ^ 2 = 1 ∧ y ≠ 0 := by
  simpa using Pell.exists_of_not_isSquare hD.1 hD.2

/-- Source-facing raw integer existence alias with mathlib's hypotheses exposed directly. -/
theorem source_raw_integer_existence_of_not_isSquare
    {D : ℤ} (hDpos : 0 < D) (hDnsq : ¬ IsSquare D) :
    ∃ x y : ℤ, x ^ 2 - D * y ^ 2 = 1 ∧ y ≠ 0 := by
  simpa using Pell.exists_of_not_isSquare hDpos hDnsq

/-- Source-facing raw integer existence alias in the local statement-shape predicate. -/
theorem nontrivial_integer_solution_exists_of_positive_nonsquare
    {D : ℤ} (hD : IsNonsquarePositivePellParameter D) :
    NontrivialIntegerSolutionExists D :=
  AwesomeTheorems.Stage1.S1_M_003.exists_nontrivial_integer_solution_mathlib_wrapper hD

/-- Public audit rows for the pinned mathlib Pell theorem family used by this path. -/
def theoremLevelAuditRows : List (String × String × String × String) := [
  ("Mathlib.NumberTheory.Pell", "Pell.Solution₁",
    "structured norm-one integer solutions to x^2 - D*y^2 = 1",
    "pinned mathlib dependency, imported by this local wrapper"),
  ("Mathlib.NumberTheory.Pell", "Pell.exists_of_not_isSquare",
    "raw nontrivial integer solution existence for positive nonsquare D",
    "local_wrapper_upstream_mathlib via source_raw_integer_existence_of_not_isSquare"),
  ("Mathlib.NumberTheory.Pell", "Pell.Solution₁.exists_pos_of_not_isSquare",
    "Candidate B: positive structured solution existence",
    "local_wrapper_upstream_mathlib via candidateB_positive_structured_solution"),
  ("Mathlib.NumberTheory.Pell", "Pell.IsFundamental.eq_zpow_or_neg_zpow",
    "fundamental-solution classification of each structured solution up to sign and zpow",
    "pinned mathlib dependency, audited as a named classification anchor"),
  ("Mathlib.NumberTheory.Pell", "Pell.existsUnique_pos_generator",
    "Candidate C: unique positive generator with signed zpow classification",
    "local_wrapper_upstream_mathlib via candidateC_positive_generator_classification")
]

/-- First proof-package queue for the M0387-level public backfill of THM-M-0388. -/
def firstProofPackageQueue : List (String × String × String × String) := [
  ("PP-A", "integer existence statement shape",
    "Pell.exists_of_not_isSquare",
    "closed locally by candidateA_nontrivial_integer_solution and source_raw_integer_existence_of_not_isSquare"),
  ("PP-B", "positive structured solution bridge",
    "Pell.Solution₁.exists_pos_of_not_isSquare",
    "closed locally by candidateB_positive_structured_solution"),
  ("PP-C", "positive generator classification",
    "Pell.existsUnique_pos_generator",
    "closed locally by candidateC_positive_generator_classification"),
  ("PP-D", "coordinate bridge between raw equation and structured solution",
    "Pell.Solution₁.prop and Pell.Solution₁.mk",
    "closed locally by structured_solution_coordinates_satisfy_equation, mk_solution_x, and mk_solution_y"),
  ("PP-E", "public theorem-tree and <=100 leaf ledger backfill",
    "PellPath.publicLeafBudgetLedger",
    "closed locally in this Lean surface; serial public-doc integration remains for the integrator")
]

/--
M0387-level local leaf ledger for the THM-M-0388 Pell path.

Each entry records `(leaf id, package id, local witness, step budget, gate state)`.
The budgets are deliberately conservative because each proof leaf is an `exact`,
`simpa`, constructor/projection bridge, or data-only audit row backed by pinned
mathlib.
-/
def publicLeafBudgetLedger : List (String × String × String × Nat × String) := [
  ("PELL-L001", "PP-A", "PellEquation", 20,
    "closed: normalized raw equation definition"),
  ("PELL-L002", "PP-A", "NontrivialIntegerSolutionExists", 20,
    "closed: normalized raw nontrivial existence predicate"),
  ("PELL-L003", "PP-A", "candidateA_nontrivial_integer_solution", 15,
    "closed: wrapper for Pell.exists_of_not_isSquare"),
  ("PELL-L004", "PP-A", "source_raw_integer_existence_of_not_isSquare", 15,
    "closed: source-facing raw integer theorem alias"),
  ("PELL-L005", "PP-B", "PositiveStructuredSolutionExists", 20,
    "closed: normalized structured-solution predicate"),
  ("PELL-L006", "PP-B", "candidateB_positive_structured_solution", 15,
    "closed: wrapper for Pell.Solution₁.exists_pos_of_not_isSquare"),
  ("PELL-L007", "PP-C", "PositiveGeneratorClassifiesAllSolutions", 30,
    "closed: normalized unique positive generator predicate"),
  ("PELL-L008", "PP-C", "candidateC_positive_generator_classification", 20,
    "closed: wrapper for Pell.existsUnique_pos_generator"),
  ("PELL-L009", "PP-C", "statementShape_mathlib_closure", 30,
    "closed: combines raw existence and generator classification"),
  ("PELL-L010", "PP-D", "structured_solution_coordinates_satisfy_equation", 20,
    "closed: projection bridge from Pell.Solution₁.prop"),
  ("PELL-L011", "PP-D", "mk_solution_x", 20,
    "closed: constructor projection for x-coordinate"),
  ("PELL-L012", "PP-D", "mk_solution_y", 20,
    "closed: constructor projection for y-coordinate"),
  ("PELL-L013", "PP-E", "theoremLevelAuditRows", 40,
    "closed: public theorem-level audit table data"),
  ("PELL-L014", "PP-E", "firstProofPackageQueue", 40,
    "closed: theorem-tree package split data"),
  ("PELL-L015", "PP-E", "m0387CompletionGateRows", 40,
    "closed: local completion-gate data; shared docs still require serial integrator backfill")
]

/-- M0387-level completion-gate audit for this repo-local Pell wrapper surface. -/
def m0387CompletionGateRows : List (String × String × String) := [
  ("machine theorem/module anchor",
    "satisfied",
    "Mathlib.NumberTheory.Pell imported and checked through local wrappers"),
  ("repo-local validation",
    "satisfied",
    "lake env lean AwesomeTheorems/Stage1/S1_M_003.lean passes"),
  ("repo-local integration debt",
    "satisfied",
    "local_wrapper_upstream_mathlib; no anchor-only completed claim"),
  ("public proof-process merge",
    "pending serial integration",
    "worker ledger supplies exact backfill text without editing shared docs"),
  ("<=100 proof-package ledger",
    "satisfied locally; pending serial public-doc integration",
    "publicLeafBudgetLedger records all local leaves with budgets <= 100")
]

#check statementShape_mathlib_closure
#check candidateA_nontrivial_integer_solution
#check candidateB_positive_structured_solution
#check candidateC_positive_generator_classification
#check raw_integer_existence_of_positive_nonsquare
#check source_raw_integer_existence_of_not_isSquare

end AwesomeTheorems.NumberTheory.THM_M_0388.PellPath
