# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source-family and neighboring-target discrimination, JSON and scoped invariants, a
narrow pinned Lean substrate probe, prohibited-construct hygiene, and whitespace. It does not
validate a canonical theorem statement or proof because the catalog supplies no stable truth-valued
proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source boundary

The repository source at `Docs/researches/math_theorems.md:10034-10039` contains only the label,
collective attribution, date, broad necessary-condition gloss, importance, and untrusted status.
All six lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; they contain no
theorem-bearing citation. No external source was fetched or admitted during this intake. Primary-
source edition, theorem/page, incorporated assumptions, proof boundary, errata, historical scope,
and independent review remain open.

## Environment fingerprint

- Platform: Linux x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned `Mathlib/Analysis/Calculus/LocalExtr/Basic.lean` SHA-256:
  `e61dea1ac1ab31e7c1c2e60d273a3605c868b7bc45177542655eb039b6d0c116`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1377` | 0 | rank 987; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 10034,10039 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; package source clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1377/IntakeProbe.lean)` | 0 | six generic local-extremum and derivative APIs elaborated; complete output SHA-256 `692f59a579b5b798d94f78d0e08a8fc0225da40d797833f10bba1d4e9d8e07b9`; no target theorem declared |
| bounded pinned-mathlib search for `calculus of variations`, `first variation`, or `Euler-Lagrange` in Lean sources | 1 | expected no match; intake discovery only, not a complete formal-candidate audit |
| bounded repo-local Lean search for the same terms | 0 | found neighboring legacy Tonelli, least-action, mechanics, and Yang-Mills planning surfaces; none supplies source-identical evidence for this target |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | 0 for each | valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-1377/check_intake.py` | 0 | scoped validator parsed without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1377/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest and authoritative-DAG identity, null target, H5/M4/R4 boundary, source pins, exact artifact inventory, receipt/worker packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 | expected no match for prohibited declarations or proof shortcuts |
| scoped per-new-file whitespace checks plus `git diff --check` | 0 | no whitespace errors |

## Known open gates

An exact source-selected proposition, immutable theorem-bearing source, incorporated-definition and
assumption mapping, proof and errata boundary, independent source review, and neighboring-target
decision remain open. So do the canonical Lean expression and environment fingerprints, checked
transports, statement mutations, exhaustive formal anchor audit, discovery protocol, obligation
registry, typed graphs, proof and composition, trust and provenance closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These failures do not invalidate a truthful
self-tested `planned` intake.
