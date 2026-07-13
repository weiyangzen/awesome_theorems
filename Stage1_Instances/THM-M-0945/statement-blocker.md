# Exact-statement gate: blocked

Item: `S56-M-0945-STATEMENT`

Theorem: `THM-M-0945`

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b` (tree
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`).

Worker context: isolated Stage1 rev-5.6 automation worker `slot18`. The run is nonrelease evidence:
the automation `.lake` symlink was already untracked, and the two blocker artifacts are the owned
untracked handoff. Their bytes must be rehashed by integration rather than self-hashed recursively.

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0945-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered
investigation, but the intake receipt declares `accepted: false`, contains no accepted receipt ID,
and deliberately leaves the canonical mathematical statement and Lean target null. Master
acceptance remains necessary before a future statement transition can be accepted.

Independently, the exact-statement gate cannot pass without inventing proposition-changing
conventions. The catalog supplies the Green-Tao name, Ben Green and Terence Tao attribution, the
year 2004, and the slogan "the primes contain arbitrarily long arithmetic progressions." It does
not cite an exact theorem passage, define a progression or prime carrier, order the binders, state
nondegeneracy or infinite-many semantics, resolve small lengths, or bind corrections and errata.
Its `verified` label is untrusted under rev-5.6.

The matching primary-source lead is precise enough to identify the family but has not been adopted
as the canonical target. Green and Tao, *The primes contain arbitrarily long arithmetic
progressions*, *Annals of Mathematics* 167(2) (2008), 481-547, DOI
`10.4007/annals.2008.167.481`, states in Theorem 1.1 on printed page 482 that the prime numbers
contain infinitely many arithmetic progressions of length `k` for all `k`. The proof on printed
page 524 discards the degenerate common-difference-zero case. The inspected publisher PDF had
SHA-256 `967dd6f5bb53d70abdbb07be0afe59e60b2a232e2c3387966013a09960e52c89`.

That remote PDF is discovery input, not a repository-admitted immutable source with independent
review. The dossier has not approved the domain or lower bound for `k`; `Nat` versus positive
integer primes; witnesses `a` and `d`; zero-based versus one-based indexing; positive versus merely
nonzero difference; pairwise distinctness; ordered binders; or a direct encoding of infinitely many
progressions versus an existence-only consequence. It also has not reconciled the 2004 preprint,
2007 revision, 2008 publication, later corrections and errata, or all cases `k = 0`, `1`, and `2`.
Each choice changes the Lean expression. Choosing one here would substitute worker judgment for an
accepted source statement.

Sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard blockers.
There is consequently no canonical expression for which minimal imports, checked transports, or
the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
can be certified. All four mutation classes are undefined, not passed. No `Statement.lean`, proof
body, weakened existence-only theorem, broadened interface, circular premise, or placeholder was
added. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Its three direct imports expose eight adjacent
interfaces: `Nat.Prime`, prime infinitude, three-term-progression-free sets, Roth's natural-number
theorem and asymptotic extremal form, and finite-color line or homothetic-copy results.

All eight checks pass; stdout has SHA-256
`648f295c23e22218182d2e2144de0b867275960a7f11a3e9a8222210c9c961a7`. None states that primes
contain arbitrary-length progressions. A bounded pinned/repo-local search found no source-identical
target declaration; the non-probe matches concern Dirichlet's distinct theorem on primes in one
fixed residue class. This is discovery-only evidence, not the downstream anchor audit or a global
absence claim. The probe imports cannot be certified minimal for an absent canonical target.

The automation-provided `Formalizations/Lean/.lake` symlink was used read-only. No dependency
update, build, clone, fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0945` | 0 | rank 1484; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped manifest, blueprint, DAG, skill, guidelines, catalog, Stage0, intake, and precedent inspection | 0 | confirmed current authority agreement, provisional dependency, null canonical target, and unresolved proposition choices |
| `sha256sum` over authority, source, intake, probe, toolchain, lockfile, and pinned mathlib inputs | 0 | exact current hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0945/check_intake.py` | 1 | the historical intake checker expects authoritative intake state `[ ]`; integration advanced it to provisional `[_]`; the intake evidence was not rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision, tree, and worktree-status checks | 0 | the recorded revision and tree agree with the lockfile; dependency worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0945/IntakeProbe.lean` | 0 | eight adjacent interfaces elaborated; stdout hash recorded above; no canonical target or proof body |
| bounded Green-Tao/prime-progression search in pinned mathlib and repository-local Lean | 0 | no source-identical target declaration located; discovery-only evidence |

Final JSON, prohibited-construct, structural, authority, whitespace, and absent-self-test checks are
recorded in the structured blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash an immutable primary or approved authoritative source edition, adopt and
independently approve the exact Theorem 1.1 proposition and incorporated conventions, reconcile
corrections and errata, and freeze the length domain, prime carrier, progression representation,
indexing, positive common difference, binder order, infinitely-many semantics, checked transports,
and every boundary case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
