# Machine-checked audit

## MC-root

The intended root declaration is
`AwesomeTheorems.Stage5.S5_CLM_00003528.borwein_sine_series`.  The frozen
provider declaration is recorded only as provenance and is not referenced as
proof authority.

## MC-no-oracles

The three claim-owned Lean surfaces contain no `sorry`, `admit`, `axiom`,
`opaque`, unsafe declaration, local semantic definition, notation, macro,
syntax extension, namespace alias, or local instance.  They import `Mathlib`.

## MC-worker-scope

This worker is forbidden to run Lean, Lake, or Elan.  The local command is
therefore semantic/evidence preflight only.  All statements about compiled
objects, exact elaborated roots, dependency bodies, observed axioms, and cold
replay are provisional inputs that the Master must independently recompute.

## MC-mutations

The evidence records rejection expectations for replacing reals by naturals,
positive naturals by naturals, `Summable` by `True`, `Real.sin` by a constant,
the provider import/declaration provenance by a different source, and any
claim-specific axiom.  Master replay must actually execute these mutations.
