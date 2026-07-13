# THM-M-0817 intake validation

Base revision: `902d9ce008e88a35a2307c85355560a230cc33c2` (tree
`dfc20d8141f18f6b09a03e818acfff408e836714`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers target-set consistency, the fail-closed planned dossier, source-statement and
non-substitution boundaries, the six-node open task DAG, structured intake invariants, and a narrow
pinned Lean graph-API probe. It does not validate a canonical Ramsey statement or proof: the
catalog does not select among materially different finite, infinite, coloring, graph, and
least-threshold variants. The automation-provided canonical `.lake` symlink was pre-existing and
used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation
was performed. This dirty worker run is nonrelease evidence.

## Source boundary

Crossref metadata identifies F. P. Ramsey, *On a Problem of Formal Logic*, *Proceedings of the
London Mathematical Society* s2-30(1), 264-286 (1930), DOI
`10.1112/plms/s2-30.1.264`; response SHA-256
`410afb38edef7fcb030d18ed242404084650762b49649739ba5e6a1e595973eb`. The
statement-bearing primary article was not obtained, so no exact primary result or proof boundary
was inspected.

The observed DML-CZ PDF of Diana Bergerova, *Game of SIM and Ramsey theory*, SHA-256
`cff253253e87f944092bbbb26f328ce8e330b3e07369750b0c4695ba1fad0e86`, states a
general finite edge-coloring theorem on printed page 14 and an asymmetric two-color Ramsey-number
definition on printed pages 15-16. It confirms the family and demonstrates the variant ambiguity,
but is secondary evidence and supplies no accepted primary crosswalk or independent review.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0817` | 0 | rank 1376; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree match this record |
| `git blame -L 6005,6010 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref DOI API retrieval and deterministic metadata inspection | 0 | author, title, 1930 date, journal, volume/issue, pages, and DOI match; raw response is 2,409 bytes with SHA-256 `410afb38edef7fcb030d18ed242404084650762b49649739ba5e6a1e595973eb` |
| `curl` DML-CZ PDF and metadata; `pdfinfo`; `pdftotext -layout`; scoped inspection | 0 | 7-page, 911,470-byte secondary PDF SHA-256 `cff253253e87f944092bbbb26f328ce8e330b3e07369750b0c4695ba1fad0e86`; text SHA-256 `910c8acafaeac4c50d19e320faecc5597d167eae91249a8916506ebaabbc058c`; printed pages 14-16 crosswalked |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0817/IntakeProbe.lean)` | 0 | eight graph-language APIs elaborated; complete output SHA-256 `4074040d350cd3bb41abb8ad2fb65d34c41c400f486cdc1adba082716c86bc44`; no target theorem or proof body |
| `rg -n -i '\bramsey\b' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | nine unrelated contributor/prose matches; no combinatorial Ramsey terminal declaration; bounded intake discovery only |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 after finalization | all structured artifacts are valid JSON objects |
| Python `ast.parse` on `Stage1_Instances/THM-M-0817/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0817/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 after finalization | target/DAG identity, null target, H1/M4/R4 boundary, pins, inventory, receipt/packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0817` | 1 | expected no-match result; no prohibited declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet, plus `git diff --check` | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |

## Known open gates

- The catalog does not select finite or infinite, symmetric or asymmetric, graph or edge-coloring,
  threshold-existence or least-number scope. Exact parameters, graph/cardinal model, quantifier
  order, size convention, and boundary cases remain open.
- The primary bibliography and a statement-bearing secondary source are pinned, but the primary
  result passage, complete definition/assumption/proof mapping, correction status, and independent
  review remain open.
- No canonical Lean expression, exact minimal imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen. The bounded search located no usable exact
  Ramsey formal artifact.
- Formal anchor and provenance audit, discovery and obligation freezes, typed graphs, proof,
  composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle,
  independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake. Only the integration lane may accept the
provisional worker receipt.
