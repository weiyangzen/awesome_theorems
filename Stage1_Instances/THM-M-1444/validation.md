# Intake validation

## Validated scope

The validation covers only the `planned` intake artifacts for `S56-M-1444-INTAKE`: manifest and
execution-node identity, source provenance, source-statement boundary, null canonical target,
`H1/M4/R4` provisional classification, exact owned-file inventory, six open downstream tasks, and
elaboration of discovery-only pinned contraction APIs. It checks no canonical theorem declaration
or proof body.

The worker began at repository commit `3815f6945257af057dfb5e6b6dfe2be5b6f451d9`, tree
`21a4f0ff758e83ab68c05b7741cdc4720f95cb1c`. The initial worktree had only the automation-provided
untracked `Formalizations/Lean/.lake` symlink. It points to the canonical pinned artifacts and was
used read-only. No `lake update`, `lake build`, fetch, clone, or dependency mutation was run.

## Environment

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux.
- Lake: `5.0.0-src+98dc76e`.
- mathlib: commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean dependency worktree.
- Contraction source SHA-256:
  `bb620eaf02513b0bbe49e60e93fb6abfd645f5934c7c7dc2ad9c579a1a495b75`.
- Primary-source scan observed during intake: DOI `10.4064/fm-3-1-133-181`, 49 pages. One observed
  download had SHA-256 `87c9b019a592cb2c16755db15e54b0df2a2a43c4769cc0df8aca4d9514b75445`;
  the publisher response may be byte-variable, so the DOI plus printed pages are the source locator
  and the unpreserved one-shot hash is not claimed as immutable content identity.
- Platform: Linux `7.0.0-27-generic`, x86_64. This inherited worker environment is not a clean-room,
  offline replay, or independent release runner.

## Exact commands and results

All commands below ran on 2026-07-13 (Asia/Shanghai). The final receipt and worker packet preserve
the same argv, exit codes, and output summaries.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard structure passed: 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and uniform `L0/rework_required` passed |
| `python3 scripts/stage1_target.py show THM-M-1444` | 0 | rank 1052, planned, score 92, hard-statement lane, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | initial status contained only the pre-existing `.lake` symlink |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base commit and tree matched the values above |
| `git blame -L 10546,10551 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9f...` |
| `curl`/`pdfinfo`/manual page inspection of the publisher scan | 0 | identified Theorem 6 on printed pp.160-161; observed 49-page scan hash above; no scan added to the repository |
| `sha256sum` of normative, source, lock, toolchain, and candidate-module inputs | 0 | hashes recorded in `instance.json` and `intake-receipt.json` |
| `lake env lean --version` (cwd `Formalizations/Lean`) | 0 | Lean version and commit matched the pinned toolchain |
| `lake --version` (cwd `Formalizations/Lean`) | 0 | Lake version above; no dependency action run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib commit/tree matched |
| `lake env lean ../../Stage1_Instances/THM-M-1444/IntakeProbe.lean` (cwd `Formalizations/Lean`) | 0 | eight selected contraction/fixed-point APIs elaborated; no target theorem |
| bounded `rg` searches over repo-local Lean and pinned mathlib | 0 | no source-selected repo-local THM-M-1444 declaration; adjacent pinned candidate family located |
| `python3 -m json.tool` on owned JSON and worker packet | 0 | all JSON parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1444-pycache python3 -m py_compile Stage1_Instances/THM-M-1444/check_intake.py` | 0 | validator compiled without generated owned-path files |
| `python3 -B Stage1_Instances/THM-M-1444/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target, source, hashes, artifacts, task chain, receipt, and worker packet agreed |
| scoped prohibited-construct `rg` scan of `IntakeProbe.lean` | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| no-index whitespace checks for every new file plus `git diff --check` | 0 | no whitespace errors |

## Structured recipes

`S56-M-1444-INTAKE-RECIPE-STRUCTURE` uses repository cwd, argv
`["python3", "-B", "Stage1_Instances/THM-M-1444/check_intake.py", "--worker-packet", ".stage1-worker-selftest.json"]`,
an empty fixed environment allowlist, timeout 30 seconds, denied network, expected exit 0, and covers
only `S56-M-1444-INTAKE`.

`S56-M-1444-INTAKE-RECIPE-LEAN-PROBE` uses cwd `Formalizations/Lean`, argv
`["lake", "env", "lean", "../../Stage1_Instances/THM-M-1444/IntakeProbe.lean"]`, an empty fixed
environment allowlist, timeout 120 seconds, denied network, expected exit 0, and covers only intake
API discovery. It covers no canonical obligation or declaration.

## Known failures and boundary

- The catalog is not binder-complete and supplies no source citation or exact conclusion bundle.
- The inspected source theorem's preceding space axioms, definitions, translation, errata, durable
  archival/license handling, and independent review remain open.
- No modern source has been selected to justify metric generality, uniqueness, convergence, or
  quantitative estimates as root conclusions.
- No canonical Lean expression, minimal import, expression/environment fingerprint, checked
  alternate encoding, or statement mutation exists.
- Formal anchor audit, obligation registry, typed graphs, proof, composition, trust closure,
  readable reconstruction, hermetic replay, deterministic bundle, independent verification,
  release, and master acceptance remain open.

These failures block downstream statement and theorem completion. They do not invalidate a
self-tested `planned` intake that truthfully freezes the source lead, ambiguity, boundaries, and
open DAG. Only the integration lane may accept the provisional receipt.
