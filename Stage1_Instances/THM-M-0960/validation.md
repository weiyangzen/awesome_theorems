# Intake validation

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a` (tree
`fdfff18dea4c6798c5b322b6088dfe556109c134`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source-statement and version
boundaries, the open task DAG, structured intake invariants, and a narrow pinned Lean API probe. It
does not validate a canonical Ellenberg-Gijswijt proposition or proof because neither has been
frozen. The automation-provided canonical `.lake` symlink was pre-existing and used read-only; no
dependency update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker
run is nonrelease evidence.

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

## Source discovery boundary

The publisher PDF, arXiv v1 PDF, arXiv API metadata, and Crossref metadata were retrieved only to
`/tmp` and were not added to the repository. Publisher Theorem 4 and Corollary 5 and the arXiv
version differences were inspected. A bounded publisher and Crossref audit found no listed erratum,
but absence was not independently certified. This supports an `H1` source lead and exact
source-selection blocker, not H0.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0960` | 0 | rank 1494; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short` (preflight) | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD` / `git rev-parse 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 7008,7013 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 60 -A 'Mozilla/5.0' -sS 'https://annals.math.princeton.edu/wp-content/uploads/annals-v185-n1-p08-p.pdf' -o /tmp/eg-annals.pdf` plus `file`, `wc -c`, `sha256sum`, `pdfinfo`, `pdftotext`, and scoped inspection | 0 each | publisher article, 5 pages and 286382 bytes; SHA-256 `9c54de6e297f0ac678c640def09b3ac8ab960aca05f4059d44e95c9e38b43c8c`; Theorem 4 on printed page 341 and Corollary 5 on 342 inspected |
| `curl -L --fail --max-time 60 -A 'Mozilla/5.0' -sS 'https://arxiv.org/pdf/1605.09223' -o /tmp/eg-paper.pdf` plus the same file/text inspection | 0 each | arXiv v1, 4 pages and 106311 bytes; SHA-256 `3cd77ddab97f046121ef684d68cea9d175b438363ee60b2abe1faa0db05f116b`; material publication differences recorded in the crosswalk |
| `curl` for arXiv API and Crossref metadata plus bounded publisher erratum searches | 0 | version metadata and bibliography confirmed; no publisher-listed erratum located in the recorded search, not a certified absence |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above |
| bounded exact-topic `rg` search for Ellenberg, Gijswijt, cap sets, slice rank, `2.756`, and related terms in pinned mathlib and repo-local Lean | 1 expected before this dossier existed | no exact target declaration found; mathlib's Roth theorem was inspected separately as a non-substitute qualitative result |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0960/IntakeProbe.lean)` | 0 | seven finite-vector-space, cardinality, and progression interface checks elaborated; no target upper-bound theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | 0 each | all structured records parsed after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0960-pycache python3 -m py_compile Stage1_Instances/THM-M-0960/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0960/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest and authoritative-DAG identity, null target, H1/M4/R4 boundary, source and dependency pins, provisional packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 expected | no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| `for f in Stage1_Instances/THM-M-0960/* .stage1-worker-selftest.json; do output=$(git diff --no-index --check /dev/null "$f" 2>&1) || code=$?; test "${code:-0}" -le 1 && test -z "$output" || exit 1; unset code; done` | 0 | no whitespace diagnostics for any new file; `git diff --no-index` returns 1 only because each file is new |
| `git diff --check -- Stage1_Instances/THM-M-0960 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Known open gates

An independently approved immutable source edition and exact root; the complete cap-set,
progression, finite-field, coefficient, monomial-count, degree-cutoff, asymptotic, decimal-constant,
rounding, and boundary conventions; final correction and errata audit; and independent source review
remain open. So do the canonical Lean expression and environment fingerprints, checked transports,
statement mutations, exhaustive formal anchor audit, discovery protocol, obligation registry, typed
graphs, proof and composition, trust and provenance closure, readable reconstruction, hermetic
replay, deterministic bundle, independent verification, master acceptance, audit completion, and
theorem completion. These open gates do not invalidate a truthful self-tested `planned` intake.
