# THM-M-0911 exact-statement gate: blocked

Item: `S56-M-0911-STATEMENT`

Base revision: `fcabbf1e0ad9507eebe91663bccabfa87d22813e` (tree
`873e589c594454b7f263c7ed2342089a4d15e842`). Attempt date: 2026-07-13
(Asia/Shanghai).

## Decision

The exact Lean 4 target cannot be truthfully frozen from the authoritative repository record. The
catalog supplies only the title binomial theorem, the unreviewed attribution "many mathematicians",
the date "antiquity", and the phrase `(a+b)^n` expansion formula. It gives no bibliography,
edition, theorem/page, quantified coefficient domain, algebraic assumptions, coefficient
convention, exact sum, proof boundary, corrections, errata, or independent review.

These omissions do not leave merely cosmetic notation choices. Pinned mathlib exposes at least
three materially different exact-topic propositions:

```lean
add_pow [CommSemiring R] (a b : R) (n : Nat) :
  (a + b) ^ n =
    ∑ m ∈ Finset.range (n + 1), a ^ m * b ^ (n - m) * (n.choose m : R)

Commute.add_pow [Semiring R] (h : Commute a b) (n : Nat) :
  (a + b) ^ n =
    ∑ m ∈ Finset.range (n + 1), a ^ m * b ^ (n - m) * (n.choose m : R)

Commute.add_pow' [Semiring R] (h : Commute a b) (n : Nat) :
  (a + b) ^ n =
    ∑ m ∈ Finset.antidiagonal n, n.choose m.1 • (a ^ m.1 * b ^ m.2)
```

The first chooses a commutative coefficient algebra. The second instead assumes two commuting
elements of a possibly noncommutative semiring. The third changes the index set, avoids natural
subtraction, and uses natural scalar action rather than a coefficient cast. The catalog does not
select among them. Nor does it fix the exponent order, equality direction, universe and binder
order, or whether a natural, integer, polynomial, real, or complex specialization is intended.

Boundary decisions are also proposition-relevant: `n = 0`, `n = 1`, `a = 0`, `b = 0`, positive
characteristic, the zero semiring, and subsingleton coefficient types must not be silently
excluded. Selecting the familiar commutative-semiring declaration because its name and formula
look convenient would therefore add source and scope decisions that the received target does not
contain. Selecting the stronger commuting-elements or antidiagonal variant would do the same.

The intake correctly leaves the canonical mathematical claim, Lean module and declaration,
ordered binders and hypotheses, expression fingerprint, canonical-target environment fingerprint,
alternate transports, and boundary registry null or open. Without a source-approved canonical
expression, minimal imports cannot be certified and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary mutations are undefined, not passed.

The node remains `[ ]`, the lifecycle remains `planned`, and the vector remains `[H1, M3, R4]`.
No `Statement.lean`, theorem declaration, statement receipt, proof body, axiom, placeholder,
weakened special case, broadened theorem, or substituted result was added.

The prerequisite `S56-M-0911-INTAKE` is independently only provisional `[_]`. Its worker receipt
is unaccepted and non-content-addressed, has no accepted receipt ID, and records an earlier base and
authority hashes. Replaying its historical checker now stops because it expects intake state `[ ]`
while the integrated execution DAG records `[_]`. This statement phase records that boundary
rather than modifying another phase's frozen evidence.

## Pinned Lean boundary

The discovery-only `IntakeProbe.lean` was re-elaborated with its sole direct import,
`Mathlib.Data.Nat.Choose.Sum`. It checked `Nat.choose`, `Commute.add_pow`,
`Commute.add_pow'`, and `add_pow`, as well as:

- the conventional commutative-semiring range-sum candidate;
- definitional agreement between `add_pow` and `(Commute.all a b).add_pow`;
- the range-sum boundary at `n = 0`;
- a range-sum example at `n = 2`; and
- an antidiagonal example at `n = 2`.

The probe passed with stdout SHA-256
`1fca6d3559b745f876989ffe3e68552566c2c0c32ebde377582bea2101e7c2e8`.
The inspected candidate axiom reports contain `propext`, `Classical.choice`, and `Quot.sound`.
This establishes pinned interface feasibility and preserves `M3`; it is not an exact statement
freeze, source transport, minimal-import proof for an absent root, downstream anchor/provenance
audit, or proof credit.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The pinned
`Mathlib.Data.Nat.Choose.Sum` source has SHA-256
`24629e74afa48706f470fccab4c8bfadd229e42e07ce8ba2e192aee4af6d3fe3`.
The automation-provided canonical `.lake` symlink was used read-only. No `lake update`,
`lake build`, dependency clone or fetch, or other `.lake` mutation ran; the pinned mathlib package
remained clean.

## Validation record

Commands ran in this isolated worker clone on 2026-07-13.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0911` | 0 | rank 1453; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided untracked `.lake` symlink existed; base revision and tree are recorded above |
| `git blame -L 6665,6670 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-0911/check_intake.py` | 1 | historical intake replay stops at line 137 because it expects intake authority state `[ ]`, while the current execution DAG records provisional `[_]`; intake evidence was not rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0911/IntakeProbe.lean` | 0 | four exact-topic interfaces and five candidate or boundary examples elaborated; exact stdout hash recorded above |
| bounded exact-topic search of pinned mathlib and repository-local Lean | 0 | the three direct candidates were confirmed in `Mathlib.Data.Nat.Choose.Sum`; no additional repo-local canonical THM-M-0911 statement was located; discovery only |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |
| JSON parse, scoped blocker invariant check, and whitespace checks | 0 aggregate | blocker identity, null target/imports, unchanged vector, false completion fields, exact two-file scope, and formatting agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because statement completion failed |

## Retry condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then lawfully preserve and independently approve one exact primary or authoritative proposition and
map every incorporated definition, ordered binder, hypothesis, conclusion, coefficient algebra,
commutativity premise, coefficient cast or scalar action, finite sum, exponent convention, proof
boundary, correction, erratum, and boundary case.

A fresh statement worker can then encode only that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
`audit_complete: false` and `theorem_complete: false`; no debt-vector change is proposed. Because
the exact-statement deliverable did not pass, `.stage1-worker-selftest.json` is intentionally absent
and no worker `[_]`, statement receipt, proof credit, accepted state, or master acceptance is
claimed.
