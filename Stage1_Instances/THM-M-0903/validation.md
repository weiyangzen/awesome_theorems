# Intake validation

Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d`; base tree:
`43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`.

This validation covers target membership, the planned dossier and six-task open DAG, literal-source
provenance, primary-source and neighbor boundaries, JSON and scoped invariants, a narrow pinned Lean
substrate probe, a bounded name/text search, prohibited-construct hygiene, and whitespace. It does
not validate a canonical statement or proof because the catalog does not select one exact root.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone/fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned files and root worker packet make the final tree dirty and
nonrelease.

## Source discovery boundary

The repository record excerpt has SHA-256
`d9e1e1e05e4da69ba7a27179d3c34e7ac05183d750e953af5e15c1ec90025702`. The official Cambridge
version-of-record of the matching 1960 Bose-Shrikhande-Parker paper was fetched to a temporary file
and inspected. It is a 15-page, 1,337,286-byte PDF with SHA-256
`cbd6489e0c3f7657a65b75ca4c2e09b3b7c9906919ed2a6b9cdc56bad6925107`. Printed page 190 supplies
the relevant definitions; printed page 202, Theorem 10 supplies the universal `v > 6` result; under
the paper's Eulerian definition restricted to positive `v > 2`, page 203 says 6 is the only
Eulerian number. The temporary source was not added to the
repository.

A Crossref DOI query returned 6,009 bytes with SHA-256
`706ed0be2b21971ede7d51d90a2e6ee05faf52eef92776847d1eb541e9d1c256` and matching bibliographic
metadata. Mutable metadata and temporary inspection are discovery only. No source packet,
catalog-root selection, complete proof-node map, correction/errata audit, or independent H0 review
is claimed.

## Environment fingerprint

- Platform: Linux x86_64; timezone Asia/Shanghai.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`; no update or build was run.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless another
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0903` | 0 | rank 1446; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6607,6612 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at the recorded source commit |
| `curl -L --fail --silent --show-error 'https://api.crossref.org/works/10.4153/CJM-1960-016-5' -o /tmp/thm-m-0903-crossref.json` | 0 | 6,009-byte response; SHA-256 `706ed0be2b21971ede7d51d90a2e6ee05faf52eef92776847d1eb541e9d1c256`; mutable metadata only |
| `curl -L --fail --silent --show-error -A 'Mozilla/5.0' 'https://www.cambridge.org/core/services/aop-cambridge-core/content/view/S0008414X0000986X' -o /tmp/thm-m-0903-source` | 0 | official 15-page, 1,337,286-byte PDF; SHA-256 `cbd6489e0c3f7657a65b75ca4c2e09b3b7c9906919ed2a6b9cdc56bad6925107`; temporary inspection only |
| `pdfinfo /tmp/thm-m-0903-source` | 0 | 15 pages, unencrypted PDF 1.4, 1,337,286 bytes |
| `pdftotext -layout /tmp/thm-m-0903-source /tmp/thm-m-0903-source.txt` | 0 | statement and proof passages became locally inspectable; no OCR text is credited over the visual PDF |
| `sha256sum /tmp/thm-m-0903-source /tmp/thm-m-0903-crossref.json` | 0 | hashes matched those recorded above |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean version and commit above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake version above; no build/update |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0903/IntakeProbe.lean)` | 0 | nine generic finite-matrix, cardinality, bijection, and product expressions elaborated; complete output SHA-256 `0deef5ed9e409b65e0ccfbaf71e0233f3cd94985ff1aeae9e68f8bf6a8cba51a` |
| `rg -n -i 'latin[ _-]?square\|orthogonal[ _-]?latin\|\bBose\b\|\bShrikhande\b\|\bParker\b' Formalizations/Lean Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 (expected no match) | no obvious declaration located; intake discovery only, not a complete external anchor audit |
| `python3 -m json.tool` on the three owned JSON files and root worker packet | 0 | valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0903-pycache python3 -m py_compile Stage1_Instances/THM-M-0903/check_intake.py` | 0 | validator compiled without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0903/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, source/dependency hashes, H1/M4/R4 null-target boundary, inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0903/check_intake.py` | 0 | public replay mode passed without scheduler-only packet |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no proof escape, bodyless declaration, or unsafe declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 1 each (expected new-file difference) | no whitespace diagnostics; each exit 1 is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0903 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; no-index checks cover untracked files |

## Known open gates

- The catalog gloss does not choose literal negation, one counterexample, the congruence family,
  primary Theorem 10, or a complete small-order classification.
- No repository-admitted immutable primary source packet, exact root, complete definition and
  premise map, proof-node boundary, correction/errata audit, or independent source review exists.
- The order domain, binders, Latin-square and orthogonality encodings, at-least-two representation,
  inequalities, congruence form, exceptional cases, and boundary with `THM-M-0902` remain open.
- No canonical Lean expression, minimal imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation exists.
- Formal anchor audit, discovery protocol, obligation registry, typed graphs, proof, composition,
  source/provenance/trust closure, readable reconstruction, hermetic replay, deterministic bundle,
  independent verification, release, and master acceptance remain open.

These failures block ordinary statement and theorem execution but do not invalidate a truthful,
self-tested planned intake. Only the integration lane may accept the provisional worker receipt.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0903-INTAKE` only. It supports a planned
dossier and concrete exact-root blocker, not an accepted node. No canonical statement, H0, proof,
audit completion, theorem completion, or master acceptance is claimed.
