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
| Inherited raw source rows | 3,338 |
| Deduplicated Stage0 blueprint items | 3,262 |
| Stage4 numbered variants | 3,484 |
| Stage4 curated additions | 146 |
| Stage4 proved-claim projection | 83 |
| Stage4 open/conditional projection | 39 |
| Stage5 current release | 5.6 |
| Stage5 5.6 catalog records | 5,525 |
| Stage5 5.6 theorem-status records | 3,500 |
| Kernel-checked, sorry-free theorem records | 2,000 |
| Stage5 5.6 effective strict conjectures | 1,425 |
| Stage5 5.6 broad open-claim records | 2,025 |
| Stage5 5.6 `open_problem` records | 599 |
| Stage5.1 organization members | 19,790 |
| Stage5.1 theorem execution members | 3,500 |
| Stage5.1 conjecture/occurrence execution members | 16,290 |
| Blueprint subcategories | 285 |
| Disciplines covered | 3 |

Inherited legacy source-row breakdown:

- Mathematics: 1,666 rows
- Physics: 1,272 rows
- Computer science: 400 rows

Most working documents are currently written in Chinese, but the structure is intended to be universal, reusable, and machine-friendly.

The immutable Stage5 5.6 inventory is now materialized under
[`Docs/catalog/v5`](./Docs/catalog/v5/README.md), with generated readable lists
for [3,500 theorem-status records](./Docs/catalog/v5/readable/5.6/Theorem_List.md),
[1,425 effective strict conjectures](./Docs/catalog/v5/readable/5.6/Strict_Conjecture_List.md),
and a [2,025-row broad open-claim projection](./Docs/catalog/v5/readable/5.6/Open_Claim_List.md).
The raw catalog contains 1,426 syntactic `conjecture` rows and 599 separately
typed `open_problem` rows. One retained Moving Sofa conjecture has revoked
strict credit, so the broad-open rows without strict credit total 600, while
the effective strict denominator remains exactly 1,425.

These numbers are an actual release inventory, not a plan. They are also not a
claim of completeness for human mathematics. The inherited 1,500 Formal
Conjectures theorem rows remain `source_asserted_not_replayed`. Releases 5.3,
5.4, and 5.6 contribute 2,000 separately evidenced mathlib formal-proposition
records that are `kernel_checked_sorry_free` at one pinned commit and compiled
environment. Release 5.6 dynamically appends exactly 1,000 of those records;
its 629 `theorem` and 371 `lemma` source declarations all elaborate to runtime
`thmInfo`, but the release does not claim 1,000 distinct human-level named
theorems or an independent universal importance ranking.

Release 5.5 establishes separate quality and open-claim boundaries: 1,000
important landmark identities, a disjoint 582-row additional-frontier set,
and 425 new strict conjectures. The strict records were curated for proposition
shape, status evidence, interest, rights, and semantic duplication; their
current-open status remains bounded by the pinned sources and review date.

The current project SSOT is the
[`Stage5.1 organization release`](./Docs/catalog/stage5_1_organization/README.md),
rooted at its sealed `Current_Release.json`. It preserves the Stage5 5.6
identities and adds one reversible organization mapping, subject assignment,
dependency assessment, and member-specific execution row for each of 19,790
frozen members. Checklist state is owned only by the
[`Stage5.1 theorem Blueprint`](./Docs/Stage5_1_Theorems_Blueprint.md) and
[`Stage5.1 conjecture Blueprint`](./Docs/Stage5_1_Conjectures_Blueprint.md).
The retired `Docs/catalog/v6/` draft tree is intentionally empty: Stage6
catalog, renumbering, qualification, and execution drafts are not current
inputs and cannot allocate identities. Any future Stage6 publication must be a
separately reviewed append-only successor rooted in a published Stage5.1
release.

The frozen 1962--2025 Putnam source universe contains 768 problem coordinates,
including the 675-key PutnamBench subset, plus 1,724 formal-language variants.
Those problem, variant, closure, and relation surfaces receive zero Stage5 5.6
catalog credit; they are not counted as theorem identities.

The audited catalog gaps are now materialized in the
[`Docs/catalog/v4`](./Docs/catalog/v4/README.md) Stage4 data release rather than
remaining Blueprint-only tasks. It dispositions all 154 frozen gap candidates
and 46 named regression fixtures, appends 146 source-backed exact records, and
maps every inherited and new ATV to an immutable `S4-CLM-########` number. Its
theorem and open/conditional lists are generated from the curated records.
This is completion of the bounded audited-gap supplement and full number
migration—not a claim that all 3,338 inherited machine-triage rows, or all
theorems known to humanity, have completed semantic review.

## H/M/R Proof Debt

Stage1 v2 tracks three independent axes. A paper, a kernel check, and a readable reconstruction answer different questions and never substitute for one another.

| Axis | Meaning | Closed state |
|---|---|---|
| `H` human-proof debt | Whether an accepted human proof of the exact statement and assumptions has been source-audited. | `H0` |
| `M` machine-proof debt | Whether the exact node is kernel-checked under the accepted axiom policy, distinguishing local bodies, mathlib wrappers, and pinned external bodies. | `M0-L`, `M0-W`, or `M0-P` |
| `R` readability debt | Whether the route, formal map, trust boundary, composition, and leaf ledger are publicly readable. | `R0` |

Evidence is graded separately as `E0` through `E5`. [`Docs/Stage1_Blueprint_v2.md`](./Docs/Stage1_Blueprint_v2.md) preserves the historical Stage1 integration cursor and evidence vocabulary; it is not the current project SSOT. Each theorem keeps scope and content-addressed validation evidence in its instance artifacts, while current execution state belongs to the corresponding Stage5.1 Blueprint.

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

### 1. Start from the current catalog or execution blueprint

Start with the
[`Stage5.1 organization design`](./Docs/Stage5_1_Organization_Design.md), its
sealed [`current organization release`](./Docs/catalog/stage5_1_organization/Current_Release.json),
and the theorem/conjecture Blueprints linked above. Together they are the
current SSOT: the release owns identity/taxonomy/relation authorities, while
the two Blueprints exclusively own their program checklist states.

For the immutable parent mathematics inventory, use the
[`Stage5 catalog`](./Docs/catalog/v5/README.md) and its 5.6 readable theorem,
strict-conjecture, and broad open-claim lists. Its JSON catalog, number
registries, migration ledger, projections, and strict-credit ledger are data
authorities rather than progress checklists. The
[`Stage4 catalog`](./Docs/catalog/v4/README.md) remains the inherited migration
baseline, not the current mathematics inventory entry point.

Stage1, Stage2, Stage3, and Stage5 predecessor Blueprints remain historical
migration/evidence surfaces. They cannot launch new work, own current
checkmarks, or compete with Stage5.1.

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
  catalog/
    v5/                          # append-only mathematics inventory releases
      README.md
      Current_Release.json
      releases/5.6/
        Claim_Catalog.json
        Theorem_List.json
        Open_Claim_List.json
        Strict_Conjecture_Ledger.json
        Release_Manifest.json
      readable/5.6/
        Theorem_List.md
        Open_Claim_List.md
        Strict_Conjecture_List.md
    stage5_1_organization/       # current identity/taxonomy/relation SSOT
      Current_Release.json
      releases/1.0/
    v4/                          # inherited Stage4 migration baseline
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

The proof/formalization programme remains blueprint-driven. The mathematics
inventory is concrete through immutable Stage5 release 5.6: 3,500
theorem-status records, 1,425 effective strict conjectures, and a 2,025-row
broad open projection. Of the theorem inventory, 2,000 mathlib formal
proposition rows are kernel-checked and sorry-free at their exact pinned
commit; the inherited 1,500 retain their weaker source-asserted evidence.
Stage5.1 is the current organization and execution revision over those frozen
Stage5 5.6 members. Its release currently remains activation-blocked until the
BOOT/fence and complete explicit concurrency-prompt gates pass. These
source-relative counts do not establish universal coverage or a universal
importance ranking.

The release directories, current pointers, generated readable projections, and
their validation evidence are versioned under `Docs/catalog/`. “Published” in
this README means that the immutable release artifacts are present in this
repository; it does not turn source-relative evidence into a claim of universal
mathematical coverage.

That means the highest-value asset right now is the structure: the classification, deduplication, and execution framing.

It is not yet a finished formal proof library, and it should not pretend to be one.

What it already gives you is a serious map.  
What it is building toward is a serious engine. ⚡
