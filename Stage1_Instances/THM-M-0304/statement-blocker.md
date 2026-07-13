# Exact-statement gate: blocked

Item: `S56-M-0304-STATEMENT`

Theorem: `THM-M-0304`

Base revision: `997541734bb32f987fb15f163335a82512992120` (tree
`2c866b9d840d48c48ac839740c62d3b9440be0e5`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0304-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt says `accepted: false`, is not
content-addressed, and has no accepted receipt ID. Rev-5.6 section 10.2 permits dependency-ordered
preparation from a provisional predecessor while concurrency is enabled, but master closure remains
dependency ordered.

Independently, the exact-statement gate fails. The complete repository claim is the title
`莫里定理` (Morrey theorem), attribution Charles Morrey, year 1940, and the gloss
`Sobolev函数的Holder连续性` (Holder continuity of Sobolev functions). It gives no bibliography,
truth-valued proposition, incorporated definitions, ordered binders, hypotheses, conclusion, proof
boundary, correction history, or independently reviewed source crosswalk. Its `已验证` label is
untrusted metadata under rev-5.6.

The gloss identifies a Morrey-Sobolev family, not one theorem. A statement still must choose:

- the domain, dimension, measure, topology, regularity, and local, whole-space, domain, or closure
  scope;
- integer or fractional order, homogeneous or inhomogeneous Sobolev model, weak-derivative or other
  encoding, and almost-everywhere quotient semantics;
- the exponent type, exact order-dimension-exponent relation, strictness, critical and subcritical
  regimes, and infinity endpoint;
- the scalar field, scalar or vector value space, finite-dimensionality, completeness, universes,
  and typeclass assumptions;
- existence and uniqueness of a concrete representative and its exact almost-everywhere agreement
  relation;
- the Holder exponent, control scope, norm or seminorm, pointwise or supremum term, quantitative
  estimate, and constant dependencies; and
- ordered binders, exact hypotheses and conclusion, plus empty or null domains, dimension zero,
  endpoints, irregular or unbounded domains, disconnected domains, zero functions, and zero
  derivatives.

These choices change the proposition rather than merely its notation. Selecting the familiar
first-order scalar `W^{1,p}` theorem with `p > n`, a bounded-domain extension theorem, or a
whole-space compact-support inequality would invent or substitute mathematics.

The source and target identity are also unresolved. Crossref metadata identifies Morrey's 1940
paper, *Functions of several variables and absolute continuity, II*, DOI
`10.1215/S0012-7094-40-00615-9`, and an explicit 1942 correction, DOI
`10.1215/S0012-7094-42-00911-6`. The article bodies, exact theorem, definitions, proof boundary, and
correction content were not inspected or independently mapped. A distinct manifested target,
`THM-M-1242` (`Morrey不等式`), has the same attribution, year, and gloss. No accepted decision makes
the targets aliases, chooses distinct variants, or transfers statement or proof ownership. The
separate Sobolev embedding targets `THM-M-0303` and `THM-M-1237` cannot replace this root either.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. There is consequently no canonical expression whose imports can be
certified minimal, no checked alternate transport, and no meaningful removed-hypothesis,
changed-domain, changed-binder-scope, or boundary-case mutation. Those mutations are undefined, not
passed. No `Statement.lean`, statement receipt, theorem declaration, or proof body was added. The
lifecycle stays `planned` and the provisional root vector stays `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated using the pinned environment. It imports:

```lean
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Topology.MetricSpace.Holder
```

It checks five smooth compact-support derivative-norm inequalities plus `HolderOnWith` and
`HolderOnWith.continuousOn`. The inequalities do not state membership in a source-selected Sobolev
space or construct a representative; the Holder APIs assume the control that the requested theorem
would need to produce. The probe's imports therefore cannot be certified minimal for the absent
canonical target. Its complete stdout is 3,574 bytes with SHA-256
`328a4d40a445bd91579c350a96fd17f7bc1065b60ca981d869551862d6b27225`.

A bounded exact-topic search of pinned mathlib matched only Morrey attribution in the proof of
Rademacher's theorem. Repository-local matches are planning or neighboring-target artifacts,
including the separately owned `THM-M-1237` statement; no exact `THM-M-0304` terminal declaration
was identified. This is narrow discovery evidence only, not the downstream immutable anchor audit
or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was used read-only, and the pinned mathlib worktree remained
clean. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation ran.

## Validation Record

Commands ran in this isolated automation clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0304` | 0 | rank 1306; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped inspection and `sha256sum` of authority, source, intake, toolchain, lock, and pinned source inputs | 0 | all recorded fingerprints agree; the input fixes only an underspecified family, correction lead, duplicate boundary, and null canonical target |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0304/IntakeProbe.lean` | 0 | seven adjacent interfaces elaborated; output size and hash recorded above; no canonical target or proof body |
| bounded exact-topic `rg` over pinned mathlib and repository-local Lean | 0 aggregate | only Rademacher comments and nonterminal or neighboring-target artifacts matched; no exact `THM-M-0304` declaration identified; discovery only |
| `python3 -B Stage1_Instances/THM-M-0304/check_intake.py` | 1 | historical intake replay stops at stale `authoritative_blueprint_sha256` after integration changed authority hashes and cursors; it was not modified or represented as statement validation |
| prohibited-declaration `rg` scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0304/statement-blocker.json` and scoped invariant assertions | 0 | structured blocker parses and its identity, null target and imports, unchanged vector, four undefined mutations, false completion fields, exact two-file scope, and absent self-test agree |
| scoped `git diff --check` and per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; each raw no-index exit 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | root self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is bound to its intake worker's earlier authority hashes. Integration
subsequently recorded intake `[_]` and changed the blueprint and DAG. Rewriting historical intake
evidence is outside this phase and would not cure the missing proposition.

## Retry Condition And Status Boundary

The integration lane must master-accept a fresh intake and resolve `THM-M-0304` versus
`THM-M-1242` identity, variant, and proof ownership. Accountable reviewers must preserve and hash a
lawful immutable primary or authoritative source and the 1942 correction, select one exact
truth-valued proposition, map every incorporated definition and assumption, freeze every domain,
dimension, order, exponent, endpoint, Sobolev, value-space, representative, Holder, estimate,
constant, binder, and boundary-case choice, audit the proof boundary, corrections, and errata, and
independently approve the mapping.

A later statement worker can then encode precisely that approved claim, minimize pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport, and
run all four required mutation classes.

This records the first failed gate. It does not complete the statement node or any downstream node.
`audit_complete` and `theorem_complete` remain false, and no debt-vector change is proposed. Because
the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, node-specific
completion receipt, worker `[_]`, proof credit, or master acceptance is claimed.
