# Statement validation

Base revision: `c6077f63d112c9e6b348b0e7e2370bc1b6024593`.

| Command | Result |
|---|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0990/Statement.lean` | exit 0; canonical declaration and all three mutation propositions elaborated and printed |
| deletion probe removing the sole direct import | exit 1; `unknown namespace` and unknown probability APIs, confirming the import is necessary |
| deletion probe removing the former `Mathlib.Probability.Moments.Basic` import | exit 0; redundant import removed |
| `python3 -m json.tool Stage1_Instances/THM-M-0990/instance.json Stage1_Instances/THM-M-0990/task-dag.json Stage1_Instances/THM-M-0990/statement.json` | exit 0 |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `git diff --check -- Stage1_Instances/THM-M-0990 .stage1-worker-selftest.json` | exit 0; no output |

The Lean command used the clone's symlink to canonical pinned `.lake` artifacts and did not update
or fetch dependencies. The worktree's untracked `Formalizations/Lean/.lake` entry is that automation
symlink, not a dependency mutation by this phase.

Known failures: exact primary-source pinpoint/errata and H0, anchor/provenance audit, proof closure,
axiom/trust audit, hermetic replay, and independent validation remain open. No theorem completion is
claimed.
