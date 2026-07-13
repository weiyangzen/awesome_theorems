# Exact-statement gate: blocked

Item: `S56-M-0481-STATEMENT`

Theorem: `THM-M-0481` (Bertrand's postulate)

Base revision: `be8701e88e791545c16a262edd1909486d5cef4b` (tree
`78b0a751473bf6d71f453a6aad18b130268a3428`).

## Decision

The exact Lean 4 target cannot yet be truthfully selected. The statement item remains `[ ]`.
Its prerequisite `S56-M-0481-INTAKE` has provisional worker state `[_]`, not master-accepted state
`[x]`; its receipt is unaccepted and not content-addressed. Rev-5.6 permits dependency-ordered
inspection of provisional work, but not dependency closure.

The independent statement blocker is mathematical identity. The repository gives only the uncited
gloss `n与2n之间必有素数` ("there is a prime between `n` and `2n`"). It specifies no domain,
positivity premise, or interval convention. These omissions change the proposition. An unrestricted
natural-number reading is false at `n = 0`. The positive half-closed formulation holds at `n = 1`
with `p = 2`, while the strict formulation `n < p < 2*n` fails there and normally starts at
`1 < n`.

Pinned mathlib exposes the familiar half-closed candidate

```text
(n : Nat) -> n != 0 ->
  Exists fun p => Nat.Prime p and n < p and p <= 2*n.
```

Calling that theorem Bertrand's postulate does not authorize silently adding its domain, premise,
or inclusive endpoint to the sparse catalog. Choosing it, the strict form, an integer domain, or an
interval/counting encoding now would invent or substitute proposition-changing clauses. The intake
accordingly leaves its canonical statement, formal target, binders, hypotheses, imports, expression
hash, and target-environment fingerprint null.

There is therefore no approved expression whose imports can be certified minimal, no credited
alternate form for a checked transport, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation suite. Those outputs are undefined, not passed. The
root vector remains `[H1, M3, R4]`; no debt change is proposed.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` imports `Mathlib.NumberTheory.Bertrand`. Against
pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, it elaborates:

- `Nat.exists_prime_lt_and_le_two_mul` and its alias `Nat.bertrand`;
- the large-number branch `Nat.exists_prime_lt_and_le_two_mul_eventually`;
- the small-number support API `Nat.exists_prime_lt_and_le_two_mul_succ`;
- the candidate at `n = 1`, the false unrestricted case at `n = 0`, and the false strict case at
  `n = 1`.

This is real kernel-checked discriminator evidence. It demonstrates why the unresolved choices are
material; it does not make those choices, identify an exact source proposition, declare a canonical
target, certify minimal imports for an absent target, or supply target-proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` link was used
read-only. No `lake update`, `lake build`, dependency clone or fetch, or other dependency mutation
was performed.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0481` | 0 | rank 1362; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| `git blame -L 3532,3537 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}' 'HEAD:Mathlib/NumberTheory/Bertrand.lean'` and package status | 0 | pinned revision, tree, and Bertrand source blob recorded in `statement-blocker.json`; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0481/IntakeProbe.lean` | 0 | five interfaces and the candidate plus `n = 0`/`n = 1` boundaries elaborated; stdout 588 bytes; SHA-256 `5011e3aaf4fc58958951774d35f933643348108e6559b87322bc0a71f936f5f5` |
| bounded exact-topic search over the owned dossier, repo-local Lean, and pinned `Mathlib.NumberTheory` | 0 | the positive half-closed theorem, alias, large-number branch, small-number support theorem, and proof architecture were located; no source-identical root was credited |
| `LC_ALL=C TZ=UTC python3 -B Stage1_Instances/THM-M-0481/check_intake.py` | 1 | historical intake replay stops at its frozen assertion that intake authority is `[ ]`; integration now records provisional `[_]` with one attempt; it was not rewritten or represented as passing |
| `python3 -m json.tool Stage1_Instances/THM-M-0481/statement-blocker.json` plus scoped semantic assertions | 0 | valid JSON; identity, blocked state, null target/imports, unchanged vector, undefined mutations, false completion flags, exact two-file scope, and absent self-test agree |
| prohibited Lean declaration scan over `Stage1_Instances/THM-M-0481/*.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token was found |
| scoped tracked and per-new-file whitespace checks | 0 | tracked check passed; both no-index checks returned only their expected new-file difference status, with no diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the exact-statement deliverable did not pass |

The historical intake checker is bound to the intake-time repository base, authority state, and
nine-file inventory. Integration has since changed the base and recorded provisional intake state,
and this statement attempt adds two owned artifacts. This known failure is recorded rather than
editing intake evidence to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve, hash, and independently approve one exact primary or authoritative proposition,
including the domain, positivity premise, strict or inclusive upper endpoint, ordered binders,
conclusion encoding, incorporated definitions, translation, proof boundary, corrections or errata,
and the `n = 0`, `n = 1`, and `n = 2` cases.

A fresh statement worker can then encode only that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four mutation classes.

This is a blocked-attempt record, not completion of the assigned node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no node receipt,
statement fingerprint, proof body, proof credit, audit completion, or master acceptance is claimed.
Because the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json` is emitted.
