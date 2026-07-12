# Intake validation

Base revision: `dd8846dbc83818f6ba7124151d5d4b7b29bb5b0d` (tree
`1bf3680085cf7338ac4d405cf4ef2188fa14ccec`). Validation ran on 2026-07-12 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants,
repository-source provenance, pinned environment identity, a narrow Lean API probe, a bounded
local name search, proof-escape hygiene, JSON integrity, and whitespace. The catalog identifies the
classical theorem family, but exact source admission and proposition-changing conventions are
still open. Elaborating a purported canonical target in this intake would prematurely choose its
proper-domain, simple-connectedness, equivalence, and normalization encodings.
`IntakeProbe.lean` therefore checks only possible substrate; it introduces no theorem and supplies
no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0227` | 0 | rank 939, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git blame -L 1640,1645 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| repository crosswalk inspection | 0 | catalog and Stage0 supply only the theorem name, attribution/year, short gloss, and untrusted status; no pinpoint source, exact definitions, assumptions, or formal artifact |
| `python3 -m json.tool Stage1_Instances/THM-M-0227/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0227/task-dag.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0227/intake-receipt.json` | 0 | valid JSON after receipt finalization |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | valid JSON after worker-manifest finalization |
| `python3 Stage1_Instances/THM-M-0227/check_intake.py` | 0 | target/DAG identity, H1/M4/R3 planned boundary, null target, empty accepted state, exact artifact inventory, receipt/self-test agreement, and six open tasks agree |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0227-pycache python3 -m py_compile Stage1_Instances/THM-M-0227/check_intake.py` | 0 | intake validator compiles without writing generated files to the owned path |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake 5.0.0 at the same Lean revision |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0227/IntakeProbe.lean)` | 0 | ten pinned unit-disk, openness, simple-connectedness, analyticity, homeomorphism, and conformality API checks elaborated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81`, respectively |
| `rg -n -i '\briemann[ _-]+mapping\b\|riemannmapping\|biholomorph\|biholomorphic\|conformal[ _-]+equivalence.{0,30}(unit\|disc\|disk)' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems --glob '*.lean'` | 1 | expected no-match exit; no exact-topic theorem name found; intake discovery only, not an exhaustive anchor audit or global absence claim |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0227 .stage1-worker-selftest.json` plus untracked-file checks in `check_intake.py` | 0 | no whitespace diagnostics |

Known downstream failures remain deliberately open: independently accepted immutable primary or
authoritative edition, exact theorem and incorporated definitions, assumptions and errata review;
domain nonemptiness/openness/connectedness, properness, planar ambient space, simple-connectedness,
global biholomorphic-equivalence, normalization, uniqueness, and boundary decisions; canonical
Lean elaboration, expression/environment fingerprints, checked transports, and all statement
mutations; immutable formal anchor audit including the uncredited RMT4 lead; discovery and
obligation freezes; proof and composition; hermetic replay; deterministic evidence bundling;
independent release verification; and master acceptance. These prevent statement or theorem
completion but do not invalidate a truthful, self-tested `planned` intake.
