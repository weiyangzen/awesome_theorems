# Anchor audit

Item: `S56-M-1248-ANCHOR_AUDIT`  
Base revision: `96f704c16df75d1a0ba6f21c8d67a3d554a6b5b3`

## Result

The pinned mathlib tree at revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` contains no declaration matching the exact
Caffarelli-Kohn-Nirenberg weighted interpolation target frozen in `Statement.lean`. The source scan
covered the exact author/theorem names and the phrases `weighted Sobolev` and
`weighted interpolation`.

The closest checked mathlib result is
`MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq` in
`Mathlib.Analysis.FunctionalSpaces.SobolevInequality`. It proves an unweighted
Gagliardo-Nirenberg-Sobolev derivative estimate. It does not supply the radial weights, the second
lower-order norm, interpolation exponent `a`, or the CKN admissibility conditions. The checked
`MeasureTheory.MemLp.mul` and
`MeasureTheory.integral_mul_le_Lp_mul_Lq_of_nonneg` declarations are Holder infrastructure, not
terminal candidates. Their types were elaborated in `AnchorAudit.lean`.

Bounded public searches on 2026-07-12 found no external Lean 4 candidate. Five unauthenticated
GitHub repository queries returned zero repositories. Four Sourcegraph queries returned zero
indexed Lean code hits, with forks and archived repositories excluded. GitHub code search was IP
rate-limited and is explicitly not counted as negative evidence. Because no external candidate was
found, there is no external revision to pin or integration task to open. This is not a claim that no
formalization exists anywhere.

The honest classification remains `[H1, M4, R3]` with `formalization_debt`. The anchor audit is
self-tested, but the theorem is not proved and no nearby theorem receives root proof credit.

## Validation

Commands run from the repository root unless the table says otherwise.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 assurance structure accepted |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets accepted |
| `python3 scripts/stage1_target.py show THM-M-1248` | 0 | rank 428; planned; theorem incomplete |
| `rg -ni 'Caffarelli|Kohn.Nirenberg|weighted (interpolation|sobolev)' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | no terminal-name or phrase hit in pinned mathlib; exit 1 means no match |
| `lake env lean ../../Stage1_Instances/THM-M-1248/AnchorAudit.lean` (from `Formalizations/Lean`) | 0 | audit metadata and all three candidate declaration types elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-1248/anchor-audit.json >/dev/null` | 0 | structured receipt parses |
| `git diff --check -- Stage1_Instances/THM-M-1248` | 0 | no whitespace errors |

The GitHub and Sourcegraph query strings and limitations are preserved in `anchor-audit.json`.
Master acceptance remains outstanding.
