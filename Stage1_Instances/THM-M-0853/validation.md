# Intake validation

Base revision: `1c0c5fc6f43e6ae5ecc3b50589b45c3628e0ead4`; base tree:
`61214aa2a03c032134ddc4958b1df63df3430a85`.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The new
target-owned dossier and root worker packet make this nonrelease dirty worker evidence.

Validation covers target-set consistency, dossier structure and scope invariants, repository and
bibliographic provenance, a narrow pinned Lean statement-substrate probe, a bounded local candidate
search, prohibited-construct hygiene, and whitespace. It does not validate a canonical statement,
source fidelity, proof, anchor absence outside the bounded search, audit completion, or theorem
completion.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0853` | exit 0; rank 1407, planned, L0/rework_required, no accepted legacy artifacts, theorem_complete false |
| `git status --short --untracked-files=all` | exit 0 at preflight; only the pre-existing automation `.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree shown above |
| `git blame -L 6257,6262 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref `curl` plus exact selected-field `jq` pipeline recorded in `intake-receipt.json` | exit 0; confirmed G. A. Dirac, title, 1952, PLMS series/volume/issue, pages 69-81, DOI; selected one-line JSON SHA-256 including final newline `610a6198...b7b1` |
| zbMATH Open `curl` plus exact selected-field `jq` pipeline recorded in `intake-receipt.json` | exit 0; confirmed record 3073652, author code `dirac.gabriel-andrew`, title, third series volume 2, pages 69-81, year, DOI; selected one-line JSON SHA-256 including final newline `e05434cb...fb5` |
| MathWorld `curl` plus exact scoped `DC.Description` extraction recorded in `intake-receipt.json` | exit 0; secondary source states the conventional simple-graph `n >= 3`, every degree `>= n/2`, Hamiltonian-cycle formulation; normalized one-line statement SHA-256 including final newline `311a4aec...b48e`; no H0 credit |
| publisher full-text endpoint probes | HTTP 403 for the publisher PDF and HTTP 400 for the unauthenticated text-mining endpoint; no article text was admitted, and no source-statement credit is based on these failures |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | exit 0; Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0 with empty output; pinned package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0853/IntakeProbe.lean)` | exit 0; eleven finite-graph/Hamiltonicity interfaces and four candidate proposition shapes elaborated; stdout SHA-256 `b424c7fc...f6bd` |
| bounded `rg` search over pinned mathlib and repo-local Lean, using the exact alternation pattern recorded in `intake-receipt.json` | exit 1 as expected for no match; no graph-theoretic Dirac closure found in that bounded search; not an exhaustive external anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0853-pycache python3 -m py_compile Stage1_Instances/THM-M-0853/check_intake.py` | exit 0; checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0853/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, current pins, null canonical target, H1/M3/R4 boundary, exact artifact inventory, receipt/packet, and six open tasks agree |
| prohibited Lean declaration scan over `Stage1_Instances/THM-M-0853` | exit 1 as expected for no match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0853 .stage1-worker-selftest.json` plus scoped per-new-file byte/no-index checks | exit 0/no diagnostics; all owned files and the worker packet have final newlines, LF endings, and no trailing whitespace |

## Known open gates

The primary article text, proposition pinpoint, incorporated definitions, assumptions, proof
boundary, corrections and errata, translation, and independent source review remain open. So do the
graph/order/degree/rounding/Hamiltonicity decisions; canonical Lean expression and environment
fingerprint; minimal import certificate; checked transports and all four mutation classes;
exhaustive anchor, proof-body, provenance, dependency, axiom and trust audits; obligation/discovery
freezes; typed graphs; proof and composition; readable reconstruction; hermetic replay;
deterministic evidence bundle; independent verification; and master acceptance.

These failures prevent downstream statement, audit, and theorem completion. They do not invalidate
the self-tested `planned` intake, whose only proposed scheduler state is provisional `[_]` pending
master integration.
