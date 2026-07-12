# S56-M-1258-STATEMENT receipt

## Frozen target

`Statement.lean` elaborates `Stage1Instances.THM_M_1258.hormanderCondition`. The target is a
predicate on an open subset of `Real^n`, one drift field `X0`, and finitely many square fields
`X j`. At every point in the domain, the values of those fields and all finite iterated Lie
brackets must span `Real^n`.

This selection follows the repository's exact row: THM-M-1258 is "Hormander condition" and its
content is "condition for subelliptic operators." It is not the neighboring THM-M-1259 regularity
theorem. Consequently the canonical Lean target is a condition-valued declaration, not a false
closed assertion that every family of vector fields satisfies the condition, and not a
hypoellipticity conclusion silently imported from the neighboring target.

Binder order is: dimensions `n` and `r`; open domain `Omega`; drift coefficients `X0`; square-field
coefficients `X`. The inductive generated family includes each original field and is closed under
binary Lie brackets, hence represents all finite iterated brackets. The domain is used only in the
pointwise quantifier. The cases `n = 0`, `r = 0`, and an empty domain are intentionally governed by
the same definition rather than excluded.

The only direct import is `Mathlib.Analysis.Calculus.VectorField`, which supplies the Lie bracket;
the remaining names used by the target are in its transitive prelude. No proof, axiom, placeholder,
analytic regularity conclusion, or theorem-completion claim occurs in this artifact.

## Validation evidence

Base revision: `c00bc6793b3d4c186b81b80bbaf165b32e125b58`.

| Command | Exit | Exact result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1258/Statement.lean` | 0 | printed the declaration and explicit `@hormanderCondition` types; no diagnostics |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1258` | 0 | rank 436, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1258` | 0 | no output |

Environment fingerprint: Lean toolchain `leanprover/lean4:v4.29.0`; toolchain-file SHA-256
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`; statement SHA-256
`dcc96ffafc032a8a8c0d5131874bdc6a3681663cb1957b64caf3fd2c244fa7d6`.

## Status boundary

This receipt supports only worker self-test of `S56-M-1258-STATEMENT` and remains subject to master
acceptance. It does not advance the source audit, anchor audit, proof, validation, or release nodes.
The historical primary article's exact page wording and errata remain H-status work; in particular,
this statement receipt does not claim H0 or machine proof of the separate analytic theorem.
