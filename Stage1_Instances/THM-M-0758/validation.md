# Intake validation

Base revision: `d05520867fab3367a9b61b9544c3e12241204f54` (tree
`fb2cfc62077d5b53e9938632cd6361dd60872067`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, the nonpropositional c.e.-degree
structure-theory boundary, source-statement crosswalk, neighboring-target exclusions, open task
DAG, JSON/scoped invariants, and a narrow pinned Lean API probe. It does not validate a canonical
source statement or proof because no exact theorem, c.e. representation, reducibility, degree
construction, structural conclusion, or binder list has been selected. The automation-provided
canonical `.lake` symlink was pre-existing and used read-only; no dependency update, build, clone,
fetch, or other `.lake` mutation was performed. This dirty worker result is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; its package worktree was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0758` | exit 0; rank 1344, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | pre-edit exit 0; only the automation-provided `Formalizations/Lean/.lake` symlink existed; base revision/tree recorded above |
| inspect and blame the manifest, execution node, repository record, Stage0 projection, neighbors, and pinned mathlib computability sources | exit 0; identified the exact scheduled topic, its catalog-only umbrella gloss, separately owned neighboring results, and adjacent formal substrates without transferring credit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree recorded above; empty package status |
| `sha256sum` over authority files, toolchain/lock, three computability modules, and `docs/references.bib` | exit 0; exact hashes are recorded in `instance.json` and `intake-receipt.json` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0758/IntakeProbe.lean)` | exit 0; ten adjacent pinned c.e.-predicate, Turing-degree, many-one-degree, order, and upper-semilattice APIs plus two prospective shapes elaborated; no target theorem or proof body declared; stdout SHA-256 `411cccb60b25f7b4febb3b277686e5b22f684cfec1c7641fedd67d800adf9ce3` |
| bounded exact-topic search in pinned computability modules and repo-local Lean | exit 0 due to unrelated `source_degree` text; no matching c.e.-degree declaration appeared under the terms; intake discovery only, not a complete anchor audit or global absence claim |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0758-pycache python3 -m py_compile Stage1_Instances/THM-M-0758/check_intake.py` | exit 0; scoped validator compiled without creating generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0758/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; target/DAG identity, null canonical target, H5/M4/R4 boundary, source/formal/neighbor boundaries, exact inventory, source hashes, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0758/check_intake.py` | exit 0; public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over owned Lean files | exit 1 as expected for no match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

Exact immutable theorem selection, complete definition, assumption, conclusion, proof-boundary,
correction/errata and independent source crosswalk, and neighboring-target ownership remain open.
The current `H5` classification also requires an accountable target decision redirecting this item
to a corrected stable proposition before ordinary theorem-proof execution can resume.
So do the c.e. representation, reducibility, degree construction, ordered binders, boundary cases,
canonical Lean expression and environment fingerprints, checked transports, statement mutations,
discovery protocol, obligation registry, typed graphs, formal anchor and provenance audit, proof and
composition, trust closure, readable reconstruction, hermetic replay, deterministic evidence
bundle, independent verification, master acceptance, audit completion, and theorem completion.
These failures do not invalidate a truthful self-tested `planned` intake.
