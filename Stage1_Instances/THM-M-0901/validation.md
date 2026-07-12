# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, the planned dossier and open task DAG, source-record
provenance, JSON and scoped intake invariants, a narrow pinned Lean substrate probe, prohibited-
construct hygiene, and whitespace. It does not validate a canonical theorem statement or proof.
The initial worktree contained only the automation-provided untracked `Formalizations/Lean/.lake`
symlink. It points to the canonical pinned artifacts, was used read-only, and was not modified.

## Source discovery boundary

The author-version PDF of McKay and Wanless, *On the Number of Latin Squares*, was retrieved to
`/tmp`, inspected at printed pages 1-3 and 7-8, and hashed. It supports definition and counting-
family disambiguation only. Crossref metadata was also checked for that paper and Marshall Hall's
1945 existence paper. No downloaded source was added to the repository, no exact root was selected,
and no complete proof-source mapping or `H0` review is claimed.

## Commands and results

All repository commands ran at the repository root unless `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0901` | 0 | rank 1043; planned; no legacy slot; legacy artifacts unaccepted; theorem-complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD` / `git rev-parse 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6593,6598 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| repository `rg` search for `THM-M-0901`, `拉丁方`, and `Latin square` | 0 | found the short catalog and open Stage0 record plus generated target projections; no binder-complete proposition or accepted legacy artifact |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0' -sS 'https://arxiv.org/pdf/0909.2101v1' -o /tmp/mckay.pdf` | 0 | retrieved the author-version counting source outside the repository |
| `file`, `wc -c`, `sha256sum`, `pdfinfo`, and `pdftotext -layout` on `/tmp/mckay.pdf` | 0 each | 11-page, 135,164-byte PDF; SHA-256 `890c1b8bac1d7ffff1cb8275040eed37b608a4708f6cebc64cf8ac143fcb0d80`; definition and theorem passages inspected |
| Crossref request for DOI `10.1007/s00026-005-0261-7`, saved to `/tmp/mckay-wanless-crossref.json` | 0 | McKay/Wanless, *On the Number of Latin Squares*, *Annals of Combinatorics* 9(3), 2005, pages 335-344; response SHA-256 `24de4128...3c38224d` |
| Crossref request for DOI `10.1090/S0002-9904-1945-08361-X`, saved to `/tmp/hall-latin-crossref.json` | 0 | Hall, *An existence theorem for latin squares*, *Bulletin AMS* 51(6), 1945, pages 387-388; metadata only; response SHA-256 `92b17b6f...f46be73` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake 5.0.0 at the same pinned Lean revision; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; pinned package remained clean |
| bounded case-insensitive `rg` over pinned mathlib and repo-local Lean for `latin.?square`, `quasigroup`, or `orthogonal.?array` | 1 | expected no-match result; no exact-topic declaration located; intake discovery only, not an exhaustive external anchor audit |
| `(cd Formalizations/Lean && LAKE_HOME=/tmp/empty-lake-home lake env lean ../../Stage1_Instances/THM-M-0901/IntakeProbe.lean)` | 0 | nine adjacent pinned matrix, finite-type, cardinality, bijection, and candidate-array type checks elaborated; no target declaration or proof body |
| `python3 -m json.tool` separately on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured records valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0901-pycache python3 -m py_compile Stage1_Instances/THM-M-0901/check_intake.py` | 0 | scoped checker compiles without writing generated files inside the owned path |
| `python3 -B Stage1_Instances/THM-M-0901/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest and execution-DAG identity, source hashes, H5/M4/R4 boundary, null canonical target, exact artifact inventory, receipt/self-test agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0901/check_intake.py` | 0 | public replay mode passes without the scheduler-only root worker packet |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0901` | 1 (expected no match) | no prohibited proof escape or declaration in the API-only probe |
| per-new-file `git diff --no-index --check /dev/null <file>` loop over the owned dossier and root self-test packet | 0 | no whitespace diagnostics; exit 1 from each individual no-index diff was accepted only as the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0901 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0901-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact root or multi-root package selection and
independent source review, canonical Lean elaboration and statement mutations, anchor audit,
discovery and obligation freezes, typed graphs, proof, composition, trust closure, readable proof
reconstruction, hermetic replay, deterministic release bundle, and independent verification remain
open. They prevent theorem completion but do not invalidate the planned intake.
