# THM-M-1171 proof-phase attempt

Item: `S56-M-1171-PROOF`  
Attempt date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `bf8f1a403fb8c22395ec64f92f93fed974f23c83`

## Verdict

`blocked`; no proof body was added and no proof credit is claimed.

The exact target in `Statement.lean` re-elaborates, but the existing pinned dependency closure does
not contain the analytic theorem needed to implement the frozen proof tree. In particular, a
case-insensitive whole-source search of pinned mathlib found no Mikhlin theorem, Marcinkiewicz
multiplier theorem, Riesz transform, or Calderon-Zygmund theorem. The related external weak `(1,1)`
Carleson result recorded by the anchor audit is neither type-equivalent to the strong `L^p`
Hessian-by-Laplacian target nor present in the pinned dependency closure. Fetching or changing that
closure is forbidden for this worker validation.

This is a mathematical integration blocker, not an elaboration workaround: proving only the
finite-dimensional assembly lemmas would leave the root open, while postulating the multiplier
bound would require an `axiom` or placeholder. Both would fail the assigned proof gate.

## Remaining root cut set

- `M1171-N-SCHWARTZ` and `M1171-N-COMPLEX`: checked transport from compactly supported smooth real
  functions to the Fourier/Schwartz setting.
- `M1171-L-FOURIER-DERIV`, `M1171-C-MULTIPLIER`, and `M1171-L-ZERO-FREQ`: the exact componentwise
  multiplier identity, including the null zero-frequency set.
- `M1171-L-MIHLIN`: strong `L^p` boundedness for the symbols
  `xi_i * xi_j / |xi|^2`, uniformly in the component indices, for every `1 < p < infinity`.
- `M1171-L-FDERIV-PARTIAL`, `M1171-L-TRACE`, `M1171-L-OPNORM`, and
  `M1171-L-LP-ASSEMBLY`: checked transports and finite-dimensional assembly into the exact frozen
  Frechet-Hessian/operator-norm and `ENNReal.eLpNorm` statement.
- `M1171-T-COMPONENT`, `M1171-T-ASSEMBLE`, and `M1171-ROOT`: checked child-to-parent composition.

The proof node can reopen when those obligations are implemented locally without placeholders, or
when an immutable dependency-legal Lean 4 result closing the strong multiplier bridge is pinned and
passes exact-type, provenance, license, axiom, and placeholder checks.

## Commands and exact results

All Lean checks used the existing `.lake` artifacts. No `lake update`, build, clone, fetch, or
dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1171` | 0 | Rank 372; lifecycle `planned`; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1171/Statement.lean` | 0 | Exact target and definitional transport elaborated; Lean printed the expanded target |
| `rg -n -i '\\b(mihlin\|marcinkiewicz)\\b\|riesz[ _-]*transform\|calder[oó]n[ _-]*zygmund' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No matching pinned mathlib source declaration |
| `rg -n '\\bsorry\\b\|\\baxiom\\b' Stage1_Instances/THM-M-1171 --glob '*.lean'` | 1 | No placeholder or axiom token in the dossier's Lean sources |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lake-manifest.json Formalizations/Lean/lean-toolchain` | 0 | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`; `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |

Because the assigned phase is not genuinely self-tested to closure,
`.stage1-worker-selftest.json` is intentionally absent.
