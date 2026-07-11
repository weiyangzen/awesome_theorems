# THM-M-1006 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Burkholder-Davis-Gundy
inequalities. It records scope only and inherits no proof credit from the source label
`已验证`.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Two-sided comparison, for every `0 < p`, between the `p`-moment of a martingale maximum and the `p/2`-moment of its quadratic variation | The legacy phrase "equivalence of martingale Lp norms" does not select discrete versus continuous time; the canonical Lean expression remains open |
| Objects | Real-valued martingales on a probability space, an adapted filtration, maximal process, and quadratic variation/square function | Lean object types and measurability/integrability predicates are deferred to the statement phase |
| Constants | Positive finite constants depending only on `p`, uniformly in the martingale and horizon | Optimal constants are excluded |
| Variants | Finite discrete-time, stopped/localized, continuous local-martingale, terminal-time, and stopping-time forms | Variants require checked transports and cannot substitute for the root |
| Boundary cases | `p > 0`; zero martingale and zero quadratic variation must be admitted | `p = 0`, negative `p`, vector-valued and jump-process generalizations are excluded |
| Foundations | Lean 4 kernel, pinned mathlib, classical probability APIs | Exact toolchain, imports, axioms, and TCB closure remain open |

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
The dependent statement task must resolve the discrete/continuous-time ambiguity without weakening
the classical two-sided theorem. The anchor audit must then map primary-source hypotheses and locate
any exact Lean declarations before the obligation denominator is frozen.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed gate is exact
statement identification: repository metadata names the theorem family but does not determine one
formal variant. This intake is self-tested as a dossier artifact, not as a theorem proof. The theorem
is not complete.

## Validation

Commands and exact outcomes are recorded in `validation.md` at base revision
`9c650bd6aac0dca129c8bc8ac01e0d7432669386`.
