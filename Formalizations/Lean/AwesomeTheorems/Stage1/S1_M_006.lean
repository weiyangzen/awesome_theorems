import Mathlib.Data.Set.Finite.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.MvPolynomial.Eval
import Mathlib.Algebra.Polynomial.Basic

/-!
# S1-M-006 / THM-M-0393: Thue's theorem, Stage1 statement boundary

This file records a conservative Lean 4 statement shape for the Thue equation
finiteness theorem: an irreducible integral binary form of degree at least three
has only finitely many integral solution pairs for any fixed right-hand side.

The current artifact is not a proof of Thue's theorem.  It keeps the
irreducibility and primitive-integral-form hypotheses as explicit audit
predicates until a later integrator chooses a concrete `Polynomial` /
`MvPolynomial` object model or pins an external Lean 4 proof package.
-/

noncomputable section

open scoped BigOperators

namespace AwesomeTheorems.Stage1.S1_M_006

/-- Audit identifier for the source theorem. -/
def theoremUID : String := "THM-M-0393"

/-- Current machine-proof debt classification for this Stage1 artifact. -/
def machineProofDebt : String := "formalization_debt"

/--
The Stage0/source row records this theorem as verified, but that status is not
repo-local Lean 4 proof closure.
-/
def sourceRowVerificationStatus : String := "source_row_verified"

/--
Public Stage1 status note: THM-M-0393 remains open in Lean 4 until the theorem
is either proved locally or an external Lean 4 proof is pinned, imported, and
checked by this repository.
-/
def stage1Lean4StatusNote : String :=
  "open_in_lean4_despite_source_row_verified"

/--
This artifact does not retain repo-local integration debt: no external Lean 4
closure was found and imported, so the remaining debt is formalization debt.
-/
def repoLocalIntegrationDebtRetained : Bool := false

/--
An integral binary form represented by its total degree and homogeneous
coefficient vector.

`coeff i` is the coefficient of `X^i Y^(degree - i)`.
-/
structure BinaryForm where
  degree : Nat
  coeff : Fin (degree + 1) → Int

/-- Evaluate an integral homogeneous binary form at an integer pair. -/
def BinaryForm.eval (F : BinaryForm) (x y : Int) : Int :=
  ∑ i : Fin (F.degree + 1), F.coeff i * x ^ (i : Nat) * y ^ (F.degree - (i : Nat))

/--
Stage1 input data for Thue's theorem.

The proposition fields are intentionally explicit boundaries.  A terminal proof
must replace them with the chosen mathlib predicates for primitive integral
binary forms and irreducibility over `ℚ`.
-/
structure ThueInput where
  form : BinaryForm
  target : Int
  primitiveIntegralBinaryForm : Prop
  irreducibleOverRat : Prop

/-- Integral solution pairs of the Thue equation `F(x,y) = m`. -/
def solutionSet (D : ThueInput) : Set (Int × Int) :=
  {p | D.form.eval p.1 p.2 = D.target}

/-- The finiteness conclusion expected from Thue's theorem. -/
def ThueConclusion (D : ThueInput) : Prop :=
  (solutionSet D).Finite

/--
Stage1 normalized statement-shape candidate for Thue's theorem.

For every primitive integral binary form of degree at least three, irreducible
over `ℚ`, the integer solutions of `F(x,y)=m` form a finite set.
-/
def StatementShape : Prop :=
  ∀ D : ThueInput,
    3 ≤ D.form.degree →
      D.primitiveIntegralBinaryForm →
        D.irreducibleOverRat →
          ThueConclusion D

/--
Statement normalization decision for this child pass.

The canonical Stage1 target keeps `target : Int` unrestricted.  This covers the
usual nonzero-right-hand-side Thue equation and leaves the zero-right-hand-side
case as a branch package, rather than creating a second root theorem.
-/
def statementTargetDecision : List String := [
  "canonical target: one StatementShape with arbitrary target : Int",
  "nonzero RHS classical Thue equation is a branch of the same target",
  "zero RHS is retained as a branch package, not a competing root theorem",
  "primitive and irreducible hypotheses remain explicit predicates until object-model integration"
]

/-- Machine-side audit result for the pinned local mathlib snapshot. -/
def mathlibAnchorAudit : List String := [
  "local rg audit found no declaration named Thue or ThueEquation in the pinned mathlib snapshot",
  "Mathlib.NumberTheory.DiophantineApproximation.Basic exists as approximation substrate",
  "Mathlib.NumberTheory.Transcendental.Liouville.LiouvilleWith exists as Liouville/Roth substrate",
  "Mathlib.NumberTheory.SiegelsLemma exists as an auxiliary linear-algebra substrate",
  "Mathlib.Combinatorics.Additive.Corner.Roth is an additive-combinatorics theorem and not the number-theoretic Roth/Thue terminal theorem"
]

/--
Repeated external Lean 4 anchor audit for `S1-M-006-A07`, run before any
status upgrade.

The audit records search surfaces only.  It does not create proof closure for
`StatementShape`.
-/
def externalLean4AnchorAudit_2026_05_01 : List String := [
  "pinned local mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95: rg found no Thue or ThueEquation declaration/module",
  "current mathlib4 HEAD 49f10344339f99fda2d3bb0aa1455bfa6801fd93: Mathlib.lean has no Thue import; DiophantineApproximation and Liouville modules remain support substrate",
  "Loogle query for declaration names containing \"Thue\" returned zero hits",
  "Loogle query for declaration names containing \"ThueEquation\" returned zero hits",
  "GitHub repository search for exact Thue equation/theorem Lean targets returned no candidate repository",
  "GitHub repository search for \"Thue\" and Lean returned only a Thue-Morse sequence repository, not Thue equation finiteness",
  "manual inspection of suzukikakuritsu-arch/externals at b099aafedf9e70ef9e2b5e12e5546b486c3b06b2 found no Thue/Pillai/Roth/Diophantine approximation Lean file or theorem",
  "GitHub unauthenticated code search was rate-limited, so this pass cannot claim exhaustive code-search coverage",
  "no external Lean 4 proof was found that can be pinned, imported, and checked for StatementShape",
  "A08 is not activated by this pass: there is no concrete external theorem URL/module/name requiring pin/import/check"
]

/--
`S1-M-006-A08` pin/import/check decision for the current child pass.

Since the repeated A07 audit found no external Lean 4 proof of Thue-equation
finiteness, this file must not invent a fake dependency task.  The gate records
the concrete fields that become mandatory if a later primary-source audit finds
an external proof candidate.
-/
def a08ExternalProofIntegrationGate : List String := [
  "A08 status on 2026-05-01: no external Lean 4 proof candidate is available",
  "no pin/import/check task is created because no project URL, commit, module, theorem name, or proof body was found",
  "if a candidate is later found, record project URL, license, commit, module path, theorem name, Lean toolchain, Lake dependency feasibility, and proof-axiom audit",
  "then either pin/import/check the candidate in this repository or record a concrete integration blocker such as toolchain mismatch, dependency conflict, license barrier, missing theorem endpoint, or axioms/sorryAx in the closure",
  "keep THM-M-0393 and S1-M-006-A08 open until repo-local validation passes; anchor-only evidence is not a completed state",
  "current machine status remains not_repo_local_closed with formalization_debt, not completed repo_local_integration_debt"
]

/-- No external proof was available in this child pass, so no A08 task was opened. -/
def a08PinImportCheckTaskCreated : Bool := false

/--
Exact mathlib support modules checked by the Stage1 ledger for this theorem.

These are support anchors only.  The audit found no terminal theorem proving
Thue-equation finiteness or Thue/Roth approximation in the pinned snapshot.
-/
def mathlibSupportModulesChecked : List String := [
  "Mathlib.NumberTheory.DiophantineApproximation.Basic",
  "Mathlib.NumberTheory.Transcendental.Liouville.LiouvilleWith",
  "Mathlib.NumberTheory.Height.MvPolynomial",
  "Mathlib.NumberTheory.Height.Northcott",
  "Mathlib.Algebra.MvPolynomial.Equiv",
  "Mathlib.Algebra.MvPolynomial.Polynomial",
  "Mathlib.RingTheory.Polynomial.Resultant.Basic",
  "Mathlib.NumberTheory.NumberField.Basic",
  "Mathlib.NumberTheory.NumberField.CanonicalEmbedding.Basic",
  "Mathlib.NumberTheory.NumberField.ClassNumber",
  "Mathlib.NumberTheory.NumberField.FinitePlaces",
  "Mathlib.NumberTheory.NumberField.FractionalIdeal",
  "Mathlib.NumberTheory.NumberField.InfinitePlace.Basic",
  "Mathlib.NumberTheory.NumberField.ProductFormula",
  "Mathlib.NumberTheory.NumberField.Units.Basic",
  "Mathlib.RingTheory.ClassGroup",
  "Mathlib.RingTheory.DedekindDomain.Basic",
  "Mathlib.RingTheory.DedekindDomain.Factorization",
  "Mathlib.RingTheory.DedekindDomain.FiniteAdeleRing",
  "Mathlib.RingTheory.DedekindDomain.Ideal.Basic",
  "Mathlib.RingTheory.DedekindDomain.IntegralClosure",
  "Mathlib.RingTheory.DedekindDomain.SInteger"
]

/--
Exact support declaration names recorded by the Stage1 mathlib-anchor audit.

The names below are useful substrate declarations.  None is recorded as a
terminal Thue theorem or as proof closure for `StatementShape`.
-/
def mathlibSupportDeclarationsChecked : List String := [
  "Real.Dirichlet.exists_int_int_abs_mul_sub_le",
  "Real.Dirichlet.exists_nat_abs_mul_sub_round_le",
  "Real.Dirichlet.exists_rat_abs_sub_le_and_den_le",
  "Real.ContfracLegendre.Ass",
  "Real.exists_rat_eq_convergent'",
  "LiouvilleWith",
  "LiouvilleWith.exists_pos",
  "LiouvilleWith.mono",
  "LiouvilleWith.frequently_lt_rpow_neg",
  "Height.Northcott",
  "Height.Northcott.exists_min_image",
  "Height.mulHeight_eval_le",
  "Height.mulHeight_eval_le'",
  "Height.logHeight_eval_le",
  "Height.logHeight_eval_le'",
  "Height.mulHeight_eval_ge",
  "Height.mulHeight_eval_ge'",
  "Height.logHeight_eval_ge",
  "Height.logHeight_eval_ge'",
  "MvPolynomial.finSuccEquiv",
  "MvPolynomial.eval_polynomial_eval_finSuccEquiv",
  "Polynomial.resultant",
  "Polynomial.discr",
  "Polynomial.resultant_eq_prod_roots_sub",
  "Polynomial.resultant_eq_prod_eval",
  "Polynomial.resultant_eq_zero_iff"
]

/-! ## Checked dehomogenization probe for the future `MvPolynomial` object model. -/

/--
The affine variable image used to dehomogenize an integral binary form.

The convention is `X₀ ↦ X` and `X₁ ↦ 1`, so a homogeneous binary form
`F(X₀, X₁)` is sent to the univariate rational polynomial `F(X, 1)`.
-/
def dehomogenizationVariable (i : Fin 2) : Polynomial Rat :=
  if i = (0 : Fin 2) then Polynomial.X else 1

/--
Dehomogenization as an algebra homomorphism from integral bivariate
`MvPolynomial`s to univariate rational polynomials.

This is only the object-model bridge for the later Thue proof route; it does
not assert homogeneity, irreducibility, or any finiteness theorem.
-/
def dehomogenizationMap : MvPolynomial (Fin 2) Int →ₐ[Int] Polynomial Rat :=
  MvPolynomial.aeval dehomogenizationVariable

/-- Dehomogenize an integral binary `MvPolynomial` by evaluating `X₁ = 1`. -/
def dehomogenize (F : MvPolynomial (Fin 2) Int) : Polynomial Rat :=
  dehomogenizationMap F

/-- Constants dehomogenize to rational constant polynomials. -/
theorem dehomogenize_C (z : Int) :
    dehomogenize (MvPolynomial.C z) = Polynomial.C (z : Rat) := by
  simp [dehomogenize, dehomogenizationMap]

/-- The first binary-form coordinate becomes the univariate polynomial variable. -/
theorem dehomogenize_X_zero :
    dehomogenize (MvPolynomial.X (0 : Fin 2) : MvPolynomial (Fin 2) Int) =
      Polynomial.X := by
  simp [dehomogenize, dehomogenizationMap, dehomogenizationVariable]

/-- The second binary-form coordinate is set to one. -/
theorem dehomogenize_X_one :
    dehomogenize (MvPolynomial.X (1 : Fin 2) : MvPolynomial (Fin 2) Int) =
      1 := by
  simp [dehomogenize, dehomogenizationMap, dehomogenizationVariable]

/-- A checked linear sanity test: `X₀ + X₁` dehomogenizes to `X + 1`. -/
theorem dehomogenize_X_zero_add_X_one :
    dehomogenize
        ((MvPolynomial.X (0 : Fin 2) + MvPolynomial.X (1 : Fin 2)) :
          MvPolynomial (Fin 2) Int) =
      Polynomial.X + 1 := by
  simp [dehomogenize, dehomogenizationMap, dehomogenizationVariable]

/--
One package in the M0387-style proof-tree frontier.

`repoLocalClosed = false` is intentional for every package in this child pass:
the file records a checked package ledger, not a completed proof of Thue's
theorem.
-/
structure ProofPackage where
  code : String
  title : String
  repoLocalClosed : Bool
  debt : String
  nextGate : String
deriving DecidableEq, Repr

/-- Algebraic-number-theory package split for the Thue theorem proof route. -/
def proofPackageLedger : List ProofPackage := [
  {
    code := "T00",
    title := "statement and binary-form object model",
    repoLocalClosed := false,
    debt := "formalization_debt",
    nextGate := "freeze MvPolynomial/Polynomial model and prove equivalence with BinaryForm"
  },
  {
    code := "T01",
    title := "primitive normalization and zero/nonzero RHS branch split",
    repoLocalClosed := false,
    debt := "formalization_debt",
    nextGate := "prove primitive scaling lemmas and isolate the target = 0 branch"
  },
  {
    code := "T02",
    title := "dehomogenization and algebraic root package",
    repoLocalClosed := false,
    debt := "formalization_debt",
    nextGate := "construct the dehomogenized polynomial over Q and attach an algebraic root"
  },
  {
    code := "T03",
    title := "number-field embedding and norm-form bridge",
    repoLocalClosed := false,
    debt := "formalization_debt",
    nextGate := "move between binary-form values and algebraic norm expressions in a chosen number field"
  },
  {
    code := "T04",
    title := "ideal factorization, valuations, and coprime denominator controls",
    repoLocalClosed := false,
    debt := "formalization_debt",
    nextGate := "split prime ideal and valuation obligations into <=100-step local leaves"
  },
  {
    code := "T05",
    title := "height estimates and rational approximation extraction",
    repoLocalClosed := false,
    debt := "formalization_debt",
    nextGate := "derive a rational approximation to an algebraic root from a sufficiently large solution"
  },
  {
    code := "T06",
    title := "terminal Thue/Roth approximation theorem dependency",
    repoLocalClosed := false,
    debt := "formalization_debt",
    nextGate := "supply a local proof body or pin/import/check an external Lean 4 approximation theorem"
  },
  {
    code := "T07",
    title := "bounded-height exceptional search and finite-set extraction",
    repoLocalClosed := false,
    debt := "formalization_debt",
    nextGate := "convert approximation bounds into a finite set of integer solution pairs"
  },
  {
    code := "T08",
    title := "repo-local closure and public completion gate",
    repoLocalClosed := false,
    debt := "formalization_debt",
    nextGate := "run lake validation after either local_proof_body, local_wrapper_upstream_mathlib, or external_upstream_pinned closure"
  }
]

/-- The child pass records exactly the public `T00` through `T08` package split. -/
theorem proofPackageLedger_length : proofPackageLedger.length = 9 :=
  rfl

/-- No package in this ledger is claimed as repo-local theorem closure. -/
theorem proofPackageLedger_no_repoLocalClosed_claim :
    proofPackageLedger.map ProofPackage.repoLocalClosed =
      [false, false, false, false, false, false, false, false, false] :=
  rfl

/--
One public proof-tree checklist row for the `T00` through `T08` split.

The checklist records package-level proof obligations only.  `leafBudgetClosed`
is false throughout this pass because no package has yet been refined to a
repo-local `<=100` step leaf ledger and no terminal theorem proof has been
checked.
-/
structure ProofTreeChecklistItem where
  code : String
  parent : String
  upstreamInputs : List String
  outputInterface : String
  proofStatus : String
  leafBudgetClosed : Bool
deriving DecidableEq, Repr

/--
M0387-style proof-tree checklist for Thue's theorem.

Every row is deliberately `unchecked`: this is an integration-ready package
split, not a local proof of `StatementShape`.
-/
def proofTreeChecklist : List ProofTreeChecklistItem := [
  {
    code := "T00",
    parent := "StatementShape",
    upstreamInputs := [
      "primitive integral binary form data",
      "degree >= 3",
      "irreducibility over Q",
      "fixed target integer"
    ],
    outputInterface := "canonical Lean object model and theorem statement boundary",
    proofStatus := "unchecked_formalization_debt",
    leafBudgetClosed := false
  },
  {
    code := "T01",
    parent := "T00",
    upstreamInputs := [
      "chosen binary-form object model",
      "integer target",
      "content/primitive normalization data"
    ],
    outputInterface := "primitive normalization plus zero/nonzero RHS branch obligations",
    proofStatus := "unchecked_formalization_debt",
    leafBudgetClosed := false
  },
  {
    code := "T02",
    parent := "T01",
    upstreamInputs := [
      "normalized binary form",
      "dehomogenization map F(X,Y) -> F(X,1)",
      "irreducibility bridge to Q[X]"
    ],
    outputInterface := "algebraic root package for the dehomogenized polynomial",
    proofStatus := "unchecked_formalization_debt",
    leafBudgetClosed := false
  },
  {
    code := "T03",
    parent := "T02",
    upstreamInputs := [
      "algebraic root",
      "number field generated by the root",
      "integer solution pair"
    ],
    outputInterface := "norm-form bridge relating F(x,y) to a number-field norm",
    proofStatus := "unchecked_formalization_debt",
    leafBudgetClosed := false
  },
  {
    code := "T04",
    parent := "T03",
    upstreamInputs := [
      "norm-form identity",
      "prime ideal factorization data",
      "coprimality and denominator controls"
    ],
    outputInterface := "valuation and ideal-factor constraints for solution pairs",
    proofStatus := "unchecked_formalization_debt",
    leafBudgetClosed := false
  },
  {
    code := "T05",
    parent := "T04",
    upstreamInputs := [
      "valuation constraints",
      "archimedean/nonarchimedean height bounds",
      "large-solution hypothesis"
    ],
    outputInterface := "rational approximation to an algebraic root",
    proofStatus := "unchecked_formalization_debt",
    leafBudgetClosed := false
  },
  {
    code := "T06",
    parent := "T05",
    upstreamInputs := [
      "algebraic irrational root",
      "rational approximation sequence",
      "height/denominator estimates"
    ],
    outputInterface := "terminal Thue/Roth approximation contradiction or imported equivalent",
    proofStatus := "unchecked_formalization_debt_blocked_on_terminal_theorem",
    leafBudgetClosed := false
  },
  {
    code := "T07",
    parent := "T06",
    upstreamInputs := [
      "terminal approximation bound",
      "bounded-height residue cases",
      "finite search domain"
    ],
    outputInterface := "finite exceptional set containing all integer solutions",
    proofStatus := "unchecked_formalization_debt",
    leafBudgetClosed := false
  },
  {
    code := "T08",
    parent := "T07",
    upstreamInputs := [
      "finite exceptional set",
      "solution-set containment proof",
      "repo-local proof/dependency closure evidence"
    ],
    outputInterface := "validated repo-local proof of StatementShape or explicit blocker",
    proofStatus := "unchecked_not_repo_local_closed",
    leafBudgetClosed := false
  }
]

/-- The proof-tree checklist has exactly the `T00` through `T08` package rows. -/
theorem proofTreeChecklist_length : proofTreeChecklist.length = 9 :=
  rfl

/-- No proof-tree package has an independent `<=100` leaf ledger in this pass. -/
theorem proofTreeChecklist_no_leafBudgetClosed_claim :
    proofTreeChecklist.map ProofTreeChecklistItem.leafBudgetClosed =
      [false, false, false, false, false, false, false, false, false] :=
  rfl

/-- The checklist package codes are the public `T00` through `T08` split. -/
theorem proofTreeChecklist_codes :
    proofTreeChecklist.map ProofTreeChecklistItem.code =
      ["T00", "T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08"] :=
  rfl

/--
One local leaf in the `<=100` M0387 budget ledger.

The rows are integration-ready planning records only.  They are deliberately
not theorem-proof closures and should not be used to mark any package closed.
-/
structure LeafBudgetItem where
  code : String
  package : String
  task : String
  status : String
deriving DecidableEq, Repr

/--
Unchecked `<=100` local leaf ledger for the Thue theorem proof route.

The ledger has 60 rows, so it satisfies the M0387 local leaf-count budget for a
public backfill proposal.  All rows remain `unchecked`; a later pass must
replace each row with concrete Lean theorem/proof work before any package can
be promoted.
-/
def leafBudgetLedger : List LeafBudgetItem := [
  { code := "M0393-L001", package := "T00", task := "define BinaryForm := MvPolynomial (Fin 2) Int", status := "unchecked" },
  { code := "M0393-L002", package := "T00", task := "define evalBinaryForm F x y", status := "unchecked" },
  { code := "M0393-L003", package := "T00", task := "define ThueSolutions F m", status := "unchecked" },
  { code := "M0393-L004", package := "T00", task := "choose exact RHS policy: require m != 0 or split m = 0", status := "unchecked" },
  { code := "M0393-L005", package := "T00", task := "choose irreducibility predicate over Rat", status := "unchecked" },
  { code := "M0393-L006", package := "T00", task := "state StatementShape : Prop without proof claim", status := "unchecked" },
  { code := "M0393-L007", package := "T01", task := "map F : MvPolynomial (Fin 2) Int to coefficients in Rat", status := "unchecked" },
  { code := "M0393-L008", package := "T01", task := "define dehomogenization F(T,1)", status := "unchecked" },
  { code := "M0393-L009", package := "T01", task := "prove finSuccEquiv evaluation identity for the chosen variables", status := "unchecked" },
  { code := "M0393-L010", package := "T01", task := "prove F(x,y) = y^n * f(x/y) for y != 0", status := "unchecked" },
  { code := "M0393-L011", package := "T01", task := "connect integer evaluation with rational evaluation by denominator clearing", status := "unchecked" },
  { code := "M0393-L012", package := "T01", task := "package roots of f over Complex or a splitting field", status := "unchecked" },
  { code := "M0393-L013", package := "T02", task := "derive support criterion from F.IsHomogeneous n", status := "unchecked" },
  { code := "M0393-L014", package := "T02", task := "prove binary scaling F(a*x,a*y)=a^n*F(x,y)", status := "unchecked" },
  { code := "M0393-L015", package := "T02", task := "prove sign-scaling variants", status := "unchecked" },
  { code := "M0393-L016", package := "T02", task := "isolate y = 0 solution branch", status := "unchecked" },
  { code := "M0393-L017", package := "T02", task := "prove finite y = 0 branch under leading coefficient condition", status := "unchecked" },
  { code := "M0393-L018", package := "T02", task := "isolate x = 0 solution branch", status := "unchecked" },
  { code := "M0393-L019", package := "T02", task := "primitive reduction for coprime (x,y)", status := "unchecked" },
  { code := "M0393-L020", package := "T02", task := "reconstruct all solutions from primitive solutions and divisors of m", status := "unchecked" },
  { code := "M0393-L021", package := "T03", task := "define dehomogenized irreducibility over Rat", status := "unchecked" },
  { code := "M0393-L022", package := "T03", task := "relate binary-form irreducibility to dehomogenized irreducibility", status := "unchecked" },
  { code := "M0393-L023", package := "T03", task := "prove dehomogenized degree equals n under leading coefficient condition", status := "unchecked" },
  { code := "M0393-L024", package := "T03", task := "handle root-at-infinity branch", status := "unchecked" },
  { code := "M0393-L025", package := "T03", task := "prove separability over characteristic zero", status := "unchecked" },
  { code := "M0393-L026", package := "T03", task := "prove distinct-root product identity", status := "unchecked" },
  { code := "M0393-L027", package := "T03", task := "connect nonzero discriminant and no repeated roots", status := "unchecked" },
  { code := "M0393-L028", package := "T03", task := "select nearest complex or real root to x/y", status := "unchecked" },
  { code := "M0393-L029", package := "T04", task := "state Thue approximation theorem for algebraic real roots", status := "unchecked" },
  { code := "M0393-L030", package := "T04", task := "encode algebraic degree >= 3 for the root", status := "unchecked" },
  { code := "M0393-L031", package := "T04", task := "encode finite exceptional rational approximants", status := "unchecked" },
  { code := "M0393-L032", package := "T04", task := "bridge coprime integer pairs to rational denominators", status := "unchecked" },
  { code := "M0393-L033", package := "T04", task := "choose the exponent variant needed by the equation proof", status := "unchecked" },
  { code := "M0393-L034", package := "T04", task := "audit whether Roth theorem would close the needed input", status := "unchecked" },
  { code := "M0393-L035", package := "T04", task := "prove/import terminal approximation theorem", status := "blocked_unchecked" },
  { code := "M0393-L036", package := "T05", task := "prove product formula f(t)=c*prod(t-alpha_i) in the chosen field", status := "unchecked" },
  { code := "M0393-L037", package := "T05", task := "derive upper bound for |f(x/y)| from F(x,y)=m", status := "unchecked" },
  { code := "M0393-L038", package := "T05", task := "convert upper bound into product of root distances", status := "unchecked" },
  { code := "M0393-L039", package := "T05", task := "bound non-nearest root distances away from zero for large |y|", status := "unchecked" },
  { code := "M0393-L040", package := "T05", task := "derive nearest-root approximation inequality", status := "unchecked" },
  { code := "M0393-L041", package := "T05", task := "prove nearest root satisfies algebraic degree hypothesis", status := "unchecked" },
  { code := "M0393-L042", package := "T05", task := "handle real-root requirement for the approximation theorem", status := "unchecked" },
  { code := "M0393-L043", package := "T05", task := "split no-real-root cases if needed", status := "unchecked" },
  { code := "M0393-L044", package := "T06", task := "prove finite set for |y| <= B", status := "unchecked" },
  { code := "M0393-L045", package := "T06", task := "package finite integer interval API", status := "unchecked" },
  { code := "M0393-L046", package := "T06", task := "show bounded denominator gives finitely many numerators", status := "unchecked" },
  { code := "M0393-L047", package := "T06", task := "close y = 0 finite branch", status := "unchecked" },
  { code := "M0393-L048", package := "T06", task := "close or exclude m = 0 branch", status := "unchecked" },
  { code := "M0393-L049", package := "T06", task := "convert finite rational approximants to finite integer pairs", status := "unchecked" },
  { code := "M0393-L050", package := "T06", task := "prove finite union over roots and exceptional sets", status := "unchecked" },
  { code := "M0393-L051", package := "T07", task := "assemble small-denominator branch", status := "unchecked" },
  { code := "M0393-L052", package := "T07", task := "assemble large-denominator contradiction branch", status := "unchecked" },
  { code := "M0393-L053", package := "T07", task := "assemble primitive branch finiteness", status := "unchecked" },
  { code := "M0393-L054", package := "T07", task := "lift primitive finiteness to all integer pairs", status := "unchecked" },
  { code := "M0393-L055", package := "T07", task := "prove final Set.Finite for ThueSolutions", status := "unchecked" },
  { code := "M0393-L056", package := "T08", task := "add private statement-only Lean wrapper in later integrator pass", status := "unchecked" },
  { code := "M0393-L057", package := "T08", task := "add local import/build target for wrapper in later integrator pass", status := "unchecked" },
  { code := "M0393-L058", package := "T08", task := "record exact mathlib revision in public Stage1 backfill", status := "unchecked" },
  { code := "M0393-L059", package := "T08", task := "repeat external Lean search before any completion claim", status := "unchecked" },
  { code := "M0393-L060", package := "T08", task := "pin/import/check external theorem if found", status := "unchecked" }
]

/-- The integration-ready leaf ledger has 60 local leaves. -/
theorem leafBudgetLedger_length : leafBudgetLedger.length = 60 :=
  rfl

/-- The local leaf ledger satisfies the M0387 `<=100` leaf-count budget. -/
theorem leafBudgetLedger_length_le_100 : leafBudgetLedger.length ≤ 100 := by
  decide

def leafBudgetLedgerCompletionStatus : String :=
  "60 unchecked leaves recorded; count gate passes but no theorem/proof package is closed"

/--
Repo-local integration-debt gate for this Stage1 slot.

No external Lean 4 proof of Thue's theorem has been pinned, imported, and
checked by this repository.  The current state is therefore open
`formalization_debt`, not a completed theorem with retained
`repo_local_integration_debt`.
-/
def repoLocalIntegrationDebtGate : List String := [
  "no local proof body for StatementShape exists in this module",
  "no terminal Thue theorem was found in the pinned local mathlib snapshot",
  "no external Lean 4 Thue proof has been pinned/imported/checked in this repository",
  "completion remains blocked until local_proof_body, local_wrapper_upstream_mathlib, or external_upstream_pinned validation passes"
]

/--
Public blocker for the missing terminal Thue/Roth approximation theorem.

This is the Stage1 `S1-M-006-A06` payload.  It is intentionally a blocker
record rather than a theorem statement: the approximation input still needs a
local proof body, a mathlib wrapper, or a pinned external proof before
`StatementShape` can be promoted.
-/
def terminalThueRothApproximationBlocker : List String := [
  "public blocker: T06 is missing a terminal Lean 4 Thue/Roth approximation theorem",
  "checked support is substrate only: DiophantineApproximation.Basic and LiouvilleWith do not prove the needed terminal theorem",
  "Mathlib.Combinatorics.Additive.Corner.Roth is a length-three arithmetic-progression theorem, not number-theoretic Roth approximation",
  "Thue-equation finiteness cannot be claimed until the approximation terminal theorem is proved locally or pin/import/check succeeds",
  "if a future external Lean 4 proof is found, keep this item open until it enters repo-local validation closure or a concrete integration blocker is recorded"
]

/-- Integration-ready public note for a later serial docs integrator. -/
def publicBackfillProposal : List String := [
  "THM-M-0393 / S1-M-006 is open in Lean 4 despite the source row saying verified.",
  "Canonical Lean target: AwesomeTheorems.Stage1.S1_M_006.StatementShape, an unrestricted target : Int finiteness theorem for primitive irreducible integral binary forms of degree at least three.",
  "Use one root theorem with target : Int; treat nonzero RHS and zero RHS as branch packages rather than separate competing root statements.",
  "A checked dehomogenization bridge now exists as AwesomeTheorems.Stage1.S1_M_006.dehomogenize : MvPolynomial (Fin 2) Int -> Polynomial Rat, with X0 mapped to Polynomial.X and X1 mapped to 1.",
  "Pinned local mathlib audit found no terminal Thue/ThueEquation theorem; support modules checked are recorded in mathlibSupportModulesChecked and support declaration names in mathlibSupportDeclarationsChecked.",
  "Public blocker S1-M-006-A06: no terminal Lean 4 Thue/Roth approximation theorem is available in the repo-local validation closure; DiophantineApproximation.Basic and LiouvilleWith are substrate only, and combinatorial Roth is not the number-theoretic theorem.",
  "Repeated A07 external Lean 4 anchor audit on 2026-05-01 found no pin-ready GitHub/mathlib proof of Thue-equation finiteness; externalLean4AnchorAudit_2026_05_01 records the exact search-surface result.",
  "A08 pin/import/check gate: no external proof candidate is available, so no fake dependency task is created; if one is later found, record URL/license/commit/module/theorem/toolchain/Lake feasibility/proof-axiom audit, then pin/import/check or record a concrete blocker while keeping the item open.",
  "Proof packages T00 through T08 are recorded in proofPackageLedger; the explicit proof-tree checklist is proofTreeChecklist, whose rows remain unchecked and whose <=100 leaf-budget gates are not closed.",
  "The integration-ready <=100 leaf ledger is leafBudgetLedger: 60 unchecked leaves, with leafBudgetLedger_length and leafBudgetLedger_length_le_100 checked locally; this is a public backfill proposal only until serial integrator review.",
  "No completed state may be claimed until a local proof body, a mathlib wrapper, or a pinned external dependency proves StatementShape and lake validation passes."
]

/-- Membership in the solution set unfolds to the defining equation. -/
theorem mem_solutionSet_iff (D : ThueInput) (p : Int × Int) :
    p ∈ solutionSet D ↔ D.form.eval p.1 p.2 = D.target :=
  Iff.rfl

/-- The statement shape unfolds to the expected quantified finiteness theorem. -/
theorem statementShape_iff :
    StatementShape ↔
      ∀ D : ThueInput,
        3 ≤ D.form.degree →
          D.primitiveIntegralBinaryForm →
            D.irreducibleOverRat →
              (solutionSet D).Finite :=
  Iff.rfl

/--
Checked reduced case: if the equation has no integer solutions by hypothesis,
then its solution set is finite.

This is a sanity wrapper around `Set.finite_empty`; it is not a proof of
Thue's theorem.
-/
theorem finite_of_no_integer_solutions
    (D : ThueInput) (h : ∀ x y : Int, D.form.eval x y ≠ D.target) :
    ThueConclusion D := by
  have h_empty : solutionSet D = ∅ := by
    ext p
    simp [solutionSet, h p.1 p.2]
  simp [ThueConclusion, h_empty]

/-- A `ThueConclusion` is exactly finiteness of the solution set. -/
theorem thueConclusion_iff (D : ThueInput) :
    ThueConclusion D ↔ (solutionSet D).Finite :=
  Iff.rfl

/-! ## Audit probes retained in the checked file. -/

#check Set.Finite
#check Set.finite_empty
#check BinaryForm.eval
#check solutionSet
#check StatementShape
#check sourceRowVerificationStatus
#check stage1Lean4StatusNote
#check statementTargetDecision
#check mathlibAnchorAudit
#check externalLean4AnchorAudit_2026_05_01
#check a08ExternalProofIntegrationGate
#check a08PinImportCheckTaskCreated
#check mathlibSupportModulesChecked
#check mathlibSupportDeclarationsChecked
#check dehomogenizationVariable
#check dehomogenizationMap
#check dehomogenize
#check dehomogenize_C
#check dehomogenize_X_zero
#check dehomogenize_X_one
#check dehomogenize_X_zero_add_X_one
#check ProofPackage
#check proofPackageLedger
#check proofPackageLedger_length
#check proofPackageLedger_no_repoLocalClosed_claim
#check ProofTreeChecklistItem
#check proofTreeChecklist
#check proofTreeChecklist_length
#check proofTreeChecklist_no_leafBudgetClosed_claim
#check proofTreeChecklist_codes
#check LeafBudgetItem
#check leafBudgetLedger
#check leafBudgetLedger_length
#check leafBudgetLedger_length_le_100
#check leafBudgetLedgerCompletionStatus
#check repoLocalIntegrationDebtGate
#check terminalThueRothApproximationBlocker
#check publicBackfillProposal

end AwesomeTheorems.Stage1.S1_M_006

/-!
## Public Stage1 theorem-name wrapper

The public blueprint asks for the theorem-UID namespace
`Stage1.THMM0393.StatementShape`.  This wrapper keeps the already checked
`S1_M_006` statement as the canonical payload while freezing the current
hypothesis package as one explicit predicate.
-/

namespace Stage1.THMM0393

abbrev ThueInput := AwesomeTheorems.Stage1.S1_M_006.ThueInput

abbrev ThueConclusion := AwesomeTheorems.Stage1.S1_M_006.ThueConclusion

/--
Frozen Stage1 hypothesis predicate for THM-M-0393.

The current boundary uses explicit proposition fields for primitive integral
binary forms and irreducibility over `ℚ`; later object-model work may replace
those fields with concrete mathlib predicates, but this wrapper name should not
be promoted to a completed theorem until that replacement and the proof closure
are validated repo-locally.
-/
def HypothesisPredicate (D : ThueInput) : Prop :=
  3 ≤ D.form.degree ∧
    D.primitiveIntegralBinaryForm ∧
      D.irreducibleOverRat

def hypothesisPredicateFreezeStatus : String :=
  "frozen_as_degree_at_least_three_primitive_integral_binary_form_irreducible_over_rat"

/--
Statement-only public wrapper for THM-M-0393 / Thue's theorem.

This is a checked Lean proposition boundary, not a proof of the theorem.
-/
def StatementShape : Prop :=
  ∀ D : ThueInput,
    HypothesisPredicate D →
      ThueConclusion D

/-- The public UID wrapper is equivalent to the existing `S1_M_006` statement. -/
theorem statementShape_iff_s1_m_006 :
    StatementShape ↔ AwesomeTheorems.Stage1.S1_M_006.StatementShape := by
  constructor
  · intro h D h_degree h_primitive h_irreducible
    exact h D ⟨h_degree, h_primitive, h_irreducible⟩
  · intro h D hD
    exact h D hD.1 hD.2.1 hD.2.2

/-! Audit probes for the public wrapper namespace. -/

#check HypothesisPredicate
#check hypothesisPredicateFreezeStatus
#check StatementShape
#check statementShape_iff_s1_m_006

end Stage1.THMM0393
