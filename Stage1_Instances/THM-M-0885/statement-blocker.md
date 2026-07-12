# Exact-statement gate: blocked

Item: `S56-M-0885-STATEMENT`

Theorem: `THM-M-0885`

Base revision: `a07fc18923e20fd2876d04809a15d5b31e55512f` (tree
`1268491c8f2677e1c8e38754fa93dd190892e69e`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record gives only the family label `Morgenstern theorem`, attributes it to Moshe Morgenstern
in 1994, and supplies the gloss `Ramanujan graph existence`. It cites no theorem and provides no
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, or formal
artifact. Stage0 explicitly leaves the precise definitions and premises open, and the catalog
label `verified` is untrusted under rev-5.6.

The matching bibliographic record does not remove the ambiguity. Crossref and DBLP identify Moshe
Morgenstern's 1994 article *Existence and Explicit Constructions of q + 1 Regular Ramanujan Graphs
for Every Prime Power q*, JCTB 62(1), pages 44-62, DOI `10.1006/jctb.1994.1054`. That title
identifies the published result family, but no immutable article edition, numbered theorem,
incorporated definitions, assumptions, construction branches, proof boundary, corrections,
errata, or independent review has been admitted.

The repository therefore does not decide:

- how a prime power is represented, including characteristic branches and small exceptions;
- whether the conclusion gives one graph, infinitely many pairwise nonisomorphic graphs, an
  indexed family, or an explicit or effective construction;
- the finite graph category, simplicity, connectedness, bipartiteness, degree convention, and
  vertex-cardinality restrictions;
- the adjacency spectrum representation, multiplicity convention, trivial eigenvalues, and exact
  Ramanujan inequality and boundary; or
- the algebraic construction data, ordered binders, complete clause bundle, and degenerate cases.

Those choices yield inequivalent propositions. Choosing a familiar `(q + 1)`-regular existence or
construction statement from the article title would invent, broaden, strengthen, or substitute
mathematics rather than elaborate the received target. The neighboring LPS construction,
general-Ramanujan-graph, and MSS targets cannot be borrowed as replacements.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. The intake correctly leaves the canonical human claim, Lean module and
expression, minimal imports, and expression/environment fingerprints null at `[H1, M4, R4]`.
Without a canonical target, alternate transports and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined, not passed. No
`Statement.lean`, axiom, placeholder, assumed graph interface, weakened example, or broadened
theorem was introduced.

The prerequisite `S56-M-0885-INTAKE` is also only provisional worker state `[_]`, not
master-accepted `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered attempt, so that did not
prevent truthful blocker work, but master acceptance remains independently required before a
future statement transition can be accepted.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with the pinned environment. Its three direct imports
expose finite simple graphs, vertex degree and regularity, real adjacency matrices, Hermitian
symmetry and real eigenvalues, and `Real.sqrt`. All eight checks pass. The probe defines no
prime-power family, source-specific Ramanujan predicate, explicit construction, canonical target,
checked source transport, or proof body. Its imports therefore cannot be certified minimal for a
target that has not been selected and receive no statement or proof credit.

A bounded exact-topic search of repository-local and pinned-mathlib Lean sources found no
`Morgenstern` or `Ramanujan graph` occurrence. This is discovery-only feasibility evidence, not the
downstream immutable anchor audit and not a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The `lean-toolchain`,
`lake-manifest.json`, and probe-output SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`338dc5b58bca6fa8b32a5e7bca7bc571b5f33033b8486a444857c78a05af24cd`.

The automation-provided `Formalizations/Lean/.lake` link points to the canonical pinned artifacts
and was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0885` | 0 | rank 1036, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped manifest, blueprint, skill, catalog, Stage0, intake, scope, and crosswalk inspection | 0 | only a broad existence gloss is authoritative; every proposition-changing choice remains open |
| `sha256sum` over authority, intake, toolchain, and pinned mathlib inputs | 0 | hashes agree with `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0885/check_intake.py` | 1 | historical intake replay stops on its pre-integration Stage1-blueprint hash; it also freezes an older base, authority state, and nine-file inventory, so this phase records rather than rewrites that evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree agree with the fingerprint; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0885/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; full stdout SHA-256 is `338dc5...24cd`; no canonical target was stated |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 1 | expected no-match exit; discovery only, not an anchor audit |
| prohibited Lean construct scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| JSON parse and scoped invariant check for `statement-blocker.json` | 0 each | IDs, open state, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact paths, and absent self-test agree |
| whitespace checks for both added blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

## Retry Condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash an immutable primary or authoritative edition of the 1994 article, select and
independently approve one exact numbered theorem, and transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, construction branch, exception, boundary case, proof
boundary, correction, and erratum. They must freeze the prime-power representation, family and
explicitness quantifiers, graph model, regularity, connectedness, bipartiteness, adjacency spectrum
and trivial-eigenvalue convention, spectral bound, construction data, and neighboring-target
ownership.

A fresh statement worker can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H1, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
