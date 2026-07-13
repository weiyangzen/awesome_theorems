# THM-M-0827 intake validation

## Scope

This record validates only the `planned` dossier, scope map, source-statement crosswalk, open task
DAG, bibliographic observations, and discovery-only pinned Lean API probe. It does not validate an
exact mathematical statement, a Floyd-Warshall specification, a recurrence invariant, weighted
all-pairs correctness, path reconstruction, transitive closure, negative-cycle detection,
termination, complexity, implementation refinement, proof, accepted receipt, audit completion, or
theorem completion.

The worker tree was nonrelease-dirty throughout: the canonical `.lake` link was already untracked,
and this intake's owned artifacts plus the root self-test packet were new. The link was used
read-only. No dependency content, authority file, generated checklist, execution-DAG state, other
target path, or `.lake` content was modified. No `lake update`, `lake build`, dependency clone, or
dependency fetch was performed.

## Environment

- Repository base: `46a0f2a3ea74765a0467c489264b838ffbb70675`
- Base tree: `7b1b5269d7da840fd086da731d6f92903c209c35`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- Platform: Linux `7.0.0-27-generic`, `x86_64`
- Timezone/date: Asia/Shanghai, 2026-07-13

Crossref and Semantic Scholar metadata were observed for Floyd DOI
`10.1145/367766.368168` and Warshall DOI `10.1145/321105.321107`. The metadata corroborates
authors, titles, venues, dates, pages, and identifiers. The transient API bytes were not retained
and are explicitly non-authoritative discovery, not a replayable source packet. Both ACM PDF
requests returned HTTP 403. No primary paper text was inspected, vendored, or credited.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0827` | 0 | rank 1385, planned, L0/rework_required, no legacy slot, theorem_complete false |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing untracked canonical `.lake` link existed; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 6075,6080 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate in `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded Crossref and Semantic Scholar queries | 0 | Floyd and Warshall 1962 bibliographic leads corroborated; transient responses not retained or credited; no primary statement or H0 mapping |
| ACM primary PDF retrieval attempts | 22 | both returned HTTP 403; primary texts remain a source blocker |
| `rg -n -i -l 'floyd[- ]?warshall\|floyd.*shortest\|warshall.*shortest\|all[- ]pairs shortest\|shortest path.*matrix' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 expected | no exact-topic occurrence in the bounded repo-local and pinned-mathlib scope; not an absence proof |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0827/IntakeProbe.lean` | 0 | 15 adjacent pinned APIs elaborated; stdout 2078 bytes, SHA-256 `26c08241afe0333e857956272de2899489e98d7ee53a4ac92e706bb54e027feb`; no target or proof credit |
| `python3 -m json.tool` on owned JSON and `.stage1-worker-selftest.json` | 0 each | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0827-pycache python3 -m py_compile Stage1_Instances/THM-M-0827/check_intake.py` | 0 | scoped validator parses without writing cache files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0827/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M4/R4 boundary, null formal target, hashes, exact inventory, receipt/packet agreement, and six open tasks agree |
| prohibited-declaration scan over `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped tracked and per-file new-file whitespace checks | 0 | no whitespace diagnostics for the owned dossier or root worker packet |

The exact transient discovery commands were:

```bash
curl -L --fail --silent --show-error --max-time 30 -A 'awesome-theorems-stage1-intake/1.0 (mailto:noreply@example.invalid)' 'https://api.crossref.org/works/10.1145/367766.368168' -o /tmp/thm-m-0827-floyd-crossref.json
# exit 0; 2481-byte non-authoritative metadata response
curl -L --fail --silent --show-error --max-time 30 -A 'awesome-theorems-stage1-intake/1.0 (mailto:noreply@example.invalid)' 'https://api.crossref.org/works/10.1145/321105.321107' -o /tmp/thm-m-0827-warshall-crossref.json
# exit 0; 2669-byte non-authoritative metadata response
curl -L --fail --silent --show-error --max-time 30 'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/367766.368168?fields=title,authors,year,venue,externalIds,openAccessPdf' -o /tmp/thm-m-0827-floyd-s2.json
# exit 0; 450-byte non-authoritative metadata response
curl -L --fail --silent --show-error --max-time 30 'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/321105.321107?fields=title,authors,year,venue,externalIds,openAccessPdf' -o /tmp/thm-m-0827-warshall-s2.json
# exit 0; 434-byte non-authoritative metadata response
curl -L --fail --silent --show-error --max-time 30 -A 'Mozilla/5.0' 'https://dl.acm.org/doi/pdf/10.1145/367766.368168' -o /tmp/thm-m-0827-floyd.pdf
# exit 22; HTTP 403, expected source blocker
curl -L --fail --silent --show-error --max-time 30 -A 'Mozilla/5.0' 'https://dl.acm.org/doi/pdf/10.1145/321105.321107' -o /tmp/thm-m-0827-warshall.pdf
# exit 22; HTTP 403, expected source blocker
```

These network observations are not structured validation recipes or accepted evidence. The two
offline recipes in `intake-receipt.json` are the self-test authority for this provisional handoff.

## Known failures and boundary

Master acceptance is pending. The catalog still lacks one selected truth-valued proposition.
Primary source text, lawful immutable editions, exact statements, definitions, assumptions, proof
maps, correction and errata audits, Floyd/Warshall provenance and transport, and independent source
review remain open. So do graph and weight models, infinity and negative-cycle semantics, matrix
initialization and recurrence, update order, output and path witnesses, the `O(n^3)` boundary, the
canonical Lean expression and fingerprints, checked transports and mutations, exhaustive anchor
audit, obligation registry, typed graphs, proof, composition, trust closure, readable proof,
hermetic replay, deterministic bundle, independent verification, audit completion, and theorem
completion. These gates do not invalidate a truthful, self-tested `planned` intake.
