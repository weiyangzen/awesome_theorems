# THM-M-0826 intake validation

## Scope

This record validates only the `planned` dossier, scope map, source-statement crosswalk, open task
DAG, bibliographic and modern source-lead observations, and discovery-only pinned Lean API probe.
It does not validate an exact mathematical statement, a Bellman-Ford specification, distance or
path correctness, negative-cycle detection, termination, complexity, implementation, proof,
accepted receipt, audit completion, or theorem completion.

The worker tree was nonrelease-dirty throughout: the canonical `.lake` link was already untracked,
and this intake's owned artifacts plus the root self-test packet were new. The link was used
read-only. No dependency content, authority file, generated checklist, execution-DAG state, or
other target path was modified. No `lake update`, `lake build`, dependency clone or fetch, or other
`.lake` mutation was performed.

## Environment

- Repository base: `902d9ce008e88a35a2307c85355560a230cc33c2`
- Base tree: `dfc20d8141f18f6b09a03e818acfff408e836714`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- Platform: Linux `7.0.0-27-generic`, `x86_64`
- Timezone/date: Asia/Shanghai, 2026-07-13

Crossref metadata for DOI `10.1090/qam/102435` was observed with a bounded `curl` request and had
SHA-256 `041757f19943e40f1b84175fb51bcbde35b87d63c34b5714d59da952ebcf7a49`.
It confirms Richard Bellman, *On a routing problem*, *Quarterly of Applied Mathematics* 16(1),
April 1958, pages 87-90. Semantic Scholar metadata had SHA-256
`c1ff12e8bba9eec0336ecf4a148d0fd20d9703e2866a4a1a0af314003b58bd2e` and points to
the publisher PDF; publisher requests returned HTTP 403/520. These mutable metadata bytes are
retained only in `/tmp` for the worker run and are bibliographic discovery, not admitted evidence.

The MIT OpenCourseWare PDF *6.006 Lecture 17: Bellman-Ford* was observed at
`https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/5edb13fb34cbe7f4cdccc13d131772e7_MIT6_006F11_lec17.pdf`.
Its SHA-256 is `7693bf7b5854cc4c45f13013a0ff9dbf0a46349e8f86877c7deed63f187e30b8`.
The optional `--mit-pdf` validator path rechecks the digest and source discriminators. The file is
not vendored, the catalog does not cite it, and source admission and independent review remain
open.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0826` | 0 | rank 1384, planned, L0/rework_required, no legacy slot, theorem_complete false |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing untracked canonical `.lake` link existed; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 6068,6073 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate in `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded Crossref and Semantic Scholar `curl` observations | 0 | Bellman 1958 bibliographic lead identified; response hashes recorded; no primary text or theorem mapping credited |
| bounded MIT OpenCourseWare PDF retrieval plus `pdftotext -layout` | 0 | six-page modern algorithm, theorem, proof-outline and corollary lead inspected; PDF digest recorded; no H0 credit |
| publisher Bellman PDF and RAND Ford paper retrieval attempts | 22/520 | exact historical texts unavailable to this worker; recorded as source blockers, not silently fetched elsewhere |
| `rg -n -i -l 'bellman[- ]?ford\|negative[- ]?(weight\|edge).*(shortest\|path)\|shortest[- ]?path.*negative[- ]?(weight\|edge)' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 expected | no occurrence in bounded repo-local and pinned-mathlib scope; not an absence proof |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0826/IntakeProbe.lean` | 0 | ten adjacent directed-graph/path-weight APIs elaborated; representative axioms are only `propext` and `Quot.sound`; no target theorem introduced; output SHA-256 `1b63986ff72da4809fb8d328b95298d4f268b874a7e2c695a6eedd065b384be5` |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 each | all structured artifacts are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0826-pycache python3 -m py_compile Stage1_Instances/THM-M-0826/check_intake.py` | 0 | scoped validator parses without writing cache files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0826/check_intake.py --mit-pdf /tmp/MIT6_006F11_lec17.pdf --worker-packet .stage1-worker-selftest.json` | 0 | source PDF discriminators plus manifest/DAG identity, null target, H5/M4/R4 boundary, source and pin hashes, receipt/packet agreement, exact inventory, Lean probe, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-0826` | 1 expected | no prohibited declaration token; `#print axioms` is an allowed diagnostic |
| `git diff --check -- Stage1_Instances/THM-M-0826 .stage1-worker-selftest.json` and per-new-file no-index whitespace checks | 0/no diagnostics | all tracked and untracked artifacts pass whitespace checks |

The final JSON, scoped-invariant, prohibited-construct, and whitespace results were recorded after
receipt and worker-packet creation. The scoped validator's exact stdout SHA-256 is
`591659f4ed7a31bfcbe67d27c4771140636a9715d9ec1527ce820d186b7545f5`.

## Known failures and boundary

Master acceptance is pending. The catalog still lacks a selected truth-valued proposition. Exact
source identity, Bellman/Ford chronology, lawful immutable primary source, result locator, graph
and algorithm definitions, complete premise/conclusion/proof/correction map, and independent
algorithms review remain open. So do the canonical Lean expression and environment fingerprints,
minimal imports, checked transports, statement mutations, exhaustive anchor and terminal-body
audit, obligation registry, typed graphs, proof, composition, trust closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, audit completion,
and theorem completion. These open gates do not invalidate a truthful, self-tested `planned`
intake.
