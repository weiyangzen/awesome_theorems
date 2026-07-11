# Intake validation record

Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0170` | 0 | rank 123, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0170/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0170/task-dag.json >/dev/null` | 0 | open task DAG is valid JSON |
| `rg -n '\\b(sorry|axiom)\\b|placeholder|theorem_complete[[:space:]]*:[[:space:]]*true' Stage1_Instances/THM-M-0170/{README.md,intake.json,source-statement-crosswalk.md,task-dag.json}` | 1 | no forbidden proof claims or placeholders (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-0170 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. It validates repository membership and
artifact structure, not the mathematical source crosswalk or any Lean theorem. Master acceptance
and all dependent phases remain outstanding.

## Statement validation (2026-07-12)

Base revision: `41a639c14626145f43eda7724d6a570cd710d688`.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0170/Statement.lean` | 0 | Exact target, `Iff.rfl` serialization, and four guarded negative mutations elaborate; printed declaration has no metavariables; `statement_iff` axioms are `propext`, `Classical.choice`, `Quot.sound` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0170` | 0 | rank 123, planned, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0170/statement.json >/dev/null` | 0 | statement receipt is valid JSON |

The Lean command reuses the canonical pinned `.lake` artifacts and performs no dependency update.
This validates statement elaboration, not existence of an embedding or theorem closure.

## Anchor-audit validation (2026-07-12)

Base revision: `046b0721abb228d13c7042349574736fe375cd97`.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0170/AnchorAudit.lean` | 0 | Pinned `exists_embedding_euclidean_of_compact` and its exact local wrapper elaborate; wrapper axioms are `propext`, `Classical.choice`, `Quot.sound` |
| `rg -n -i 'nash.{0,30}(embed\|imbedd)\|isometric.{0,30}(embed\|imbedd)\|riemannian.{0,30}(embed\|imbedd)' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/.lake/packages/mathlib/Archive Formalizations/Lean/.lake/packages/mathlib/Counterexamples` | 0 | Matches are generic metric/linear isometric embeddings only; no Nash/Riemannian terminal theorem occurs |
| `rg -n -i 'Nash.{0,40}(embedding\|imbedding)\|Nash-Kuiper\|convex integration' . --glob '!Formalizations/Lean/.lake/**' --glob '!Docs/Stage0_Blueprint.md' --glob '!Docs/Stage1_Blueprint*.md'` | 0 | Finds the legacy THM-M-0170 statement/audit artifact and unrelated exclusion references; no root proof body |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0170` | 0 | rank 123, planned, theorem incomplete |
| `rg -n '\b(sorry\|axiom)\b\|placeholder\|theorem_complete[[:space:]]*:[[:space:]]*true' Stage1_Instances/THM-M-0170/{AnchorAudit.lean,anchor-audit.md}` | 1 | no forbidden declarations, placeholders, or completion claims (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-0170 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The GitHub repository-metadata searches and the grep.app failure boundary are recorded in
`anchor-audit.md`; they are discovery evidence, not kernel evidence. The Lean check uses the
existing pinned `.lake` tree without updating dependencies. It validates only the nearby compact
Whitney substrate and does not prove the Nash target.

## Obligation-tree validation (2026-07-12)

Base revision: `c2687431b1d86bac7bd509c9abbfdc1e763c060c`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0170/build_obligation_artifacts.py` | 0 | deterministically generated the 17-row frozen registry, validation recipes, and seven typed graph indexes |
| `python3 Stage1_Instances/THM-M-0170/check_obligation_tree.py` | 0 | `PASS THM-M-0170 obligation tree: 17 obligations, 41 typed edges`; denominator `9b30c70c...df079f`; graph reciprocity, indexes, acyclicity, root reachability, node schema, budgets, and source hygiene passed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0170/ObligationTree.lean` | 0 | conditional compact/noncompact recomposition elaborated; axioms were exactly `propext`, `Classical.choice`, `Quot.sound` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0170` | 0 | rank 123, planned, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0170/obligation-registry.json >/dev/null && python3 -m json.tool Stage1_Instances/THM-M-0170/typed-graphs.json >/dev/null && python3 -m json.tool Stage1_Instances/THM-M-0170/validation-specs.json >/dev/null` | 0 | all structured artifacts are valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0170 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The Lean check reused the pinned `.lake` closure and performed no update, build, clone, or fetch.
The architecture is self-tested only: both substantive branch packages and every Nash analytic
engine remain open, no proof coverage is credited, and master acceptance remains required.

## Proof execution validation (2026-07-12)

Base revision: `45225aadff56e3948bc75a950e5287a960a002b5`.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0170/Proof.lean` | 0 | `statement_of_isEmpty` closes the exact empty-manifold boundary case with target dimension zero; axioms are exactly `propext`, `Classical.choice`, `Quot.sound` |
| `python3 -m json.tool Stage1_Instances/THM-M-0170/proof-receipt.json >/dev/null` | 0 | structured proof receipt is valid JSON |
| `rg -n '\b(sorry|axiom)\b|placeholder|theorem_complete[[:space:]]*:[[:space:]]*true' Stage1_Instances/THM-M-0170/{Proof.lean,proof-receipt.json}` | 1 | no forbidden declarations, proof gaps, or false completion claim (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-0170 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This proof phase makes genuine but bounded machine-checked progress on `M0170-S-BOUNDARY`. It does
not close either member of the frozen root cut set (`M0170-B-COMPACT`, `M0170-B-NONCOMPACT`) and
therefore does not establish the Nash embedding theorem. The next actionable proof work remains the
substantive compact and noncompact construction packages and their shared analytic engines.
