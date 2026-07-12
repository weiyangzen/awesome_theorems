# Anchor audit validation record

Item: `S56-M-1515-ANCHOR_AUDIT`  
Base revision: `4161921b2a43484a498bcf39900c1c468bc4174e`

## Result

The audit is bound to the frozen expression hash and to mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). Four useful calculus candidates elaborate:
`HasDerivAt.sub`, `HasDerivAt.clm_apply`, `HasFDerivAt.clm_apply`, and
`DifferentiableAt.hasFDerivAt`. They are substrate for a later chain-rule proof, not terminal
Noether theorems.

All Lean files in the already installed pinned dependency closure were searched for the exact and
semantic terms recorded in `anchor-audit.json`. There was no terminal match. Name-only Noether
matches were unrelated algebraic theorems. The immutable legacy artifact at repository revision
`16d227cffb7cb7d9e8392b6c0ff8211e498e1330` was also inspected: it expressly leaves the terminal
theorem open and uses a different abstract package, so it receives discovery credit only.

The successful GitHub repository query for `"Noether's theorem" Lean` returned zero repositories.
Further public discovery was bounded by API rate limiting, a grep.app security checkpoint, and
timeouts while trying to inspect PhysLean. Those failures are recorded rather than converted into
a global nonexistence claim. PhysLean is not pinned in this project and no immutable revision was
obtained, so it receives no formal-candidate or proof credit. No dependency was fetched or changed.

## Commands and results

All commands ran inside this worker clone, using the existing pinned Lake artifacts.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1515` | 0 | rank 184, planned, theorem incomplete |
| pinned dependency `rg` search for the eight recorded terms | 0 | no variational Noether terminal candidate; unrelated name matches classified |
| GitHub repository API query for `"Noether's theorem" Lean` | 0 | `total_count: 0`, `incomplete_results: false` |
| additional GitHub, grep.app, PhysLean remote/raw probes | non-authoritative failure | rate limits, security checkpoint, or timeout; bounded-search limitation recorded |
| `python3 Stage1_Instances/THM-M-1515/check_anchor_audit.py` | 0 | statement and immutable mathlib pins matched; four anchors elaborated; root remained M3 |
| `python3 -m json.tool Stage1_Instances/THM-M-1515/anchor-audit.json >/dev/null` | 0 | structured audit parses |
| forbidden-token scan of new executable and structured artifacts | 1 | no prohibited proof substitute; exit 1 is ripgrep no-match |
| `git diff --check -- Stage1_Instances/THM-M-1515 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This anchor-audit node is self-tested pending master acceptance. Root debt stays
`[H1, M3, R3]`. No exact terminal declaration, external pinned integration, proof body, source
review, obligation tree, or theorem-completion evidence was produced.
