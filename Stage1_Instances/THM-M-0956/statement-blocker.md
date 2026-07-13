# THM-M-0956 exact-statement gate: blocked

Item: `S56-M-0956-STATEMENT`

Base revision: `d66b6e80968b53d5b99774584721ae8976f303a5` (tree
`aaa82721074fccea81033a9a18d21652af89f8e4`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0956-INTAKE` is only provisional worker
state `[_]`: `intake-receipt.json` is unaccepted and non-content-addressed, has no accepted receipt
IDs, and is bound to an older base plus older blueprint and execution-DAG hashes. There is no
master-accepted dependency receipt. Dependency-ordered investigation may record this blocker, but
it cannot close the statement node.

Independently and decisively, the exact-source-statement gate fails. The complete repository record
is the title `Erdos-Turan construction`, the Erdos/Turan attribution and 1941 date, and the gloss
`construction of a Sidon set`. It supplies no citation, construction formula, Sidon convention,
ambient domain, parameter restrictions, ordered binders, hypotheses, conclusion, quantitative
bound, boundary cases, proof boundary, correction, erratum, reviewer, or formal artifact. Stage0
explicitly leaves the precise definitions and premises, formal system, proof route, dependencies,
alternate forms, axioms, machine status, and artifact links open. The catalog's `verified` value is
untrusted metadata under rev-5.6.

The intake inspected the matching primary paper: P. Erdos and P. Turan, "On a Problem of Sidon in
Additive Number Theory, and on some Related Problems," *Journal of the London Mathematical
Society* s1-16(4) (1941), 212-215, DOI `10.1112/jlms/s1-16.4.212`. Section I on printed page 213
gives a strong candidate: for prime `p` and `1 <= k <= p - 1`, set

```text
a_k = 2*p*k + r_k,
```

where `r_k` is the least positive residue of `k^2` modulo `p`; the `p - 1` terms are below
`2*p^2` and have distinct sums for distinct unordered index pairs. The paper also records the
extremal corollary `Phi(2*p^2) >= p - 1` and passes to an asymptotic lower bound.

Those clauses identify a result family, not the accepted root. No independent reviewer has verified
the scan transcription, incorporated definitions, proof boundary, corrections or errata. The
catalog does not choose the explicit indexed construction, a finite-set restatement, the extremal
corollary, the asymptotic consequence, or a conjunction. It also does not freeze unique sums with
diagonal pairs versus another Sidon convention; sequence versus `Finset` representation; positive
residue versus natural remainder; ordered versus unordered pairs; strict bounds; prime and index
endpoints; or asymptotic quantifiers. Selecting any of those now would invent, omit, broaden, or
substitute proposition-changing mathematics.

Sections 5 and 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` make statement ambiguity and a missing
elaborated-expression fingerprint hard blockers. The intake therefore correctly leaves the
canonical human claim, Lean module and expression, domains, binders, hypotheses, minimal imports,
and expression and environment fingerprints null at `[H1, M4, R4]`. With no canonical target,
checked transports and the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations are undefined, not passed. No `Statement.lean`, theorem declaration,
assumed Sidon interface, axiom, placeholder, weakened theorem, or broadened theorem was introduced.

## Pinned Lean boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with the existing pinned artifacts.
Its direct imports expose finite sets and intervals, pairwise and injectivity predicates, finite
sums, and natural square roots. All eight checks pass under Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The complete combined output SHA-256 is
`79534f6c65ded867c4c8189d2f7ba92c8b0321e969159f57dca08b77d8b344c3`.

The probe defines no prime parameter, Erdos-Turan sequence, positive-residue convention, Sidon
predicate, extremal function, canonical target, checked transport, or proof body. Its imports cannot
be certified minimal for an absent target and receive no statement or proof credit. A bounded
exact-topic search of repository-local and pinned-mathlib Lean sources found no Sidon or named
Erdos-Turan construction occurrence. This is discovery-only evidence, not the downstream immutable
anchor audit or a global absence claim.

The automation-provided `Formalizations/Lean/.lake` symlink was used read-only. No `lake update`,
`lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`). Exact argument arrays and
results are also preserved in `statement-blocker.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0956` | 0 | rank 1490; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| authority and intake `sha256sum` command recorded in the JSON | 0 | current input fingerprints agree with the structured blocker |
| `python3 -B Stage1_Instances/THM-M-0956/check_intake.py` | 1 | historical intake replay stops at line 137 because it expects intake `[ ]`, while integration now records provisional `[_]`; this phase records rather than rewrites stale evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision, tree, and package-status checks | 0 | revision and tree agree; package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0956/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; combined-output hash recorded above; no canonical target or proof body |
| bounded exact-topic Lean search | 1 | expected no-match exit; no source-selected Sidon or named Erdos-Turan target was located |
| prohibited Lean construct scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| final JSON, invariant, whitespace, scoped-change, and absent-self-test checks | 0, with no-index exit 1 expected for each added file | structured blocker and exact two-file scope agree; no whitespace diagnostics; root self-test is absent |

## Retry condition and status boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash an immutable primary or approved authoritative source, independently
approve the exact source clause or result bundle, and verify its transcription, incorporated
definitions, proof boundary, corrections, and errata. They must freeze the explicit construction
versus corollary scope; `B_2`/Sidon convention; sequence or finite-set representation; positive
residue encoding; prime and index restrictions; ordered or unordered pair identity; cardinality,
ambient and strictness bounds; quantifiers; asymptotic scope; profiles; alternate encodings; and
every degenerate case.

A fresh statement worker can then encode precisely that source-selected claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H1, M4, R4]`; `audit_complete: false` and `theorem_complete: false`; no debt change,
statement receipt, worker `[_]`, accepted state, or master acceptance is claimed. Because the
assigned phase did not pass its exact-statement gate, `.stage1-worker-selftest.json` remains absent.
