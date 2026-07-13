# THM-M-0748 exact-statement gate: blocked

- Item: `S56-M-0748-STATEMENT`
- Base revision: `444860f481e8bbf64a3357008fd4d01a52006f08` (tree
  `dee24a14497f877ebd81712a99d2da08de62d7ad`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The exact-source-statement and encoding freeze required by sections 5 and 5.1 of
`Docs/Stage1_Blueprint_rev-5.6.md` cannot be completed from the accepted inputs. The repository
record says only that Post's problem asks whether there is a degree strictly between the
computable and complete degrees. It omits the computably enumerable restriction, Turing
reducibility, definitions and representatives of both endpoints, ordered binders, a positive
existence proposition, a source locator, a proof boundary, corrections, and independent review.
Its `solved` label is explicitly untrusted metadata under rev-5.6.

The intake identifies the intended family as the classical question whether a c.e. Turing degree
`a` satisfies `0 <_T a <_T 0'`. That family-level disambiguation is not an approved exact root.
The identified Post 1944 bibliography has no preserved primary passage or page-level statement in
the dossier, and the Friedberg and Muchnik solution statements have not been independently
inspected and crosswalked. In particular, the inputs do not decide whether this target owns direct
intermediate-degree existence or a checked consequence of the stronger two-incomparable-c.e.-sets
formulation scheduled separately as `THM-M-0749`.

The remaining choices change the proposition and its formal meaning:

- a c.e. set or predicate, a domain or range of a partial recursive function, a characteristic
  oracle, or another source-mapped representative;
- mathlib's partial-function `TuringDegree` quotient or a checked set-level degree construction;
- concrete representatives and transports for the computable bottom degree and c.e.-complete
  halting degree `0'`;
- strict degree order versus reducibility plus non-equivalence, and all representative/quotient
  well-definedness obligations;
- direct existence versus Friedberg-Muchnik incomparability plus checked consequences;
- empty and universal sets, constant or nowhere-defined partial functions, duplicate degree
  representatives, and witnesses equal to either endpoint; and
- the ordered binders, universes, typeclass context, logic, choice, quotient, extensionality,
  computability-coding, TCB, and computation policies.

Selecting the familiar formula `exists a, IsCE a /\ 0 < a /\ a < 0'` would merely hide these
unresolved definitions behind invented parameters or new infrastructure. Selecting a
noncomputable c.e. set without Turing-incompleteness, an incomplete degree without the c.e.
restriction, an intermediate many-one degree, or the theorem called "Post's theorem" in mathlib
would weaken or substitute the assigned claim. None is permitted.

There is therefore no canonical Lean expression whose imports can be certified minimal, no
elaborated expression or canonical environment fingerprint to preserve, and no approved alternate
encoding for a checked transport. The required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined rather than passed. The root
vector remains `[H1, M4, R4]`.

The intake dependency is only provisional `[_]`. Its worker receipt declares `accepted: false`,
is not content-addressed, and contains no accepted receipt ID. Provisional inspection can inform
this fail-closed attempt, but master acceptance is still required before a later statement
transition can be accepted.

## Pinned Lean boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated through its two direct imports:

```lean
import Mathlib.Computability.Halting
import Mathlib.Computability.TuringDegree
```

It checks ten c.e.-predicate, partial-recursion, oracle-reducibility, equivalence, quotient-degree,
and order interfaces, then elaborates only an abstract shape parameterized by an arbitrary `IsCE`
predicate and arbitrary endpoint degrees. The command exited 0; stdout was 823 bytes with SHA-256
`6d773b601b70e0b3b5b67214ef375fcad1140ccaa431c313604cd6c7ba0fdb84`, and stderr was empty. The
probe declares no canonical Post-problem target, endpoint, c.e.-to-degree bridge, checked transport,
or proof body. Its imports therefore cannot be called minimal imports for the absent target and
receive no statement or proof credit.

A bounded exact-topic search of pinned mathlib and `Formalizations/Lean/AwesomeTheorems` found no
Post-problem, Friedberg-Muchnik, or intermediate-Turing-degree declaration. This is narrow
statement-surface feasibility evidence, not the downstream immutable anchor audit or a global
absence claim.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided canonical `.lake` symlink
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0748` | 0 | rank 1334; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped inspection of the blueprint, execution skill, guidelines, target manifest and DAG entries, source records, Stage0 projection, and complete intake dossier | 0 | the standard c.e. Turing-degree family is identified, but the canonical human claim, source-approved encoding, Lean expression, and fingerprints remain null |
| `git blame -L 5514,5526 -- Docs/researches/math_theorems.md` | 0 | the Post-problem and adjacent Friedberg-Muchnik catalog rows originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over current authority, source, intake, toolchain, lockfile, probe, and pinned computability inputs | 0 | current input digests agree with `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0748/IntakeProbe.lean` | 0 | ten adjacent APIs and one abstract order shape elaborated; output digest recorded above; no canonical target or proof body |
| bounded exact-topic `rg` over pinned mathlib and repo-local shared Lean | 1 | expected no match; discovery only, not an anchor audit or absence proof |
| `python3 -B Stage1_Instances/THM-M-0748/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`; integration now records provisional `[_]`, so it fails closed before statement evidence is considered |
| prohibited-construct scan over owned Lean files | 1 | expected no match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0748/statement-blocker.json` and scoped blocker assertions | 0 | structured syntax, identity, null target/imports/hashes, four undefined mutations, unchanged vector, false completion flags, exact two-file scope, and absent self-test agree |
| `git diff --check` plus per-added-file `git diff --no-index --check` | 0 aggregate | no whitespace diagnostics; each raw no-index command returned only the expected added-file difference status 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable did not pass |

The intake checker is historical phase-local evidence: it freezes the intake-time authority cursor
and exact nine-file inventory. This phase neither rewrites that checker nor changes scheduler,
blueprint, or DAG state to manufacture freshness.

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash immutable primary question and solution sources, select and
independently approve one exact positive proposition, and transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, and
boundary case. That selection must fix the c.e. representation, oracle/reducibility conventions,
bottom and complete representatives, quotient transports, strict order, direct-versus-
incomparability route, neighboring-target ownership, and foundation and trust policies.

A later statement run can then encode only that approved claim, establish minimal pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four mutation classes. Until then this node remains `[ ]`; `audit_complete` and
`theorem_complete` are false. Because the assigned phase did not pass its completion gate, no
`.stage1-worker-selftest.json`, statement receipt, proof credit, or master acceptance is claimed.
