# Intake validation

Base revision: `997541734bb32f987fb15f163335a82512992120` (tree
`2c866b9d840d48c48ac839740c62d3b9440be0e5`). Validation date: `2026-07-13`
(`Asia/Shanghai`).

Validation is limited to target membership, standard consistency, dossier and all-open DAG
structure, repository source provenance, JSON syntax, pinned dependency identity, a narrow Lean
substrate probe, prohibited-declaration hygiene, and whitespace. The catalog does not determine an
equation, so no canonical target, expression fingerprint, mutation certificate, theorem
declaration, or proof is claimed.

The automation-provided `Formalizations/Lean/.lake` symlink existed before this work and exposes
the canonical pinned artifacts. It was used read-only. No `lake update`, `lake build`, dependency
clone/fetch, or other `.lake` mutation was run. This dirty worker evidence is nonrelease evidence.

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
- Pinned `SimpleGraph/Finite.lean` SHA-256:
  `968b2c58d0e77e91c69815bf1ed5e3fafa7302eaebc08139d9fdbb323ad910e8`.
- Pinned `SimpleGraph/Connectivity/Connected.lean` SHA-256:
  `9171842c49be5f8951c6a2d5c39ae374279d46eaa317efd69bdf3039d289eeff`.

## Commands and results

All commands ran at the repository root unless a `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0810` | 0 | rank 1369; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake` existed; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 5956,5961 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of the catalog, Stage0 projection, target manifest, execution node, and neighboring Euler-named targets | 0 | planar-graph family, absent equation/assumptions, uniform L0 boundary, and explicit exclusions confirmed |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short --untracked-files=all` | 0 | empty output; dependency source remained clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0810/IntakeProbe.lean)` | 0 | six finite simple-graph counting/connectivity APIs elaborated; no embedding, face, target statement, or proof declared |
| bounded `rg` over repo-local Lean outside this target and pinned `Mathlib.Combinatorics.SimpleGraph` | 0 | repo-local results were unrelated uses of "planar"; the pinned `SimpleGraph` result was only a `Coloring.lean` documentation bullet. No target-specific planarity/face/Euler-formula interface was found; intake discovery only, not a complete anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured records valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0810-pycache python3 -m py_compile Stage1_Instances/THM-M-0810/check_intake.py` | 0 | scoped checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0810/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned lifecycle, null target, H5/M4/R4 boundary, immutable inputs, all-open task chain, artifact inventory, receipt, and worker packet agree |
| `python3 -B Stage1_Instances/THM-M-0810/check_intake.py` | 0 | public replay mode passed without the scheduler-only worker packet |
| prohibited Lean declaration scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0810 .stage1-worker-selftest.json` plus a scoped byte check | 0 | no trailing whitespace, invalid bytes, or missing final newline |

The bounded formal search and hygiene commands were:

```bash
rg -n -i '\bplanar\b|plane graph|face count|euler.?s? formula|vertices.*edges.*faces' Formalizations/Lean/AwesomeTheorems --glob '*.lean'
find Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph -type f -name '*.lean' -print0 | xargs -0 rg -n -i '\bplanar\b|plane graph|face count|euler.?s? formula|vertices.*edges.*faces'
rg -n --glob '*.lean' '\b(sorry|admit)\b|\bsorryAx\b|^[[:space:]]*(axiom|constant|opaque|unsafe)\b' Stage1_Instances/THM-M-0810
```

## Status boundary

This is provisional worker self-test evidence for `S56-M-0810-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Pinpoint primary-source selection, exact equation
and scope identity, independent source review, canonical Lean elaboration and mutations, anchor
audit, discovery and obligation freezes, typed graphs, proof and composition, transitive trust,
readable reconstruction, hermetic replay, deterministic release bundle, independent verification,
and master acceptance remain open. These gates prevent audit and theorem completion but do not
invalidate the self-tested planned intake.
