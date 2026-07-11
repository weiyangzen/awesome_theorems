# Anchor-audit validation record

Item: `S56-M-0404-ANCHOR_AUDIT`  
Base revision: `8080ef51fed93624a05602e368c1e2187b6fcb02`

## Result

The exact repo-local artifact is only the proposition
`Stage1Instances.THM_M_0404.SkolemMahlerLechTarget`, so it remains `M3` as a statement candidate.
Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies the recurrence object,
solution, uniqueness, solution-space, companion-operator, characteristic-polynomial, and geometric
solution APIs checked in `AnchorAudit.lean`. Neither `Mathlib.Algebra.LinearRecurrence` nor a
repository-wide pinned-source name search contains a terminal Skolem-Mahler-Lech declaration.
Those declarations are support infrastructure and cannot be promoted to an exact wrapper.

No exact external Lean 4 proof candidate was found. The public Sourcegraph name search and GitHub
repository search returned zero results; unauthenticated GitHub code search returned HTTP 401, so
that lane is explicitly blocked rather than reported negative. The complete Git tree of
`google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c` had 1204 entries and
no relevant SML or linear-recurrence-zero path. The public search responses are dated and hashed
query evidence, not immutable proof candidates; the mathlib and Formal Conjectures inspections are
bound to immutable commits.

Consequently the exact root is `M4`: there is no proof body to integrate. This is a completed,
bounded anchor audit, not theorem completion and not a claim that no Lean proof exists anywhere.

## Commands and results

Commands ran on 2026-07-12 inside this worker clone. The Lean commands used only the existing
pinned `.lake` artifacts; no dependency update, fetch, clone, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0404/AnchorAudit.lean` | 0 | Eleven pinned mathlib support declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0404/Statement.lean` | 0 | Exact target and checked statement transport re-elaborated; statement file printed the explicit target expression |
| `python3 Stage1_Instances/THM-M-0404/check_anchor_audit.py` | 0 | Audit schema/status boundary, 11 probes, manifest pin, and installed mathlib HEAD agreed |
| `rg -n -i 'Skolem.?Mahler|Mahler.?Lech|Strassmann|linear recurrence.{0,60}(zero|finite)|zero.{0,60}linear recurrence|eventually periodic' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No match in pinned mathlib source; exit 1 is ripgrep's expected no-match status |
| `curl ... https://sourcegraph.com/.api/search/stream ...` | 0 | `matchCount=0`; response SHA-256 `cfac28415b7bb5fa3f47c3f45457de612723b03b090f54777b2cbda2780ec6cd` |
| `curl ... https://api.github.com/search/repositories?q=%22Skolem-Mahler-Lech%22+lean` | 0 | `total_count=0`, complete response; SHA-256 `08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2` |
| `curl ... https://api.github.com/search/code?q=%22Skolem-Mahler-Lech%22+language%3ALean` | 0 | Request response captured; HTTP 401 authentication blocker; SHA-256 `9afb6c806b49740a42046dbf409c715a3d4da277b495226906a5f3275203c5bf` |
| `curl ... /google-deepmind/formal-conjectures/git/trees/b2e608...?...recursive=1` plus `jq` | 0 | Immutable revision confirmed; complete 1204-entry tree; only unrelated Mahler-measure paths matched broad names; response SHA-256 `76fa3f96fc2ff7fc85addfd1e85852dae3fcb5022fc1ef35b030a3dc1e3efc61` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0404` | 0 | rank 17; planned; legacy artifacts unaccepted; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0404` | 0 | No whitespace errors |

## Open integration gate

Reopen integration only upon locating a repository URL, immutable commit, Lean toolchain,
dependency graph, module, declaration, and exact normalized type. The candidate must then undergo
proof-body, placeholder, axiom, unsafe/oracle, license, and repo-local wrapper checks. Until that
happens, no `M0-P`, `M1`, or theorem-completion credit is valid.
