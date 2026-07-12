# Source-statement crosswalk

## Available repository source

`Docs/researches/math_theorems.md` records the title, attribution `AKNS`, year 1974, and the phrase
`可积系统的统一框架`. `Docs/Stage0_Blueprint.md` repeats these fields and explicitly leaves the exact
definitions, premises, proof route, equivalent formulations, axioms, and machine artifact open.
These records establish provenance of the intake phrase but do not establish a mathematical
theorem or human-proof status.

## Candidate primary source

Mark J. Ablowitz, David J. Kaup, Alan C. Newell, and Harvey Segur, *The Inverse Scattering
Transform-Fourier Analysis for Nonlinear Problems*, Studies in Applied Mathematics 53 (1974),
249-315, is the likely original source behind the repository record. It is recorded only as a
discovery candidate. This intake did not independently inspect a stable scan for the exact
equation/theorem/page, assumptions, corrections, or errata, so the citation is not `H0` evidence.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "AKNS system" | a matrix spectral problem and compatible evolution | matrix-valued functions/operators with a spectral parameter | family identified; exact conventions open |
| "unified framework" | a common zero-curvature construction yielding selected nonlinear evolution equations | compatibility predicate and proved coefficient equivalence | not itself a proposition |
| "integrable systems" | source-enumerated equations or hierarchy reductions | explicit flow/reduction predicates and transports | quantified class open; no universal claim allowed |
| 1974 / AKNS | historical locator | no formal proof component | candidate paper identified only |
| `已验证` | untrusted inventory status | no kernel evidence | no proof credit |

## Source and machine boundary

A repository search found no theorem-specific Lean artifact and no `AKNS` or full-name match in the
pinned mathlib source tree. This is narrow intake evidence, not a complete anchor audit and not
evidence that no formalization exists elsewhere. Anchor audit remains dependency-ordered after the
statement phase.

Before `H0`, an independent reviewer must inspect a fixed edition and approve a pinpointed result,
the exact operator formulas, all analytic and algebraic assumptions, the proof boundary, and known
errata. Before statement credit, every approved source component must map row by row to an
elaborated Lean expression; alternate formulations require checked transports.
