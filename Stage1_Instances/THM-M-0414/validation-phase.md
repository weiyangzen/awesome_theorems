# THM-M-0414 validation-phase result

Item `S56-M-0414-VALIDATION` was run against base revision
`bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad` (tree
`ca999baf360c6ce2440bbc2c01aeb8d519269a90`). Validation added no proof credit or accepted
obligation closure. It re-elaborated the frozen statement, conditional composition, and proof-phase
root from fresh temporary source copies, then added and checked a separately written validation-only
root probe that imports only `Statement`. Existing pinned Lean artifacts were reused without
mutation.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborate from copied sources; the proof declaration closes the exact frozen root. |
| Differential local implementation | pass, not independent release evidence | `Validation.lean` imports neither `Proof` nor `ObligationTree` and reconstructs the exact root directly from the two pinned mathlib declarations. It ran in the same worker and cache. |
| Placeholder/unsafe/oracle hygiene | pass for inspected sources | The four local Lean modules contain no `sorry`, `admit`, `sorryAx`, local axiom, unsafe declaration, native decision, external implementation, or opaque proof body. This source scan is additional defense, not a complete transitive parser/elaborator audit. |
| Axiom observation | provisional pass | Both proof routes and both terminal declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`. Final foundation-profile and TCB approval remain open. |
| Local provenance | pass | Statement, registry, graph, proof receipt, mathlib revision/tree/source hashes, remote, license, and clean pinned dependency worktree agree. |
| Dependency legality and structured freshness | fail closed | `S56-M-0414-PROOF` is only `[_]`; it is not master accepted. The frozen graph retains `THM-M-0414-TRUST` as an open release gate, and no accepted state was rewritten. |
| Complete transitive provenance and TCB | fail closed | No complete declaration/import closure hash, imported compiled-artifact inventory, compiler/bootstrap inventory, plugin/evaluator inventory, or complete trust-closure hash exists. This is the first failed release gate. |
| Hermetic release replay | fail closed | The worker reused the shared warm `.lake` symlink. It did not create a clean checkout with empty caches, cold-build, restore offline, or produce an SBOM/archive/signed attestation. |
| Independent verification | fail closed | There is no distinct verifier identity, independently provisioned clean runner, second signature, second attestation, or independently implemented release verifier. |

## Commands and results

The recorded node command and fixed `LC_ALL=C`, `TZ=UTC`, and `PYTHONOPTIMIZE=0` environment ran on
2026-07-13. The recipe declares network denied; the checker made no network request, but this
same-worker run did not independently attest OS-level network isolation, so enforcement fails closed.
No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.

```text
python3 -B Stage1_Instances/THM-M-0414/check_validation.py
  exit 0
  PASS THM-M-0414 narrow validation
  kernel: exact statement, conditional composition, proof root, and differential root elaborated
  trust: checked local and terminal declarations report only propext, Classical.choice, Quot.sound
  provenance: frozen proof hashes and clean pinned mathlib revision/tree/source/license agree
  blocked: THM-M-0414-TRUST lacks complete transitive TCB and compiled-import closure
  blocked: shared warm .lake is not cold hermetic replay; same worker is not independent verification

bash Stage1_Instances/THM-M-0414/check_proof.sh
  exit 0: the proof receipt's recorded root recipe replayed; all three proof declarations reported
  exactly [propext, Classical.choice, Quot.sound], and the forbidden-token scan passed

PYTHONOPTIMIZE=1 python3 -B Stage1_Instances/THM-M-0414/check_validation.py
  exit 1 as required: validation rejected optimized Python before any gate assertions

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups; 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0414
  exit 0: rank 69, planned, L0/rework_required, theorem_complete false
python3 -B Stage1_Instances/THM-M-0414/check_anchor_audit.py
  exit 0: three candidates classified; two immutable mathlib anchors verified
python3 -B Stage1_Instances/THM-M-0414/validate_obligation_tree.py
  exit 0: four obligations, two proof edges, acyclic reachability, separate trust gate
python3 -B Stage1_Instances/THM-M-0414/check_whitespace.py
  exit 0: all seven changed artifacts pass trailing-whitespace and final-newline checks
```

The first node-acceptance failure is `S56-M-0414-VALIDATION-PREREQUISITE-NOT-ACCEPTED`; the first
release gate failure is the missing section 7.3/7.4 complete transitive provenance and TCB closure.
Section 10.6's cold hermetic replay is the first failed reproduction-protocol gate. The accepted
vector remains `H2/M3/R3` as recorded by the instance authority. This provisional packet claims no
`E0/E1`, accepted `M0-W`, `AUDIT-Z`, `THEOREM-Z`, theorem completion, release, or master acceptance.
