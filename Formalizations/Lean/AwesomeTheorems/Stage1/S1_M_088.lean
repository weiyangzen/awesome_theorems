import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point
import Mathlib.AlgebraicGeometry.EllipticCurve.Jacobian.Point
import Mathlib.Data.ZMod.Basic
import Mathlib.GroupTheory.Torsion
import Mathlib.NumberTheory.ModularForms.Cusps

/-!
# S1-M-088 / THM-M-0442: Mazur's torsion theorem

This Stage1 file records a Lean 4 statement-shape boundary for Mazur's theorem classifying
the possible rational torsion subgroups of elliptic curves over `Q`.

The local dependency closure supplies Weierstrass elliptic curves over `Q`, rational point groups,
and the additive torsion subgroup API. It does not supply a proof of Mazur's classification, so the
terminal theorem is intentionally represented as a precise `Prop` statement shape plus low-risk
wrappers around available mathlib declarations.
-/

noncomputable section

open scoped WeierstrassCurve.Affine
open scoped MatrixGroups

namespace AwesomeTheorems.Stage1.S1_M_088

/-- The cyclic orders appearing in Mazur's classification. -/
def IsMazurCyclicOrder (n : ℕ) : Prop :=
  (1 ≤ n ∧ n ≤ 10) ∨ n = 12

/-- The second factor orders in the non-cyclic `ZMod 2 × ZMod n` cases. -/
def IsMazurBicyclicSecondOrder (n : ℕ) : Prop :=
  n = 2 ∨ n = 4 ∨ n = 6 ∨ n = 8

/-- The rational torsion subgroup of a Weierstrass elliptic curve over `Q`. -/
abbrev RationalTorsionGroup (E : WeierstrassCurve ℚ) [E.IsElliptic] : Type :=
  AddCommGroup.torsion E⟮ℚ⟯

/-- One cyclic case in Mazur's classification, phrased as an additive group equivalence. -/
def HasCyclicTorsionOrder (E : WeierstrassCurve ℚ) [E.IsElliptic] (n : ℕ) : Prop :=
  Nonempty (RationalTorsionGroup E ≃+ ZMod n)

/-- One non-cyclic case in Mazur's classification, phrased as an additive group equivalence. -/
def HasBicyclicTorsionType (E : WeierstrassCurve ℚ) [E.IsElliptic] (n : ℕ) : Prop :=
  Nonempty (RationalTorsionGroup E ≃+ (ZMod 2 × ZMod n))

/--
The exact classification conclusion of Mazur's theorem in the current mathlib object model.

This is a statement shape only. A terminal proof would need either a local proof body or a pinned
external Lean 4 dependency proving this proposition without placeholder assumptions.
-/
def MazurTorsionClassified (E : WeierstrassCurve ℚ) [E.IsElliptic] : Prop :=
  (∃ n : ℕ, IsMazurCyclicOrder n ∧ HasCyclicTorsionOrder E n) ∨
    (∃ n : ℕ, IsMazurBicyclicSecondOrder n ∧ HasBicyclicTorsionType E n)

/--
Stage1 statement shape: the rational torsion subgroup of every elliptic curve over `Q` has one of
Mazur's allowed group types.
-/
def StatementShape : Prop :=
  ∀ (E : WeierstrassCurve ℚ) [E.IsElliptic], MazurTorsionClassified E

/--
The weaker bound shape used by the external FLT project as an assumption. This is not a local proof
of the bound; it records the exact proposition that a future pinned dependency could expose.
-/
def TorsionBoundAtMostSixteenShape : Prop :=
  ∀ (E : WeierstrassCurve ℚ) [E.IsElliptic],
    (AddCommGroup.torsion E⟮ℚ⟯ : Set E⟮ℚ⟯).ncard ≤ 16

/-! ## Cardinality bridge -/

/-- Every cyclic order allowed by Mazur's classification is at most `16`. -/
theorem IsMazurCyclicOrder.le_sixteen {n : ℕ} (h : IsMazurCyclicOrder n) : n ≤ 16 := by
  rcases h with ⟨_, h10⟩ | rfl
  · exact h10.trans (by norm_num)
  · norm_num

/-- Every non-cyclic order allowed by Mazur's classification has size at most `16`. -/
theorem IsMazurBicyclicSecondOrder.two_mul_le_sixteen {n : ℕ}
    (h : IsMazurBicyclicSecondOrder n) : 2 * n ≤ 16 := by
  rcases h with rfl | rfl | rfl | rfl <;> norm_num

/--
If the rational torsion subgroup is additively equivalent to `ZMod n`, its `Set.ncard` is `n`.

The bridge uses `Nat.card_coe_set_eq` to move from the coerced torsion set to the subtype,
then transports cardinality across the additive equivalence and evaluates `ZMod` by
`Nat.card_zmod`.
-/
theorem torsion_ncard_eq_of_hasCyclicTorsionOrder
    {E : WeierstrassCurve ℚ} [E.IsElliptic] {n : ℕ}
    (h : HasCyclicTorsionOrder E n) :
    (AddCommGroup.torsion E⟮ℚ⟯ : Set E⟮ℚ⟯).ncard = n := by
  rcases h with ⟨e⟩
  rw [← Nat.card_coe_set_eq]
  exact (Nat.card_congr e.toEquiv).trans (Nat.card_zmod n)

/--
If the rational torsion subgroup is additively equivalent to `ZMod 2 × ZMod n`, its `Set.ncard`
is `2 * n`.

This is the finite-cardinality API choice needed for the Mazur bridge: first pass through
`Nat.card_coe_set_eq`, then use `Nat.card_congr`, `Nat.card_prod`, and `Nat.card_zmod`.
-/
theorem torsion_ncard_eq_of_hasBicyclicTorsionType
    {E : WeierstrassCurve ℚ} [E.IsElliptic] {n : ℕ}
    (h : HasBicyclicTorsionType E n) :
    (AddCommGroup.torsion E⟮ℚ⟯ : Set E⟮ℚ⟯).ncard = 2 * n := by
  rcases h with ⟨e⟩
  rw [← Nat.card_coe_set_eq]
  calc
    Nat.card (RationalTorsionGroup E) = Nat.card (ZMod 2 × ZMod n) :=
      Nat.card_congr e.toEquiv
    _ = 2 * n := by rw [Nat.card_prod, Nat.card_zmod, Nat.card_zmod]

/-- The full Mazur classification for one curve implies the weak `ncard ≤ 16` torsion bound. -/
theorem MazurTorsionClassified.torsion_ncard_le_sixteen
    {E : WeierstrassCurve ℚ} [E.IsElliptic]
    (h : MazurTorsionClassified E) :
    (AddCommGroup.torsion E⟮ℚ⟯ : Set E⟮ℚ⟯).ncard ≤ 16 := by
  rcases h with ⟨n, hn, hcyc⟩ | ⟨n, hn, hbic⟩
  · rw [torsion_ncard_eq_of_hasCyclicTorsionOrder hcyc]
    exact hn.le_sixteen
  · rw [torsion_ncard_eq_of_hasBicyclicTorsionType hbic]
    exact hn.two_mul_le_sixteen

/-- The Stage1 full classification statement implies the weaker `ncard ≤ 16` statement shape. -/
theorem statementShape_implies_torsionBoundAtMostSixteenShape
    (h : StatementShape) : TorsionBoundAtMostSixteenShape := by
  intro E hE
  exact MazurTorsionClassified.torsion_ncard_le_sixteen (h E)

/-! ## External FLT anchor audit -/

/--
Repo-local status for the ImperialCollegeLondon/FLT Mazur source.

The current Stage1 artifact records the upstream source as an axiom-level,
non-completion anchor only. It is not imported, pinned as a Lake dependency, or
used as a proof of `TorsionBoundAtMostSixteenShape`.
-/
inductive ExternalFLTMazurAnchorStatus where
  | axiomLevelNonCompletionAnchor
  | pinnedAndImported
  | concreteIntegrationBlockerRecorded
  deriving DecidableEq, Repr

/-- Current decision for this child task: the FLT source is an axiom-level anchor only. -/
def selectedExternalFLTMazurAnchorStatus : ExternalFLTMazurAnchorStatus :=
  .axiomLevelNonCompletionAnchor

theorem selectedExternalFLTMazurAnchorStatus_eq :
    selectedExternalFLTMazurAnchorStatus =
      ExternalFLTMazurAnchorStatus.axiomLevelNonCompletionAnchor := rfl

/-- Upstream repository containing the axiom-level Mazur source used by the FLT project. -/
def externalFLTMazurRepository : String :=
  "https://github.com/ImperialCollegeLondon/FLT"

/-- Exact upstream revision audited for the axiom-level Mazur source. -/
def externalFLTMazurRevision : String :=
  "1f76653ab824d19fd2475c24ba8c20f06fd9cc1d"

/-- Exact upstream file path audited for the axiom-level Mazur source. -/
def externalFLTMazurPath : String :=
  "FLT/Assumptions/Mazur.lean"

/-- Upstream declaration name for the axiom-level weaker Mazur bound. -/
def externalFLTMazurDeclaration : String :=
  "Mazur_statement"

/--
The proposition shape of `ImperialCollegeLondon/FLT`'s axiom-level
`Mazur_statement` declaration at revision
`1f76653ab824d19fd2475c24ba8c20f06fd9cc1d`.

This definition is only a checked local restatement of the proposition shape;
it is not a proof of the bound and it deliberately introduces no axiom.
-/
def ExternalFLTMazurAxiomShape : Prop :=
  ∀ (E : WeierstrassCurve ℚ) [E.IsElliptic],
    (AddCommGroup.torsion E⟮ℚ⟯ : Set E⟮ℚ⟯).ncard ≤ 16

/-- The audited FLT axiom shape is propositionally the same as the local weaker bound shape. -/
theorem externalFLTMazurAxiomShape_iff_torsionBoundAtMostSixteenShape :
    ExternalFLTMazurAxiomShape ↔ TorsionBoundAtMostSixteenShape := Iff.rfl

/-- Low-risk wrapper: the rational torsion subgroup carries an additive commutative group. -/
@[reducible]
def rationalTorsionGroupAddCommGroup
    (E : WeierstrassCurve ℚ) [E.IsElliptic] : AddCommGroup (RationalTorsionGroup E) :=
  inferInstance

/-- Low-risk wrapper: membership in the torsion subgroup is finite additive order. -/
theorem mem_rationalTorsionGroup_iff
    (E : WeierstrassCurve ℚ) [E.IsElliptic] (P : E⟮ℚ⟯) :
    P ∈ AddCommGroup.torsion E⟮ℚ⟯ ↔ IsOfFinAddOrder P := by
  exact AddCommGroup.mem_torsion (G := E⟮ℚ⟯) P

/-- Low-risk wrapper: mathlib exposes the rational point group on a Weierstrass elliptic curve. -/
@[reducible]
def rationalPointAddCommGroup
    (E : WeierstrassCurve ℚ) [E.IsElliptic] : AddCommGroup E⟮ℚ⟯ :=
  inferInstance

/-! ## Mathlib anchor audit -/

/-- Anchor: mathlib's Weierstrass curve object model over `Q`. -/
abbrev mathlibWeierstrassCurveAnchor : Type :=
  WeierstrassCurve ℚ

/-- Anchor: mathlib's ellipticity predicate for Weierstrass curves. -/
def mathlibIsEllipticAnchor (E : WeierstrassCurve ℚ) : Prop :=
  E.IsElliptic

/-- Anchor: mathlib's affine nonsingular point type and `E⟮Q⟯` notation. -/
abbrev mathlibAffinePointAnchor (E : WeierstrassCurve ℚ) : Type :=
  E⟮ℚ⟯

/-- Anchor: mathlib's Jacobian nonsingular point type for the same Weierstrass curve. -/
abbrev mathlibJacobianPointAnchor (E : WeierstrassCurve ℚ) : Type :=
  WeierstrassCurve.Jacobian.Point E.toJacobian

/-- Anchor: mathlib's additive torsion subgroup API, specialized to rational points. -/
abbrev mathlibTorsionAnchor
    (E : WeierstrassCurve ℚ) [E.IsElliptic] : Type :=
  AddCommGroup.torsion E⟮ℚ⟯

/-- Anchor: mathlib's finite cyclic target type used in the Mazur statement shape. -/
abbrev mathlibZModAnchor (n : ℕ) : Type :=
  ZMod n

/-- Sanity check for the finite list of cyclic orders in the statement shape. -/
theorem twelve_isMazurCyclicOrder : IsMazurCyclicOrder 12 := by
  exact Or.inr rfl

/-- Sanity check for one non-cyclic order in the statement shape. -/
theorem eight_isMazurBicyclicSecondOrder : IsMazurBicyclicSecondOrder 8 := by
  exact Or.inr <| Or.inr <| Or.inr rfl

/-! ## Modular-curve API audit for Mazur's proof route -/

/-- Anchor: mathlib's congruence subgroup `Γ₀(N)`. -/
abbrev mathlibGamma0Anchor (N : ℕ) : Subgroup SL(2, ℤ) :=
  CongruenceSubgroup.Gamma0 N

/-- Anchor: mathlib's congruence subgroup `Γ₁(N)`. -/
abbrev mathlibGamma1Anchor (N : ℕ) : Subgroup SL(2, ℤ) :=
  CongruenceSubgroup.Gamma1 N

/-- Anchor: mathlib's `Γ₀(N)` cusp-orbit type after mapping into `GL(2, R)`. -/
abbrev mathlibGamma0CuspOrbitsAnchor (N : ℕ) : Type :=
  CuspOrbits (CongruenceSubgroup.Gamma0 N : Subgroup (GL (Fin 2) ℝ))

/-- Anchor: mathlib's `Γ₁(N)` cusp-orbit type after mapping into `GL(2, R)`. -/
abbrev mathlibGamma1CuspOrbitsAnchor (N : ℕ) : Type :=
  CuspOrbits (CongruenceSubgroup.Gamma1 N : Subgroup (GL (Fin 2) ℝ))

/-- Anchor: mathlib's cusp predicate for arithmetic subgroups of `GL(2, R)`. -/
def mathlibIsCuspAnchor (c : OnePoint ℝ) (Γ : Subgroup (GL (Fin 2) ℝ)) : Prop :=
  IsCusp c Γ

/-- Anchor: mathlib's cusp width at infinity for subgroups of `GL(2, R)`. -/
noncomputable abbrev mathlibWidthInftyAnchor (Γ : Subgroup (GL (Fin 2) ℝ)) : ℝ :=
  Γ.widthInfty

/--
Repo-local status labels for the modular-curve API pieces needed in Mazur's proof route.

This is audit metadata, not a substitute for the missing geometry.  `checkedMathlibAnchor` means
the local Lean file names and typechecks an adjacent mathlib API.  `notFoundInRepoLocalClosure`
means no usable declaration was found in the pinned local Lake dependency closure.
-/
inductive MazurModularCurveApiStatus where
  | checkedMathlibAnchor
  | notFoundInRepoLocalClosure
  | notPinnedExternalCandidate
  | concreteIntegrationBlocker
  deriving DecidableEq, Repr

/-- Components audited for the modular-curve route through Mazur's torsion theorem. -/
inductive MazurModularCurveApiComponent where
  | gamma0Subgroup
  | gamma1Subgroup
  | cuspOrbits
  | x0CompactifiedCurve
  | x1CompactifiedCurve
  | modularCurveJacobian
  | eisensteinIdeal
  | windingQuotient
  | rationalPointsOnModularCurves
  deriving DecidableEq, Repr

/--
Current repo-local audit result for each modular-curve component in Mazur's proof route.

The local mathlib closure supplies congruence subgroups and cusp orbits.  It does not supply
compactified modular curves `X_0(N)`/`X_1(N)`, their Jacobians, Eisenstein ideals, winding
quotients, or rational-point classification APIs sufficient to run Mazur's proof.
-/
def mazurModularCurveApiStatus :
    MazurModularCurveApiComponent → MazurModularCurveApiStatus
  | .gamma0Subgroup => .checkedMathlibAnchor
  | .gamma1Subgroup => .checkedMathlibAnchor
  | .cuspOrbits => .checkedMathlibAnchor
  | .x0CompactifiedCurve => .notFoundInRepoLocalClosure
  | .x1CompactifiedCurve => .notFoundInRepoLocalClosure
  | .modularCurveJacobian => .notFoundInRepoLocalClosure
  | .eisensteinIdeal => .notFoundInRepoLocalClosure
  | .windingQuotient => .notFoundInRepoLocalClosure
  | .rationalPointsOnModularCurves => .notFoundInRepoLocalClosure

theorem mazurModularCurveApiStatus_gamma0 :
    mazurModularCurveApiStatus .gamma0Subgroup =
      MazurModularCurveApiStatus.checkedMathlibAnchor := rfl

theorem mazurModularCurveApiStatus_gamma1 :
    mazurModularCurveApiStatus .gamma1Subgroup =
      MazurModularCurveApiStatus.checkedMathlibAnchor := rfl

theorem mazurModularCurveApiStatus_cuspOrbits :
    mazurModularCurveApiStatus .cuspOrbits =
      MazurModularCurveApiStatus.checkedMathlibAnchor := rfl

/-- The audited local dependency closure is not sufficient for Mazur's modular-curve route. -/
def mazurModularCurveRouteApiSufficient : Bool :=
  false

theorem mazurModularCurveRouteApiSufficient_eq_false :
    mazurModularCurveRouteApiSufficient = false := rfl

/--
The missing terminal APIs are formalization debt in the local dependency closure, not
repo-local integration debt from an already-pinned external Lean proof.
-/
theorem mazurModularCurveApi_missingTerminalPieces :
    mazurModularCurveApiStatus .x0CompactifiedCurve =
        MazurModularCurveApiStatus.notFoundInRepoLocalClosure ∧
      mazurModularCurveApiStatus .x1CompactifiedCurve =
        MazurModularCurveApiStatus.notFoundInRepoLocalClosure ∧
      mazurModularCurveApiStatus .modularCurveJacobian =
        MazurModularCurveApiStatus.notFoundInRepoLocalClosure ∧
      mazurModularCurveApiStatus .eisensteinIdeal =
        MazurModularCurveApiStatus.notFoundInRepoLocalClosure ∧
      mazurModularCurveApiStatus .windingQuotient =
        MazurModularCurveApiStatus.notFoundInRepoLocalClosure ∧
      mazurModularCurveApiStatus .rationalPointsOnModularCurves =
        MazurModularCurveApiStatus.notFoundInRepoLocalClosure := by
  exact ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩

/-! ## External proof search audit -/

/--
Search/result labels for the external Mazur proof-body audit.

This is checked audit metadata only.  The `authenticatedGithubUnavailable` case records that this
worker had no `gh` login or `GH_TOKEN`, so an authenticated GitHub code search could not be run.
The result therefore cannot close the public child task by itself.
-/
inductive MazurExternalProofSearchStatus where
  | authenticatedGithubUnavailable
  | githubUnauthenticatedRateLimited
  | reservoirPackageSearchNoProofBodyFound
  | loogleNoIdentifierFound
  | localDependencySearchNoProofBodyFound
  | fltAxiomAnchorOnly
  deriving DecidableEq, Repr

/-- Search strings required by the Stage1 child task for Mazur's torsion theorem. -/
def mazurExternalProofSearchTerms : List String :=
  ["Mazur",
    "Mazur_statement",
    "MazurTorsion",
    "EisensteinIdeal",
    "X_1",
    "X0",
    "X1",
    "rational torsion",
    "AddCommGroup.torsion E⟮ℚ⟯"]

/--
Current external proof-body audit result for this repo-local artifact.

No complete Lean 4 proof body for `StatementShape` was imported, pinned, or found in the local Lake
dependency closure.  The known FLT source remains an axiom-level weaker-bound anchor.
-/
def mazurExternalProofSearchStatus : List MazurExternalProofSearchStatus :=
  [.authenticatedGithubUnavailable,
    .githubUnauthenticatedRateLimited,
    .reservoirPackageSearchNoProofBodyFound,
    .loogleNoIdentifierFound,
    .localDependencySearchNoProofBodyFound,
    .fltAxiomAnchorOnly]

theorem mazurExternalProofSearchStatus_head :
    mazurExternalProofSearchStatus.head? =
      some MazurExternalProofSearchStatus.authenticatedGithubUnavailable := rfl

/-- Integration blocker for this child pass: no usable external Lean 4 proof body was available. -/
def mazurExternalProofSearchIntegrationBlocker : String :=
  "Authenticated GitHub code search is unavailable in this worker (`gh auth status` reports no " ++
    "login and no GH_TOKEN); unauthenticated GitHub API search is rate-limited; local dependency, " ++
    "Reservoir page, Loogle, and FLT-source checks found no non-axiom Lean 4 proof body for " ++
    "Mazur's rational torsion classification."

/-- No external Mazur proof was pinned into this repository by this audit pass. -/
def mazurExternalProofPinnedInRepo : Bool :=
  false

theorem mazurExternalProofPinnedInRepo_eq_false :
    mazurExternalProofPinnedInRepo = false := rfl

/-! ## Proof-tree backfill for Mazur's theorem -/

/--
Top-level branches for a future Mazur torsion proof tree.

The branches are checked metadata only.  They do not provide compactified
modular curves, Eisenstein ideals, rational-point classifications, or a proof
of `StatementShape`.
-/
inductive MazurProofTreeBranch where
  | modularCurveReduction
  | eisensteinIdealDescent
  | primeOrderExclusions
  | compositeOrderExclusions
  | existenceRealization
  deriving DecidableEq, Repr

/-- Package row for the M0387-style Mazur proof-tree split. -/
structure MazurProofTreePackage where
  code : String
  branch : MazurProofTreeBranch
  packageName : String
  mathematicalRole : String
  requiredLeanSurface : List String
  currentStatus : String
  completionGate : String

/-- The five requested top-level branches for the Mazur proof route. -/
def mazurProofTreePackages : List MazurProofTreePackage :=
  [ { code := "MAZUR-PKG01"
      branch := .modularCurveReduction
      packageName := "modular_curve_reduction"
      mathematicalRole :=
        "Reduce a rational torsion point of order N to a rational point on X_1(N) or X_0(N), with cuspidal and noncuspidal cases separated."
      requiredLeanSurface :=
        [ "compactified modular curves X_1(N) and X_0(N)",
          "elliptic-curve level structure moduli interpretation",
          "cusp and noncusp predicates",
          "rational-point functoriality over Q" ]
      currentStatus := "unchecked_formalization_debt_not_completed"
      completionGate :=
        "Needs concrete modular-curve objects and a checked torsion-to-rational-point construction." },
    { code := "MAZUR-PKG02"
      branch := .eisensteinIdealDescent
      packageName := "eisenstein_ideal_descent"
      mathematicalRole :=
        "Use Hecke algebra, Eisenstein ideal, cuspidal subgroup, and winding quotient control to descend rational points toward cusps or known exceptional cases."
      requiredLeanSurface :=
        [ "Hecke algebra acting on modular-curve Jacobians",
          "Eisenstein ideal and cuspidal subgroup",
          "winding quotient or equivalent rank-control quotient",
          "descent from Jacobian information to rational points" ]
      currentStatus := "unchecked_formalization_debt_not_completed"
      completionGate :=
        "Needs checked Hecke/Jacobian/Eisenstein infrastructure or a pinned external proof body." },
    { code := "MAZUR-PKG03"
      branch := .primeOrderExclusions
      packageName := "prime_order_exclusions"
      mathematicalRole :=
        "Exclude prime torsion orders outside Mazur's cyclic list, especially p >= 11 with p != 13 and the remaining prime-level exceptional analysis."
      requiredLeanSurface :=
        [ "prime-level modular curves",
          "rational points on X_1(p)",
          "cuspidal reduction and formal immersion criteria",
          "separate handling for the classical p = 11, 13, 17, 19 frontier" ]
      currentStatus := "unchecked_formalization_debt_not_completed"
      completionGate :=
        "Needs checked prime-level rational-point exclusion theorems in the local dependency closure." },
    { code := "MAZUR-PKG04"
      branch := .compositeOrderExclusions
      packageName := "composite_order_exclusions"
      mathematicalRole :=
        "Exclude cyclic composite orders outside 1..10 and 12, and exclude noncyclic products other than ZMod 2 x ZMod 2, 4, 6, 8."
      requiredLeanSurface :=
        [ "divisibility reduction from composite torsion to prime-power torsion",
          "2-primary and odd-primary subgroup analysis",
          "rational isogeny constraints",
          "finite abelian group decomposition for torsion subgroups" ]
      currentStatus := "unchecked_formalization_debt_not_completed"
      completionGate :=
        "Needs checked group-theoretic reductions plus modular-curve exclusions for all forbidden composite cases." },
    { code := "MAZUR-PKG05"
      branch := .existenceRealization
      packageName := "existence_and_realization"
      mathematicalRole :=
        "Realize every allowed cyclic and bicyclic torsion type by an elliptic curve over Q, and connect those examples to the statement-shape group equivalences."
      requiredLeanSurface :=
        [ "Tate normal form or explicit elliptic-curve families",
          "nonsingularity checks over Q",
          "torsion point order proofs",
          "additive-group equivalences for the torsion subgroup" ]
      currentStatus := "unchecked_formalization_debt_not_completed"
      completionGate :=
        "Needs explicit checked examples or families for every allowed torsion type." } ]

/-- Checked package count for the five requested Mazur proof branches. -/
theorem mazurProofTreePackages_length :
    mazurProofTreePackages.length = 5 := rfl

/-- Checked package-code coverage for the Mazur proof-tree split. -/
theorem mazurProofTreePackages_codes :
    mazurProofTreePackages.map (fun row ↦ row.code) =
      [ "MAZUR-PKG01",
        "MAZUR-PKG02",
        "MAZUR-PKG03",
        "MAZUR-PKG04",
        "MAZUR-PKG05" ] := rfl

/-- One M0387-style leaf in a future Mazur proof ledger. -/
structure MazurProofTreeLeaf where
  code : String
  parentPackage : String
  branch : MazurProofTreeBranch
  leafTask : String
  maxStepBudget : Nat
  currentStatus : String
  completionGate : String

/-- Local leaf ledger for the modular-curve reduction branch. -/
def mazurModularCurveReductionLeaves : List MazurProofTreeLeaf :=
  [ { code := "MAZUR-MCR-L001"
      parentPackage := "MAZUR-PKG01"
      branch := .modularCurveReduction
      leafTask :=
        "Define or import compactified X_1(N) and X_0(N) over Q with cusp and noncusp predicates."
      maxStepBudget := 100
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs concrete compactified modular curves in Lean." },
    { code := "MAZUR-MCR-L002"
      parentPackage := "MAZUR-PKG01"
      branch := .modularCurveReduction
      leafTask :=
        "Construct the map from an elliptic curve with a rational point of order N to a rational point of X_1(N)."
      maxStepBudget := 100
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs level-structure moduli interpretation for rational torsion points." },
    { code := "MAZUR-MCR-L003"
      parentPackage := "MAZUR-PKG01"
      branch := .modularCurveReduction
      leafTask :=
        "Relate cyclic subgroups and rational N-isogenies to the X_0(N) reduction branch where needed."
      maxStepBudget := 90
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs rational cyclic-subgroup and isogeny-level moduli APIs." },
    { code := "MAZUR-MCR-L004"
      parentPackage := "MAZUR-PKG01"
      branch := .modularCurveReduction
      leafTask :=
        "Separate cuspidal images from noncuspidal images and state the contradiction target for forbidden N."
      maxStepBudget := 80
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs cusp/noncusp dichotomy tied to the moduli construction." } ]

/-- Local leaf ledger for the Eisenstein-ideal descent branch. -/
def mazurEisensteinIdealDescentLeaves : List MazurProofTreeLeaf :=
  [ { code := "MAZUR-EID-L001"
      parentPackage := "MAZUR-PKG02"
      branch := .eisensteinIdealDescent
      leafTask :=
        "Define the Hecke algebra action on the Jacobian of the relevant modular curve."
      maxStepBudget := 100
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs modular-curve Jacobians and Hecke correspondences." },
    { code := "MAZUR-EID-L002"
      parentPackage := "MAZUR-PKG02"
      branch := .eisensteinIdealDescent
      leafTask :=
        "Define the Eisenstein ideal and prove its basic annihilation relation for the cuspidal subgroup."
      maxStepBudget := 100
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs Hecke algebra, cuspidal divisors, and Eisenstein congruence statements." },
    { code := "MAZUR-EID-L003"
      parentPackage := "MAZUR-PKG02"
      branch := .eisensteinIdealDescent
      leafTask :=
        "Construct the winding quotient or equivalent quotient controlling rational divisor classes."
      maxStepBudget := 100
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs quotient Jacobian infrastructure and rank/control theorem." },
    { code := "MAZUR-EID-L004"
      parentPackage := "MAZUR-PKG02"
      branch := .eisensteinIdealDescent
      leafTask :=
        "Use the descent package to force rational noncuspidal points into the finite exceptional frontier."
      maxStepBudget := 100
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs the terminal rational-point descent theorem." } ]

/-- Local leaf ledger for forbidden prime-order torsion exclusions. -/
def mazurPrimeOrderExclusionLeaves : List MazurProofTreeLeaf :=
  [ { code := "MAZUR-POE-L001"
      parentPackage := "MAZUR-PKG03"
      branch := .primeOrderExclusions
      leafTask :=
        "Reduce a forbidden rational point of prime order p to a noncuspidal rational point on X_1(p)."
      maxStepBudget := 90
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Depends on the modular-curve reduction branch." },
    { code := "MAZUR-POE-L002"
      parentPackage := "MAZUR-PKG03"
      branch := .primeOrderExclusions
      leafTask :=
        "Exclude prime levels p >= 17 by the Eisenstein/descent and formal-immersion route."
      maxStepBudget := 100
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs checked prime-level formal-immersion/descent theorem." },
    { code := "MAZUR-POE-L003"
      parentPackage := "MAZUR-PKG03"
      branch := .primeOrderExclusions
      leafTask :=
        "Handle the exceptional prime level p = 13 and show it does not realize rational 13-torsion."
      maxStepBudget := 100
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs the checked rational-point classification for X_1(13)." },
    { code := "MAZUR-POE-L004"
      parentPackage := "MAZUR-PKG03"
      branch := .primeOrderExclusions
      leafTask :=
        "Keep p = 2, 3, 5, 7 inside the allowed cyclic-order branch and route p = 11 through the allowed order 11 case."
      maxStepBudget := 80
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs compatibility between the exclusion branch and the allowed-order statement shape." } ]

/-- Local leaf ledger for forbidden composite-order torsion exclusions. -/
def mazurCompositeOrderExclusionLeaves : List MazurProofTreeLeaf :=
  [ { code := "MAZUR-COE-L001"
      parentPackage := "MAZUR-PKG04"
      branch := .compositeOrderExclusions
      leafTask :=
        "Reduce forbidden cyclic composite order N to prime-power and prime-order modular-curve constraints."
      maxStepBudget := 100
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs finite torsion subgroup divisibility and reduction lemmas." },
    { code := "MAZUR-COE-L002"
      parentPackage := "MAZUR-PKG04"
      branch := .compositeOrderExclusions
      leafTask :=
        "Exclude cyclic orders 11 < N with N != 12 by combining prime divisors, isogeny constraints, and modular-curve exclusions."
      maxStepBudget := 100
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs checked forbidden-cyclic-order theorem for all composite N." },
    { code := "MAZUR-COE-L003"
      parentPackage := "MAZUR-PKG04"
      branch := .compositeOrderExclusions
      leafTask :=
        "Classify the possible 2-primary contribution to rational torsion and constrain products with odd torsion."
      maxStepBudget := 100
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs checked 2-primary torsion structure over Q." },
    { code := "MAZUR-COE-L004"
      parentPackage := "MAZUR-PKG04"
      branch := .compositeOrderExclusions
      leafTask :=
        "Exclude noncyclic products other than ZMod 2 x ZMod 2, 4, 6, and 8."
      maxStepBudget := 100
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs checked finite-abelian-group and elliptic-curve torsion constraints." } ]

/-- Local leaf ledger for the existence and realization branch. -/
def mazurExistenceRealizationLeaves : List MazurProofTreeLeaf :=
  [ { code := "MAZUR-EXR-L001"
      parentPackage := "MAZUR-PKG05"
      branch := .existenceRealization
      leafTask :=
        "Provide explicit curves or Tate-normal-form families realizing cyclic torsion orders 1 through 10 and 12."
      maxStepBudget := 100
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs explicit nonsingular curves and point-order proofs." },
    { code := "MAZUR-EXR-L002"
      parentPackage := "MAZUR-PKG05"
      branch := .existenceRealization
      leafTask :=
        "Provide explicit curves or families realizing ZMod 2 x ZMod n for n = 2, 4, 6, and 8."
      maxStepBudget := 100
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs checked full 2-torsion plus second-factor order proofs." },
    { code := "MAZUR-EXR-L003"
      parentPackage := "MAZUR-PKG05"
      branch := .existenceRealization
      leafTask :=
        "Prove the generated torsion subgroup has exactly the target additive-group equivalence."
      maxStepBudget := 100
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs torsion-subgroup generation and no-extra-torsion proofs." },
    { code := "MAZUR-EXR-L004"
      parentPackage := "MAZUR-PKG05"
      branch := .existenceRealization
      leafTask :=
        "Bridge the checked examples to `HasCyclicTorsionOrder` and `HasBicyclicTorsionType` in the local statement shape."
      maxStepBudget := 80
      currentStatus := "unchecked_formalization_debt"
      completionGate := "Needs additive equivalences into the exact local statement-shape predicates." } ]

/-- Combined M0387-style local proof-tree leaf ledger for Mazur's theorem. -/
def mazurProofTreeLeaves : List MazurProofTreeLeaf :=
  mazurModularCurveReductionLeaves ++
    mazurEisensteinIdealDescentLeaves ++
    mazurPrimeOrderExclusionLeaves ++
    mazurCompositeOrderExclusionLeaves ++
    mazurExistenceRealizationLeaves

/-- Checked leaf count for the modular-curve reduction branch. -/
theorem mazurModularCurveReductionLeaves_length :
    mazurModularCurveReductionLeaves.length = 4 := rfl

/-- Checked leaf count for the Eisenstein-ideal descent branch. -/
theorem mazurEisensteinIdealDescentLeaves_length :
    mazurEisensteinIdealDescentLeaves.length = 4 := rfl

/-- Checked leaf count for the prime-order exclusion branch. -/
theorem mazurPrimeOrderExclusionLeaves_length :
    mazurPrimeOrderExclusionLeaves.length = 4 := rfl

/-- Checked leaf count for the composite-order exclusion branch. -/
theorem mazurCompositeOrderExclusionLeaves_length :
    mazurCompositeOrderExclusionLeaves.length = 4 := rfl

/-- Checked leaf count for the existence/realization branch. -/
theorem mazurExistenceRealizationLeaves_length :
    mazurExistenceRealizationLeaves.length = 4 := rfl

/-- Checked total leaf count for the local Mazur proof-tree ledger. -/
theorem mazurProofTreeLeaves_length :
    mazurProofTreeLeaves.length = 20 := rfl

/-- Checked per-leaf budgets for the modular-curve reduction branch. -/
theorem mazurModularCurveReductionLeaves_budgets :
    mazurModularCurveReductionLeaves.map (fun row ↦ row.maxStepBudget) =
      [100, 100, 90, 80] := rfl

/-- Checked per-leaf budgets for the Eisenstein-ideal descent branch. -/
theorem mazurEisensteinIdealDescentLeaves_budgets :
    mazurEisensteinIdealDescentLeaves.map (fun row ↦ row.maxStepBudget) =
      [100, 100, 100, 100] := rfl

/-- Checked per-leaf budgets for the prime-order exclusion branch. -/
theorem mazurPrimeOrderExclusionLeaves_budgets :
    mazurPrimeOrderExclusionLeaves.map (fun row ↦ row.maxStepBudget) =
      [90, 100, 100, 80] := rfl

/-- Checked per-leaf budgets for the composite-order exclusion branch. -/
theorem mazurCompositeOrderExclusionLeaves_budgets :
    mazurCompositeOrderExclusionLeaves.map (fun row ↦ row.maxStepBudget) =
      [100, 100, 100, 100] := rfl

/-- Checked per-leaf budgets for the existence/realization branch. -/
theorem mazurExistenceRealizationLeaves_budgets :
    mazurExistenceRealizationLeaves.map (fun row ↦ row.maxStepBudget) =
      [100, 100, 100, 80] := rfl

/--
Completion boundary for the proof-tree backfill.

The local artifact now checks the branch split and leaf-ledger metadata, but
the terminal theorem remains `formalization_debt` / `not_repo_local_closed`.
-/
def mazurProofTreeBackfillCompletionStatus : String :=
  "checked_proof_tree_split_only_terminal_mazur_theorem_remains_formalization_debt"

theorem mazurProofTreeBackfillCompletionStatus_eq :
    mazurProofTreeBackfillCompletionStatus =
      "checked_proof_tree_split_only_terminal_mazur_theorem_remains_formalization_debt" := rfl

end AwesomeTheorems.Stage1.S1_M_088
