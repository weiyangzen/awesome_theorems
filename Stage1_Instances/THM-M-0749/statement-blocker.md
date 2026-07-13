# THM-M-0749 exact-statement gate: blocked

- Item: `S56-M-0749-STATEMENT`
- Base revision: `adc87f8ea24dcc7c5e2668c0a5ede0ca5c5f0f55` (tree
  `3c83596059f716cde0d50a5f6b390ada6ca7c8e1`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully completed from the repository's accepted inputs. The catalog says only `Post problem's
affirmative solution`; a separate repository record and a versioned secondary source identify the
usual family as the existence of two computably enumerable sets `A` and `B` with neither Turing
reducible to the other. The intake identifies Friedberg's 1957 and Muchnik's 1956 primary
publications, but no immutable primary proof text or reviewed translation, pinpoint definition and
result passage, premise map, proof boundary, correction history, errata disposition, or independent
source review is accepted. Therefore the exact primary-source proposition is not frozen.

The unresolved formal choices also change the proposition rather than merely its notation:

- whether witnesses are predicates, sets, Boolean characteristic functions, enumeration domains,
  partial functions, or quotient degrees;
- which c.e. convention is canonical and how it is related to mathlib's `REPred`;
- the total set-oracle encoding required for ordinary set Turing reducibility, including the
  membership bit convention and any classical decidability or coding policy;
- ordered existential binders and the exact two nonreducibility conjuncts;
- whether distinctness, noncomputability, incompleteness, or an intermediate c.e. degree is part of
  the root conclusion or only a checked consequence; and
- the foundation, extensionality, quotient, carrier, empty/finite/computable/equal/complete-set, and
  other boundary-case policies.

Selecting one modern convention would invent fields that the source and intake deliberately leave
open. Replacing the target by intermediate-degree existence, unrestricted Kleene-Post
incomparability, a different reducibility, or generic order-theoretic incomparability would
substitute a different theorem. Consequently there is no canonical expression on which to certify
minimal imports, serialize an elaborated-expression fingerprint, compile credited transports, or
run the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations. Those tests are undefined, not passed. The root remains `[H1, M4, R4]`.

The execution DAG projects the intake dependency as provisional `[_]`, while its receipt declares
`accepted: false`, is not content-addressed, and supplies no accepted receipt ID. Dependency-ordered
investigation is useful, but eventual statement acceptance still requires a fresh master-accepted
intake and source/encoding decisions.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports `Mathlib.Computability.TuringDegree` and
`Mathlib.Computability.Halting`, checks adjacent APIs, and proposes a positive-information partial
oracle

```text
fun n => Part.assert (A n) (fun _ => Part.some n)
```

This is not the total characteristic oracle of a set. More strongly,
`StatementBlockerProbe.lean` proves in the pinned kernel that `REPred A` makes this partial oracle
`Nat.Partrec`, and hence `Nat.Partrec.turingReducible` reduces it to every oracle. The exact
prospective c.e.-incomparability expression from intake is therefore inconsistent. It cannot be
promoted to the Friedberg-Muchnik statement. A future statement phase must source and justify a
genuine total set-oracle representation rather than silently changing this definition.

The blocker probe has exactly the two direct imports above. It is evidence against the prospective
encoding, not a canonical target or proof of incomparable c.e. degrees. A bounded search found no
named Friedberg-Muchnik, Post-problem, or c.e.-degree incomparability declaration in pinned mathlib
or shared repo-local Lean. This is only a narrow feasibility result, not the downstream anchor
audit or a global absence claim.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided canonical `.lake` symlink
was used read-only. No update, build, clone, fetch, or other dependency mutation was run.

## Validation evidence

Commands ran from the worker clone on 2026-07-13 (Asia/Shanghai), except where a different working
directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0749` | 0 | rank 1335; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are above |
| scoped reads of the blueprint, execution skill, guidelines, manifest, DAG, catalogs, Stage0 records, and complete intake dossier | 0 | target family identified, but primary-source statement and proposition-critical representations remain open |
| `git blame -L 5521,5526 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0749/IntakeProbe.lean` | 0 | adjacent APIs and prospective expression elaborated; stdout 525 bytes, 11 lines, SHA-256 `fa572fa...d2681`; no canonical target |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0749/StatementBlockerProbe.lean` | 0 | three blocker declarations elaborated; stdout 603 bytes, 9 lines, SHA-256 `cb118c15...a17c7` |
| bounded exact-topic `rg` over pinned mathlib and shared Lean | 1 | expected no-match exit; no named target declaration located |
| prohibited-construct `rg` over owned Lean | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless constant, opaque declaration, or unsafe declaration |
| `python3 -B Stage1_Instances/THM-M-0749/check_intake.py` | 1 | historical intake checker rejects the evolved blueprint hash; this statement phase did not rewrite historical intake evidence |

The intake checker is phase-local historical evidence. It freezes the intake-time blueprint digest
and exact original inventory; current authority and this statement attempt have evolved. This
known freshness failure is recorded rather than modifying the checker or intake receipt to
manufacture a pass.

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash immutable primary editions or an approved authoritative statement, pinpoint and
independently approve the exact definitions, result, assumptions, proof boundary, translations,
corrections, and errata, and freeze the witness model, c.e. convention, total set-oracle transport,
reducibility convention, ordered binders, exact conclusion, intermediate-degree relationship,
foundation profile, credited transports, and boundary cases.

A fresh statement run can then encode precisely that claim, prove its representation transports,
minimize pinned imports, serialize and hash the elaborated expression and environment, and run all
four mutation classes. Until then this node remains `[ ]`; `audit_complete` and `theorem_complete`
are false. Because the assigned phase did not pass its completion gate, no
`.stage1-worker-selftest.json`, node receipt, worker `[_]`, proof credit, or master acceptance is
claimed.
