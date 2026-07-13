# Intake validation

Base revision: `2bfb272c83b2089e9b285d48dce2c30616ff6c36` (tree
`f44853226ddecdf2a2b462fd6c85e770bbffbaa3`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers manifest membership, the planned dossier and source/non-substitution
boundaries, the open task DAG, scoped intake invariants, and a narrow pinned Lean API probe. It
does not validate a canonical Burnside proposition or proof because neither is frozen. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no update,
build, clone, fetch, or other `.lake` mutation was performed. The dirty worker run is nonrelease
evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0069` | exit 0; rank 1100, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 512,517 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error https://api.crossref.org/works/10.1112/plms/s2-1.1.388 -o /tmp/burnside-crossref.json` | exit 0; SHA-256 `eb8d4651d702764f7883407e85d9d9da4ed47fc89aafa097c2ce169b2ed38a3b`; W. Burnside, 1904 title, journal, and pages 388-392 located |
| `curl -L --fail --silent --show-error https://api.wiley.com/onlinelibrary/tdm/v1/articles/10.1112%2Fplms%2Fs2-1.1.388 -o /tmp/burnside1904.pdf` | exit 22; HTTP 400, no file admitted |
| `curl -L --fail --silent --show-error https://londmathsoc.onlinelibrary.wiley.com/doi/pdf/10.1112/plms/s2-1.1.388 -o /tmp/burnside1904-wiley.pdf` | exit 22; HTTP 403, no file admitted |
| `git -C Formalizations/Lean/.lake/packages/mathlib grep -in -E 'p.?alpha.?q.?beta\|groups? of order p\|p.?\^.?a.?\*?.?q.?\^.?b' HEAD -- Mathlib` | exit 1; expected no-match result, with no direct p-alpha q-beta solvability declaration located |
| `git -C Formalizations/Lean/.lake/packages/mathlib grep -in -E 'Burnside\|IsSolvable\|IsPGroup\|ker_transferSylow_isComplement' HEAD -- Mathlib/GroupTheory/Solvable.lean Mathlib/GroupTheory/PGroup.lean Mathlib/GroupTheory/Sylow.lean Mathlib/GroupTheory/Transfer.lean Mathlib/GroupTheory/SpecificGroups/ZGroup.lean` | exit 0; 142 adjacent-interface source lines located and then boundedly inspected |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0069/IntakeProbe.lean)` | exit 0; eight adjacent APIs elaborated, and four inspected declarations reported only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each finalized JSON artifact |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0069-pycache python3 -m py_compile Stage1_Instances/THM-M-0069/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0069/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; target/DAG identity, source and pin hashes, H1/M3/R4 null-target boundary, exact inventory, packet agreement, Lean replay, and six open tasks agree |
| `rg -n --glob '*.lean' '(^\|[^A-Za-z])(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)([^A-Za-z]\|$)' Stage1_Instances/THM-M-0069` | exit 1 as expected; no prohibited declaration or proof escape matched |
| `for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-0069/*; do git diff --no-index --check /dev/null "$f" >/tmp/thm-m-0069-diff-check.out 2>&1; rc=$?; if [ "$rc" -gt 1 ]; then cat /tmp/thm-m-0069-diff-check.out; exit "$rc"; fi; done; git diff --check -- Stage1_Instances/THM-M-0069 .stage1-worker-selftest.json` | exit 0; every new file passed the explicit whitespace check, with no tracked-diff diagnostics |

## Known open gates

An accepted source edition and exact theorem passage, complete definition/assumption/errata
crosswalk, independent source review, finiteness encoding, prime distinctness, exponent boundaries,
cardinality formulation, binder order, solvability convention, and checked alternate transports
remain open. So do canonical target elaboration and mutations, exhaustive anchor/provenance/trust
audits, discovery and obligation freezes, typed graphs, proof and composition, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master acceptance,
audit completion, and theorem completion. These open gates do not invalidate a truthful self-tested
`planned` intake.

Schema authority remains an integration boundary: the artifacts use the repository's prevalent
`stage1-instance-intake/1.0`, `stage1-open-task-dag/1.0`, and `stage1-node-receipt/1.0` identifiers
and the scoped checker enforces their intake fields, but no repository-wide published strict-schema
validator was found. This worker does not claim that master schema-acceptance gate.
