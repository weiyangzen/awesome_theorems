# Intake validation

Base revision: `35681bf154be61836528486ed7830f619fc03231`; base tree:
`b45fc969fef64ad53ac30dc548894b08e8bef834`.

This validation covers target membership, the planned dossier and six-task open DAG, literal-source
provenance, source-family and neighbor boundaries, JSON and scoped invariants, a narrow pinned Lean
substrate probe, a bounded exact-design-name search, prohibited-construct hygiene, and whitespace.
It does not validate a canonical theorem statement or proof because the catalog does not supply one.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone/fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned files and root worker packet make the final tree dirty and
nonrelease.

## Source discovery boundary

The exact catalog record has SHA-256
`8e9acf9467705a995a1355ecae6499ba515792a2507454d26a5a70dde439b8e3` and contains no citation.
A temporary Crossref query returned metadata for Wilson's 1972 PBD papers I/II and 1975 proof paper
III. The observed 81,724-byte JSON had SHA-256
`b49baca41b082b4b1ecc794080d9218c9d93137bb5599f9d5072badf683b56b2`. It was not added to the
repository. Mutable bibliographic metadata is discovery only: no paper body, theorem statement,
definitions, premise/proof map, correction history, source admission, or H0 review is claimed.

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
| `python3 scripts/stage1_target.py show THM-M-0899` | 0 | rank 1041; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6579,6584 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at the recorded source commit |
| Crossref REST query for Wilson's PBD series using `curl`, then `jq`, `wc`, and `sha256sum` on the temporary response | 0 | parts I/II (1972) and proof part III (1975) identified; response size/hash above; no source admitted |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean version and commit above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake version above; no build/update |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0899/IntakeProbe.lean)` | 0 | five generic APIs elaborated; complete output SHA-256 `2514bbeb6e9ac4190163b459b04953a7ea56ce7f4013c443c905630bb70a797d` |
| bounded exact-design declaration search in repo-local Lean and pinned mathlib | 1 (expected no match) | no exact PBD, BIBD, block-design, Steiner-system, or `TDesign` declaration; intake discovery only |
| bounded `Wilson` search in pinned mathlib | 0 | located only the unrelated factorial/primality theorem plus author strings; name collision excluded |
| `python3 -m json.tool` on the three owned JSON files and root worker packet | 0 | valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0899-pycache python3 -m py_compile Stage1_Instances/THM-M-0899/check_intake.py` | 0 | validator compiled without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0899/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, source/dependency hashes, H5/M4/R4 null-target boundary, inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0899/check_intake.py` | 0 | public replay mode passed without scheduler-only packet |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no proof escape, bodyless declaration, or unsafe declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 1 each (expected new-file difference) | no whitespace diagnostics; each exit 1 is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0899 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; no-index checks cover untracked files |

## Known open gates

- The catalog's arbitrary-`t` gloss and 1972 date are not reconciled with Wilson's PBD/BIBD series
  and its 1975 proof paper. No repository-selected immutable primary source, exact theorem/corollary,
  edition/page, complete premise map, proof boundary, correction/errata decision, or independent
  source review exists.
- Design class, carrier/block representation, simplicity and multiplicity, parameters and binder
  order, admissibility/divisibility conditions, fixed-versus-varying convention, threshold,
  exceptional values, exact conclusion, and boundary cases remain open.
- Overlap with the neighboring general, Kirkman, asymptotic, and Latin-square design targets remains
  open.
- No canonical Lean expression, minimal imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation exists.
- Formal anchor audit, discovery protocol, obligation registry, typed graphs, proof, composition,
  source/provenance/trust closure, readable reconstruction, hermetic replay, deterministic bundle,
  independent verification, release, and master acceptance remain open.

These failures block ordinary statement and theorem execution but do not invalidate a truthful,
self-tested planned intake. Only the integration lane may accept the provisional worker receipt.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0899-INTAKE` only. It supports a planned
dossier and concrete source-identity blocker, not an accepted node. No canonical statement, H0,
proof, audit completion, theorem completion, or master acceptance is claimed.
