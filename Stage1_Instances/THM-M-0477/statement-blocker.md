# THM-M-0477 exact-statement gate: blocked

Item: `S56-M-0477-STATEMENT`

Base revision: `3ef3a6bf4f2f9b86930beb27693f7429fea3e63a` (tree
`c9eba4c65f6e228f9cefc8bdf62136b7fb69426a`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0477-INTAKE` is only provisional worker
state `[_]`: `intake-receipt.json` is not content-addressed, declares `accepted: false`, and has no
accepted receipt ID. Its recorded blueprint and execution-DAG hashes also predate the current
authority. The intake can guide this fail-closed inspection, but it is not master-accepted evidence
for a statement transition.

Independently and decisively, the exact source proposition is absent. The complete catalog record
names the Chinese remainder theorem and says only `同余方程组的解法`, a method or solution for
systems of congruences. It supplies no bibliography, exact theorem passage, incorporated
definitions, ordered binders, hypotheses, conclusion, proof boundary, translation, correction or
errata review, or independent approval. Its `已验证` label is untrusted metadata under rev-5.6.

The gloss does not select the historical Sunzi residue problem or a modern general theorem. It does
not fix natural, integer, `ZMod`, or quotient-ring carriers; two equations or an indexed family;
finite or potentially infinite scope; pairwise coprimality or general gcd compatibility; positive,
nonzero, signed, or zero-modulus conventions; existence or a constructed witness; uniqueness modulo
a product or lcm; a bounded representative; or empty, singleton, duplicate-index, repeated-modulus,
unit, and incompatible-system cases. Each choice changes the proposition.

Pinned mathlib exposes several materially different candidates: a compatible two-natural-modulus
construction, its coprime specialization, list and finset constructions, a two-factor `ZMod` ring
equivalence, and a general quotient-ideal equivalence. Choosing any one merely because it elaborates
would narrow, broaden, or substitute the received target. It would also override the intake's
explicit null `canonical_statement` and null canonical formal target.

Rev-5.6 sections 5 and 5.1 therefore fail closed at exact immutable source-statement identity and
scope freeze. There is no honest canonical Lean expression whose imports can be certified minimal,
no expression or environment-expression fingerprint to preserve, and no approved alternate
encoding to transport. The required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations are not meaningful rather than passed. Lifecycle stays `planned`; the root
vector stays `[H5, M4, R4]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` was re-elaborated with the existing pinned environment. Its
two imports expose these distinct surfaces:

```text
Nat.chineseRemainder' :
  a congruent to b modulo gcd n m ->
  {k // k congruent to a modulo n and k congruent to b modulo m}

Nat.chineseRemainderOfList :
  pairwise-coprime natural moduli in a list -> a simultaneous natural solution

ZMod.chineseRemainder :
  m.Coprime n -> ZMod (m * n) equivalent as a ring to ZMod m x ZMod n
```

The probe also checks coprime, finset, boundedness, and uniqueness interfaces. It exits successfully
with stdout SHA-256
`0e5ad70cfd1ae07bf4b9b7f7c98db7e0cffc250a8bbd598f1a164a9c2cfa872a`; the three diagnostic axiom
reports are `[propext, Classical.choice, Quot.sound]`. This authenticates candidate APIs only. It
does not select a canonical target, certify minimal imports for one, check a source transport, or
provide proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0477` | 0 | rank 1358; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0477/IntakeProbe.lean` | 0 | eleven distinct CRT interfaces elaborated; diagnostic axioms and stdout hash recorded above |
| `python3 -B Stage1_Instances/THM-M-0477/check_intake.py` (before adding blocker artifacts) | 0 | planned intake invariants passed at `[H5, M4, R4]` with six open tasks |
| same historical intake checker after adding blocker artifacts | 1 | expected inventory assertion: it is intentionally frozen to the original nine-file intake and is not a statement validator |
| bounded `rg` search for Chinese-remainder interfaces in repo-local Lean and pinned mathlib | 0 | found multiple incompatible exact-topic API families and no source-selected repository target |

Final JSON invariants, prohibited-construct hygiene, scoped whitespace checks, and confirmation that
the worker self-test handoff is absent are recorded in `statement-blocker.json` after finalization.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before accepting a later
statement transition. Accountable reviewers must preserve and hash one lawful immutable primary or
authoritative source, distinguish the historical problem or method from a later theorem, and
independently approve one exact passage with every incorporated definition, carrier, ordered
binder, family index, compatibility or coprimality premise, modulus convention, conclusion,
uniqueness or representative clause, proof boundary, translation, correction, erratum, and
degenerate case. A fresh statement worker can then encode that same claim, minimize pinned imports,
serialize and hash the elaborated expression and environment, compile each credited transport, and
run all four required mutation classes.

This is truthful blocker evidence for the assigned attempt only. No statement receipt,
`.stage1-worker-selftest.json`, worker `[_]`, statement fingerprint, debt reduction, proof credit,
audit completion, theorem completion, or master acceptance is claimed.
