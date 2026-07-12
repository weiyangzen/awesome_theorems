# THM-M-0352 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the source label "Calderon-Zygmund theory."
It starts from `L0 / rework_required` and inherits no proof credit from the metadata value
`source_status_untrusted: 已验证`.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Repository wording | "the theory of singular integral operators" | This is a subject area, not a proposition with ordered binders and a conclusion |
| Operators | Singular integral operators governed by Calderon-Zygmund kernel conditions | Kernel representation, size, regularity, cancellation, truncation, and initial domain are unspecified |
| Ambient analysis | Function spaces and a measure-bearing domain | Euclidean versus homogeneous-space setting, scalar field, measure, and dimension are unspecified |
| Possible conclusions | Boundedness or endpoint results associated with the theory | `L2`, weak `(1,1)`, strong `Lp`, maximal truncation, and weighted variants are inequivalent choices |
| Neighboring targets | `THM-M-0298` (decomposition) and `THM-M-1171` (Hessian estimate) | They are separate targets and cannot supply a substitute statement for this item |
| Lean surface | A future exact proposition after source selection | No declaration or expression is selected at intake |
| Trust surface | Lean 4 kernel plus pinned mathlib candidate | Exact imports, toolchain fingerprint, dependency closure, and trust policy belong to later phases |

An eventual dossier could require a kernel definition, truncations, a base `L2` hypothesis, a
Calderon-Zygmund decomposition, endpoint control, interpolation, and strong `Lp` consequences. That
is only a map of the named theory, not a frozen proof architecture or evidence of any one theorem.

## Intake verdict

Lifecycle is `planned`; the provisional root vector is `[H4, M4, R4]`. The first failed downstream
gate is exact source-statement identification. Choosing a standard theorem from the broad theory
would invent information absent from the repository record and could duplicate a neighboring
target. The authoritative lane must select a primary source and pinpoint theorem, including all
domains, operator assumptions, endpoints, and conclusion, before the statement phase can elaborate
an exact Lean target.

This intake node itself is structurally self-tested. It creates no Lean declaration, makes no
kernel claim, and does not claim theorem completion. Exact commands and results are in
`validation.md`.
