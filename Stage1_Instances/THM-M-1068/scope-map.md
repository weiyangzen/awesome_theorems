# Scope map

## Preserved source scope

- Named family: Tanaka's formula.
- Process family: the repository explicitly mentions reflected Brownian motion; the standard
  identity is formulated using Brownian motion or, more generally, a real continuous
  semimartingale.
- Mathematical ingredients: positive part or absolute value, a stochastic integral with an
  indicator/sign integrand, and local time at a spatial level.
- Intended role: a nonsmooth extension of Ito's formula and its relationship to reflection.

This is the maximum scope justified at intake. It does not decide that a general semimartingale
statement is the repository root, nor that a Brownian special case or reflection corollary may
replace the selected source theorem.

## Decisions required by the statement phase

The source audit and statement freeze must select exactly one root and record:

- positive-part, negative-part, or absolute-value form;
- Brownian motion, reflected Brownian motion, or continuous-semimartingale domain;
- local time at zero or an arbitrary level `a`, and right/symmetric local-time normalization;
- the convention for `sgn 0` and endpoint indicators in the stochastic integrand;
- initial value and initial-local-time terms;
- fixed-time, simultaneous-all-times, indistinguishability, or almost-sure quantification;
- filtration usual conditions, adaptation, continuity, integrability, and measurability assumptions;
- the construction/API used for stochastic integrals and local time;
- binder order, universes, minimal imports, logical profiles, and boundary cases.

The statement phase must provide checked transports before crediting another formula as equivalent.
For example, deriving the absolute-value identity from positive and negative parts depends on
matching local-time and sign conventions; deriving reflected Brownian motion requires a precise
Skorokhod decomposition and is not definitional equality.

## Explicit exclusions

- Ordinary smooth `C^2` Ito formula without the local-time correction.
- A deterministic identity containing abstract fields that already assume the Tanaka equality.
- A discrete random-walk approximation or numerical simulation as the root theorem.
- Only the occupation-time formula, Levy's identity, or the Skorokhod reflection lemma.
- Replacing Brownian motion by a special deterministic path, or replacing a source-selected
  Brownian theorem by an unbridged general-semimartingale formulation.
- Treating the metadata label `已验证` as source or Lean evidence.

No proof tree, machine candidate, or obligation denominator is frozen in this intake; those belong
to later dependency-ordered phases.
