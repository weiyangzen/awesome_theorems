# Anchor-audit validation record

Item: `S56-M-1148-ANCHOR_AUDIT`  
Base revision: `915e3cad7d9f0c51622da7a7ab548cdacd00db77`

## Result

The exact local artifact is the frozen proposition only. Pinned mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95` contains four especially close Poisson/Herglotz-Riesz
identities. The two Poisson-kernel declarations were checked in Lean and their source bodies were
inspected: each rewrites to its Herglotz-Riesz counterpart. They assume either
`HarmonicOnNhd f (closedBall c R)` or `HarmonicContOnCl f (ball c R)` and conclude the integral
identity for that same `f`. The frozen root instead starts with arbitrary continuous boundary data
`g` and must produce `u`, harmonicity, closure continuity, boundary trace, and the formula. Thus the
mathlib candidates are genuine support but not an exact theorem or a legal wrapper.

The legacy `S1_M_144.lean` artifact repeats the exact existential shape as a proposition definition
and provides only an introduction wrapper whose premise is the whole claim. It has no terminal proof
body. Bounded public searches discovered no other candidate. Sourcegraph and GitHub repository
responses were content-hashed; GitHub code search (HTTP 401) and grep.app (HTTP 429) were blocked and
are not reported as negative results.

The root therefore remains `M4` with `formalization_debt`. There is no discovered external closure
to create `repo_local_integration_debt`. The concrete missing bridge is Poisson-integral construction,
harmonicity, continuity on the closed disk, and convergence to arbitrary continuous boundary data.
This completes only the bounded anchor-audit phase; it is not theorem completion or H0 evidence.

## Commands and results

Commands ran on 2026-07-12 inside this worker clone. Lean used only the existing pinned `.lake`
closure. No update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1148/AnchorAudit.lean` | 0 | six declarations and two typed probes elaborated; both retained Poisson declarations reported axioms `[propext, Classical.choice, Quot.sound]` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1148/Statement.lean` | 0 | exact frozen target and mutations re-elaborated |
| `python3 Stage1_Instances/THM-M-1148/check_anchor_audit.py` | 0 | structured boundary, four anchors, manifest pin, and installed mathlib HEAD agreed |
| `git -C Formalizations/Lean/.lake/packages/mathlib grep -n -i -E 'poisson\|dirichlet' -- 'Mathlib/**/*.lean'` | 0 | relevant mathlib hits were confined to representation formulas; unrelated Poisson summation and Dirichlet-named theories were excluded |
| `curl -G https://sourcegraph.com/.api/search/stream --data-urlencode 'q=context:global archived:yes fork:yes lang:Lean ("circleAverage_poissonKernel_smul" OR "poissonKernel c w") count:100'` | 0 | `matchCount=0`; response SHA-256 `8840775e5302f9e8056468ec83b4a6a7b6ff5c1eb3dac952fdbd0536ddccf5ad` |
| `curl ... 'https://api.github.com/search/repositories?q=%22Poisson+integral%22+Lean+theorem+prover&per_page=20'` | 0 | `total_count=0`, `incomplete_results=false`; response SHA-256 `08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2` |
| GitHub REST code search for `poissonKernel language:Lean` | 22 | HTTP 401 authentication blocker; no result claimed |
| grep.app API search for `poissonKernel`, Lean filter | 22 | HTTP 429 rate-limit blocker; no result claimed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1148` | 0 | rank 353, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1148 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Reopen the machine-integration question only with a concrete repository URL, immutable commit,
toolchain, module, declaration, exact-type comparison or checked transport, terminal-body provenance,
license, and successful local wrapper check.
