# Anchor audit validation

Item: `S56-M-1055-ANCHOR_AUDIT`  
Base revision: `bbb17fe085a3545a76988417fdad024a9e9e136a`

## Result

The pinned local mathlib checkout supplies the exact average definition, finite-average a.e.
transport, the ergodicity predicate, fixed-point convergence, and an invariant-function-to-constant
bridge. It does not supply the pointwise a.e. convergence step required by the canonical target.
The only identified external Lean 4 candidate is pinned by commit, but is not in this Lake closure,
uses older Lean and mathlib revisions, and ends at an invariant conditional expectation rather than
the canonical constant space mean. It is therefore anchor-only evidence, not kernel closure.

The external repository metadata is corroborated by the existing git-tracked source audit in
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_247.lean`. A fresh HTTPS retrieval of the immutable
raw source timed out (`curl` exit 28, HTTP 000), so this worker explicitly leaves its current
placeholder/axiom inspection unverified rather than manufacturing a clean result.

## Commands and exact results

All Lean commands used the existing pinned `.lake`; no dependency update, fetch, clone, or build was
run.

| Command | Exit | Result |
|---|---:|---|
| `git rev-parse HEAD` | 0 | `bbb17fe085a3545a76988417fdad024a9e9e136a` |
| `jq '.packages[] | select(.name=="mathlib")' Formalizations/Lean/lake-manifest.json` | 0 | mathlib `rev` and `inputRev` both `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; pinned checkout clean |
| focused `rg` declaration/search inventory over pinned mathlib | 0 | found supporting declarations listed in `anchor-audit.json`; no terminal target candidate |
| `curl -L --max-time 30 .../fc06094.../lean-toolchain` | 28 | connection timed out after 30001 ms; HTTP 000 |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1055/AnchorAudit.lean` | 0 | all local anchor names/types elaborated; axiom reports recorded the standard mathlib foundations only |
| `python3 -m json.tool Stage1_Instances/THM-M-1055/anchor-audit.json` | 0 | valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1055` | 0 | rank 247; `L0`, `rework_required`, theorem complete false |
| `git diff --check -- Stage1_Instances/THM-M-1055 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This completes only the node-scoped candidate inventory and classification pending master
acceptance. It does not import the external project, prove the missing convergence theorem, close
M-debt, or claim theorem completion. The first downstream proof blocker is a locally checked
pointwise a.e. convergence theorem, followed by the invariant-conditional-expectation-to-integral
bridge if the external route is selected.
