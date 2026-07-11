# Source-statement crosswalk

| Claim component | Source evidence currently available | Lean surface | Intake assessment |
|---|---|---|---|
| Attribution and subject | Repository research record: Paul Levy, 1925, "inversion of the characteristic function" | none frozen | Metadata is discovery-only and too terse for source fidelity |
| Interval probability | Standard Levy inversion formulation recovers `mu((a,b])` when endpoints are continuity points | proposed `Measure Real` root | Primary edition/theorem/page and exact interval convention remain open |
| Characteristic function | Fourier-Stieltjes transform of the probability law | mathlib Fourier/measure integration APIs to be audited | Sign and normalization conventions must be frozen together |
| Endpoint hypotheses | No atoms at `a` and `b`, or continuity of the distribution function there | singleton-measure equalities proposed | Equivalence and required measurability facts are unchecked |
| Symmetric improper limit | Limit of integrals over `[-T,T]` as `T -> +infinity` | filter limit plus interval integral candidate | Treatment of `t = 0` and complex-to-real equality is unresolved |

## Source boundary

The repository's only located source statement is
`Docs/researches/math_theorems.md`, which says only "characteristic-function inversion." It does
not specify the interval, endpoint hypotheses, normalization, sign convention, or limiting mode.
Consequently it cannot support `H0` or an exact Lean target by itself.

The interval-mass formula in `intake.json` is the conventional candidate interpretation, not a
claimed transcription of Levy's 1925 text. Before the statement node can close, the source audit
must record a stable scan or edition, bibliographic title, theorem/page, all assumptions, notation
translation, and an errata search. A modern authoritative probability text may clarify notation,
but it must not replace the primary-source genealogy silently.

## Required statement checks

1. Decide and cite the precise root variant: atom-free endpoints or the averaged boundary formula.
2. Freeze the Fourier sign, `2*pi` normalization, half-open interval, and value of the kernel at zero.
3. Inspect pinned mathlib for characteristic-function and Fourier-Stieltjes declarations; record
   exact types rather than inferring an anchor from a name.
4. Elaborate the minimal Lean expression and check transports to distribution functions and laws of
   random variables.
5. Mutation-test endpoint atoms, endpoint order, transform sign, probability normalization, and
   limiting filter.

No external or mathlib theorem is credited at intake, and no human-proof closure is claimed.
