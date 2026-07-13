# Intake validation

Validation date: `2026-07-13` (`Asia/Shanghai`). Base revision:
`adc87f8ea24dcc7c5e2668c0a5ede0ca5c5f0f55`.

This validates target membership, the planned dossier and open task DAG, repository and dependency
pins, official historical archive metadata, JSON and cross-file invariants, and a narrow exact-type
probe against existing pinned mathlib. The pre-existing canonical `.lake` link and artifacts were
used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was run.

The Lean probe establishes only that the named Turán candidate definitions and theorems elaborate
in the pinned environment. It does not choose the canonical source variant, serialize its target
expression, run statement mutations, audit terminal proof bodies or axioms, or grant proof credit.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0816` | exit 0; rank 1375, planned, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` link existed before the intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base commit `adc87f8ea24dcc7c5e2668c0a5ede0ca5c5f0f55`, tree `3c83596059f716cde0d50a5f6b390ada6ca7c8e1` |
| `git blame -L 5998,6003 -- Docs/researches/math_theorems.md` | exit 0; all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl` of official REAL-J OAI `GetRecord` metadata for `oai:real-j.mtak.hu:7297` to `/tmp` | exit 0; 4,323-byte OAI record, SHA-256 `c21ee6cc0cd65e9648d54be1405bc53ef422328559b992332b1ca9b4f7ea2bed`, identifies volume 48 (1941) and Turán's article title |
| `curl` of the official REAL-J EPrints XML export for record `7297` to `/tmp` | exit 0; 4,295-byte export, SHA-256 `c20bed70362f84e709e1dba521d0dbea66838815cbf0986af752e40a758b997a`, reports a public 320,878,611-byte volume scan, MD5 `ce19dc2521b25d59df7c793146b70c56`, and the Turán contents entry; article text was not incorporated, so no H0 |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake 5.0.0-src+98dc76e |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0816/IntakeProbe.lean)` | exit 0; exact types for Turán maximality, graph construction, clique-freeness, uniqueness, exact edge formula, upper bound, and extremal-number candidates elaborated |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0816-pycache python3 -m py_compile Stage1_Instances/THM-M-0816/check_intake.py` | exit 0; validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0816/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest/DAG identity, H1/M3/R4 boundary, source and mathlib pins, exact artifact inventory, receipt/packet, and six open tasks agree |
| prohibited Lean construct scan over the owned probe | exit 1 as expected for no match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped per-new-file whitespace checks and `git diff --check` | exit 0; no whitespace errors |

## Known open gates

The exact proposition and proof in the 1941 article, article-page snapshot, corrections or errata,
independent source review, forbidden clique parameter, and choice among inequality, exact value,
equality, uniqueness, and extremal-number roots remain open. So do the normalized canonical Lean
expression and environment fingerprint, checked transports, all four mutation classes, exhaustive
anchor and proof-body provenance audit, obligation and discovery freezes, typed graphs,
proof/composition and trust evidence, readable reconstruction, hermetic replay, deterministic
bundle, independent verification, and master acceptance. These boundaries prevent audit and
theorem completion but do not invalidate a truthful self-tested `planned` intake.
