# Intake validation

Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e`; base tree:
`6434a20532ae7c523ad293e67a6228ab384bfb8a`.

This validation covers target membership, the planned dossier and open task DAG, repository and
source-lead provenance, JSON and scoped intake invariants, a narrow pinned Lean substrate probe,
prohibited-construct hygiene, and whitespace. It does not validate a canonical theorem statement or
proof. The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. It points to the canonical pinned artifacts, was used read-only,
and was not modified.

## Source discovery boundary

The E244 English translation at arXiv `math/0507201v2`, Bell's historical study at arXiv
`math/0510054v2`, and NIST DLMF E2-E5 TeX resources were retrieved only to `/tmp`, inspected, and
hashed. E244 Proposition 3 is a matching primary proof lead; DLMF E4-E5 is a matching authoritative
modern statement lead; and the historical study explains 1750 as a first-proof date. None is
admitted as H0: source/translation fidelity, exact modern semantics, proof-node mapping, corrections
and errata, and independent review remain open. Dynamic full-section DLMF HTML is not used as a
replay-stable input; the four equation TeX payloads are recorded instead.

## Commands and results

All repository commands ran at the repository root unless `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0916` | 0 | rank 1458; planned; no legacy slot; legacy artifacts unaccepted; theorem-complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD` / `git rev-parse 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6700,6705 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| repository `rg` for the Chinese name, `pentagonal`, partition generating functions, and Euler aliases | 0 | found the sparse catalog/Stage0 records and pinned generic partition infrastructure; no repo-local exact theorem artifact |
| `curl -L --fail --max-time 60 -A 'Mozilla/5.0' -sS https://arxiv.org/pdf/math/0507201v2 -o /tmp/e244-bell-translation.pdf` plus `file`, `wc -c`, `sha256sum`, `pdfinfo`, and `pdftotext -layout` | 0 each | 8-page, 88,041-byte PDF; SHA-256 `0900718052a4085b7b9b2067fd2710b323223a90f4b8683a0bbe7795f177770e`; product and expansion on pages 1-2 and Proposition 3 proof on pages 3-5 inspected |
| `curl -L --fail --max-time 60 -A 'Mozilla/5.0' -sS https://arxiv.org/pdf/math/0510054v2 -o /tmp/bell-pentagonal-history.pdf` plus `file`, `wc -c`, `sha256sum`, `pdfinfo`, and `pdftotext -layout` | 0 each | 21-page, 220,767-byte PDF; SHA-256 `28623ab30a2a9b025d3c5946f1426366195578b715bffdc53e4874f316f3bcf4`; formula/first-proof/publication chronology inspected as secondary evidence |
| `for id in 2 3 4 5; do curl -L --fail --max-time 30 -sS "https://dlmf.nist.gov/27.14.E${id}.tex" -o "/tmp/dlmf-27.14.E${id}.tex"; wc -c ...; sha256sum ...; done` | 0 each | observed 2026-07-13: 87, 79, 144, and 34 bytes; SHA-256 `678ece35634aba3460abd71fab710f833ba619fc42986733827e0e1759738331`, `5ccf9eb943d8fa75eb0c3ba5bd74acd66063ee626c8d0a440280e3854664157b`, `a5f9de98289d8d6872f4b17d1726972d5ba5ed673117c0d586a6321629859191`, and `2e184a4385ee799a583614fa11872cbd6b5d8ff51428ee706f7f7d0e9b2294f5`; stable locators with observed mutable bytes, not immutable admissions |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake 5.0.0 at the same pinned Lean revision; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; pinned package remained clean |
| bounded case-insensitive `rg` over pinned mathlib and repo-local Lean for `pentagonal` and related aliases | 1 (expected no match) | no exact-topic declaration located; intake discovery only, not an exhaustive external anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0916/IntakeProbe.lean)` | 0 | eight adjacent pinned partition and power-series API checks elaborated; no target declaration or proof body |
| `python3 -m json.tool` separately on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured records valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0916-pycache python3 -m py_compile Stage1_Instances/THM-M-0916/check_intake.py` | 0 | scoped checker compiles without writing generated files inside the owned path |
| `python3 -B Stage1_Instances/THM-M-0916/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest and execution-DAG identity, source and dependency hashes, H1/M4/R4 boundary, null canonical target, exact artifact inventory, receipt/self-test agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0916/check_intake.py` | 0 | public replay mode passes without the scheduler-only root worker packet |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0916` | 1 (expected no match) | no prohibited proof escape or declaration in the API-only probe |
| per-new-file `git diff --no-index --check /dev/null <file>` loop over the owned dossier and root self-test packet | 0 | no whitespace diagnostics; exit 1 from each individual no-index diff was accepted only as the expected new-file difference, while any other exit failed the loop |
| `git diff --check -- Stage1_Instances/THM-M-0916 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0916-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Source admission and independent review, canonical
Lean elaboration and statement mutations, anchor audit, discovery and obligation freezes, typed
graphs, proof, composition, trust closure, readable proof reconstruction, hermetic replay,
deterministic release bundle, and independent verification remain open. They prevent theorem
completion but do not invalidate the planned intake.
