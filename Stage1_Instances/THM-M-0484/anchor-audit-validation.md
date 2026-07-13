# THM-M-0484 anchor-audit validation

Item: `S56-M-0484-ANCHOR_AUDIT`

Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d`

Base tree: `43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the two terminal
declarations `lucas_lehmer_sufficiency` and `lucas_lehmer_necessity` compose exactly into the frozen
target for every natural `p` with `3 <= p`. The lower bound discharges sufficiency's `1 < p`
premise, and necessity already has the canonical lower bound. `AnchorAudit.lean` restates the exact
target independently and checks this composition without weakening the domain or either direction.

The narrow replay runs Lean with `--trust=0`, so the imported declarations are rechecked rather
than merely trusted from their oleans. Lean's `assert_no_sorry` passes for both terminal bodies and
the adapter; `#print sorries` reports that they are sorry-free. All three axiom probes report only
`propext`, `Classical.choice`, and `Quot.sound`. An ImportGraph traversal over the two terminals and
adapter visits 35,389 transitive declarations in 1,243 modules and reports no bodyless nonaxiom or
unsafe declaration. The exact terminal source slices, complete source blob, direct imports,
compiled olean, pinned ImportGraph traversal implementation, licenses, and historical introduction
commits are content-fingerprinted in the
structured ledger. A complete sorted closure hash, imported-olean provenance, and executable TCB
remain downstream release gates.

The immutable pinned-mathlib search covers all 8,374 tracked Lean files and finds no monolithic iff
declaration; the exact closure is the checked two-direction composition. Repository-local hits are
separate targets or discovery probes. Complete Sourcegraph-index queries including forks and
archives find only mathlib4, historical mathlib3, two downstream/name-only false positives, and a
different Lucas primality test. The indexed formal-conjectures project has no exact-topic hit.
GitHub code search and grep.app were rate-limited, so public discovery is bounded and no global
saturation claim is made.

The exact route is an `M0-W` candidate with nonrelease `E2` worker evidence. The accepted root
remains `[H1, M3, R4]` pending proof-phase integration, full provenance/trust closure, and master
acceptance. `AUDIT-Z` and theorem completion are both false.

## Commands and exact outcomes

All commands ran inside this worker clone. The scheduler-provided canonical `.lake` symlink was
used read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0484` | 0 | rank 1365; planned; L0/rework-required; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | mathlib revision `8a1783...ea95`, tree `bdc39a...5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned mathlib source worktree clean |
| `lake env lean --trust=0 ../../Stage1_Instances/THM-M-0484/AnchorAudit.lean` (`cwd=Formalizations/Lean`) | 0 | exact wrapper elaborated; three declarations sorry-free; axiom closure matched; transitive walk found 35,389 declarations, 1,243 modules, no bodyless nonaxiom, and no unsafe declaration; stdout SHA-256 `4a27ad95...c37` |
| `python3 -B Stage1_Instances/THM-M-0484/check_anchor_audit.py --worker-packet .stage1-worker-selftest.json` | 0 | item/statement identity, eight candidates, pins, blobs, source slices, history, search receipts, trust-zero replay, fail-closed status, and seven-key worker packet matched |
| `lake env lean ../../Stage1_Instances/THM-M-0484/Statement.lean` (`cwd=Formalizations/Lean`) | 0 | predecessor exact target, two transports, four mutations, and `p = 2` boundary re-elaborated |
| `python3 ../../Stage1_Instances/THM-M-0484/check_statement.py` (`cwd=Formalizations/Lean`) | 0 | predecessor target/source fingerprints, minimal import, transports, and mutations remain valid |
| `python3 -B Stage1_Instances/THM-M-0484/check_statement_artifacts.py` | 0 | tracked statement record/receipt and target artifacts remain internally consistent |
| `python3 -B Stage1_Instances/THM-M-0484/check_intake.py` | 0 | planned dossier preserves intake identity, open downstream DAG, H1/M3/R4, and empty accepted state |
| immutable `git grep` over pinned mathlib and `rg` over all manifest packages/repo-local Lean | 0 | all 8,374 mathlib Lean files and local package/repository boundaries searched; exact terminal pair is unique |
| six complete Sourcegraph global queries and three formal-conjectures repo queries recorded in `anchor-audit.json` | 0 | no independent exact Lean 4 closure; all response hashes and limitations recorded |
| GitHub REST code search / grep.app | 403 / 429 | explicit access failures recorded; no negative-result claim |
| `python3 -m json.tool` on owned JSON files and root packet | 0 | all structured artifacts parse without duplicate keys |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0484-anchor-pycache python3 -m py_compile Stage1_Instances/THM-M-0484/check_anchor_audit.py` | 0 | validator compiles outside the repository tree |
| scoped prohibited-construct scan over `AnchorAudit.lean` | 1 (expected no match) | no proof gap, custom axiom/constant, unsafe/opaque declaration, external implementation, or placeholder |
| supplemental comment-stripped prohibited-construct scan over the pinned Lucas-Lehmer source | 1 (expected no match) | no proof-gap, bodyless, unsafe/opaque, external-code, or generated-proof marker |
| `git diff --check -- Stage1_Instances/THM-M-0484 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status boundary

The two predecessor validators received successor-aware, fail-closed maintenance so they continue
to validate their frozen intake/statement surfaces without treating this node's owned files or the
master's later checklist projection as predecessor drift.

This self-test supports only a provisional anchor-audit node pending master acceptance. It does not
freeze the obligation registry, install the proof-phase canonical wrapper, close the full TCB or
human-source/readability gates, accept M0, complete `AUDIT-Z`, or complete the theorem.
