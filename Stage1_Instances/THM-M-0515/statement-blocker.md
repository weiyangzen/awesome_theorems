# Exact-statement gate: blocked

Item: `S56-M-0515-STATEMENT`  
Theorem: `THM-M-0515`  
Base revision: `e9252b1cfdc99a094324c8a10d260769df2eca15`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is `虚二次域的类域的生成` ("generation of class fields of imaginary
quadratic fields"). Stage0 supplies no exact definitions or assumptions, source edition, theorem
number, page, ordered binders, hypotheses, conclusion, or machine artifact. The intake therefore
correctly records a theorem family rather than a canonical proposition.

Several inequivalent claims remain compatible with the gloss: generation of a Hilbert class field
by a singular modulus, generation of ring class fields attached to nonmaximal orders, generation of
ray class fields by other modular-function values, or a broader reciprocity/classification result.
They differ in the quadratic field and order, conductor, named class field, modular function, CM
point, base field, field-adjunction equality, quantifier order, and exceptional discriminant,
integrality, unit, and roots-of-unity cases. Selecting any one would invent or substitute missing
mathematics.

Consequently there is no canonical human statement from which to choose minimal imports, no exact
Lean expression to serialize or hash, and no sound removed-hypothesis, changed-domain,
changed-binder-scope, or boundary mutation test. Section 5.1 of the rev-5.6 blueprint fails before
proof evidence may be inspected. No declaration, assumed generation hypothesis, weakened special
case, placeholder, or axiom was introduced. The statement node remains open at `M4`; audit and
theorem completion remain false.

## Pinned environment boundary

The existing `IntakeProbe.lean` imports
`Mathlib.NumberTheory.NumberField.CMField` and
`Mathlib.NumberTheory.NumberField.ClassNumber`. It checks the pinned CM-field predicate, ring of
integers, class group, and class number APIs. Re-elaborating that file distinguishes an available
Lean environment from the missing mathematical statement; it is not a canonical target and earns
no statement or proof credit.

Narrow searches of pinned mathlib found no declaration named for Jugendtraum, Hilbert/ring/ray
class-field generation, singular moduli, or a complex-multiplication class-field theorem. This is
only a bounded feasibility observation, not the later anchor audit. The environment is Lean
`4.29.0` at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Existing canonical `.lake` artifacts were read only;
no update, build, clone, or fetch was run.

## Exact validation record

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0515` | 0 | rank 889, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in `statement-blocker.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision recorded above |
| repository `rg` search for the theorem ID, Chinese/English name, and gloss | 0 | only underspecified metadata and intake records; no exact proposition or primary-source anchor |
| pinned-mathlib `rg` search for Jugendtraum and named class-field-generation variants | 1 | expected no-match exit; no theorem-specific declaration located |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0515/IntakeProbe.lean` | 0 | all four prerequisite API checks elaborated; no canonical theorem asserted |
| `rg -n '\\b(sorry|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0515 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary-source edition, select
and transcribe one exact theorem and page, record incorporated definitions and errata, fix every
field/order/conductor/function/base/boundary choice above, and independently approve the mapping.
Only then can a later statement run encode the same claim, minimize imports, fingerprint the
elaborated expression, check alternate transports, and execute all four mutation classes.

This is the first failed gate. The assigned phase is not genuinely self-tested to completion, so
no `.stage1-worker-selftest.json` is emitted.
