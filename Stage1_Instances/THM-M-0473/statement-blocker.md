# THM-M-0473 exact-statement gate: blocked

Item: `S56-M-0473-STATEMENT`

Base revision: `997541734bb32f987fb15f163335a82512992120` (tree
`2c866b9d840d48c48ac839740c62d3b9440be0e5`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0473-INTAKE` is only in provisional
worker state `[_]`: `intake-receipt.json` has `accepted: false`, is not content-addressed, and has
no accepted receipt IDs. It also binds older blueprint and execution-DAG hashes. It is useful
discovery input, but it is neither current accepted dependency evidence nor authority for an exact
statement transition.

More importantly, the intake deliberately leaves `canonical_statement`, `canonical_claim`, the
ordered binders and quantifiers, the Lean module and declaration or expression, the elaborated
expression hash, and the canonical-target environment fingerprint unresolved. The entire catalog
claim is `ax+by=gcd(a,b)` has integer solutions. It does not say whether `a` and `b` are integers
or naturals, formally quantify any variable, define the sign and ambient type of `gcd(a,b)`, fix
the cast of a nonnegative gcd to the integers, order the binders or products, orient the equality,
or resolve negative inputs and `(0,0)`. It supplies no primary or authoritative edition and
theorem/page, correction or errata audit, or independent statement review.

Two familiar propositions fit the gloss but are different formal targets:

```text
forall a b : Int, exists x y : Int,
  (Int.gcd a b : Int) = a * x + b * y

forall a b : Nat, exists x y : Int,
  (Nat.gcd a b : Int) = (a : Int) * x + (b : Int) * y
```

The first covers signed inputs; the second narrows the input domain. Reversing the equality would
more literally follow the displayed equation but would be another proposition-level choice.
Selecting any of these at this phase would override the intake's explicit source-selection
boundary and silently supply proposition-changing mathematics. A broader Euclidean-domain or
Bezout-ring result, or a coprime-only specialization, would be a substituted theorem.

Rev-5.6 therefore fails closed at exact source-statement identity and scope freeze. There is no
truthful canonical Lean expression whose imports can be certified minimal, no expression or
environment fingerprint to preserve, and no approved alternate encoding to transport. The
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are
not meaningful rather than passed. The root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` was re-elaborated against the existing pinned environment.
Its sole direct import, `Mathlib.Data.Int.GCD`, exposes `Nat.gcd_eq_gcd_ab` and
`Int.gcd_eq_gcd_ab`. The probe kernel-checks existential wrappers for both candidate domains and
the integer `(0,0)` case. Both candidate axiom reports list only `propext` and `Quot.sound` in this
environment. This confirms a usable `M3` statement surface; it does not choose the canonical
domain, establish source fidelity, certify minimal imports for a missing target, or provide proof
credit for an unselected root.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The toolchain and Lake manifest SHA-256 values are
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
The automation-provided canonical `.lake` symlink was used read-only. No dependency update, build,
clone, fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0473` | 0 | rank 1355; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `pwd; git status --short --untracked-files=all; git rev-parse HEAD 'HEAD^{tree}'` | 0 | worker clone confirmed; pre-edit status contained only the automation-provided untracked `Formalizations/Lean/.lake`; base revision and tree appear above |
| `git blame -L 3476,3481 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'; git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0473/IntakeProbe.lean` | 0 | eight gcd/coefficient APIs elaborated; natural-input and integer-input existential wrappers plus `(0,0)` checked; stdout SHA-256 `a45cf152d82a94f2075a2ee7feb63cca3426b73a13b2e2f053dc0e1c07aa5fed`; no canonical target was selected |
| `python3 -B Stage1_Instances/THM-M-0473/check_intake.py` | 1 | historical intake validator rejected the integration-updated authoritative intake state `[_]` at its intake-time `[ ]` assertion; it is not statement evidence and was not modified |
| prohibited Lean declaration scan over `Stage1_Instances/THM-M-0473/*.lean` | 0 | inner `rg` returned the expected no-match exit 1; no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration was found |

The historical intake validator is bound to the earlier repository base, authority hashes, exact
nine-file intake inventory, and intake-time `[ ]` state. Its fail-closed result after master
projection changed the intake to `[_]` is recorded rather than hidden; repairing it would exceed
this statement-only assignment.

## Retry Condition And Status Boundary

The integration lane must accept current intake evidence before an accepted statement transition.
Accountable reviewers must preserve and hash a lawful immutable primary or authoritative source,
pinpoint and independently approve one exact proposition, and freeze the input and coefficient
domains, nonnegative-gcd definition and cast, ordered binders, equality and multiplication
orientation, negative and zero cases, proof boundary, and correction or errata disposition. A
later statement run can then encode only that claim, minimize its pinned imports, serialize the
elaborated expression and environment, compile every credited transport, and execute all four
mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
No canonical target, statement fingerprint, statement receipt, root worker self-test packet,
worker `[_]`, master acceptance, proof credit, audit completion, or theorem completion is claimed.
Because the assigned phase did not pass its completion gate, no `.stage1-worker-selftest.json` is
emitted.
