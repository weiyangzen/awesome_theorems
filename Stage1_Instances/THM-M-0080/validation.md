# Intake validation

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b` (tree
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, primary-source statement locator, source-statement and
non-substitution boundaries, open task DAG, structured intake invariants, and a narrow pinned Lean
API probe. It does not validate a canonical Lean proposition or proof because the exact formal
encoding and independent source review are not frozen. The automation-provided canonical `.lake`
symlink was pre-existing and used read-only; no dependency update, build, clone, fetch, or other
`.lake` mutation was performed. This dirty worker run is nonrelease evidence.

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

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0080` | 0 | rank 1529, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight contained only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 589,594 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 30 'https://api.crossref.org/works/10.1007/BF01449159' -o /tmp/thm-m-0080-crossref.json` | 0 | Crossref record SHA-256 `10886d4d...a6e8`; title, author, date, journal, volume, and pages agree |
| `curl -L --silent --show-error --max-time 60 'https://manifests.sub.uni-goettingen.de/iiif/presentation/PPN235181684_0109/manifest?version=7a696723' -o /tmp/gdzmanifest` | 0 | GDZ IIIF manifest SHA-256 `1d39f29a...be74`; article range and printed-page canvases located |
| `curl -L --fail --silent --show-error --max-time 120 'https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0109/LOG_0044.pdf' -o /tmp/kurosh-gdz.pdf` | 0 | 15-page PDF, 1,064,413 bytes, SHA-256 `358e2a35...3d44`; external research source, not vendored |
| `curl -L --fail --silent --show-error --max-time 120 'https://gdz.sub.uni-goettingen.de/iiif/image/gdz:PPN235181684_0109:00000655/full/1200,/0/default.jpg' -o /tmp/kurosh-p651-1200.jpg` | 0 | printed-page-651 scan, 1200 by 1865 pixels, SHA-256 `245396c7...1a0d`; theorem headline visually checked |
| `curl -L --fail --silent --show-error --max-time 60 'https://gdz.sub.uni-goettingen.de/fulltext/PPN235181684_0109/00000655.xml' -o /tmp/thm-m-0080-gdz-655.xml` | 0 | page-651 OCR SHA-256 `d7dfc41d...74b6`; transcription checked against scan |
| looped the same GDZ OCR request over suffixes `00000653` through `00000664` (printed pages 649-660), then hashed the filename-plus-content manifest | 0 | OCR manifest SHA-256 `cd65357a...316`; primary statement, arbitrary-family context, footnote, proof span, and bounded correction evidence inspected; H1 pending complete mapping and independent review |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and scoped package status | 0 | pinned revision and tree recorded above; package worktree clean |
| bounded `rg` inspection for Kurosh/Kurosch and free-product subgroup declarations | 0 | no terminal Kurosh declaration found; substantive `CoprodI` and subgroup interfaces plus an unlinked 1000-theorems title found; bounded discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0080/IntakeProbe.lean)` | 0 | twelve pinned free-product, reduced-word, free-group, and subgroup APIs elaborated; stdout SHA-256 `3e17d30f52671e0bc1e325a2d7cd109ab6e0f91cba4704929041f93ca240d50d`; no target or proof body |
| `python3 -m json.tool` on the owned JSON files and root worker packet | 0 | all structured artifacts are valid JSON after finalization |
| `python3 -B Stage1_Instances/THM-M-0080/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, sources, pins, H1/M3/R4 source candidate with null Lean target, inventory, packet, receipt, recipes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0080/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-declaration `rg` on `IntakeProbe.lean` | 1, expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null` plus scoped `git diff --check` | 0 aggregate | no whitespace diagnostics |

## Known open gates

The source headline and arbitrary-family context are located, but independent scan transcription
and German-to-English review, a complete definition/assumption/proof-node and boundary crosswalk,
an expanded correction and erratum audit, and an accountable source review remain open. The exact
Lean encoding must still fix universes, internal versus external free product, component maps,
subgroup and conjugacy carriers, existential factor index, infinite-cyclic predicate, and what
source phrase "can be decomposed" means as a checked equivalence.

Pinned mathlib supplies meaningful `M3` free-product and subgroup infrastructure, but no Kurosh
decomposition declaration was located. Canonical Lean target, minimal imports, expression and
environment fingerprints, checked transports, statement mutations, exhaustive anchor audit,
discovery protocol, obligation registry, typed graphs, proof and composition, trust and provenance
closure, readable reconstruction, hermetic replay, deterministic bundle, independent verification,
master acceptance, audit completion, and theorem completion all remain open.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0080-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No exact Lean statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
