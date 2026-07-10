import Mathlib.MeasureTheory.Function.UniformIntegrable
import Mathlib.Probability.Martingale.Basic
import Mathlib.Probability.Martingale.Convergence
import Mathlib.Probability.Martingale.OptionalStopping
import Mathlib.Probability.Process.Predictable

/-!
# S1-M-240 / THM-M-1047: Kazamaki condition

This Stage1 artifact records a conservative Lean 4 boundary for Kazamaki's
criterion for the martingality of stochastic exponentials.

The analytic theorem is a continuous-time/local-martingale result: under the
Kazamaki exponential-submartingale condition, the Doléans-Dade stochastic
exponential of a continuous local martingale is a uniformly integrable
martingale.  At the pinned mathlib revision used by this repository, the local
API has filtrations, predictable processes, martingales/submartingales,
conditional expectations, stopping-time tools, convergence, and uniform
integrability.  It does not expose a terminal Kazamaki theorem, a Novikov
criterion, a local-martingale API, or a stochastic-integral/stochastic-
exponential API.

Accordingly this file provides only a checked statement shape and low-risk
projection wrappers around the currently available mathlib objects.  The fields
`stochasticExponentialFormula`, `kazamakiCondition`, and
`terminalKazamakiConclusion` mark the boundary that a later formalization must
replace by pinned definitions and proofs.  No terminal proof of Kazamaki's
criterion is claimed here.

## mathlib anchor audit at revision 8a178386ffc0f5fef0b77738bb5449d50efeea95

| Anchor | Source module | Repo-local use | Boundary |
|---|---|---|---|
| `MeasureTheory.Martingale` | `Mathlib.Probability.Martingale.Basic` | Encodes the discrete source-process proxy and the future stochastic-exponential conclusion. | This is not a local-martingale or continuous-time stochastic-calculus API. |
| `MeasureTheory.Submartingale` | `Mathlib.Probability.Martingale.Basic` | Encodes the half-exponential Kazamaki-side submartingale placeholder. | The exact continuous Kazamaki condition still has to be formalized. |
| `MeasureTheory.UniformIntegrable` | `Mathlib.MeasureTheory.Function.UniformIntegrable` | Encodes the terminal uniform-integrability target for the stochastic exponential. | It supplies the target property, not the Kazamaki-to-UI theorem. |
| `MeasureTheory.IsPredictable` | `Mathlib.Probability.Process.Predictable` | Confirms that predictable-process vocabulary exists in the pinned closure. | It is not yet connected here to stochastic integrals or local martingales. |
| `MeasureTheory.Submartingale.stoppedProcess` | `Mathlib.Probability.Martingale.OptionalStopping` | Confirms optional-stopping support for stopped submartingales. | It is a discrete stopping-process theorem, not a Kazamaki localization proof. |
| `MeasureTheory.Martingale.ae_eq_condExp_limitProcess` | `Mathlib.Probability.Martingale.Convergence` | Confirms martingale-convergence conditional-expectation support under uniform integrability. | It requires an already established martingale and uniform-integrability hypothesis. |

## KAZ-P3 continuous-local-martingale route decision

This slot should not introduce a second Kazamaki-specific continuous local
martingale structure.  The safe Stage1 route is to reuse the already checked
repo-local continuous-local-martingale boundary as an interim target, while
keeping terminal completion blocked on a pinned upstream or repo-local
stochastic-calculus API for local martingales, quadratic variation, stochastic
integration, and Doléans-Dade stochastic exponentials.  The checked declarations
below record this as a policy object only; they are not a proof of Kazamaki's
criterion.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal NNReal ProbabilityTheory Topology

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_240

universe u

/--
Normalized data for a discrete-index placeholder around Kazamaki's criterion.

The genuine theorem is continuous-time and local-martingale based.  The index is
kept as `ℕ` here because the pinned mathlib martingale/stopping-time API has
strong discrete support, while the continuous stochastic-exponential API is not
available in this repository's Lean dependency closure.
-/
structure KazamakiData (Ω : Type u) [MeasurableSpace Ω] where
  μ : Measure Ω
  filtration : Filtration ℕ ‹MeasurableSpace Ω›
  localMartingaleProxy : ℕ → Ω → ℝ
  quadraticVariationProxy : ℕ → Ω → ℝ
  stochasticExponential : ℕ → Ω → ℝ
  isProbability : IsProbabilityMeasure μ
  sigmaFiniteFiltration : SigmaFiniteFiltration μ filtration
  sourceMartingale : Martingale localMartingaleProxy filtration μ
  sourceSquareIntegrable : ∀ n : ℕ, MemLp (localMartingaleProxy n) 2 μ
  halfExponentialSubmartingale :
    Submartingale (fun n ω => Real.exp (localMartingaleProxy n ω / 2)) filtration μ
  stochasticExponentialAdapted : StronglyAdapted filtration stochasticExponential
  stochasticExponentialPositive : ∀ n : ℕ, 0 ≤ᵐ[μ] stochasticExponential n
  stochasticExponentialFormula :
    ∀ n : ℕ,
      stochasticExponential n =ᵐ[μ]
        fun ω => Real.exp (localMartingaleProxy n ω - quadraticVariationProxy n ω / 2)
  kazamakiCondition : Prop
  localMartingaleContinuityBoundary : Prop
  stochasticIntegralBoundary : Prop
  terminalKazamakiConclusion :
    Martingale stochasticExponential filtration μ ∧
      UniformIntegrable stochasticExponential 1 μ

/--
Hypotheses for the Stage1 statement boundary.

These include the checked mathlib-side objects plus explicit proposition fields
for the currently missing continuous local-martingale, stochastic integral, and
stochastic exponential infrastructure.
-/
def KazamakiHypotheses
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) : Prop :=
  D.kazamakiCondition ∧
    D.localMartingaleContinuityBoundary ∧
      D.stochasticIntegralBoundary

/--
Conclusion package expected from a completed Kazamaki formalization.

A later proof should derive this conclusion from a concrete Kazamaki condition
and a pinned stochastic-exponential construction, rather than carrying it as
data.
-/
def KazamakiConclusion
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) : Prop :=
  Martingale D.stochasticExponential D.filtration D.μ ∧
    UniformIntegrable D.stochasticExponential 1 D.μ

/--
Stage1 normalized statement shape for Kazamaki's criterion.

The `terminalKazamakiConclusion` field is intentionally not part of
`KazamakiHypotheses`; it records the future proof obligation and prevents this
file from pretending that the theorem is already available locally.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ D : KazamakiData Ω,
      KazamakiHypotheses D → KazamakiConclusion D

/-- The normalized statement unfolds to the explicit data-parametrized implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω],
        ∀ D : KazamakiData Ω,
          KazamakiHypotheses D → KazamakiConclusion D :=
  Iff.rfl

/--
Projection wrapper for the future terminal conclusion field.

This is not a Kazamaki proof: it only verifies that the intended conclusion
package has a Lean type accepted by the pinned mathlib APIs.
-/
theorem terminalConclusion_project
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) :
    KazamakiConclusion D :=
  D.terminalKazamakiConclusion

/-- Project the source martingale predicate from the normalized data. -/
theorem source_martingale
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) :
    Martingale D.localMartingaleProxy D.filtration D.μ :=
  D.sourceMartingale

/-- mathlib's martingale API supplies integrability of each source time slice. -/
theorem source_integrable
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) (n : ℕ) :
    Integrable (D.localMartingaleProxy n) D.μ :=
  D.sourceMartingale.integrable n

/-- Project square-integrability of each source time slice from the normalized data. -/
theorem source_memLp_two
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) (n : ℕ) :
    MemLp (D.localMartingaleProxy n) 2 D.μ :=
  D.sourceSquareIntegrable n

/-- Project the Kazamaki half-exponential submartingale condition. -/
theorem half_exponential_submartingale
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) :
    Submartingale (fun n ω => Real.exp (D.localMartingaleProxy n ω / 2))
      D.filtration D.μ :=
  D.halfExponentialSubmartingale

/-- The half-exponential process is integrable at every discrete time. -/
theorem half_exponential_integrable
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) (n : ℕ) :
    Integrable (fun ω => Real.exp (D.localMartingaleProxy n ω / 2)) D.μ :=
  D.halfExponentialSubmartingale.integrable n

/-- Project adaptedness of the stochastic-exponential placeholder. -/
theorem stochasticExponential_stronglyAdapted
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) :
    StronglyAdapted D.filtration D.stochasticExponential :=
  D.stochasticExponentialAdapted

/-- Project the stochastic-exponential positivity side condition. -/
theorem stochasticExponential_nonnegative
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) (n : ℕ) :
    0 ≤ᵐ[D.μ] D.stochasticExponential n :=
  D.stochasticExponentialPositive n

/-- Project the placeholder Doléans-Dade exponential formula. -/
theorem stochasticExponential_formula
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) (n : ℕ) :
    D.stochasticExponential n =ᵐ[D.μ]
      fun ω => Real.exp (D.localMartingaleProxy n ω - D.quadraticVariationProxy n ω / 2) :=
  D.stochasticExponentialFormula n

/-- Project the martingale part of the future Kazamaki conclusion. -/
theorem terminal_stochasticExponential_martingale
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) :
    Martingale D.stochasticExponential D.filtration D.μ :=
  D.terminalKazamakiConclusion.1

/-- Project the uniform-integrability part of the future Kazamaki conclusion. -/
theorem terminal_stochasticExponential_uniformIntegrable
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) :
    UniformIntegrable D.stochasticExponential 1 D.μ :=
  D.terminalKazamakiConclusion.2

/-- Uniform integrability gives `L¹` membership for each stochastic-exponential time slice. -/
theorem terminal_stochasticExponential_memLp_one
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) (n : ℕ) :
    MemLp (D.stochasticExponential n) 1 D.μ :=
  D.terminalKazamakiConclusion.2.memLp n

/-- The terminal martingale conclusion gives integrability of each stochastic-exponential slice. -/
theorem terminal_stochasticExponential_integrable
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) (n : ℕ) :
    Integrable (D.stochasticExponential n) D.μ :=
  D.terminalKazamakiConclusion.1.integrable n

/-! ## KAZ-P3 checked API-route decision. -/

/--
Route classification for the continuous-local-martingale API decision.

The selected route below deliberately avoids creating a second
Kazamaki-specific continuous local martingale structure in this file.
-/
inductive ContinuousLocalMartingaleRoute where
  | newKazamakiSpecificStructure
  | reuseExistingStage1BoundaryWhileWaitingForPinnedUpstream
  | waitForPinnedUpstreamOnly
  deriving DecidableEq, Repr

/--
KAZ-P3 decision: reuse the existing Stage1 continuous-local-martingale boundary
as the interim local target, and wait for or pin an upstream stochastic-calculus
API before claiming a terminal Kazamaki proof.
-/
def selectedContinuousLocalMartingaleRoute : ContinuousLocalMartingaleRoute :=
  .reuseExistingStage1BoundaryWhileWaitingForPinnedUpstream

/--
The selected route is not a new Kazamaki-specific continuous local martingale
structure.
-/
theorem selected_route_not_new_kazamaki_specific :
    selectedContinuousLocalMartingaleRoute ≠
      ContinuousLocalMartingaleRoute.newKazamakiSpecificStructure := by
  decide

/--
The selected route is stronger than waiting passively: it permits reuse of the
checked Stage1 local-martingale boundary while keeping the terminal theorem
blocked on a pinned stochastic-calculus API.
-/
theorem selected_route_reuses_existing_stage1_boundary :
    selectedContinuousLocalMartingaleRoute =
      ContinuousLocalMartingaleRoute.reuseExistingStage1BoundaryWhileWaitingForPinnedUpstream :=
  rfl

/--
Concrete API blockers that must be replaced by definitions/theorems or pinned
upstream declarations before the Kazamaki theorem can be marked complete.
-/
def continuousLocalMartingaleRouteBlockers : List String := [
  "canonical continuous local martingale predicate or structure",
  "localizing stopping-time bridge to stopped martingales",
  "quadratic variation for continuous local martingales",
  "stochastic integral API",
  "Doleans-Dade stochastic exponential API",
  "Kazamaki-to-uniform-integrability theorem"
]

/-! ## KAZ-P4 quadratic-variation and Doleans-Dade API boundary. -/

/--
Route classification for the quadratic-variation and Doleans-Dade stochastic
exponential API required by Kazamaki's criterion.
-/
inductive StochasticCalculusAPIRoute where
  | pinnedMathlibQuadraticVariationAndDoleansDade
  | pinnedExternalQuadraticVariationAndDoleansDade
  | repoLocalStage1SuppliedCandidateOnly
  deriving DecidableEq, Repr

/--
KAZ-P4 decision: the current pinned dependency closure has no canonical
mathlib quadratic-variation or Doleans-Dade stochastic-exponential API, so this
file records a supplied-candidate Stage1 boundary instead of a terminal pin.
-/
def selectedStochasticCalculusAPIRoute : StochasticCalculusAPIRoute :=
  .repoLocalStage1SuppliedCandidateOnly

/-- The KAZ-P4 route is a repo-local supplied-candidate specification only. -/
theorem selected_stochastic_calculus_api_route_is_repo_local_spec :
    selectedStochasticCalculusAPIRoute =
      StochasticCalculusAPIRoute.repoLocalStage1SuppliedCandidateOnly :=
  rfl

/-- The KAZ-P4 route is not a completed mathlib pin. -/
theorem selected_stochastic_calculus_api_route_not_pinned_mathlib :
    selectedStochasticCalculusAPIRoute ≠
      StochasticCalculusAPIRoute.pinnedMathlibQuadraticVariationAndDoleansDade := by
  decide

/--
Supplied-candidate API package for the quadratic variation and Doleans-Dade
stochastic exponential in the Kazamaki slot.

This is deliberately a record of properties for the already stored candidate
processes in `KazamakiData`, not a construction of quadratic variation or a
proof of the Doleans-Dade SDE.  A terminal Kazamaki proof must replace the final
three proposition fields with pinned or repo-local theorem bodies.
-/
structure KazamakiStochasticCalculusAPIs
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) where
  quadraticVariationStronglyAdapted :
    StronglyAdapted D.filtration D.quadraticVariationProxy
  quadraticVariationNonnegative :
    ∀ n : ℕ, 0 ≤ᵐ[D.μ] D.quadraticVariationProxy n
  quadraticVariationStartsAtZero :
    D.quadraticVariationProxy 0 =ᵐ[D.μ] 0
  quadraticVariationIdentifiesBracket : Prop
  quadraticVariationIdentifiesBracketProof :
    quadraticVariationIdentifiesBracket
  stochasticExponentialStronglyAdapted :
    StronglyAdapted D.filtration D.stochasticExponential
  stochasticExponentialPositive :
    ∀ n : ℕ, 0 ≤ᵐ[D.μ] D.stochasticExponential n
  doleansDadeFormula :
    ∀ n : ℕ,
      D.stochasticExponential n =ᵐ[D.μ]
        fun ω => Real.exp (D.localMartingaleProxy n ω - D.quadraticVariationProxy n ω / 2)
  stochasticExponentialSolvesDoleansDadeSDE : Prop
  stochasticExponentialSolvesDoleansDadeSDEProof :
    stochasticExponentialSolvesDoleansDadeSDE
  pinnedOrConstructedAPI : Prop
  pinnedOrConstructedAPIProof : pinnedOrConstructedAPI

/--
The P4 API package is available only when the bracket identification,
Doleans-Dade SDE identification, and pin/construction gate are all supplied.
-/
def KazamakiP4APIsAvailable
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (A : KazamakiStochasticCalculusAPIs D) : Prop :=
  A.quadraticVariationIdentifiesBracket ∧
    A.stochasticExponentialSolvesDoleansDadeSDE ∧
      A.pinnedOrConstructedAPI

/-- Project adaptedness of the P4 quadratic-variation candidate. -/
theorem p4_quadraticVariation_stronglyAdapted
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (A : KazamakiStochasticCalculusAPIs D) :
    StronglyAdapted D.filtration D.quadraticVariationProxy :=
  A.quadraticVariationStronglyAdapted

/-- Project nonnegativity of the P4 quadratic-variation candidate. -/
theorem p4_quadraticVariation_nonnegative
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (A : KazamakiStochasticCalculusAPIs D) (n : ℕ) :
    0 ≤ᵐ[D.μ] D.quadraticVariationProxy n :=
  A.quadraticVariationNonnegative n

/-- Project the zero-start condition of the P4 quadratic-variation candidate. -/
theorem p4_quadraticVariation_startsAtZero
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (A : KazamakiStochasticCalculusAPIs D) :
    D.quadraticVariationProxy 0 =ᵐ[D.μ] 0 :=
  A.quadraticVariationStartsAtZero

/-- Project the bracket-identification boundary for the P4 quadratic variation. -/
theorem p4_quadraticVariation_identifiesBracket
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (A : KazamakiStochasticCalculusAPIs D) :
    A.quadraticVariationIdentifiesBracket :=
  A.quadraticVariationIdentifiesBracketProof

/-- Project adaptedness of the P4 Doleans-Dade stochastic exponential candidate. -/
theorem p4_doleansDade_stronglyAdapted
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (A : KazamakiStochasticCalculusAPIs D) :
    StronglyAdapted D.filtration D.stochasticExponential :=
  A.stochasticExponentialStronglyAdapted

/-- Project positivity of the P4 Doleans-Dade stochastic exponential candidate. -/
theorem p4_doleansDade_positive
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (A : KazamakiStochasticCalculusAPIs D) (n : ℕ) :
    0 ≤ᵐ[D.μ] D.stochasticExponential n :=
  A.stochasticExponentialPositive n

/-- Project the P4 Doleans-Dade exponential formula. -/
theorem p4_doleansDade_formula
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (A : KazamakiStochasticCalculusAPIs D) (n : ℕ) :
    D.stochasticExponential n =ᵐ[D.μ]
      fun ω => Real.exp (D.localMartingaleProxy n ω - D.quadraticVariationProxy n ω / 2) :=
  A.doleansDadeFormula n

/-- Project the Doleans-Dade SDE-identification boundary. -/
theorem p4_doleansDade_solvesSDE
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (A : KazamakiStochasticCalculusAPIs D) :
    A.stochasticExponentialSolvesDoleansDadeSDE :=
  A.stochasticExponentialSolvesDoleansDadeSDEProof

/-- Project the pin/construction gate for the P4 stochastic-calculus API. -/
theorem p4_pinnedOrConstructedAPI
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (A : KazamakiStochasticCalculusAPIs D) :
    A.pinnedOrConstructedAPI :=
  A.pinnedOrConstructedAPIProof

/-- Package the three P4 completion gates from the supplied API record. -/
theorem p4_apis_available_of_api_gates
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (A : KazamakiStochasticCalculusAPIs D)
    (hBracket : A.quadraticVariationIdentifiesBracket)
    (hSDE : A.stochasticExponentialSolvesDoleansDadeSDE)
    (hPinned : A.pinnedOrConstructedAPI) :
    KazamakiP4APIsAvailable A :=
  ⟨hBracket, hSDE, hPinned⟩

/-- A complete supplied P4 API package directly discharges the local P4 API gate. -/
theorem p4_apis_available_of_package
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (A : KazamakiStochasticCalculusAPIs D) :
    KazamakiP4APIsAvailable A :=
  ⟨A.quadraticVariationIdentifiesBracketProof,
    A.stochasticExponentialSolvesDoleansDadeSDEProof,
    A.pinnedOrConstructedAPIProof⟩

/-- The exact repo-local build command for this Stage1 artifact. -/
def p4BuildCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_240.lean"

/-- Checked declarations introduced or exposed for KAZ-P4. -/
def p4CheckedDeclarationNames : List String := [
  "AwesomeTheorems.Stage1.S1_M_240.StochasticCalculusAPIRoute",
  "AwesomeTheorems.Stage1.S1_M_240.selectedStochasticCalculusAPIRoute",
  "AwesomeTheorems.Stage1.S1_M_240.selected_stochastic_calculus_api_route_is_repo_local_spec",
  "AwesomeTheorems.Stage1.S1_M_240.selected_stochastic_calculus_api_route_not_pinned_mathlib",
  "AwesomeTheorems.Stage1.S1_M_240.KazamakiStochasticCalculusAPIs",
  "AwesomeTheorems.Stage1.S1_M_240.KazamakiP4APIsAvailable",
  "AwesomeTheorems.Stage1.S1_M_240.p4_quadraticVariation_stronglyAdapted",
  "AwesomeTheorems.Stage1.S1_M_240.p4_quadraticVariation_nonnegative",
  "AwesomeTheorems.Stage1.S1_M_240.p4_quadraticVariation_startsAtZero",
  "AwesomeTheorems.Stage1.S1_M_240.p4_quadraticVariation_identifiesBracket",
  "AwesomeTheorems.Stage1.S1_M_240.p4_doleansDade_stronglyAdapted",
  "AwesomeTheorems.Stage1.S1_M_240.p4_doleansDade_positive",
  "AwesomeTheorems.Stage1.S1_M_240.p4_doleansDade_formula",
  "AwesomeTheorems.Stage1.S1_M_240.p4_doleansDade_solvesSDE",
  "AwesomeTheorems.Stage1.S1_M_240.p4_pinnedOrConstructedAPI",
  "AwesomeTheorems.Stage1.S1_M_240.p4_apis_available_of_api_gates",
  "AwesomeTheorems.Stage1.S1_M_240.p4_apis_available_of_package",
  "AwesomeTheorems.Stage1.S1_M_240.p4BuildCommand"
]

/--
Requested KAZ-P4 stochastic-calculus API search result against the pinned
mathlib dependency in `Formalizations/Lean/lake-manifest.json`.
-/
def p4PinnedMathlibSearchResults : List String := [
  "QuadraticVariation: no canonical `Mathlib/` source match at mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "Doleans/Doléans/Dade stochastic exponential: no canonical `Mathlib/` source match at mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "StochasticExponential: no canonical `Mathlib/` source match at mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "StochasticIntegral/local martingale/semimartingale terminal API: no canonical `Mathlib/` source match at mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95"
]

/-! ## KAZ-P5 half-exponential Kazamaki condition with localization. -/

/--
The Kazamaki half-exponential process attached to the source martingale proxy.

For a genuine continuous local martingale `M`, this is the process usually
written `exp (M / 2)`.  The repository currently models it over the discrete
time index supported by the pinned martingale and stopping-time API.
-/
def kazamakiHalfExponentialProcess
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) :
    ℕ → Ω → ℝ :=
  fun n ω => Real.exp (D.localMartingaleProxy n ω / 2)

/--
Stopping/localization parameters for the repo-local Kazamaki condition.

The finite `horizon` is the checked discrete substitute for a terminal time.
The family `localizingStops` records the stopping times used to localize the
source local martingale and the half-exponential Kazamaki condition.  The
monotonicity and exhaustion fields are kept as explicit gates because mathlib
does not yet provide the continuous local-martingale localization package
needed for the terminal theorem.
-/
structure KazamakiLocalizationParameters
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) where
  horizon : ℕ
  localizingStops : ℕ → Ω → WithTop ℕ
  localizingStops_isStoppingTime :
    ∀ k : ℕ, IsStoppingTime D.filtration (localizingStops k)
  localizingStops_boundedByHorizon :
    ∀ k : ℕ, ∀ ω : Ω, localizingStops k ω ≤ horizon
  localizingStops_monotone :
    ∀ {k l : ℕ}, k ≤ l → ∀ ω : Ω, localizingStops k ω ≤ localizingStops l ω
  localizingStops_exhaustHorizon :
    ∀ ω : Ω, ∃ k : ℕ, localizingStops k ω = horizon

/--
The half-exponential process stopped at one localization parameter.
-/
def kazamakiStoppedHalfExponential
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (L : KazamakiLocalizationParameters D) (k : ℕ) :
    ℕ → Ω → ℝ :=
  stoppedProcess (kazamakiHalfExponentialProcess D) (L.localizingStops k)

/--
KAZ-P5 package: the exact Stage1 half-exponential Kazamaki condition.

The analytic theorem says that the half-exponential process associated to the
source local martingale satisfies a submartingale condition after the relevant
stopping/localization parameters are fixed.  This package records that checked
shape: every localizing stop is a stopping time, bounded by the finite horizon,
monotone and horizon-exhausting, and each localized half-exponential process is
a mathlib `Submartingale`.

This is still a condition package, not the bridge from Kazamaki's condition to
uniform integrability of the Doléans-Dade stochastic exponential.
-/
structure KazamakiHalfExponentialCondition
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω) where
  localization : KazamakiLocalizationParameters D
  localizedHalfExponentialSubmartingale :
    ∀ k : ℕ,
      Submartingale (kazamakiStoppedHalfExponential localization k)
        D.filtration D.μ
  halfExponentialConditionPinsKazamakiHypothesis : Prop
  halfExponentialConditionPinsKazamakiHypothesisProof :
    halfExponentialConditionPinsKazamakiHypothesis

/-- Project the finite terminal horizon from the P5 localization package. -/
def p5_horizon
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (K : KazamakiHalfExponentialCondition D) :
    ℕ :=
  K.localization.horizon

/-- Project the `k`-th localizing stopping time from the P5 condition package. -/
def p5_localizingStop
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (K : KazamakiHalfExponentialCondition D) (k : ℕ) :
    Ω → WithTop ℕ :=
  K.localization.localizingStops k

/-- Project the stopping-time proof for the `k`-th localizing stop. -/
theorem p5_localizingStop_isStoppingTime
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (K : KazamakiHalfExponentialCondition D) (k : ℕ) :
    IsStoppingTime D.filtration (K.localization.localizingStops k) :=
  K.localization.localizingStops_isStoppingTime k

/-- Project the finite-horizon bound for the `k`-th localizing stop. -/
theorem p5_localizingStop_boundedByHorizon
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (K : KazamakiHalfExponentialCondition D) (k : ℕ) (ω : Ω) :
    K.localization.localizingStops k ω ≤ K.localization.horizon :=
  K.localization.localizingStops_boundedByHorizon k ω

/-- Project monotonicity of the P5 localizing stopping-time family. -/
theorem p5_localizingStop_monotone
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (K : KazamakiHalfExponentialCondition D) {k l : ℕ} (hkl : k ≤ l)
    (ω : Ω) :
    K.localization.localizingStops k ω ≤ K.localization.localizingStops l ω :=
  K.localization.localizingStops_monotone hkl ω

/-- Project horizon exhaustion of the P5 localizing stopping-time family. -/
theorem p5_localizingStop_exhaustHorizon
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (K : KazamakiHalfExponentialCondition D) (ω : Ω) :
    ∃ k : ℕ, K.localization.localizingStops k ω = K.localization.horizon :=
  K.localization.localizingStops_exhaustHorizon ω

/-- Project the localized half-exponential submartingale condition. -/
theorem p5_localized_halfExponential_submartingale
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (K : KazamakiHalfExponentialCondition D) (k : ℕ) :
    Submartingale (kazamakiStoppedHalfExponential K.localization k)
      D.filtration D.μ :=
  K.localizedHalfExponentialSubmartingale k

/-- Each localized half-exponential slice is integrable. -/
theorem p5_localized_halfExponential_integrable
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (K : KazamakiHalfExponentialCondition D) (k n : ℕ) :
    Integrable (kazamakiStoppedHalfExponential K.localization k n) D.μ :=
  (K.localizedHalfExponentialSubmartingale k).integrable n

/--
Optional-stopping monotonicity for the localized half-exponential condition.

This is the checked discrete stopping-parameter consequence available in the
current mathlib API: for bounded ordered stopping probes `σ ≤ τ`, the
expectation of the localized half-exponential stopped at `σ` is bounded above
by the expectation stopped at `τ`.
-/
theorem p5_localized_halfExponential_expected_stoppedValue_mono
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (K : KazamakiHalfExponentialCondition D) (k : ℕ)
    {σ τ : Ω → WithTop ℕ}
    (hσ : IsStoppingTime D.filtration σ)
    (hτ : IsStoppingTime D.filtration τ)
    (hστ : σ ≤ τ) {N : ℕ} (hτ_bdd : ∀ ω : Ω, τ ω ≤ N) :
    D.μ[stoppedValue (kazamakiStoppedHalfExponential K.localization k) σ] ≤
      D.μ[stoppedValue (kazamakiStoppedHalfExponential K.localization k) τ] := by
  letI : SigmaFiniteFiltration D.μ D.filtration := D.sigmaFiniteFiltration
  exact (K.localizedHalfExponentialSubmartingale k).expected_stoppedValue_mono
    hσ hτ hστ hτ_bdd

/--
The existing global half-exponential submartingale field localizes through
mathlib's stopped-process theorem whenever a stopping time is supplied.
-/
theorem p5_localized_halfExponential_of_global
    {Ω : Type u} [MeasurableSpace Ω] (D : KazamakiData Ω)
    (L : KazamakiLocalizationParameters D) (k : ℕ) :
    Submartingale (kazamakiStoppedHalfExponential L k) D.filtration D.μ := by
  letI : SigmaFiniteFiltration D.μ D.filtration := D.sigmaFiniteFiltration
  exact D.halfExponentialSubmartingale.stoppedProcess
    (L.localizingStops_isStoppingTime k)

/-- Project the P5 pin/equivalence gate for the selected Kazamaki hypothesis. -/
theorem p5_condition_pins_kazamaki_hypothesis
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (K : KazamakiHalfExponentialCondition D) :
    K.halfExponentialConditionPinsKazamakiHypothesis :=
  K.halfExponentialConditionPinsKazamakiHypothesisProof

/-- Checked declarations introduced or exposed for KAZ-P5. -/
def p5CheckedDeclarationNames : List String := [
  "AwesomeTheorems.Stage1.S1_M_240.kazamakiHalfExponentialProcess",
  "AwesomeTheorems.Stage1.S1_M_240.KazamakiLocalizationParameters",
  "AwesomeTheorems.Stage1.S1_M_240.kazamakiStoppedHalfExponential",
  "AwesomeTheorems.Stage1.S1_M_240.KazamakiHalfExponentialCondition",
  "AwesomeTheorems.Stage1.S1_M_240.p5_horizon",
  "AwesomeTheorems.Stage1.S1_M_240.p5_localizingStop",
  "AwesomeTheorems.Stage1.S1_M_240.p5_localizingStop_isStoppingTime",
  "AwesomeTheorems.Stage1.S1_M_240.p5_localizingStop_boundedByHorizon",
  "AwesomeTheorems.Stage1.S1_M_240.p5_localizingStop_monotone",
  "AwesomeTheorems.Stage1.S1_M_240.p5_localizingStop_exhaustHorizon",
  "AwesomeTheorems.Stage1.S1_M_240.p5_localized_halfExponential_submartingale",
  "AwesomeTheorems.Stage1.S1_M_240.p5_localized_halfExponential_integrable",
  "AwesomeTheorems.Stage1.S1_M_240.p5_localized_halfExponential_expected_stoppedValue_mono",
  "AwesomeTheorems.Stage1.S1_M_240.p5_localized_halfExponential_of_global",
  "AwesomeTheorems.Stage1.S1_M_240.p5_condition_pins_kazamaki_hypothesis"
]

/-!
KAZ-P5 status boundary: this file now has a checked repo-local condition
package for the half-exponential submartingale side, including finite-horizon
and stopping/localization parameters.  The remaining formalization debt is the
continuous-time local-martingale interpretation and the P6 bridge from this
condition to true martingality and uniform integrability of the stochastic
exponential.
-/

/-! ## KAZ-P6 Kazamaki-to-UI martingality bridge boundary. -/

/--
Machine status for the P6 bridge from the Kazamaki condition to true
martingality and uniform integrability of the stochastic exponential.

The selected status below is deliberately open: the pinned mathlib closure has
the target predicates, but no terminal Kazamaki/Novikov/stochastic-exponential
bridge theorem to wrap.
-/
inductive KazamakiP6BridgeStatus where
  | pinnedMathlibBridge
  | pinnedExternalBridge
  | repoLocalProofBody
  | openFormalizationDebt
  deriving DecidableEq, Repr

/-- Current P6 status: no repo-local or pinned upstream bridge theorem is present. -/
def selectedKazamakiP6BridgeStatus : KazamakiP6BridgeStatus :=
  .openFormalizationDebt

/-- P6 is not closed by a pinned mathlib theorem in the current dependency closure. -/
theorem selected_p6_bridge_status_not_pinned_mathlib :
    selectedKazamakiP6BridgeStatus ≠
      KazamakiP6BridgeStatus.pinnedMathlibBridge := by
  decide

/-- P6 is not closed by a pinned external Lean 4 theorem in this repository. -/
theorem selected_p6_bridge_status_not_pinned_external :
    selectedKazamakiP6BridgeStatus ≠
      KazamakiP6BridgeStatus.pinnedExternalBridge := by
  decide

/-- P6 is not closed by a repo-local proof body in this file. -/
theorem selected_p6_bridge_status_not_repo_local_proof :
    selectedKazamakiP6BridgeStatus ≠
      KazamakiP6BridgeStatus.repoLocalProofBody := by
  decide

/-- The current P6 bridge status is explicitly open formalization debt. -/
theorem selected_p6_bridge_status_open_formalization_debt :
    selectedKazamakiP6BridgeStatus =
      KazamakiP6BridgeStatus.openFormalizationDebt :=
  rfl

/--
Input package for any future P6 bridge theorem.

It deliberately joins the P4 stochastic-calculus API gate, the P5
half-exponential condition gate, and the original Kazamaki hypotheses.  A
terminal proof must turn these inputs into `KazamakiConclusion D`; this
definition only records the checked shape of that bridge obligation.
-/
def KazamakiP6BridgeInputs
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (A : KazamakiStochasticCalculusAPIs D)
    (K : KazamakiHalfExponentialCondition D) : Prop :=
  KazamakiP4APIsAvailable A ∧
    K.halfExponentialConditionPinsKazamakiHypothesis ∧
      KazamakiHypotheses D

/--
Checked assembly of the P6 input package from the previously verified P4 and
P5 gates, plus the original statement hypotheses.
-/
theorem p6_bridge_inputs_of_packages
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (A : KazamakiStochasticCalculusAPIs D)
    (K : KazamakiHalfExponentialCondition D)
    (hHyp : KazamakiHypotheses D) :
    KazamakiP6BridgeInputs A K :=
  ⟨p4_apis_available_of_package A,
    K.halfExponentialConditionPinsKazamakiHypothesisProof,
    hHyp⟩

/--
P6 bridge theorem package expected from a completed Kazamaki formalization.

The field `conclusion_of_bridgeInputs` is the missing theorem: it must be
provided by a local proof body, a wrapper around pinned mathlib, or a pinned
external Lean dependency before the parent theorem can be marked complete.
Until then, this structure is only an integration target.
-/
structure KazamakiP6Bridge
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    (A : KazamakiStochasticCalculusAPIs D)
    (K : KazamakiHalfExponentialCondition D) where
  bridgePinnedOrRepoLocal : Prop
  bridgePinnedOrRepoLocalProof : bridgePinnedOrRepoLocal
  conclusion_of_bridgeInputs :
    KazamakiP6BridgeInputs A K → KazamakiConclusion D

/-- Project the P6 pin/local-proof gate from a supplied bridge package. -/
theorem p6_bridge_pinned_or_repoLocal
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    {A : KazamakiStochasticCalculusAPIs D}
    {K : KazamakiHalfExponentialCondition D}
    (B : KazamakiP6Bridge A K) :
    B.bridgePinnedOrRepoLocal :=
  B.bridgePinnedOrRepoLocalProof

/--
Conditional P6 conclusion wrapper.

This is not an unconditional proof of Kazamaki's criterion.  It says that once
the P6 bridge package is supplied and pinned/repo-local, the existing P4/P5
packages produce the terminal conclusion shape.
-/
theorem p6_conclusion_of_bridge
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    {A : KazamakiStochasticCalculusAPIs D}
    {K : KazamakiHalfExponentialCondition D}
    (B : KazamakiP6Bridge A K)
    (hHyp : KazamakiHypotheses D) :
    KazamakiConclusion D :=
  B.conclusion_of_bridgeInputs
    (p6_bridge_inputs_of_packages A K hHyp)

/-- Conditional projection of true martingality from a supplied P6 bridge. -/
theorem p6_stochasticExponential_martingale_of_bridge
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    {A : KazamakiStochasticCalculusAPIs D}
    {K : KazamakiHalfExponentialCondition D}
    (B : KazamakiP6Bridge A K)
    (hHyp : KazamakiHypotheses D) :
    Martingale D.stochasticExponential D.filtration D.μ :=
  (p6_conclusion_of_bridge B hHyp).1

/-- Conditional projection of uniform integrability from a supplied P6 bridge. -/
theorem p6_stochasticExponential_uniformIntegrable_of_bridge
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    {A : KazamakiStochasticCalculusAPIs D}
    {K : KazamakiHalfExponentialCondition D}
    (B : KazamakiP6Bridge A K)
    (hHyp : KazamakiHypotheses D) :
    UniformIntegrable D.stochasticExponential 1 D.μ :=
  (p6_conclusion_of_bridge B hHyp).2

/-- Conditional `L¹` consequence from the uniform-integrability half of P6. -/
theorem p6_stochasticExponential_memLp_one_of_bridge
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    {A : KazamakiStochasticCalculusAPIs D}
    {K : KazamakiHalfExponentialCondition D}
    (B : KazamakiP6Bridge A K)
    (hHyp : KazamakiHypotheses D) (n : ℕ) :
    MemLp (D.stochasticExponential n) 1 D.μ :=
  (p6_stochasticExponential_uniformIntegrable_of_bridge B hHyp).memLp n

/-- Conditional integrability consequence from the true-martingale half of P6. -/
theorem p6_stochasticExponential_integrable_of_bridge
    {Ω : Type u} [MeasurableSpace Ω] {D : KazamakiData Ω}
    {A : KazamakiStochasticCalculusAPIs D}
    {K : KazamakiHalfExponentialCondition D}
    (B : KazamakiP6Bridge A K)
    (hHyp : KazamakiHypotheses D) (n : ℕ) :
    Integrable (D.stochasticExponential n) D.μ :=
  (p6_stochasticExponential_martingale_of_bridge B hHyp).integrable n

/-- Checked declarations introduced or exposed for KAZ-P6. -/
def p6CheckedDeclarationNames : List String := [
  "AwesomeTheorems.Stage1.S1_M_240.KazamakiP6BridgeStatus",
  "AwesomeTheorems.Stage1.S1_M_240.selectedKazamakiP6BridgeStatus",
  "AwesomeTheorems.Stage1.S1_M_240.selected_p6_bridge_status_not_pinned_mathlib",
  "AwesomeTheorems.Stage1.S1_M_240.selected_p6_bridge_status_not_pinned_external",
  "AwesomeTheorems.Stage1.S1_M_240.selected_p6_bridge_status_not_repo_local_proof",
  "AwesomeTheorems.Stage1.S1_M_240.selected_p6_bridge_status_open_formalization_debt",
  "AwesomeTheorems.Stage1.S1_M_240.KazamakiP6BridgeInputs",
  "AwesomeTheorems.Stage1.S1_M_240.p6_bridge_inputs_of_packages",
  "AwesomeTheorems.Stage1.S1_M_240.KazamakiP6Bridge",
  "AwesomeTheorems.Stage1.S1_M_240.p6_bridge_pinned_or_repoLocal",
  "AwesomeTheorems.Stage1.S1_M_240.p6_conclusion_of_bridge",
  "AwesomeTheorems.Stage1.S1_M_240.p6_stochasticExponential_martingale_of_bridge",
  "AwesomeTheorems.Stage1.S1_M_240.p6_stochasticExponential_uniformIntegrable_of_bridge",
  "AwesomeTheorems.Stage1.S1_M_240.p6_stochasticExponential_memLp_one_of_bridge",
  "AwesomeTheorems.Stage1.S1_M_240.p6_stochasticExponential_integrable_of_bridge"
]

/--
P6 local-search result against the pinned mathlib dependency.

The target predicates are present, but this repository has no checked theorem
turning Kazamaki's condition into the terminal stochastic-exponential
conclusion.
-/
def p6PinnedMathlibSearchResults : List String := [
  "Kazamaki: no canonical `Mathlib/` source match at mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "Novikov: no canonical `Mathlib/` source match at mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "StochasticExponential / exponential martingale bridge: no canonical `Mathlib/` source match at mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "Kazamaki-to-uniform-integrability bridge theorem: no pinned or repo-local Lean theorem in the current Lake closure"
]

/-! ## KAZ-P8 external Lean proof integration gate. -/

/--
External-proof status for the KAZ-P8 gate.

The completed states require a proof body to be inside this repository's Lake
closure, either by direct local proof, pinned mathlib wrapper, or pinned
external dependency.  Anchor-only evidence is deliberately not a completed
state.
-/
inductive KazamakiP8ExternalProofStatus where
  | noExactExternalTerminalProofFound
  | externalProofFoundIntegrationBlocked
  | externalUpstreamPinnedAndChecked
  | localWrapperOrProofBodyChecked
  deriving DecidableEq, Repr

/--
Current KAZ-P8 status after the primary-source audit: no exact external Lean 4
terminal proof of Kazamaki's criterion was found.
-/
def selectedKazamakiP8ExternalProofStatus : KazamakiP8ExternalProofStatus :=
  .noExactExternalTerminalProofFound

/-- KAZ-P8 is not closed by a pinned external dependency in this repository. -/
theorem selected_p8_status_not_external_pinned :
    selectedKazamakiP8ExternalProofStatus ≠
      KazamakiP8ExternalProofStatus.externalUpstreamPinnedAndChecked := by
  decide

/-- KAZ-P8 is not closed by a local wrapper or local proof body in this file. -/
theorem selected_p8_status_not_local_wrapper_or_proof :
    selectedKazamakiP8ExternalProofStatus ≠
      KazamakiP8ExternalProofStatus.localWrapperOrProofBodyChecked := by
  decide

/-- The current KAZ-P8 status is the negative external-terminal-proof finding. -/
theorem selected_p8_status_no_exact_external_terminal_proof :
    selectedKazamakiP8ExternalProofStatus =
      KazamakiP8ExternalProofStatus.noExactExternalTerminalProofFound :=
  rfl

/-- Absolute date of the KAZ-P8 external-proof audit. -/
def p8ExternalProofAuditDate : String :=
  "2026-05-01"

/-- Search surfaces used for the KAZ-P8 external-proof audit. -/
def p8ExternalProofSearchSurfaces : List String := [
  "pinned repo-local mathlib source tree under Formalizations/Lean/.lake/packages/mathlib/Mathlib",
  "repo-local Stage1 stochastic-calculus artifacts S1_M_237.lean, S1_M_239.lean, and S1_M_240.lean",
  "public web search for exact phrases `Kazamaki` plus `Lean 4`, `mathlib`, and `GitHub`",
  "GitHub REST repository search for Kazamaki/Lean and BrownianMotion/Lean4/stochastic-integral candidates",
  "GitHub REST code search for `Kazamaki language:Lean`, which returned a 401 authentication requirement and therefore was not completion evidence"
]

/-- Search terms used for the KAZ-P8 external terminal proof audit. -/
def p8ExternalProofSearchTerms : List String := [
  "Kazamaki",
  "Kazamaki theorem",
  "Kazamaki Lean 4",
  "Kazamaki mathlib",
  "Novikov",
  "StochasticExponential",
  "stochastic exponential",
  "Doleans-Dade",
  "exponential martingale",
  "continuous local martingale"
]

/--
Primary external Lean project checked as an adjacent stochastic-calculus
candidate for KAZ-P8.

It has useful local-martingale and quadratic-variation scaffolding, but no
terminal Kazamaki proof was found there, so it is not a proof dependency to pin.
-/
def p8AdjacentExternalCandidate : List String := [
  "repository: https://github.com/RemyDegenne/brownian-motion",
  "audited commit: 91885e6172648ea7f9c6a16b3a7069f92c88e023",
  "commit date: 2026-05-01T06:05:08Z",
  "lean-toolchain: leanprover/lean4:v4.30.0-rc1",
  "mathlib dependency: f23306121184717ace04f3ac514be974e3224c8b",
  "adjacent modules: BrownianMotion/StochasticIntegral/LocalMartingale.lean, QuadraticVariation.lean, SimpleProcess.lean, L2M.lean, DoobMeyer.lean"
]

/--
Positive adjacent anchors found in the external candidate.

These anchors are not imported here and do not prove Kazamaki's criterion.
-/
def p8AdjacentExternalAnchors : List String := [
  "BrownianMotion/StochasticIntegral/LocalMartingale.lean defines ProbabilityTheory.IsLocalMartingale",
  "BrownianMotion/StochasticIntegral/LocalMartingale.lean defines ProbabilityTheory.IsLocalSubmartingale",
  "BrownianMotion/StochasticIntegral/QuadraticVariation.lean defines ProbabilityTheory.quadraticVariation",
  "BrownianMotion/StochasticIntegral/SimpleProcess.lean defines ProbabilityTheory.SimpleProcess.integral",
  "BrownianMotion/StochasticIntegral/L2M.lean defines ProbabilityTheory.L2Predictable"
]

/-- Negative terminal-proof findings for KAZ-P8. -/
def p8NegativeTerminalProofFindings : List String := [
  "No exact Lean 4 theorem named or described as Kazamaki's criterion was found in the current repo-local Lake closure.",
  "No exact Kazamaki source match was found in the pinned mathlib source tree at commit 8a178386ffc0f5fef0b77738bb5449d50efeea95.",
  "Public web search did not locate a primary Lean 4 repository containing a terminal Kazamaki theorem.",
  "GitHub REST repository search for Kazamaki/Lean returned no repository candidates.",
  "The adjacent brownian-motion project has no source match for Kazamaki, StochasticExponential, stochastic exponential, Doleans-Dade, or exponential martingale at commit 91885e6172648ea7f9c6a16b3a7069f92c88e023."
]

/--
Concrete blockers preventing the audited adjacent external project from closing
KAZ-P8 as an external proof dependency.
-/
def p8AdjacentExternalIntegrationBlockers : List String := [
  "No terminal theorem for Kazamaki's condition was found in the audited external sources.",
  "No Doleans-Dade or stochastic-exponential construction was found in the audited external sources.",
  "The adjacent project uses Lean 4.30.0-rc1 and mathlib f23306121184717ace04f3ac514be974e3224c8b, while this repository validates S1_M_240.lean against Lean 4.29.0 and mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95.",
  "The adjacent project is not pinned or imported into this repository's Lake closure.",
  "A future discovery of an exact terminal proof would require a pinned dependency or vendored proof body plus a repo-local wrapper checked by `lake env lean` before any completion claim."
]

/--
KAZ-P8 repo-local integration-debt gate.

Since no exact external terminal proof was found, there is no known proof body
left as anchor-only completed evidence.  The parent theorem remains open as
formalization debt, not completed with repo-local integration debt.
-/
def p8RepoLocalIntegrationDebtGate : String :=
  "passed for this audit child: no exact external terminal proof was found, no anchor-only evidence is marked completed, and the parent remains formalization debt"

/-- Checked declarations introduced or exposed for KAZ-P8. -/
def p8CheckedDeclarationNames : List String := [
  "AwesomeTheorems.Stage1.S1_M_240.KazamakiP8ExternalProofStatus",
  "AwesomeTheorems.Stage1.S1_M_240.selectedKazamakiP8ExternalProofStatus",
  "AwesomeTheorems.Stage1.S1_M_240.selected_p8_status_not_external_pinned",
  "AwesomeTheorems.Stage1.S1_M_240.selected_p8_status_not_local_wrapper_or_proof",
  "AwesomeTheorems.Stage1.S1_M_240.selected_p8_status_no_exact_external_terminal_proof",
  "AwesomeTheorems.Stage1.S1_M_240.p8ExternalProofAuditDate",
  "AwesomeTheorems.Stage1.S1_M_240.p8ExternalProofSearchSurfaces",
  "AwesomeTheorems.Stage1.S1_M_240.p8ExternalProofSearchTerms",
  "AwesomeTheorems.Stage1.S1_M_240.p8AdjacentExternalCandidate",
  "AwesomeTheorems.Stage1.S1_M_240.p8AdjacentExternalAnchors",
  "AwesomeTheorems.Stage1.S1_M_240.p8NegativeTerminalProofFindings",
  "AwesomeTheorems.Stage1.S1_M_240.p8AdjacentExternalIntegrationBlockers",
  "AwesomeTheorems.Stage1.S1_M_240.p8RepoLocalIntegrationDebtGate"
]

/-! ## Audit probes retained in the checked file. -/

#check ContinuousLocalMartingaleRoute
#check selectedContinuousLocalMartingaleRoute
#check selected_route_not_new_kazamaki_specific
#check selected_route_reuses_existing_stage1_boundary
#check StochasticCalculusAPIRoute
#check selectedStochasticCalculusAPIRoute
#check selected_stochastic_calculus_api_route_is_repo_local_spec
#check selected_stochastic_calculus_api_route_not_pinned_mathlib
#check KazamakiStochasticCalculusAPIs
#check KazamakiP4APIsAvailable
#check p4_quadraticVariation_stronglyAdapted
#check p4_quadraticVariation_nonnegative
#check p4_quadraticVariation_startsAtZero
#check p4_quadraticVariation_identifiesBracket
#check p4_doleansDade_stronglyAdapted
#check p4_doleansDade_positive
#check p4_doleansDade_formula
#check p4_doleansDade_solvesSDE
#check p4_pinnedOrConstructedAPI
#check p4_apis_available_of_api_gates
#check p4_apis_available_of_package
#check p4BuildCommand
#check p4CheckedDeclarationNames
#check p4PinnedMathlibSearchResults
#check kazamakiHalfExponentialProcess
#check KazamakiLocalizationParameters
#check kazamakiStoppedHalfExponential
#check KazamakiHalfExponentialCondition
#check p5_horizon
#check p5_localizingStop
#check p5_localizingStop_isStoppingTime
#check p5_localizingStop_boundedByHorizon
#check p5_localizingStop_monotone
#check p5_localizingStop_exhaustHorizon
#check p5_localized_halfExponential_submartingale
#check p5_localized_halfExponential_integrable
#check p5_localized_halfExponential_expected_stoppedValue_mono
#check p5_localized_halfExponential_of_global
#check p5_condition_pins_kazamaki_hypothesis
#check p5CheckedDeclarationNames
#check KazamakiP6BridgeStatus
#check selectedKazamakiP6BridgeStatus
#check selected_p6_bridge_status_not_pinned_mathlib
#check selected_p6_bridge_status_not_pinned_external
#check selected_p6_bridge_status_not_repo_local_proof
#check selected_p6_bridge_status_open_formalization_debt
#check KazamakiP6BridgeInputs
#check p6_bridge_inputs_of_packages
#check KazamakiP6Bridge
#check p6_bridge_pinned_or_repoLocal
#check p6_conclusion_of_bridge
#check p6_stochasticExponential_martingale_of_bridge
#check p6_stochasticExponential_uniformIntegrable_of_bridge
#check p6_stochasticExponential_memLp_one_of_bridge
#check p6_stochasticExponential_integrable_of_bridge
#check p6CheckedDeclarationNames
#check p6PinnedMathlibSearchResults
#check KazamakiP8ExternalProofStatus
#check selectedKazamakiP8ExternalProofStatus
#check selected_p8_status_not_external_pinned
#check selected_p8_status_not_local_wrapper_or_proof
#check selected_p8_status_no_exact_external_terminal_proof
#check p8ExternalProofAuditDate
#check p8ExternalProofSearchSurfaces
#check p8ExternalProofSearchTerms
#check p8AdjacentExternalCandidate
#check p8AdjacentExternalAnchors
#check p8NegativeTerminalProofFindings
#check p8AdjacentExternalIntegrationBlockers
#check p8RepoLocalIntegrationDebtGate
#check p8CheckedDeclarationNames
#check MeasureTheory.Filtration
#check MeasureTheory.SigmaFiniteFiltration
#check MeasureTheory.StronglyAdapted
#check MeasureTheory.IsPredictable
#check MeasureTheory.Martingale
#check MeasureTheory.Martingale.integrable
#check MeasureTheory.Submartingale
#check MeasureTheory.Submartingale.integrable
#check MeasureTheory.UniformIntegrable
#check MeasureTheory.UniformIntegrable.memLp
#check MeasureTheory.Martingale.ae_eq_condExp_limitProcess
#check MeasureTheory.Submartingale.ae_tendsto_limitProcess
#check MeasureTheory.Submartingale.stoppedProcess

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Function.UniformIntegrable",
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Martingale.Convergence",
  "Mathlib.Probability.Martingale.OptionalSampling",
  "Mathlib.Probability.Martingale.OptionalStopping",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Adapted",
  "Mathlib.Probability.Process.Predictable",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Moments.Basic",
  "Mathlib.MeasureTheory.Measure.Tilted",
  "Mathlib.MeasureTheory.Measure.LogLikelihoodRatio"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.Filtration",
  "MeasureTheory.SigmaFiniteFiltration",
  "MeasureTheory.StronglyAdapted",
  "MeasureTheory.IsPredictable",
  "MeasureTheory.Martingale",
  "MeasureTheory.Martingale.integrable",
  "MeasureTheory.Martingale.condExp_ae_eq",
  "MeasureTheory.Martingale.ae_eq_condExp_limitProcess",
  "MeasureTheory.Submartingale",
  "MeasureTheory.Submartingale.integrable",
  "MeasureTheory.Submartingale.ae_tendsto_limitProcess",
  "MeasureTheory.Submartingale.stoppedProcess",
  "MeasureTheory.UniformIntegrable",
  "MeasureTheory.UniformIntegrable.memLp",
  "MeasureTheory.Integrable.uniformIntegrable_condExp_filtration"
]

/--
Search terms audited while checking for a terminal Kazamaki or stochastic
exponential anchor.
-/
def absentTerminalSearchTerms : List String := [
  "Kazamaki",
  "Novikov",
  "Doleans",
  "Doléans",
  "stochastic exponential",
  "StochasticExponential",
  "exponential martingale",
  "ExponentialMartingale",
  "local martingale",
  "LocalMartingale",
  "quadratic variation",
  "QuadraticVariation"
]

/-! ## KAZ-P7 validation record. -/

/-- Exact repo-local validation command for the latest KAZ-P7 rerun. -/
def p7ValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_240.lean"

/-- Exact calendar date of the latest KAZ-P7 validation rerun. -/
def p7ValidationDate : String :=
  "2026-05-01"

/--
Result of the latest KAZ-P7 validation rerun.

This records validation of the Stage1 artifact only.  It is not a completion
claim for Kazamaki's criterion.
-/
def p7ValidationResult : String :=
  "passed with exit code 0"

/--
KAZ-P7 repo-local integration-debt gate for the validation rerun.

The validation pass checks this Stage1 boundary file.  The parent theorem still
has open formalization debt: no terminal Kazamaki theorem, stochastic
exponential API, or Kazamaki-to-uniform-integrability bridge has been proved or
pinned in the repo-local Lake closure.
-/
def p7RepoLocalIntegrationDebtGate : String :=
  "passed for the validation-record child; no completed theorem state is claimed"

#check p7ValidationCommand
#check p7ValidationDate
#check p7ValidationResult
#check p7RepoLocalIntegrationDebtGate

end S1_M_240
end Stage1
end AwesomeTheorems
