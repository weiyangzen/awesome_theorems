# Intake validation

Base revision: `cbe531e6fdc68190477a9c7e8f635fe5a68a4bcd` (tree
`0b4a5720f51c89484fdc5f6b6f07dc01ee1e95c8`).

Validation date: `2026-07-12` (`Asia/Shanghai`). This phase covers target membership, planned
dossier invariants, source retrieval and crosswalk evidence, JSON integrity, a bounded pinned
mathlib name search, and a narrow Lean API probe. The automation-provided
`Formalizations/Lean/.lake` symlink existed before this work and was used read-only. No `lake
update`, `lake build`, dependency clone/fetch, or `.lake` mutation was run.

The official Smale PDF was retrieved twice from the recorded AMS URL; both byte streams had
SHA-256 `759e0601e50ceebc812c4a4c67e5b9ed59534848c6d342a2e2cf56871db19551`. The PDF was inspected
outside the repository and is not an owned or delivered artifact. Retrieval and inspection support
the candidate source crosswalk, not H0, canonical-statement identity, or proof credit.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1414` | 0 | rank 913, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short` | 0 | only the pre-existing untracked `Formalizations/Lean/.lake` symlink; it was preserved and excluded from this packet |
| `curl -A 'Mozilla/5.0' -L --fail --silent --show-error <recorded AMS PDF URL> \| sha256sum` (two runs) | 0 | both downloads produced `759e0601...19551`; source statement, competing flow variant, and proof-sketch locators were inspected |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81`, respectively |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1414/IntakeProbe.lean)` | 0 | eight generic invariant-set, periodic-point, dense-set, action-transitivity, and flow APIs elaborated; no target theorem was stated |
| bounded target-name search in `Formalizations/Lean/.lake/packages/mathlib/Mathlib/Dynamics` | 1 | expected no-match result for spectral decomposition, Smale/Axiom A, nonwandering, hyperbolic splitting, basic component, or dynamical indecomposability; intake-only evidence, not an exhaustive anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, and the finalized `intake-receipt.json` | 0 | all structured artifacts are valid JSON |
| `python3 Stage1_Instances/THM-M-1414/check_intake.py` | 0 | `intake invariant check: ok`; IDs, rank, source-open null target, planned lifecycle, empty accepted state, provisional vector, six open downstream tasks, receipt boundary, hashes, and inventory agree |
| prohibited Lean construct scan on the owned path | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1414 .stage1-worker-selftest.json` plus per-new-file `git diff --no-index --check` | 0 | no whitespace errors in tracked or untracked deliverables |

These checks validate only a truthful `planned` intake proposal. The first downstream blocker is
independent selection of the diffeomorphism or flow source variant followed by exact Lean statement
freeze. Primary-source review and errata audit, statement fingerprint and mutations, anchor audit,
obligation/discovery freezes, proof, composition, hermetic replay, independent verification,
deterministic release evidence, and master acceptance all remain open.
