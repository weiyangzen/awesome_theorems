# Intake validation

Base revision: `be8701e88e791545c16a262edd1909486d5cef4b`; base tree:
`78b0a751473bf6d71f453a6aad18b130268a3428`.

This validation covers target membership, the planned dossier and six-node open DAG, catalog and
neighbor boundaries, exact upstream source anchors, non-substitution rules, owned-file invariants,
and a narrow pinned Lean coloring-schema probe. Because the catalog does not select whether its
root is a mathematical proposition, an artifact-closure claim, or their conjunction, no canonical
target, expression hash, mutation result, source acceptance, upstream build, transport, or proof is
claimed.

The automation-provided `Formalizations/Lean/.lake` symlink and its canonical pinned artifacts were
used read-only. No `lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation was
performed. The pre-existing symlink and new target-owned files make this nonrelease worker evidence.

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

## Source boundary

Immutable raw-source inspection located `four_color` in historical mirror revision
`eb30720f9e773fdcbf13dc6c61fdb245587cf401` and maintained release `v1.4.2` at revision
`9990abd7a15f80916c14367ac6dec947a836e60e`. The former states
`forall m : map R, simple_map m -> map_colorable 4 m`; the latter states the corresponding
`simple_map m -> colorable_with 4 m`. Source files and definition files were hashed and are recorded
in `instance.json` and `source-statement-crosswalk.md`.

These are source-discovery observations, not repository dependencies or kernel evidence. No Coq or
Rocq executable, compiled object, dependency closure, or accepted build receipt was present, and no
network dependency was installed. The human publication text, correction history, authoritative
revision genealogy, and independent review remain open. The strongest accepted claim is therefore
neither H0 nor M1/M0.

## Commands and results

All commands ran from the worker clone on 2026-07-13 (Asia/Shanghai), except where a `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0838` | 0 | rank 1395; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD` and `git rev-parse 'HEAD^{tree}'` | 0 each | base revision and tree recorded above |
| `git blame -L 6152,6157 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| repository crosswalk search for `THM-M-0838`, Four Color, Gonthier, and neighboring targets | 0 | artifact-label ambiguity, Four Color identity, Gonthier/2008 attribution, separate generic/computer/RSST targets, and missing catalog definitions confirmed |
| immutable raw retrieval of historical `fourcolor.v`, `realmap.v`, and `combinatorial4ct.v` | 0 | exact `four_color`, supporting definitions, and intermediate `four_color_hypermap` inspected; hashes recorded; no source was added as a dependency |
| immutable raw retrieval of maintained `v1.4.2` README, `fourcolor.v`, `realplane.v`, and `combinatorial4ct.v` | 0 | maintained project identity, final declarations, source model, and intermediate boundary inspected; hashes recorded; no build or pin performed |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; pinned dependency tree remained clean |
| bounded Four Color/planarity search over repo-local Lean and pinned mathlib | 0 | no exact Four Color or source-map declaration located; mathlib coloring documentation lists planar graphs under TODO; bounded discovery only, not a global absence result |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0838/IntakeProbe.lean)` | 0 | three pinned coloring interfaces and the parameterized schema elaborated; 309 stdout bytes, SHA-256 `3b4420d610be9311f05a67ab4618c7d2424e338ddbe6613e10f33ac4c81ecd71`; no target theorem or proof body |
| `python3 -m json.tool` on all structured owned files and `.stage1-worker-selftest.json` | 0 each | valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0838-pycache python3 -m py_compile Stage1_Instances/THM-M-0838/check_intake.py` | 0 | scoped validator compiled outside the owned path |
| `python3 -B Stage1_Instances/THM-M-0838/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, H5/M4/R4 planned boundary, null target, source hashes, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0838/check_intake.py` | 0 | public replay mode passed without requiring the scheduler-only root packet |
| prohibited-construct `rg` over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check`, plus `git diff --check -- Stage1_Instances/THM-M-0838 .stage1-worker-selftest.json` | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file was treated as a difference, not an error |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0838-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted receipt. Root-kind selection, exact source and independent
review, canonical Lean elaboration and mutation tests, upstream integration, exhaustive anchor and
trust audit, discovery and obligation freezes, typed graphs, proof, composition, readable
reconstruction, hermetic replay, deterministic release bundle, independent verification, and
master acceptance remain open. They prevent theorem completion but do not invalidate this intake.
