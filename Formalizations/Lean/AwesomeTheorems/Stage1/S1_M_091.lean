import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point
import Mathlib.AlgebraicGeometry.EllipticCurve.Reduction
import Mathlib.FieldTheory.AbsoluteGaloisGroup
import Mathlib.NumberTheory.LSeries.DirichletContinuation
import Mathlib.RingTheory.DedekindDomain.SelmerGroup

/-!
# S1-M-091 / THM-M-0445: Rubin-Kolyvagin theorem for BSD

This Stage1 artifact records a conservative Lean 4 statement-shape boundary for
the Rubin-Kolyvagin theorem family around BSD consequences for elliptic curves.

The pinned mathlib snapshot has useful substrates for Weierstrass elliptic curves,
rational point groups, Dirichlet L-functions, absolute Galois groups, and a
Dedekind-domain Selmer group.  It does not expose the terminal theorem connecting
Euler/Kolyvagin systems or Rubin's Iwasawa-theoretic input to the BSD rank and
Tate-Shafarevich finiteness conclusions for elliptic curves.

The declarations below therefore avoid proof placeholders and false completion
claims.  They freeze the formalization boundary and add only small wrappers around
checked mathlib declarations.
-/

noncomputable section

open scoped WeierstrassCurve.Affine nonZeroDivisors

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_091

universe uK uR

/-- The mathlib rational point group for a Weierstrass elliptic curve over `Q`. -/
abbrev RationalPointGroup (E : WeierstrassCurve ℚ) [E.IsElliptic] : Type :=
  E⟮ℚ⟯

/--
Abstract BSD data for the portion of BSD controlled by the Rubin-Kolyvagin
theorem family.

The numeric fields deliberately do not define analytic rank or Mordell-Weil rank
from first principles.  Those APIs are not available in the local mathlib closure
for elliptic curves.  A future terminal proof must replace these fields by the
actual order of vanishing of the elliptic-curve L-function, the rank of `E(Q)`,
and the Tate-Shafarevich group.
-/
structure BSDRankShaData (E : WeierstrassCurve ℚ) [E.IsElliptic] where
  analyticRank : ℕ
  mordellWeilRank : ℕ
  tateShafarevichFinite : Prop
  leadingTermFormula : Prop

namespace BSDRankShaData

variable {E : WeierstrassCurve ℚ} [E.IsElliptic]

/-- The BSD rank equality component. -/
def RankEquality (D : BSDRankShaData E) : Prop :=
  D.mordellWeilRank = D.analyticRank

/-- The Tate-Shafarevich finiteness component. -/
def ShaFiniteness (D : BSDRankShaData E) : Prop :=
  D.tateShafarevichFinite

/--
The stronger BSD leading-term component.

This is retained as a separate field because the classical Kolyvagin/Rubin
package usually closes rank and finiteness consequences before the full leading
coefficient formula has a formal object model.
-/
def LeadingTermFormula (D : BSDRankShaData E) : Prop :=
  D.leadingTermFormula

end BSDRankShaData

/--
Abstract boundary for the elliptic-curve Hasse-Weil L-function side of BSD.

The current mathlib snapshot has general `LSeries` and Dirichlet L-functions, but
not the canonical Hasse-Weil L-function attached to a Weierstrass elliptic curve
over `ℚ`.  This structure separates the future API into the exact components
needed by the Rubin-Kolyvagin/BSD statement: arithmetic coefficients, Euler
factors, continuation, functional equation, analytic rank at `s = 1`, and the
leading coefficient.
-/
structure EllipticHasseWeilLFunctionData (E : WeierstrassCurve ℚ) [E.IsElliptic] where
  coefficient : ℕ → ℂ
  localEulerFactorAt : ℕ → ℂ → ℂ
  hasseWeilLFunction : ℂ → ℂ
  agreesWithNaiveLSeriesOnConvergenceHalfPlane : Prop
  hasAnalyticContinuation : Prop
  satisfiesFunctionalEquation : Prop
  analyticRankAtOne : ℕ
  orderOfVanishingAtOne_is_analyticRank : Prop
  leadingCoefficientAtOne : ℂ
  leadingCoefficientMatchesBSDFormula : Prop

namespace EllipticHasseWeilLFunctionData

variable {E : WeierstrassCurve ℚ} [E.IsElliptic]

/-- The naive Dirichlet series attached to the abstract Hasse-Weil coefficients. -/
noncomputable def naiveLSeries (L : EllipticHasseWeilLFunctionData E) (s : ℂ) : ℂ :=
  LSeries L.coefficient s

/-- The local Euler factor supplied by the abstract Hasse-Weil boundary. -/
def localEulerFactor (L : EllipticHasseWeilLFunctionData E) (p : ℕ) (s : ℂ) : ℂ :=
  L.localEulerFactorAt p s

/-- The analytic-rank value exposed by the abstract Hasse-Weil boundary. -/
def AnalyticRank (L : EllipticHasseWeilLFunctionData E) : ℕ :=
  L.analyticRankAtOne

/-- Bridge saying the BSD rank datum uses the Hasse-Weil analytic rank. -/
def MatchesBSDAnalyticRank (L : EllipticHasseWeilLFunctionData E)
    (D : BSDRankShaData E) : Prop :=
  D.analyticRank = L.AnalyticRank

/-- Checked unfolding of the naive `LSeries` wrapper. -/
theorem naiveLSeries_eq_LSeries (L : EllipticHasseWeilLFunctionData E) (s : ℂ) :
    L.naiveLSeries s = LSeries L.coefficient s :=
  rfl

end EllipticHasseWeilLFunctionData

/--
Formal input boundary for a Rubin-Kolyvagin BSD implication.

The proposition fields isolate the currently missing formal APIs: analytic rank
`≤ 1`, Euler-system/Kolyvagin-system hypotheses, Rubin-style CM/Iwasawa input
when needed, and local/global Selmer-control lemmas.
-/
structure RubinKolyvaginBSDInput (E : WeierstrassCurve ℚ) [E.IsElliptic] where
  bsdData : BSDRankShaData E
  hasseWeilLFunctionData : EllipticHasseWeilLFunctionData E
  analyticRankMatchesHasseWeil : Prop
  analyticRankAtMostOne : Prop
  eulerOrKolyvaginSystemHypotheses : Prop
  rubinCMOrIwasawaInput : Prop
  localGlobalSelmerControl : Prop

namespace RubinKolyvaginBSDInput

variable {E : WeierstrassCurve ℚ} [E.IsElliptic]

/--
The rank-and-Sha-finiteness conclusion normally associated with the
Rubin-Kolyvagin theorem family.
-/
def RankAndShaFiniteConclusion (I : RubinKolyvaginBSDInput E) : Prop :=
  I.analyticRankMatchesHasseWeil →
    I.hasseWeilLFunctionData.agreesWithNaiveLSeriesOnConvergenceHalfPlane →
      I.hasseWeilLFunctionData.hasAnalyticContinuation →
        I.hasseWeilLFunctionData.orderOfVanishingAtOne_is_analyticRank →
          I.analyticRankAtMostOne →
    I.eulerOrKolyvaginSystemHypotheses →
      I.rubinCMOrIwasawaInput →
        I.localGlobalSelmerControl →
          I.bsdData.RankEquality ∧ I.bsdData.ShaFiniteness

/--
Optional strengthened conclusion including the BSD leading-term formula.

This is intentionally separate from `RankAndShaFiniteConclusion`; the local
artifact does not claim that mathlib has the elliptic-curve L-function,
Tate-Shafarevich group, regulator, Tamagawa factors, or period formalized in the
needed form.
-/
def FullBSDConclusion (I : RubinKolyvaginBSDInput E) : Prop :=
  I.RankAndShaFiniteConclusion ∧
    (I.analyticRankMatchesHasseWeil →
      I.hasseWeilLFunctionData.agreesWithNaiveLSeriesOnConvergenceHalfPlane →
        I.hasseWeilLFunctionData.hasAnalyticContinuation →
          I.hasseWeilLFunctionData.satisfiesFunctionalEquation →
            I.hasseWeilLFunctionData.orderOfVanishingAtOne_is_analyticRank →
              I.hasseWeilLFunctionData.leadingCoefficientMatchesBSDFormula →
                I.analyticRankAtMostOne →
                  I.eulerOrKolyvaginSystemHypotheses →
                    I.rubinCMOrIwasawaInput →
                      I.localGlobalSelmerControl →
                        I.bsdData.LeadingTermFormula)

end RubinKolyvaginBSDInput

/--
Stage1 statement shape for the Rubin-Kolyvagin BSD theorem family.

This is a proposition boundary only.  A terminal theorem must instantiate the
abstract input fields with concrete elliptic-curve L-functions, Mordell-Weil
rank, Tate-Shafarevich group, Euler/Kolyvagin systems, and local Selmer
conditions, or import a pinned Lean 4 proof supplying those objects.
-/
def StatementShape : Prop :=
  ∀ (E : WeierstrassCurve ℚ) [E.IsElliptic],
    ∀ I : RubinKolyvaginBSDInput E, I.RankAndShaFiniteConclusion

/-- Variant statement shape for an eventual full BSD leading-term conclusion. -/
def FullBSDStatementShape : Prop :=
  ∀ (E : WeierstrassCurve ℚ) [E.IsElliptic],
    ∀ I : RubinKolyvaginBSDInput E, I.FullBSDConclusion

/-- Checked wrapper: rational points on a Weierstrass elliptic curve form an additive group. -/
@[reducible]
def rationalPointAddCommGroup (E : WeierstrassCurve ℚ) [E.IsElliptic] :
    AddCommGroup (RationalPointGroup E) :=
  inferInstance

/-- Checked wrapper: a Weierstrass elliptic curve has unit discriminant. -/
theorem elliptic_discriminant_isUnit (E : WeierstrassCurve ℚ) [E.IsElliptic] :
    IsUnit E.Δ :=
  E.isUnit_Δ

/-- The absolute Galois group object currently available in mathlib. -/
abbrev AbsoluteGaloisGroup (K : Type uK) [Field K] : Type uK :=
  Field.absoluteGaloisGroup K

/--
The Dedekind-domain Selmer group available in mathlib.

This is not the elliptic-curve Galois-cohomological Selmer group used in the
terminal Rubin-Kolyvagin theorem, but it is a checked Selmer-group substrate in
the pinned local dependency closure.
-/
abbrev DedekindSelmerGroup
    (R : Type uR) [CommRing R] [IsDedekindDomain R]
    (K : Type uK) [Field K] [Algebra R K] [IsFractionRing R K]
    (S : Set (IsDedekindDomain.HeightOneSpectrum R)) (n : ℕ) :
    Subgroup (Kˣ ⧸ (powMonoidHom n : Kˣ →* Kˣ).range) :=
  @IsDedekindDomain.selmerGroup R _ _ K _ _ _ S n

/-- Checked wrapper: Selmer groups are monotone in the allowed set of primes. -/
theorem dedekindSelmerGroup_monotone
    (R : Type uR) [CommRing R] [IsDedekindDomain R]
    (K : Type uK) [Field K] [Algebra R K] [IsFractionRing R K]
    {S S' : Set (IsDedekindDomain.HeightOneSpectrum R)} {n : ℕ} (hS : S ≤ S') :
    DedekindSelmerGroup R K S n ≤ DedekindSelmerGroup R K S' n := by
  exact IsDedekindDomain.selmerGroup.monotone (K := K) (n := n) hS

/--
Checked adjacent L-function wrapper.

This is only a Dirichlet L-function theorem, not the Hasse-Weil L-function of an
elliptic curve needed for BSD.
-/
theorem dirichlet_LFunction_differentiable_anchor {N : ℕ} [NeZero N]
    {χ : DirichletCharacter ℂ N} (hχ : χ ≠ 1) :
    Differentiable ℂ (DirichletCharacter.LFunction χ) :=
  DirichletCharacter.differentiable_LFunction hχ

/-- The local Lean toolchain used for this Stage1 audit. -/
def leanToolchainVersion : String :=
  "leanprover/lean4:v4.29.0"

/-- The pinned mathlib repository recorded by `lake-manifest.json`. -/
def mathlibPinnedRepository : String :=
  "https://github.com/leanprover-community/mathlib4.git"

/-- The pinned mathlib revision recorded by `lake-manifest.json`. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point",
  "Mathlib.AlgebraicGeometry.EllipticCurve.Reduction",
  "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass",
  "Mathlib.FieldTheory.AbsoluteGaloisGroup",
  "Mathlib.NumberTheory.LSeries.Basic",
  "Mathlib.NumberTheory.LSeries.DirichletContinuation",
  "Mathlib.NumberTheory.ModularForms.Basic",
  "Mathlib.NumberTheory.NumberField.AdeleRing",
  "Mathlib.NumberTheory.LocalField.Basic",
  "Mathlib.RingTheory.DedekindDomain.SelmerGroup"
]

/-- Search terms that did not locate a terminal Rubin-Kolyvagin/BSD theorem in mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Rubin",
  "Kolyvagin",
  "Birch",
  "Swinnerton",
  "BSD",
  "TateShafarevich",
  "Tate-Shafarevich",
  "MordellWeil",
  "Heegner",
  "EulerSystem",
  "KolyvaginSystem"
]

/-- Missing API leaves for an eventual elliptic Hasse-Weil L-function formalization. -/
inductive EllipticHasseWeilMissingAPI where
  | arithmeticCoefficients
  | localEulerFactors
  | conductorAndBadReduction
  | globalHasseWeilLFunction
  | convergenceRegionComparison
  | analyticContinuation
  | functionalEquation
  | analyticRankOrderOfVanishing
  | leadingCoefficientBSDFormula
  | modularityOrAutomorphicBridge
  deriving DecidableEq, Repr

namespace EllipticHasseWeilMissingAPI

/-- Stable label for public and private audit surfaces. -/
def label : EllipticHasseWeilMissingAPI → String
  | arithmeticCoefficients => "M0445-HW-arithmetic-coefficients"
  | localEulerFactors => "M0445-HW-local-Euler-factors"
  | conductorAndBadReduction => "M0445-HW-conductor-and-bad-reduction"
  | globalHasseWeilLFunction => "M0445-HW-global-L-function"
  | convergenceRegionComparison => "M0445-HW-convergence-region-comparison"
  | analyticContinuation => "M0445-HW-analytic-continuation"
  | functionalEquation => "M0445-HW-functional-equation"
  | analyticRankOrderOfVanishing => "M0445-HW-analytic-rank-order-of-vanishing"
  | leadingCoefficientBSDFormula => "M0445-HW-leading-coefficient-BSD-formula"
  | modularityOrAutomorphicBridge => "M0445-HW-modularity-or-automorphic-bridge"

/-- Concrete next action needed to close each missing Hasse-Weil API leaf. -/
def requiredNextAction : EllipticHasseWeilMissingAPI → String
  | arithmeticCoefficients =>
      "define the elliptic-curve coefficients a_n from point counts or Frobenius traces"
  | localEulerFactors =>
      "define good, multiplicative, and additive local Euler factors with reduction data"
  | conductorAndBadReduction =>
      "connect minimal models, conductor exponents, and bad-reduction classifications"
  | globalHasseWeilLFunction =>
      "construct the canonical Hasse-Weil L-function attached to E over Q"
  | convergenceRegionComparison =>
      "prove agreement with the naive coefficient LSeries on the initial half-plane"
  | analyticContinuation =>
      "prove or import analytic continuation of the elliptic Hasse-Weil L-function"
  | functionalEquation =>
      "prove or import the completed functional equation and root number"
  | analyticRankOrderOfVanishing =>
      "define analytic rank as the order of vanishing at s = 1"
  | leadingCoefficientBSDFormula =>
      "define the leading coefficient and relate it to the BSD formula terms"
  | modularityOrAutomorphicBridge =>
      "supply the modularity or automorphic bridge used to obtain the analytic package"

end EllipticHasseWeilMissingAPI

/-- The complete C003 missing-API split for the elliptic Hasse-Weil L-function side. -/
def ellipticHasseWeilMissingAPISplit : List EllipticHasseWeilMissingAPI := [
  .arithmeticCoefficients,
  .localEulerFactors,
  .conductorAndBadReduction,
  .globalHasseWeilLFunction,
  .convergenceRegionComparison,
  .analyticContinuation,
  .functionalEquation,
  .analyticRankOrderOfVanishing,
  .leadingCoefficientBSDFormula,
  .modularityOrAutomorphicBridge
]

/-- Audit gate for child `S1-M-091-C003`. -/
structure C003HasseWeilAPIGate where
  abstractBoundaryInLean : Bool
  naiveLSeriesWrapperChecked : Bool
  missingAPISplitRecorded : Bool
  terminalEllipticHasseWeilAPI : Bool
  repoLocalCompletionClaimed : Bool
  debtClassification : String
  blocker : String
  missingLeaves : List EllipticHasseWeilMissingAPI

/--
C003 gate result: the missing API is split and the local abstract boundary is
checked, but the terminal elliptic Hasse-Weil L-function API remains open.
-/
def c003HasseWeilAPIGate : C003HasseWeilAPIGate where
  abstractBoundaryInLean := true
  naiveLSeriesWrapperChecked := true
  missingAPISplitRecorded := true
  terminalEllipticHasseWeilAPI := false
  repoLocalCompletionClaimed := false
  debtClassification := "formalization_debt"
  blocker :=
    "pinned mathlib has general LSeries and Dirichlet L-functions, not the elliptic-curve Hasse-Weil L-function package needed by BSD"
  missingLeaves := ellipticHasseWeilMissingAPISplit

/-- Checked guard: C003 records formalization debt only and makes no completion claim. -/
theorem c003HasseWeilAPIGate_no_completion_claim :
    c003HasseWeilAPIGate.repoLocalCompletionClaimed = false ∧
      c003HasseWeilAPIGate.terminalEllipticHasseWeilAPI = false :=
  And.intro rfl rfl

/-- Search terms required by child `S1-M-091-C004` for the Rubin external audit. -/
def c004RubinExternalAuditSearchTerms : List String := [
  "Rubin",
  "Kolyvagin",
  "BSD",
  "Birch",
  "Swinnerton",
  "TateShafarevich",
  "Tate-Shafarevich",
  "MordellWeil",
  "Heegner",
  "EulerSystem",
  "KolyvaginSystem",
  "WeierstrassCurve"
]

/-- External-audit gate for child `S1-M-091-C004`. -/
structure C004RubinExternalAuditGate where
  localMathlibSearched : Bool
  localFltRegularSearched : Bool
  githubCliAuthenticated : Bool
  githubTokenConfigured : Bool
  githubCodeSearchAuthenticated : Bool
  githubRepositorySearchReturnedCandidate : Bool
  sameNameRubinCandidateRejected : Bool
  externalLeanClosureFound : Bool
  externalUpstreamPinned : Bool
  repoLocalCompletionClaimed : Bool
  debtClassification : String
  blocker : String
  searchTerms : List String

/--
C004 gate result: local primary dependencies were searched and no external Lean
closure is claimed. Authenticated GitHub code search was blocked because the
environment had neither `gh` login nor a configured GitHub token.
-/
def c004RubinExternalAuditGate : C004RubinExternalAuditGate where
  localMathlibSearched := true
  localFltRegularSearched := true
  githubCliAuthenticated := false
  githubTokenConfigured := false
  githubCodeSearchAuthenticated := false
  githubRepositorySearchReturnedCandidate := true
  sameNameRubinCandidateRejected := true
  externalLeanClosureFound := false
  externalUpstreamPinned := false
  repoLocalCompletionClaimed := false
  debtClassification := "formalization_debt_with_authenticated_external_audit_blocker"
  blocker :=
    "gh auth status reports no GitHub login and no GH_TOKEN/GITHUB_TOKEN-style environment variable is configured; unauthenticated repository search found adri326/rubin-lean4, but its README identifies the topological group-action Rubin theorem, not the Rubin-Kolyvagin/BSD theorem; authenticated GitHub code search for Rubin must be rerun before public completion"
  searchTerms := c004RubinExternalAuditSearchTerms

/-- Checked guard: C004 makes no external-anchor or completion claim. -/
theorem c004RubinExternalAuditGate_no_completion_claim :
    c004RubinExternalAuditGate.externalLeanClosureFound = false ∧
      c004RubinExternalAuditGate.externalUpstreamPinned = false ∧
        c004RubinExternalAuditGate.repoLocalCompletionClaimed = false :=
  And.intro rfl (And.intro rfl rfl)

/-- Repo-local integration gate for child `S1-M-091-C005`. -/
structure C005RubinIntegrationGate where
  c004ExternalAuditUsed : Bool
  lakeHasOnlyMathlibAndFltRegularExternalProofDeps : Bool
  sameNameRubinCandidateRejected : Bool
  pinReadyExternalRubinKolyvaginClosureFound : Bool
  externalUpstreamPinned : Bool
  repoLocalCompletionClaimed : Bool
  debtClassification : String
  blocker : String
  requiredActionIfClosureAppears : String

/--
C005 gate result: no pin-ready external Lean 4 proof closure for the
Rubin-Kolyvagin/BSD implication is available to import in this repository pass.

The gate therefore records a blocker rather than creating an anchor-only
completion claim.
-/
def c005RubinIntegrationGate : C005RubinIntegrationGate where
  c004ExternalAuditUsed := true
  lakeHasOnlyMathlibAndFltRegularExternalProofDeps := true
  sameNameRubinCandidateRejected := true
  pinReadyExternalRubinKolyvaginClosureFound := false
  externalUpstreamPinned := false
  repoLocalCompletionClaimed := false
  debtClassification := "formalization_debt_with_external_audit_blocker"
  blocker :=
    "the current Lake closure contains mathlib and flt-regular only; C004 found no pin-ready Lean 4 Rubin-Kolyvagin/BSD proof closure and rejected adri326/rubin-lean4 as a different Rubin theorem about topological group actions"
  requiredActionIfClosureAppears :=
    "pin the exact external repository revision in Lake or vendor the proof body, import the terminal theorem, add a local wrapper for StatementShape or FullBSDStatementShape, and rerun local Lean validation before any completion claim"

/-- Checked guard: C005 leaves no anchor-only external proof as a completed state. -/
theorem c005RubinIntegrationGate_no_completion_claim :
    c005RubinIntegrationGate.pinReadyExternalRubinKolyvaginClosureFound = false ∧
      c005RubinIntegrationGate.externalUpstreamPinned = false ∧
        c005RubinIntegrationGate.repoLocalCompletionClaimed = false :=
  And.intro rfl (And.intro rfl rfl)

#check EllipticHasseWeilLFunctionData
#check EllipticHasseWeilLFunctionData.naiveLSeries_eq_LSeries
#check EllipticHasseWeilMissingAPI
#check ellipticHasseWeilMissingAPISplit
#check c003HasseWeilAPIGate_no_completion_claim
#check c004RubinExternalAuditGate_no_completion_claim
#check c005RubinIntegrationGate_no_completion_claim

end S1_M_091
end Stage1
end AwesomeTheorems
