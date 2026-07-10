import Mathlib.NumberTheory.Cyclotomic.Basic
import Mathlib.NumberTheory.NumberField.Cyclotomic.Ideal
import Mathlib.NumberTheory.DirichletCharacter.Basic
import Mathlib.NumberTheory.RamificationInertia.HilbertTheory
import Mathlib.NumberTheory.NumberField.AdeleRing
import Mathlib.FieldTheory.Galois.Abelian

/-!
# S1-M-074 / THM-M-0419

Stage1 statement-shape artifact for the Kronecker-Weber theorem.

The classical theorem says that every finite abelian extension of `ℚ` embeds
into a cyclotomic extension of `ℚ`.  The current mathlib closure has
cyclotomic extensions and abelian Galois extensions, but this file does not
assert a terminal Kronecker-Weber proof.
-/

namespace AwesomeTheorems.Stage1.S1_M_074

universe uK

/--
Lean statement-shape candidate for the Kronecker-Weber theorem.

For a number field `K` presented as a finite abelian Galois extension of `ℚ`,
there should exist a nonzero conductor `n` and a `ℚ`-algebra embedding of `K`
into the `n`-th cyclotomic field over `ℚ`.

The local `CyclotomicField.algebraBase` instance is intentional: without it,
Lean may choose the generic `Rat`-algebra structure on the target field, while
the cyclotomic API is stated using the splitting-field algebra structure.
-/
def StatementShape
    (K : Type uK) [Field K] [Algebra ℚ K] [NumberField K]
    [IsAbelianGalois ℚ K] : Prop :=
  ∃ n : ℕ, n ≠ 0 ∧
    letI : Algebra ℚ (CyclotomicField n ℚ) := CyclotomicField.algebraBase n ℚ ℚ
    Nonempty (K →ₐ[ℚ] CyclotomicField n ℚ)

/--
Checked mathlib anchor: a nonzero cyclotomic field over `ℚ` is a cyclotomic
extension for the singleton set `{n}`.
-/
theorem nonzeroCyclotomic_isCyclotomicExtension (n : ℕ) [NeZero n] :
    letI : Algebra ℚ (CyclotomicField n ℚ) := CyclotomicField.algebraBase n ℚ ℚ
    IsCyclotomicExtension {n} ℚ (CyclotomicField n ℚ) := by
  letI : Algebra ℚ (CyclotomicField n ℚ) := CyclotomicField.algebraBase n ℚ ℚ
  exact CyclotomicField.isCyclotomicExtension n ℚ

/--
Checked mathlib anchor: a nonzero cyclotomic field over `ℚ` is an abelian
Galois extension of `ℚ`.

This is the easy direction adjacent to Kronecker-Weber, not the theorem's
converse containment statement.
-/
theorem nonzeroCyclotomic_isAbelianGalois (n : ℕ) [NeZero n] :
    letI : Algebra ℚ (CyclotomicField n ℚ) := CyclotomicField.algebraBase n ℚ ℚ
    IsAbelianGalois ℚ (CyclotomicField n ℚ) := by
  letI : Algebra ℚ (CyclotomicField n ℚ) := CyclotomicField.algebraBase n ℚ ℚ
  letI : IsCyclotomicExtension {n} ℚ (CyclotomicField n ℚ) :=
    CyclotomicField.isCyclotomicExtension n ℚ
  exact IsCyclotomicExtension.isAbelianGalois {n} ℚ (CyclotomicField n ℚ)

/--
Checked mathlib anchor: cyclotomic fields over `ℚ` are number fields.
-/
theorem cyclotomicField_numberField (n : ℕ) :
    letI : Algebra ℚ (CyclotomicField n ℚ) := CyclotomicField.algebraBase n ℚ ℚ
    NumberField (CyclotomicField n ℚ) := by
  letI : Algebra ℚ (CyclotomicField n ℚ) := CyclotomicField.algebraBase n ℚ ℚ
  exact CyclotomicField.instNumberField n ℚ

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.Cyclotomic.Basic",
  "Mathlib.NumberTheory.Cyclotomic.PrimitiveRoots",
  "Mathlib.NumberTheory.Cyclotomic.Gal",
  "Mathlib.NumberTheory.Cyclotomic.Rat",
  "Mathlib.NumberTheory.NumberField.Cyclotomic.Basic",
  "Mathlib.NumberTheory.NumberField.Cyclotomic.Ideal",
  "Mathlib.NumberTheory.DirichletCharacter.Basic",
  "Mathlib.FieldTheory.Galois.Abelian",
  "Mathlib.NumberTheory.NumberField.AdeleRing",
  "Mathlib.NumberTheory.RamificationInertia.Basic",
  "Mathlib.NumberTheory.RamificationInertia.Galois",
  "Mathlib.NumberTheory.RamificationInertia.HilbertTheory"
]

/-- Checked mathlib declarations used as local anchors. -/
def checkedMathlibAnchors : List String := [
  "IsCyclotomicExtension",
  "CyclotomicField",
  "CyclotomicField.algebraBase",
  "CyclotomicField.isCyclotomicExtension",
  "IsCyclotomicExtension.isAbelianGalois",
  "IsAbelianGalois",
  "NumberField",
  "CyclotomicField.instNumberField",
  "DirichletCharacter.conductor",
  "DirichletCharacter.factorsThrough_conductor",
  "Ideal.ramificationIdxIn",
  "Ideal.inertiaDegIn",
  "Ideal.card_inertia_eq_ramificationIdxIn",
  "IsCyclotomicExtension.Rat.ramificationIdxIn_eq",
  "IsCyclotomicExtension.Rat.inertiaDegIn_eq",
  "IsDecompositionField",
  "IsInertiaField",
  "NumberField.AdeleRing",
  "IntermediateField.val",
  "AlgEquiv.toAlgHom",
  "AlgHom.comp"
]

/--
Checked anchor for the only conductor API found in the local mathlib closure
that is close to the word "conductor": Dirichlet-character conductors.

This is not yet the conductor of a finite abelian extension of `ℚ`.
-/
noncomputable abbrev dirichletCharacterConductorAnchor
    {R : Type*} [CommMonoidWithZero R] {n : ℕ}
    (χ : DirichletCharacter R n) : ℕ :=
  DirichletCharacter.conductor χ

/--
Checked anchor for mathlib's Galois-extension ramification-index invariant.
-/
noncomputable abbrev idealRamificationIdxInAnchor
    {A : Type*} [CommRing A] (p : Ideal A)
    (B : Type*) [CommRing B] [Algebra A B] : ℕ :=
  Ideal.ramificationIdxIn p B

/--
Checked anchor for mathlib's Galois-extension inertia-degree invariant.
-/
noncomputable abbrev idealInertiaDegInAnchor
    {A : Type*} [CommRing A] (p : Ideal A)
    (B : Type*) [CommRing B] [Algebra A B] : ℕ :=
  Ideal.inertiaDegIn p B

/--
P5 audit status: local mathlib has useful conductor-adjacent and
ramification/inertia anchors, but not the ray-class/global-reciprocity bridge
that would produce the Kronecker-Weber conductor `n`.
-/
inductive P5ConductorBridgeAuditStatus
  | partialMathlibAnchorsNoTerminalBridge
  deriving DecidableEq, Repr

/-- Current P5 conductor-and-ramification bridge status. -/
def p5ConductorBridgeAuditStatus : P5ConductorBridgeAuditStatus :=
  .partialMathlibAnchorsNoTerminalBridge

/-- Compile-checked status witness for the P5 bridge audit. -/
theorem p5ConductorBridgeAuditStatus_eq_partial :
    p5ConductorBridgeAuditStatus =
      P5ConductorBridgeAuditStatus.partialMathlibAnchorsNoTerminalBridge := rfl

/-- P5 positive anchors found in the local mathlib dependency closure. -/
def p5PositiveMathlibAnchors : List String := [
  "`DirichletCharacter.conductor`: conductor for Dirichlet characters only.",
  "`Ideal.ramificationIdxIn` and `Ideal.inertiaDegIn`: Galois-extension ramification/inertia invariants for Dedekind-domain prime ideals.",
  "`Ideal.card_inertia_eq_ramificationIdxIn`: inertia-group size equals ramification index in the Galois Dedekind-domain setting.",
  "`IsCyclotomicExtension.Rat.ramificationIdxIn_eq` and `IsCyclotomicExtension.Rat.inertiaDegIn_eq`: explicit cyclotomic-field ramification and inertia formulas over `ℚ`.",
  "`IsDecompositionField` and `IsInertiaField`: Hilbert ramification-theory field predicates.",
  "`NumberField.AdeleRing`: additive adele substrate, not an idele-class reciprocity theorem."
]

/-- P5 missing APIs blocking production of the Kronecker-Weber conductor `n`. -/
def p5MissingTerminalBridgeAPIs : List String := [
  "No repo-local `RayClass` / ray-class-group API was found in the pinned mathlib closure.",
  "No global Artin reciprocity map or class-field-theory correspondence theorem was found.",
  "No finite-abelian-extension conductor object was found that maps `[IsAbelianGalois ℚ K]` to a nonzero `n : ℕ`.",
  "No theorem was found converting ramification/inertia constraints for `K/ℚ` into containment in `CyclotomicField n ℚ`.",
  "The Dirichlet-character conductor API is useful adjacent infrastructure, but it is not a completed bridge from abstract abelian extensions to cyclotomic containment."
]

/--
P2 public-backfill facts checked by this local artifact.

These are object-model facts for the cyclotomic target side only.  They do not
prove the Kronecker-Weber containment direction.
-/
def p2CyclotomicObjectModelBackfill : List String := [
  "Use `CyclotomicField.algebraBase n ℚ ℚ` as the local `ℚ`-algebra structure on `CyclotomicField n ℚ`.",
  "`nonzeroCyclotomic_isCyclotomicExtension` checks the nonzero cyclotomic-extension wrapper.",
  "`nonzeroCyclotomic_isAbelianGalois` checks the nonzero abelian-Galois easy-direction wrapper.",
  "`cyclotomicField_numberField` checks that cyclotomic fields over `ℚ` are number fields.",
  "These wrappers are local_wrapper_upstream_mathlib anchors, not a terminal Kronecker-Weber proof."
]

/--
Search terms that did not locate a terminal Kronecker-Weber theorem in the
repo-local mathlib dependency closure.
-/
def absentTerminalSearchTerms : List String := [
  "Kronecker",
  "Weber",
  "KroneckerWeber",
  "ClassField",
  "Artin",
  "Reciprocity",
  "abelian extension cyclotomic"
]

/--
P6 route decision for the Kronecker-Weber proof core.

The current repo-local closure has no pinned external Lean 4 Kronecker-Weber
proof and no mathlib class-field-theory bridge strong enough to prove the
terminal containment theorem.  The Stage1 route should therefore be a local
direct-proof package, while keeping an explicit P8 gate for any later external
proof that can be pinned, imported, and checked.
-/
inductive P6CoreRouteDecision
  | localDirectProofPackageUntilPinnedExternalOrClassFieldTheory
  deriving DecidableEq, Repr

/-- Current P6 class-field-theory/direct-proof route decision. -/
def p6CoreRouteDecision : P6CoreRouteDecision :=
  .localDirectProofPackageUntilPinnedExternalOrClassFieldTheory

/-- Compile-checked status witness for the P6 route decision. -/
theorem p6CoreRouteDecision_eq_localDirect :
    p6CoreRouteDecision =
      P6CoreRouteDecision.localDirectProofPackageUntilPinnedExternalOrClassFieldTheory := rfl

/-- P6 route-decision rationale recorded in the repo-local Lean artifact. -/
def p6RouteDecisionRationale : List String := [
  "No terminal Kronecker-Weber theorem was found in the pinned mathlib closure.",
  "No public Lean 4 external proof anchor was located that can currently be added as a pinned dependency or vendored proof body.",
  "The pinned mathlib closure has cyclotomic, abelian-Galois, conductor-adjacent, and ramification/inertia anchors, but no ray-class/global-Artin-reciprocity/class-field-theory bridge producing the conductor `n`.",
  "The active route is therefore a local direct-proof package through ramification, prime-power cyclic reductions, cyclotomic containment, and final embedding closure.",
  "If future mathlib class field theory or an external Lean 4 Kronecker-Weber proof appears, the P8 gate must pin/import/check it or record a concrete integration blocker before any completion claim."
]

/-- P6 direct-proof leaves that remain below the terminal Kronecker-Weber proof. -/
def p6RemainingDirectProofLeaves : List String := [
  "Formalize the ramification reduction that removes tame primes after adjoining suitable cyclotomic subfields.",
  "Decompose the finite abelian Galois group into prime-power cyclic or primary components and transfer this decomposition to intermediate fields.",
  "Prove the prime-power cyclic core containment theorem for the remaining wildly ramified case.",
  "Show that finite composita of the selected cyclotomic fields embed into one cyclotomic field.",
  "Connect the containment theorem to the exact `StatementShape` embedding conclusion."
]

/--
P7 adapter: if a proof already has the exact embedding-shaped conclusion under
the cyclotomic `ℚ`-algebra structure, it is already in the form required by the
Stage1 statement.
-/
theorem p7_embeddingConclusion_of_exactAlgHom
    (K : Type uK) [Field K] [Algebra ℚ K]
    (n : ℕ)
    (h : letI : Algebra ℚ (CyclotomicField n ℚ) := CyclotomicField.algebraBase n ℚ ℚ
      Nonempty (K →ₐ[ℚ] CyclotomicField n ℚ)) :
    letI : Algebra ℚ (CyclotomicField n ℚ) := CyclotomicField.algebraBase n ℚ ℚ
    Nonempty (K →ₐ[ℚ] CyclotomicField n ℚ) := by
  exact h

/--
P7 adapter: convert a containment theorem phrased as "`K` is equivalent to an
intermediate field of `CyclotomicField n ℚ`" into the exact embedding conclusion
used by `StatementShape`.

The explicit local `CyclotomicField.algebraBase` instance is part of the
interface, so downstream containment theorems cannot accidentally discharge the
wrong target algebra structure.
-/
theorem p7_embeddingConclusion_of_intermediateFieldEquiv
    (K : Type uK) [Field K] [Algebra ℚ K]
    (n : ℕ)
    (h : letI : Algebra ℚ (CyclotomicField n ℚ) := CyclotomicField.algebraBase n ℚ ℚ
      ∃ F : IntermediateField ℚ (CyclotomicField n ℚ), Nonempty (K ≃ₐ[ℚ] F)) :
    letI : Algebra ℚ (CyclotomicField n ℚ) := CyclotomicField.algebraBase n ℚ ℚ
    Nonempty (K →ₐ[ℚ] CyclotomicField n ℚ) := by
  letI : Algebra ℚ (CyclotomicField n ℚ) := CyclotomicField.algebraBase n ℚ ℚ
  rcases h with ⟨F, ⟨e⟩⟩
  exact ⟨F.val.comp e.toAlgHom⟩

/--
P7 adapter at the parent-statement level: a conductor `n`, nonzeroness, and an
intermediate-field containment theorem imply the current `StatementShape`.

This is not a proof of Kronecker-Weber because the required containment theorem
is still missing.
-/
theorem p7_statementShape_of_intermediateFieldEquiv
    (K : Type uK) [Field K] [Algebra ℚ K] [NumberField K]
    [IsAbelianGalois ℚ K]
    (h : ∃ n : ℕ, n ≠ 0 ∧
      letI : Algebra ℚ (CyclotomicField n ℚ) := CyclotomicField.algebraBase n ℚ ℚ
      ∃ F : IntermediateField ℚ (CyclotomicField n ℚ), Nonempty (K ≃ₐ[ℚ] F)) :
    StatementShape K := by
  rcases h with ⟨n, hn, hF⟩
  refine ⟨n, hn, ?_⟩
  exact p7_embeddingConclusion_of_intermediateFieldEquiv K n hF

/--
P7 closure status: the embedding-shape adapters are checked, but the
mathematical containment theorem they consume is not yet repo-local.
-/
inductive P7EmbeddingClosureStatus
  | adaptersCheckedContainmentTheoremMissing
  deriving DecidableEq, Repr

/-- Current P7 embedding-and-intermediate-field closure status. -/
def p7EmbeddingClosureStatus : P7EmbeddingClosureStatus :=
  .adaptersCheckedContainmentTheoremMissing

/-- Compile-checked status witness for the P7 embedding closure task. -/
theorem p7EmbeddingClosureStatus_eq_adaptersChecked :
    p7EmbeddingClosureStatus =
      P7EmbeddingClosureStatus.adaptersCheckedContainmentTheoremMissing := rfl

/-- P7 repo-local adapters checked in this artifact. -/
def p7CheckedEmbeddingAdapters : List String := [
  "`p7_embeddingConclusion_of_exactAlgHom`: recognizes the exact `Nonempty (K →ₐ[ℚ] CyclotomicField n ℚ)` conclusion under `CyclotomicField.algebraBase n ℚ ℚ`.",
  "`p7_embeddingConclusion_of_intermediateFieldEquiv`: composes `AlgEquiv.toAlgHom` with `IntermediateField.val` to turn `K ≃ₐ[ℚ] F` for an intermediate field `F ≤ CyclotomicField n ℚ` into the exact embedding conclusion.",
  "`p7_statementShape_of_intermediateFieldEquiv`: packages a nonzero conductor and intermediate-field containment into `StatementShape K`."
]

/-- P7 leaves still needed before the Kronecker-Weber statement can close. -/
def p7RemainingEmbeddingClosureLeaves : List String := [
  "Produce or import the actual containment theorem giving `∃ F : IntermediateField ℚ (CyclotomicField n ℚ), Nonempty (K ≃ₐ[ℚ] F)` for the conductor `n`.",
  "Ensure the containment theorem is stated under `CyclotomicField.algebraBase n ℚ ℚ`, or bridge any definitional mismatch explicitly.",
  "If the containment theorem is stated as a subfield/subalgebra inclusion rather than an intermediate-field equivalence, add a checked adapter to construct the required `AlgEquiv` or direct `AlgHom`.",
  "Use `p7_statementShape_of_intermediateFieldEquiv` only after the conductor-production and containment theorem are repo-locally validated."
]

/--
P8 repo-local closure-gate status.

No terminal Kronecker-Weber Lean 4 proof is currently pinned into this
repository's Lake closure.  The parent theorem therefore remains open; an
external URL, theorem name, or prose reference is not completion evidence.
-/
inductive P8RepoLocalClosureGateStatus
  | openNoPinnedExternalProofNoCompletion
  deriving DecidableEq, Repr

/-- Current P8 repo-local closure-gate status. -/
def p8RepoLocalClosureGateStatus : P8RepoLocalClosureGateStatus :=
  .openNoPinnedExternalProofNoCompletion

/-- Compile-checked status witness for the P8 repo-local closure gate. -/
theorem p8RepoLocalClosureGateStatus_eq_open :
    p8RepoLocalClosureGateStatus =
      P8RepoLocalClosureGateStatus.openNoPinnedExternalProofNoCompletion := rfl

/-- P8 completion gate required before the parent theorem can be marked closed. -/
def p8RepoLocalCompletionGate : List String := [
  "A terminal Kronecker-Weber theorem must be available as a local proof body, a local wrapper over pinned mathlib, or a pinned/vendored external Lean 4 proof.",
  "If an external Lean 4 proof appears, record repository URL, commit hash, `lean-toolchain`, `lakefile.lean`, license, module path, and terminal theorem name before relying on it.",
  "The external proof must be added to this repository's Lake closure or vendored, imported by a narrow local wrapper, and checked with the repo-local Lean command.",
  "If integration fails, record the exact blocker: Lean version mismatch, mathlib pin conflict, missing license permission, dependency cycle, missing theorem name, `sorry`/`admit`/axiom residue, or API mismatch.",
  "Do not mark `S1-M-074 / THM-M-0419` completed from anchor-only evidence such as a URL, paper, theorem name, or unimported external repository."
]

/-- Current P8 audit facts for this repo-local artifact. -/
def p8CurrentRepoLocalClosureAudit : List String := [
  "No terminal Kronecker-Weber theorem is defined in this local artifact.",
  "No external Kronecker-Weber Lean 4 proof has been pinned, vendored, imported, or checked in this repository.",
  "The checked local declarations cover statement shape, cyclotomic target-side wrappers, conductor/ramification audit metadata, P6 route decision metadata, and P7 embedding adapters only.",
  "The terminal parent theorem remains `not_repo_local_closed` / `formalization_debt`.",
  "No completed-state `repo_local_integration_debt` is retained because no completion is claimed."
]

/-- P8 remaining leaves below the repo-local closure gate. -/
def p8RemainingRepoLocalClosureLeaves : List String := [
  "Run a renewed primary-source Lean 4 audit before any future status upgrade.",
  "If a no-placeholder external Lean 4 Kronecker-Weber proof is found, pin or vendor the exact revision and add a local wrapper theorem.",
  "Validate the wrapper with `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_074.lean` or with the replacement file containing the wrapper.",
  "If pin/import/check cannot be completed, record the precise integration blocker and keep the parent theorem open.",
  "Merge public blueprint/todo status only after the local validation, public theorem-tree budget ledger, and no-integration-debt gate all agree."
]

end AwesomeTheorems.Stage1.S1_M_074
