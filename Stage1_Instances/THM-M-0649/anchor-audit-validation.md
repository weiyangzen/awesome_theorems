# Anchor-audit validation record

Item: `S56-M-0649-ANCHOR_AUDIT`  
Base revision: `2eb836c21ebdba77082dcafd9222259988e44a54`

## Result

The bounded inventory contains one exact local statement artifact and two pinned mathlib ingredient
families. No candidate closes the frozen root. `DirectLimit.of` is only an ordinary language
embedding; `exists_of` and `iSup_range_of_eq_top` provide coverage; `Equiv_iSup` is a structural
equivalence; and the two `isElementary_of_exists` declarations require the Tarski-Vaught witness
condition that is precisely still missing. Consequently the truthful root machine classification
after this phase is `M3`, not `M0-W` or `M1`.

The repository and pinned-mathlib searches were locally replayable. External discovery was bounded:
GitHub anonymous code search required authentication or returned a shared-address rate-limit error,
and grep.app returned HTTP 503. The ledger therefore does not claim exhaustive public saturation.
No moving dependency was fetched, cloned, or added.

## Commands and results

All Lean commands ran from `Formalizations/Lean` against the existing pinned `.lake` artifacts.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0649/AnchorAuditProbe.lean` | 0 | all seven nearest mathlib declarations elaborated at the pinned revision |
| `lake env lean ../../Stage1_Instances/THM-M-0649/Statement.lean` | 0 | exact frozen target and statement mutations still elaborate |
| `git -C .lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | commit `8a178386...a95`, tree `bdc39a...c2b` |
| `git -C .lake/packages/mathlib status --short` | 0 | no output; pinned dependency tree clean |
| scoped `git grep` in `.lake/packages/mathlib/Mathlib/ModelTheory` | 1 | no exact elementary-chain/direct-limit-elementarity declaration matched; nearby declarations were manually inventoried |
| scoped `rg` over repository `*.lean`, `*.md`, and `*.json` | 0 | no root proof or external formal candidate; only this dossier and unrelated phrase-level prose |
| anonymous GitHub REST/code and HTML searches | mixed | repository API responses were rate-limit payloads (SHA-256 `08c082...00b2`); code API HTTP 403; HTML required sign-in |
| five anonymous grep.app queries | 22 | HTTP 503 for each; empty response SHA-256 `e3b0c4...b855` |
| `python3 -m json.tool Stage1_Instances/THM-M-0649/anchor-audit.json` | 0 | structured candidate ledger valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard and 1546-target projection valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and uniform L0/rework-required baseline valid |
| `python3 scripts/stage1_target.py show THM-M-0649` | 0 | rank 695, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0649 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Boundary

This node is self-tested audit evidence pending master acceptance. It neither proves the theorem nor
closes the full dossier audit. The next formal cut is to derive the Tarski-Vaught witness property
for the canonical direct-limit embedding and freeze that work as explicit downstream obligations.
