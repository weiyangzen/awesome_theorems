# Exact-statement gate: blocked

Item: `S56-M-0862-STATEMENT`

Theorem: `THM-M-0862`

Base revision: `39704171d88ffcdc33a47365ae9791f855fa3a44` (tree
`050ab5c6392560337051d2eadd1b82277dbe1c4f`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0862-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. More importantly, that intake truthfully leaves the
canonical human proposition and Lean target null. The repository supplies only the title Menger's
theorem, the attribution Menger/1927, and the gloss "vertex connectivity and disjoint paths."

That gloss names a theorem family, not one proposition. It does not choose the finite set-to-set
separator equality, the distinct-nonadjacent point form, the global `k`-connectivity
characterization, or a numeric connectivity equality. It also does not fix the graph class and
finiteness assumptions; terminal sets or vertices; vertex-disjoint versus internally
vertex-disjoint paths; whether separators may contain terminals; the parameter `k`; graph-order
premises; ordered binders; the equality or equivalence orientation; or degenerate cases. These
choices change the proposition and cannot be inferred by Lean.

The inspected sources expose rather than remove the ambiguity. Menger's 1927 `Satz beta` is a
topological result about finite terminal sets and pairwise disjoint arcs in a compact regular
one-dimensional space; its definition chain, translation, graph transport, corrections, errata,
and independent review remain open. Diestel's modern account distinguishes the finite set-to-set
theorem, its point-to-point corollary, and a global connectivity form, and attributes the global
form to Whitney in 1932. The repository also separately schedules `THM-M-0813` for an overlapping
Menger-family gloss without an accepted alias, deduplication, exact-root, or ownership decision.

Selecting any familiar finite-graph formulation would therefore invent, broaden, or substitute
mathematics. Rev-5.6 makes statement ambiguity and a missing elaborated-expression fingerprint hard
blockers. There is no honest canonical expression whose imports can be certified minimal, no
approved alternate encoding for checked transport, and no target against which the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can run.
Those mutation results are undefined, not passed. The root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with the pinned environment. It
checks eight adjacent path, reachability, induced-graph, and edge-connectivity interfaces. A bounded
search found only `SimpleGraph.Walk.IsPath.disjoint_support_of_append`, not a direct Menger,
vertex-connectivity, or vertex-separator/path-packing characterization. The probe declares no
canonical target, transport, or proof body, and its imports cannot be certified minimal for an
absent target. It receives no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The probe's complete output SHA-256 is
`acddbc7c967786d595d8bce3393b249946d3bd2b5e495df6f246698d6b8c21d7`.

The automation-provided `Formalizations/Lean/.lake` symlink was used read-only. No `lake update`,
`lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0862` | 0 | rank 1416; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped reads and hashes of the standard, skill, target entry, catalog records, Stage0 projections, current execution DAG, and complete intake dossier | 0 | confirmed provisional dependency state, null canonical target, distinct source variants, overlap, and unresolved proposition-defining inputs |
| `git blame -L 6320,6325 -- Docs/researches/math_theorems.md`; corresponding overlap blame | 0 | both sparse Menger-family records originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version; lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | expected pinned revision/tree; mathlib package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0862/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `acddbc7c...21d7`; no canonical target or proof declared |
| bounded repo-local and pinned-mathlib exact-topic `rg` search | 0 | only the intake disclaimer and one appended-path support lemma matched; no exact Menger target was found |
| `python3 -B Stage1_Instances/THM-M-0862/check_intake.py` | 1 | historical intake validator freezes pre-integration authority hashes; the blueprint and DAG have since changed, so it is not current statement evidence and was not modified |
| prohibited-construct scan over owned Lean | expected no-match | no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| JSON parse, scoped blocker assertions, final-newline/trailing-whitespace checks, and diff checks | 0 | blocker identity, current inputs, null target/imports, unchanged vector, four undefined mutations, false completion fields, exact two-file scope, absent self-test, valid JSON, and clean whitespace agree |

## Retry Condition And Status Boundary

The integration lane must first master-accept fresh intake evidence bound to current authority.
Accountable reviewers must then preserve and hash an immutable primary or approved authoritative
source, select and independently approve one exact proposition, and transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, and
boundary case. They must resolve the `THM-M-0862`/`THM-M-0813` identity and ownership boundary and
the Menger/1927 versus Whitney/1932 attribution boundary.

A fresh statement run can then encode precisely the approved claim, fix every graph, terminal,
path-disjointness, separator, `k`, graph-order, and degenerate-case convention, minimize pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, master
acceptance, statement fingerprint, or proof credit is claimed.
