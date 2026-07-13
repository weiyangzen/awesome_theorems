# Exact-statement gate: blocked

Item: `S56-M-0761-STATEMENT`

Theorem: `THM-M-0761`

Base revision: `748243faadc15828fb087059337fd05b7be9fdeb` (tree
`e46d642646f80980838b6f016f5d69b817bd464d`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0761-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. Rev-5.6 section
10.2 permits this dependency-ordered statement attempt, but the intake receipt is `accepted:
false`, contains no accepted receipt ID, and deliberately leaves the canonical mathematical
statement and formal target null. Master acceptance remains necessary before any future statement
transition can be accepted.

The exact-statement gate cannot pass from the received repository record. The target-bearing
catalog says only `正则语言与上下文无关语言的泵引理`: the pumping lemmas for regular and
context-free languages. It supplies no formula, bibliography, pinpoint proposition, definition
chain, ordered binders, proof boundary, corrections, errata, or independent review. Separate
computer-science records confirm that both branches belong to the collective scope, but they are
distinct targets and transfer no statement, state, receipt, or proof credit.

The two branches require materially different propositions. A regular-language formulation
normally has a three-factor decomposition and pumps one nonempty factor. A context-free-language
formulation normally has five factors, pumps two factors simultaneously, and uses different length
and joint-nonemptiness clauses. The repository does not fix:

1. alphabets, language representations, universes, finiteness, decidable equality, or regularity
   and context-freeness witnesses;
2. pumping-length existence, positivity, dependency order, and accepted-word thresholds;
3. factor order, concatenation association, prefix or central-region bounds, nonemptiness, exponent
   domain, and degenerate cases for either branch; or
4. conjunction, structure, or indexed-family composition and shared versus branch-local binders.

Selecting only the pinned `DFA.pumping_lemma` would weaken the collective target. Constructing a
familiar textbook context-free branch and conjunction would silently resolve proposition-defining
choices that were never received or approved. Rev-5.6 sections 5 and 5.1 make this ambiguity and
the missing expression fingerprint hard blockers. There is consequently no canonical expression
whose imports can be certified minimal, no credited alternate form, and no target against which
the removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can be
run. Those mutations are undefined, not passed. The lifecycle remains `planned`, and the root
vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates against the pinned environment through direct imports
`Mathlib.Computability.DFA` and `Mathlib.Computability.ContextFreeGrammar`. It exposes the following
one-branch candidate:

```text
DFA.pumping_lemma :
  x in M.accepts -> Fintype.card sigma <= x.length ->
  exists a b c,
    x = a ++ b ++ c and
    a.length + b.length <= Fintype.card sigma and
    b != [] and
    {a} * {b}* * {c} <= M.accepts
```

The probe also checks the context-free grammar and language interfaces and a generic two-`Prop`
conjunction shape. A bounded search found no context-free pumping declaration in the selected CFG
module. This is neither an exhaustive anchor audit nor a global absence claim. The probe defines no
canonical target, checked transport, or proof body, and its imports cannot be certified minimal for
an absent target. Its complete stdout has SHA-256
`68b9323262d8e64dcc22aa69f56d226a75fef5d05b4d7212185c1a1f40508c64`.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read only. No update, build, dependency clone, fetch,
or other dependency mutation was run.

## Validation Record

Validation ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0761` | 0 | rank 1347; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped inspection of the blueprint, skill, target manifest/DAG, catalog and Stage0 records, related branch records, and complete intake dossier | 0 | the catalog fixes a two-branch family but not one binder-complete proposition; intake deliberately leaves the canonical statement, imports, expression hash, and canonical environment fingerprint null |
| `sha256sum` over current authority, source, intake, toolchain, lockfile, probe, and relevant pinned mathlib inputs | 0 | input digests recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0761/check_intake.py` | 1 | historical intake replay stops because its frozen assertion expects intake state `[ ]`; integration advanced that cursor to `[_]`; the historical checker was preserved rather than rewritten as statement evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | pinned revision/tree recorded above; dependency worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0761/IntakeProbe.lean` | 0 | fourteen adjacent interfaces plus a generic branch-container shape elaborated; no canonical target or proof body; stdout hash recorded above |
| bounded pumping-name search in repo-local Lean and the pinned DFA/CFG modules | 0 | matches only `DFA.pumping_lemma` and its documentation; bounded discovery only |
| prohibited-construct scan over owned Lean files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool` plus scoped JSON invariant assertions | 0 | valid JSON; identity, dependency, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and no-self-test policy agree |
| scoped and per-new-file `git diff --check` diagnostics inspection | 0 | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker freezes intake-time authority state and an exact nine-file inventory.
Master integration advanced the authoritative intake cursor to `[_]`, and this phase adds two owned
blocker artifacts. Its failure is recorded rather than weakening or rewriting the intake evidence
to manufacture statement success.

## Retry Condition And Status Boundary

First, the integration lane must master-accept refreshed intake evidence. Accountable reviewers
must then preserve and hash lawful immutable primary or approved authoritative passages for both
branches and independently approve their exact formulas and collective target identity. They must
freeze every incorporated definition, domain, ordered binder, hypothesis, pumping-length
dependency, decomposition clause, bound, nonemptiness condition, exponent convention, boundary
case, alternate encoding, proof boundary, correction, and erratum.

A fresh statement worker can then encode only that approved collective claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport and branch-to-root wrapper, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. Because the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, proof credit, or master acceptance is claimed.
