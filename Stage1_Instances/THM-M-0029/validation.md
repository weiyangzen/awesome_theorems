# THM-M-0029 intake validation

Base revision: `936bf2b9e968abd3b79b5b36d32f2f2bff648c7e`; base tree:
`8c9d3261b0ba9a81deb5bfc19a335a02cb80f962`. Validation date: 2026-07-13
(Asia/Shanghai). Exact timestamps are recorded in the provisional receipt.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, theorem-family scope, JSON/scoped invariants, a narrow pinned Lean interface probe,
prohibited-construct hygiene, and whitespace. It does not pass the exact statement, source,
anchor-audit, proof, audit-completion, or theorem-completion gates.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned files and worker packet make this nonrelease evidence.

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

The publisher-hosted PDF of Tadasi Nakayama, *A Remark on Finitely Generated Modules*, Nagoya
Mathematical Journal 3 (1951), pages 139-140, DOI `10.1017/S0027763000012265`, was inspected from
temporary storage; its SHA-256 was
`1a2eeb7d75a2b8373ea8eddfef547714029550b296bda80d65714134cbd36515`.
It contains distinct assertions I-V. Assertion II is a noncommutative right-module radical-
vanishing statement, but the catalog's "about generators" gloss does not select assertion II over
I or a modern generator-lifting form. No immutable archive was added, correction/errata audit or
complete definition/proof crosswalk was performed, and no independent review exists. It supports
`H1`, not `H0`.

## Commands and results

All commands ran at repository root unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0029` | 0 | rank 1074; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 228,233 -- Docs/researches/math_theorems.md` | 0 | all six catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error 'https://doi.org/10.1017/S0027763000012265' -o /tmp/thm-m-0029-doi.html` | 0 | publisher metadata page retrieved; title, author spelling, October 1951 date, volume 3, pages 139-140, DOI, and PDF URL located |
| `curl -L --fail --silent --show-error 'https://www.cambridge.org/core/services/aop-cambridge-core/content/view/8ECAE429F97A64E8F598A39B7E4EA48E/S0027763000012265a.pdf/div-class-title-a-remark-on-finitely-generated-modules-div.pdf' -o /tmp/thm-m-0029-nakayama.pdf` | 0 | publisher-hosted primary candidate retrieved to temporary storage; no repository source archive created |
| `sha256sum /tmp/thm-m-0029-nakayama.pdf` | 0 | `1a2eeb7d75a2b8373ea8eddfef547714029550b296bda80d65714134cbd36515` |
| `pdfinfo /tmp/thm-m-0029-nakayama.pdf` | 0 | 2 pages, 210232 bytes; blank embedded title/author metadata |
| `pdftotext -f 1 -l 2 -layout /tmp/thm-m-0029-nakayama.pdf /tmp/thm-m-0029-nakayama.txt` and scoped `sed` inspection | 0 | assertions I-V inspected; assertion II is right-module radical vanishing; no exact catalog-to-assertion identity or H0 credited |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above; package status clean |
| `sha256sum` on authority, source, toolchain, lock, and two probed mathlib modules | 0 | hashes recorded in `instance.json` and replay-checked by `check_intake.py` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0029/IntakeProbe.lean)` | 0 | eight pinned Nakayama-related interfaces elaborated; no target declaration or proof credit |
| `python3 -m json.tool` on all structured owned files and the root packet | 0 | valid JSON after finalization |
| `python3 -c` with `ast.parse` on `check_intake.py` | 0 | scoped checker parsed without bytecode output |
| `python3 -B Stage1_Instances/THM-M-0029/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, source/dependency hashes, null statement, H1/M3/R4 boundary, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0029/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for each owned file and worker packet | 0 aggregate | no whitespace diagnostics; exit 1 from each no-index invocation was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0029 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; per-file checks cover untracked files |

## Known open gates

Exact source assertion and variant selection, terminology/handedness transport, pinpoint definition
and assumption mapping, corrections/errata audit, proof-node mapping, and independent source review
remain open. So do canonical Lean elaboration and fingerprints, checked transports, four statement
mutation classes, exhaustive anchor and terminal-body audit, discovery protocol, obligation registry
and typed graphs, proof/composition/provenance/trust closure, readable proof reconstruction,
hermetic replay, deterministic release evidence, independent verification, master acceptance,
audit completion, and theorem completion.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0029-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No H0, M0, R0, exact statement, proof, audit completion,
theorem completion, or master acceptance is claimed.
