# THM-M-1078 proof-phase blocker

Item: `S56-M-1078-PROOF`  
Base revision: `888613d9a2a747d4f8fca16dc48f34cc88627ba4`  
Attempt date: `2026-07-12` (`Asia/Shanghai`)

## Verdict

The proof phase is blocked and is not self-tested as complete. No proof receipt, machine-closure
credit, or theorem-completion claim is made.

The frozen proof route requires the terminal declaration
`MeasureTheory.Lp_Burkholder_inequality_martingaleTransform` from
`SmaniaD/Burkholder` at commit `afa97ef3c85697fa3b2a67af89af8d6dd09eda69`. That declaration is
not present in the repository's pinned Lean dependency closure. A direct import using the required
`lake env lean` validation environment fails before elaboration with `unknown module prefix
'Burkholder'`.

The audited source archive in `/tmp` is only discovery material, not a pinned dependency or valid
worker evidence. It targets Lean `v4.30.0-rc2` and mathlib
`aa7b3adc05244052861add85ec0ae8d9a664d7fc`, whereas the repository pins Lean `v4.29.0` and
mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`. The archive also has no local `.lake` artifacts.
Compiling or adapting its proof would therefore require fetching/building a different dependency
closure or vendoring and porting its substantive majorant development. The worker instructions
forbid `lake update`, `lake build`, dependency fetches, and mutation of the canonical `.lake`
artifacts, so this missing artifact must be reported rather than manufactured.

The exact wrapper also retains substantive open bridges recorded by the frozen obligation tree:

- terminal `MemLp (f n) p mu` must imply the all-time `MemLp` premise used upstream for arbitrary
  `1 < p < infinity`; the pinned mathlib search found conditional-expectation `MemLp` closure only
  at exponent `2`, not the required general exponent;
- mathlib `IsPredictable` must be transported to the external `IsStronglyPredictable` interface;
- indexing and `eLpNorm`/`lpNorm` transports must be checked against the imported declaration.

Those bridges cannot close the root without first placing the external definitions and terminal
body in the same kernel environment. The existing `ObligationTree.lean` proves only conditional
composition from two open proposition-valued inputs and is not a proof body for the target.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard passed: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1078` | 0 | rank 520; planned; L0/rework-required; theorem incomplete |
| `git rev-parse HEAD` | 0 | `888613d9a2a747d4f8fca16dc48f34cc88627ba4` |
| `cd Formalizations/Lean && lake env lean /tmp/thm1078-proof-import-kPZl.lean` | 1 | line 1: unknown module prefix `Burkholder`; no `Burkholder` module in any pinned search-path entry |

The temporary probe contained exactly:

```lean
import Burkholder.MartingaleTransforms
#check MeasureTheory.Lp_Burkholder_inequality_martingaleTransform
```

No `lake update`, `lake build`, clone, fetch, dependency write, or `.lake` mutation was performed.

## Reopen condition

Provide an immutable, license-reviewed Burkholder dependency or vendored port compatible with the
repository's pinned Lean/mathlib closure, including its transitive proof bodies and compiled
artifacts. Then implement and kernel-check the exact wrapper and every registered bridge, and
inspect the terminal declaration's axioms and provenance. Until that happens,
`S56-M-1078-PROOF` remains open and `.stage1-worker-selftest.json` must remain absent.
