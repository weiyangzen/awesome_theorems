# THM-M-0843 obligation-tree validation

Item: `S56-M-0843-OBLIGATION_TREE`. Base revision:
`02cc55f883d5b5d091ead6851bffe89199eb8391`; base tree:
`035212d041a1e61553b3d2f465964c9bbb35e47d`. Validated on 2026-07-13 in the
isolated worker clone. The pre-existing automation-provided `Formalizations/Lean/.lake` link and
canonical pinned artifacts were reused read-only. No update, build, clone, fetch, or network access
was performed.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0843` | 0 | rank 1032; planned; L0/rework-required; theorem incomplete. |
| `python3 -B Stage1_Instances/THM-M-0843/build_obligation_artifacts.py` | 0 | deterministically wrote 44 obligations and 261 typed edges; denominator `5373c66a...66751f06`. |
| `python3 -B Stage1_Instances/THM-M-0843/check_obligation_tree.py` | 0 | 44 obligations, 261 typed edges, 105 structured ledger steps; zero closed obligations; accepted root H1/M3/R4. |
| `python3 -m json.tool` on the registry, graphs, specs, and receipt | 0 | all four structured artifacts parse. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0843/Statement.lean` | 0 | exact target, checked transport, and four expected mutation failures elaborated. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0843/AnchorAudit.lean` | 0 | exact terminal wrapper elaborated; terminal sorry-free; terminal and wrapper axioms were `propext`, `Classical.choice`, `Quot.sound`. |
| Scoped statement interface compilation plus `lake env lean` on `ObligationTree.lean`, executed by `check_obligation_tree.py` | 0 | a temporary `Statement.olean` outside the repository made the canonical declaration importable; terminal, adapter, and root composition elaborated; terminal was sorry-free; all four axiom reports were `propext`, `Classical.choice`, `Quot.sound`; temporary directory was removed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0843-obligation-pycache python3 -m py_compile ...` | 0 | builder and checker compile without owned-path cache output. |
| `git diff --check -- Stage1_Instances/THM-M-0843 .stage1-worker-selftest.json` | 0 | no whitespace errors. |

The checker also binds the exact statement and anchor hashes, current repository base, pinned
mathlib revision/tree and seven Regularity source hashes. It validates denominator projections,
all required node fields, <=100 budgets, stable structured ledger steps, readable anchors, seven
separate graph types, endpoint legality, proof reciprocity, root reachability, acyclicity, fingerprint-
bound root composition certificate, 18 explicitly unverified internal decomposition plans,
validation coverage boundaries, source-body markers, and prohibited proof-construct hygiene.

## Boundary

This is scoped dirty-worker evidence pending master acceptance, not proof or release evidence. The
exact pinned candidate is locally checked at `E2`, while accepted `M0-W` requires `E1`; consequently
all proof obligations remain open and the accepted root remains `H1/M3/R4`. Primary-source H0,
readable R0, transitive provenance and trust, hermetic replay, independent validation, AUDIT-Z,
THEOREM-Z, and master acceptance remain open. In particular, the internal proof relations are
frozen source-body plans rather than checked child-to-parent composition certificates; proof work
must supply those exact harnesses before any internal parent can close.
