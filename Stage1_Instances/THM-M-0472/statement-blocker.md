# THM-M-0472 exact-statement gate: blocked

Item: `S56-M-0472-STATEMENT`

Base revision: `464759128569180ab640c412cd80bc5dd2c3b44a` (tree
`8da3c9130640d08d4e179450a0418368d0454745`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0472-INTAKE` is only in provisional
worker state `[_]`: `intake-receipt.json` has `accepted: false`, is not content-addressed, and has
no accepted receipt IDs. It is also bound to an older repository base and older authority hashes.
The intake is useful discovery evidence, but it is neither master-accepted dependency evidence nor
authority for an exact statement transition.

More importantly, the received catalog claim is only `求最大公约数的算法`, "an algorithm for
finding the greatest common divisor." It supplies no truth-valued proposition. It does not choose
natural, positive, or signed inputs; subtraction versus remainder presentation; quotient and
remainder convention; pair orientation; stopping rule or termination measure; recurrence,
termination, total correctness, trace correctness, or program refinement as the root; ordered
binders and hypotheses; or `(0,0)`, one-zero, equal, divisible, and relatively-prime boundaries.
It cites no edition, proposition and proof locator, incorporated definitions, translation or
errata audit, or independent review that licenses one of those choices.

The existing intake therefore deliberately leaves `canonical_statement`, `canonical_claim`,
ordered binders, quantifiers, the Lean module and declaration or expression, the elaborated
expression hash, and the canonical-target environment fingerprint unresolved. Selecting the
familiar recurrence

```text
forall m n : Nat, Nat.gcd m n = Nat.gcd (n % m) m
```

would state equality preservation but not the termination and full returned-value contract of an
independently described algorithm. Selecting a bundled natural-number total-correctness contract,
an explicit trace refined to `Nat.gcd`, Euclid's repeated-subtraction construction, a signed-integer
algorithm, or an abstract Euclidean-domain algorithm would make other proposition-changing choices.
None can truthfully be substituted for the absent source-selected root.

Rev-5.6 consequently fails closed at exact source-statement identity and algorithm-contract scope.
There is no canonical expression to elaborate, no honest minimal-import result, no expression or
environment fingerprint to serialize, and no approved alternate encoding to transport. The
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are
undefined rather than passed. The root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` was re-elaborated against the existing pinned environment.
Its sole declared import, `Init.Data.Nat.Gcd`, exposes `Nat.gcd`, its base and recurrence equations,
well-founded induction, both direct divisibility results, the greatest-common-divisor constructor,
and the universal gcd characterization. The pinned recurrence orientation is
`(m,n) -> (n % m,m)`. The probe kernel-checks recurrence and characterization wrappers plus zero
and `(48,18)` boundary examples. Both printed axiom reports list `propext` and `Quot.sound`.

This confirms a narrow usable `M3` candidate surface. It does not select a canonical root, make
`Init.Data.Nat.Gcd` a minimal import for an absent target, establish source fidelity, audit the
logical-model/runtime-override boundary, or provide proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The toolchain and Lake manifest SHA-256 values are
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
The automation-provided canonical `.lake` symlink was used read-only. No update, build, clone,
fetch, or dependency mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0472` | 0 | rank 1354; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `pwd; git status --short --untracked-files=all; git rev-parse HEAD 'HEAD^{tree}'` | 0 | worker clone confirmed; pre-edit status contained only the automation-provided untracked `Formalizations/Lean/.lake`; base revision and tree appear above |
| `git blame -L 3469,3474 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'; git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0472/IntakeProbe.lean` | 0 | nine gcd APIs, recurrence and correctness wrappers, and boundary checks elaborated; stdout SHA-256 `6e0a37a3e493bb3e2c64443649682c2a0af9e1f0000ca7e6d113b9404116f51c`; no canonical target selected |
| `python3 -B Stage1_Instances/THM-M-0472/check_intake.py` | 1 | historical intake validator rejected the integration-updated authoritative intake state `[_]` at its intake-time `[ ]` assertion; it is not statement evidence and was not modified |
| prohibited Lean declaration scan over `Stage1_Instances/THM-M-0472/*.lean` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, unsafe declaration, or placeholder marker was found |

The historical intake validator is bound to its earlier base and authority hashes, exact nine-file
intake inventory, and intake-time authoritative `[ ]` state. Its fail-closed result after authority
changed the intake to `[_]` is recorded rather than hidden. Repairing historical intake evidence
would exceed this statement-only assignment.

## Retry Condition And Status Boundary

The integration lane must first accept fresh intake evidence. Accountable reviewers must lawfully
preserve and hash an immutable primary or approved authoritative source, pinpoint and independently
approve one exact proposition, and freeze domains, algorithm presentation and orientation,
division convention, termination and output contract, ordered binders, every boundary case, proof
scope, translation, corrections, and errata. A later statement run can then encode only that claim,
minimize its pinned imports, serialize its elaborated expression and environment, compile every
credited transport, and execute all four mutation classes.

This is truthful blocker evidence for the assigned statement attempt, not completion. No canonical
target, statement fingerprint, statement receipt, worker `[_]`, master acceptance, proof credit,
audit completion, or theorem completion is claimed. Because this phase did not pass its completion
gate, no `.stage1-worker-selftest.json` is emitted.
