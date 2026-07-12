# Anchor-audit validation record

Item: `S56-M-1527-ANCHOR_AUDIT`  
Base revision: `86e472db58e8bcf559808ae07c9f5abe9fa78434`  
Audit cutoff: 2026-07-12

## Result

The exact repo-local artifact is a proposition definition without a proof body. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies exterior derivatives, `d^2 = 0`, pullback, and
vector-field evaluation, but no Maxwell declaration or classical/covariant coordinate bridge.

The public search found a substantive candidate that the legacy audit missed:
`leanprover-community/physlib@851e49a321d5a8dad4da23583da422f569c53cb4`. Its
`Physlib/Electromagnetism/ThreeDimension/MaxwellEquations.lean` explicitly proves Gauss-electric,
Gauss-magnetic, Ampere, and Faraday equations for fields derived from a potential; the sourced
equations assume Physlib's `IsExtrema`. This is useful partial formalization, not the frozen target:
it has no differential-form Maxwell system, Lorentzian Hodge star, 3+1 decomposition theorem, or
equivalence with the covariant equations. It therefore receives `M3_partial_non_target`, not root
proof credit. The root remains `M4`.

The immutable Physlib source hashes to
`3373642bc4740de4522a427ad5073a34adf948988dac654b5e93ae3327051578`. Its toolchain is Lean 4.30.0
and manifest pins mathlib `c5ea00351c28e24afc9f0f84379aa41082b1188f`; this worker's closure uses
Lean 4.29.0 and mathlib `8a178386...`. Per the worker constraints, Physlib was inspected through
commit-qualified raw files and was not cloned, fetched, installed, or added to `.lake`. Thus its
transitive kernel/axiom closure is not claimed locally checked.

## Commands and exact results

Commands ran in this worker clone and reused the existing pinned `.lake` artifacts.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1527/AnchorAudit.lean` | 0 | six pinned mathlib declarations elaborated and their types printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1527/Statement.lean` | 0 | exact canonical statement re-elaborated |
| `python3 Stage1_Instances/THM-M-1527/check_anchor_audit.py` | 0 | audit boundary, six probes, external classification, manifest pin, and installed mathlib HEAD agreed |
| `rg -n -i --glob '*.lean' 'maxwell\|electromagnet\|faraday\|\\bamp[eè]re\\b\|gauss.*(electric\|magnetic)\|hodge.*star' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | no Maxwell-specific match in pinned mathlib; exit 1 is ripgrep's no-match status |
| `curl -G https://sourcegraph.com/.api/search/stream --data-urlencode 'q=context:global lang:Lean Maxwell count:100'` | 0 | discovered 22 results, all in Physlib at indexed commit `851e49a...`; the initial stream was incomplete, so no exhaustive negative claim is made |
| `curl -G https://sourcegraph.com/.api/search/stream --data-urlencode 'q=context:global repo:^github.com/leanprover-community/physlib$ lang:Lean (Maxwell OR electromagnetism OR gaussLawElectric OR faradayLaw) count:100'` | 0 | 100 project-scoped matches; result-limit warning; response SHA-256 `4cce43...50eb` |
| commit-qualified `curl` for Physlib `MaxwellEquations.lean`, `lean-toolchain`, `lake-manifest.json`, and `LICENSE`, followed by `sha256sum` | 0 | hashes `337364...1578`, `95902a...a286`, `b14db9...6c52b`, and `c71d23...ab4`; exact declarations and dependency pins inspected |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure passed for 15 groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1527` | 0 | rank 195; planned; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1527/anchor-audit.json >/dev/null` | 0 | structured audit is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1527 .stage1-worker-selftest.json` | 0 | no whitespace errors before receipt creation |

## Boundary

This is a completed bounded anchor audit pending master acceptance. Sourcegraph hit a result limit,
grep.app was blocked, and authenticated GitHub code search was unavailable, so global search
saturation is not claimed. No exact external proof was found, nothing is eligible for root
integration, and theorem completion remains false.
