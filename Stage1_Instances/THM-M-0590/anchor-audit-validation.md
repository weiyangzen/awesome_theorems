# Anchor-audit validation

Item: `S56-M-0590-ANCHOR_AUDIT`  
Base revision: `fe921f79cbbe97438c1012a2a3d06e4f2bf2daf0`

## Result

The exact repo-local artifact is only the proposition definition
`THMM0590.brownDouglasFillmoreTarget`; re-elaboration does not make it a proof candidate. Pinned
mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies the compact-operator closure,
Hilbert-space adjoint, ordinary spectrum, and compact-operator Fredholm-alternative declarations
checked in `AnchorAudit.lean`. A pinned-source search found no Calkin algebra, general Fredholm
predicate/index, essential-spectrum definition, essentially-normal predicate, or BDF theorem.
The Fredholm alternative is about the nonzero spectrum of a compact operator and is not the BDF
classification of essentially normal operators modulo compacts.

No exact external Lean 4 candidate was found in the bounded public searches. Sourcegraph's public
index and GitHub repository search returned zero results. GitHub code search requires
authentication, so that lane is recorded as blocked rather than falsely reported negative. The
complete tree of `google-deepmind/formal-conjectures` at immutable commit
`b2e608fc52d765510915a244bb69b1a2741acc3c` has 1204 entries and no matching path. Search
responses are dated and content-hashed discovery evidence; only inspected Git commits are
immutable revisions.

The root is therefore classified `M4`: no proof body is available to integrate. This completes
the assigned anchor-audit node only. It is not theorem completion and does not claim that no Lean
formalization exists outside the bounded searches.

## Commands and results

Commands ran on 2026-07-12 in this worker clone. Lean used the existing pinned `.lake` artifacts;
no update, build, clone, or fetch command was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0590/AnchorAudit.lean` | 0 | Twelve pinned mathlib support declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0590/Statement.lean` | 0 | Printed `THMM0590.brownDouglasFillmoreTarget.{u_2, u_3} : Prop`; no proof body |
| `rg -n -i 'Brown.?Douglas.?Fillmore|Calkin|essentialSpectrum|essential spectrum|IsFredholm|fredholmIndex|essentiallyNormal|essentially normal|Busby' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No matches in pinned mathlib source; exit 1 is ripgrep's no-match status |
| Sourcegraph streaming API query recorded in `anchor-audit.json` | 0 | `matchCount=0`; response SHA-256 `6faa81834f9a1b38a603a6defc568ead9252a35be2de54e822c63e576f59f424` |
| GitHub REST repository search recorded in `anchor-audit.json` | 0 | `total_count=0`, `incomplete_results=false`; SHA-256 `08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2` |
| GitHub REST code search recorded in `anchor-audit.json` | 0 | Response captured with HTTP 401 authentication blocker; SHA-256 `b7dbd173f33b19650f61b1c528737e2037cf768d90076fdfce5d32541765e29e` |
| GitHub tree API for `formal-conjectures@b2e608fc...`, filtered with `jq` | 0 | Commit matched, `truncated=false`, 1204 paths, zero relevant paths; SHA-256 `76fa3f96fc2ff7fc85addfd1e85852dae3fcb5022fc1ef35b030a3dc1e3efc61` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok` for 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0590` | 0 | Rank 630, planned, statement-first lane, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0590/anchor-audit.json >/dev/null` | 0 | Receipt JSON parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0590` | 0 | No whitespace errors |

## Open integration gate

Reopen only for a repository URL, immutable commit, Lean toolchain, dependency graph, module,
declaration, and exact normalized type. The terminal body must then pass placeholder, axiom,
unsafe/oracle, provenance, license, and local wrapper checks. Until then, no `M0-P`, `M1`, or
theorem-completion credit is valid.
