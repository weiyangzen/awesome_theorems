# Intake validation

Base revision: `b72c38f3df59ba12e643e0a20be2dd36c063eafc`; base tree:
`4b2126951b48faf4dd3d85dc1e81962ea29a7004`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source-family discrimination, JSON and scoped invariants, a narrow pinned Lean substrate
probe, bounded repository/mathlib search, prohibited-construct hygiene, and whitespace. It does not
validate a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The author-hosted preliminary edition of Gerald Teschl's *Ordinary Differential Equations and
Dynamical Systems* was inspected as a temporary worker input at printed pages 317-318. Section
12.2 separates equation (12.9), Lemma 12.2,
Corollary 12.3, and
Theorem 12.4: return-map definition, orbit/fixed-point stability equivalence, a derivative criterion,
and monodromy-spectrum comparison. The command
`pdftotext -f 328 -l 329 -layout <temporary-source-pdf> <temporary-extract>` produced a 6,781-byte
extract with SHA-256
`990e8a5c8e7c21c1ea9ca08dd57112ba46c1328ccecb5ea75343ab1742969880`; the PDF has SHA-256
`362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e` and size 4,133,331
bytes. No source file was added to the repository. The catalog does not cite this source, and no
immutable source admission, historical attribution audit, complete assumption/errata mapping, or
independent H0 review is claimed.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1351` | 0 | rank 961; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 9852,9857 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `pdftotext -f 328 -l 329 -layout <temporary-source-pdf> <temporary-extract>` | 0 | external worker-input recipe; extracted 6,781 bytes; SHA-256 `990e8a5c...99880` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...85b1d2` and `321626c8...2d81` as recorded in structured artifacts |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1351/IntakeProbe.lean)` | 0 | seven generic adjacent APIs elaborated; complete output SHA-256 `662854a6...bee5` |
| `rg -n -i --glob '*.lean' 'poincar[eé].*map\|return[ _-]*map\|first[ _-]*return' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 0 | found only adjacent references, generic partial-function return maps, and other targets; no source-identical target declaration; intake discovery only |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=<temporary-cache> python3 -m py_compile Stage1_Instances/THM-M-1351/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-1351/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H5/M4/R4 boundary, source hashes, null target, exact artifact inventory, packet agreement, and six open tasks agree |
| `python3 Stage1_Instances/THM-M-1351/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| `rg -n -i 'sorry\|admit\|sorryax\|axiom\|constant\|opaque\|unsafe\|placeholder\|fake result' Stage1_Instances/THM-M-1351 --glob '*.lean'` | 1 (expected no match) | no prohibited construct in the discovery-only Lean probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1351 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked new-file coverage comes from the preceding no-index checks |

## Status boundary

This is provisional worker self-test evidence for `S56-M-1351-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact source selection and independent review,
canonical Lean elaboration and statement mutations, complete anchor audit and discovery freeze,
obligation registry, typed graphs, proof, composition, trust closure, hermetic replay, deterministic
release bundle, and independent verification remain open. These failures prevent statement,
audit-completion, and theorem-completion claims, but they do not invalidate the planned intake.
