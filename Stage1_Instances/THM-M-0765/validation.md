# Intake validation

Base revision: `fd0fab2ab7f4f514a5cc625bbce92879e718ba13` (tree
`4116d53bcf2573069e4b67205353fe3469dbe7bd`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, the source-family and neighboring-
topic boundaries, the source-statement crosswalk, the open task DAG, JSON/scoped invariants, and a
narrow pinned Lean API probe. It does not validate a canonical source statement or proof because
the catalog supplies no truth-valued proposition and does not freeze the language, machine,
recognition, or recursive-enumerability conventions. The automation-provided canonical `.lake`
symlink was pre-existing and used read-only; no dependency update, build, clone, fetch, or other
`.lake` mutation was performed. This dirty worker result is nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-0765` | exit 0; rank 1351, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | pre-edit exit 0; only the automation-provided `Formalizations/Lean/.lake` symlink existed; base revision/tree recorded above |
| inspect the target manifest, execution node, repository source, Stage0 projection, neighboring computer-science topic, and pinned computability/Turing sources | exit 0; identified a catalog concept family rather than a proposition, isolated the neighboring topic, and found adjacent formal components without transferring statement or proof credit |
| bounded case-insensitive search for Turing-recognizable/recursively-enumerable language terms in repo-local Lean and pinned mathlib | exit 0 overall; found `REPred` and simulation infrastructure but no explicitly named language-equivalence root; intake discovery only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree recorded above; empty package status |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0765/IntakeProbe.lean)` | exit 0; ten pinned predicate, partial-recursive-code, and TM2-simulation interfaces elaborated; no theorem or proof body declared; stdout SHA-256 `4173c3e8a8b372ef140edd9c38c64cfbbfb47b2e09d24e7bcfdc0bb6b0b5a90b` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0765-pycache python3 -m py_compile Stage1_Instances/THM-M-0765/check_intake.py` | exit 0; scoped validator compiled without creating an owned generated file |
| `python3 -B Stage1_Instances/THM-M-0765/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; target/DAG identity, null canonical target, H5/M4/R4 boundary, neighbor boundary, artifact inventory, source hashes, worker packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0765` | exit 1 as expected for no match; no prohibited declaration or proof escape |
| `git diff --check -- Stage1_Instances/THM-M-0765 .stage1-worker-selftest.json` plus per-file `git diff --no-index --check /dev/null <new-file>` | exit 0 for the tracked check; every no-index command found only the expected new-file difference and no whitespace diagnostic |

## Known open gates

An immutable primary or approved authoritative proposition, incorporated definitions, assumptions,
conclusion, proof boundary, translation, correction/errata disposition, and independent source
review remain open. So do the alphabet and word encoding, machine and program model, execution and
acceptance semantics, recursive-enumerability and enumeration contracts, root direction, ordered
binders, hypotheses, boundary cases, canonical Lean expression and environment fingerprint,
checked transports and mutations, discovery protocol, obligation registry, typed graphs, formal
anchor and provenance audit, proof and composition, trust closure, readable reconstruction,
hermetic replay, deterministic evidence bundle, independent verification, master acceptance,
audit completion, and theorem completion. These failures do not invalidate a truthful self-tested
`planned` intake.
