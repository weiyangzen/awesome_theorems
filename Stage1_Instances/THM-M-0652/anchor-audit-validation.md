# THM-M-0652 anchor-audit validation

Item: `S56-M-0652-ANCHOR_AUDIT`  
Base revision: `eb5c892a92c1c04b8fef2fcfa1216419112ad294`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The pinned mathlib checkout is clean at `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
Its compactness, model semantics, and language-map declarations elaborate, but a source scan found
no first-order Craig interpolation theorem. The historical `S1_M_298` module is an alternate,
overbroad statement plus conditional proof architecture: completeness, extraction, and terminal
correctness are inputs rather than a proof of the frozen target.

The external search located a genuine sorry-free Lean 4 interpolation theorem at immutable commit
`1faed382f0c4d2b6656801a595b9dd2a4b0c2ea6` of `mgignoux/lean4-gl-coalgebras`. It proves Craig
interpolation for propositional modal Goedel-Loeb logic, not arbitrary first-order languages and
structures, so it is explicitly excluded as a domain mismatch. No exact external first-order
candidate was established. The root remains `M3` with formalization debt and is not kernel-closed.

## Commands and exact outcomes

| Command | Exit/result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0; 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0652` | 0; rank 298, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0; empty output |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0652/Statement.lean` | 0; exact frozen statement and mutation probes elaborated; `statement_iff` reports `Quot.sound` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0652/AnchorAudit.lean` | 0; support wrappers elaborated; compactness reports `propext`, `Classical.choice`, `Quot.sound`, while the language-map wrapper reports `propext`, `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0652/check_anchor_audit.py` | 0; local pin/source facts and immutable external hashes/types matched; root remained `M3` |
| `python3 -m json.tool Stage1_Instances/THM-M-0652/anchor-audit.json` | 0; valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0652 .stage1-worker-selftest.json` | 0; no whitespace errors |

Repository searches covered the local target, the historical module, every pinned mathlib Lean
source, GitHub repository metadata, and immutable raw source for the credible GL candidate. GitHub's
core API quota was exhausted after discovery and grep.app returned a security checkpoint; the audit
therefore makes no exhaustive global negative claim. No `lake update`, build, clone, fetch, or
dependency mutation was performed.

This self-tests the candidate inventory and classification only. It does not complete the broader
audit endpoint, obligation tree, proof, validation, release, independent review, or theorem gates.
