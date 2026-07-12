# Exact-statement gate: blocked

Item: `S56-M-0658-STATEMENT`  
Base revision: `5b9e686366f361227feae83dad76ed1231180191`  
Checked: 2026-07-12 (Asia/Shanghai)

## Gate result

No exact Lean target can truthfully be elaborated from the available source record. The repository
claim is only the Chinese phrase `稳定性理论` ("stability theory"), attributed to Saharon Shelah
and dated 1978. It contains no proposition, definition reference, ordered binders, hypotheses,
conclusion, or source locator. A theory/topic is not an exact theorem statement.

The intake crosswalk lists several proposition-changing readings: a type-counting definition of
stability, a characterization by absence of the order property, or a stability-spectrum theorem.
They differ in theory completeness, whether types are over sets or models, tuple/formula arity,
cardinal and language hypotheses, quantifier order, and conclusion. Nothing in the catalog record
selects one of them. Choosing any one would therefore be a substituted theorem, which the
rev-5.6 exact-statement gate forbids.

Consequently there is deliberately no `Statement.lean`, canonical declaration, expression hash,
minimal-import claim, transport, or mutation-test receipt. The existing `IntakeProbe.lean` checks
only that pinned mathlib exposes possible vocabulary; it is not a target and receives no statement
credit. The root remains `[H3, M4, R4]`, and statement, audit, and theorem completion remain false.

## Smallest real validation

The worker reused the existing pinned `.lake` artifacts read-only. It did not run `lake update`,
`lake build`, clone, fetch, or any dependency-mutating command.

| Command | Exact result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | exit 0; `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0658` | exit 0; rank 703; lifecycle `planned`; `legacy_artifacts_accepted: false`; `theorem_complete: false` |
| `sed -n '4868,4882p' Docs/researches/math_theorems.md` | exit 0; the complete target record gives only proposer Shelah, year 1978, statement `稳定性理论`, importance high, and untrusted status `已验证` |
| `rg -n 'THM-M-0658|谢拉赫稳定性理论|Shelah stability|Stability theory' Docs Formalizations Stage1_Instances --glob '!Stage1_Instances/THM-M-0658/**'` | exit 0; only generated catalog/manifest/blueprint references were found; no exact target-specific proposition or source locator was found |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0658/IntakeProbe.lean` | exit 0; the discovery-only model-theory vocabulary elaborated under the pinned environment |
| `git diff --check -- Stage1_Instances/THM-M-0658` | exit 0; no output |

The Lean command is a real environment check, but it cannot validate a nonexistent canonical
expression. Import minimality is likewise undefined until the expression is fixed.

## First failed gate and unblock condition

The first failed gate is exact source-statement identity. To unblock it, a source reviewer must
provide and justify an immutable primary-source edition plus a pinpointed theorem or definition,
including every incorporated definition, assumption, edition difference, correction, and erratum,
and independently confirm that this is the intended referent of the catalog entry. Only then can a
later statement attempt freeze the binders and boundary cases and elaborate the exact Lean target.

This is a blocker receipt, not a worker self-test or a completion claim. No
`.stage1-worker-selftest.json` is emitted.
