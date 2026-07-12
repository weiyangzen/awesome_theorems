# Anchor-audit validation

Item: `S56-M-0729-ANCHOR_AUDIT`  
Base revision: `91055abb3f5bee7f79323bc9cbefa7f2a8145f1f`  
Audit date: 2026-07-12 (`Asia/Shanghai`)

## Result

The repository-local exact artifact is the elaborated proposition definition
`Stage1Instances.THM_M_0729.PCPTheorem`, not a theorem with a PCP proof body. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies deterministic Turing machines,
polynomial-time computation witnesses, natural logarithms, and finite-cardinality APIs. The seven
retained probes elaborate, but none defines NP or PCP, supplies randomized proof-oracle verifier
semantics, or proves either class inclusion.

No exact external Lean 4 proof candidate was found by the bounded public searches. Sourcegraph's
Lean alias query completed with zero matches, and three GitHub repository searches completed with
zero results. GitHub code search required authentication, so that lane is recorded as a blocker,
not a negative result. The complete 1204-entry tree of
`google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c` had no matching
path. Search responses are dated and content-hashed discovery evidence; they are not proof of
global absence.

The exact root therefore remains `M3`: the statement and genuine low-level interfaces exist, but
no terminal PCP proof body was located. This self-tests the bounded anchor-audit node only and
supplies no proof, human-source fidelity, full-audit, or theorem-completion credit.

## Commands and results

Commands ran inside this worker clone. Existing pinned `.lake` artifacts were used read only; no
update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | rank 766, planned, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0729/Statement.lean` | 0 | exact canonical statement and transport re-elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0729/AnchorAudit.lean` | 0 | seven pinned supporting declarations elaborated |
| `python3 Stage1_Instances/THM-M-0729/check_anchor_audit.py` | 0 | immutable pins and hashes agreed; no exact root claimed; root `M3` |
| scoped `rg` over repo-local and all pinned dependency Lean sources | 1 | expected no-match exit outside the local exact statement; no named terminal PCP candidate found |
| Sourcegraph public Lean alias query | 0 | `matchCount=0`; response SHA-256 `c377c9...ad75` |
| three GitHub REST repository searches | 0 | each `total_count=0`, `incomplete_results=false`; response SHA-256 `08c082...2600b2` |
| GitHub REST code search | 0 | response captured: HTTP 401 authentication blocker; SHA-256 `b7dbd1...5e29e` |
| GitHub immutable recursive-tree inspection of `formal-conjectures@b2e608...` | 0 | non-truncated 1204-entry tree, no matching path; response SHA-256 `76fa3f...efc61` |
| `python3 -m json.tool Stage1_Instances/THM-M-0729/anchor-audit.json >/dev/null` | 0 | structured audit is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0729 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open integration gate

Reopen integration only for a candidate with an immutable revision, exact declaration and type
mapping, compatible toolchain and dependency graph, license, terminal-body provenance, placeholder
and axiom audit, and a successful repo-local wrapper check. Until then no `M0-P`, `M1`, audit
completion, or theorem-completion credit is valid.
