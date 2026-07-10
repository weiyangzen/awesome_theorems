import Mathlib.Data.Nat.Factorization.PrimePow
import Mathlib.Data.Nat.Prime.Int
import Mathlib.Data.Nat.Squarefree

/-!
# Stage1 statement shape for S1-M-004 / THM-M-0390

Catalan's theorem, also known as Mihailescu's theorem, says that `8` and `9`
are the only consecutive nontrivial perfect powers.  This Stage1 artifact does
not claim a machine proof of the theorem.  It records a precise natural-number
statement shape and a small checked witness for the exceptional pair.
-/

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_004

/--
Statement-normalization note for the public Stage1 blueprint:

* `NontrivialNatPower n` means that `n` is a natural-number perfect power
  `base ^ exponent` with both parameters greater than `1`.
* `StatementShape` is the unordered-by-variables, ordered-by-value consecutive
  pair form: if `lower + 1 = upper` and both entries are nontrivial powers,
  then `(lower, upper) = (8, 9)`.
* `OrderedCatalanShape` is the oriented exponential-equation form
  `x ^ a + 1 = y ^ b`, normalized to the unique solution
  `(x, a, y, b) = (2, 3, 3, 2)`.

These declarations are statement shapes and low-dimensional checks only; they
do not assert a repo-local proof of Catalan/Mihailescu's theorem.
-/
def NontrivialNatPower (n : Nat) : Prop :=
  ∃ base exponent : Nat, 1 < base ∧ 1 < exponent ∧ n = base ^ exponent

/-- Compatibility alias for earlier local notes using the `Is...` spelling. -/
def IsNontrivialNatPower (n : Nat) : Prop :=
  NontrivialNatPower n

/-- The normalized consecutive-perfect-power relation used by the Catalan shape. -/
def ConsecutivePowerPair (lower upper : Nat) : Prop :=
  lower + 1 = upper ∧ NontrivialNatPower lower ∧ NontrivialNatPower upper

/--
Statement shape for Catalan's theorem: every consecutive pair of nontrivial
natural-number perfect powers is the exceptional pair `8, 9`.
-/
def StatementShape : Prop :=
  ∀ {lower upper : Nat}, ConsecutivePowerPair lower upper → lower = 8 ∧ upper = 9

/--
Equivalent exponential-equation statement shape for the oriented equation
`x ^ a + 1 = y ^ b`.
-/
def OrderedCatalanShape : Prop :=
  ∀ {x y a b : Nat},
    1 < x → 1 < y → 1 < a → 1 < b → x ^ a + 1 = y ^ b →
      x = 2 ∧ a = 3 ∧ y = 3 ∧ b = 2

/-- Compatibility alias for earlier local notes using equation-shape wording. -/
def ExponentialEquationShape : Prop :=
  OrderedCatalanShape

/-- The lower member of the Catalan exceptional pair is a nontrivial power. -/
theorem eight_is_nontrivial_power : NontrivialNatPower 8 := by
  refine ⟨2, 3, ?_, ?_, ?_⟩
  · decide
  · decide
  · decide

/-- The upper member of the Catalan exceptional pair is a nontrivial power. -/
theorem nine_is_nontrivial_power : NontrivialNatPower 9 := by
  refine ⟨3, 2, ?_, ?_, ?_⟩
  · decide
  · decide
  · decide

/-- Repo-local checked witness that `8` and `9` satisfy the normalized shape. -/
theorem exceptional_pair_is_consecutive_power_pair : ConsecutivePowerPair 8 9 := by
  exact ⟨by decide, eight_is_nontrivial_power, nine_is_nontrivial_power⟩

/-- Repo-local checked witness for the oriented exceptional equation `2 ^ 3 + 1 = 3 ^ 2`. -/
theorem exceptional_pair_satisfies_ordered_equation : 2 ^ 3 + 1 = 3 ^ 2 := by
  decide

/--
Finite low-dimensional sanity check for the oriented statement shape.

This only classifies the grid where all four parameters are in `{2, 3}`.  It is
not a proof of `OrderedCatalanShape`.
-/
theorem two_three_grid_orderedCatalanShape_check {x y a b : Nat}
    (hx : x = 2 ∨ x = 3) (hy : y = 2 ∨ y = 3)
    (ha : a = 2 ∨ a = 3) (hb : b = 2 ∨ b = 3)
    (h : x ^ a + 1 = y ^ b) :
    x = 2 ∧ a = 3 ∧ y = 3 ∧ b = 2 := by
  rcases hx with rfl | rfl <;>
    rcases hy with rfl | rfl <;>
    rcases ha with rfl | rfl <;>
    rcases hb with rfl | rfl
  all_goals norm_num at h
  all_goals norm_num

/--
Local replica of the support-definition shape used by Formal Conjectures'
`Nat.IsPerfectPower`, kept under a project-specific name to avoid importing or
claiming ownership of the external namespace.
-/
def FormalConjecturesIsPerfectPowerShape (n : Nat) : Prop :=
  ∃ base exponent : Nat, 1 < base ∧ 1 < exponent ∧ base ^ exponent = n

/--
The Formal Conjectures support-definition shape is definitionally the same
mathematical predicate as this module's `NontrivialNatPower`, up to the side of
the final equality.
-/
theorem nontrivialNatPower_iff_formalConjecturesIsPerfectPowerShape (n : Nat) :
    NontrivialNatPower n ↔ FormalConjecturesIsPerfectPowerShape n := by
  constructor
  · rintro ⟨base, exponent, hbase, hexponent, rfl⟩
    exact ⟨base, exponent, hbase, hexponent, rfl⟩
  · rintro ⟨base, exponent, hbase, hexponent, hpow⟩
    exact ⟨base, exponent, hbase, hexponent, hpow.symm⟩

/-- Names of repo-local declarations that define and sanity-check this statement boundary. -/
def checkedDeclarationNames : List String :=
  [ "AwesomeTheorems.Stage1.S1_M_004.NontrivialNatPower",
    "AwesomeTheorems.Stage1.S1_M_004.IsNontrivialNatPower",
    "AwesomeTheorems.Stage1.S1_M_004.ConsecutivePowerPair",
    "AwesomeTheorems.Stage1.S1_M_004.StatementShape",
    "AwesomeTheorems.Stage1.S1_M_004.OrderedCatalanShape",
    "AwesomeTheorems.Stage1.S1_M_004.ExponentialEquationShape",
    "AwesomeTheorems.Stage1.S1_M_004.eight_is_nontrivial_power",
    "AwesomeTheorems.Stage1.S1_M_004.nine_is_nontrivial_power",
    "AwesomeTheorems.Stage1.S1_M_004.exceptional_pair_is_consecutive_power_pair",
    "AwesomeTheorems.Stage1.S1_M_004.exceptional_pair_satisfies_ordered_equation",
    "AwesomeTheorems.Stage1.S1_M_004.two_three_grid_orderedCatalanShape_check",
    "AwesomeTheorems.Stage1.S1_M_004.FormalConjecturesIsPerfectPowerShape",
    "AwesomeTheorems.Stage1.S1_M_004.nontrivialNatPower_iff_formalConjecturesIsPerfectPowerShape" ]

/-- Low-dimensional Stage1 checks contributed by the initial Catalan wrapper. -/
def checkedLowDimensionalCheckNames : List String :=
  [ "AwesomeTheorems.Stage1.S1_M_004.exceptional_pair_is_consecutive_power_pair",
    "AwesomeTheorems.Stage1.S1_M_004.exceptional_pair_satisfies_ordered_equation",
    "AwesomeTheorems.Stage1.S1_M_004.two_three_grid_orderedCatalanShape_check" ]

/--
Negative terminal-theorem audit for the local mathlib pin.

The local dependency closure contains Catalan-number combinatorics and a
polynomial Fermat-Catalan theorem, but the Stage1 audit did not find a direct
Lean 4 theorem for Catalan/Mihailescu's consecutive-perfect-power statement.
-/
def mathlibNegativeTerminalTheoremAudit : List String :=
  [ "mathlib rev 8a178386ffc0f5fef0b77738bb5449d50efeea95",
    "Lean toolchain leanprover/lean4:v4.29.0",
    "Mathlib.Combinatorics.Enumerative.Catalan is about Catalan numbers, not Catalan's theorem",
    "Mathlib.RingTheory.PowerSeries.Catalan is about Catalan generating functions",
    "Mathlib.NumberTheory.FLT.Polynomial.Polynomial.flt_catalan proves a polynomial Fermat-Catalan result, not Mihailescu",
    "No local declaration named Catalan/Mihailescu/PerfectPower closes StatementShape" ]

/-- Structured mathlib-anchor audit row for `THM-M-0390-P1`. -/
structure MathlibAnchorAuditEntry where
  auditTarget : String
  localPin : String
  evidence : String
  conclusion : String
  repoLocalStatus : String
deriving Repr

/--
Integration-ready P1 mathlib-anchor audit table.

The table records the local mathlib pin and the negative terminal-theorem
result.  Nearby Catalan-number and polynomial Fermat-Catalan declarations are
useful search evidence, but none proves the natural-number Mihailescu statement
encoded by `StatementShape` or `OrderedCatalanShape`.
-/
def mathlibAnchorAudit : List MathlibAnchorAuditEntry :=
  [ { auditTarget := "local mathlib dependency pin",
      localPin :=
        "mathlib4 rev 8a178386ffc0f5fef0b77738bb5449d50efeea95; Lean toolchain leanprover/lean4:v4.29.0",
      evidence :=
        "Formalizations/Lean/lakefile.lean pins mathlib at this revision; lake-manifest.json records the same mathlib package revision",
      conclusion :=
        "P1 audit is tied to the repo-local Lake dependency closure, not an unpinned upstream search",
      repoLocalStatus := "pinned audit context" },
    { auditTarget := "Mihailescu theorem docs anchor",
      localPin :=
        "mathlib4 rev 8a178386ffc0f5fef0b77738bb5449d50efeea95",
      evidence :=
        "mathlib docs/1000.yaml contains Q174955 with title Mihailescu's theorem and no decl or decls field",
      conclusion :=
        "the mathlib documentation index does not point to a Lean declaration proving the terminal theorem",
      repoLocalStatus := "negative terminal-theorem evidence" },
    { auditTarget := "Catalan-number name collision",
      localPin :=
        "mathlib4 rev 8a178386ffc0f5fef0b77738bb5449d50efeea95",
      evidence :=
        "Mathlib.Combinatorics.Enumerative.Catalan and Mathlib.RingTheory.PowerSeries.Catalan define Catalan numbers and their generating series",
      conclusion :=
        "these modules are combinatorial name collisions, not Catalan/Mihailescu consecutive-perfect-power theorems",
      repoLocalStatus := "adjacent non-terminal mathlib material" },
    { auditTarget := "polynomial Fermat-Catalan theorem",
      localPin :=
        "mathlib4 rev 8a178386ffc0f5fef0b77738bb5449d50efeea95",
      evidence :=
        "Mathlib.NumberTheory.FLT.Polynomial.Polynomial.flt_catalan proves nonsolvability for a polynomial Fermat-Catalan equation",
      conclusion :=
        "the theorem is polynomial-domain adjacent infrastructure and does not close natural-number StatementShape or OrderedCatalanShape",
      repoLocalStatus := "adjacent non-terminal mathlib theorem" },
    { auditTarget := "terminal Catalan/Mihailescu theorem search",
      localPin :=
        "mathlib4 rev 8a178386ffc0f5fef0b77738bb5449d50efeea95",
      evidence :=
        "repo-local search for Catalan, Mihailescu, Mihailescu-with-diacritic, PerfectPower, and consecutive perfect powers found no mathlib declaration proving the natural-number terminal theorem",
      conclusion :=
        "no direct mathlib theorem currently proves StatementShape, OrderedCatalanShape, or a direct Catalan/Mihailescu wrapper",
      repoLocalStatus := "not_repo_local_closed; formalization_debt remains" } ]

/-- Canonical declaration names for the P1 mathlib-anchor audit table. -/
def mathlibAnchorAuditDeclarationNames : List String :=
  [ "AwesomeTheorems.Stage1.S1_M_004.MathlibAnchorAuditEntry",
    "AwesomeTheorems.Stage1.S1_M_004.mathlibAnchorAudit",
    "AwesomeTheorems.Stage1.S1_M_004.mathlibNegativeTerminalTheoremAudit" ]

/-- Structured record for support APIs inspected for a future proof package. -/
structure SupportApiAuditEntry where
  declaration : String
  moduleName : String
  role : String
  stage1Status : String
deriving Repr

/-- Support APIs checked by this module for the first real Lean proof-package audit. -/
def mathlibSupportApiQueue : List String :=
  [ "Nat.Prime.pow_inj'",
    "Nat.exists_eq_pow_of_pow_eq_pow",
    "Nat.exists_eq_pow_of_exponent_coprime_of_pow_eq_pow",
    "IsPrimePow",
    "isPrimePow_nat_iff",
    "IsPrimePow.minFac_pow_factorization_eq",
    "isPrimePow_iff_factorization_eq_single",
    "isPrimePow_iff_unique_prime_dvd",
    "isPrimePow_pow_iff",
    "Nat.Coprime.isPrimePow_dvd_mul",
    "Squarefree",
    "Squarefree.natFactorization_le_one",
    "Nat.squarefree_iff_factorization_le_one",
    "Nat.factorization",
    "Nat.factorization_pow",
    "Nat.Prime.factorization_pow" ]

/-- Integration-ready audit table for the support APIs named by `THM-M-0390-P2`. -/
def mathlibSupportApiAudit : List SupportApiAuditEntry :=
  [ { declaration := "Nat.Prime.pow_inj'",
      moduleName := "Mathlib.Data.Nat.Prime.Int",
      role := "uniqueness for equal positive prime powers; useful after reducing bases to primes",
      stage1Status := "checked support API only, not a Catalan theorem" },
    { declaration := "Nat.exists_eq_pow_of_pow_eq_pow",
      moduleName := "Mathlib.Data.Nat.Factorization.Basic",
      role := "extracts a common root from an equality of natural powers with nonzero exponent data",
      stage1Status := "checked support API only, not a Catalan theorem" },
    { declaration := "Nat.exists_eq_pow_of_exponent_coprime_of_pow_eq_pow",
      moduleName := "Mathlib.Data.Nat.Factorization.Basic",
      role := "coprime-exponent version of common-root extraction for power equalities",
      stage1Status := "checked support API only, not a Catalan theorem" },
    { declaration := "Nat.factorization",
      moduleName := "Mathlib.Data.Nat.Factorization.Basic",
      role := "prime-exponent finitely supported factorization for natural numbers",
      stage1Status := "checked object-model support" },
    { declaration := "Nat.factorization_pow",
      moduleName := "Mathlib.Data.Nat.Factorization.Basic",
      role := "rewrites factorization of a natural-number power as scalar multiplication",
      stage1Status := "checked object-model support" },
    { declaration := "Nat.Prime.factorization_pow",
      moduleName := "Mathlib.Data.Nat.Factorization.Basic",
      role := "specializes factorization of a prime power to a single finitely supported exponent",
      stage1Status := "checked object-model support" },
    { declaration := "Squarefree",
      moduleName := "Mathlib.Data.Nat.Squarefree",
      role := "squarefree predicate for natural-number radical and repeated-prime-factor branches",
      stage1Status := "checked object-model support" },
    { declaration := "Nat.squarefree_iff_factorization_le_one",
      moduleName := "Mathlib.Data.Nat.Squarefree",
      role := "characterizes squarefree naturals by factorization exponents bounded by one",
      stage1Status := "checked object-model support" },
    { declaration := "IsPrimePow",
      moduleName := "Mathlib.Algebra.IsPrimePow",
      role := "prime-power predicate over commutative monoids with zero, specialized to naturals",
      stage1Status := "checked object-model support" },
    { declaration := "isPrimePow_nat_iff",
      moduleName := "Mathlib.Algebra.IsPrimePow",
      role := "natural-number prime-power witness form with a prime base and positive exponent",
      stage1Status := "checked object-model support" },
    { declaration := "IsPrimePow.minFac_pow_factorization_eq",
      moduleName := "Mathlib.Data.Nat.Factorization.PrimePow",
      role := "recovers a prime power from its minimal prime factor and factorization exponent",
      stage1Status := "checked object-model support" },
    { declaration := "isPrimePow_iff_factorization_eq_single",
      moduleName := "Mathlib.Data.Nat.Factorization.PrimePow",
      role := "characterizes natural prime powers by singleton factorization support",
      stage1Status := "checked object-model support" },
    { declaration := "isPrimePow_iff_unique_prime_dvd",
      moduleName := "Mathlib.Data.Nat.Factorization.PrimePow",
      role := "characterizes natural prime powers by a unique prime divisor",
      stage1Status := "checked object-model support" },
    { declaration := "isPrimePow_pow_iff",
      moduleName := "Mathlib.Data.Nat.Factorization.PrimePow",
      role := "transfers prime-power status across nonzero natural powers",
      stage1Status := "checked object-model support" },
    { declaration := "Nat.Coprime.isPrimePow_dvd_mul",
      moduleName := "Mathlib.Data.Nat.Factorization.PrimePow",
      role := "splits prime-power divisibility across coprime factors",
      stage1Status := "checked object-model support" } ]

/--
Checked anchor for `Nat.Prime.pow_inj'`.

This is a support wrapper only.  It proves no Catalan/Mihailescu statement.
-/
theorem support_pow_inj_prime_power_anchor {p q m n : Nat}
    (hp : Nat.Prime p) (hq : Nat.Prime q) (hm : m ≠ 0) (hn : n ≠ 0)
    (h : p ^ m = q ^ n) : p = q ∧ m = n :=
  Nat.Prime.pow_inj' hp hq hm hn h

/--
Checked anchor for `Nat.exists_eq_pow_of_pow_eq_pow`.

This extracts a common root from an equality of powers; it is not a
consecutive-perfect-power theorem.
-/
theorem support_exists_eq_pow_of_pow_eq_pow_anchor {a b m n : Nat}
    (hmn : m ≠ 0 ∨ n ≠ 0) (h : a ^ m = b ^ n) :
    ∃ c, a = c ^ (n / Nat.gcd m n) ∧ b = c ^ (m / Nat.gcd m n) :=
  Nat.exists_eq_pow_of_pow_eq_pow hmn h

/-- Checked anchor for the coprime-exponent common-root extraction API. -/
theorem support_exists_eq_pow_of_exponent_coprime_anchor {a b m n : Nat}
    (hmn : m.Coprime n) (h : a ^ m = b ^ n) :
    ∃ c, a = c ^ n ∧ b = c ^ m :=
  Nat.exists_eq_pow_of_exponent_coprime_of_pow_eq_pow hmn h

/-- Checked anchor for `Nat.factorization_pow`. -/
theorem support_factorization_pow_anchor (n k : Nat) :
    (n ^ k).factorization = k • n.factorization :=
  Nat.factorization_pow n k

/-- Checked anchor for factorization of prime powers. -/
theorem support_prime_factorization_pow_anchor {p k : Nat} (hp : Nat.Prime p) :
    (p ^ k).factorization = Finsupp.single p k :=
  Nat.Prime.factorization_pow hp

/-- Checked anchor for the squarefree/factorization-exponent characterization. -/
theorem support_squarefree_factorization_anchor {n : Nat} (hn : n ≠ 0) :
    Squarefree n ↔ ∀ p, n.factorization p ≤ 1 :=
  Nat.squarefree_iff_factorization_le_one hn

/-- Checked anchor for squarefree naturals having factorization exponents at most one. -/
theorem support_squarefree_natFactorization_le_one_anchor {n p : Nat}
    (hn : Squarefree n) : n.factorization p ≤ 1 :=
  hn.natFactorization_le_one p

/-- Checked anchor for the natural-number witness form of `IsPrimePow`. -/
theorem support_isPrimePow_nat_anchor (n : Nat) :
    IsPrimePow n ↔ ∃ p k, Nat.Prime p ∧ 0 < k ∧ p ^ k = n :=
  isPrimePow_nat_iff n

/-- Checked anchor recovering a prime power from `minFac` and factorization. -/
theorem support_isPrimePow_minFac_anchor {n : Nat} (hn : IsPrimePow n) :
    n.minFac ^ n.factorization n.minFac = n :=
  IsPrimePow.minFac_pow_factorization_eq hn

/-- Checked anchor for singleton-factorization prime-power characterization. -/
theorem support_isPrimePow_single_anchor {n : Nat} :
    IsPrimePow n ↔ ∃ p k : Nat, 0 < k ∧ n.factorization = Finsupp.single p k :=
  isPrimePow_iff_factorization_eq_single

/-- Checked anchor for unique-prime-divisor prime-power characterization. -/
theorem support_isPrimePow_unique_prime_anchor {n : Nat} :
    IsPrimePow n ↔ ∃! p : Nat, Nat.Prime p ∧ p ∣ n :=
  isPrimePow_iff_unique_prime_dvd

/-- Checked anchor transferring prime-power status across nonzero powers. -/
theorem support_isPrimePow_pow_iff_anchor {n k : Nat} (hk : k ≠ 0) :
    IsPrimePow (n ^ k) ↔ IsPrimePow n :=
  isPrimePow_pow_iff hk

/-- Checked anchor for splitting prime-power divisibility across coprime factors. -/
theorem support_isPrimePow_dvd_mul_anchor {n a b : Nat}
    (hab : a.Coprime b) (hn : IsPrimePow n) :
    n ∣ a * b ↔ n ∣ a ∨ n ∣ b :=
  hab.isPrimePow_dvd_mul hn

/-- Repo-local wrapper names that Lean checked for the support-API audit. -/
def checkedSupportApiAnchorNames : List String :=
  [ "AwesomeTheorems.Stage1.S1_M_004.support_pow_inj_prime_power_anchor",
    "AwesomeTheorems.Stage1.S1_M_004.support_exists_eq_pow_of_pow_eq_pow_anchor",
    "AwesomeTheorems.Stage1.S1_M_004.support_exists_eq_pow_of_exponent_coprime_anchor",
    "AwesomeTheorems.Stage1.S1_M_004.support_factorization_pow_anchor",
    "AwesomeTheorems.Stage1.S1_M_004.support_prime_factorization_pow_anchor",
    "AwesomeTheorems.Stage1.S1_M_004.support_squarefree_factorization_anchor",
    "AwesomeTheorems.Stage1.S1_M_004.support_squarefree_natFactorization_le_one_anchor",
    "AwesomeTheorems.Stage1.S1_M_004.support_isPrimePow_nat_anchor",
    "AwesomeTheorems.Stage1.S1_M_004.support_isPrimePow_minFac_anchor",
    "AwesomeTheorems.Stage1.S1_M_004.support_isPrimePow_single_anchor",
    "AwesomeTheorems.Stage1.S1_M_004.support_isPrimePow_unique_prime_anchor",
    "AwesomeTheorems.Stage1.S1_M_004.support_isPrimePow_pow_iff_anchor",
    "AwesomeTheorems.Stage1.S1_M_004.support_isPrimePow_dvd_mul_anchor" ]

/-- Structured record for an external Lean statement anchor that is not a proof. -/
structure ExternalStatementOnlyAnchorAuditEntry where
  repository : String
  commit : String
  sourceFile : String
  namespaceName : String
  theoremName : String
  sourceStatementShape : String
  proofStatus : String
  repoLocalStatus : String
  integrationBlocker : String
deriving Repr

/--
External statement-only anchor found during the Stage1 audit.

Google DeepMind's `formal-conjectures` repository has
`FormalConjectures/Wikipedia/Catalan.lean`, namespace `Catalan`, theorem
`catalans_conjecture`, but that theorem is closed by an unproved placeholder;
it is a useful statement comparison, not a proof anchor.
-/
def externalStatementOnlyAnchor : String :=
  "google-deepmind/formal-conjectures: FormalConjectures/Wikipedia/Catalan.lean, Catalan.catalans_conjecture, statement-only with unproved placeholder"

/-- M0387-level external-anchor audit entry for `Catalan.catalans_conjecture`. -/
def formalConjecturesCatalanAnchor : ExternalStatementOnlyAnchorAuditEntry :=
  { repository := "google-deepmind/formal-conjectures",
    commit := "7871d8fc7a8164a1ac16c3765b40c25ce015b681",
    sourceFile := "FormalConjectures/Wikipedia/Catalan.lean",
    namespaceName := "Catalan",
    theoremName := "catalans_conjecture",
    sourceStatementShape :=
      "for naturals a b x y, 1 < a, 1 < b, 0 < x, 0 < y, and x ^ a - y ^ b = 1 imply a = 2, b = 3, x = 3, y = 2",
    proofStatus :=
      "statement-only external Lean theorem closed by an unproved placeholder; not a machine-checked Mihailescu proof",
    repoLocalStatus :=
      "external_upstream_anchor_only; not imported, pinned as a dependency, or used to close StatementShape",
    integrationBlocker :=
      "not completion evidence because the upstream theorem has no proof body and its project uses Lean 4.27 while this repo uses Lean 4.29" }

/-- Source URLs captured for the external statement-only Catalan anchor. -/
def formalConjecturesCatalanAnchorUrls : List String :=
  [ "https://github.com/google-deepmind/formal-conjectures/tree/7871d8fc7a8164a1ac16c3765b40c25ce015b681",
    "https://github.com/google-deepmind/formal-conjectures/blob/7871d8fc7a8164a1ac16c3765b40c25ce015b681/FormalConjectures/Wikipedia/Catalan.lean",
    "https://github.com/google-deepmind/formal-conjectures/blob/7871d8fc7a8164a1ac16c3765b40c25ce015b681/lean-toolchain",
    "https://github.com/google-deepmind/formal-conjectures/blob/7871d8fc7a8164a1ac16c3765b40c25ce015b681/lakefile.toml" ]

/-- External statement-only anchors recorded by this module. -/
def externalStatementOnlyAnchorAudit : List ExternalStatementOnlyAnchorAuditEntry :=
  [ formalConjecturesCatalanAnchor ]

/-- Structured record for deciding whether to use an external support definition. -/
structure SupportDefinitionDecisionEntry where
  externalDeclaration : String
  sourceFile : String
  decision : String
  reason : String
  repoLocalAction : String
  repoLocalDebt : String
deriving Repr

/--
Decision for `THM-M-0390-P4`.

The Formal Conjectures `Nat.IsPerfectPower` support definition is not imported
as a dependency and its auxiliary factorization-gcd theorem is not ported here.
This module keeps the smaller local predicate required for Catalan statement
normalization and checks the equivalence of predicate shapes.
-/
def formalConjecturesPerfectPowerDecision : SupportDefinitionDecisionEntry :=
  { externalDeclaration := "Nat.IsPerfectPower",
    sourceFile :=
      "google-deepmind/formal-conjectures@7871d8fc7a8164a1ac16c3765b40c25ce015b681/FormalConjecturesForMathlib/Data/Nat/PerfectPower.lean",
    decision :=
      "ignore as an import target; do not port the auxiliary theorem as canonical API for this Stage1 wrapper",
    reason :=
      "the external file is Lean 4.27-era support infrastructure, not a Catalan/Mihailescu proof; the needed predicate shape is already available locally as NontrivialNatPower; mathlib prime-power and factorization APIs already cover the proof-audit support queue",
    repoLocalAction :=
      "added FormalConjecturesIsPerfectPowerShape and a checked equivalence theorem to NontrivialNatPower",
    repoLocalDebt :=
      "none for completion purposes: this is support-definition triage, not an external terminal theorem proof; the parent theorem remains formalization_debt" }

/-- Source URLs captured for the Formal Conjectures perfect-power support audit. -/
def formalConjecturesPerfectPowerUrls : List String :=
  [ "https://github.com/google-deepmind/formal-conjectures/blob/7871d8fc7a8164a1ac16c3765b40c25ce015b681/FormalConjecturesForMathlib/Data/Nat/PerfectPower.lean",
    "https://github.com/google-deepmind/formal-conjectures/blob/7871d8fc7a8164a1ac16c3765b40c25ce015b681/lean-toolchain",
    "https://github.com/google-deepmind/formal-conjectures/blob/7871d8fc7a8164a1ac16c3765b40c25ce015b681/lakefile.toml" ]

/-- First proof-package queue for a future Mihailescu formalization attempt. -/
def firstProofPackageQueue : List String :=
  [ "P0 statement normalization between consecutive-value and oriented-equation forms",
    "P1 primitive/coprime/parity normalization for a minimal counterexample",
    "P2 Cassels-style divisibility restrictions on bases and exponents",
    "P3 double-Wieferich obstruction package",
    "P4 cyclotomic-unit and ideal-factorization package",
    "P5 class-group obstruction package",
    "P6 final contradiction and transfer back to StatementShape" ]

/-- Structured record for the classical Mihailescu proof-package tree. -/
structure ClassicalProofPackageEntry where
  packageId : String
  packageName : String
  upstreamInput : List String
  localObligation : List String
  downstreamOutput : List String
  currentRepoStatus : String
  debtClass : String
deriving Repr

/--
Expanded theorem-tree skeleton requested by `THM-M-0390-P6`.

These are integration-ready proof packages, not completed Lean proofs.  Every
package is intentionally marked `unchecked`; the declarations record the next
formalization interfaces while avoiding a false claim that this repository has a
machine-checked proof of Catalan/Mihailescu's theorem.
-/
def classicalProofPackageTree : List ClassicalProofPackageEntry :=
  [ { packageId := "P6.0",
      packageName := "statement and primitive-counterexample normalization",
      upstreamInput :=
        [ "StatementShape",
          "OrderedCatalanShape",
          "ConsecutivePowerPair",
          "NontrivialNatPower" ],
      localObligation :=
        [ "prove equivalence between consecutive nontrivial powers and an oriented equation",
          "extract a primitive/minimal counterexample with coprime positive bases",
          "record parity and exponent-normalization branches before Cassels inputs are invoked" ],
      downstreamOutput :=
        [ "primitive normalized counterexample object for Cassels divisibility packages" ],
      currentRepoStatus :=
        "unchecked skeleton only; this file currently has statement shapes and low-dimensional witnesses",
      debtClass := "formalization_debt" },
    { packageId := "P6.1",
      packageName := "Cassels divisibility restrictions",
      upstreamInput :=
        [ "primitive normalized counterexample",
          "prime-power/factorization support APIs",
          "coprime splitting support APIs" ],
      localObligation :=
        [ "formalize the Cassels restriction that each prime divisor on one side imposes exponent divisibility data on the opposite side",
          "split the argument into odd/even and primitive/non-primitive cases where the classical proof does so",
          "export exact divisibility hypotheses needed by double-Wieferich and cyclotomic packages" ],
      downstreamOutput :=
        [ "Cassels divisibility certificate",
          "prime support constraints for the double-Wieferich obstruction" ],
      currentRepoStatus :=
        "unchecked theorem-tree package; no Cassels theorem is imported or proved locally",
      debtClass := "formalization_debt" },
    { packageId := "P6.2",
      packageName := "double-Wieferich obstruction",
      upstreamInput :=
        [ "Cassels divisibility certificate",
          "primitive counterexample congruence data" ],
      localObligation :=
        [ "state the two-sided Wieferich congruence obligations forced by a surviving counterexample",
          "separate local congruence lemmas from the global contradiction branch",
          "connect the obstruction back to the prime support supplied by Cassels" ],
      downstreamOutput :=
        [ "double-Wieferich obstruction certificate for the normalized counterexample" ],
      currentRepoStatus :=
        "unchecked theorem-tree package; no local Wieferich obstruction proof body",
      debtClass := "formalization_debt" },
    { packageId := "P6.3",
      packageName := "cyclotomic-unit and ideal-factorization package",
      upstreamInput :=
        [ "Cassels divisibility certificate",
          "double-Wieferich obstruction certificate",
          "normalized exponential equation in a cyclotomic field" ],
      localObligation :=
        [ "build the cyclotomic field and ring-of-integers context required by the classical proof",
          "factor the relevant principal ideals and isolate the cyclotomic-unit equation",
          "prove the unit and ideal-divisibility interfaces consumed by the class-group package" ],
      downstreamOutput :=
        [ "cyclotomic-unit certificate",
          "ideal-factorization certificate" ],
      currentRepoStatus :=
        "unchecked theorem-tree package; mathlib support for this full package has not been audited here",
      debtClass := "formalization_debt" },
    { packageId := "P6.4",
      packageName := "class-group obstruction package",
      upstreamInput :=
        [ "cyclotomic-unit certificate",
          "ideal-factorization certificate",
          "Cassels and double-Wieferich certificates" ],
      localObligation :=
        [ "state the class-group divisibility obstruction used to rule out the remaining counterexample",
          "separate the ideal-class order argument from required cyclotomic arithmetic facts",
          "export a contradiction certificate for the primitive normalized equation" ],
      downstreamOutput :=
        [ "class-group contradiction certificate" ],
      currentRepoStatus :=
        "unchecked theorem-tree package; no class-group obstruction theorem is imported or proved locally",
      debtClass := "formalization_debt" },
    { packageId := "P6.5",
      packageName := "final contradiction and transfer to Catalan shapes",
      upstreamInput :=
        [ "primitive normalized counterexample",
          "class-group contradiction certificate",
          "statement-normalization equivalence" ],
      localObligation :=
        [ "derive contradiction for every normalized non-exceptional solution",
          "prove the exceptional solution remains the only oriented equation solution",
          "transfer the oriented conclusion back to StatementShape for consecutive powers" ],
      downstreamOutput :=
        [ "OrderedCatalanShape",
          "StatementShape" ],
      currentRepoStatus :=
        "unchecked theorem-tree package; no terminal Catalan proof exists in this repo",
      debtClass := "formalization_debt" } ]

/-- Canonical names for the package-level leaves opened by `THM-M-0390-P6`. -/
def classicalProofPackageLeafNames : List String :=
  [ "S1-M-004.P6.0.statement-primitive-normalization",
    "S1-M-004.P6.1.Cassels-divisibility-restrictions",
    "S1-M-004.P6.2.double-Wieferich-obstruction",
    "S1-M-004.P6.3.cyclotomic-unit-ideal-factorization",
    "S1-M-004.P6.4.class-group-obstruction",
    "S1-M-004.P6.5.final-contradiction-transfer" ]

/--
Completion gate for `THM-M-0390-P6`.

The gate deliberately remains open: the current contribution is an auditable
package tree, while all five mathematical proof packages still need local
Lean theorem statements, proof bodies or pinned checked upstream replacements,
and independent `<=100`-step leaf ledgers.
-/
def classicalProofPackageCompletionGate : String :=
  "open: theorem-tree expanded, but all packages are unchecked formalization_debt"

/-- Structured record for repo-local build-validation instructions. -/
structure BuildValidationInstructionEntry where
  workingDirectory : String
  command : String
  validates : String
  doesNotValidate : String
  rerunPolicy : String
  publicStatusPolicy : String
deriving Repr

/--
Build-validation instructions for `THM-M-0390-P7`.

These instructions are intentionally stored in the theorem-local Stage1 artifact
so a serial public-doc integrator can copy them into the blueprint/todo surface
without racing on shared planning files.  The command validates this wrapper's
statement shapes, support API anchors, external-anchor audit data, and unchecked
proof-package metadata.  It does not validate a proof of Catalan/Mihailescu's
theorem.
-/
def buildValidationInstructions : BuildValidationInstructionEntry :=
  { workingDirectory := "Formalizations/Lean",
    command := "lake env lean AwesomeTheorems/Stage1/S1_M_004.lean",
    validates :=
      "the repo-local Stage1 wrapper file, including statement-shape declarations, low-dimensional checks, support-API wrappers, external statement-only audit data, proof-package metadata, and these build-validation instructions",
    doesNotValidate :=
      "StatementShape, OrderedCatalanShape, or any full Catalan/Mihailescu theorem proof; all classical proof packages remain unchecked formalization_debt",
    rerunPolicy :=
      "rerun after every edit to Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_004.lean and before any public status or checkbox update that cites this wrapper",
    publicStatusPolicy :=
      "record the command and current pass/fail result publicly, but keep THM-M-0390 open until a terminal local proof body, checked mathlib wrapper, or pinned external proof dependency validates and independent <=100 leaf ledgers are closed" }

/-- Exact command line to use from the repository root when validating this wrapper. -/
def buildValidationCommandFromRepoRoot : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_004.lean"

/-- Canonical local validation surface recorded by `THM-M-0390-P7`. -/
def buildValidationSurfaceNames : List String :=
  [ "AwesomeTheorems.Stage1.S1_M_004.buildValidationInstructions",
    "AwesomeTheorems.Stage1.S1_M_004.buildValidationCommandFromRepoRoot" ]

/--
Machine-proof audit marker for this Stage1 module.

`StatementShape` and `OrderedCatalanShape` are statement shapes only; this
module has no local proof body, no mathlib wrapper for Catalan, and no pinned
external Lean dependency proving the full theorem.
-/
def machineProofDebt : String := "formalization_debt"

/--
Repo-local integration debt gate.

This is `False` because no external Lean 4 proof of Catalan/Mihailescu's theorem
has been pinned, imported, and checked by this repository in this repair pass.
-/
def repoLocalIntegrationDebtClosed : Prop := False

/-- Structured M0387 completion-gate row for `THM-M-0390-P8`. -/
structure M0387CompletionGateEntry where
  gateName : String
  repoLocalEvidence : String
  gateStatus : String
  requiredBeforeClose : String
deriving Repr

/--
P8 gate audit for the public Stage1 checkbox.

Every row is intentionally `open`.  The current module records useful statement
shapes, support anchors, and proof-package metadata, but it does not close
Catalan/Mihailescu in Lean.
-/
def p8M0387CompletionGateAudit : List M0387CompletionGateEntry :=
  [ { gateName := "machine theorem anchor",
      repoLocalEvidence :=
        "No local proof body, mathlib wrapper theorem, or pinned external proof dependency proves StatementShape or OrderedCatalanShape",
      gateStatus := "open",
      requiredBeforeClose :=
        "provide a repo-local proof body, a checked mathlib wrapper, or a pinned external dependency with a closed theorem proof" },
    { gateName := "local validation",
      repoLocalEvidence :=
        "The validation command for this wrapper is recorded as buildValidationCommandFromRepoRoot",
      gateStatus := "open for completion",
      requiredBeforeClose :=
        "run the validation command after the terminal machine anchor exists and record the passing result in the public surface" },
    { gateName := "public merge-back",
      repoLocalEvidence :=
        "This module is theorem-local implementation evidence; the shared Stage1 blueprint and todo surfaces remain serial-integration targets",
      gateStatus := "open",
      requiredBeforeClose :=
        "merge the statement audit, support audit, proof-package tree, validation record, and status boundary into the public blueprint/todo surfaces" },
    { gateName := "independent <=100 leaf ledgers",
      repoLocalEvidence :=
        "The classical proof packages are unchecked skeletons and do not yet have independent closed leaf ledgers",
      gateStatus := "open",
      requiredBeforeClose :=
        "split every proof package into independently checked leaves whose proof procedures are each <=100 steps" } ]

/-- Public Stage1 checkbox status implied by the P8 audit. -/
def p8PublicCheckboxStatus : String :=
  "keep open: machine anchor, completion-grade validation, public merge-back, and independent <=100 leaf ledgers are not all closed"

/-- Checked witness that the repo-local integration-debt gate is not closed. -/
theorem repoLocalIntegrationDebtGate_open : ¬ repoLocalIntegrationDebtClosed := by
  intro h
  exact h

end S1_M_004
end Stage1
end AwesomeTheorems
