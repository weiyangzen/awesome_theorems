# Exact-statement gate: blocked

Item: `S56-M-1597-STATEMENT`

Theorem: `THM-M-1597`

Base revision: `db6914155f1f63e835364b89ba0a3b25f1d7f936` (tree
`a5488edccb2687c4ff0bbdccf4650e06b2e45337`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1597-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. More importantly, the intake deliberately freezes no
canonical proposition: the repository record says only `RSA加密` (RSA encryption) and `公钥加密系统`
(public-key cryptosystem). A system name and purpose are not a truth-valued theorem with ordered
binders, hypotheses, and a conclusion.

The catalog does not choose among construction, one or both round-trip correctness laws, an inverse
permutation result, signature correctness, efficient implementation, private-key recovery,
factoring hardness, or a modern security property. It also does not fix distinctness of the primes,
the exponent equation, the message and ciphertext carriers, modular-reduction conventions,
padding, adversary or cost models, or boundary cases. Selecting textbook RSA correctness, a
security theorem, or the distinct `THM-C-0201` record would broaden or substitute the received
target.

The inspected Rivest-Shamir-Adleman paper is a primary-source lead, not an admitted canonical root.
Sections II and V-VI contain a plausible all-message inverse-permutation theorem, while Sections VII
and IX concern algorithms and unproved security claims. The repository does not select the Section
VI result. Its obvious formal reading also needs a truth-critical distinct-primes correction: for
`p = q = 3`, `e*d = 5`, and `M = 2`, the exponent congruence modulo `(p-1)(q-1) = 4` holds, but
`2^5` is not congruent to `2` modulo `9`. The exact edition, correction and errata record,
definition chain, proposition boundary, and independent review remain open.

There is therefore no honest canonical Lean expression whose imports can be certified minimal, no
canonical expression or environment fingerprint, and no approved alternate encoding. The required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are not
meaningful until a proposition is lawfully selected. The root vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with these direct imports:

- `Mathlib.Data.Nat.ModEq`
- `Mathlib.Data.Nat.Totient`
- `Mathlib.NumberTheory.PowModTotient`
- `Mathlib.Data.ZMod.Basic`

It checks nine modular-congruence, totient, exponent-reduction, and Chinese-remainder interfaces.
All checks pass in the pinned environment. A bounded repo-local and pinned-mathlib search found no
exact RSA declaration. The totient exponent interfaces require a coprime base and therefore cannot
alone prove the possible all-message result. The probe declares no target, checked transport, or
proof body, and its imports cannot be certified minimal for an absent canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1597` | 0 | rank 1217; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | before this attempt, only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 11763,11768 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short`; `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean; pinned revision and tree recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1597/IntakeProbe.lean` | 0 | nine adjacent interfaces elaborated; two representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `rg -n -i '(\bRSA\b\|Rivest\|Shamir\|Adleman\|public[- ]key.{0,40}(crypt\|encrypt)\|encrypt.{0,40}decrypt\|decrypt.{0,40}encrypt)' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 (expected) | no exact RSA declaration or topic match in the searched Lean sources; bounded discovery only, not an anchor audit or absence proof |
| `python3 -B Stage1_Instances/THM-M-1597/check_intake.py` | 1 | the historical intake validator is stale against the integration-updated intake state `[_]` and freezes the original nine-file intake inventory; it is not statement evidence and was not modified |
| prohibited-declaration scan over owned `*.lean` files | 0 | the inner search returned expected no-match exit 1; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration was found |
| `python3 -m json.tool Stage1_Instances/THM-M-1597/statement-blocker.json` plus scoped invariant check | 0 | JSON identity, null target/imports/fingerprints, four unrunnable mutations, unchanged vector, false completion fields, and no-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-1597` plus per-new-file `git diff --no-index --check /dev/null PATH` | 0 | no whitespace diagnostics; no-index exit 1 means only that each file is new |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the statement deliverable did not pass |

The intake checker is bound to the intake-time authoritative hashes and original file inventory.
The integration lane has since recorded intake as `[_]`; adding statement artifacts also correctly
exceeds that intake-only inventory. Its fail-closed exit is recorded rather than repaired or
represented as statement validation.

## Retry Condition And Status Boundary

The integration lane must master-accept a suitable intake dependency. Accountable reviewers must
also lawfully preserve and hash an immutable primary or authoritative source, select and
independently approve one exact proposition, and transcribe every incorporated definition, ordered
binder, hypothesis, conclusion, correction, proof boundary, and boundary case. They must decide the
construction/correctness/signature/security/complexity boundary; prime, exponent, message, and
modular contracts; one or both inverse directions; padding and randomness; and every degenerate
case without borrowing scope from `THM-C-0201`.

A later statement run can then encode precisely that claim, minimize its pinned imports, serialize
the elaborated expression and environment, compile every credited transport, and execute all four
mutation classes. This blocker is the assigned phase's truthful result, not completion of the
statement node or any downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, master acceptance, statement fingerprint, or proof credit is
claimed.
