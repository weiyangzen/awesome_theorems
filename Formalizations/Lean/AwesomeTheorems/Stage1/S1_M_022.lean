import Mathlib.NumberTheory.FLT.Basic
import Mathlib.NumberTheory.FLT.Three
import Mathlib.NumberTheory.FLT.Four
import Mathlib.NumberTheory.FLT.Polynomial
import Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass

/-!
# S1-M-022 / THM-M-0133: Wiles theorem

This Stage1 repair artifact records a conservative Lean boundary for the
Wiles/Taylor-Wiles proof of Fermat's Last Theorem.

The file does not claim a completed repo-local formalization of the
Wiles/Taylor-Wiles argument.  It freezes the terminal FLT statement shape,
names the semistable elliptic-curve modularity boundary used by the classical
route, and adds checked wrappers for the FLT reduction and the mathlib `n = 3`
and `n = 4` branches that are already in the current Lake dependency closure.
-/

namespace AwesomeTheorems.Stage1.S1_M_022

universe u

/-- Root Stage1 statement shape: Wiles/Taylor-Wiles proves Fermat's Last Theorem. -/
def StatementShape : Prop :=
  FermatLastTheorem

/--
The precise odd-prime-exponent family that, together with mathlib's `n = 4`
branch, closes the normalized FLT statement.
-/
def OddPrimeExponentClosure : Prop :=
  ∀ p : ℕ, Nat.Prime p → Odd p → FermatLastTheoremFor p

/--
The theorem-internal formalization boundary for this slot.

Mathematically this is supplied by the Wiles/Taylor-Wiles route through
modularity of semistable elliptic curves; in this repo-local Lean closure it is
kept as a proposition boundary rather than as a claimed proof.
-/
def WilesTaylorWilesFormalizationDebt : Prop :=
  OddPrimeExponentClosure

/--
Minimal semistable elliptic-curve input for the classical Wiles application.

The Weierstrass curve and ellipticity predicate are mathlib-backed objects.
Semistability, conductor control, Galois-representation attachment, and
modularity remain named proposition boundaries for later replacement by
concrete APIs or a pinned upstream theorem.
-/
structure SemistableEllipticCurveInput where
  curve : WeierstrassCurve ℚ
  isElliptic : curve.IsElliptic
  semistable : Prop
  conductor : ℕ
  residualRepresentationAttached : Prop
  modularityConclusion : Prop

/--
Semistable modularity statement shape used by the Wiles route to FLT.

This is a statement boundary only: every semistable elliptic curve over `ℚ`
with the expected arithmetic attachment has the named modularity conclusion.
-/
def SemistableModularityStatementShape : Prop :=
  ∀ E : SemistableEllipticCurveInput, E.semistable →
    E.residualRepresentationAttached → E.modularityConclusion

/--
The Frey-curve/Ribet bridge shape connecting a hypothetical FLT counterexample
to the semistable modularity contradiction.
-/
def FreyRibetBridgeShape : Prop :=
  ∀ p : ℕ, Nat.Prime p → Odd p → FermatLastTheoremFor p

/--
Pipeline boundary for the classical Wiles route.

In a future closed formalization, semistable modularity plus the Frey/Ribet
bridge should discharge the odd-prime-exponent closure.  The present artifact
keeps that implication as an explicit proposition boundary, rather than
silently treating either input as already formalized.
-/
def WilesModularityPipelineShape : Prop :=
  SemistableModularityStatementShape →
    FreyRibetBridgeShape →
      OddPrimeExponentClosure

/--
Named frontier package for the Wiles/Taylor-Wiles proof route.

This structure packages the three missing proof-frontier ingredients without
axiomatizing them globally: semistable modularity, the Frey/Ribet bridge, and
the pipeline implication from those ingredients to the odd-prime FLT closure.
-/
structure WilesModularityProofFrontier where
  semistableModularity : SemistableModularityStatementShape
  freyRibetBridge : FreyRibetBridgeShape
  closesOddPrimeExponents : WilesModularityPipelineShape

/-- Checked wrapper: a fully supplied frontier package closes the odd-prime-exponent family. -/
theorem oddPrimeExponentClosure_of_wilesFrontier
    (frontier : WilesModularityProofFrontier) : OddPrimeExponentClosure :=
  frontier.closesOddPrimeExponents frontier.semistableModularity frontier.freyRibetBridge

/-- Checked wrapper: a fully supplied frontier package implies the Stage1 terminal statement. -/
theorem statementShape_of_wilesFrontier
    (frontier : WilesModularityProofFrontier) : StatementShape :=
  FermatLastTheorem.of_odd_primes
    (oddPrimeExponentClosure_of_wilesFrontier frontier)

/-- Checked mathlib wrapper: FLT for exponent `3`. -/
theorem fltThree_mathlib_wrapper : FermatLastTheoremFor 3 :=
  fermatLastTheoremThree

/-- Checked mathlib wrapper: FLT for exponent `4`. -/
theorem fltFour_mathlib_wrapper : FermatLastTheoremFor 4 :=
  fermatLastTheoremFour

/-- Checked mathlib wrapper: exponents divisible by `4` reduce to the `n = 4` branch. -/
theorem fltForExponentDivisibleByFour {n : ℕ} (hdiv : 4 ∣ n) :
    FermatLastTheoremFor n :=
  FermatLastTheoremFor.mono hdiv fltFour_mathlib_wrapper

/--
Checked mathlib wrapper: the polynomial-ring FLT variant proves that pairwise
nonzero polynomial solutions in `k[X]` are scalar-unit multiples after removing
a common factor.  This is adjacent polynomial evidence only; it is not a Wiles
route proof for natural-number exponents.
-/
theorem polynomialFltVariant_mathlib_wrapper {k : Type u} [Field k]
    {n : ℕ} (hn : 3 ≤ n) (chn : (n : k) ≠ 0) :
    FermatLastTheoremWith' (Polynomial k) n :=
  fermatLastTheoremWith'_polynomial hn chn

/--
Checked reduction wrapper: an odd-prime-exponent closure is sufficient for the
full normalized FLT statement in mathlib.
-/
theorem statementShape_of_oddPrimeExponentClosure
    (hodd : OddPrimeExponentClosure) : StatementShape :=
  FermatLastTheorem.of_odd_primes hodd

/-- Statement-shape identity for audit tools. -/
theorem statementShape_iff_fermatLastTheorem :
    StatementShape ↔ FermatLastTheorem :=
  Iff.rfl

/-- The repo-local artifact intentionally remains below completion state. -/
def repoLocalIntegrationDebtGate : List String := [
  "no complete external Lean 4 Wiles/Taylor-Wiles proof was found in the current Lake closure",
  "therefore this slot is not completed and has no anchor-only completed state",
  "if an external proof is later found, pin/import/check it or record an integration blocker"
]

/-- Machine proof debt classification for this Stage1 slot. -/
def machineProofDebtClassification : List String := [
  "formalization_debt: full Wiles/Taylor-Wiles odd-prime-exponent family is not repo-local closed",
  "no mathematical_debt: the theorem is mathematically proved",
  "not completed: repo-local validation covers statement shape and imported partial FLT wrappers only"
]

/-- Checked local targets in this partial Stage1 artifact. -/
def checkedPartialLeanTargets : List String := [
  "StatementShape is definitionally FermatLastTheorem",
  "FermatLastTheoremFor 3 is wrapped from mathlib",
  "FermatLastTheoremFor 4 is wrapped from mathlib",
  "4-divisible exponents reduce to the n = 4 wrapper",
  "FermatLastTheoremWith' k[X] n is wrapped from Mathlib.NumberTheory.FLT.Polynomial",
  "OddPrimeExponentClosure implies StatementShape via FermatLastTheorem.of_odd_primes",
  "WilesModularityProofFrontier implies StatementShape when all frontier fields are supplied"
]

/-- M0387-level theorem-tree frontier nodes that remain unchecked for the full Wiles route. -/
def uncheckedWilesFrontierLeaves : List String := [
  "Frey package/counterexample normalization for odd prime exponents: unchecked",
  "Frey curve construction over Q with semistability/conductor control: unchecked",
  "residual Galois representation attachment to the Frey curve: unchecked",
  "Ribet level-lowering/non-modularity contradiction bridge: unchecked",
  "semistable elliptic-curve modularity theorem over Q: unchecked",
  "Taylor-Wiles deformation/Hecke R=T package supporting semistable modularity: unchecked",
  "local <=100-step proof ledgers for the preceding frontier leaves: unchecked"
]

/-- Human-readable Stage1 theorem-tree skeleton for public backfill. -/
def theoremTreeSkeleton : List String := [
  "root: FermatLastTheorem",
  "checked reduction: OddPrimeExponentClosure -> FermatLastTheorem",
  "checked special branch: FermatLastTheoremFor 3",
  "checked special branch: FermatLastTheoremFor 4",
  "unchecked frontier: WilesModularityProofFrontier",
  "unchecked leaf family: Frey/Ribet bridge plus semistable modularity",
  "unchecked terminal blocker: no hole-free Wiles/Taylor-Wiles proof in the repo-local Lake closure"
]

/--
Public theorem-tree package stub for S1-M-022-C007.

These six rows are copied from the private S1-M-022 package ledger for later
public backfill.  They intentionally preserve `unchecked` status: this is a
tree/scope artifact, not a completion claim for Wiles/Taylor-Wiles.
-/
def publicTheoremTreePackageStub : List String := [
  "S1-M-022-ROOT | FermatLastTheorem / Wiles theorem as full FLT proof chain in Lean 4 | status: unchecked",
  "S1-M-022-PKG-01 statement-normalization | freeze FermatLastTheoremWith, FermatLastTheoremFor, FermatLastTheorem, and positive-natural bridge shapes | status: unchecked",
  "S1-M-022-PKG-02 mathlib-object-model-audit | record exact statement, special-case, and reduction anchors from mathlib; separate infrastructure availability from theorem proof availability | status: unchecked",
  "S1-M-022-PKG-03 regular-primes-and-small-exponent-branch | reuse existing M0387 evidence for n = 3, n = 4, and regular primes; partial FLT evidence only, not Wiles completion | status: unchecked",
  "S1-M-022-PKG-04 Frey-curve-and-reduction-bridge | bridge not FermatLastTheorem to Frey package, irreducibility, modularity, and contradiction; external Imperial names remain incomplete-assumption anchors | status: unchecked",
  "S1-M-022-PKG-05 algebraic-geometry-and-deformation-core | schemes, sheaves, sites, deformation rings, Hecke algebras, patching, and modularity lifting; high-risk Wiles/Taylor-Wiles formalization core | status: unchecked",
  "S1-M-022-PKG-06 repo-local-closure-gate | decide between local wrapper, pinned external dependency, or blocker; completion requires local validation and public merge-back | status: unchecked"
]

/--
M0387-level local leaf-budget rows for the six-package public theorem-tree
stub.  Every row is deliberately `unchecked`; the budget is a future splitting
target, not a completed proof ledger.
-/
def publicTheoremTreeUncheckedLeafBudgetStub : List String := [
  "S1-M-022-L001 | PKG-01 | Import Mathlib.NumberTheory.FLT.Basic and expose StatementShape := FermatLastTheorem | budget <=20 | status: unchecked",
  "S1-M-022-L002 | PKG-01 | Prove expanded semiring shape definition is definitional-equivalent to mathlib's FermatLastTheoremWith | budget <=40 | status: unchecked",
  "S1-M-022-L003 | PKG-01 | Bridge FermatLastTheorem to positive-natural endpoint PNat.pow_add_pow_ne_pow shape | budget <=80 | status: unchecked",
  "S1-M-022-L004 | PKG-02 | Audit FermatLastTheoremFor.mono and divisibility exponent reduction | budget <=60 | status: unchecked",
  "S1-M-022-L005 | PKG-02 | Audit FermatLastTheorem.of_odd_primes root assembly | budget <=60 | status: unchecked",
  "S1-M-022-L006 | PKG-02 | Audit fermatLastTheoremFor_iff_int and integer transport | budget <=70 | status: unchecked",
  "S1-M-022-L007 | PKG-02 | Audit available scheme, cover, sheaf, and site modules without claiming theorem closure | budget <=50 | status: unchecked",
  "S1-M-022-L008 | PKG-03 | Reuse M0387 flt3Path as checked small-exponent branch if imported into this slot | budget <=40 | status: unchecked",
  "S1-M-022-L009 | PKG-03 | Reuse M0387 flt4Path and flt4IntPath as checked small-exponent branch if imported into this slot | budget <=40 | status: unchecked",
  "S1-M-022-L010 | PKG-03 | Reuse M0387 regularPrimesPath from pinned flt-regular if imported into this slot | budget <=50 | status: unchecked",
  "S1-M-022-L011 | PKG-03 | Record that regular-prime closure does not imply full odd-prime closure | budget <=25 | status: unchecked",
  "S1-M-022-L012 | PKG-04 | Bridge not FermatLastTheorem to a Frey package statement shape | budget <=100 | status: unchecked",
  "S1-M-022-L013 | PKG-04 | Bridge Frey package to mod-p Galois representation statement shape | budget <=100 | status: unchecked",
  "S1-M-022-L014 | PKG-04 | Record Mazur irreducibility input as an assumption/debt node unless machine-closed | budget <=70 | status: unchecked",
  "S1-M-022-L015 | PKG-04 | Record Ribet/Wiles non-irreducibility input as an assumption/debt node unless machine-closed | budget <=70 | status: unchecked",
  "S1-M-022-L016 | PKG-04 | Assemble contradiction Mazur_Frey + Wiles_Frey -> no Frey package | budget <=80 | status: unchecked",
  "S1-M-022-L017 | PKG-04 | Assemble no Frey package -> FermatLastTheorem | budget <=70 | status: unchecked",
  "S1-M-022-L018 | PKG-05 | Freeze local-ring/deformation-functor object interfaces | budget <=100 | status: unchecked",
  "S1-M-022-L019 | PKG-05 | Freeze complete local algebra and tangent-space interfaces | budget <=100 | status: unchecked",
  "S1-M-022-L020 | PKG-05 | Freeze Galois representation and residual representation interfaces | budget <=100 | status: unchecked",
  "S1-M-022-L021 | PKG-05 | Freeze Hecke algebra/action interfaces | budget <=100 | status: unchecked",
  "S1-M-022-L022 | PKG-05 | Freeze modular form / automorphic form object interfaces | budget <=100 | status: unchecked",
  "S1-M-022-L023 | PKG-05 | Freeze patching-system object and morphism interfaces | budget <=100 | status: unchecked",
  "S1-M-022-L024 | PKG-05 | Record base-change/descent lemmas needed for patching | budget <=100 | status: unchecked",
  "S1-M-022-L025 | PKG-05 | Record local-global compatibility branch as a named debt node | budget <=100 | status: unchecked",
  "S1-M-022-L026 | PKG-05 | Record modularity-lifting theorem statement shape | budget <=100 | status: unchecked",
  "S1-M-022-L027 | PKG-05 | Record semistable elliptic curve modularity bridge | budget <=100 | status: unchecked",
  "S1-M-022-L028 | PKG-06 | Check whether an external terminal theorem is sorry/axiom-free | budget <=50 | status: unchecked",
  "S1-M-022-L029 | PKG-06 | If terminal theorem is clean, pin/import/check as Lake dependency or vendor proof body | budget <=100 | status: unchecked",
  "S1-M-022-L030 | PKG-06 | If terminal theorem is not clean, record formalization blocker and keep Stage1 open | budget <=40 | status: unchecked"
]

/-- mathlib modules checked while fixing the local Lean boundary. -/
def mathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.FLT.Basic",
  "Mathlib.NumberTheory.FLT.Three",
  "Mathlib.NumberTheory.FLT.Four",
  "Mathlib.NumberTheory.FLT.Polynomial",
  "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass"
]

/-- Integration-ready public audit rows for the FLT mathlib modules named by S1-M-022-C002. -/
def mathlibFltModuleAuditRows : List String := [
  "Mathlib.NumberTheory.FLT.Basic | FermatLastTheoremWith, FermatLastTheoremFor, FermatLastTheorem, FermatLastTheoremWith.mono, FermatLastTheoremFor.mono, fermatLastTheoremFor_iff_int, fermatLastTheoremFor_iff_rat | statement/reduction API; full FermatLastTheorem is a Prop definition, not a completed Wiles proof",
  "Mathlib.NumberTheory.FLT.Three | fermatLastTheoremThree, FermatLastTheoremForThreeGen, FermatLastTheoremForThree_of_FermatLastTheoremThreeGen | checked n = 3 branch; adjacent special-case evidence only",
  "Mathlib.NumberTheory.FLT.Four | fermatLastTheoremFour, FermatLastTheoremFor.mono, FermatLastTheorem.of_odd_primes | checked n = 4 branch and odd-prime reduction assembly; odd-prime family remains Wiles/Taylor-Wiles formalization_debt",
  "Mathlib.NumberTheory.FLT.Polynomial | Polynomial.flt_catalan, Polynomial.flt, fermatLastTheoremWith'_polynomial | checked polynomial-ring FLT variant using Mason-Stothers; not a natural-number Wiles theorem proof"
]

/--
Integration-ready public audit row for S1-M-022-C003.

The M0387 FLT work gives checked adjacent branches for small exponents and
regular primes.  Those branches are useful evidence for the FLT proof graph,
but they do not supply the Wiles/Taylor-Wiles odd-prime-exponent theorem.
-/
def m0387PartialFltAdjacentEvidenceAuditRows : List String := [
  "THM-M-0387 partial FLT branches | mathlib n = 3, mathlib n = 4, and the pinned regular-prime branch through the M0387 ledger | adjacent checked evidence for special/regular-prime exponents only; not a completed Wiles/Taylor-Wiles proof, not a full FermatLastTheorem closure, and not grounds for marking S1-M-022 completed"
]

/--
Integration-ready public external audit row for S1-M-022-C004.

The named Imperial FLT revision exposes the expected terminal names, but its
top-level positive-natural FLT endpoint still reports `sorryAx` and the proof
path uses project-local assumption constants.  This is therefore an external
anchor for ongoing work, not a completed upstream proof to pin as closure.
-/
def imperialCollegeLondonFltExternalAuditRows : List String := [
  "ImperialCollegeLondon/FLT @ af3806f58145c94b97265f2e3c962be8025dd4ed | FermatsLastTheorem.lean: PNat.pow_add_pow_ne_pow; FLT/Basic/Reductions.lean: Wiles_Taylor_Wiles | external Lean 4 FLT/Wiles anchor only: the printed axioms for the terminal positive-natural theorem include sorryAx, and the route still uses project-local assumption constants such as knownin1980s, Mazur_statement, and Odlyzko_statement; do not mark S1-M-022 completed or treat this as external_upstream_pinned until a hole-free terminal theorem is pin/import/check validated in this repository, or a concrete integration blocker is recorded"
]

/--
Integration-ready public blocker row for S1-M-022-C005.

The full Wiles/Taylor-Wiles machine proof remains formalization debt while the
known Lean endpoint evidence still depends on hole markers or project-local
assumption constants.
-/
def wilesTaylorWilesFormalizationDebtBlockerRows : List String := [
  "Full Wiles/Taylor-Wiles machine proof | terminal FermatLastTheorem / odd-prime-exponent closure | blocker: remains formalization_debt while the audited terminal Lean endpoint depends on sorryAx or project-local custom axioms/assumption constants; do not mark S1-M-022 completed until a hole-free terminal theorem is pin/import/check validated in this repository, or a concrete integration blocker is recorded"
]

/--
Integration-ready public gate row for S1-M-022-C006.

This gate prevents an anchor-only external terminal theorem from being treated
as completion.  A future hole-free terminal theorem must either enter this
repository's checked dependency closure or receive a concrete integration
blocker before any public completion update.
-/
def terminalTheoremIntegrationGateRows : List String := [
  "Future hole-free Wiles/Taylor-Wiles terminal theorem | FermatLastTheorem or odd-prime-exponent FLT closure | integration gate: before any S1-M-022 completion update, pin/import/check the theorem in this repository and record the exact dependency revision, module, theorem name, and validation command; if local integration cannot be performed, record a concrete blocker such as toolchain incompatibility, dependency conflict, license barrier, or missing import path instead of treating anchor-only evidence as completed"
]

/-- Terminal theorem/search names not present as a complete Wiles route in this dependency closure. -/
def absentTerminalSearchTerms : List String := [
  "Wiles",
  "Taylor-Wiles",
  "semistable modularity",
  "Frey curve",
  "Ribet",
  "odd-prime-exponent FLT closure"
]

/-! ## Audit probes -/

#check FermatLastTheoremWith
#check FermatLastTheoremFor
#check FermatLastTheorem
#check FermatLastTheoremFor.mono
#check FermatLastTheorem.of_odd_primes
#check fermatLastTheoremThree
#check fermatLastTheoremFour
#check Polynomial.flt_catalan
#check Polynomial.flt
#check fermatLastTheoremWith'_polynomial
#check WeierstrassCurve
#check polynomialFltVariant_mathlib_wrapper
#check SemistableModularityStatementShape
#check statementShape_of_oddPrimeExponentClosure
#check WilesModularityPipelineShape
#check WilesModularityProofFrontier
#check oddPrimeExponentClosure_of_wilesFrontier
#check statementShape_of_wilesFrontier
#check m0387PartialFltAdjacentEvidenceAuditRows
#check imperialCollegeLondonFltExternalAuditRows
#check wilesTaylorWilesFormalizationDebtBlockerRows
#check terminalTheoremIntegrationGateRows
#check publicTheoremTreePackageStub
#check publicTheoremTreeUncheckedLeafBudgetStub

end AwesomeTheorems.Stage1.S1_M_022
