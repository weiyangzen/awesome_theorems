# Exact-statement gate: blocked

Item: `S56-M-0891-STATEMENT`

Theorem: `THM-M-0891`

Base revision: `46a0f2a3ea74765a0467c489264b838ffbb70675` (tree
`7b1b5269d7da840fd086da731d6f92903c209c35`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0891-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered
investigation, but the intake receipt declares `accepted: false`, is not content-addressed,
contains no accepted receipt ID, and deliberately leaves the canonical mathematical statement and
formal target null. Master acceptance remains necessary before a future statement transition can
be accepted.

Independently, the exact-statement gate cannot pass from the received repository claim. The catalog
supplies only the name Wilf theorem, the Herbert Wilf/1967 attribution, and the gloss
`色数的谱下界`, literally "a spectral lower bound for the chromatic number." It supplies no formula,
graph conventions, ordered binders, hypotheses, equality scope, source locator, proof boundary,
correction history, or boundary cases. Its `已验证` label is untrusted under rev-5.6.

The matching primary bibliographic record is H. S. Wilf, *The Eigenvalues of a Graph and Its
Chromatic Number*, Journal of the London Mathematical Society s1-42 (1967), pages 330-332, DOI
`10.1112/jlms/s1-42.1.330`. Current Crossref, OpenAlex, Unpaywall, and Semantic Scholar records
confirm this closed publication but expose no lawful full text. The Wiley text-mining route
returned HTTP 400 and the publisher PDF route returned an access challenge. Thus the exact primary
formula, assumptions, equality clause, incorporated definitions, proof boundary, and corrections
were not admitted or independently reviewed.

A versioned secondary source, Assis, Coutinho, and Juliano, arXiv `2401.03042v2`, printed page 2,
attributes to Wilf the familiar inequality

```text
chi(G) <= 1 + lambda_1(G),
```

and reports equality exactly for complete graphs and odd cycles. That is an upper bound on the
chromatic number, or after rearrangement a lower bound
`lambda_1(G) >= chi(G) - 1` on the largest adjacency eigenvalue. It therefore does not resolve
whether the catalog intends the common upper bound, its rearranged spectral-radius form, the
equality characterization, a connected-graph version, or a different lower-bound result such as
the neighboring least-eigenvalue family.

The proposition-changing Lean choices remain open:

- finite undirected simple graphs, carrier universes, `Fintype`, decidable adjacency,
  nonemptiness, and connectedness;
- mathlib's `ENat`-valued chromatic number versus a natural minimum or a universally quantified
  colorability form, including finite-colorability and cast conventions;
- the real adjacency matrix and largest-eigenvalue representation, ordering, multiplicity, and
  the empty-carrier boundary;
- inequality orientation, real/natural subtraction, and checked algebraic transport between the
  two candidate forms;
- whether complete-graph and odd-cycle equality cases belong to the root and their isomorphism,
  component, parity, and cycle-length conventions; and
- empty, singleton, edgeless, disconnected, isolated-component, complete-graph, and cycle cases.

Selecting any one of these encodings without source adoption and review would invent, narrow,
broaden, or substitute mathematics. In particular, `THM-M-0890` owns Hoffman's least-eigenvalue
bound, `THM-M-0858` owns Brooks' maximum-degree theorem, and `THM-M-0887` is the broader spectral
graph-theory record; none can supply this target's statement identity.

Sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard blockers.
There is consequently no canonical expression for which minimal imports, checked alternate
transports, or the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations can be certified. All four mutation classes are undefined, not passed.
No `Statement.lean`, proof body, weakened special case, broadened interface, or circular assumption
was added. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned toolchain. Its four direct imports
expose graph coloring and chromatic number, real adjacency matrices, Hermitian eigenvalues,
connectedness, and complete graphs. All ten interface checks pass, with complete output SHA-256
`37f180a93211c0fdddfb6f991e24f5e1c079199201822662e286798a9472bf45`.
The probe defines no Wilf predicate, canonical target, checked source transport, equality
classification, or proof body. Its imports therefore cannot be certified minimal for an absent
canonical target and receive no statement or proof credit.

A bounded exact-topic search over pinned mathlib and repository-local Lean found no Wilf
spectral-coloring declaration under the recorded search terms. This is discovery-only evidence,
not the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No dependency update, build, clone, fetch,
or other `.lake` mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0891` | 0 | rank 1441; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, guidelines, intake, and source-boundary inspection | 0 | confirmed the sparse catalog wording, closed primary bibliographic record, secondary direction conflict, null canonical target, and unresolved source and encoding decisions |
| current OpenAlex, Unpaywall, Semantic Scholar, Crossref, Wiley, and arXiv discovery queries | 0 aggregate | primary publication remains closed with no repository full text; publisher routes returned HTTP 400/403; no exact primary statement was admitted |
| `sha256sum` over authority, intake, source, probe, toolchain, lock, and pinned mathlib inputs | 0 | exact current hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0891/check_intake.py` | 1 | historical intake replay rejects current authoritative intake state `[_]` because its worker-time validator froze `[ ]`; it also freezes older authority hashes and the original nine-file inventory, so this phase records rather than rewrites it |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0891/IntakeProbe.lean` | 0 | ten adjacent pinned interfaces elaborated; output SHA-256 above; no canonical target or proof body |
| bounded Wilf spectral-coloring search in pinned mathlib and repo-local Lean | 1 | expected no-match result; discovery-only evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash an immutable primary or approved authoritative edition, transcribe and
independently approve the exact theorem and incorporated definitions, resolve the catalog's
direction against the Wilf inequality, identify the proof boundary, and complete correction and
errata review. They must freeze the graph, chromatic-number, eigenvalue, coercion, equality,
connectedness, alternate-encoding, binder, and boundary conventions.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
