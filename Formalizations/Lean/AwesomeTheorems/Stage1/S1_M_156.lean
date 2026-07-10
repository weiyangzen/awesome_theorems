import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.MeasureTheory.Function.LpSpace.Basic
import Mathlib.MeasureTheory.Measure.Hausdorff

/-!
# S1-M-156 / THM-M-1228: Caffarelli-Kohn-Nirenberg theorem

This Stage1 artifact records a conservative Lean statement-shape boundary for
the Caffarelli-Kohn-Nirenberg partial regularity theorem for suitable weak
solutions of the three-dimensional incompressible Navier-Stokes equations.

The pinned mathlib snapshot
`8a178386ffc0f5fef0b77738bb5449d50efeea95` has Lp predicates,
distribution/test-function infrastructure, smoothness predicates,
Sobolev-adjacent estimates, and Hausdorff measure. It does not expose a
terminal Navier-Stokes suitable-weak solution API, local energy inequality
package, parabolic Hausdorff metric, or CKN partial regularity theorem.

The declarations below therefore keep the PDE equation and local energy
inequality as explicit proposition fields while making the regularity locus,
singular set, Lp hypotheses, and Euclidean Hausdorff-measure surrogate
checkable in local Lean.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal

namespace AwesomeTheorems.Stage1.S1_M_156

/-- Three-dimensional space-time for the classical Navier-Stokes setting. -/
abbrev SpaceTime : Type := (Fin 3 → ℝ) × ℝ

/-- Velocity values in three spatial dimensions. -/
abbrev Velocity : Type := Fin 3 → ℝ

/-- The measure used for local space-time integrability hypotheses. -/
def domainMeasure (Ω : Set SpaceTime) : Measure SpaceTime :=
  Measure.restrict (volume : Measure SpaceTime) Ω

/--
Data package for a suitable weak Navier-Stokes solution.

The Lp fields are concrete mathlib predicates. The weak equation,
divergence-free constraint, local energy inequality, and parabolic metric model
are kept as propositions because the audited dependency closure has no
canonical CKN-specific API for them.
-/
structure SuitableWeakSolutionData where
  domain : Set SpaceTime
  velocity : SpaceTime → Velocity
  pressure : SpaceTime → ℝ
  force : SpaceTime → Velocity
  domain_isOpen : IsOpen domain
  velocity_energy_memLp : MemLp velocity (2 : ℝ≥0∞) (domainMeasure domain)
  velocity_cubic_memLp : MemLp velocity (3 : ℝ≥0∞) (domainMeasure domain)
  pressure_memLp : MemLp pressure ((3 : ℝ≥0∞) / 2) (domainMeasure domain)
  force_memLp : MemLp force (2 : ℝ≥0∞) (domainMeasure domain)
  weak_navierStokes_equation : Prop
  weak_divergenceFree : Prop
  local_energy_inequality : Prop
  parabolic_metric_model : Prop

/-! ## Parabolic geometry task surface -/

/--
Two-sided CKN parabolic cylinder centered at `(x₀,t₀)` with spatial radius
`r` and time radius `r²`.
-/
def twoSidedParabolicCylinder (center : SpaceTime) (radius : ℝ) :
    Set SpaceTime :=
  {z | dist z.1 center.1 < radius ∧ |z.2 - center.2| < radius ^ 2}

/-- Backward CKN parabolic cylinder `(t₀ - r²,t₀) × B(x₀,r)`. -/
def backwardParabolicCylinder (center : SpaceTime) (radius : ℝ) :
    Set SpaceTime :=
  {z | dist z.1 center.1 < radius ∧
    center.2 - radius ^ 2 < z.2 ∧ z.2 < center.2}

/-- Forward CKN parabolic cylinder `(t₀,t₀ + r²) × B(x₀,r)`. -/
def forwardParabolicCylinder (center : SpaceTime) (radius : ℝ) :
    Set SpaceTime :=
  {z | dist z.1 center.1 < radius ∧
    center.2 < z.2 ∧ z.2 < center.2 + radius ^ 2}

/-- A named local CKN parabolic cylinder with positive spatial radius. -/
structure ParabolicCylinder where
  center : SpaceTime
  radius : ℝ
  radius_pos : 0 < radius

/-- The two-sided set associated to a named CKN parabolic cylinder. -/
def ParabolicCylinder.twoSidedSet (Q : ParabolicCylinder) :
    Set SpaceTime :=
  twoSidedParabolicCylinder Q.center Q.radius

/-- The backward set associated to a named CKN parabolic cylinder. -/
def ParabolicCylinder.backwardSet (Q : ParabolicCylinder) :
    Set SpaceTime :=
  backwardParabolicCylinder Q.center Q.radius

/-- The forward set associated to a named CKN parabolic cylinder. -/
def ParabolicCylinder.forwardSet (Q : ParabolicCylinder) :
    Set SpaceTime :=
  forwardParabolicCylinder Q.center Q.radius

/--
Parabolic rescaling about a space-time center: `x ↦ x₀ + λ (x - x₀)` and
`t ↦ t₀ + λ² (t - t₀)`.
-/
def parabolicRescale (center : SpaceTime) (scale : ℝ) (z : SpaceTime) :
    SpaceTime :=
  (center.1 + scale • (z.1 - center.1),
    center.2 + scale ^ 2 * (z.2 - center.2))

/-- Velocity scaling associated with the Navier-Stokes parabolic rescaling. -/
def parabolicRescaledVelocity
    (D : SuitableWeakSolutionData) (center : SpaceTime) (scale : ℝ) :
    SpaceTime → Velocity :=
  fun z => scale • D.velocity (parabolicRescale center scale z)

/-- Pressure scaling associated with the Navier-Stokes parabolic rescaling. -/
def parabolicRescaledPressure
    (D : SuitableWeakSolutionData) (center : SpaceTime) (scale : ℝ) :
    SpaceTime → ℝ :=
  fun z => scale ^ 2 * D.pressure (parabolicRescale center scale z)

/-- Force scaling associated with the forced Navier-Stokes parabolic rescaling. -/
def parabolicRescaledForce
    (D : SuitableWeakSolutionData) (center : SpaceTime) (scale : ℝ) :
    SpaceTime → Velocity :=
  fun z => (scale ^ 3) • D.force (parabolicRescale center scale z)

/--
Formalization target for replacing the abstract parabolic metric field by a
concrete parabolic-cylinder, rescaling, and Hausdorff-measure geometry package.

The concrete cylinder and rescaling functions are defined above.  The remaining
fields are proof obligations because CKN needs scale-compatibility and
parabolic Hausdorff-measure infrastructure that is not present in the audited
mathlib snapshot.
-/
structure ParabolicGeometryAPI (D : SuitableWeakSolutionData) where
  cylinder : ParabolicCylinder
  cylinder_subset_domain : cylinder.backwardSet ⊆ D.domain
  scalingFactor : ℝ
  scalingFactor_pos : 0 < scalingFactor
  rescaledVelocity : SpaceTime → Velocity :=
    parabolicRescaledVelocity D cylinder.center scalingFactor
  rescaledPressure : SpaceTime → ℝ :=
    parabolicRescaledPressure D cylinder.center scalingFactor
  rescaledForce : SpaceTime → Velocity :=
    parabolicRescaledForce D cylinder.center scalingFactor
  rescaling_maps_unit_to_cylinder : Prop
  rescaling_maps_unit_to_cylinder_proof : rescaling_maps_unit_to_cylinder
  rescaled_domain_model : Prop
  rescaled_domain_model_proof : rescaled_domain_model
  scale_invariant_metric_ball_basis : Prop
  scale_invariant_metric_ball_basis_proof : scale_invariant_metric_ball_basis
  parabolic_hausdorff_measure_model : Prop
  parabolic_hausdorff_measure_model_proof : parabolic_hausdorff_measure_model
  geometry_matches_abstract_field :
    parabolic_hausdorff_measure_model → D.parabolic_metric_model

/-- The open-domain object associated to a suitable weak solution package. -/
def solutionOpenDomain (D : SuitableWeakSolutionData) :
    TopologicalSpace.Opens SpaceTime :=
  ⟨D.domain, D.domain_isOpen⟩

/-- Scalar test functions on the open space-time domain of a solution. -/
abbrev ScalarTestFunction (D : SuitableWeakSolutionData) : Type :=
  TestFunction (solutionOpenDomain D) ℝ ⊤

/-- Vector-valued test functions on the open space-time domain of a solution. -/
abbrev VectorTestFunction (D : SuitableWeakSolutionData) : Type :=
  TestFunction (solutionOpenDomain D) Velocity ⊤

/-- Scalar distributions on the open space-time domain of a solution. -/
abbrev ScalarDistribution (D : SuitableWeakSolutionData) : Type :=
  Distribution (solutionOpenDomain D) ℝ ⊤

/-- Vector-valued distributions on the open space-time domain of a solution. -/
abbrev VectorDistribution (D : SuitableWeakSolutionData) : Type :=
  Distribution (solutionOpenDomain D) Velocity ⊤

/--
Formalization target for a concrete distributional incompressible
Navier-Stokes API over the open domain carried by a suitable weak solution.

This is intentionally a contract, not an instance.  Supplying an element of
this structure would require constructing the distributional representatives
and proving that the selected distributional momentum and divergence-free
equations imply the abstract fields currently stored in
`SuitableWeakSolutionData`.
-/
structure DistributionalNavierStokesAPI (D : SuitableWeakSolutionData) where
  velocity_distribution : VectorDistribution D
  pressure_distribution : ScalarDistribution D
  force_distribution : VectorDistribution D
  time_derivative_term : VectorDistribution D
  viscosity_laplacian_term : VectorDistribution D
  convection_term : VectorDistribution D
  pressure_gradient_term : VectorDistribution D
  force_term : VectorDistribution D
  distributional_momentum_equation : Prop
  distributional_momentum_equation_proof : distributional_momentum_equation
  distributional_divergenceFree_equation : Prop
  distributional_divergenceFree_equation_proof :
    distributional_divergenceFree_equation
  representatives_match_memLp_data : Prop
  representatives_match_memLp_data_proof : representatives_match_memLp_data
  momentum_matches_abstract_field :
    distributional_momentum_equation → D.weak_navierStokes_equation
  divergenceFree_matches_abstract_field :
    distributional_divergenceFree_equation → D.weak_divergenceFree
  smooth_representative_classical_bridge : Prop

/-- The PDE-side hypotheses that a terminal CKN proof must discharge. -/
def SuitableWeakSolutionHypotheses (D : SuitableWeakSolutionData) : Prop :=
  D.weak_navierStokes_equation ∧
    D.weak_divergenceFree ∧
      D.local_energy_inequality ∧
        D.parabolic_metric_model

/-- A point is regular when the velocity is smooth at that space-time point. -/
def RegularAt (D : SuitableWeakSolutionData) (z : SpaceTime) : Prop :=
  ContDiffAt ℝ ⊤ D.velocity z

/-- The CKN singular set, restricted to the solution domain. -/
def SingularSet (D : SuitableWeakSolutionData) : Set SpaceTime :=
  {z | z ∈ D.domain ∧ ¬ RegularAt D z}

/-! ## Epsilon-regularity proof-package task surface -/

/-- The `r⁻¹` normalizer used by CKN local energy and dissipation quantities. -/
def cknEnergyNormalizer (radius : ℝ) : ℝ :=
  radius⁻¹

/--
The `r⁻²` normalizer used by CKN space-time cubic-velocity and pressure
quantities.
-/
def cknSpaceTimeNormalizer (radius : ℝ) : ℝ :=
  (radius ^ 2)⁻¹

/-- A named wrapper for multiplying a raw local integral by its CKN normalizer. -/
def cknScaleInvariantValue (normalizer rawQuantity : ℝ) : ℝ :=
  normalizer * rawQuantity

/--
Scale-invariant quantity package for the epsilon-regularity branch.

The raw local quantities are kept as real-valued slots because this repository
does not yet have a concrete distributional-gradient/local-energy API for
Navier-Stokes.  The checked fields record the CKN normalizing factors and the
remaining proof obligations that a future analytic development must discharge
before these values can be used as terminal estimates.
-/
structure CKNScaleInvariantQuantities (D : SuitableWeakSolutionData) where
  cylinder : ParabolicCylinder
  cylinder_subset_domain : cylinder.backwardSet ⊆ D.domain
  localKineticEnergy : ℝ
  localDissipation : ℝ
  localVelocityCubic : ℝ
  localPressureThreeHalves : ℝ
  localForceContribution : ℝ
  kineticEnergyQuantity : ℝ :=
    cknScaleInvariantValue (cknEnergyNormalizer cylinder.radius)
      localKineticEnergy
  dissipationQuantity : ℝ :=
    cknScaleInvariantValue (cknEnergyNormalizer cylinder.radius)
      localDissipation
  velocityCubicQuantity : ℝ :=
    cknScaleInvariantValue (cknSpaceTimeNormalizer cylinder.radius)
      localVelocityCubic
  pressureThreeHalvesQuantity : ℝ :=
    cknScaleInvariantValue (cknSpaceTimeNormalizer cylinder.radius)
      localPressureThreeHalves
  forceQuantity : ℝ
  quantities_nonnegative : Prop
  quantities_nonnegative_proof : quantities_nonnegative
  quantities_match_solution_fields : Prop
  quantities_match_solution_fields_proof : quantities_match_solution_fields

/-- The combined CKN epsilon-smallness quantity tracked by this Stage1 package. -/
def CKNScaleInvariantQuantities.totalRegularityQuantity
    {D : SuitableWeakSolutionData} (Q : CKNScaleInvariantQuantities D) : ℝ :=
  Q.velocityCubicQuantity + Q.pressureThreeHalvesQuantity + Q.forceQuantity

/-- Epsilon-smallness of the checked CKN scale-invariant quantity package. -/
def CKNScaleInvariantQuantities.smallAt
    {D : SuitableWeakSolutionData} (Q : CKNScaleInvariantQuantities D)
    (epsilon : ℝ) : Prop :=
  Q.totalRegularityQuantity < epsilon

/--
Compactness/decay package required by the CKN epsilon-regularity proof.

This is a checked proof-task contract: it records the blow-up compactness,
decay estimate, and scale-iteration obligations without claiming those
analytic estimates are already formalized in this repository.
-/
structure CKNCompactnessDecayPackage (D : SuitableWeakSolutionData) where
  quantities : CKNScaleInvariantQuantities D
  smallerRadius : ℝ
  smallerRadius_pos : 0 < smallerRadius
  smallerRadius_lt_radius : smallerRadius < quantities.cylinder.radius
  blowup_compactness : Prop
  blowup_compactness_proof : blowup_compactness
  decay_estimate : Prop
  decay_estimate_proof : decay_estimate
  scale_iteration : Prop
  scale_iteration_proof : scale_iteration

/--
Proof-package boundary for the CKN epsilon-regularity criterion.

A completed instance would connect checked scale-invariant quantities and the
compactness/decay branch to pointwise smoothness of the velocity at the center
of the parabolic cylinder.
-/
structure CKNEpsilonRegularityPackage (D : SuitableWeakSolutionData) where
  quantities : CKNScaleInvariantQuantities D
  epsilon0 : ℝ
  epsilon0_pos : 0 < epsilon0
  center_mem_domain : quantities.cylinder.center ∈ D.domain
  compactnessDecay : CKNCompactnessDecayPackage D
  compactnessDecay_matches_quantities : compactnessDecay.quantities = quantities
  epsilon_smallness : quantities.smallAt epsilon0
  epsilon_regularity_statement : Prop
  epsilon_regularity_statement_proof : epsilon_regularity_statement
  criterion_matches_regularAt :
    epsilon_regularity_statement → RegularAt D quantities.cylinder.center

/--
Bridge task from local epsilon regularity packages to regularity outside the
CKN singular set.
-/
structure CKNRegularityOutsideSingularBridge (D : SuitableWeakSolutionData) where
  local_epsilon_package_available : Prop
  local_epsilon_package_available_proof : local_epsilon_package_available
  nonsingular_points_have_small_quantities : Prop
  nonsingular_points_have_small_quantities_proof :
    nonsingular_points_have_small_quantities
  regularity_outside_singular :
    local_epsilon_package_available →
      nonsingular_points_have_small_quantities →
        ∀ z ∈ D.domain, z ∉ SingularSet D → RegularAt D z

/--
Euclidean Hausdorff-measure surrogate for the singular-set smallness
conclusion. CKN uses parabolic one-dimensional Hausdorff measure; the local
mathlib anchor here records the available Hausdorff-measure API without
claiming that it is the terminal parabolic statement.
-/
def EuclideanHausdorffSingularSetZero (D : SuitableWeakSolutionData) : Prop :=
  Measure.hausdorffMeasure (1 : ℝ) (SingularSet D) = 0

/--
Terminal package shape for the Caffarelli-Kohn-Nirenberg conclusion.

The parabolic measure statement is abstract, while the regular set and a
Euclidean Hausdorff-measure surrogate are expressed with concrete mathlib
objects. A future formalization should replace the abstract parabolic fields by
a pinned parabolic metric/Hausdorff-measure construction and prove all fields
from `SuitableWeakSolutionHypotheses`.
-/
structure CaffarelliKohnNirenbergPackage (D : SuitableWeakSolutionData) where
  epsilon_regularity_criterion : Prop
  epsilon_regularity_criterion_proof : epsilon_regularity_criterion
  parabolic_singular_set_measure_zero : Prop
  parabolic_singular_set_measure_zero_proof : parabolic_singular_set_measure_zero
  euclidean_hausdorff_surrogate : EuclideanHausdorffSingularSetZero D
  regular_outside_singular :
    ∀ z ∈ D.domain, z ∉ SingularSet D → RegularAt D z

/--
Normalized Stage1 statement shape for CKN partial regularity.

Every suitable weak solution of the three-dimensional Navier-Stokes equations
has a CKN regularity package: smoothness away from the singular set, the
epsilon-regularity branch, and the smallness of the singular set in the
parabolic Hausdorff sense once the missing parabolic infrastructure is supplied.
-/
def StatementShape : Prop :=
  ∀ D : SuitableWeakSolutionData,
    SuitableWeakSolutionHypotheses D →
      Nonempty (CaffarelliKohnNirenbergPackage D)

/-- The statement shape unfolds to the expected implication over all data packages. -/
theorem statementShape_iff :
    StatementShape ↔
      ∀ D : SuitableWeakSolutionData,
        SuitableWeakSolutionHypotheses D →
          Nonempty (CaffarelliKohnNirenbergPackage D) :=
  Iff.rfl

/-- Apply the normalized statement shape to one suitable weak solution package. -/
theorem StatementShape.apply
    (h : StatementShape) (D : SuitableWeakSolutionData)
    (hD : SuitableWeakSolutionHypotheses D) :
    Nonempty (CaffarelliKohnNirenbergPackage D) :=
  h D hD

/-- Membership in the singular set is exactly domain membership plus non-regularity. -/
theorem mem_singularSet_iff (D : SuitableWeakSolutionData) (z : SpaceTime) :
    z ∈ SingularSet D ↔ z ∈ D.domain ∧ ¬ RegularAt D z :=
  Iff.rfl

/-- The singular set is contained in the solution domain by construction. -/
theorem singularSet_subset_domain (D : SuitableWeakSolutionData) :
    SingularSet D ⊆ D.domain := by
  intro z hz
  exact hz.1

/-- A domain point outside the singular set is regular by the chosen definition. -/
theorem regularAt_of_mem_domain_not_mem_singular
    (D : SuitableWeakSolutionData) {z : SpaceTime}
    (hzD : z ∈ D.domain) (hz : z ∉ SingularSet D) :
    RegularAt D z := by
  by_contra hreg
  exact hz ⟨hzD, hreg⟩

/-- The stored velocity energy hypothesis is a concrete `MemLp` fact. -/
theorem velocity_memLp_two (D : SuitableWeakSolutionData) :
    MemLp D.velocity (2 : ℝ≥0∞) (domainMeasure D.domain) :=
  D.velocity_energy_memLp

/-- The stored cubic velocity hypothesis is a concrete `MemLp` fact. -/
theorem velocity_memLp_three (D : SuitableWeakSolutionData) :
    MemLp D.velocity (3 : ℝ≥0∞) (domainMeasure D.domain) :=
  D.velocity_cubic_memLp

/-- The stored pressure integrability hypothesis is a concrete `MemLp` fact. -/
theorem pressure_memLp_three_halves (D : SuitableWeakSolutionData) :
    MemLp D.pressure ((3 : ℝ≥0∞) / 2) (domainMeasure D.domain) :=
  D.pressure_memLp

/-- A CKN package exposes regularity outside the singular set. -/
theorem CaffarelliKohnNirenbergPackage.regularAt_of_not_mem_singular
    {D : SuitableWeakSolutionData}
    (pkg : CaffarelliKohnNirenbergPackage D) {z : SpaceTime}
    (hzD : z ∈ D.domain) (hz : z ∉ SingularSet D) :
    RegularAt D z :=
  pkg.regular_outside_singular z hzD hz

/-- The PDE-side hypotheses project to the weak Navier-Stokes equation field. -/
theorem SuitableWeakSolutionHypotheses.weak_navierStokes_equation
    {D : SuitableWeakSolutionData}
    (h : SuitableWeakSolutionHypotheses D) :
    D.weak_navierStokes_equation :=
  h.1

/-- The PDE-side hypotheses project to the weak divergence-free field. -/
theorem SuitableWeakSolutionHypotheses.weak_divergenceFree
    {D : SuitableWeakSolutionData}
    (h : SuitableWeakSolutionHypotheses D) :
    D.weak_divergenceFree :=
  h.2.1

/-- The PDE-side hypotheses project to the local energy inequality field. -/
theorem SuitableWeakSolutionHypotheses.local_energy_inequality
    {D : SuitableWeakSolutionData}
    (h : SuitableWeakSolutionHypotheses D) :
    D.local_energy_inequality :=
  h.2.2.1

/-- The PDE-side hypotheses project to the parabolic metric model field. -/
theorem SuitableWeakSolutionHypotheses.parabolic_metric_model
    {D : SuitableWeakSolutionData}
    (h : SuitableWeakSolutionHypotheses D) :
    D.parabolic_metric_model :=
  h.2.2.2

/--
A completed concrete distributional API would discharge the abstract weak
Navier-Stokes field used by the Stage1 suitable-weak-solution package.
-/
theorem DistributionalNavierStokesAPI.weak_navierStokes_equation
    {D : SuitableWeakSolutionData}
    (api : DistributionalNavierStokesAPI D) :
    D.weak_navierStokes_equation :=
  api.momentum_matches_abstract_field api.distributional_momentum_equation_proof

/--
A completed concrete distributional API would discharge the abstract
divergence-free field used by the Stage1 suitable-weak-solution package.
-/
theorem DistributionalNavierStokesAPI.weak_divergenceFree
    {D : SuitableWeakSolutionData}
    (api : DistributionalNavierStokesAPI D) :
    D.weak_divergenceFree :=
  api.divergenceFree_matches_abstract_field
    api.distributional_divergenceFree_equation_proof

/-- Projection for the representative compatibility obligation in the API task. -/
theorem DistributionalNavierStokesAPI.representatives_match_memLp_data_holds
    {D : SuitableWeakSolutionData}
    (api : DistributionalNavierStokesAPI D) :
    api.representatives_match_memLp_data :=
  api.representatives_match_memLp_data_proof

/-- Membership in a two-sided CKN parabolic cylinder unfolds to spatial/time bounds. -/
theorem mem_twoSidedParabolicCylinder_iff
    {center z : SpaceTime} {radius : ℝ} :
    z ∈ twoSidedParabolicCylinder center radius ↔
      dist z.1 center.1 < radius ∧ |z.2 - center.2| < radius ^ 2 :=
  Iff.rfl

/-- Membership in a backward CKN parabolic cylinder unfolds to spatial/time bounds. -/
theorem mem_backwardParabolicCylinder_iff
    {center z : SpaceTime} {radius : ℝ} :
    z ∈ backwardParabolicCylinder center radius ↔
      dist z.1 center.1 < radius ∧
        center.2 - radius ^ 2 < z.2 ∧ z.2 < center.2 :=
  Iff.rfl

/-- Membership in a forward CKN parabolic cylinder unfolds to spatial/time bounds. -/
theorem mem_forwardParabolicCylinder_iff
    {center z : SpaceTime} {radius : ℝ} :
    z ∈ forwardParabolicCylinder center radius ↔
      dist z.1 center.1 < radius ∧
        center.2 < z.2 ∧ z.2 < center.2 + radius ^ 2 :=
  Iff.rfl

/-- A parabolic-geometry package exposes its cylinder-domain inclusion. -/
theorem ParabolicGeometryAPI.backwardSet_subset_domain
    {D : SuitableWeakSolutionData}
    (api : ParabolicGeometryAPI D) :
    api.cylinder.backwardSet ⊆ D.domain :=
  api.cylinder_subset_domain

/--
A completed parabolic Hausdorff-measure model would discharge the abstract
parabolic metric field used by the Stage1 suitable-weak-solution package.
-/
theorem ParabolicGeometryAPI.parabolic_metric_model
    {D : SuitableWeakSolutionData}
    (api : ParabolicGeometryAPI D) :
    D.parabolic_metric_model :=
  api.geometry_matches_abstract_field api.parabolic_hausdorff_measure_model_proof

/-- The checked CKN value wrapper is definitionally multiplication by a normalizer. -/
theorem cknScaleInvariantValue_eq_mul
    (normalizer rawQuantity : ℝ) :
    cknScaleInvariantValue normalizer rawQuantity =
      normalizer * rawQuantity :=
  rfl

/-- Epsilon-smallness unfolds to a bound on the combined regularity quantity. -/
theorem CKNScaleInvariantQuantities.smallAt_iff
    {D : SuitableWeakSolutionData} (Q : CKNScaleInvariantQuantities D)
    (epsilon : ℝ) :
    Q.smallAt epsilon ↔ Q.totalRegularityQuantity < epsilon :=
  Iff.rfl

/-- A scale-invariant quantity package exposes its cylinder-domain inclusion. -/
theorem CKNScaleInvariantQuantities.backwardSet_subset_domain
    {D : SuitableWeakSolutionData}
    (Q : CKNScaleInvariantQuantities D) :
    Q.cylinder.backwardSet ⊆ D.domain :=
  Q.cylinder_subset_domain

/-- Projection for the nonnegativity obligation in the scale-invariant package. -/
theorem CKNScaleInvariantQuantities.quantities_nonnegative_holds
    {D : SuitableWeakSolutionData}
    (Q : CKNScaleInvariantQuantities D) :
    Q.quantities_nonnegative :=
  Q.quantities_nonnegative_proof

/--
A completed epsilon-regularity package yields regularity at the center of its
CKN parabolic cylinder.
-/
theorem CKNEpsilonRegularityPackage.regularAt_center
    {D : SuitableWeakSolutionData}
    (pkg : CKNEpsilonRegularityPackage D) :
    RegularAt D pkg.quantities.cylinder.center :=
  pkg.criterion_matches_regularAt pkg.epsilon_regularity_statement_proof

/--
A completed outside-singular bridge yields the regularity conclusion expected
by the terminal CKN package.
-/
theorem CKNRegularityOutsideSingularBridge.regularAt_of_not_mem_singular
    {D : SuitableWeakSolutionData}
    (bridge : CKNRegularityOutsideSingularBridge D)
    {z : SpaceTime} (hzD : z ∈ D.domain) (hz : z ∉ SingularSet D) :
    RegularAt D z :=
  bridge.regularity_outside_singular
    bridge.local_epsilon_package_available_proof
    bridge.nonsingular_points_have_small_quantities_proof
    z hzD hz

/-- C005 child-task status for the distributional Navier-Stokes API surface. -/
def distributionalNavierStokesAPIStatus : String :=
  "formalization_task_added_checked_distribution_and_test_function_types_not_terminal_proof"

/--
M0387-level local leaves for replacing the abstract weak Navier-Stokes fields
by a concrete distributional equation package.
-/
def distributionalNavierStokesAPILeaves : List String := [
  "M1228-C005-L001 checked: define open-domain test-function and distribution types for scalar and vector fields",
  "M1228-C005-L002 checked: add a DistributionalNavierStokesAPI contract exposing velocity, pressure, force, and residual-term distributions",
  "M1228-C005-L003 checked: project a completed distributional momentum equation to the abstract weak Navier-Stokes field",
  "M1228-C005-L004 checked: project a completed distributional divergence-free equation to the abstract weak divergence-free field",
  "M1228-C005-L005 unchecked: construct distributions from the current MemLp velocity, pressure, and force representatives",
  "M1228-C005-L006 unchecked: define the actual ∂_t u - Δu + div(u ⊗ u) + ∇p = f residual with mathlib distributional derivatives",
  "M1228-C005-L007 unchecked: prove equivalence between the concrete distributional residual and the suitable-weak-solution PDE fields",
  "M1228-C005-L008 unchecked: prove the smooth-representative bridge from the distributional residual to the classical Navier-Stokes equation"
]

/-- C006 child-task status for the parabolic-geometry formalization surface. -/
def parabolicGeometryAPIStatus : String :=
  "formalization_task_added_checked_cylinders_and_scaling_not_terminal_proof"

/--
M0387-level local leaves for replacing the abstract parabolic metric field by
concrete CKN parabolic cylinders, rescaling, and parabolic Hausdorff measure.
-/
def parabolicGeometryAPILeaves : List String := [
  "M1228-C006-L001 checked: define two-sided, backward, and forward CKN parabolic cylinders in space-time",
  "M1228-C006-L002 checked: define a positive-radius ParabolicCylinder package and its set projections",
  "M1228-C006-L003 checked: define centered Navier-Stokes parabolic rescaling for space-time points",
  "M1228-C006-L004 checked: define velocity, pressure, and force scaling under the parabolic rescaling",
  "M1228-C006-L005 checked: add a ParabolicGeometryAPI contract bridging concrete parabolic Hausdorff geometry to the abstract parabolic metric field",
  "M1228-C006-L006 checked: prove membership-unfolding wrappers for the concrete cylinder definitions",
  "M1228-C006-L007 unchecked: prove positive-scale maps from unit cylinders to named CKN cylinders",
  "M1228-C006-L008 unchecked: prove the scaling laws for local energy and epsilon-regularity quantities",
  "M1228-C006-L009 unchecked: construct the parabolic Hausdorff measure model and compare it to the Euclidean surrogate",
  "M1228-C006-L010 unchecked: prove that the concrete parabolic geometry discharges D.parabolic_metric_model"
]

/-- C007 child-task status for the epsilon-regularity proof-package surface. -/
def epsilonRegularityAPIStatus : String :=
  "proof_package_task_added_checked_scale_invariant_quantities_not_terminal_proof"

/--
M0387-level local leaves for the CKN epsilon-regularity proof package:
scale-invariant quantities, compactness/decay, and regularity outside the
singular set.
-/
def epsilonRegularityAPILeaves : List String := [
  "M1228-C007-L001 checked: define CKN normalizers for local energy/dissipation and space-time cubic/pressure quantities",
  "M1228-C007-L002 checked: add a CKNScaleInvariantQuantities package over a named backward parabolic cylinder",
  "M1228-C007-L003 checked: define totalRegularityQuantity and epsilon-smallness for the CKN quantity package",
  "M1228-C007-L004 checked: add a CKNCompactnessDecayPackage contract for blow-up compactness, decay estimates, and scale iteration",
  "M1228-C007-L005 checked: add a CKNEpsilonRegularityPackage contract bridging smallness to RegularAt at the cylinder center",
  "M1228-C007-L006 checked: add a CKNRegularityOutsideSingularBridge contract for deriving regularity outside SingularSet",
  "M1228-C007-L007 unchecked: construct raw kinetic-energy, dissipation, velocity-cubic, pressure, and force quantities from concrete integrals",
  "M1228-C007-L008 unchecked: prove Navier-Stokes scaling laws for all CKN scale-invariant quantities",
  "M1228-C007-L009 unchecked: prove the compactness/decay estimate package from the local energy inequality",
  "M1228-C007-L010 unchecked: prove the epsilon-regularity criterion and regularity outside the singular set"
]

/-- Exact mathlib revision pinned by the local Lake manifest for this audit. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.MeasureTheory.Function.LpSeminorm.Basic",
  "Mathlib.MeasureTheory.Measure.Hausdorff",
  "Mathlib.Topology.MetricSpace.HausdorffDimension",
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.TestFunction",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.Analysis.Calculus.ContDiff.Basic",
  "Mathlib.Analysis.InnerProductSpace.Laplacian"
]

/-- Checked local names used as anchors for the statement-shape boundary. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.MemLp",
  "MeasureTheory.Measure.restrict",
  "MeasureTheory.Measure.hausdorffMeasure",
  "MeasureTheory.Distribution",
  "TestFunction",
  "ContDiffAt",
  "ContDiff",
  "MeasureTheory.eLpNorm",
  "MeasureTheory.Lp",
  "MeasureTheory.volume"
]

/--
Search terms that did not locate a terminal CKN partial regularity theorem in
pinned mathlib.
-/
def absentTerminalSearchTerms : List String := [
  "Caffarelli",
  "Kohn",
  "Nirenberg",
  "Caffarelli-Kohn-Nirenberg",
  "NavierStokes",
  "Navier-Stokes",
  "suitable weak solution",
  "local energy inequality",
  "partial regularity",
  "parabolic Hausdorff measure",
  "epsilon regularity"
]

/-- Checked metadata row for the C004 no-terminal-mathlib-anchor child audit. -/
structure TerminalMathlibAnchorAudit where
  auditScope : String
  searchedTerms : List String
  foundTerminalAnchor : Bool
  status : String
  debtClassification : String

/--
C004 terminal-anchor result: pinned mathlib exposes adjacent analysis
infrastructure, but this pass found no terminal CKN partial-regularity theorem.
-/
def terminalMathlibAnchorAudit : TerminalMathlibAnchorAudit where
  auditScope := "pinned mathlib declaration/source search for CKN terminal theorem"
  searchedTerms := absentTerminalSearchTerms
  foundTerminalAnchor := false
  status := "no_terminal_mathlib_theorem_found"
  debtClassification := "formalization_debt_not_repo_local_closed"

/-- The C004 audit is explicitly negative for a terminal pinned-mathlib anchor. -/
theorem terminalMathlibAnchorAudit_foundTerminalAnchor_eq :
    terminalMathlibAnchorAudit.foundTerminalAnchor = false :=
  rfl

/-! ## Child C008 external primary-source Lean 4 audit metadata -/

/--
Primary-source repository record for child task `S1-M-156-C008`.

The `acceptedAsTerminalCKNProof` flag is deliberately strict: statement
scaffolding, unrelated Navier-Stokes regularity claims, theorem bodies
depending on project postulates, unfinished proof placeholders, or placeholder
`True` definitions do not count as an external Caffarelli-Kohn-Nirenberg
partial-regularity proof.
-/
structure C008ExternalLeanAuditRecord where
  repository : String
  revision : String
  leanToolchain : String
  sourcePath : String
  declarationsOrHits : List String
  diagnosis : String
  acceptedAsTerminalCKNProof : Bool
deriving Repr, DecidableEq

/-- Search terms requested by the C008 external-audit child task. -/
def c008RequestedSearchTerms : List String := [
  "Caffarelli",
  "Kohn",
  "Nirenberg",
  "Caffarelli-Kohn-Nirenberg",
  "CKN",
  "NavierStokes",
  "Navier-Stokes",
  "suitable weak solution",
  "local energy inequality",
  "partial regularity",
  "parabolic Hausdorff measure",
  "epsilon regularity"
]

/--
External primary-source records inspected by C008.

GitHub CLI authentication was unavailable in this worker, so these rows combine
the available unauthenticated GitHub repository search, direct `git ls-remote`
revision checks, and cloned primary-source inspection. They are not imported
dependencies and they do not close the CKN theorem.
-/
def c008ExternalLeanAuditRecords : List C008ExternalLeanAuditRecord := [
  {
    repository := "https://github.com/lean-dojo/LeanMillenniumPrizeProblems",
    revision := "540da94826f70f3edf4d4fc66ce6cda20e903f61",
    leanToolchain := "leanprover/lean4:v4.26.0",
    sourcePath :=
      "Problems/NavierStokes/Navierstokes.lean; " ++
      "Problems/NavierStokes/Millennium.lean",
    declarationsOrHits := [
      "NavierStokes.NavierStokesEquations",
      "NavierStokes.Solution",
      "MillenniumNavierStokes.NavierStokesMillenniumProblem"
    ],
    diagnosis :=
      "Navier-Stokes equation and Clay Millennium statement scaffolding; no " ++
      "Caffarelli-Kohn-Nirenberg, suitable-weak-solution, local-energy, " ++
      "epsilon-regularity, or parabolic-Hausdorff terminal theorem found.",
    acceptedAsTerminalCKNProof := false
  },
  {
    repository := "https://github.com/motanova84/3D-Navier-Stokes",
    revision := "7fbbcb26c1557ef2f048f7e21a40caf1107e5995",
    leanToolchain := "leanprover/lean4:v4.25.0-rc2",
    sourcePath :=
      "Lean4-Formalization/SerrinEndpoint.lean; " ++
      "formal_verification/lean4/PsiNSE/SerrinEndpoint.lean; " ++
      "PsiNSE/Foundation/Complete.lean",
    declarationsOrHits := [
      "NavierStokes.serrin_criterion",
      "NavierStokes.serrin_endpoint",
      "NavierStokes.global_regularity_via_serrin",
      "CInfinity is defined as True in one route",
      "formal_verification/lean4/PsiNSE/SerrinEndpoint.lean contains proof gaps"
    ],
    diagnosis :=
      "Navier-Stokes/Serrin-adjacent project, not a CKN partial-regularity " ++
      "formalization; inspected files include placeholder True definitions, " ++
      "unfinished proof routes, and non-CKN proof targets.",
    acceptedAsTerminalCKNProof := false
  },
  {
    repository := "https://github.com/Bitumenmachina/ns-lean4-pipeline",
    revision := "4cfc7bfd6aaf2c7e5ad28c6234864ef859346e87",
    leanToolchain := "leanprover/lean4:v4.29.0",
    sourcePath :=
      "lean/NSLean4/NSTheorems.lean; lean/NSLean4/NSCerts.lean",
    declarationsOrHits := [
      "NS.viscosity_bootstrap_failure",
      "NS.Certs.K_Re6400_t40_gt_one",
      "NS.Certs.conv_ratio_256_128_lt_13"
    ],
    diagnosis :=
      "Conditional direction-field/DNS certificate pipeline; mentions a " ++
      "Gagliardo-Nirenberg-type estimate but not the Caffarelli-Kohn-" ++
      "Nirenberg theorem. The certificate layer uses generated axioms, so it " ++
      "is not an importable terminal CKN proof.",
    acceptedAsTerminalCKNProof := false
  },
  {
    repository := "https://github.com/MohamedMoawadHassan/GIGD-Formalization",
    revision := "1d04458c60e40ca2cf5a58129a5e77c080e616f1",
    leanToolchain := "leanprover/lean4:v4.28.0",
    sourcePath := "GIGDProject.lean",
    declarationsOrHits := [
      "GIGD_critical_inequality",
      "GIGD_enstrophy_bound",
      "incompressibility_L2 project postulate",
      "standard_gronwall project postulate"
    ],
    diagnosis :=
      "Vortex-stretching/GIGD inequality formalization, not CKN partial " ++
      "regularity for suitable weak solutions; it depends on project postulates " ++
      "and cannot be used as terminal evidence.",
    acceptedAsTerminalCKNProof := false
  }
]

/-- GitHub CLI authentication was unavailable for C008. -/
def c008GitHubCliAuthenticated : Bool :=
  false

/--
Unauthenticated GitHub repository-search observation for the exact CKN query.

The query `Lean Caffarelli Kohn Nirenberg` returned zero repositories through
the unauthenticated REST repository-search surface in this worker.
-/
def c008UnauthenticatedExactRepositoryHits : Nat :=
  0

/--
Unauthenticated GitHub code search could not be completed after the REST API
reported a rate-limit error for this worker IP.
-/
def c008UnauthenticatedCodeSearchRateLimited : Bool :=
  true

/--
No accepted external Lean 4 terminal CKN proof was found by C008.

This is not a global nonexistence claim; it records the local pinned mathlib
search, unavailable authenticated GitHub CLI channel, unauthenticated search
observations, and the cloned primary-source repositories inspected here.
-/
def c008AcceptedExternalTerminalCKNProofFound : Bool :=
  false

/--
C008 does not create a dependency-integration task because no acceptable
external terminal proof was found. If authenticated search later locates one,
M0387 requires pin/import/check or a concrete integration blocker before any
completion claim.
-/
def c008DependencyIntegrationTaskRequiredNow : Bool :=
  false

/-- Remaining C008 audit leaves after this worker pass. -/
def c008RemainingAuditLeaves : List String := [
  "M1228-C008-L001: rerun GitHub code search with an authenticated token for the requested CKN/Navier-Stokes terms",
  "M1228-C008-L002: if a real external Lean 4 CKN proof is found, create a serialized pin/import/check task or record a concrete integration blocker",
  "M1228-C008-L003: keep THM-M-1228 open because current evidence is formalization_debt_not_repo_local_closed, not repo-local completion"
]

/-- Checked search-term count for C008. -/
theorem c008RequestedSearchTerms_length :
    c008RequestedSearchTerms.length = 12 :=
  rfl

/-- Checked primary-source record count for C008. -/
theorem c008ExternalLeanAuditRecords_length :
    c008ExternalLeanAuditRecords.length = 4 :=
  rfl

/-- Checked non-authentication gate for the GitHub CLI code-search channel. -/
theorem c008GitHubCliAuthenticated_eq_false :
    c008GitHubCliAuthenticated = false :=
  rfl

/-- Checked unauthenticated exact-repository-search observation. -/
theorem c008UnauthenticatedExactRepositoryHits_eq_zero :
    c008UnauthenticatedExactRepositoryHits = 0 :=
  rfl

/-- Checked rate-limit observation for unauthenticated code search. -/
theorem c008UnauthenticatedCodeSearchRateLimited_eq_true :
    c008UnauthenticatedCodeSearchRateLimited = true :=
  rfl

/-- Checked negative terminal-proof discovery result for C008. -/
theorem c008AcceptedExternalTerminalCKNProofFound_eq_false :
    c008AcceptedExternalTerminalCKNProofFound = false :=
  rfl

/-- Checked integration-task gate for C008. -/
theorem c008DependencyIntegrationTaskRequiredNow_eq_false :
    c008DependencyIntegrationTaskRequiredNow = false :=
  rfl

/-! ## Child C009 integration-gate metadata -/

/--
Repo-local integration gate for child task `S1-M-156-C009`.

This record is intentionally stricter than the statement-shape scaffold: the
Stage1 item may close only after a terminal theorem is present in the local
Lean validation closure, or after an external terminal proof has been pinned,
imported, and checked locally. Anchor-only evidence is recorded as incomplete.
-/
structure C009IntegrationGate where
  terminalRepoLocalTheoremName : Option String
  validationCommand : String
  repoLocalTerminalTheoremValidated : Bool
  acceptedExternalTerminalProofFound : Bool
  externalProofIntegratedLocally : Bool
  anchorOnlyEvidenceCountedCompleted : Bool
  stage1ItemMayClose : Bool
  debtClassification : String
  diagnosis : String
  remainingLeaves : List String
deriving Repr, DecidableEq

/--
C009 result for the current repository state: keep the parent Stage1 item open.

The checked statement-shape artifact compiles, and C008 did not accept any
external terminal Lean 4 CKN proof. Therefore the integration gate is closed
against completion rather than against future formalization work.
-/
def c009IntegrationGate : C009IntegrationGate where
  terminalRepoLocalTheoremName := none
  validationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_156.lean"
  repoLocalTerminalTheoremValidated := false
  acceptedExternalTerminalProofFound := c008AcceptedExternalTerminalCKNProofFound
  externalProofIntegratedLocally := false
  anchorOnlyEvidenceCountedCompleted := false
  stage1ItemMayClose := false
  debtClassification := "formalization_debt_not_repo_local_closed"
  diagnosis :=
    "statement_shape_checked_but_no_terminal_caffarelli_kohn_nirenberg_theorem"
  remainingLeaves := [
    "M1228-C009-L001: produce a terminal Lean theorem proving StatementShape or an equivalent CKN partial-regularity theorem from concrete suitable-weak-solution APIs",
    "M1228-C009-L002: if a genuine external Lean 4 terminal proof is found, pin/import/check it locally or record a concrete integration blocker",
    "M1228-C009-L003: keep the public Stage1 checklist open until the terminal theorem or integrated external proof passes local validation",
    "M1228-C009-L004: forbid anchor-only repository notes from being counted as completion"
  ]

/-- C009 has no terminal repo-local theorem name in this pass. -/
theorem c009IntegrationGate_terminalRepoLocalTheoremName_eq_none :
    c009IntegrationGate.terminalRepoLocalTheoremName = none :=
  rfl

/-- C009 records that no terminal repo-local theorem has been validated. -/
theorem c009IntegrationGate_repoLocalTerminalTheoremValidated_eq_false :
    c009IntegrationGate.repoLocalTerminalTheoremValidated = false :=
  rfl

/-- C009 records that no external terminal proof has been accepted by C008. -/
theorem c009IntegrationGate_acceptedExternalTerminalProofFound_eq_false :
    c009IntegrationGate.acceptedExternalTerminalProofFound = false :=
  rfl

/-- C009 records that no external proof has entered the local validation closure. -/
theorem c009IntegrationGate_externalProofIntegratedLocally_eq_false :
    c009IntegrationGate.externalProofIntegratedLocally = false :=
  rfl

/-- C009 explicitly does not count anchor-only evidence as completion. -/
theorem c009IntegrationGate_anchorOnlyEvidenceCountedCompleted_eq_false :
    c009IntegrationGate.anchorOnlyEvidenceCountedCompleted = false :=
  rfl

/-- C009 keeps the Stage1 item open in the current repo-local state. -/
theorem c009IntegrationGate_stage1ItemMayClose_eq_false :
    c009IntegrationGate.stage1ItemMayClose = false :=
  rfl

/-- C009 exposes four remaining M0387-level integration leaves. -/
theorem c009IntegrationGate_remainingLeaves_length :
    c009IntegrationGate.remainingLeaves.length = 4 :=
  rfl

/-! ## Repo-local validation status -/

/-- Validation command used for this Stage1 statement-shape artifact. -/
def localValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_156.lean"

/-- Machine status recorded by the validation child: checked statement shape, not terminal CKN. -/
def localValidationMachineStatus : String :=
  "statement_shape_local_checked_not_terminal_caffarelli_kohn_nirenberg"

/--
Repo-local integration-debt gate for this validation pass.

No external Lean proof is being counted as completed here. If a terminal CKN
formalization is later found outside this repository, it must be pinned,
imported, and checked locally, or else recorded as a concrete integration
blocker.
-/
def repoLocalIntegrationDebtGateStatus : String :=
  "passed_no_anchor_only_external_evidence_marked_completed"

/-! ## Audit probes -/

#check SpaceTime
#check Velocity
#check domainMeasure
#check SuitableWeakSolutionData
#check twoSidedParabolicCylinder
#check backwardParabolicCylinder
#check forwardParabolicCylinder
#check ParabolicCylinder
#check ParabolicCylinder.twoSidedSet
#check ParabolicCylinder.backwardSet
#check ParabolicCylinder.forwardSet
#check parabolicRescale
#check parabolicRescaledVelocity
#check parabolicRescaledPressure
#check parabolicRescaledForce
#check ParabolicGeometryAPI
#check cknEnergyNormalizer
#check cknSpaceTimeNormalizer
#check cknScaleInvariantValue
#check CKNScaleInvariantQuantities
#check CKNScaleInvariantQuantities.totalRegularityQuantity
#check CKNScaleInvariantQuantities.smallAt
#check CKNCompactnessDecayPackage
#check CKNEpsilonRegularityPackage
#check CKNRegularityOutsideSingularBridge
#check solutionOpenDomain
#check ScalarTestFunction
#check VectorTestFunction
#check ScalarDistribution
#check VectorDistribution
#check DistributionalNavierStokesAPI
#check SuitableWeakSolutionHypotheses
#check RegularAt
#check SingularSet
#check EuclideanHausdorffSingularSetZero
#check CaffarelliKohnNirenbergPackage
#check StatementShape
#check mathlibPinnedRevision
#check absentTerminalSearchTerms
#check terminalMathlibAnchorAudit
#check terminalMathlibAnchorAudit_foundTerminalAnchor_eq
#check C008ExternalLeanAuditRecord
#check c008RequestedSearchTerms
#check c008RequestedSearchTerms_length
#check c008ExternalLeanAuditRecords
#check c008ExternalLeanAuditRecords_length
#check c008GitHubCliAuthenticated_eq_false
#check c008UnauthenticatedExactRepositoryHits_eq_zero
#check c008UnauthenticatedCodeSearchRateLimited_eq_true
#check c008AcceptedExternalTerminalCKNProofFound_eq_false
#check c008DependencyIntegrationTaskRequiredNow_eq_false
#check c008RemainingAuditLeaves
#check C009IntegrationGate
#check c009IntegrationGate
#check c009IntegrationGate_terminalRepoLocalTheoremName_eq_none
#check c009IntegrationGate_repoLocalTerminalTheoremValidated_eq_false
#check c009IntegrationGate_acceptedExternalTerminalProofFound_eq_false
#check c009IntegrationGate_externalProofIntegratedLocally_eq_false
#check c009IntegrationGate_anchorOnlyEvidenceCountedCompleted_eq_false
#check c009IntegrationGate_stage1ItemMayClose_eq_false
#check c009IntegrationGate_remainingLeaves_length
#check distributionalNavierStokesAPIStatus
#check distributionalNavierStokesAPILeaves
#check parabolicGeometryAPIStatus
#check parabolicGeometryAPILeaves
#check epsilonRegularityAPIStatus
#check epsilonRegularityAPILeaves
#check DistributionalNavierStokesAPI.weak_navierStokes_equation
#check DistributionalNavierStokesAPI.weak_divergenceFree
#check DistributionalNavierStokesAPI.representatives_match_memLp_data_holds
#check mem_twoSidedParabolicCylinder_iff
#check mem_backwardParabolicCylinder_iff
#check mem_forwardParabolicCylinder_iff
#check ParabolicGeometryAPI.backwardSet_subset_domain
#check ParabolicGeometryAPI.parabolic_metric_model
#check cknScaleInvariantValue_eq_mul
#check CKNScaleInvariantQuantities.smallAt_iff
#check CKNScaleInvariantQuantities.backwardSet_subset_domain
#check CKNScaleInvariantQuantities.quantities_nonnegative_holds
#check CKNEpsilonRegularityPackage.regularAt_center
#check CKNRegularityOutsideSingularBridge.regularAt_of_not_mem_singular
#check MeasureTheory.MemLp
#check MeasureTheory.Measure.hausdorffMeasure
#check Distribution
#check TestFunction
#check ContDiffAt
#check localValidationCommand
#check localValidationMachineStatus
#check repoLocalIntegrationDebtGateStatus

end AwesomeTheorems.Stage1.S1_M_156
