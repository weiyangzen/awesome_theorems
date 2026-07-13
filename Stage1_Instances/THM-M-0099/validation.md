# Intake validation

Base revision: `771d5d4800fbd95eaaa343e9bc55ebfdde20b364` (tree
`a98ba0c37e56a7c04256f7d7df305c88e5cbe76e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and duplicate-ownership boundaries,
open task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does not
validate a canonical Fundamental Lemma proposition or proof because neither has been frozen. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-0099` | exit 0; rank 1115, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 726,731 -- Docs/researches/math_theorems.md` | exit 0; all six sparse catalog fields originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| versioned arXiv `0801.0446v3` PDF inspection | exit 0; SHA-256 `4d48819f7ecf7e4e1d0fd036df2a62fa5b49f171f6fda56449b3dfbc0d43fb51`; introductory Theorem 1, local Theorem 1.11.1, and the characteristic boundary located; H1 source lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded exact-topic `rg` search in pinned mathlib | exit 0; only unrelated homotopical-algebra and Selberg-sieve text matched; no endoscopic Fundamental Lemma target located |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0099/IntakeProbe.lean)` | exit 0; the three adjacent local-field, scheme, and Haar-measure APIs elaborated; stdout SHA-256 `6301409cbcad14585946ce70a8fdee223e07d8322d672e5090ba652b0391136f`; no canonical target or proof was declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0099-pycache python3 -m py_compile Stage1_Instances/THM-M-0099/check_intake.py` | exit 0; the scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0099/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, pins, null target, H1/M4/R4 boundary, duplicate and source boundaries, provisional receipt, packet, and six open tasks agree |
| `rg -n '\\b(sorry\\|admit\\|sorryAx\\|axiom\\|constant\\|opaque\\|unsafe)\\b' Stage1_Instances/THM-M-0099 --glob '*.lean'` | exit 1 as expected; no prohibited Lean declaration or placeholder found |
| `git diff --check -- Stage1_Instances/THM-M-0099 .stage1-worker-selftest.json` plus per-new-file `git diff --no-index --check /dev/null` | exit 0 for the tracked check; each no-index check returned expected new-file difference exit 1 with no whitespace diagnostics |

## Known open gates

Master duplicate-target resolution, accepted source preservation, exact source proposition and
definition chain, normalization and characteristic transports, errata audit, independent source
review, canonical Lean expression and environment fingerprint, checked alternate encodings,
statement mutations, exhaustive formal anchor audit, discovery protocol, obligation registry,
typed graphs, proof and composition, trust and provenance closure, readable reconstruction,
hermetic replay, deterministic bundle, independent verification, master acceptance, audit
completion, and theorem completion remain open. These gates do not invalidate a truthful
self-tested `planned` intake.
