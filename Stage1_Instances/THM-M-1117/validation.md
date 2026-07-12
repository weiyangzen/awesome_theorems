# Intake validation

Base revision: `2734644ab66534a403c2062af16eda4fb799e018`.

Validation is limited to target-manifest consistency, planned-dossier structure, JSON syntax,
scope invariants, pinned-environment graph API availability, prohibited proof constructs, and
whitespace. Because the source phrase is not an exact proposition, the Lean file is an API probe,
not a canonical statement or proof. No statement-gate, source-proof, or kernel-proof result is
claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1117` | exit 0; rank 557, planned L0/rework_required, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1117/instance.json` and `task-dag.json` | exit 0; valid JSON |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1117/IntakeProbe.lean)` | exit 0; pinned Lean elaborated `SimpleGraph`, `Connected`, `dist`, `diam`, and `neighborSet` checks |
| scoped Python intake assertions | exit 0 after the dossier was complete; planned lifecycle, H5/M4/R4 boundary, null canonical target/fingerprint, empty accepted state, six open dependency-ordered tasks, and owned-file references checked |
| `if rg -n '\b(sorry|axiom|admit)\b' Stage1_Instances/THM-M-1117/IntakeProbe.lean; then exit 1; else echo 'forbidden proof construct scan: clean'; fi` | exit 0; no prohibited construct found |
| `git diff --check -- Stage1_Instances/THM-M-1117 .stage1-worker-selftest.json` | exit 0; no output |

During assembly, the first run of the scoped invariant script exited 1 because `validation.md`,
already listed in `owned_artifacts`, had not yet been written. This was a dossier-completeness check,
not a mathematical or Lean failure; after adding this record, the identical assertions passed.

The first downstream failed gate is statement identity. Retry requires selection and independent
inspection of one exact source-supported analytic proposition, including model conventions,
observables, probability/asymptotic semantics, and the boundary between proof and simulation.
Canonical elaboration and mutation tests, source review, formal-candidate audit, obligation
registry, proof, hermetic replay, and independent release validation remain open. These boundaries
prevent audit and theorem completion but are compatible with this truthful planned intake.
