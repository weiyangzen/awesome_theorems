# THM-M-1537 proof attempt

Item: `S56-M-1537-PROOF`  
Date: `2026-07-12`  
Base revision: `d8e739d08e6a4c17f08c309bafac6637d21620bb`

## Verdict

`blocked`: the exact frozen target is false, not merely unsupported. The
structure `SemiclassicalBlackHole` stores `thermodynamicEntropy` independently
of area and the four constants. Its three regime markers and positivity
premises add no relation between those fields.

The frozen obligation-tree source supplies an admissible instance with area
zero, entropy one, all constants one, and all regime propositions true.
`not_bekensteinHawkingAreaLaw` is a placeholder-free kernel-checked proof of
`Not BekensteinHawkingAreaLaw`: all hypotheses hold, but `entropyFromArea` is
zero. Thus no Lean proof body for the canonical root can exist in the current
consistent environment.

The only open machine cut is `M1537-B-PHYSICS`. It cannot be inhabited from the
frozen premises, since `AreaLawBridge` is definitionally the same universal
claim as the root. The historical `S1_M_200` wrappers consume records or
hypotheses that already include an area-law relation and therefore cannot be
transported without adding the missing conclusion as an assumption. The
pinned mathlib and audited external Physlib candidate contain no terminal
black-hole area-law result.

No proof source, axiom, placeholder, unsafe declaration, weakened statement,
or unpinned dependency was added. Because the assigned proof phase is not
self-tested complete, this attempt deliberately does not create
`.stage1-worker-selftest.json`.

## Narrow validation evidence

All commands ran from the worker clone on `2026-07-12`. The pre-existing
untracked `Formalizations/Lean/.lake` symlink points to the canonical pinned
artifacts; it was reused but not modified. No update, build, clone, fetch, or
dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard passes: 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passes: 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1537` | 0 | Rank 200, planned, hard-mathlib-anchor lane, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1537/check_obligation_tree.py` | 0 | Nine obligations and 16 typed edges pass; the exact root is refuted and remains M5. |
| scoped copies under `Formalizations/Lean`, then `lake env lean -o <temp>/Statement.olean <temp>/Statement.lean` and `LEAN_PATH=<temp>:$(lake env printenv LEAN_PATH) lake env lean <temp>/ObligationTree.lean` | 0 | Exact statement, conditional composition, and countermodel refutation elaborate with pinned Lean 4.29.0; both printed declarations use only `propext`, `Classical.choice`, and `Quot.sound`. Temporary files were removed. |
| `rg -n -i 'BekensteinHawkingAreaLaw\|AreaLawBridge\|Bekenstein\|Hawking\|horizonArea\|black[- ]?hole entropy' --glob '*.lean' Stage1_Instances/THM-M-1537 Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | Finds the frozen dossier and historical assumption-carrying wrappers, but no proof of the exact unconstrained target in the pinned closure. |
| `rg -n '^\\s*(sorry\|admit\|axiom)(\\s\|$)\|sorryAx\|unsafe' Stage1_Instances/THM-M-1537 -g '*.lean'` | 1 | No prohibited Lean declaration token found; exit 1 means no match. |

The first failed gate is the substantive physics bridge
`M1537-B-PHYSICS`. Unblocking requires an authorized correction of the model
or theorem statement to encode a genuine entropy-area premise or derivation,
then rerunning all upstream gates. It cannot be repaired during this proof
phase without changing or assuming the theorem.
