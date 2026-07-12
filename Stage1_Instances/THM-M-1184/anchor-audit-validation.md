# Anchor-audit validation

Item: `S56-M-1184-ANCHOR_AUDIT`. Base revision:
`68e663d8ce85727d9e1baf107d3b32eb7a434ba8`.

## Result

The frozen local inventory contains useful machine-checked sub-obligations but no exact terminal
candidate for `Stage1Instances.THM_M_1184.KantorovichDualityTarget`. The root is conservatively
`M2`: this is formalization debt, not a discovered-but-unintegrated `M1` result. In particular,
`primalInf_eq_dualSup_of_data` is not a proof candidate: its input package already contains the
reverse inequality. The old ENNReal/nonnegative interface also does not match the frozen signed-real
continuous interface.

## Commands and exact outcomes

All commands ran from the repository root on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Outcome |
|---|---:|---|
| `git rev-parse HEAD` | 0 | `68e663d8ce85727d9e1baf107d3b32eb7a434ba8` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'kantorovich|optimal.transport|transport.*dual|wasserstein.*dual|duality.*transport' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Only unrelated `Translate.ToDual` text matched; no optimal-transport terminal theorem. |
| `rg -n '\\bsorry\\b|\\badmit\\b|^axiom\\b|^unsafe\\b' Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_169.lean Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_151.lean` | 0 | No matches (the command was followed by `|| true`; raw `rg` no-match status is 1). |
| four GitHub repository API queries listed in `anchor-audit.json`, piped to `sha256sum` | 0 | Response hashes: `3bc18b...bf77`, `34e844...4266`, `08c082...600b2`, `34e844...4266`; only the Newton-Kantorovich name collision appeared for Lean. |
| GitHub repository queries for `\"Kantorovich duality\"` and `Kantorovich Lean4` | 0 | Three non-Lean numerical/web projects for the former; zero repositories for the latter. |
| GitHub commit-detail query for the excluded name collision | 0 pipeline status | `curl` itself returned HTTP 403; therefore no immutable external commit claim is made. |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_169.lean` | 0 | The complete historical candidate source elaborated without diagnostics. |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_151.lean` | 0 | The complete adjacent transport source elaborated without diagnostics. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1184/AnchorAudit.lean` | 0 | All five pinned-mathlib adjacent declarations resolved. |
| `python3 -m json.tool Stage1_Instances/THM-M-1184/anchor-audit.json` | 0 | JSON valid. |
| `git diff --check -- Stage1_Instances/THM-M-1184` | 0 | No whitespace errors. |

The `.lake` path is the pre-existing canonical pinned artifact exposed in this worker clone. No
Lake update/build, dependency clone/fetch, or `.lake` mutation was performed.

## Boundary

This is a candidate/provenance audit receipt, not theorem evidence. External discovery was an
unauthenticated, cutoff-scoped repository search and is explicitly not saturation evidence. The
next phase must freeze strong duality, representation/encoding bridges, weak duality, compactness,
and nonemptiness as separate obligations rather than crediting the conditional equality wrapper.
