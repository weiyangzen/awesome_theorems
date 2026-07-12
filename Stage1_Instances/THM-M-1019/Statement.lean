import Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic

/-!
# THM-M-1019 canonical statement

This file freezes the measure-level uniqueness theorem for characteristic functions on the real
line. It elaborates the proposition and its integral encoding; it does not prove the proposition.
-/

noncomputable section

open MeasureTheory

namespace Stage1Instances.THM_M_1019

/-- A real Borel probability measure is uniquely determined by its characteristic function. -/
def CharacteristicFunctionUniqueness : Prop :=
  forall (mu nu : Measure Real),
    IsProbabilityMeasure mu ->
    IsProbabilityMeasure nu ->
    charFun mu = charFun nu ->
    mu = nu

/-- Public canonical target for the statement phase. -/
abbrev Statement : Prop := CharacteristicFunctionUniqueness

/-- The same target with the characteristic functions expanded as pointwise integrals. -/
def IntegralForm : Prop :=
  forall (mu nu : Measure Real),
    IsProbabilityMeasure mu ->
    IsProbabilityMeasure nu ->
    (forall t : Real,
      (∫ x : Real, Complex.exp (t * x * Complex.I) ∂mu) =
      ∫ x : Real, Complex.exp (t * x * Complex.I) ∂nu) ->
    mu = nu

/-- Checked transport between the API-level and expanded-integral encodings. -/
theorem statement_iff_integralForm : Statement <-> IntegralForm := by
  simp only [Statement, CharacteristicFunctionUniqueness, IntegralForm, charFun_apply_real,
    funext_iff]

-- Structural mutations consumed by `check_statement.py`.
def MutationNoProbability : Prop :=
  forall (mu nu : Measure Real), charFun mu = charFun nu -> mu = nu

def MutationComplexDomain : Prop :=
  forall (mu nu : Measure Complex),
    IsProbabilityMeasure mu ->
    IsProbabilityMeasure nu ->
    charFunDual mu = charFunDual nu ->
    mu = nu

def MutationNonnegativeFrequencies : Prop :=
  forall (mu nu : Measure Real),
    IsProbabilityMeasure mu ->
    IsProbabilityMeasure nu ->
    (forall t : Real, 0 <= t -> charFun mu t = charFun nu t) ->
    mu = nu

def MutationExcludesDiracZero : Prop :=
  forall (mu nu : Measure Real),
    IsProbabilityMeasure mu ->
    IsProbabilityMeasure nu ->
    mu ≠ Measure.dirac 0 ->
    nu ≠ Measure.dirac 0 ->
    charFun mu = charFun nu ->
    mu = nu

#check Statement
#check statement_iff_integralForm
#print CharacteristicFunctionUniqueness
#print IntegralForm
#print MutationNoProbability
#print MutationComplexDomain
#print MutationNonnegativeFrequencies
#print MutationExcludesDiracZero

end Stage1Instances.THM_M_1019
