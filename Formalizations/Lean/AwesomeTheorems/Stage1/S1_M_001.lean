import AwesomeTheorems.NumberTheory.THM_M_0387.StatementAndReductionPath
import AwesomeTheorems.NumberTheory.THM_M_0387.FLT4Path
import AwesomeTheorems.NumberTheory.THM_M_0387.FLT3Path
import AwesomeTheorems.NumberTheory.THM_M_0387.RegularPrimesPath
import AwesomeTheorems.NumberTheory.THM_M_0387.SmallExponentsPath

/-!
# S1-M-001 / THM-M-0387: Fermat's Last Theorem

Stage1 theorem-internal repair artifact for Fermat's Last Theorem.

This file is deliberately not a proof of the full Wiles/Taylor-Wiles route.
It records the normalized full statement shape and local checked wrappers for
the branches that are already in the current Lake dependency closure:

* mathlib statement/reduction layer;
* mathlib `n = 3`;
* mathlib `n = 4`;
* pinned `leanprover-community/flt-regular` regular-primes branch through the
  repo-local `regularPrimesPath` wrapper.

The remaining complete odd-prime-exponent family is kept as a precise `Prop`
so this module compiles without proof placeholders.
-/

namespace AwesomeTheorems.Stage1.S1_M_001

open AwesomeTheorems.NumberTheory.THM_M_0387

/-- Normalized Stage1 statement shape for Fermat's Last Theorem. -/
abbrev StatementShape : Prop :=
  fermatLastTheoremRootStatement

/--
The exact missing theorem family needed, together with the `n = 4` branch, to
assemble the full FLT statement using mathlib's reduction theorem.
-/
abbrev OddPrimeExponentClosure : Prop :=
  AwesomeTheorems.NumberTheory.THM_M_0387.OddPrimeExponentClosure

/--
The Wiles/Taylor-Wiles part of the full theorem, expressed as the same precise
odd-prime-exponent family.  This remains `formalization_debt` for this Stage1
slot; no proof placeholder is introduced here.
-/
def WilesTaylorWilesFormalizationDebt : Prop :=
  OddPrimeExponentClosure

/-- The checked `n = 3` branch imported from mathlib through the repo wrapper. -/
theorem fltThreeBranch : FermatLastTheoremFor 3 :=
  flt3Path

/-- The checked `n = 4` branch imported from mathlib through the repo wrapper. -/
theorem fltFourBranch : FermatLastTheoremFor 4 :=
  flt4Path

/-- Exponents divisible by `4` reduce to the checked `n = 4` branch. -/
theorem fltForExponentDivisibleByFour {n : ℕ} (hdiv : 4 ∣ n) :
    FermatLastTheoremFor n :=
  FermatLastTheoremFor.mono hdiv fltFourBranch

/--
The checked regular-prime branch imported from the pinned `flt-regular`
dependency through the repo-local wrapper theorem.
-/
theorem regularPrimeBranch {p : ℕ} [Fact p.Prime]
    (hreg : IsRegularPrime p) (hodd : p ≠ 2) : FermatLastTheoremFor p :=
  regularPrimesPath hreg hodd

/-- The checked pinned family for every exponent in the closed interval `3 .. 16`. -/
theorem smallExponentBranch {n : ℕ} (hn : n ∈ Finset.Icc 3 16) :
    FermatLastTheoremFor n :=
  fltSmallExponentsPath hn

/--
If the missing odd-prime-exponent family is supplied, mathlib assembles the
full normalized FLT statement.  This is a checked wrapper around the local
reduction theorem, not a proof of the missing family.
-/
theorem statementShape_of_oddPrimeExponentClosure
    (hodd : OddPrimeExponentClosure) : StatementShape :=
  fermatLastTheoremRootOfOddPrimesPath hodd

/-- Statement-shape identity for audit tools. -/
theorem statementShape_iff_fermatLastTheorem :
    StatementShape ↔ FermatLastTheorem :=
  fermatLastTheoremRootStatement_iff

/-- Repo-local integration status for the regular-primes branch. -/
def regularPrimesRepoLocalIntegrationDebtClosed : Prop :=
  ∀ {p : ℕ} [Fact p.Prime], IsRegularPrime p → p ≠ 2 → FermatLastTheoremFor p

/-- The regular-primes integration-debt gate is closed by `regularPrimesPath`. -/
theorem regularPrimesRepoLocalIntegrationDebtGate :
    regularPrimesRepoLocalIntegrationDebtClosed :=
  fun hreg hodd => regularPrimesPath hreg hodd

/--
The checked Stage1 branch frontier for this repository: mathlib's `n = 3` and
`n = 4` branches plus the pinned regular-primes branch.
-/
def CheckedBranchFrontier : Prop :=
  FermatLastTheoremFor 3 ∧
    FermatLastTheoremFor 4 ∧
      regularPrimesRepoLocalIntegrationDebtClosed

/--
The repo-local integration-debt gate for every checked branch claimed
by this Stage1 slot.  The full Wiles/Taylor-Wiles odd-prime-exponent family is
not part of this theorem; it remains `formalization_debt`.
-/
theorem checkedBranchFrontierRepoLocalIntegrationDebtGate :
    CheckedBranchFrontier :=
  ⟨fltThreeBranch, fltFourBranch, regularPrimesRepoLocalIntegrationDebtGate⟩

/-- Pinned external dependency commit used for the regular-primes branch. -/
def fltRegularPinnedRevision : String :=
  "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"

/-- Machine-status classification for the regular-primes branch. -/
def regularPrimesMachineStatus : String :=
  "external_upstream_pinned"

/--
Concise audit note for the regular-primes branch.  This records that the
branch is inside the repo-local Lake dependency closure rather than an
anchor-only upstream reference.
-/
def regularPrimesExternalUpstreamPinnedAudit : List String := [
  "status: external_upstream_pinned",
  "upstream: leanprover-community/flt-regular",
  "revision: 56161b6eb5281fbfe9c38f2bcec0f429ebc11a27",
  "lake dependency: flt-regular is pinned in lakefile.lean and lake-manifest.json",
  "imported module: AwesomeTheorems.NumberTheory.THM_M_0387.RegularPrimesPath imports FltRegular.FltRegular",
  "terminal upstream theorem: flt_regular",
  "repo-local wrapper theorem: regularPrimesPath",
  "completion gate: regularPrimesRepoLocalIntegrationDebtGate",
  "anchor-only: false"
]

/-- Pinned mathlib commit used by this repo-local Lean project. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Concise audit note for the `Mathlib.NumberTheory.FLT.Basic` surface used by
this Stage1 wrapper at `mathlibPinnedRevision`.
-/
def fltBasicStatementReductionAudit : List String := [
  "module: Mathlib.NumberTheory.FLT.Basic",
  "revision: 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "statement objects: FermatLastTheoremWith, FermatLastTheoremFor, FermatLastTheorem",
  "reduction/transport: FermatLastTheoremWith.mono, FermatLastTheoremFor.mono, fermatLastTheoremWith_nat_int_rat_tfae, fermatLastTheoremFor_iff_int, fermatLastTheoremFor_iff_rat",
  "primitive-solution helpers: fermatLastTheoremWith_of_fermatLastTheoremWith_coprime, dvd_c_of_prime_of_dvd_a_of_dvd_b_of_FLT, isCoprime_of_gcd_eq_one_of_FLT"
]

/--
Concise audit note for the mathlib special-case terminals wrapped by this
repo-local Stage1 surface.
-/
def fltThreeFourTerminalAudit : List String := [
  "Mathlib.NumberTheory.FLT.Three supplies fermatLastTheoremThree : FermatLastTheoremFor 3",
  "AwesomeTheorems.NumberTheory.THM_M_0387.flt3Path wraps fermatLastTheoremThree",
  "Mathlib.NumberTheory.FLT.Four supplies fermatLastTheoremFour : FermatLastTheoremFor 4",
  "AwesomeTheorems.NumberTheory.THM_M_0387.flt4Path wraps fermatLastTheoremFour",
  "status: local_wrapper_upstream_mathlib after repo-local Lean validation"
]

/--
Machine proof debt classification for this Stage1 slot.

The regular-primes repo-local integration debt is closed by the pinned
dependency and wrapper above.  The full Wiles/Taylor-Wiles route remains
formalization debt, represented by `WilesTaylorWilesFormalizationDebt`.
-/
def machineProofDebtClassification : List String := [
  "repo_local_integration_debt closed for regular primes via regularPrimesPath",
  "formalization_debt remains for Wiles/Taylor-Wiles odd-prime-exponent family",
  "no mathematical_debt: Fermat's Last Theorem is mathematically proved"
]

/-- Canonical high-risk leaf names fixed by the M0387 guideline. -/
def canonicalHighRiskLeaves : List String := [
  "raw coprime triple classification",
  "square extraction for r*s with sign cleanup",
  "strict natAbs descent hic",
  "Case II ideal-factor layer / global product to local p-th powers",
  "Case II distinguished root / p_pow_dvd_c_eta_zero",
  "Case II descent core / three-root formula and raw descent",
  "Case II close / merge / not_exists_solution'"
]

/-- Public Stage1 unchecked frontier leaf metadata. -/
structure UncheckedFrontierLeaf where
  id : String
  title : String
  status : String
  debtClass : String
  localBudget : String
deriving Repr, DecidableEq

/--
Full-FLT public frontier proposed for the Stage1 blueprint.

Every item is intentionally marked `unchecked`: these are not repo-local Lean
proof leaves, and none may be promoted before a concrete proof body, a pinned
external dependency, or an explicit integration blocker is validated.
-/
def m0387FullFrontierUncheckedLeaves : List UncheckedFrontierLeaf := [
  {
    id := "M0387-U-001",
    title := "odd-prime exponent closure target for FermatLastTheorem.of_odd_primes",
    status := "unchecked",
    debtClass := "formalization_debt",
    localBudget := "no <=100-step local proof ledger"
  },
  {
    id := "M0387-U-002",
    title := "primitive counterexample normalization for an odd prime exponent",
    status := "unchecked",
    debtClass := "formalization_debt",
    localBudget := "no <=100-step local proof ledger"
  },
  {
    id := "M0387-U-003",
    title := "Frey curve construction and invariant package",
    status := "unchecked",
    debtClass := "formalization_debt",
    localBudget := "no <=100-step local proof ledger"
  },
  {
    id := "M0387-U-004",
    title := "semistability, minimal discriminant, and conductor control for the Frey curve",
    status := "unchecked",
    debtClass := "formalization_debt",
    localBudget := "no <=100-step local proof ledger"
  },
  {
    id := "M0387-U-005",
    title := "mod-p Galois representation package attached to the Frey curve",
    status := "unchecked",
    debtClass := "formalization_debt",
    localBudget := "no <=100-step local proof ledger"
  },
  {
    id := "M0387-U-006",
    title := "semistable elliptic-curve modularity theorem over Q",
    status := "unchecked",
    debtClass := "formalization_debt",
    localBudget := "no <=100-step local proof ledger"
  },
  {
    id := "M0387-U-007",
    title := "modular forms and Hecke algebra infrastructure used by modularity",
    status := "unchecked",
    debtClass := "formalization_debt",
    localBudget := "no <=100-step local proof ledger"
  },
  {
    id := "M0387-U-008",
    title := "Taylor-Wiles deformation and R=T patching package",
    status := "unchecked",
    debtClass := "formalization_debt",
    localBudget := "no <=100-step local proof ledger"
  },
  {
    id := "M0387-U-009",
    title := "Ribet level-lowering bridge for the Frey representation",
    status := "unchecked",
    debtClass := "formalization_debt",
    localBudget := "no <=100-step local proof ledger"
  },
  {
    id := "M0387-U-010",
    title := "terminal modular-form contradiction for the lowered level",
    status := "unchecked",
    debtClass := "formalization_debt",
    localBudget := "no <=100-step local proof ledger"
  },
  {
    id := "M0387-U-011",
    title := "recompose all odd prime exponents with the checked n=4 branch",
    status := "unchecked",
    debtClass := "formalization_debt",
    localBudget := "no <=100-step local proof ledger"
  },
  {
    id := "M0387-U-012",
    title := "full-frontier validation, public merge-back, and no-integration-debt gate",
    status := "unchecked",
    debtClass := "formalization_debt",
    localBudget := "no <=100-step local proof ledger"
  }
]

/-- Public backfill section lines for the unchecked full-FLT frontier. -/
def m0387FullFrontierPublicBackfill : List String := [
  "### Full-FLT unchecked frontier for S1-M-001 / THM-M-0387",
  "- [ ] M0387-U-001: odd-prime exponent closure target for FermatLastTheorem.of_odd_primes (`unchecked`, `formalization_debt`).",
  "- [ ] M0387-U-002: primitive counterexample normalization for an odd prime exponent (`unchecked`, `formalization_debt`).",
  "- [ ] M0387-U-003: Frey curve construction and invariant package (`unchecked`, `formalization_debt`).",
  "- [ ] M0387-U-004: semistability, minimal discriminant, and conductor control for the Frey curve (`unchecked`, `formalization_debt`).",
  "- [ ] M0387-U-005: mod-p Galois representation package attached to the Frey curve (`unchecked`, `formalization_debt`).",
  "- [ ] M0387-U-006: semistable elliptic-curve modularity theorem over Q (`unchecked`, `formalization_debt`).",
  "- [ ] M0387-U-007: modular forms and Hecke algebra infrastructure used by modularity (`unchecked`, `formalization_debt`).",
  "- [ ] M0387-U-008: Taylor-Wiles deformation and R=T patching package (`unchecked`, `formalization_debt`).",
  "- [ ] M0387-U-009: Ribet level-lowering bridge for the Frey representation (`unchecked`, `formalization_debt`).",
  "- [ ] M0387-U-010: terminal modular-form contradiction for the lowered level (`unchecked`, `formalization_debt`).",
  "- [ ] M0387-U-011: recompose all odd prime exponents with the checked n=4 branch (`unchecked`, `formalization_debt`).",
  "- [ ] M0387-U-012: full-frontier validation, public merge-back, and no-integration-debt gate (`unchecked`, `formalization_debt`)."
]

/-- Canonical local validation command for public checkbox updates in this slot. -/
def m0387RunLocalValidationCommand : String :=
  "bash THM-M-0387/run_local_validation.sh"

/--
Public backfill text for the local-validation gate.

This records the command an integrator must rerun before any public checkbox
update that relies on current local build status.  It is not itself a proof of
the full FLT statement.
-/
def m0387RunLocalValidationPublicBackfill : List String := [
  "- Local validation gate: rerun `bash THM-M-0387/run_local_validation.sh` in the repository root before any public checkbox update that relies on current local build status.",
  "- The script builds `StatementAndReductionPath`, `FLT4Path`, `FLT3Path`, `RegularPrimesPath`, `SmallExponentsPath`, `Sample`, `Stage1.S1_M_001`, and the aggregator; it checks `THM-M-0387/FermatLastTheorem_Sample.lean` and runs `scripts/lint_theorem_dossier.py THM-M-0387`.",
  "- Passing this gate validates only the claimed local branches and dossier probes; the full `FermatLastTheorem` remains unchecked until the odd-prime-exponent family is supplied by a repo-local proof body or a pinned/imported/checked dependency."
]

/-- Audited external Lean 4 full-FLT project candidate. -/
def imperialCollegeLondonFltProject : String :=
  "ImperialCollegeLondon/FLT"

/-- Upstream HEAD audited for `imperialCollegeLondonFltProject` on 2026-07-10. -/
def imperialCollegeLondonFltAuditedRevision : String :=
  "44df7744a2a65cdc111875dc1b6f0db85477348f"

/--
External full-FLT integration audit for the Imperial College London Lean 4
project.  This is a blocker record, not a completion claim: the terminal
`#print axioms` report still contains `sorryAx` at the audited revision.
-/
def imperialCollegeLondonFltIntegrationAudit : List String := [
  "project: ImperialCollegeLondon/FLT",
  "status: M5 source-audited blocked exact-root candidate",
  "audited revision: 44df7744a2a65cdc111875dc1b6f0db85477348f",
  "audited date: 2026-07-10 Asia/Shanghai",
  "terminal files: FLT/Proof.lean and FermatsLastTheorem.lean",
  "terminal theorems: flt : FermatLastTheorem; PNat.pow_add_pow_ne_pow (x y z : Nat+) (n : Nat) (hn : n > 2) : x^n + y^n != z^n",
  "direct terminal blocker: B4_proof : B4 := sorry",
  "reported axioms for terminal positive-natural theorem: [knownin1980s, propext, sorryAx, Classical.choice, Quot.sound]",
  "custom-axiom blocker: knownin1980s proves an arbitrary proposition",
  "placeholder scan: 86 occurrences of sorry in 25 Lean files",
  "toolchain: Lean 4.32.0-rc1; mathlib 8bba4200986270d3b30be2bb2f8840af47a7854f",
  "reproduction limit: Lean toolchain download failed with an HTTP/2 framing error; source audit is E3, not E2",
  "required follow-up: require a new immutable revision whose exact root builds and whose terminal axiom report omits sorryAx, knownin1980s, and every disallowed custom axiom",
  "repo-local completed: false"
]

/--
Public backfill text for the external full-FLT integration gate.

This gives the serial public-doc integrator a dedicated task for the found
external project while preserving the no-`repo_local_integration_debt` gate.
-/
def m0387ExternalFullFltIntegrationPublicBackfill : List String := [
  "- [ ] `S1-M-001-C007.integration.ImperialCollegeLondon-FLT`: track `ImperialCollegeLondon/FLT` as an M5 exact-root candidate at audited revision `44df7744a2a65cdc111875dc1b6f0db85477348f`.",
  "  Blocker: `B4_proof : B4 := sorry`; the terminal wrapper depends on `[knownin1980s, propext, sorryAx, Classical.choice, Quot.sound]`; source scan found 86 `sorry` occurrences in 25 Lean files; its Lean 4.32.0-rc1 toolchain also differs from this repository.",
  "  Follow-up gate: require an immutable placeholder-free revision, an exact checked equivalence or root wrapper, and a terminal axiom report without `sorryAx`, `knownin1980s`, or other disallowed custom axioms before integration or completion."
]

/--
Status-alignment audit for README/meta/blueprint surfaces.

This is integration-ready text for a serial public-doc merge.  It deliberately
keeps the completed boundary at checked partial branches and does not promote
the full `FermatLastTheorem` statement to repo-local closure.
-/
def publicSurfaceStatusAlignmentAudit : List String := [
  "README/meta/blueprint status: partial verification only",
  "checked local branches: n = 3 via flt3Path, n = 4 via flt4Path, exponents divisible by 4 via FermatLastTheoremFor.mono, and regular primes via regularPrimesPath",
  "regular primes status: external_upstream_pinned through the pinned leanprover-community/flt-regular dependency",
  "full FermatLastTheorem status: not_repo_local_closed",
  "full theorem debt class: formalization_debt for the Wiles/Taylor-Wiles odd-prime-exponent family",
  "completion prohibition: do not mark S1-M-001 or THM-M-0387 completed from partial-branch evidence",
  "integration-debt gate: no completed public state may retain repo_local_integration_debt"
]

/--
Exact public backfill text for synchronizing README/meta/blueprint wording after
serial integration.
-/
def m0387PublicSurfaceStatusAlignmentBackfill : List String := [
  "- Public status wording for `S1-M-001 / THM-M-0387` must stay `partial` / `部分验证`: repo-local Lean validation covers the `n = 3`, `n = 4`, exponent-divisible-by-4, and pinned regular-primes branches, but it does not close the full `FermatLastTheorem`.",
  "- `README.md`, `THM-M-0387/meta.json`, and `Docs/Stage1_Blueprint.md` should use the same boundary language: checked partial branches are local or pinned-wrapper evidence; the full Wiles/Taylor-Wiles odd-prime-exponent family remains `formalization_debt` and `not_repo_local_closed`.",
  "- Do not mark the public `S1-M-001` checkbox complete until a repo-local proof body or a pinned/imported/checked external dependency closes `FermatLastTheorem`, or a precise blocker is recorded for any found external full-FLT project.",
  "- A completed public state may not retain `repo_local_integration_debt`; anchor-only external references are blockers or audit notes, not completion evidence."
]

/-! ## Audit probes -/

#check FermatLastTheoremWith
#check FermatLastTheoremFor
#check FermatLastTheorem
#check FermatLastTheoremWith.mono
#check FermatLastTheoremFor.mono
#check fermatLastTheoremWith_nat_int_rat_tfae
#check fermatLastTheoremFor_iff_int
#check fermatLastTheoremFor_iff_rat
#check fermatLastTheoremWith_of_fermatLastTheoremWith_coprime
#check dvd_c_of_prime_of_dvd_a_of_dvd_b_of_FLT
#check isCoprime_of_gcd_eq_one_of_FLT
#check FermatLastTheorem.of_odd_primes
#check fermatLastTheoremThree
#check fermatLastTheoremFour
#check regularPrimesPath
#check flt5Path
#check flt7Path
#check flt11Path
#check flt13Path
#check fltSmallExponentsPath
#check smallExponentBranch
#check regularPrimesMachineStatus
#check regularPrimesExternalUpstreamPinnedAudit
#check regularPrimesRepoLocalIntegrationDebtGate
#check checkedBranchFrontierRepoLocalIntegrationDebtGate
#check statementShape_of_oddPrimeExponentClosure
#check statementShape_iff_fermatLastTheorem
#check UncheckedFrontierLeaf
#check m0387FullFrontierUncheckedLeaves
#check m0387FullFrontierPublicBackfill
#check m0387RunLocalValidationCommand
#check m0387RunLocalValidationPublicBackfill
#check imperialCollegeLondonFltProject
#check imperialCollegeLondonFltAuditedRevision
#check imperialCollegeLondonFltIntegrationAudit
#check m0387ExternalFullFltIntegrationPublicBackfill
#check publicSurfaceStatusAlignmentAudit
#check m0387PublicSurfaceStatusAlignmentBackfill

end AwesomeTheorems.Stage1.S1_M_001
