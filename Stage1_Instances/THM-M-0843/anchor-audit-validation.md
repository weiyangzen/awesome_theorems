# Anchor-audit validation

Item: `S56-M-0843-ANCHOR_AUDIT`  
Base revision: `5ae439adae290d44dcf08cc6439c5fb64154fe47`

## Result

The frozen target has an exact candidate in pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`: `szemeredi_regularity` in
`Mathlib.Combinatorics.SimpleGraph.Regularity.Lemma`. Its binders, positivity and graph-size
premises, full-vertex equipartition, lower and explicit upper bounds, and formal partition-uniformity
conclusion agree with the statement-phase proposition. `AnchorAudit.lean` repeats that proposition
literally and closes it through the pinned declaration.

The terminal declaration has an explicit proof at `Lemma.lean:79-155`. It first uses the singleton
partition when the graph is no larger than the explicit bound, treats `epsilon >= 1` with an
arbitrary equipartition, and otherwise iterates the energy increment until nonuniformity would force
energy above one. The direct source import is `Regularity.Increment`; the six directly relevant
regularity support modules and their hashes are recorded in `anchor-audit.json`.

Lean reports the terminal declaration sorry-free. The narrow kernel check reports exactly
`propext`, `Classical.choice`, and `Quot.sound` for both the terminal theorem and the audit adapter.
All seven pinned `Regularity/*.lean` sources have explicit
declarations and pass a comment-aware supplemental scan for `sorry`, `admit`, `sorryAx`, custom
axioms, unsafe declarations, and opaque declarations. No solver, external evaluator, generated
certificate, or oracle is used by the adapter. This is classified as an exact `M0-W / E2`
candidate, not accepted `E1` theorem evidence: full transitive provenance and TCB acceptance,
obligation composition, hermetic replay, and master acceptance remain later gates.

## External audit

A discovery protocol was frozen before the public queries. Anonymous GitHub repository searches
for the English and accented names and the formalization-paper title returned no Lean project. The
declaration-name query returned only three non-Lean repositories. GitHub code search returned HTTP
401 without a credential, and grep.app returned HTTP 429 with a Vercel checkpoint; both are access
failures, not negative evidence. Response hashes and the exact limitation are retained in the
structured ledger. No dependency was cloned, fetched, built, or added. The official Lean
formalization is the pinned mathlib source, not a second independent terminal body. The ledger
also records its immutable Lean 3 introduction and Lean 4 port commits as historical lineage only;
neither is double-counted as a separate candidate.

## Commands and results

All local checks ran in this worker clone against the existing pinned Lake artifacts read-only.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0843` | 0 | rank 1032; planned; legacy artifacts unaccepted; theorem incomplete |
| `git status --short` | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` link existed at preflight |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...ea95`; tree `bdc39a31...5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned source tree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0843/AnchorAudit.lean` | 0 | exact wrapper elaborated; terminal is machine-reported sorry-free; terminal and wrapper axiom reports are `propext`, `Classical.choice`, `Quot.sound` |
| `python3 -B Stage1_Instances/THM-M-0843/check_anchor_audit.py` | 0 | target/authority identity, immutable pins, seven source hashes, terminal body markers, forbidden constructs, exact adapter, candidate classifications, and fail-closed boundary agree |
| GitHub repository API queries recorded in `anchor-audit.json` | 0 | three zero-result responses plus one three-result non-Lean response; immutable response hashes recorded |
| GitHub code API query `szemeredi_regularity language:Lean` | 22 from `curl --fail-with-body`; HTTP 401 | explicit unauthenticated access failure; response SHA-256 recorded |
| grep.app API query `szemeredi_regularity` | 22 from `curl --fail-with-body`; HTTP 429 | explicit Vercel-checkpoint access failure; response SHA-256 recorded |
| `python3 -m json.tool Stage1_Instances/THM-M-0843/anchor-audit.json` | 0 | structured ledger parses |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0843-anchor-pycache python3 -m py_compile Stage1_Instances/THM-M-0843/check_anchor_audit.py` | 0 | checker compiles without owned-path cache output |
| scoped prohibited-construct scan and `git diff --check -- Stage1_Instances/THM-M-0843 .stage1-worker-selftest.json` | expected no-match / 0 | no prohibited declaration in new Lean; no whitespace errors |

## Boundary

This self-tests only the assigned anchor-audit node. The bounded inventory is classified and an
exact pinned candidate is kernel-checked, but discovery saturation is not claimed. The obligation
registry, complete typed provenance/trust graph, accepted `E1`, primary-source `H0`, readable `R0`,
full audit, release evidence, theorem completion, and master acceptance all remain open.
