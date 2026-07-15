# THM-M-0651 partial proof execution (slot64)

Item: `S56-M-0651-PROOF`
Base: `48fb6596b1844f4183c411142415d872ff21e842` / tree
`eb8dfff0e90b5ce5b11ac2096777060d62874064`

## Verdict

`no_state_change`, with self-tested partial proof progress proposed as worker state `[_]`.
`ProofLemmas.lean` now contains eight unconditional, placeholder-free declarations. Seven existing
bodies supply countable scheduling and the nullary boundary. The new
`exists_consistent_avoidance_extension` proves the semantic core of the dense nonprincipality step:
if `phi` is consistent with `T` and `p` is nonprincipal, then some `psi` in `p` preserves
satisfiability after adding `not (phi implies psi)`. This is semantically `phi and not psi`.

The file repeats the frozen `Isolates` and `IsNonprincipal` definitions exactly so the leaf remains
independently replayable. It does not yet contain a checked cross-module equality transport, and
the frozen registry gives the relevant obligations architecture fingerprints instead of exact Lean
types consumed by a composition. Consequently this packet claims zero frozen obligations closed.

The exact root stays `[H1, M4, R3]` and `theorem_complete=false`. `M0651-L-HENKIN` and
`M0651-L-OMIT` still lack bodies. In addition, the frozen `AvoidanceInterface` is not a valid target
for the planned split: `Candidate` stores an arbitrary countable model, while the interface demands
that every such model omit every supplied nonprincipal type. A real architecture must retain the
avoidance invariants in the constructed candidate or return the omitted model jointly.

## Validation

All Lean commands reused the pre-existing canonical pinned `.lake` symlink without update, build,
clone, fetch, or dependency mutation. Temporary compilation outputs were created under `/tmp` and
removed by the replay script.

| Command | Exit | Result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-0651/check_proof.sh` | 0 | fresh temporary copies of statement, conditional composition, and eight partial bodies elaborated with `--trust=0 -t0`; exact axiom reports passed |
| `python3 Stage1_Instances/THM-M-0651/check_statement.py` | 0 | exact expression hash reproduced; both frozen mutations killed |
| `python3 Stage1_Instances/THM-M-0651/check_obligation_tree.py` | 0 | 11 obligations and 21 typed edges passed; root open at M4 |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranked targets passed |
| `python3 scripts/stage1_target.py show THM-M-0651` | 0 | rank 697; planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0651/check_proof.py` | 0 | source, pins, evidence, and worker packet passed fail-closed checks |
| `git diff --check -- Stage1_Instances/THM-M-0651 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Six nontrivial declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`. Both
zero-arity witnesses report no axioms. Lean's `assert_no_sorry` accepts all eight declarations, and
the supplemental source scan finds no prohibited proof construct.

## Boundary

The predecessor `S56-M-0651-OBLIGATION_TREE` is itself only worker-provisional `[_]`, so the master
cannot accept this proof item before dependency-ordered predecessor acceptance. This receipt is
warm-cache nonrelease evidence and supports neither `AUDIT-Z` nor `THEOREM-Z`.

Reopen the mathematical construction after versioning exact consumed interfaces, then implement a
joint countable Henkin construction carrying the avoidance invariants and the schedule-decoding
omission proof.
