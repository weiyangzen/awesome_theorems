import Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass
import Mathlib.AlgebraicGeometry.EllipticCurve.Jacobian.Basic
import Mathlib.FieldTheory.AbsoluteGaloisGroup
import Mathlib.NumberTheory.Cyclotomic.Gal
import Mathlib.NumberTheory.LocalField.Basic
import Mathlib.NumberTheory.LSeries.Basic
import Mathlib.NumberTheory.NumberField.AdeleRing
import Mathlib.RingTheory.DedekindDomain.SelmerGroup
import Mathlib.RingTheory.ClassGroup

/-!
# S1-M-090 / THM-M-0444: Kolyvagin Euler systems

This Stage1 file records a conservative Lean statement-shape boundary for the
construction of Kolyvagin Euler systems.  The pinned mathlib snapshot contains
useful local substrates for absolute Galois groups, Dedekind-domain Selmer groups,
and Weierstrass elliptic curves, but it does not provide a terminal Euler-system
or Kolyvagin-system construction theorem.

The declarations below therefore avoid proof placeholders and false completion claims:
they define the data a later proof or pinned dependency must supply, plus a few
small wrappers around existing mathlib facts.
-/

open scoped nonZeroDivisors

universe uK uR uT uI v

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_090

/-- The absolute Galois group object currently available in mathlib. -/
abbrev AbsoluteGaloisGroup (K : Type uK) [Field K] : Type uK :=
  Field.absoluteGaloisGroup K

/--
The Dedekind-domain Selmer group already available in mathlib.

This is not the full Galois-cohomological Selmer group used in Kolyvagin's
method, but it is a checked arithmetic Selmer-group substrate in the pinned
mathlib revision.
-/
abbrev DedekindSelmerGroup
    (R : Type uR) [CommRing R] [IsDedekindDomain R]
    (K : Type uK) [Field K] [Algebra R K] [IsFractionRing R K]
    (S : Set (IsDedekindDomain.HeightOneSpectrum R)) (n : ℕ) :
    Subgroup (Kˣ ⧸ (powMonoidHom n : Kˣ →* Kˣ).range) :=
  @IsDedekindDomain.selmerGroup R _ _ K _ _ _ S n

/-- Monotonicity of the checked Dedekind-domain Selmer group with respect to the allowed set. -/
theorem dedekindSelmerGroup_monotone
    (R : Type uR) [CommRing R] [IsDedekindDomain R]
    (K : Type uK) [Field K] [Algebra R K] [IsFractionRing R K]
    {S S' : Set (IsDedekindDomain.HeightOneSpectrum R)} {n : ℕ} (hS : S ≤ S') :
    DedekindSelmerGroup R K S n ≤ DedekindSelmerGroup R K S' n := by
  exact IsDedekindDomain.selmerGroup.monotone (K := K) (n := n) hS

/--
Abstract data package for a future formal construction of Kolyvagin classes
from an Euler system.

The fields are intentionally abstract.  They isolate the formalization boundary:
one must later replace the index set, norm relation, derivative operators, local
conditions, and Selmer-control conclusion by concrete Galois-cohomological
definitions or by a checked upstream Lean 4 theorem.
-/
structure KolyvaginEulerSystemConstructionData
    (BaseField : Type uK) (Coeff : Type uR) (T : Type uT)
    [Field BaseField] [CommRing Coeff] [AddCommGroup T] [Module Coeff T] :
    Type (max (max (max uK uR) uT) (uI + 1)) where
  AuxiliaryIndex : Type uI
  IsAdmissible : AuxiliaryIndex → Prop
  DividesLevel : AuxiliaryIndex → AuxiliaryIndex → Prop
  EulerClass : AuxiliaryIndex → T
  KolyvaginClass : AuxiliaryIndex → T
  NormRelation : AuxiliaryIndex → AuxiliaryIndex → T → T → Prop
  DerivativeOperator : AuxiliaryIndex → T → T
  LocalSelmerCondition : AuxiliaryIndex → T → Prop
  SelmerControlConclusion : Prop
  norm_compatible :
    ∀ {m n}, DividesLevel m n → IsAdmissible m → IsAdmissible n →
      NormRelation m n (EulerClass m) (EulerClass n)
  kolyvagin_class_eq_derivative :
    ∀ n, IsAdmissible n → KolyvaginClass n = DerivativeOperator n (EulerClass n)
  kolyvagin_class_local :
    ∀ n, IsAdmissible n → LocalSelmerCondition n (KolyvaginClass n)
  selmer_control :
    (∀ n, IsAdmissible n → LocalSelmerCondition n (KolyvaginClass n)) →
      SelmerControlConclusion

/--
Stage1 statement-shape candidate for "construction of Kolyvagin Euler systems".

This is a namespace-level formal target only.  It says that, for a field, a
coefficient ring, and a coefficient module, the expected construction data exist.
It is deliberately weaker than a terminal theorem until the abstract fields above
are replaced by concrete arithmetic geometry APIs or by a pinned Lean 4 proof.
-/
def StatementShape
    (BaseField : Type uK) (Coeff : Type uR) (T : Type uT)
    [Field BaseField] [CommRing Coeff] [AddCommGroup T] [Module Coeff T] : Prop :=
  Nonempty (KolyvaginEulerSystemConstructionData.{uK, uR, uT, uI} BaseField Coeff T)

/-- The statement-shape definition unfolds to nonemptiness of the abstract construction data. -/
theorem statementShape_iff_nonempty
    (BaseField : Type uK) (Coeff : Type uR) (T : Type uT)
    [Field BaseField] [CommRing Coeff] [AddCommGroup T] [Module Coeff T] :
    StatementShape.{uK, uR, uT, uI} BaseField Coeff T ↔
      Nonempty (KolyvaginEulerSystemConstructionData.{uK, uR, uT, uI} BaseField Coeff T) :=
  Iff.rfl

/-!
## Statement normalization boundary

The public Stage1 statement for `THM-M-0444` should currently be normalized to
`AwesomeTheorems.Stage1.S1_M_090.StatementShape`.  This boundary only asserts
nonemptiness of the abstract `KolyvaginEulerSystemConstructionData` package above:
Euler classes, Kolyvagin classes, norm compatibility, derivative operators, local
conditions, and a Selmer-control conclusion are fields supplied by future APIs or a
pinned upstream theorem.

Consequently this Lean artifact is a checked statement-shape target, not a terminal
Kolyvagin Euler-system construction theorem.  A completion claim still requires
concrete Galois-cohomological definitions, finite/singular local conditions,
Kolyvagin/admissible prime machinery, and a checked Selmer-control theorem inside
the repo-local Lake closure.
-/

/-- Checked wrapper around the standard Weierstrass discriminant identity in mathlib. -/
theorem weierstrass_c_relation
    (R : Type v) [CommRing R] (W : WeierstrassCurve R) :
    1728 * W.Δ = W.c₄ ^ 3 - W.c₆ ^ 2 := by
  exact W.c_relation

/-- Pinned mathlib revision used by the Stage1 audit for `THM-M-0444`. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.FieldTheory.AbsoluteGaloisGroup",
  "Mathlib.RingTheory.DedekindDomain.SelmerGroup",
  "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass",
  "Mathlib.AlgebraicGeometry.EllipticCurve.Jacobian.Basic",
  "Mathlib.NumberTheory.Cyclotomic.Gal",
  "Mathlib.NumberTheory.LocalField.Basic",
  "Mathlib.NumberTheory.NumberField.AdeleRing",
  "Mathlib.NumberTheory.LSeries.Basic",
  "Mathlib.RingTheory.ClassGroup"
]

/-- Public-facing short module labels from the `THM-M-0444.mathlib-audit` child task. -/
def mathlibAuditShortModuleLabels : List String := [
  "AbsoluteGaloisGroup",
  "DedekindDomain.SelmerGroup",
  "EllipticCurve.Weierstrass",
  "EllipticCurve.Jacobian",
  "Cyclotomic.Gal",
  "LocalField.Basic",
  "NumberField.AdeleRing",
  "LSeries.Basic",
  "ClassGroup"
]

/-!
## Missing formal API split

The terminal theorem is blocked by several independent API families.  The
checked declarations below make that split explicit for the public
`THM-M-0444.missing-api` backfill task.  They are audit metadata only: no entry
below is a proof that the corresponding API already exists in this repository.
-/

/-- Coarse formal API blocks still needed for a terminal Kolyvagin Euler-system theorem. -/
inductive MissingAPIBlock where
  | galoisCohomology
  | corestrictionNormMaps
  | eulerSystemIndexing
  | kolyvaginAdmissiblePrimes
  | derivativeOperators
  | finiteSingularLocalConditions
  | terminalSelmerControlTheorem
  deriving DecidableEq, Repr

/-- One integration-ready row in the missing-API inventory for `THM-M-0444`. -/
structure MissingAPIRequirement where
  block : MissingAPIBlock
  publicLabel : String
  currentRepoLocalBoundary : String
  requiredConcreteAPI : String
  closureGate : String
  deriving Repr

/--
Integration-ready split of the missing formal APIs for Kolyvagin Euler systems.

The entries are intentionally phrased as requirements, not as completed anchors.
-/
def missingAPIRequirements : List MissingAPIRequirement := [
  {
    block := MissingAPIBlock.galoisCohomology
    publicLabel := "Galois cohomology"
    currentRepoLocalBoundary := "The coefficient module T in StatementShape is abstract."
    requiredConcreteAPI :=
      "Continuous Galois cohomology groups, cocycles, coboundaries, H^1 classes, and functorial maps for arithmetic Galois modules."
    closureGate :=
      "Replace the abstract T/EulerClass fields by classes in a checked Galois-cohomological object or import a pinned theorem providing them."
  },
  {
    block := MissingAPIBlock.corestrictionNormMaps
    publicLabel := "Corestriction/norm maps"
    currentRepoLocalBoundary := "NormRelation is an abstract relation between two Euler classes."
    requiredConcreteAPI :=
      "Corestriction, restriction, and arithmetic norm maps across the selected field/conductor tower, with compatibility lemmas."
    closureGate :=
      "Prove the Euler-system norm relation using concrete maps, not an abstract NormRelation field."
  },
  {
    block := MissingAPIBlock.eulerSystemIndexing
    publicLabel := "Euler-system indexing"
    currentRepoLocalBoundary := "AuxiliaryIndex, IsAdmissible, and DividesLevel are abstract fields."
    requiredConcreteAPI :=
      "A concrete index category such as squarefree conductors, finite extensions, or admissible level data with divisibility/order structure."
    closureGate :=
      "Instantiate the EulerClass family over the concrete index set and validate its functorial/conductor bookkeeping."
  },
  {
    block := MissingAPIBlock.kolyvaginAdmissiblePrimes
    publicLabel := "Kolyvagin/admissible primes"
    currentRepoLocalBoundary := "IsAdmissible is an uninterpreted predicate on AuxiliaryIndex."
    requiredConcreteAPI :=
      "Prime splitting, congruence, ramification, squarefree product, and Kolyvagin-prime admissibility predicates with closure lemmas."
    closureGate :=
      "Replace IsAdmissible by checked prime-level conditions strong enough for derivative classes and local comparisons."
  },
  {
    block := MissingAPIBlock.derivativeOperators
    publicLabel := "Derivative operators"
    currentRepoLocalBoundary := "DerivativeOperator is an abstract endomorphism of T for each index."
    requiredConcreteAPI :=
      "Group-ring or Galois-operator derivative constructions, plus commutation and norm-compatibility lemmas."
    closureGate :=
      "Define KolyvaginClass from the concrete derivative operator and prove the derivative-class equation locally."
  },
  {
    block := MissingAPIBlock.finiteSingularLocalConditions
    publicLabel := "Finite/singular local conditions"
    currentRepoLocalBoundary := "LocalSelmerCondition is a single abstract predicate on classes."
    requiredConcreteAPI :=
      "Local cohomology, finite and singular subgroups or quotients, localization maps, and comparison exactness at Kolyvagin primes."
    closureGate :=
      "Show each derived class satisfies the intended local Selmer condition or finite/singular comparison theorem."
  },
  {
    block := MissingAPIBlock.terminalSelmerControlTheorem
    publicLabel := "Terminal Selmer-control theorem"
    currentRepoLocalBoundary := "SelmerControlConclusion and selmer_control are abstract fields."
    requiredConcreteAPI :=
      "The final theorem bounding or controlling the relevant Selmer group from the constructed Kolyvagin system."
    closureGate :=
      "Prove or pin/import/check the terminal Selmer-control theorem inside the repo-local Lake closure before any completion claim."
  }
]

/-- The missing-API split has exactly the seven public blocks requested for this child task. -/
theorem missingAPIRequirements_blocks :
    missingAPIRequirements.map (fun row => row.block) = [
      MissingAPIBlock.galoisCohomology,
      MissingAPIBlock.corestrictionNormMaps,
      MissingAPIBlock.eulerSystemIndexing,
      MissingAPIBlock.kolyvaginAdmissiblePrimes,
      MissingAPIBlock.derivativeOperators,
      MissingAPIBlock.finiteSingularLocalConditions,
      MissingAPIBlock.terminalSelmerControlTheorem
    ] :=
  rfl

/-- The checked missing-API inventory contains seven rows. -/
theorem missingAPIRequirements_length : missingAPIRequirements.length = 7 :=
  rfl

/-- Search terms that did not locate a terminal Kolyvagin/Euler-system theorem in mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Kolyvagin",
  "EulerSystem",
  "Euler system",
  "KolyvaginSystem",
  "Heegner",
  "TateShafarevich",
  "Iwasawa"
]

/-!
## External Lean 4 audit boundary

The public `THM-M-0444.external-audit` child requires authenticated primary-source
Lean 4 searches.  The declarations below only preserve the exact requested search
surface and the repo-local integration gate.  They are not a certificate that an
authenticated external-code audit has succeeded, and they are not a theorem
completion claim.
-/

/-- Exact external-source search terms requested for the Kolyvagin Euler-system audit. -/
def externalAuditSearchTerms : List String := [
  "Kolyvagin",
  "EulerSystem",
  "Euler system",
  "KolyvaginSystem",
  "Heegner",
  "TateShafarevich",
  "SelmerGroup",
  "Galois cohomology"
]

/-- The external audit search-term list has exactly the eight requested entries. -/
theorem externalAuditSearchTerms_length : externalAuditSearchTerms.length = 8 :=
  rfl

/--
Repo-local closure gate for any future external Lean 4 Kolyvagin/Euler-system
candidate.

An external theorem URL or theorem name can only become completion evidence after
the dependency is pinned or vendored, imported by a local wrapper, and checked by
the repo-local Lake toolchain.
-/
def externalAuditRepoLocalClosureGate : String :=
  "If an external Lean 4 Kolyvagin/Euler-system closure is found, pin/import/check \
it in the repo-local Lake closure or record a concrete integration blocker; \
anchor-only evidence must not be marked completed."

/-!
## Integration gate status

The integration gate is separate from the search-term inventory above.  Its role
is to prevent an external URL, theorem name, or unauthenticated search hit from
being treated as completed evidence.  In this repo-local artifact no terminal
external Lean 4 Kolyvagin/Euler-system closure has been verified, pinned, imported,
or checked.
-/

/-- Repo-local integration-gate status for a possible external proof candidate. -/
structure IntegrationGateRecord where
  currentMachineStatus : String
  externalClosureVerified : Bool
  externalDependencyPinnedOrVendored : Bool
  localWrapperChecked : Bool
  concreteBlockerIfClaimed : String
  publicCompletionAllowed : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  deriving Repr

/--
Current integration-gate record for `THM-M-0444`.

Because no terminal external Lean 4 closure has been verified in the repo-local
audit surface, there is nothing pin-ready to import.  Any later external claim
must provide a repository URL, exact commit, module path, theorem name, Lean
toolchain, Lake dependency feasibility, placeholder-free proof path, and license
feasibility before it can be upgraded from an audit note to a dependency candidate.
-/
def integrationGateRecord : IntegrationGateRecord where
  currentMachineStatus := "not_repo_local_closed"
  externalClosureVerified := false
  externalDependencyPinnedOrVendored := false
  localWrapperChecked := false
  concreteBlockerIfClaimed :=
    "No pin-ready external Lean 4 Kolyvagin/Euler-system closure has been verified. \
Authenticated primary-source code search remains open; until a candidate supplies \
repository URL, exact commit, module path, theorem name, Lean toolchain, Lake file, \
placeholder-free proof path, and dependency/license feasibility, anchor-only \
evidence cannot support completion."
  publicCompletionAllowed := false
  completedStateRetainsRepoLocalIntegrationDebt := false

/-- The current integration gate does not allow a public completion claim. -/
theorem integrationGateRecord_publicCompletionAllowed :
    integrationGateRecord.publicCompletionAllowed = false :=
  rfl

/-- The current integration gate retains no repo-local integration debt in a completed state. -/
theorem integrationGateRecord_no_completed_repo_local_integration_debt :
    integrationGateRecord.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

end S1_M_090
end Stage1
end AwesomeTheorems
