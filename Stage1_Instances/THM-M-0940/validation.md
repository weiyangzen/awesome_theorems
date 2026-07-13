# Intake validation

Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7` (tree
`018557070da18ea1733a82de81a238750c59aa84`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers target membership, the planned dossier and all-open task DAG, literal repository
provenance, target-identity discrimination, JSON and scoped invariants, and a narrow pinned Lean API
probe. It does not validate a canonical additive-combinatorics statement or proof because the
catalog does not select one. The automation-provided canonical `.lake` symlink was pre-existing and
used read-only. No `lake update`, `lake build`, dependency clone or fetch, network-triggering Lake
operation, or other `.lake` mutation was performed. This dirty worker evidence is nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean before and after the probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source discovery boundary

The repository record contains no bibliography, and all six catalog lines originate at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. A repository-wide exact-title search found no other
source or Lean target. On 2026-07-13, an exact-title arXiv API query returned zero results; a
Crossref title query returned general additive-combinatorics books and unrelated works rather than
a uniquely named theorem; and a DuckDuckGo HTML query timed out. These mutable bounded searches are
discovery inputs only. They neither prove global absence nor replace target correction and primary-
source review.

Pinned mathlib contains several exact neighboring declarations, but they have mutually different
contracts. The probe checks seven representative signatures without selecting one. A bounded exact-
phrase search over repo-local Lean and pinned mathlib found no declaration named for the generic
catalog title. This is not the downstream exhaustive formal-anchor audit.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0940` | 0 | rank 1479; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6868,6873 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| exact catalog, Stage0, and manifest excerpt hashing plus whole-input `sha256sum` | 0 | hashes bound in `instance.json` and `intake-receipt.json` |
| `curl -L --fail --silent --show-error --max-time 30 'https://export.arxiv.org/api/query?search_query=all:%22fundamental%20theorem%20of%20additive%20combinatorics%22&start=0&max_results=10'` | 0 | 780-byte dated mutable response; `totalResults=0`; SHA-256 `d176983c769a3030dd80f575bb986e6648da6aa3de204fbfdbfb8ca23b53e6c0` |
| `curl -L --fail --silent --show-error --max-time 30 'https://api.crossref.org/works?query.title=fundamental%20theorem%20of%20additive%20combinatorics&rows=10&select=DOI,title,author,published'` | 0 | 2695-byte dated mutable response; top results were additive-combinatorics books and unrelated works; SHA-256 `dc6a48a67d0a1154b14398b8fb4bad3a8ecba3a128a86ac3848efa8a65ddd50e` |
| `curl -L --fail --silent --show-error --max-time 30 -A 'Mozilla/5.0' 'https://html.duckduckgo.com/html/?q=%22fundamental+theorem+of+additive+combinatorics%22'` | 28 | timed out after 30 seconds; no result or evidence credited |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, pinned commit and target recorded above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0940/IntakeProbe.lean)` | 0 | seven distinct adjacent signatures elaborated; stdout SHA-256 `135604d6...8711`, stderr empty; no target declaration or proof credit |
| exact-phrase `rg` over pinned mathlib, repo-local Lean, and existing target artifacts | 1 (expected) | no Lean occurrence of the generic English or Chinese title; bounded intake search only |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0940-pycache python3 -m py_compile Stage1_Instances/THM-M-0940/check_intake.py` | 0 | scoped validator compiled without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0940/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and DAG identity, source/dependency hashes, H5/M4/R4 null-target boundary, exact artifact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0940/check_intake.py` | 0 | public replay mode passed without the scheduler-only packet |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null` checks plus `git diff --check` | 0 aggregate | no whitespace diagnostics in any changed artifact |

## Known open gates

An accountable target correction, one immutable authoritative pinpoint proposition, complete
definition/premise/conclusion/proof-boundary/correction mapping, neighbor-scope reconciliation, and
independent source review remain open. So do the canonical Lean expression and environment
fingerprints, minimal imports, checked transports and statement mutations, exhaustive anchor audit,
discovery and obligation freezes, typed graphs, proof, composition, provenance and trust closure,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, and
master acceptance. These failures do not invalidate a truthful, self-tested `planned` intake.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0940-INTAKE` only. It supports a planned
dossier and an explicit H5/M4/R4 worker proposal, not an accepted node receipt. Lifecycle remains
`planned`, `audit_complete=false`, and `theorem_complete=false`; every downstream node is open.
