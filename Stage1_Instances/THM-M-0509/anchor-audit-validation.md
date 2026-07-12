# Anchor-audit validation record

Item: `S56-M-0509-ANCHOR_AUDIT`  
Base revision: `e9d545372b66f73be63271b2fb408ef134d1d6f7`

## Result

The exact repo-local artifact is only the proposition definition
`Stage1Instances.THM_M_0509.ChenTheoremTarget`, not a proof. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies elementary primality, factorization,
prime-factor-list, and smooth-number APIs checked in `AnchorAudit.lean`. A precise alias search of
the pinned source found no Chen-theorem, almost-prime, or semiprime declaration. These APIs are
supporting infrastructure; none proves the uniform `P + P2` conclusion.

No exact external Lean 4 proof candidate was found in the bounded public searches. Sourcegraph and
GitHub repository search returned zero results. GitHub code search returned HTTP 401, so that lane
is recorded as blocked rather than negative. The complete 1204-entry tree of
`google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c` contained no relevant
path. Public query responses are dated and content-hashed discovery evidence, while the mathlib and
Formal Conjectures inspections are bound to immutable commits.

The exact root therefore remains `M4`: there is no proof body to integrate. This completes the
assigned bounded anchor audit pending master acceptance. It does not prove global absence, provide
human-source acceptance, or prove Chen's theorem.

## Commands and results

Commands ran on 2026-07-12 in this worker clone. The Lean checks reused existing pinned `.lake`
artifacts. No dependency update, fetch, clone, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0509` | 0 | rank 883, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0509/AnchorAudit.lean` | 0 | 13 pinned mathlib support declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0509/Statement.lean` | 0 | exact statement and checked transport re-elaborated |
| `python3 Stage1_Instances/THM-M-0509/check_anchor_audit.py` | 0 | audit boundary, inventory, probe coverage, manifest pin, and installed mathlib HEAD agreed |
| precise `rg` alias search in pinned mathlib Lean source | 1 | expected no-match status for Chen-theorem/almost-prime/semiprime aliases |
| Sourcegraph public Lean search | 0 | `matchCount=0`; response SHA-256 `9b88e8ccad6bf516dd2bebec4aa8462f6e18f655bc473f74cc235c9509eff2eb` |
| GitHub REST repository search | 0 | `total_count=0`, `incomplete_results=false`; SHA-256 `08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2` |
| GitHub REST code search | 0 | response captured with HTTP 401 blocker; SHA-256 `b7dbd173f33b19650f61b1c528737e2037cf768d90076fdfce5d32541765e29e` |
| immutable Formal Conjectures recursive-tree inspection | 0 | commit confirmed, `truncated=false`, 1204 entries, no relevant path; SHA-256 `76fa3f96fc2ff7fc85addfd1e85852dae3fcb5022fc1ef35b030a3dc1e3efc61` |
| placeholder/axiom scan of the owned Lean files | 1 | expected no-match status; no `sorry`, `admit`, or line-leading `axiom` |
| `git diff --check -- Stage1_Instances/THM-M-0509` | 0 | no whitespace errors |

## Open integration gate

Integration can reopen only for a concrete repository URL, immutable revision, license, Lean
toolchain, dependency graph, module, declaration, and exact normalized type. Its terminal body must
then pass placeholder, axiom, unsafe/oracle, provenance, and repo-local wrapper checks. Until then,
no `M0-P`, `M1`, audit-completion, or theorem-completion credit is valid.
