# THM-M-0762 exact-statement gate: blocked

Item: `S56-M-0762-STATEMENT`

Base revision: `1c0c5fc6f43e6ae5ecc3b50589b45c3628e0ead4` (tree
`61214aa2a03c032134ddc4958b1df63df3430a85`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0762-INTAKE` is only provisional worker
state `[_]`: its receipt is unaccepted and non-content-addressed, has no accepted receipt IDs, and
leaves the canonical mathematical statement and formal target null. Rev-5.6 section 10.2 permits
preparation of later provisional evidence, but master closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete repository record
provides only the title `上下文无关语言的性质` ("properties of context-free languages"), collective
attribution, the period "twentieth century", and the gloss `CFL的闭包性质` ("closure properties of
context-free languages"). It contains no bibliography, formula, operation list, definition chain,
ordered binders, hypotheses, conclusion, proof boundary, corrections, or reviewer. Stage0
explicitly leaves the formal system, exact definitions and premises, proof route, dependencies,
alternate forms, axioms, machine state, and artifacts open.

"Closure properties" is a theorem family, not one proposition. Standard members include positive
closure under union, concatenation, Kleene star, reversal, homomorphic image, inverse homomorphism,
and intersection with a regular language. Ordinary context-free languages are not positively closed
under arbitrary intersection or complement. The record does not say whether this target is one
implication, a positive bundle, or a classification including negative branches. It also does not
fix the alphabet and grammar models, epsilon and erasure conventions, regularity witnesses,
operation-specific source and target alphabets, ordered binders, witness encodings, or boundary
cases. Selecting any familiar theorem or conjunction would invent, narrow, strengthen, or possibly
falsify the received target.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression fingerprint
hard blockers. There is therefore no canonical expression whose imports can honestly be certified
minimal, no source-approved alternate encoding to transport, and no canonical target against which
the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
can be run. Those mutation classes are undefined, not passed.

No `Statement.lean`, theorem declaration, proof body, substituted reversal theorem, weakened special
case, or invented operation bundle was added. The root remains `[H5, M3, R4]`;
`audit_complete: false` and `theorem_complete: false`.

## Pinned Lean Boundary

Pinned mathlib contains one direct closure theorem:

```lean
Language.IsContextFree.reverse.{u} {T : Type u} (L : Language T) :
  L.IsContextFree -> L.reverse.IsContextFree
```

The existing `IntakeProbe.lean` was re-elaborated using its single direct import
`Mathlib.Computability.ContextFreeGrammar`. Nine language, grammar, context-freeness, and reversal
interfaces elaborated; Lean reported the reversal theorem's axiom set as `propext`,
`Classical.choice`, and `Quot.sound`. A bounded search found only the pinned `IsContextFree`
definition and reversal theorem in the scoped Lean roots.

This is useful candidate-interface evidence only. The catalog does not select reversal, so neither
the theorem nor its import can be relabeled as the canonical target or a minimal canonical import.
The bounded search is not the downstream exhaustive anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No update, build, clone, fetch, or other dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0762` | 0 | rank 1348; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped blueprint, skill, guidelines, manifest/DAG, source, Stage0, and intake inspection | 0 | the catalog identifies a family but not one binder-complete proposition; the intake intentionally leaves the canonical statement and formal target null |
| authority, source, intake, toolchain, lockfile, probe, and mathlib `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0762/check_intake.py` | 1 | historical intake replay stops at its frozen base-revision assertion because integration advanced HEAD; the intake checker was preserved rather than rewritten as statement evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; dependency worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0762/IntakeProbe.lean` | 0 | nine adjacent interfaces elaborated; exact reversal type and its three axioms printed; stdout SHA-256 `320921c25c5c868f9699d3f4eeff9488ee290d15236305f9c349b764f4782737` |
| bounded `IsContextFree` search over repo-local and pinned mathlib Lean sources | 0 | only the pinned definition, reversal theorem, and module documentation matched; bounded discovery only |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

The historical intake checker freezes intake-time repository identity, authority hashes, and an
exact intake-only file inventory. Master integration advanced the repository and this phase adds
two blocker artifacts. Its failure is recorded rather than weakening the checker to manufacture a
passing statement attempt.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then preserve one lawful immutable primary or approved authoritative source and independently
select one exact theorem or explicitly enumerated bundle. They must map every incorporated
definition, operation and polarity, alphabet and grammar convention, ordered binder, hypothesis,
conclusion, witness, alternate encoding, proof boundary, correction, erratum, and degenerate case.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
