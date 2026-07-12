# Anchor audit validation record

Item: `S56-M-1247-ANCHOR_AUDIT`  
Base revision: `950964e64a8a340a562abdc58bb0987c439a6f11`

## Result

The audit is attached to the frozen expression SHA-256 `4697dbba...5c90e`, statement SHA-256
`0fb5f4dd...bf266`, and mathlib revision `8a178386...95`. All Lean sources in the eleven pinned Lake
packages were searched for five Rellich/Hardy-Rellich spellings. No matching dependency source file
or exact terminal declaration was found. Seven concrete mathlib declarations in three substrate
families were then elaborated: the Laplacian/iterated-derivative encoding, compact-support behavior
of derivatives, and one-dimensional compact-support integral identities. None has the weighted
multidimensional inequality or its sharp constant.

Sourcegraph public Lean search returned `matchCount=0`, and GitHub repository search returned zero
repositories with `incomplete_results=false`; their dated responses are content-hashed in
`anchor-audit.json`. GitHub code search was rate-limited, so no global absence claim is made. The
known `abenenson/rellich-kondrachov` project was inspected through the existing repository audit at
immutable commit `85f2c2e9...b60`; its advertised theorem is compactness of an `H1 -> L2` operator,
which is explicitly outside the frozen sharp weighted inequality. It receives no proof credit and
was not fetched or added to `.lake`.

## Commands and results

All commands ran in this worker clone. Lean reused the existing pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | rank 427; planned; theorem incomplete |
| pinned dependency `rg` search for `Rellich`, `Hardy-Rellich`, `HardyRellich`, `Rellich inequality`, and `rellichInequality` | 0 | zero matching Lean files for every term |
| Sourcegraph stream query recorded in `anchor-audit.json` | 0 | `matchCount=0`; response SHA-256 `bf0673c0...d712` |
| GitHub repository query recorded in `anchor-audit.json` | 0 | `total_count=0`, complete response; SHA-256 `08c082fd...2600` |
| GitHub code query recorded in `anchor-audit.json` | non-authoritative failure | API rate limit; limitation preserved rather than treated as a negative search |
| `python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py` | 0 | pins/digests matched; seven anchors in three families elaborated; terminal result open |
| `python3 -m json.tool Stage1_Instances/THM-M-1247/anchor-audit.json >/dev/null` | 0 | valid JSON |
| forbidden proof-token scan over new Lean/Python/JSON artifacts | 1 | no match; ripgrep uses exit 1 for no matches |
| `git diff --check -- Stage1_Instances/THM-M-1247 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This is self-tested anchor-audit evidence pending master acceptance. Root vector remains
`[H1, M3, R3]`. The exact proposition is expressible, but no exact terminal proof candidate or
sufficient bridge entered the verification closure. Human-source acceptance, obligation-tree,
proof, full validation, release, and theorem completion remain open.
