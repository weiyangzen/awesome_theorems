# Anchor-audit validation

Validation date: 2026-07-12. Base revision:
`20b8abf35019d24fc944d56d6af62cb098711ee3`.

| Working directory | Exact command | Exit | Result |
|---|---|---:|---|
| repository root | `python3 Stage1_Instances/THM-M-0669/check_anchor_audit.py` | 0 | `PASS: 3/3 frozen candidates classified; exact proof candidate absent; M3 retained` |
| `Formalizations/Lean` | `lake env lean ../../Stage1_Instances/THM-M-0669/AnchorAuditProbe.lean` | 0 | all seven pinned supporting declarations elaborated |
| `Formalizations/Lean` | `lake env lean ../../Stage1_Instances/THM-M-0669/Statement.lean` | 0 | canonical target still elaborates; no proof body introduced |
| repository root | `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structural standard passed |
| repository root | `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets passed |
| repository root | `git diff --check -- Stage1_Instances/THM-M-0669` | 0 | no whitespace errors |

Discovery commands included pinned local `rg` searches, GitHub repository API queries, immutable
raw-source reads, and `git ls-remote https://github.com/avigad/qelim.git refs/heads/master`. Exact
query outcomes and response/source hashes are preserved in `anchor-audit.json`; transient `/tmp`
responses are not release artifacts. grep.app requests failed with HTTP 429 and were not used to
support a negative claim. No dependency was fetched, cloned, updated, or written into `.lake`.

Known limitations: the worker input already exposes the canonical `.lake` path as an untracked
symlink; this audit did not create or modify it. Network search is bounded rather than exhaustive,
and primary mathematical source review is outside this phase. These limitations do not change the
fail-closed `M3` decision: usable artifacts exist only at the statement/interface level.
