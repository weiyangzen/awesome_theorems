# THM-M-1276 rev-5.6 intake

This is the `planned` dossier for Trudinger's critical Sobolev embedding. The Stage0 phrase
`临界Sobolev嵌入` is too short to identify a formal proposition by itself. This intake selects the
standard non-sharp, zero-boundary exponential-integrability form and explicitly keeps its precise
domain regularity open for the primary-source audit. It does not merge the neighboring sharp
Moser-Trudinger target `THM-M-1277` into this theorem.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Root | Existence of positive `alpha` and finite `C` controlling exponential integrability of normalized `W_0^{1,n}` functions on a bounded domain | Exact source hypotheses and Lean encoding remain open |
| Domain | Dimension `n >= 2`, bounded domain in real Euclidean space, zero trace | Cone/Lipschitz/open/measurable assumptions must be pinned from the source and formal API |
| Normalization | Gradient `L^n` energy at most one | Norm-versus-modular conventions require checked transport |
| Endpoint | Exponent `n/(n-1)` and some positive exponential coefficient | No optimal coefficient or failure beyond it is claimed |
| Equivalent form | Embedding into the corresponding exponential Orlicz space | Orlicz definitions and equivalence are unimplemented candidates |
| Foundations | Lean kernel, measure theory, Bochner/weak derivative and Sobolev infrastructure | Toolchain, imports, axioms and feasibility are unaudited |

The future statement phase must resolve the regularity phrase rather than silently choosing a
convenient mathlib domain. It must also decide whether an existing Sobolev-space API can express
zero trace and weak gradients without substituting a stronger smooth-function theorem.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed gate is exact
source-statement identity: the repository supplies only a title and gloss, and the discovered
primary paper has not yet received a pinned theorem/page/assumption/errata crosswalk. Consequently
there is no canonical Lean expression or environment fingerprint. The theorem is not complete.

## Validation

The exact structural commands and their results are recorded in `validation.md`. They validate
manifest membership, the rev-5.6 standard, JSON syntax, and dossier-local consistency only.
