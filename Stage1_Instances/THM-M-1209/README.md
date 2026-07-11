# THM-M-1209 rev-5.6 intake

This is a new `planned` instance for the Keel-Tao endpoint Strichartz estimate. The repository's
short label is ambiguous; this intake resolves it provisionally to the abstract theorem in Keel and
Tao (1998), Theorem 1.2, rather than to one equation-specific corollary.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Root | Abstract endpoint Strichartz theorem under energy and dispersive estimates | Exact constants and all source notation await statement transcription |
| Inputs | Hilbert data, compatible Banach/interpolation spaces, operator family `U(t)`, forcing `F` | Lean structures, strong measurability, and almost-everywhere conventions are open |
| Exponents | Sharp `sigma`-admissible pairs allowed by source Theorem 1.2 | Exceptional endpoint must not be broadened |
| Outputs | Homogeneous, dual homogeneous, and retarded inhomogeneous mixed-norm bounds | No component is credited as formally closed |
| Proof architecture | `TT*`, dyadic bilinear decomposition, interpolation/summation, Christ-Kiselev-sensitive retarded bound | Obligation registry belongs to a later phase |
| Foundations | Lean kernel plus pinned mathlib analysis stack | Toolchain, imports, classical/choice use, and trust closure are open |

The apparent duplicate `THM-M-0382` is a separate owned target. It is not inspected for proof credit
or modified here; deduplication is an integration-lane question.

## Intake verdict

Lifecycle is `planned`, with provisional vector `[H1, M4, R3]`. The source is identified, but a
pinpoint premise-by-premise audit is incomplete and no canonical Lean expression exists. The first
failed gate is therefore the exact statement/elaboration gate. The theorem is not complete.

## Validation

The exact commands and results are recorded in `validation.md`. They validate manifest membership,
the rev-5.6 standard, JSON syntax, local references, and whitespace only; they are not kernel proof
evidence.
