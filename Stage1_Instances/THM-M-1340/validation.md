# Intake validation

Base revision: `5a057abd0705ba3f4cadbff1712f2bb7467e6354`.

Validation covers target membership, dossier invariants, source identity, JSON integrity, and a
narrow pinned Lean API probe. The canonical `.lake` artifacts were used read-only; no update,
build, clone, fetch, or dependency mutation was run. Because no exact proposition is selected, the
probe is feasibility evidence only and no target elaboration or proof is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1340` | exit 0; rank 951, planned, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` | exit 0; preflight contained only the automation-provided `.lake` symlink, preserved read-only |
| source retrieval and inspection for Teschl, DOI `10.1090/gsm/140` | exit 0; author-hosted preliminary PDF, Theorem 2.11/page 47, and bibliographic metadata inspected; candidate only, not H0 |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | exit 0; Lake `5.0.0-src+98dc76e` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1340/IntakeProbe.lean)` | exit 0; eight adjacent ODE and derivative interfaces elaborated without a root declaration |
| bounded repository and pinned-mathlib search for parameter differentiability/sensitivity of ODE solutions | exit 1 for theorem-specific terms; no usable exact formal artifact found, not an exhaustive anchor audit |

The final JSON, scoped checker, prohibited-construct scan, artifact and packet reconciliation, and
whitespace checks are recorded in `intake-receipt.json` after finalization. Known downstream
failures are the exact source decision and review; statement elaboration and mutations; anchor and
provenance audit; obligation tree; proof and composition; readable reconstruction; hermetic replay;
deterministic evidence bundle; independent validation; and master acceptance. They prevent audit
and theorem completion but do not invalidate a truthful self-tested `planned` intake.
