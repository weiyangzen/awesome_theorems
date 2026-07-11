# Anchor-audit validation

Item: `S56-M-0442-ANCHOR_AUDIT`  
Base revision: `32823ced1a433a51abc96f396ec91970ee6336ac`  
Audit cutoff: 2026-07-12

## Result

The frozen inventory has three classified candidates. The repo-local file is a statement plus
supporting bridges, pinned mathlib supplies only substrate, and the Imperial FLT declaration is an
`axiom` for a weaker cardinality bound. Consequently the exact root remains `M4`. There is no
eligible external proof body to integrate, and no theorem-completion claim is made.

## Immutable external evidence

At FLT commit `1f76653ab824d19fd2475c24ba8c20f06fd9cc1d` (tree
`aff9afa34dcc2786a04d3807efea920b5f9899ba`), raw file
`FLT/Assumptions/Mazur.lean` hashes to
`1849f8b351cc1b2ad3597947779d55a83ac184bea65a7038ef88fbd8d8ba6780`. Its terminal declaration is
literally `axiom Mazur_statement`; it bounds `Set.ncard` by 16 rather than classifying the torsion
group. The pinned FLT toolchain is Lean `v4.30.0-rc2` and its mathlib revision is
`b80f22719410f979c475e9b1d62221ec1dd7a3c6`, distinct from this repository's pinned closure.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0442` | 0 | rank 88; planned; L0/rework-required; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'mazur\|rational.*torsion\|torsion.*rational\|IsMazur' Formalizations/Lean Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'` | 0 | local historical statement/metadata and unrelated name matches; no terminal classification body in the pinned closure |
| `curl -L --fail --silent --show-error https://raw.githubusercontent.com/ImperialCollegeLondon/FLT/1f76653ab824d19fd2475c24ba8c20f06fd9cc1d/FLT/Assumptions/Mazur.lean \| sha256sum` | 0 | `1849f8...6780`; source inspection shows `axiom Mazur_statement` and the weaker `ncard <= 16` type |
| `curl -L --fail --silent --show-error 'https://api.github.com/search/repositories?q=Mazur+theorem+Lean4&per_page=50'` | 0 | `total_count: 0` |
| `curl -L --fail --silent --show-error 'https://grep.app/api/search?q=Mazur_statement&regexp=false'` | 22 | HTTP 429; recorded access limitation |
| `lake env lean ../../Stage1_Instances/THM-M-0442/AnchorAudit.lean` | 0 | pinned mathlib object-model, torsion, congruence-subgroup, and cusp anchors elaborate; exact declarations printed |
| `python3 -m json.tool ../../Stage1_Instances/THM-M-0442/anchor-audit.json >/dev/null` | 0 | structured audit is valid JSON |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)' ../../Stage1_Instances/THM-M-0442` | 1 | no prohibited Lean declaration tokens; exit 1 means no matches |
| `git diff --check -- Stage1_Instances/THM-M-0442 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The existing `.lake` link/worktree is reused read-only. No dependency update, fetch, clone, or build
was run. Public search saturation remains unproved because unauthenticated grep.app code search was
rate-limited; this does not prevent truthful classification of the frozen inventory.
