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

Read [`Docs/Stage0_Blueprint.md`](./Docs/Stage0_Blueprint.md) first.

This is the authoritative execution blueprint for the repo. It is the best entry point if you want the structured, deduplicated, execution-oriented view.

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
  researches/
    math_theorems.md
    physics_theorems.md
    cs_theorems.md
    classified_theorems.md
    formalization_classification.md

scripts/
  generate_stage0_blueprint.py
```

## 🚧 Current Status

This repo is still blueprint-first.

That means the highest-value asset right now is the structure: the classification, deduplication, and execution framing.

It is not yet a finished formal proof library, and it should not pretend to be one.

What it already gives you is a serious map.  
What it is building toward is a serious engine. ⚡
