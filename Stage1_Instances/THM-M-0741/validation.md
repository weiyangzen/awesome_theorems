# Intake validation

Base revision: `0e5ae82e6d507ee607c3f011900571ffd8096800` (tree
`400e6edf1f69b971b60a367e3ea29be359b07907`). Validation date: 2026-07-13
(Asia/Shanghai).

This historical validation covers target membership, the original planned intake dossier, the halting-undecidability scope
boundary, source-statement crosswalk, duplicate-target boundary, open task DAG, JSON/scoped
invariants, and a narrow pinned Lean API/prospective-shape probe. It does not validate a canonical
source statement or proof because the primary passage, machine model, encoding, semantics, and
effective-decider contract have not been frozen. The automation-provided canonical `.lake` symlink
was pre-existing and used read-only; no dependency update, build, clone, fetch, or other `.lake`
mutation was performed. This dirty worker result is nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-0741` | exit 0; rank 1329, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | pre-edit exit 0; only the automation-provided `Formalizations/Lean/.lake` symlink existed; base revision/tree recorded above |
| inspect the target manifest, execution node, repository source, Stage0 projection, `THM-M-0707`, and pinned halting source | exit 0; identified the exact scheduled target, catalog-only claim, same-family duplicate boundary, and fixed-input mathlib candidate without transferring credit |
| `curl -L --fail --silent --show-error --max-time 60 'https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf' -o /tmp/Turing_Paper_1936.pdf` | curl exit 28; request timed out and produced no file, so no primary-source hash, page, or H0 claim was recorded |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree recorded above; empty package status |
| `sha256sum Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/Halting.lean` | exit 0; `c2a073a05c631e7fc957577a66025e9ac36dac741f9aa865e0f053b17f0c85de` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0741/IntakeProbe.lean)` | exit 0; eight pinned APIs and two prospective arbitrary-pair shapes elaborated; no theorem declaration or proof body added; stdout SHA-256 `a4997862a110c81887f9cf5535e9bd2d5afb395118acf2f9e1d9c060aa6cd88e` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0741-pycache python3 -m py_compile Stage1_Instances/THM-M-0741/check_intake.py` | exit 0; scoped validator compiled without creating an owned generated file |
| original intake-time scoped checker | exit 0 at intake; the historical null-target H1/M4/R4 snapshot passed before statement reconciliation |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0741` | exit 1 as expected for no match; no prohibited declaration or proof escape |
| `git diff --check -- Stage1_Instances/THM-M-0741 .stage1-worker-selftest.json` plus per-file `git diff --no-index --check /dev/null <new-file>` | exit 0 for the tracked check; every no-index command found only the expected new-file difference and no whitespace diagnostic |

## Known open gates

This intake snapshot is superseded for current dossier replay by the statement phase. Primary
full-text acquisition, exact proposition locator, complete definition, premise, conclusion,
proof-boundary, correction/errata and translation crosswalk, and independent source review remain
open. Current machine model, effective-decider contract, expression fingerprints, mutations, and
boundaries are recorded in `statement-validation.md`; concrete Turing-machine and fixed/self-input
transports, discovery protocol, obligation registry, typed graphs, formal anchor and provenance
audit, proof and composition, trust closure, readable reconstruction, hermetic replay, deterministic
evidence bundle, independent verification, master acceptance, audit completion, and theorem
completion remain open. These failures do not invalidate the historical truthful `planned` intake.
