# Obligation-tree validation

Item: `S56-M-0648-OBLIGATION_TREE`

Base revision: `78890c5f1b62587a2048303f2f011e6049a50559`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0648/build_obligation_artifacts.py` | 0 | generated registry, seven typed graphs, and validation specs; denominator `036fe747addebe5c3c0ff50f1de9cb0d8ddaf0d4898672a16cc2cc67b8b573dc` |
| `python3 Stage1_Instances/THM-M-0648/check_obligation_tree.py` | 0 | PASS: 12 unique obligations, 30 typed edges, reciprocal indexes, digest, acyclicity, and required root reachability checked |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0648/ObligationTree.lean` | 0 | conditional exact conjunction elaborated; `root_compose` axioms were `propext` and `Quot.sound` |
| `python3 -m json.tool` on all three generated JSON artifacts | 0 | valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean targets accepted |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0648` | 0 | rank 694, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0648` | 0 | no whitespace errors |

The first attempted combined validation used the repository-relative Python path while its working
directory was `Formalizations/Lean`; it exited 2 with “can't open file”. The command was corrected
by running the Python checks at repository root and the Lean check at its required Lake root. This
is a command-invocation mistake, not a failed artifact gate.

Known downstream failures remain explicit: all proof obligations are uncredited, the primary-source
pinpoint review is H2, readable reconstruction is R4, and transitive provenance, trust, hermetic,
freshness, independent-verification, release, and master-acceptance gates are open. This phase does
not claim theorem or audit completion.
