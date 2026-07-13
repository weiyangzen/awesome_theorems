# Intake validation

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458`; base tree:
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`. Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, scope and source crosswalks, the
six-node open task DAG, repository-source provenance, structured invariants, and a narrow pinned Lean
candidate probe. It does not validate a canonical closed graph proposition or proof because exact
source assumptions and statement transport remain open.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The final owned files and root worker packet are dirty, nonrelease
evidence.

## Environment

- Linux `7.0.0-27-generic`, x86_64, timezone Asia/Shanghai.
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

All repository commands ran from the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0277` | 0 | rank 1283; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 1992,1997 -- Docs/researches/math_theorems.md` and duplicate lines 2267-2272 | 0 | both identical uncited source records originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded external source request for a Banach 1932 scan | 28 | timed out with no artifact; no moving or inaccessible source was admitted, and the exact human-source gate remains open |
| bounded `rg` over repository and pinned mathlib for closed-graph interfaces | 0 | direct total-map theorem, sequential form, continuous-linear constructors, and partial-operator discriminator located; this was intake discovery, not exhaustive anchor audit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package `status --short` | 0 | pinned revision/tree above; empty status output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0277/IntakeProbe.lean)` | 0 | seven total/partial closed-graph APIs elaborated; the two direct theorem candidates report `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `18ef25189f8f15a3f8418f4ce077a0f6d45185ea07001c00714f87a2e5484cf8` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 for each after finalization | all structured artifacts parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0277-pycache python3 -m py_compile Stage1_Instances/THM-M-0277/check_intake.py` | 0 | checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0277/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 after finalization | target/DAG identity, immutable inputs, H1/M3/R4 null target, exact inventory, candidate probe, receipt/packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0277/check_intake.py` | 0 after finalization | public replay mode passes without the scheduler-only root packet |
| token-anchored prohibited Lean declaration scan over `Stage1_Instances/THM-M-0277` | 1 as expected | no declaration token for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe`; `#print axioms` is an allowed diagnostic |
| per-file `git diff --no-index --check /dev/null` for each owned file and the worker packet, plus scoped `git diff --check` | 0 aggregate/no diagnostics | no whitespace errors; no-index exit 1 was treated only as the expected new-file difference |

## Known open gates

- No immutable pinpoint primary source, exact incorporated definition/assumption map, proof boundary,
  correction or errata audit, source-to-node mapping, or independent H0 review exists.
- Total versus partial domain, Banach/completeness hypotheses, scalar field, product topology, graph
  predicate, continuity/boundedness conclusion, binders, and boundary cases remain open.
- No canonical Lean expression, exact import set, expression/environment fingerprint, checked
  alternate encoding, or four required statement mutations are frozen.
- Exhaustive anchor and terminal-body provenance audit, discovery protocol, obligation registry,
  typed graphs, proof and composition, trust closure, readable reconstruction, hermetic replay,
  deterministic bundle, independent verification, release, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to preserve the sparse source
scope and open work. Only the integration lane may accept the provisional receipt.
