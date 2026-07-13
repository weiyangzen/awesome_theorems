# Intake validation

Base revision: `9a1ce196889e32911beeeffa685084b48a969866` (tree
`00d5c1749015f44fb0c5694181253c3a08db5d47`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers manifest membership, the planned dossier and source/non-substitution
boundaries, the open task DAG, scoped intake invariants, and a narrow pinned Lean API probe. It does
not validate a canonical Maschke proposition or proof because neither is frozen. The
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
| `python3 scripts/stage1_target.py show THM-M-0067` | exit 0; rank 1098, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 498,503 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `for doi in 10.1007/BF01448063 10.1007/BF01444297; do curl -fsSL --max-time 30 "https://api.crossref.org/works/$doi" | jq -c '{DOI:.message.DOI,title:.message.title,author:.message.author,container:.message["container-title"],volume:.message.volume,issue:.message.issue,page:.message.page,published:.message.published}'; done` | exit 0; Crossref returned the two 1898 Maschke records, including titles, author, journal, volume/issue, pages, and publication dates; their exact theorem relevance and the catalog's 1899 date remain open |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0067/IntakeProbe.lean)` | exit 0; six relevant APIs and exact candidate instance synthesis elaborated, and all five inspected named declarations reported only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, and `intake-receipt.json` | exit 0 for each |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0067-pycache python3 -m py_compile Stage1_Instances/THM-M-0067/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0067/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, H1/M3/R4 planned boundary, null target, source and pin hashes, receipt packet, exact owned inventory, and six open tasks agree |
| `if rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|\bunsafe\b' Stage1_Instances/THM-M-0067; then exit 1; else echo 'prohibited Lean construct scan: no matches'; fi` | exit 0; the inner `rg` returned the expected no-match status for every prohibited construct |
| `for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-0067/*; do [ -f "$f" ] || continue; rc=0; out=$(git diff --no-index --check /dev/null "$f" 2>&1) || rc=$?; if [ "$rc" -gt 1 ] || [ -n "$out" ]; then printf '%s\n' "$out"; exit 1; fi; done` | exit 0; every new owned file and the worker packet had no whitespace diagnostics; the wrapper treats `git diff --no-index` status 1 as the expected content difference |
| `git diff --check -- Stage1_Instances/THM-M-0067 .stage1-worker-selftest.json` | exit 0; no tracked-diff whitespace diagnostics |

## Known open gates

An accepted source edition and exact theorem passage, complete definition/assumption/errata
crosswalk, independent source review, scalar and dimensionality conventions, finiteness and group-
order encodings, characteristic premise, complete-reducibility meaning, binder order, boundary
cases, and checked alternate transports remain open. So do canonical target elaboration and
mutations, exhaustive anchor/provenance/trust audits, discovery and obligation freezes, typed
graphs, proof and composition credit, readable reconstruction, hermetic replay, deterministic
bundle, independent verification, master acceptance, audit completion, and theorem completion.
These open gates do not invalidate a truthful self-tested `planned` intake.
