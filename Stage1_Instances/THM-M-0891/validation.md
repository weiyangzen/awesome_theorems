# Intake validation

Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d`; base tree:
`43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`. Validation date: 2026-07-13
(Asia/Shanghai); exact timestamps are recorded in the provisional receipt.

This validates only the `S56-M-0891-INTAKE` planned dossier: target membership, catalog
provenance, primary bibliographic and secondary statement-family boundaries, direction ambiguity,
scope/crosswalk, open task DAG, and adjacent pinned Lean APIs. It does not validate a canonical
Wilf statement, a primary-source proof mapping, or any theorem proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or
other `.lake` mutation was performed. The owned files and root worker packet make the final tree
dirty and nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status was clean before and after the
  probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source discovery boundary

Crossref, OpenAlex, Semantic Scholar, Unpaywall, and publisher routes were queried for DOI
`10.1112/jlms/s1-42.1.330`. They consistently identify Wilf's 1967 three-page article. OpenAlex
and Unpaywall report it closed with no repository full text; the DOI publisher route returned an
access challenge, and Crossref's text-mining endpoint returned HTTP 400. No primary formula or
proof was inferred from metadata.

The versioned secondary source arXiv `2401.03042v2` was inspected. Its printed page 2 reports
`chi(G) <= 1 + lambda_1(G)` and the complete/odd-cycle equality cases, and printed page 12 cites
Wilf. The PDF SHA-256 is
`59e61f62eed77b712aaef5bbebe6a255ba43077cd1ca1ddecb2422aaf23adbbd`.
It corroborates the theorem family but cannot replace primary admission or resolve the catalog's
opposite-looking "lower bound" wording. Consequently the source state remains `H1`.

## Commands and results

All repository commands ran from the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0891` | 0 | rank 1441, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6523,6528 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref/OpenAlex/Semantic Scholar/Unpaywall/publisher inspection for DOI `10.1112/jlms/s1-42.1.330` | 0 aggregate | exact bibliographic family confirmed; lawful primary full text unavailable; closed/access-failure boundary recorded |
| arXiv API and PDF inspection for `2401.03042v2` | 0 | secondary inequality/equality report and Wilf reference inspected; PDF digest recorded above |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean version, platform, and commit recorded above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake version recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree recorded; package status empty before and after validation |
| `sha256sum` on authority, source, toolchain, lock, four pinned mathlib source modules, and secondary PDF | 0 | digests recorded in `instance.json` and provisional receipt |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0891/IntakeProbe.lean)` | 0 | ten adjacent pinned APIs elaborated; complete output SHA-256 `37f180a93211c0fdddfb6f991e24f5e1c079199201822662e286798a9472bf45`; no target statement or proof credit |
| bounded exact-topic `rg` search over repo-local and pinned-mathlib Lean | 0 | only unrelated Fine-Wilf periodicity occurrences found; no spectral-coloring match; intake discovery only, not exhaustive anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | every finalized structured artifact is valid JSON |
| `python3 -c` using `ast.parse` on `check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0891/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, null canonical target, H1/M4/R4 boundary, source/dependency hashes, exact inventory, receipt/packet agreement, and six open tasks agree |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet, plus scoped `git diff --check` | 0 aggregate | no whitespace diagnostics; no-index exit 1 was accepted only for ordinary new-file differences with empty diagnostics |

## Known open gates

Lawful immutable primary-source admission, exact theorem/proof locator, premise and definition
crosswalk, correction or errata audit, independent source review, inequality-direction decision,
equality and connectedness scope, graph model, chromatic-number/coercion/eigenvalue representation,
boundary cases, canonical target and minimal imports, expression/environment fingerprints, checked
transports, and all four statement mutations remain open. So do exhaustive anchor/provenance audit,
discovery protocol, obligation registry, typed graphs, proof and composition, trust closure,
readable reconstruction, hermetic replay, deterministic evidence bundle, independent verification,
master acceptance, audit completion, and theorem completion.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0891-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
