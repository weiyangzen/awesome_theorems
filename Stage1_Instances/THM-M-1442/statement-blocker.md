# Exact-statement gate: blocked

Item: `S56-M-1442-STATEMENT`

Theorem: `THM-M-1442`

Base revision: `be1f1d3c684eb883c819bcc968e0631d7f151bb0` (tree
`cff05d9f99014e6c54839589d4470f02df94a986`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1442-INTAKE` is provisional worker state
`[_]`, not master-accepted `[x]`. More decisively, the exact Lean 4 target cannot be truthfully
elaborated from the authoritative repository record.

The record supplies only the label `二分法` (bisection method), the collective attribution "many
mathematicians," antiquity, and the gloss `方程求根的线性方法` ("a linear method for finding roots of
equations"). It cites no source and supplies no equation, definition, ordered binder, hypothesis,
conclusion, proof boundary, correction, erratum, or formal artifact. The catalog label `已验证` is
untrusted metadata under rev-5.6.

Bisection is a method family, not one proposition. The repository does not select among:

- root existence from a sign-changing interval;
- a total midpoint-and-branch recurrence;
- preservation of a nested, sign-changing bracket;
- convergence of endpoint or midpoint sequences to some root;
- a geometric interval-width or point-error inequality;
- a finite iteration bound for a positive tolerance; or
- correctness of an exact, interval, rational, or floating-point implementation.

It also leaves open the function and scalar domain, initial bracket, continuity and sign premises,
endpoint and midpoint root conventions, tie and branch rules, approximant, indexing, convergence
mode, rate and error definition, stopping contract, arithmetic semantics, binder order, and all
boundary cases. Those choices produce inequivalent propositions.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing expression
fingerprint hard blockers. Without a canonical proposition, there is no exact Lean expression for
which imports can be certified minimal, no elaborated expression or environment fingerprint, no
credited alternate transport, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation. Those mutation classes are undefined, not passed.
No surrogate theorem, weakened special case, axiom, placeholder, broadened interface, or proof body
was added.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its three direct
imports expose three intermediate-value interfaces, a generic geometric-decay result, and an
unrelated `norm_num` metaprogram whose comment uses "bisection method" for natural-power certificate
search. All five checks pass.

The intermediate-value declarations can support root existence after missing premises are selected,
but define no bisection recurrence or approximant and prove no bracket invariant, convergence rate,
error, complexity, or solver correctness. The geometric-limit declaration needs a checked bridge
from a source-selected bisection error. The `norm_num` metaprogram is not equation-root bisection.
The probe selects no candidate, supplies no checked source transport, and has no proof body. Its
imports therefore cannot be certified minimal for an absent target and receive no statement,
anchor, or proof credit.

A bounded search found only the unrelated `norm_num` lexical hit for target-specific bisection
vocabulary. This is scoped discovery evidence, not the downstream immutable anchor audit or a
global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The complete probe output has SHA-256
`4a41fd723fda152eab851abee65f0f2252234046248ab8855f906a65163e050d`.

The automation-provided `Formalizations/Lean/.lake` link points to canonical pinned artifacts and
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai), from the repository root
unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1442` | 0 | rank 1121, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; the base revision and tree are recorded above |
| exact `bash -lc` inspection recipe recorded in `statement-blocker.json` | 0 | only a method label, purpose, and rate adjective are authoritative; intake deliberately freezes a null canonical statement and target at `[H5, M4, R4]` |
| `git blame -L 10532,10537 -- Docs/researches/math_theorems.md` and scoped hashes | 0 | all uncited catalog lines originate at `bcf3f9fa...`; current authority, source, intake, toolchain, and mathlib fingerprints are recorded in the JSON blocker |
| `python3 -B Stage1_Instances/THM-M-1442/check_intake.py` | 1 | historical intake replay requires base `b4e1220...`, not current worker base `be1f1d3...`; this run records rather than rewrites historical intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision, tree, and package-status checks | 0 | revision and tree agree with the fingerprint; the package worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1442/IntakeProbe.lean` | 0 | five adjacent or lexical interfaces elaborated; no canonical target was stated |
| exact bounded `rg` expression and search roots recorded in `statement-blocker.json` | 0 | only the unrelated natural-power certificate comment matched; no source-identical target declaration was found |
| prohibited Lean construct scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and exact scoped invariant command recorded in `statement-blocker.json` | 0 each | identity, open blocked state, null target and imports, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and absent self-test agree |
| exact whitespace wrapper recorded in `statement-blocker.json` | 0 | tracked check exited 0; each added-file no-index check returned the expected difference exit 1 with no whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

The intake receipt is bound to an older repository base, declares `accepted: false`, is not
content-addressed, and has no accepted receipt ID. Its validator is intake-specific and freezes the
original nine-file inventory. This statement run does not rewrite that historical receipt,
validator, instance manifest, target-local DAG, generated checklist, or authoritative DAG to
manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash an immutable primary or approved authoritative source, select and independently
approve one exact truth-valued proposition, and map every incorporated definition, equation,
binder, premise, conclusion, proof boundary, correction, and erratum. They must freeze the domain,
bracket, recurrence, branch and tie rules, approximant, exact conclusion, arithmetic model, boundary
cases, and separation from neighboring numerical methods, the intermediate-value theorem, and
discrete binary search.

A fresh statement worker may then encode precisely that source-selected claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

The first failed gate is exact source-statement identity. The root remains `[H5, M4, R4]`, with
`audit_complete: false` and `theorem_complete: false`; no debt-vector change is proposed. This is
blocked-attempt evidence, not completion of the statement node or any downstream node. Because the
assigned phase is not genuinely self-tested to its completion gate, no `.stage1-worker-selftest.json`
is emitted and no statement receipt, worker `[_]`, or master acceptance is claimed.
