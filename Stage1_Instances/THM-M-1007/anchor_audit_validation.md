# Anchor-audit validation

Base revision: `32a5ff1576146ad5f0f6ce7cc6ca7ca0c64a48af`. Audit date: 2026-07-12.

The local dependency tree was not fetched or updated. Its checked-out mathlib HEAD is the manifest
pin `8a178386ffc0f5fef0b77738bb5449d50efeea95`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard check passed: 15 groups and 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Manifest check passed: 1546 unique ranked targets. |
| `python3 scripts/stage1_target.py show THM-M-1007` | 0 | Rank 287; planned; L0/rework-required; theorem incomplete. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Exact pinned revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `rg -n -i 'three[-_ ]series|three series|kolmogorov.*series|series.*kolmogorov' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/.lake/packages/mathlib/Archive` | 1 | No terminal name/text candidate in pinned mathlib (`rg` 1 means no match). |
| `rg -n -i 'three[-_ ]series|three series|kolmogorov.*series|series.*kolmogorov' --glob '*.lean' --glob '!Formalizations/Lean/.lake/packages/mathlib/**' . Formalizations/Lean/.lake/packages` | 0 | Only the canonical statement and historical `S1_M_287.lean` appeared; inspection found no terminal theorem. |
| GitHub repository API searches for `"Kolmogorov three-series" lean` and `"three series theorem" Lean` | 0 | Both responses reported `total_count 0`. |
| Sourcegraph global `lang:Lean` searches for the four queries in `anchor_audit.json` | 0 | Each completed with `matchCount 0`; archived repositories and forks were excluded by the public index defaults. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1007/AnchorAudit.lean` | 0 | Pinned Lean checked all six substrate names, measurable truncation, and independence preservation. |
| `python3 -m json.tool Stage1_Instances/THM-M-1007/anchor_audit.json >/dev/null` | 0 | Structured receipt is valid JSON. |
| `rg -n '\bsorry\b|\badmit\b|\baxiom\b' Stage1_Instances/THM-M-1007` | 1 | No forbidden proof shortcuts in the owned artifacts. |
| `git diff --check -- Stage1_Instances/THM-M-1007 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The audit found useful pinned substrate, but no exact terminal candidate. Consequently it records
`formalization_debt`, preserves `M3`, and makes no theorem-completion claim. Public search results
are dated discovery evidence only; because they yielded no candidate, no mutable external branch is
treated as an immutable proof anchor.
