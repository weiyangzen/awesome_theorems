# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers only the planned dossier, scope and non-substitution boundaries, source
crosswalk, six-node open task DAG, structured intake invariants, and a narrow pinned Lean API
probe. It does not validate a canonical BCH proposition or proof because neither has been selected.
The automation-provided canonical `.lake` symlink pre-existed and was used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty inherited worker
environment is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; its package worktree was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1591` | 0 | rank 1212; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight showed only the automation-provided untracked `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base commit and tree recorded above |
| `git blame -L 11721,11726 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error 'https://repository.lib.ncsu.edu/bitstreams/2fac7e12-6b78-403c-af0f-b19a91282a2b/download' -o /tmp/THM-M-1591-ISMS_1959_240.pdf` | 0 | retrieved the temporary primary report scan outside the workspace |
| `sha256sum /tmp/THM-M-1591-ISMS_1959_240.pdf` and `wc -c /tmp/THM-M-1591-ISMS_1959_240.pdf` | 0 | 556,750 bytes; SHA-256 `b3beca1aa6fb6f5d47ab94eded5d0119a794b6761de866964a80aece8a3980d8` |
| `pdfinfo /tmp/THM-M-1591-ISMS_1959_240.pdf` | 0 | 15 pages, unencrypted PDF 1.2; metadata recorded only for source inspection |
| `for p in 4 7 10 11 12; do pdftoppm -f "$p" -l "$p" -png -r 130 -singlefile /tmp/THM-M-1591-ISMS_1959_240.pdf "/tmp/thm1591-p${p}"; done`, followed by visual inspection of the five PNGs | 0 | inspected PDF pages 4, 7, and 10-12 corresponding to printed pp.3, 6, and 9-11; located Lemma 1, Theorem 1, Lemma 2, and Theorem 3; H1 source discrimination only |
| Crossref metadata queries for DOI `10.1016/S0019-9958(60)90287-4` and DOI `10.1016/S0019-9958(60)90870-6` | 0 | authenticated the two Bose-Ray-Chaudhuri journal records; their textual relationship to the 1959 report remains unaudited |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the recorded fingerprint |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1591/IntakeProbe.lean)` | 0 | ten adjacent Hamming, finite-field, polynomial, and root-of-unity APIs elaborated; complete stdout SHA-256 `fe1641879fe7cfc4c9882ea5bafa3c6a308bc194a809f72e944e581918085d5d`; no target declaration or proof body |
| `rg -n -i --glob '*.lean' '\bBCH[ _-]?codes?\b\|Bose.{0,3}(Ray.)?Chaudhuri\|Hocquenghem\|\bcyclic[ _-]?codes?\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | bounded exact-topic search found no BCH or cyclic-code occurrence; empty output SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; not an exhaustive anchor audit |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-1591/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1591/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned H1/M4/R4 boundary, null target, sources, pins, artifacts, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1591/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| `rg -n -i --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-1591` | 1 (expected no match) | no prohibited declaration or placeholder in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1591 .stage1-worker-selftest.json` | 0 | no tracked-diff whitespace diagnostics; the preceding no-index checks cover untracked files |

## Known downstream failures

- The catalog does not select construction/existence, the BCH distance bound, error-correction
  consequence, a dimension estimate, or decoder correctness as its exact proposition.
- The 1959 primary report was inspected and candidate theorem locators are known, but the catalog
  does not select among them. Exact assumption/end-point transcription, journal-version changes,
  errata, complete mapping, lawful preservation, and independent H0 review remain open;
  Hocquenghem's 1959 paper remains an unauthenticated bibliographic lead in this intake.
- Base/extension field, length, primitive/narrow-sense convention, root interval, generator, actual
  and designed distance, correction radius, code and decoder models, binder order, conclusion, and
  every degenerate case remain open.
- No canonical Lean expression, minimal import, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- Formal anchor/discovery audits, obligation registry, typed graphs, proof, composition, trust and
  provenance closure, readable reconstruction, hermetic replay, deterministic bundle, independent
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
