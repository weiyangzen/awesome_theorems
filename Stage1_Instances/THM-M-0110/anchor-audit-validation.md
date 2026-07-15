# Anchor-audit validation

Item: `S56-M-0110-ANCHOR_AUDIT`  
Base: `88a5a5c6fe6bac0d813a74ca20fa553eaf2a6d68`  
Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`  
Cutoff: `2026-07-15T20:00:00+08:00`

## Result

The eight-member candidate inventory and two human-source metadata records are
classified. No exact or stronger terminal Lean 4 theorem was found. The
strongest retained formal evidence is `E3`; the root remains
`[H1, M3, R3]`. The literal target's unconstrained semantic labels are the
first integration blocker. This validates the assigned bounded audit node
only; `audit_complete=false` and `theorem_complete=false` refer to the full
theorem assurance decisions.

## Commands

| Working directory | Exact command | Exit | Result |
|---|---|---:|---|
| repository root | `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| repository root | `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| repository root | `python3 scripts/stage1_target.py show THM-M-0110` | 0 | rank 34, planned, legacy unaccepted, theorem incomplete |
| repository root | `git rev-parse HEAD^{commit} HEAD^{tree}` | 0 | base commit/tree above |
| repository root | `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD^{commit} HEAD^{tree}` | 0 | pinned commit/tree above |
| repository root | `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain=v1` | 0 | empty; package source clean |
| `Formalizations/Lean` | `lake env lean ../../Stage1_Instances/THM-M-0110/Statement.lean` | 0 | exact statement, expansion, four mutation rejections, print, and axiom report elaborate |
| `Formalizations/Lean` | `lake env lean ../../Stage1_Instances/THM-M-0110/AnchorAudit.lean` | 0 | exact carrier bridge and retained candidate probes elaborate; only standard axioms reported |
| repository root | `python3 -B Stage1_Instances/THM-M-0110/check_anchor_audit.py` | 0 | DAG, hashes, immutable sources, inventory bijection, receipt, self-test packet, and Lean output reconcile |
| repository root | `python3 -m json.tool Stage1_Instances/THM-M-0110/anchor-discovery-protocol.json >/dev/null` | 0 | valid JSON; audit, receipt, and worker packet pass the same parser separately |
| repository root | `python3 -B Stage1_Instances/THM-M-0110/check_anchor_audit.py` source-hygiene gate | 0 | parser-aware-enough comment stripping plus constructed prohibited-token pattern found no live forbidden construct in `AnchorAudit.lean` |
| repository root | `git diff --check -- Stage1_Instances/THM-M-0110 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Discovery evidence

Pinned-tree negative queries used `git grep` against the immutable mathlib
commit for Kodaira aliases, canonical/dualizing sheaves, Serre duality, ample
line bundles, scheme projectivity, line-bundle interfaces, and module tensor
interfaces. Each terminal-family result list was empty, SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Sourcegraph exact-identifier `KodairaVanishing` and exact-phrase quoted
`Kodaira vanishing` searches,
with archived repositories and forks included, completed with zero matches;
response SHA-256 values are `983ed0f5...` and `6ac099d0...`. The broad query
completed with 16 matches only in Atlas and Physlib and response SHA-256
`e99bfa53...`; every hit is classified in the inventory. Five GitHub
repository-query families completed with zero repositories and canonical JSON
SHA-256 `08c082fd...`. Anonymous GitHub code search returned HTTP 403 due to
the shared-IP rate limit; it is an access failure, not negative evidence.

Crossref and Europe PMC metadata responses bind Kodaira's DOI, PNAS volume,
issue, pages, date, PMID, and PMCID. PMC reports the item is not open access.
Hartshorne's DOI metadata binds the 1977 Springer book. No theorem-text scan is
credited, so source fidelity remains `H1`.

## Boundary

No dependency update, build, fetch, clone, checkout, or `.lake` mutation was
performed. `Formalizations/Lean/.lake` is an automation-provided untracked
symlink, making this nonrelease worker evidence. The receipt is provisional,
accepts no state, and cannot establish H0, M1/M0, full audit completion,
`AUDIT-Z`, validation, release, or theorem completion.
