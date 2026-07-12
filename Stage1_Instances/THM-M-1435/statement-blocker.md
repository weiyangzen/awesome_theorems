# Exact-statement gate: blocked

Item: `S56-M-1435-STATEMENT`

Theorem: `THM-M-1435`

Base revision: `00890977f5ac2d94be2403ddfafae007a79c69f0` (tree
`061723c466c8cd25b6dc1d49dc72524392c756aa`).

## Decision

The exact Lean 4 target cannot be truthfully frozen or elaborated from the authoritative repository
record. The complete mathematical wording is the label `McMullen定理`, Curtis McMullen, the year
1994, and the gloss `有理函数的Julia集` (Julia sets of rational functions/maps). This names an
author, subject, and year, not a truth-valued proposition with ordered binders, hypotheses, and a
conclusion. Stage0 explicitly leaves the exact definitions, premises, proof route, axioms, and
formal artifact open. The catalog status `已验证` is untrusted metadata under rev-5.6.

The repository also schedules `THM-M-0259`, whose translated title and other five catalog fields are
semantically identical. It remains a separate root. It cannot lend this item a source, statement,
or proof, and this worker cannot decide whether the two records should merge, redirect, split, or
name different claims.

McMullen's immutable 1994 survey is useful ambiguity evidence, but it does not repair the catalog.
Among many inequivalent statements, its Theorem 5.2 says that an infinitely renormalizable real
quadratic polynomial `f(z) = z^2 + c` has a Julia set carrying no invariant line field. The catalog
cites neither that survey nor that theorem and supplies no conclusion. Selecting Theorem 5.2, its
Corollary 5.3, a result from the later renormalization book, or another familiar theorem would
substitute missing mathematics rather than elaborate the received target.

The integrated intake therefore deliberately leaves `canonical_statement`, `canonical_claim`, the
Lean module and expression, the elaborated-expression hash, and the environment-expression
fingerprint null. Its worker state `[_]` allowed this dependency-ordered attempt, but its receipt is
still provisional with `accepted: false`; master acceptance remains a separate requirement for any
eventual accepted statement transition.

Section 5.1 of the rev-5.6 standard fails first at exact source-statement identity. There is no
canonical expression for which imports can be certified minimal. Checked alternate transports and
the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
are undefined, not passed. No surrogate definition, convenient special case, theorem declaration,
axiom, placeholder, or broadened interface was added. The root remains `[H5, M4, R4]`.

## Pinned Lean boundary

The existing discovery-only `IntakeProbe.lean` directly imports five pinned mathlib modules and
re-elaborates ten adjacent complex, one-point-compactification, meromorphic, iteration,
periodic-point, closure, and frontier interfaces. It defines neither rational-sphere dynamics nor a
Julia set and states no McMullen theorem. Its successful elaboration is a substrate check only; its
imports are not claimed to be minimal for the unknown root and receive no statement or proof credit.

A bounded source-name search over repo-local and pinned mathlib Lean files found no McMullen,
Julia-set, Mandelbrot, complex-dynamics, rational-dynamics, normal-family, or Lattes target. The few
matches were unrelated occurrences of the words `normal family`. This is narrow feasibility
evidence, not the later anchor audit or proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The `lean-toolchain`, `lake-manifest.json`, and probe
SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`378d68bc317b83d4f7474a26fa6816830b2c075a056b88ff68b9cfee891ac761`.

The automation-provided `Formalizations/Lean/.lake` link points to the canonical pinned artifacts
and was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1435` | 0 | rank 933, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all; git rev-parse HEAD 'HEAD^{tree}'; readlink Formalizations/Lean/.lake` | 0 | before this attempt, only the automation-provided `.lake` link was untracked; base revision, tree, and link target were recorded |
| catalog, Stage0, target manifest, blueprint, and intake dossier inspection | 0 | the records supply only the author/topic/year gloss, leave the canonical claim and formal target null, and expose the separate semantic duplicate |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake match the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status inspection | 0 | pinned mathlib revision and tree match; its source worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1435/IntakeProbe.lean` | 0 | all ten adjacent APIs elaborated; no canonical target was stated |
| bounded McMullen/Julia/Mandelbrot/complex-dynamics/rational-dynamics/normal-family/Lattes search over repo-local and pinned mathlib Lean sources | 0 | only unrelated `normal family` phrase matches; no target declaration found; discovery only |
| `python3 -B Stage1_Instances/THM-M-1435/check_intake.py` before blocker artifacts were added | 1 | known stale intake-receipt failure: its blueprint input hash predates the integrated blueprint; this phase did not rewrite intake evidence to manufacture agreement |
| `python3 -m json.tool Stage1_Instances/THM-M-1435/statement-blocker.json` | 0 | structured blocker parsed as JSON |
| scoped statement-blocker invariant check | 0 | item identity, open state, null target, undefined mutations, unchanged H5/M4/R4 vector, false completion flags, and absent self-test agree |
| prohibited Lean proof-escape scan over `Stage1_Instances/THM-M-1435` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped tracked and added-file whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the statement deliverable is blocked |

## Retry condition and status boundary

An accountable source reviewer must preserve and hash an immutable primary edition, select and
transcribe one exact truth-valued proposition and every incorporated definition with pinpoint
locators, map all assumptions and the proof boundary, check translation, publication-date
provenance, corrections, and errata, and obtain independent approval. The decision must freeze the
map class, ambient sphere or plane, Julia-set convention, ordered binders, hypotheses, conclusion,
and all degree, pole, infinity, exceptional-map, renormalization, measure, and other boundary cases.
It must also authoritatively resolve the relationship to `THM-M-0259` without transferring credit.

A later statement worker can then encode that same claim, minimize pinned imports, serialize and
hash the elaborated expression and environment, compile all credited transports, and run the four
required mutation classes. Master acceptance of the intake is also required before an accepted
statement transition.

The first failed gate is exact source-statement identity. This is blocked-attempt evidence, not
completion of the statement node or any downstream node. `statement_elaborated`, `audit_complete`,
and `theorem_complete` remain false; no debt-vector change or accepted receipt is proposed. Because
the assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted and no worker `[_]` claim is made.
