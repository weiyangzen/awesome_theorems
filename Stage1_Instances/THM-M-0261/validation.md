# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, source
provenance and pinpoint discovery, pinned environment identity, a narrow Lean API probe, a bounded
local name search, proof-escape hygiene, JSON integrity, and whitespace. The catalog identifies a
recognizable theorem family, but exact primary-source admission and the definition chain remain
open. Elaborating a purported canonical target in this intake would choose unresolved encodings
prematurely. `IntakeProbe.lean` therefore checks only possible substrate; it introduces no theorem
and supplies no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
Temporary source-discovery downloads were written under `/tmp`, outside the repository. This is
nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0261` | 0 | rank 1269, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD` and `git rev-parse HEAD^{tree}` | 0 | base revision and tree match the values above |
| `git blame -L 1878,1883 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| repository and source crosswalk search for both Mandelbrot-connectedness records | 0 | exact duplicate metadata target `THM-M-1431` found; no identity, evidence, status, or owned artifact was shared or modified |
| `curl -L --fail --silent --show-error --max-time 180 -o /tmp/thm-m-0261-orsay-full.pdf https://pi.math.cornell.edu/~hubbard/OrsayEnglish.pdf`, followed by `sha256sum`, `pdfinfo`, `pdftotext -layout`, and pinpoint `rg` | 0 | hash-identified 178-page PDF SHA-256 `287d476...569d`; Chapter 1 definitions, Chapter 8 Theorem 8.1, Corollary 8.3(a) "The set M is connected," `[DH1]`, and the separate local-connectivity conjecture were inspected; no H0 admission claimed |
| immutable raw-source `curl` for `girving/ray@0ca7b1e746b2911557ac76f56259068cfd1423ab/Ray/Mandelbrot.lean` | 0 | source SHA-256 `f5d04806...3db8`; `mandelbrot`, `mandelbrot_eq_multibrot`, and `isConnected_mandelbrot` identified under another Lean/mathlib pin; source discovery only, not fetched into dependencies, built, or credited as M1 |
| `python3 -m json.tool` over `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| `python3 Stage1_Instances/THM-M-0261/check_intake.py` | 0 | target/DAG identity, H1/M4/R3 planned boundary, null target, duplicate boundary, remote-candidate boundary, empty accepted state, exact artifact inventory, receipt/self-test agreement, and six open tasks agree |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0261-pycache python3 -m py_compile Stage1_Instances/THM-M-0261/check_intake.py` | 0 | intake validator compiles without generated files in the owned path |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake 5.0.0 at the same revision |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0261/IntakeProbe.lean)` | 0 | eleven pinned complex, quadratic-map, iteration, range, boundedness, connectedness, preconnectedness, and compactness API checks elaborated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD`, `HEAD^{tree}`, and package status | 0 | pinned mathlib revision `8a178386...a95`, tree `bdc39a31...c2b`; package status empty |
| `sha256sum` over the target manifest, blueprint, execution DAG, skill, guidelines, repository source, Stage0 projection, Lean toolchain, and Lake manifest | 0 | values agree with the structured environment/source fingerprint |
| bounded exact-topic search under pinned mathlib and repo-local Lean | 0 | only an unrelated Hubbard-and-West ODE bibliography line matched; no queried complex-dynamics declaration was identified; intake discovery only, not a global absence claim |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0261 .stage1-worker-selftest.json` plus owned-file invariants | 0 | no whitespace diagnostics; the scoped validator checks each untracked owned file |

Known downstream failures remain deliberately open: independently accepted primary edition, exact
theorem and definition chain, publication/translation relationship, corrections and errata review;
reconciliation of duplicate `THM-M-1431` without evidence sharing; exact quadratic normalization,
orbit, boundedness/non-escape, parameter-set, topology, and connectedness conventions; canonical
Lean elaboration, expression/environment fingerprints, checked transports, and all statement
mutations; immutable formal anchor audit including the remote candidate; discovery and obligation
freezes; proof and composition; hermetic replay; deterministic evidence bundling; independent
release verification; and master acceptance. These prevent statement or theorem completion but do
not invalidate a truthful, self-tested `planned` intake.
