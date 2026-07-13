# THM-M-0926 exact-statement gate: blocked

- Item: `S56-M-0926-STATEMENT`
- Base revision: `b243ebc0f9058ba5afafef8240b92c2dfb2edc6e`
- Base tree: `b4b092069141ac54ea1ab5a6ea946192a30ec78c`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully selected from the authoritative repository record.
The record gives the title `卡西尼恒等式` (Cassini's identity), attributes it to Cassini in 1680,
and says only `斐波那契数列的恒等式` (an identity of the Fibonacci sequence). It contains no
formula, Fibonacci definition, index or value domain, lower bound, ordered binder, equation
orientation, sign convention, exponent convention, source locator, proof boundary, correction, or
erratum. The catalog's `已验证` label is untrusted under rev-5.6.

The intake dossier therefore deliberately leaves `canonical_statement`, `canonical_claim`, the
canonical Lean module and expression, the expression hash, and the target environment fingerprint
null. It records the familiar formula family

```text
F_(n-1) * F_(n+1) - F_n^2 = (-1)^n
```

only as an uncredited lead. Before that formula can become the root, accountable reviewers must
choose and approve a source, zero- or one-based Fibonacci convention, natural/positive-natural/
integer index domain, value carrier and coercions, lower bound, sign and equation orientation,
exponent representation, shifts, and the treatment of zero and negative indices. These are
proposition-changing choices, not notation that a statement worker may silently fill in.

Pinned mathlib's all-integer theorem is likewise a strong formal candidate rather than statement
authority. It fixes an integer extension and uses `n.natAbs` in the exponent. Installing it as the
root would broaden a usual positive-natural reading and resolve every open convention without an
approved source-to-target correction. A natural predecessor form, rearranged equality, shifted
form, Catalan identity, or finite numerical case would also be a different or stronger/weaker
proposition and cannot substitute for this target.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression
fingerprint hard blockers. With no canonical proposition, there is no honest target for which to
certify minimal imports, compile credited transports, or run the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations. Those mutations are undefined,
not passed. No `Statement.lean`, theorem declaration, assumed predicate, wrapper, or proof body was
added.

The prerequisite `S56-M-0926-INTAKE` is also only provisional worker state `[_]`, not
master-accepted `[x]`. Its receipt is unsigned, non-content-addressed, has `accepted: false`, and
contains no accepted receipt ID. Dependency-ordered investigation is possible, but neither that
receipt nor the current source boundary supports an accepted statement transition.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` imports
`Mathlib.Data.Int.Fib.Lemmas`. A fresh replay with the existing pinned artifacts elaborated the
public candidate:

```lean
Int.fib_succ_mul_fib_pred_sub_fib_sq (n : Int) :
  Int.fib (n + 1) * Int.fib (n - 1) - Int.fib n ^ 2 = (-1) ^ n.natAbs
```

It also elaborated adjacent `Int.fib`, `Nat.fib`, recurrence, cast, and Catalan interfaces. The
candidate axiom diagnostics reported `propext`, `Classical.choice`, and `Quot.sound`. The complete
probe output was 8,015 bytes with SHA-256
`f7f0d934748edec5e6a13cf5012caa0387ae63c87de616626dd2c546a2d5b9cc`.

This is candidate-availability evidence only. The module is the direct proof-bearing candidate
import, but it is not a minimal-import certificate for an absent canonical target. The probe
declares no canonical `THM-M-0926` target or checked source transport, and its printed upstream body
and axiom report receive no proof credit in this statement attempt.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link to canonical artifacts was used read only. No `lake update`,
`lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai), from the repository root
unless another working directory is shown. Exact arguments, exits, input hashes, and boundaries are
also recorded in `statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0926` | 0 | rank 1545; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| scoped authority, intake, source, and hash inspection | 0 | statement depends on provisional intake; the received claim and intake agree that the exact target, imports, fingerprints, transports, and mutation fixtures are unresolved |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --version && lake --version` | 0 | Lean and Lake versions agree with the pinned environment above |
| mathlib revision, tree, and worktree-status checks | 0 | pinned revision and tree above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0926/IntakeProbe.lean` | 0 | nine candidate interfaces, the upstream body, and two axiom reports elaborated; output digest and size appear above; no canonical target or local proof was declared |
| bounded Cassini search over the owned path, repo-local Lean, and pinned integer-Fibonacci modules | 0 | found the expected pinned Cassini declaration and intake probe; no source-approved `THM-M-0926` target identity was found |
| `python3 -B Stage1_Instances/THM-M-0926/check_intake.py` | 1 | historical intake replay stopped at its stale recorded blueprint hash after integration updated authority; it was preserved and not represented as current statement evidence |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| final JSON parse, scoped blocker assertions, whitespace checks, and absent-self-test check | 0 | the two blocker artifacts agree on identity, unchanged debt, null target/imports, four undefined mutations, false completion flags, and no worker packet |

The historical intake freshness failure is separate from, and weaker than, the decisive
mathematical blocker: even its original provisional snapshot deliberately selected no truth-valued
root. Intake evidence was not rewritten to manufacture freshness or acceptance.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable source and
formal reviewers must lawfully preserve and hash one immutable primary or approved authoritative
source, select or correct one exact truth-valued Cassini proposition, and independently approve its
complete source crosswalk. They must fix the Fibonacci definition, index and value domains, lower
bound, ordered binders, equation and sign orientation, exponent representation, transports,
foundation/TCB/computation profiles, proof and translation boundary, corrections, errata, and all
zero, first-positive, and negative-index cases.

A fresh statement worker can then encode exactly that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H5, M3, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion
gate, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master
acceptance is claimed.
