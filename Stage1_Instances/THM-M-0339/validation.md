# Intake validation

Base revision: `3d8dd27e4ff1200a2d9c8daaa9cae8072eca6241`.

Validation covers manifest membership, dossier structure, JSON integrity, primary-source retrieval,
and a narrow pinned Lean API probe. The existing canonical `.lake` link/artifacts were used read-only;
no dependency update, fetch, or build was run. The pre-existing untracked `Formalizations/Lean/.lake`
entry makes this nonrelease evidence. No canonical expression, mutation result, or proof is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0339` | exit 0; rank 832, planned, legacy artifacts unaccepted, theorem_complete false |
| `curl -L --fail https://arxiv.org/pdf/1306.3969 -o /tmp/mss-kadison-singer.pdf` and `pdftotext -layout ...` | exit 0; arXiv v4 primary source retrieved and pp. 1-3 inspected |
| `python3 -m json.tool Stage1_Instances/THM-M-0339/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0339/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0339/IntakeProbe.lean)` | exit 0; all six pinned API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0339` | exit 0; no output |

Known downstream failures are intentionally open: exact endpoint selection, implication-boundary
freeze, canonical statement elaboration and mutation tests, anchor audit, obligation/provenance
graphs, proof, hermetic replay, source/formal independent review, and release acceptance. They block
theorem completion but do not invalidate a truthful `planned` intake.

## Statement-phase validation

Base revision: `230f719da7724afb27c761dcb8c62a327557fe63`.

The statement phase selected MSS Corollary 1.5 and elaborated its exact deterministic partition
claim. The historical reductions to the operator-algebraic Kadison-Singer endpoint are explicitly
outside this root. Validation reused the existing pinned `.lake` artifacts read-only; no update,
fetch, clone, or build was run. The pre-existing untracked `Formalizations/Lean/.lake` remains a
nonrelease worktree condition.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0339` | exit 0; rank 832, planned, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0339/Statement.lean)` | exit 0; printed `Stage1.THM_M_0339.MSSPartitionStatement : Prop` under Lean 4.29.0 |
| `sha256sum Stage1_Instances/THM-M-0339/Statement.lean /tmp/thm-m-0339-statement.out` | exit 0; source `b906c95d...679fd`, elaborated printed expression `65f33abc...03dc` |
| `git diff --check -- Stage1_Instances/THM-M-0339` | exit 0; no output |

This is statement-elaboration evidence only. Proof search, axiom/provenance closure, mutation tests,
anchor audit, obligation graphs, hermetic replay, independent review, and release remain open.
