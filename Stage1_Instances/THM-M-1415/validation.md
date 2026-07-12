# Intake validation

- Item: `S56-M-1415-INTAKE`
- Base revision: `cbe531e6fdc68190477a9c7e8f635fe5a68a4bcd`
- Base tree: `0b4a5720f51c89484fdc5f6b6f07dc01ee1e95c8`
- Validation date: 2026-07-12 (Asia/Shanghai)

Validation is limited to target membership, manifest consistency, the truthful `planned` dossier,
the open task DAG, JSON and source-literal invariants, publisher metadata, a narrow pinned Lean API
probe, bounded formal-candidate search, prohibited-construct hygiene, and whitespace. The catalog
gloss is not a proposition, so this validation does not establish a canonical mathematical claim,
an exact Lean expression, or a proof.

The preflight worktree contained only the existing untracked link `Formalizations/Lean/.lake`. It
points to the canonical checkout's pinned artifacts and was used read-only. No `lake update`,
`lake build`, dependency clone/fetch, or other `.lake` mutation was performed. This is nonrelease
worker evidence.

Environment fingerprint:

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1415` | 0 | rank 914; planned; L0/rework_required; legacy artifacts unaccepted; theorem incomplete |
| `git status --short` | 0 | before edits, only the automation-provided untracked `Formalizations/Lean/.lake` link was present |
| `git rev-parse HEAD` and `git rev-parse HEAD^{tree}` | 0 | base revision and tree agree with the identifiers above |
| `cd Formalizations/Lean && lake env lean --version && lake --version && sha256sum lean-toolchain lake-manifest.json && git -C .lake/packages/mathlib rev-parse HEAD` | 0 | toolchain, pin-file hashes, and mathlib revision agree with the environment fingerprint |
| Crossref API query for DOI `10.2307/2373370`, selecting DOI/title/author/date/journal/volume/issue/page/publisher/URL with `jq` | 0 | publisher metadata identify Bowen, the paper title, journal 92(3), July 1970, starting p. 725, and DOI; bibliographic discovery only |
| Crossref API query for DOI `10.1007/BF01075361`, selecting DOI/title/author/date/journal/volume/issue/page/publisher/URL with `jq` | 0 | publisher metadata identify Sinai, the first paper, journal 2(1), 1968, pp. 61-82, and DOI; bibliographic discovery only |
| Crossref API query for DOI `10.1007/BF01076126`, selecting DOI/title/author/date/journal/volume/issue/page/publisher with `jq` | 0 | publisher metadata identify the related Sinai construction paper, journal 2(3), 1968, pp. 245-253, and DOI; bibliographic discovery only |
| OpenAlex API queries for DOI `10.2307/2373370` and `10.1007/BF01075361`, selecting location and open-access fields with `jq` | 0 | both principal records report closed access and no repository full text; bounded access observation only |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured intake artifacts are valid JSON |
| Python `ast.parse` on `Stage1_Instances/THM-M-1415/check_intake.py` | 0 | scoped intake validator parses without writing bytecode |
| `PYTHONDONTWRITEBYTECODE=1 python3 Stage1_Instances/THM-M-1415/check_intake.py --without-handoff` | 0 | dossier, receipt, source, DAG, and completion invariants pass before relying on the root handoff manifest |
| `python3 Stage1_Instances/THM-M-1415/check_intake.py` | 0 | manifest/source identity, planned null-target boundary, `[H1,M4,R3]`, empty accepted state, six ordered open tasks, artifacts, receipt, and false completion flags agree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1415/IntakeProbe.lean` | 0 | seven generic pinned partition, stream, and semiconjugacy APIs elaborated; no Markov-partition proposition or proof was introduced |
| bounded exact-phrase `rg` for Markov partitions, subshifts, shift spaces, symbolic dynamics, Axiom A, Anosov, hyperbolic sets, and local product structures in repo-local and pinned-mathlib Lean sources | 1 | expected no-match exit; no named target surface found in the bounded search |
| `rg` for `sorry`, `admit`, `sorryAx`, `axiom`, `opaque`, or `constant` in the owned Lean probe | 1 | expected no-match exit; no prohibited proof construct or assumed declaration |
| per-file `git diff --no-index --check -- /dev/null <new-file>` loop over the nine owned files and `.stage1-worker-selftest.json` | 0 | every file produced only the expected added-content status and no whitespace diagnostic |

## Known downstream failures

- The catalog wording is not a stable proposition, and no independently reviewed primary theorem
  passage selects the root.
- The Bowen/Sinai source boundary, the catalog's 1970 date versus Sinai's 1968 publication, exact
  definitions, assumptions, proof boundary, translation, corrections, and errata remain open.
- No canonical Lean expression, expression/environment hash, exact imports, alternate-encoding
  witness, or statement mutation test exists.
- Discovery protocol, anchor audit, obligation registry and typed graphs, proof, composition and
  trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle, and
  independent release verification are open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
self-tested `planned` intake whose purpose is to freeze the honest ambiguity boundary and open DAG.
Only the integration lane may accept the provisional worker receipt.
