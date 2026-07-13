# Intake validation

Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7`; base tree:
`018557070da18ea1733a82de81a238750c59aa84`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, primary bibliographic identity and statement-family discrimination, JSON and scoped
invariants, a narrow pinned Lean substrate probe, prohibited-construct hygiene, and whitespace. It
does not validate a canonical theorem statement or proof because source admission and the
general-`h` versus `h = 2` target choice belong to the dependent statement gate.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

Crossref confirmed the 1994 primary article identity, DOI, journal, issue, and pages. Following the
DOI reached a publisher path that returned HTTP 403; the Crossref text-mining PDF endpoint returned
HTTP 400 without content. The article was therefore not retrieved or inspected. The zbMATH Open
record `Zbl 0819.11007` (`id 695039`) supplied a source-close summary of the general `m`-subset-sum
bound, but omitted the admissible `m` range and internal theorem/page locator. This is indexed
summary evidence, not primary proof admission.

Three public scholarly PDFs were inspected outside the repository. Balandraud
arXiv:1702.06419v1, Definition 1 and Theorem 2, and Feher-Nagy arXiv:1610.02539v4, Theorem 3.1,
state the general fixed-cardinality restricted-sumset theorem. Jayasuriya-Reich-Wheeler
arXiv:1210.6509v2, Theorem 2.2 and Remark 2.3, uses the theorem name for the `h = 2`, `A = B`
Erdos-Heilbronn case. Their observed PDF SHA-256 digests are recorded in `instance.json` and the
provisional receipt. These are discovery and scope-discrimination inputs, not an `H0` crosswalk.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64.
- Lean: 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless another
working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0935` | 0 | rank 1474; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 6833,6838 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -fsSL 'https://api.crossref.org/works/10.1112%2Fblms%2F26.2.140' -o /tmp/THM-M-0935-crossref.json`; `sha256sum`; `wc -c` | 0 | dated mutable discovery input: matching primary bibliography; 2,558 bytes; SHA-256 `c839748e...7293`; not a replay-stable validation recipe |
| `curl -IL --max-redirs 8 'https://doi.org/10.1112/blms/26.2.140'` | 0 | DOI redirect observed; terminal publisher response HTTP 403, so no article text was inspected |
| `curl -L 'https://api.wiley.com/onlinelibrary/tdm/v1/articles/10.1112%2Fblms%2F26.2.140' -o /tmp/dias.pdf` | 0 | curl transport completed with HTTP 400 and zero bytes; no primary PDF obtained |
| `curl -fsSL 'https://api.zbmath.org/v1/document/_search?search_string=doi%3A10.1112%2Fblms%2F26.2.140' -o /tmp/THM-M-0935-zbmath.json`; `sha256sum`; `wc -c` | 0 | one matching indexed record with general theorem summary; 3,612 bytes; SHA-256 `17ccea16...6b234`; summary omits `m` range and internal locator |
| download and inspect arXiv:1702.06419v1 with `pdfinfo` and `pdftotext -layout` | 0 | 13 pages, 189,018 bytes, SHA-256 `479d268d...8bf`; Definition 1 and Theorem 2 state the general bound |
| download and inspect arXiv:1610.02539v4 with `pdfinfo` and `pdftotext -layout` | 0 | 26 pages, 369,241 bytes, SHA-256 `2d2d3b70...f59`; Theorem 3.1 states the general bound with `1 <= k <= n` |
| download and inspect arXiv:1210.6509v2 with `pdfinfo` and `pdftotext -layout` | 0 | 17 pages, 198,290 bytes, SHA-256 `fb3e54b8...26c`; Theorem 2.2 and Remark 2.3 identify the `A = B`, `h = 2` usage |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | expected no match | no Dias da Silva-Hamidoune, Erdos-Heilbronn, or exact restricted fixed-cardinality sumset declaration; intake discovery only |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0 and pinned commit/target above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision and tree shown above; package status clean |
| `sha256sum` on authoritative inputs, source records, toolchain, lock, and three probed mathlib modules | 0 | hashes recorded in `instance.json` and provisional receipt |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0935/IntakeProbe.lean)` | 0 | ten adjacent pinned APIs elaborated; complete output SHA-256 `9e94f8b9...6e8b`; no target or proof body |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0935-pycache python3 -m py_compile Stage1_Instances/THM-M-0935/check_intake.py` | 0 | scoped validator compiled without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0935/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and DAG identity, hashes, null target, H1/M4/R4 boundary, artifacts, packet, receipt, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0935/check_intake.py` | 0 | public replay mode passed without the scheduler-only worker packet |
| prohibited Lean construct scan over the owned path | expected no match | no proof escape, bodyless declaration, or unsafe declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0935 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; no-index checks cover all untracked artifacts |

## Known open gates

Primary article retrieval and lawful preservation, exact theorem/page and incorporated-context
transcription, proof and correction/errata audit, independent source review, general-`h` versus
`h = 2` target and neighbor ownership, `h` endpoint and domain conventions, restricted-sumset Lean
encoding, and every boundary case remain open. So do the canonical Lean expression and environment
fingerprints, checked transports, four mutation classes, exhaustive anchor audit and discovery
freeze, obligation registry, typed graphs, proof and composition, provenance and trust closure,
readable reconstruction, hermetic replay, deterministic evidence bundle, independent validation,
master acceptance, audit completion, and theorem completion.

These failures block statement and theorem execution but do not invalidate a truthful self-tested
planned intake.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0935-INTAKE` only. It supports a planned
dossier and exact scope blocker, not an accepted node receipt. No canonical statement, H0, M0, R0,
proof, audit completion, theorem completion, or master acceptance is claimed.
