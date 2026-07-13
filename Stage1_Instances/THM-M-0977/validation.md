# Intake validation

Base revision: `9c75282d42a7ef447d885d1d56997a79418bcd8a` (tree
`cc5285432a02107fadffb68c698690d1b98ac5f2`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, catalog and duplicate-record
provenance, proposition-changing scope choices, the open task DAG, structured intake invariants,
and a narrow pinned Lean candidate-API probe. It does not validate a canonical Chernoff proposition
or proof because neither has been frozen. The automation-provided canonical `.lake` symlink was
pre-existing and used read-only; no dependency update, build, clone, fetch, or `.lake` mutation was
performed. This dirty worker run is nonrelease evidence.

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

The catalog provides only a theorem-family gloss. A Crossref query confirmed the metadata for a
plausible 1952 Chernoff paper, but the Project Euclid article and PDF endpoints returned
access-control HTML in this environment. No paper text, exact theorem, proof passage, assumptions,
errata, or source-to-catalog map was inspected. The translated duplicate `THM-M-0993` was also
identified. These observations support a provisional `H1` family classification and a concrete
statement/identity blocker, not H0 or root selection.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0977` | 0 | rank 1511; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD` / `git rev-parse 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 7134,7139 -- Docs/researches/math_theorems.md` | 0 | all six target catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git blame -L 7259,7264 -- Docs/researches/math_theorems.md` | 0 | all six translated-duplicate lines originate at the same commit |
| Crossref query for DOI `10.1214/aoms/1177729330` plus `wc`, `sha256sum`, and `jq` inspection | 0 | 1781-byte metadata response, SHA-256 `a48c5f084f838e04637cc2301ef87d08be66d8a05e0ff15dedcb08bbe530b7d6`; author, title, date, volume, issue, pages, and DOI confirmed |
| Project Euclid article and PDF retrieval plus `file`, `wc`, and `pdfinfo` | retrieval 0; PDF identification failed as expected | endpoints returned short access-control HTML rather than article text; no primary statement was credited |
| bounded `rg` search for Chernoff/MGF/CGF declarations in pinned mathlib, repo-local Lean, and `THM-M-0993` | 0 | exact-topic pinned candidates and cross-target wrappers located; no source-mapped THM-M-0977 root credited |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | tool versions recorded above |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0977/IntakeProbe.lean)` | 0 | seven candidate interfaces elaborated; each reported `propext`, `Classical.choice`, and `Quot.sound`; stdout SHA-256 `618599c0352f40ad75934e61ed256b1f31a9db2a7632fa14a5646cbd1db3c47e` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root packet | 0 each | all structured records parsed after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0977-pycache python3 -m py_compile Stage1_Instances/THM-M-0977/check_intake.py` | 0 | scoped validator compiled without generating owned-path cache files |
| `python3 -B Stage1_Instances/THM-M-0977/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | authority identity, null target, duplicate boundary, H1/M3/R4 vector, source/dependency pins, packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token |
| per-file `git diff --no-index --check /dev/null` loop over the nine owned files and root packet | 0 | no whitespace diagnostics; per-file diff status 1 means only that each file is new |
| `git diff --check -- Stage1_Instances/THM-M-0977 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Known open gates

An immutable independently reviewed primary statement and proof locator; complete assumptions,
definitions, corrections, and errata mapping; `THM-M-0977`/`THM-M-0993` identity and allocation;
tail direction, variable family, indexing, parameter, formula, and boundary choices; canonical Lean
expression, environment fingerprint, checked transports, and statement mutations remain open. So do
the exhaustive formal anchor/provenance audit, discovery and obligation freezes, typed graphs,
proof, composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle,
independent verification, release, and master acceptance. These open gates do not invalidate a
truthful self-tested `planned` intake.
