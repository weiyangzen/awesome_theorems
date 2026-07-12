# Exact-statement gate: blocked

Item: `S56-M-0904-STATEMENT`

Theorem: `THM-M-0904`

Base revision: `4b93dbd88c5b39d7b83f2f9278c3371f53703d76` (tree
`a526f0ad0273426336b064730ac8b85143e3e5db`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0904-INTAKE` has only provisional worker
state `[_]`, not master-accepted state `[x]`. Its receipt declares `accepted: false`, has no accepted
receipt ID, and is stale against the current authoritative blueprint. The current replay of
`check_intake.py` stops at `stale receipt input hash: Docs/Stage1_Blueprint_rev-5.6.md`.

Independently, no exact Lean 4 target can be truthfully elaborated from the authoritative repository
record. The record gives only `Dinitz猜想`, Jeff Dinitz, 1979, and `列表着色的存在性` (existence of
list coloring). It gives no bibliography, domains, ordered binders, hypotheses, conclusion, proof
boundary, correction, or erratum. Stage0 explicitly leaves the precise definitions and premises
open, and the catalog's `已证明` label is untrusted under rev-5.6.

The familiar problem family uses an `n x n` array of allowed-color collections and asks for one
allowed color in every cell, with distinct choices in each row and each column. That description
still leaves proposition-changing choices unresolved:

- whether every cell contains exactly `n` colors or at least `n` colors, and which thinning
  principle transports between the forms;
- whether an allowed-color collection is a `Finset`, duplicate-bearing `List`, or `Multiset`, and
  whether repetitions contribute to its size;
- whether the color carrier is arbitrary or finite and which decidable-equality, choice, and common
  finite-palette assumptions are present;
- whether `n` ranges over all naturals or only positive naturals, including the empty and singleton
  arrays and an empty color carrier;
- whether row and column distinctness uses pairwise inequalities, injective sections, proper
  coloring of a line graph, or another source-defined predicate; and
- whether this root is the array assertion, list edge-colorability of `K_(n,n)`, equality of a list
  chromatic index with `n`, or some other formulation.

The neighboring target `THM-M-0905` is Galvin's theorem and is glossed as the proof of the Dinitz
conjecture. Galvin's stronger bipartite-multigraph theorem may eventually provide a checked bridge,
but silently making it this target would substitute a broader theorem. The intake records Galvin's
1995 paper and Slivnik's 1996 abstract only as source leads; neither has been admitted as the exact
source for this root or independently mapped through all definitions and assumptions.

Selecting the conventional finite-set, at-least-`n`, all-natural-numbers array proposition from
memory would therefore invent decisions that the received target does not make. Section 5 of the
rev-5.6 blueprint makes statement ambiguity and a missing elaborated-expression fingerprint hard
blockers. There is no canonical expression on which to certify minimal imports, checked alternate
transports, or the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations. Those tests are undefined, not passed. The root remains
`[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` directly imports pinned simple-graph bipartite, basic, and line-graph
modules. It re-elaborates eight adjacent interfaces for ordinary vertex coloring, bipartiteness,
complete bipartite graphs, and line graphs. It states no Dinitz target and provides no list-coloring
definition. Its imports are discovery inputs only and cannot be called minimal for an unselected
target.

A bounded source search of pinned mathlib and repository-local Lean found no Dinitz, Galvin,
list-coloring, choosability, or list-chromatic declaration. This is narrow feasibility evidence,
not the downstream anchor audit and not a claim of absence outside the searched closure.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The SHA-256 values of `lean-toolchain`,
`lake-manifest.json`, and `IntakeProbe.lean` are, respectively,
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`d33d136bbc327c9ad21d878a16ddd842418e7b63fe6a188aa2e4c3f190275b63`.

The automation-provided `Formalizations/Lean/.lake` link to the canonical pinned artifacts was used
read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was
run. The pinned mathlib package remained clean.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0904` | 0 | rank 1044; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| repository/source inspection for `THM-M-0904`, Dinitz, Galvin, and list coloring | 0 | found the sparse catalog/Stage0 records, provisional null intake target, and unresolved array-versus-stronger-theorem boundary; no admitted source-selected proposition |
| `python3 -B Stage1_Instances/THM-M-0904/check_intake.py` | 1 | the historical intake receipt is stale at the current blueprint SHA-256; this statement run does not rewrite historical evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0904/IntakeProbe.lean` | 0 | eight generic coloring, bipartite, complete-bipartite, and line-graph interfaces elaborated; output SHA-256 `907604cddd32525598d553e88cf0783bf4bc3cca0bf82de358ffced9f8555442` |
| bounded search for Dinitz, Galvin, list coloring, choosability, or list chromatic declarations | 1 | expected no-match result in pinned mathlib and repository-local Lean; discovery-only evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped invariant check for `statement-blocker.json` | 0 each | blocker identity, null target and imports, unchanged vector, four undefined mutations, false completion flags, and absent-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-0904` plus per-new-file no-index checks | 0; 1 each | no whitespace diagnostics; no-index exits are only the expected new-file differences |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must first accept refreshed intake evidence. Accountable reviewers must then
preserve and hash an immutable primary or authoritative source, select and independently approve
one exact Dinitz root, and transcribe every incorporated definition, ordered binder, hypothesis,
conclusion, list-size and duplicate convention, color and `n` domain, boundary case, proof boundary,
correction, and erratum. They must also freeze the boundary and any checked transport between this
array target and `THM-M-0905`'s stronger Galvin theorem.

A fresh statement worker can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
