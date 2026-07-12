# Exact-statement gate: blocked

Item: `S56-M-0948-STATEMENT`

Theorem: `THM-M-0948`

Base revision: `bdb4ee4eb79433800f3b28633d046959f18b57e9` (tree
`8a7b02bd1c876c4f44ab2e5863e71534155c2629`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0948-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered
investigation, but the intake receipt declares `accepted: false`, contains no accepted receipt ID,
and deliberately leaves the canonical mathematical statement and Lean target null. Master
acceptance remains necessary before a future statement transition can be accepted.

Independently, the exact-statement gate cannot pass from the received repository claim. The catalog
supplies only the name Szemeredi's theorem, the Endre Szemeredi/1975 attribution, and the slogan
"positive-density sets contain arbitrarily long arithmetic progressions." It does not define
density, choose an ambient integer domain, order the quantifiers, select a finite or infinite form,
specify the progression encoding and nonzero step, resolve small lengths, cite a theorem passage,
or bind a correction history. Its `verified` label is untrusted under rev-5.6.

The matching primary-source scan gives a sharper candidate, not an admitted canonical root. On
printed pages 199-200, Szemeredi defines `r_k(n)` as the greatest size of a subset of
`{1, ..., n}` containing no `k`-term arithmetic progression, notes that
`lim (r_k(n) / n) = c_k` exists, and states the result proved in the paper as `c_k = 0 for all k`.
This extremal finite-density formulation is materially more precise than choosing an arbitrary
upper/lower/natural/Banach density convention for an infinite set. However, the source is a remote
image-only scan not preserved as an accepted immutable repository artifact. No accountable
independent reviewer has approved the transcription, incorporated definitions, exact range of
`k`, equivalence to the catalog slogan, proof boundary, or corrections and errata. The DOI and
Crossref metadata also omit the word `no` that is visible in the scanned title, reinforcing the
need for reviewed source handling rather than silent normalization.

The proposition-changing Lean choices therefore remain open: the exact finite interval and its
one-based/zero-based transport; the definition of a nonconstant `k`-term progression; the extremal
maximum and existence proof; natural-to-real casts and the limit filter; the binder order over `k`
and `n`; the relationship between `c_k = 0`, `r_k(n) / n -> 0`, finitary density thresholds, and an
infinite positive-density form; and the cases `k = 0`, `1`, and `2`, `n = 0`, empty/full subsets,
and zero common difference. Selecting any one of these encodings without source adoption and
review would invent or substitute mathematics.

Sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard blockers.
There is consequently no canonical expression for which minimal imports, checked transports, or
the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
can be certified. All four mutation classes are undefined, not passed. No `Statement.lean`, proof
body, weakened special case, broadened interface, or circular assumption was added. The root
remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned toolchain. Its three direct imports
expose Schnirelmann density, Roth's three-term finite-density theorem, and finite-color
Hales-Jewett/homothetic-copy interfaces. All six checks pass. Schnirelmann density is a different
density, Roth fixes progression length three, and finite coloring is not the positive-density
root. These imports cannot be certified minimal for an absent canonical target.

A bounded exact-topic search over pinned mathlib and repository-local Lean found only two
Szemeredi-regularity comment matches, not an arbitrary-length positive-density declaration. This is
discovery-only evidence, not the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No dependency update, build, clone, fetch,
or other `.lake` mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0948` | 0 | rank 1021; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, guidelines, intake, and primary-scan inspection | 0 | confirmed the sparse catalog claim, exact extremal source candidate, null canonical target, and unresolved adoption/review and encoding decisions |
| `sha256sum` over authority, intake, source, probe, toolchain, and pinned mathlib inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0948/check_intake.py` | 1 | historical intake replay rejects the current regenerated blueprint hash; this statement run records rather than rewrites the provisional intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0948/IntakeProbe.lean` | 0 | six adjacent APIs elaborated; stdout SHA-256 `f069f4c14ac981d6f0f51a0c20716a416fbb53951990fa30718343b39f069388`; no canonical target or proof body |
| bounded full-Szemeredi search in pinned mathlib and repo-local Lean | 0 | only two regularity-module comment matches; discovery-only evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash an immutable edition, independently transcribe and approve the exact
source theorem and incorporated definitions, audit corrections and errata, and decide whether the
canonical root is the paper's extremal `c_k = 0` form, a checked equivalent formulation, or another
precisely cited theorem passage. The review must freeze every binder, density and interval
normalization, progression definition, limit convention, and boundary case.

A fresh statement worker can then encode exactly that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
