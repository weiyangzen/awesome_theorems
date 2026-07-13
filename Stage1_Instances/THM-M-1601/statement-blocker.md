# THM-M-1601 exact-statement gate: blocked

Item: `S56-M-1601-STATEMENT`

Base revision: `997541734bb32f987fb15f163335a82512992120` (tree
`2c866b9d840d48c48ac839740c62d3b9440be0e5`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1601-INTAKE` is provisional worker state
`[_]`, not master-accepted state `[x]`. The intake receipt is unaccepted and non-content-addressed,
has no accepted receipt ID, and binds an older repository revision and older blueprint and
execution-DAG hashes. Rev-5.6 permits this dependency-ordered provisional attempt, but master
closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The repository supplies only
the title `同态加密` (`homomorphic encryption`), Craig Gentry attribution, year 2009, and the gloss
`密文上的计算` (`computation on ciphertexts`). This identifies a subject and capability, not a
truth-valued proposition with fixed binders, hypotheses, and conclusion. Stage0 explicitly leaves
the formal system, precise definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifacts open. The catalog's `已验证` label is untrusted metadata.

The inspected source-family lead, Gentry's 2009 STOC paper *Fully Homomorphic Encryption Using
Ideal Lattices*, contains materially different possible roots: the evaluation-correctness equation
on page 169; homomorphic, fully homomorphic, and leveled definitions on pages 169-170; the
bootstrapping result in Theorem 3 on page 171; correctness of the ideal-lattice scheme in Theorem 6
on page 172; `E3` bootstrappability under a parameter inequality in Theorem 11 on page 177; and a
composite FHE construction with additional security assumptions. The catalog cites and selects none
of them. They differ in cryptosystem, algorithms and types, circuit class, correctness,
compactness, security, probability, complexity, quantifier order, and boundary cases. Choosing one
now, conjoining several, or using the separate `THM-C-0210` record would invent, narrow, broaden, or
substitute proposition-changing mathematics.

Sections 5 and 5.1 of the rev-5.6 standard make ambiguity and a missing elaborated-expression
fingerprint hard blockers. There is no honest canonical Lean expression whose imports can be
certified minimal. The expression and environment fingerprints, checked alternate transports, and
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are
undefined, not passed. No `Statement.lean`, theorem declaration, proof body, weakened special case,
broadened interface, axiom, or placeholder was added. The vector remains `[H5, M4, R4]`; this says
only that the received catalog target is not one stable proposition, not that correctly stated
homomorphic-encryption results are false or open.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with two direct imports:

- `Mathlib.Algebra.Ring.Hom.Defs`
- `Mathlib.Logic.Function.Conjugate`

Its seven checks expose generic operation-preservation and commuting-diagram interfaces. They
define no encryption scheme, circuit semantics, evaluation correctness, compactness, security,
canonical target, checked transport, or proof body. The probe imports therefore cannot be
certified minimal for an absent target and receive no statement or proof credit.

A bounded lexical search of pinned mathlib and repository-local Lean found only the probe's own
disclaimer under the homomorphic-encryption search terms. It located no source-selected declaration.
This is discovery-only feasibility evidence, not the downstream immutable anchor audit or a global
absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation
was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1601` | 0 | rank 1221; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 11791,11796 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, source, intake, probe, toolchain, lockfile, and relevant mathlib `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-1601/check_intake.py` | 1 | historical intake replay stops at its stale pre-integration blueprint hash; this statement phase records rather than rewrites that evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1601/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; stdout SHA-256 `b7a18d02483866e5c2304d7b501505d2e42607721a3b24b68d004c0d37e8c4dd`; no canonical target or proof body |
| bounded homomorphic-encryption target search over pinned mathlib, repo-local Lean, and the owned target | 0 | only the probe disclaimer matched; no source-selected declaration was located |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

The final JSON, invariant, whitespace, scoped-change, and absent-self-test checks passed after these
two blocker artifacts were written. The historical intake checker is frozen to intake-time
authority inputs and its original artifact inventory. This run records that limitation instead of
rewriting the intake checker, receipt, instance, task DAG, generated blueprint, or authoritative
execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers
must then approve a target correction, redirection, or split; lawfully preserve and hash one
immutable primary or approved authoritative source; select and independently approve one exact
truth-valued proposition; and freeze the selected scheme and algorithms, all types, circuit syntax
and semantics, permitted circuit class, randomness and probability, correctness and compactness,
security and complexity, ordered binders, hypotheses, conclusion, corrections, proof boundary,
neighboring-target boundary, and every degenerate case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
