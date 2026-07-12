import Mathlib.Analysis.Calculus.Deriv.Basic

/-!
# THM-M-1131 canonical statement

This module freezes a homogeneous, isotropic, finite-dimensional formulation of
Fourier's constitutive law and its conditional heat-equation consequence. It
contains the target proposition, not a proof of it.
-/

noncomputable section

namespace Stage1Instances.THM_M_1131

/-- Euclidean coordinate space used for the spatial variables. -/
abbrev Space (n : Nat) := Fin n -> Real

/-- Coordinate gradient, expressed through the Frechet derivative. -/
def gradient {n : Nat} (f : Space n -> Real) (x : Space n) : Space n :=
  fun i => fderiv Real f x (Pi.single i 1)

/-- Coordinate divergence of a vector field. -/
def divergence {n : Nat} (F : Space n -> Space n) (x : Space n) : Real :=
  Finset.univ.sum fun i => fderiv Real (fun y => F y i) x (Pi.single i 1)

/-- Coordinate Laplacian, fixed definitionally as divergence of the gradient. -/
def laplacian {n : Nat} (f : Space n -> Real) (x : Space n) : Real :=
  divergence (fun y => gradient f y) x

/-- Time derivative at a space-time point. -/
def timeDerivative {n : Nat} (temperature : Real -> Space n -> Real)
    (t : Real) (x : Space n) : Real :=
  deriv (fun s => temperature s x) t

/--
The constant-coefficient heat equation follows from local energy balance and
Fourier's homogeneous isotropic flux law `q = -kappa * grad T`.

The balance sign convention is `rho*c*T_t = -div q + source`. Positivity of the
material parameters records their physical regime even though the displayed
algebraic implication does not need division by them.
-/
def FourierHeatConductionLaw : Prop :=
  forall (n : Nat), 0 < n ->
    forall (rho heatCapacity conductivity : Real),
      0 < rho -> 0 < heatCapacity -> 0 <= conductivity ->
        forall (temperature : Real -> Space n -> Real)
          (heatFlux : Real -> Space n -> Space n) (source : Real -> Space n -> Real),
          (forall t x,
            heatFlux t x = fun i => -conductivity * gradient (temperature t) x i) ->
          forall t x,
            rho * heatCapacity * timeDerivative temperature t x =
                -divergence (heatFlux t) x + source t x ->
              rho * heatCapacity * timeDerivative temperature t x =
                conductivity * laplacian (temperature t) x + source t x

/-- Public canonical target for this statement phase. -/
abbrev Statement : Prop := FourierHeatConductionLaw

-- Structural mutations fingerprint the selected convention and hypotheses.
def MutationReversedFluxSign : Prop :=
  forall (n : Nat), 0 < n ->
    forall (rho heatCapacity conductivity : Real),
      0 < rho -> 0 < heatCapacity -> 0 <= conductivity ->
        forall (temperature : Real -> Space n -> Real)
          (heatFlux : Real -> Space n -> Space n) (source : Real -> Space n -> Real),
          (forall t x,
            heatFlux t x = fun i => conductivity * gradient (temperature t) x i) ->
          forall t x,
            rho * heatCapacity * timeDerivative temperature t x =
                -divergence (heatFlux t) x + source t x ->
              rho * heatCapacity * timeDerivative temperature t x =
                conductivity * laplacian (temperature t) x + source t x

def MutationNoEnergyBalance : Prop :=
  forall (n : Nat), 0 < n ->
    forall (rho heatCapacity conductivity : Real),
      0 < rho -> 0 < heatCapacity -> 0 <= conductivity ->
        forall (temperature : Real -> Space n -> Real)
          (heatFlux : Real -> Space n -> Space n) (source : Real -> Space n -> Real),
          (forall t x,
            heatFlux t x = fun i => -conductivity * gradient (temperature t) x i) ->
          forall t x,
            rho * heatCapacity * timeDerivative temperature t x =
              conductivity * laplacian (temperature t) x + source t x

def MutationZeroSource : Prop :=
  forall (n : Nat), 0 < n ->
    forall (rho heatCapacity conductivity : Real),
      0 < rho -> 0 < heatCapacity -> 0 <= conductivity ->
        forall (temperature : Real -> Space n -> Real)
          (heatFlux : Real -> Space n -> Space n),
          (forall t x,
            heatFlux t x = fun i => -conductivity * gradient (temperature t) x i) ->
          forall t x,
            rho * heatCapacity * timeDerivative temperature t x =
                -divergence (heatFlux t) x ->
              rho * heatCapacity * timeDerivative temperature t x =
                conductivity * laplacian (temperature t) x

def MutationVariableConductivity : Prop :=
  forall (n : Nat), 0 < n ->
    forall (rho heatCapacity : Real) (conductivity : Space n -> Real),
      0 < rho -> 0 < heatCapacity -> (forall x, 0 <= conductivity x) ->
        forall (temperature : Real -> Space n -> Real)
          (heatFlux : Real -> Space n -> Space n) (source : Real -> Space n -> Real),
          (forall t x,
            heatFlux t x = fun i => -conductivity x * gradient (temperature t) x i) ->
          forall t x,
            rho * heatCapacity * timeDerivative temperature t x =
                -divergence (heatFlux t) x + source t x ->
              rho * heatCapacity * timeDerivative temperature t x =
                divergence (fun y i => conductivity y * gradient (temperature t) y i) x + source t x

#check Statement
#print FourierHeatConductionLaw
#print MutationReversedFluxSign
#print MutationNoEnergyBalance
#print MutationZeroSource
#print MutationVariableConductivity

end Stage1Instances.THM_M_1131
