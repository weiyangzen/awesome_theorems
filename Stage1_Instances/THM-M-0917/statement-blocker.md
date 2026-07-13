# Exact-statement gate: blocked

Item: `S56-M-0917-STATEMENT`

Theorem: `THM-M-0917`

Base revision: `fcabbf1e0ad9507eebe91663bccabfa87d22813e` (tree
`873e589c594454b7f263c7ed2342089a4d15e842`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0917-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, is not
content-addressed, and contains no accepted receipt ID. Rev-5.6 section 10.2 permits this
dependency-ordered investigation, but the integration lane must accept fresh intake evidence
before any future statement transition can be accepted.

Independently, the exact-statement gate cannot pass from the received repository record. The
complete catalog entry supplies only the label `分拆函数` (partition function), Leonhard Euler,
1748, and the gloss `整数分拆的计数` (counting integer partitions). This is the name and description
of a mathematical object, not a truth-valued proposition. It has no formula, source locator,
definition chain, ordered binders, hypotheses, conclusion, proof boundary, correction record, or
boundary convention. Its `已验证` label is untrusted metadata under rev-5.6.

The intake correctly leaves materially different possible roots unselected:

- a definition or representation theorem such as a function whose value at `n` is
  `Fintype.card (Nat.Partition n)`;
- an equivalence between multiset, nonincreasing-list, Ferrers/Young-diagram, or multiplicity
  encodings;
- Euler's generating-function product or pentagonal recurrence;
- a congruence, positivity or monotonicity result, asymptotic, or exact formula; and
- a restricted-partition identity such as the Glaisher theorem.

These are not interchangeable claims. Several are already separated into neighboring repository
targets, including `THM-M-0916`, `THM-M-0918`, `THM-M-0510`, and `THM-M-0511`. Selecting a familiar
partition theorem or treating a chosen definition as proof of an unspecified source theorem would
broaden, narrow, or substitute the target.

Even a definition or representation target would still require an approved source and decisions
about positive unordered summands, the representation and equality convention, input domain,
codomain, `p(0)`, negative inputs if present, empty partitions, zero parts, order sensitivity,
coercions, binder order, and boundary cases. No accountable correction or independently reviewed
pinpoint source currently fixes those choices.

Sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard blockers.
There is therefore no canonical expression for which direct imports can be minimized, no
elaborated expression or target-environment fingerprint to serialize, and no alternate transport
to credit. The required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations are undefined, not passed. No `Statement.lean`, theorem declaration, proof body,
placeholder, axiom, weakened special case, or broadened interface was added. The root remains
`[H5, M3, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates under the pinned toolchain. Its two
direct imports expose `Nat.Partition`, its `Fintype`, unique zero and one cases, cardinality, and
generic partition generating-function APIs. All eight checks pass, with complete stdout SHA-256
`8c70d48c13a20efd7b48243defbca122c1b207b2e5132a136a8f7d9d20dd282a`.

The probe defines no partition-number function, truth-valued canonical target, checked source
transport, or proof body. Its imports cannot be certified minimal for an absent target and receive
no statement or proof credit. In particular, mathlib's `Partition.GenFun` module explicitly marks
the constant-one ordinary partition-function specialization as `TODO: prove this`.

A bounded search over pinned mathlib and repository-local Lean found partition definitions, the
generic generating function, restricted-partition theorems, and unrelated thermodynamic uses, but
no repository-selected THM-M-0917 proposition. This is discovery-only evidence, not the downstream
anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No dependency update, build, clone, fetch,
or other `.lake` mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0917` | 0 | rank 1459; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, guidelines, and complete intake inspection | 0 | confirmed that the catalog supplies an object gloss rather than a proposition, the canonical target is null, and source and encoding decisions remain open |
| `python3 -B Stage1_Instances/THM-M-0917/check_intake.py` | 1 | historical intake replay rejects the current authoritative intake state `[_]` because its worker-time validator froze `[ ]`; this phase records rather than rewrites historical intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0917/IntakeProbe.lean` | 0 | eight adjacent pinned interfaces elaborated; stdout SHA-256 above; no canonical target or proof body |
| bounded partition-function search in pinned mathlib and repo-local Lean | 0 | only definitions, generic generating functions, restricted identities, and unrelated meanings were found; no canonical root selected |
| prohibited-construct scan over owned Lean files | expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
approve either a target correction or one lawful immutable pinpoint source proposition, then
independently crosswalk its incorporated definitions, assumptions, proof boundary, edition and
page, corrections, and errata. They must freeze the partition representation, input and codomain,
`p(0)` and any totalization, ordered binders, hypotheses, exact conclusion, alternate encodings,
and all boundary cases.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change, statement receipt, worker `[_]`, proof credit,
or master acceptance is claimed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json` is emitted.
