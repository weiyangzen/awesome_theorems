# Exact-statement gate: blocked

Item: `S56-M-0920-STATEMENT`

Theorem: `THM-M-0920`

Base revision: `9c75282d42a7ef447d885d1d56997a79418bcd8a` (tree
`cc5285432a02107fadffb68c698690d1b98ac5f2`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0920-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`; the intake receipt declares `accepted: false`, is not
content-addressed, and has no accepted receipt ID. Rev-5.6 section 10.2 permits this
dependency-ordered inspection while concurrency is enabled, but any statement acceptance remains
dependency ordered.

Independently and decisively, the exact-statement gate fails. The repository supplies only the
Chinese title `安德鲁斯分裂定理`, attributes it to George Andrews in 1974, and gives the gloss
`分拆函数的进一步推广` (a further generalization of the partition function). It gives no
bibliography, formula, incorporated definitions, ordered binders, hypotheses, conclusion, proof
boundary, correction history, or boundary convention. The title also uses the ordinary Chinese
word for "splitting" while the gloss uses the word for integer partition. Its `已验证` label is
untrusted metadata under rev-5.6.

The intake correctly leaves the canonical mathematical claim and Lean expression null. The record
can denote materially different roots, including:

- Theorem 1 of Andrews' 1974 PNAS paper as an analytic multiple-series/product identity for odd
  moduli;
- a coefficientwise formal-power-series rendering of that identity;
- a combinatorial Andrews-Gordon equality between two source-defined restricted-partition
  families;
- an exact result or corollary from Andrews' distinct 1974 AMS Memoir *On the general
  Rogers-Ramanujan theorem*; or
- another Andrews partition result selected by an accountable correction of the catalog record.

The PNAS paper is the strongest inspected lead. Its Theorem 1 states, for integers `1 <= i <= k`,
a `(k-1)`-fold Eulerian series/product identity involving cumulative indices, q-Pochhammer
denominators, whose product side ranges over exponents outside residue classes `0`, `i`, and `-i`
modulo `2*k+1`. The catalog does not cite that article or distinguish its analytic identity from a
combinatorial coefficient statement. The separate 1974 AMS Memoir creates a genuine competing
source boundary. Neither has been adopted through immutable source admission, complete
definition/premise/correction mapping, and independent review. Selecting either would substitute
proposition-changing mathematics.

Even after source selection, the statement must resolve every parameter and summation range, the
cumulative-index and q-Pochhammer definitions, analytic versus formal semantics, the carrier and
convergence premise for `q`, the infinite-product convention, the residue predicate, ordered
binders, and cases such as `k = 0`, `i = 0`, `i > k`, empty tuples and products, `q = 0`, `q = 1`,
roots of unity, the empty partition, and `n = 0`. It must also distinguish this target from the
classical Rogers-Ramanujan target `THM-M-0918` and Gordon's theorem `THM-M-0919`.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression
fingerprint hard blockers. There is consequently no honest canonical Lean target whose imports can
be certified minimal, no credited alternate encoding, and no meaningful removed-hypothesis,
changed-domain, changed-binder-scope, or boundary-case mutation suite. Those mutation results are
undefined, not passed. Lifecycle remains `planned`, and the root vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned environment with these two direct
imports:

- `Mathlib.Combinatorics.Enumerative.Partition.GenFun`
- `Mathlib.Data.Nat.ModEq`

It checks seven adjacent ordinary/restricted-partition, generating-function, and congruence APIs:
`Nat.Partition`, its `Fintype`, `Nat.Partition.restricted`, `Nat.Partition.genFun`,
`Nat.Partition.coeff_genFun`, `Nat.Partition.hasProd_genFun`, and `Nat.ModEq`. All checks pass. The
probe defines no source-specific multiple sum, q-Pochhammer symbol, infinite product, restricted
partition predicate, canonical target, checked transport, or proof body. Its imports are adjacent
substrate only and cannot be certified minimal for an absent target. The complete probe stdout is
727 bytes with SHA-256
`a97594753144f2051a17f022dfcf4001208d337ec66fbeea6a042e8adf15ff55`; stderr is empty.

A bounded exact-topic search found no Andrews-Gordon, general Rogers-Ramanujan, odd-modulus, or
Eulerian-series target in pinned mathlib or repository-local Lean. This is statement-feasibility
evidence only, not the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone, fetch, or other dependency mutation was run; the pinned mathlib worktree remained clean.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0920` | 0 | rank 1462; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base identifiers appear above |
| authority, source, intake, toolchain, lockfile, and imported mathlib `sha256sum` commands | 0 | current input fingerprints are recorded in `statement-blocker.json` |
| `git blame -L 6728,6733 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-0920/check_intake.py` | 1 | historical intake checker stops in `check_authorities`: it freezes intake state `[ ]` and attempts `0`, while the integrated execution DAG records provisional `[_]` and attempts `1` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0920/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; stdout 727 bytes with the hash above; empty stderr; no target theorem |
| bounded exact-topic `rg` search over pinned mathlib and repository-local Lean | 1 (expected no match) | no exact topic declaration matched; discovery only |
| prohibited declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0920/statement-blocker.json` plus scoped invariant checks | 0 | finalized structured blocker parses; identity, null target/imports, unchanged vector, four undefined mutations, false completion fields, two-file scope, and absent self-test agree |
| scoped `git diff --check` plus per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; each no-index exit 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the exact-statement deliverable did not pass |

The intake checker is a historical receipt checker. It binds the earlier intake authority state,
shared-input hashes, base revision, and original nine-file inventory. This statement attempt
records its exact replay limitation rather than rewriting the intake receipt, checker, instance,
target-local task DAG, generated blueprint, or authoritative execution DAG to manufacture
agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before a future statement can be
accepted. Accountable reviewers must correct or confirm the catalog title; preserve and hash one
lawful immutable primary or approved authoritative source; select and independently approve one
exact result; and transcribe every incorporated definition, ordered binder, hypothesis,
conclusion, proof boundary, correction, erratum, and boundary case. They must freeze analytic
versus formal versus combinatorial scope, all multiple-sum/product and residue conventions,
parameter and convergence contracts, checked transports, and neighboring-target boundaries.

A fresh statement attempt can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
