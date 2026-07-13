# Exact-statement gate: blocked

Item: `S56-M-0490-STATEMENT`

Theorem: `THM-M-0490`

Base revision: `1c0c5fc6f43e6ae5ecc3b50589b45c3628e0ead4` (tree
`61214aa2a03c032134ddc4958b1df63df3430a85`).

## Decision

The statement item remains `[ ]`. Its intake prerequisite has provisional state `[_]`, but its
worker receipt is unaccepted and non-content-addressed. More importantly, the intake deliberately
leaves the canonical statement and formal target null because the source-to-Lean map is not yet
approved. Choosing its prospective proposition would turn discovery input into a canonical target
without satisfying the rev-5.6 statement gate.

The repository gloss says only that infinitely many pairs of primes have difference below seventy
million. The inspected primary paper states the sharper consecutive-prime consequence

```text
lim inf as n tends to infinity of (p_(n+1) - p_n) < 7 * 10^7,
```

where `p_n` is the increasing prime sequence. The intake correctly distinguishes this consequence
from Zhang's stronger admissible-tuple Theorem 1, which is a proof source rather than an allowed
replacement root. It also records that no independent reviewer has accepted the complete source
definition, proof-boundary, incorporated-dependency, correction/errata, catalog-translation, and
source-to-Lean crosswalk.

Several proposition-changing choices remain unresolved:

- the source's positive indexing versus mathlib's zero-indexed `Nat.nth Nat.Prime`;
- literal liminf over a specified codomain versus `Filter.Frequently` or `forall N, exists n >= N`;
- natural subtraction versus subtraction after coercion to integers or reals;
- the checked equivalence between a strict liminf bound and infinitely often gaps below the same
  integer threshold;
- the exact ordered binders, casts, first-prime boundary, and overflow interpretation; and
- source-level approval that the consecutive-prime consequence, not the admissible-tuple theorem,
  is the canonical root.

The intake's formula

```lean
forall N : Nat, exists n : Nat,
  N <= n /\ Nat.nth Nat.Prime (n + 1) - Nat.nth Nat.Prime n < 70000000
```

elaborates only as a prospective type. `IntakeProbe.lean` explicitly says it is noncanonical and
does not relate it to the published liminf statement. Re-labeling it as exact would contradict the
owned intake evidence. Consequently there is no canonical expression on which to certify minimal
imports, serialize an expression and environment fingerprint, compile every credited transport,
or execute the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations. Those checks are undefined, not passed. The vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` directly imports
`Mathlib.NumberTheory.PrimeCounting`. In the pinned environment it checks `Nat.nth`, `Nat.Prime`,
`Nat.infinite_setOf_prime`, `Nat.prime_nth_prime`, `Nat.nth_strictMono`, and
`Nat.primeCounting`; it proves only primality and strict ordering of adjacent enumerated primes and
elaborates the prospective cutoff proposition. It declares no Zhang target or proof body. Its
single import is convenient substrate, but cannot be certified minimal for a canonical target that
does not exist.

A bounded exact-topic search in repo-local Lean and pinned mathlib found only the three explanatory
or prospective occurrences in this target's intake probe. This is statement-feasibility evidence,
not the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided `.lake` link was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`). Lean commands ran from
`Formalizations/Lean`; all other commands ran from the repository root unless noted otherwise.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0490` | 0 | rank 1367; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` before editing | 0 | only the automation-provided untracked `.lake` link existed; base revision and tree are recorded above |
| exact `python3 -c` authority/null-target assertions recorded in `statement-blocker.json` | 0 | intake `[_]`, statement `[ ]`, dependency order, unaccepted intake receipt, null canonical statement and target, and `[H1,M4,R4]` agreed |
| exact `sha256sum` argv recorded in `statement-blocker.json` | 0 | authority, source, intake, toolchain, lockfile, probe, and pinned-prime-module digests agreed with the structured record |
| `lake env lean --version`; `lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision, tree, and package status | 0 | revision and tree agree; the package worktree is clean |
| `lake env lean ../../Stage1_Instances/THM-M-0490/IntakeProbe.lean` | 0 | six APIs, adjacent-prime facts, and the prospective proposition type elaborated; 430 output bytes; SHA-256 `e3f281515b7acbbf05e6653544c9f65160841085a55293cfc6225d2ff8506078` |
| bounded Lean search for bounded/prime-gap and decimal-bound terms | 0 | only three owned intake-probe lines matched; output SHA-256 `2880bb78f851e64815e40d34f54ebc441526c14750bed005131cd87879a41010`; discovery only |
| `python3 -B Stage1_Instances/THM-M-0490/check_intake.py` | 1 | historical intake checker expects authority state `[ ]`, while current authority records provisional `[_]`; this statement phase records rather than rewrites historical intake evidence |
| scoped prohibited-construct scan over owned Lean | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool`, exact `python3 -c` blocker assertions, and exact scoped `bash -lc` whitespace recipe recorded in `statement-blocker.json` | 0 | exact IDs and two-file scope, null target/imports, false completion flags, four undefined mutations, and clean formatting agreed |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable did not pass |

The intake checker also freezes its original nine-file inventory. Adding later-phase blocker
artifacts makes that intake-only inventory historical. This run does not rewrite the intake
checker, receipt, instance, task DAG, generated blueprint, or authoritative execution DAG to
manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers
must preserve and hash the lawful primary source, independently approve the published consecutive-
prime consequence as the root and Theorem 1 as proof source, and complete the definition,
assumption, proof-boundary, incorporated-source, correction/errata, and catalog-translation
crosswalk. They must freeze and check zero/one indexing, liminf codomain, infinitude formulation,
gap domain, cast/subtraction order, strict bound, ordered binders, first-index and overflow cases,
and every credited transport.

A later statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, and execute all four
mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the assigned deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
