# awesome_theorems

> Not just an awesome list.  
> 🧠 A serious map for turning important theorems into structured, research-ready, formalization-ready assets.

If you have ever wanted one place that helps answer questions like:

- Which theorems matter most across math, physics, and CS?
- Which ones are already formalized, partially formalized, or still blocked?
- What sits between a famous theorem statement and a machine-checked proof?

This repo is built for that gap. 🚀

`awesome_theorems` collects major theorems from mathematics, theoretical physics, and theoretical computer science, then pushes them toward an executable blueprint for formal verification, dependency tracking, and deeper research.

## ✨ At a Glance

| Scope | Current signal |
|---|---:|
| Raw source entries | 3,338 |
| Deduplicated Stage0 blueprint items | 3,262 |
| Blueprint subcategories | 285 |
| Disciplines covered | 3 |

Source breakdown:

- Mathematics: 1,666 theorems
- Physics: 1,272 theorems
- Computer science: 400 theorems

Most working documents are currently written in Chinese, but the structure is intended to be universal, reusable, and machine-friendly.

## H/M/R Proof Debt

Stage1 v2 tracks three independent axes. A paper, a kernel check, and a readable reconstruction answer different questions and never substitute for one another.

| Axis | Meaning | Closed state |
|---|---|---|
| `H` human-proof debt | Whether an accepted human proof of the exact statement and assumptions has been source-audited. | `H0` |
| `M` machine-proof debt | Whether the exact node is kernel-checked under the accepted axiom policy, distinguishing local bodies, mathlib wrappers, and pinned external bodies. | `M0-L`, `M0-W`, or `M0-P` |
| `R` readability debt | Whether the route, formal map, trust boundary, composition, and leaf ledger are publicly readable. | `R0` |

Evidence is graded separately as `E0` through `E5`. [`Docs/Stage1_Blueprint_v2.md`](./Docs/Stage1_Blueprint_v2.md) is the sole current Stage1 requirements, ordering, acceptance, and task-state blueprint. Superseded Stage1 assurance material lives only in Git history and is not read by current commands. Each theorem keeps scope and content-addressed validation evidence in its instance artifacts, while all current `[ ]`, `[_]`, and `[x]` progress remains in the v2 blueprint.

For this repository, Stage1 covers exactly the `1546` metadata-screened Lean 4 targets in
[`Docs/Stage1_Target_Membership_v2.json`](./Docs/Stage1_Target_Membership_v2.json),
not all `1601` deduplicated mathematics records. The target manifest is a membership input to the
v2 blueprint, never an alternative requirements or progress authority. All `1546` targets started at
`L0 / rework_required`; the former 300 priority-slot artifacts are retained only as legacy discovery
inputs and confer no higher assurance or proof credit. The other `55` mathematics records remain
outside the frozen Stage1 membership.

Execution is driven by [`$execute-stage1-v2`](./skills/execute-stage1-v2/SKILL.md). Its ordinary
proof-phase intent is `integrate`, limited to exact human-proved and machine-proved targets whose
external or pinned proof has not yet been accepted here. The separate `frontier_prove` intent is
available only under a current scheduler-owned, independently reviewed, bounded exception with
completion probability at least `0.70`; otherwise the workflow fails closed.

The flagship example is [`THM-M-0387`](./THM-M-0387/README.md), Fermat's Last Theorem. Its `n = 3`, `n = 4`, regular-prime, and `3 <= n <= 16` branches are locally checked through pinned dependencies and wrappers. The exact root remains `M2`: the general odd-prime Wiles/Taylor-Wiles chain is not kernel-closed here, and the audited Imperial full-FLT candidate is blocked by `sorryAx` and a disallowed arbitrary-proposition axiom.

Historical dossier metrics and receipts remain provenance only. They do not establish a current
human-proof source, exact machine-proof closure, focus admission, or Stage1 completion. Only evidence
revalidated under the v2 focus policy can authorize integration or acceptance.

## 🔥 Why This Repo Exists

The internet already has theorem lists. Textbooks already have statements. Formal proof libraries already have islands of machine-checked results.

What is usually missing is the bridge.

This repo is trying to build that bridge by turning scattered theorem knowledge into a structured execution map:

- what the theorem says
- why it matters
- whether it is already formalized, partially formalized, or still blocked
- which logic or formal foundation it should live in
- which proof assistant or verification system fits it best
- which assumptions, lemmas, and references are needed underneath it

In short: this repo is for people who do not just want to read theorems, but want to work with them. ⚙️

## 🛠️ How to Use This Repo

### 1. Start from the blueprint

Read [`Docs/Stage1_Blueprint_v2.md`](./Docs/Stage1_Blueprint_v2.md) first. It is the only current Stage1 blueprint and the only writable Stage1 task-state source. The target JSON and DAG files are derived or membership surfaces; the old assurance document is optional historical provenance and is not an operational input or gate. [`Docs/Stage0_Blueprint.md`](./Docs/Stage0_Blueprint.md) is the upstream Stage0 catalog snapshot, not a competing Stage1 execution source.

The v2 blueprint defines requirements and execution status. Per-theorem evidence supports acceptance but cannot override its checklist; generated DAGs and todo snapshots are not completion authority.

### 2. Use the source collections for raw coverage

The research docs are the source pools that feed the blueprint:

- [`Docs/researches/math_theorems.md`](./Docs/researches/math_theorems.md)
- [`Docs/researches/physics_theorems.md`](./Docs/researches/physics_theorems.md)
- [`Docs/researches/cs_theorems.md`](./Docs/researches/cs_theorems.md)

These are useful when you want breadth, original grouping, or quick browsing by discipline.

### 3. Pick a theorem cluster, not just a theorem name

A better workflow is:

1. choose a discipline
2. choose a subcategory
3. inspect the theorem group
4. follow the dependencies and blockers
5. decide whether you want to study it, formalize it, or use it as a benchmark

That makes this repo much more useful than a flat alphabetical list. 🧩
For automated Stage1 execution, "formalize" means integrate an already-existing exact machine proof;
new root-proof construction remains outside the ordinary lane and requires the bounded
`frontier_prove` admission described above.

### 4. Read each theorem as a task, not just a fact

The blueprint is designed to track fields such as:

- theorem content
- proposition type
- formalization status
- target formal system
- logical foundation
- assumptions and precise definitions
- proof path and key lemmas
- evidence type
- formalization blockers
- artifact links

### 5. Use it for the job you actually care about

- 📚 Learning the landscape of major theorems
- 🔬 Finding formalization targets for Lean, Coq, Isabelle/HOL, HOL Light, TLA+, or model checkers
- ⚙️ Building research backlogs, datasets, benchmarks, or agent workflows
- 🧠 Studying theorem families and dependency chains instead of isolated names

### 6. Read a worked theorem case study

If you want one concrete example of how the blueprint fields can be filled in for a single theorem,
start here:

- [`THM-M-0387/README.md`](./THM-M-0387/README.md)
- [`THM-M-0387/full_study.md`](./THM-M-0387/full_study.md)
- [`THM-M-0387/FermatLastTheorem_Sample.lean`](./THM-M-0387/FermatLastTheorem_Sample.lean)
- [`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT4Path.lean`](./Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT4Path.lean)
- [`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT3Path.lean`](./Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT3Path.lean)
- [`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/StatementAndReductionPath.lean`](./Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/StatementAndReductionPath.lean)
- [`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/RegularPrimesPath.lean`](./Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/RegularPrimesPath.lean)
- [`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/SmallExponentsPath.lean`](./Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/SmallExponentsPath.lean)
- [`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/Sample.lean`](./Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/Sample.lean)

### 7. Check the blueprint guidelines

For the quality bar used when filling or upgrading blueprint items, read:

- [`Docs/Blueprint_Guidelines.md`](./Docs/Blueprint_Guidelines.md)

## 🎁 What You Can Get From This Repo Once the Blueprint Is Fully Finished

Once the blueprint is fully completed, this repo should become much more than a reading list.

You should be able to get:

- a curated, cross-discipline map of important theorems
- a deduplicated theorem-by-theorem execution backlog
- clear separation between what is already formalizable and what is still blocked
- proof-path visibility instead of disconnected theorem names
- target-system guidance for Lean, Coq, Isabelle/HOL, HOL Light, TLA+, and related tools
- structured metadata that can be reused for research, teaching, benchmarking, or automation
- a much faster path from curiosity to implementation

The real payoff is this:

> from “that theorem sounds important”  
> to “here is its statement, assumptions, proof chain, formal target, blockers, and next move.” 🎯

## 🗂️ Repo Structure

```text
Docs/
  Stage0_Blueprint.md
  Blueprint_Guidelines.md
  case_studies/
    fermat_last_theorem_formalization_study.md  # redirect stub
  tools/
    generate_stage0_blueprint.py
  researches/
    math_theorems.md
    physics_theorems.md
    cs_theorems.md
    classified_theorems.md
    formalization_classification.md

THM-M-0387/
  README.md
  full_study.md
  machine_checked_audit.md
  process_audit.md
  build_validation.md
  FermatLastTheorem_Sample.lean
  eligibles/
  run_local_validation.sh
  meta.json

Formalizations/
  Lean/
    README.md
    lakefile.lean
    lean-toolchain
    lake-manifest.json
    AwesomeTheorems.lean
    AwesomeTheorems/
      NumberTheory/
        THM_M_0387/
          FLT4Path.lean
          FLT3Path.lean
          RegularPrimesPath.lean
          Sample.lean

```

根目录承担的是 dossier 与共享 formalization trees 的并列组织：

- `THM-*` 目录保存 theorem dossier
- `Formalizations/` 保存 assistant-specific 共享源码树
- `Docs/` 保存 blueprint、规范与研究总览

## 🚧 Current Status

This repo is still blueprint-first.

That means the highest-value asset right now is the structure: the classification, deduplication, and execution framing.

It is not yet a finished formal proof library, and it should not pretend to be one.

What it already gives you is a serious map.  
What it is building toward is a serious engine. ⚡
