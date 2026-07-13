# THM-M-0746 exact-statement gate: blocked

- Item: `S56-M-0746-STATEMENT`
- Base revision: `997541734bb32f987fb15f163335a82512992120` (tree
  `2c866b9d840d48c48ac839740c62d3b9440be0e5`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully completed from the authoritative repository record. The record supplies only the title
`创造集` (creative sets), attribution to Emil Post in 1944, and the gloss `创造集的性质`
(properties of creative sets). It supplies no formula, bibliography, proposition locator, ordered
binders, hypotheses, exact conclusion, proof boundary, correction history, or independent review.
Stage0 explicitly leaves the definitions and premises open, and rev-5.6 treats the catalog's
`已验证` label as untrusted metadata.

The intake inspected Emil L. Post, *Recursively enumerable sets of positive integers and their
decision problems*, *Bulletin of the American Mathematical Society* 50(5), 284-316 (1944), DOI
`10.1090/S0002-9904-1944-08111-1`. Section 3 spans printed pages 295-297. The definition of a
creative set spans pages 295-296; page 296 proves existence using the complete set `K` and records
distinct consequences; pages 296-297 introduce adjacent reduction and completeness results. This
source therefore confirms that the repository gloss denotes a family of inequivalent claims rather
than selecting one root.

The missing choices change the proposition rather than merely its notation:

- the definition package, existence theorem, noncomputability consequence, complement-infinitude
  consequence, one-one or many-one completeness result, or an explicitly approved multi-root
  package;
- Post's positive integers versus `Nat`, including zero and a checked transport;
- a predicate, set, range, partial-function domain, or another computably enumerable
  representation, together with its effective numbering;
- Post's basis/index interface and the total recursive witness function's behavior outside the
  conditional subset-of-complement premise;
- complement, subset, freshness, extensionality, reduction direction, ordered-binder, foundation,
  typeclass, and computation conventions; and
- empty, universal, finite, malformed-index, duplicate-index, and positive-integer boundary cases.

Choosing one result, conjoining several, or replacing Post's formulation with a convenient modern
productive-complement or completeness statement would invent or substitute mathematics. The
separate computer-science row `创造集与单纯集`, whose gloss is merely the existence of a
nonrecursive c.e. set, is weaker and is not this target's exact source statement.

Consequently there is no canonical expression on which to certify minimal imports, serialize an
elaborated-expression fingerprint, compile checked alternate transports, or run the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations. Those tests
are undefined, not passed. The root remains `[H5, M4, R4]`.

The intake dependency is only provisional `[_]`. Its receipt declares `accepted: false`, is not
content-addressed, and contains no accepted receipt ID. Rev-5.6 section 10.2 permits this
dependency-ordered attempt, but eventual statement acceptance still requires master-accepted
intake evidence. The substantive first blocker remains exact source-statement identity and root
selection.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated through its direct import
`Mathlib.Computability.Reduce`. It checks twelve adjacent c.e.-predicate, computability, code,
halting, and reduction interfaces. The probe exited successfully; stdout was 1,351 bytes over 17
lines with SHA-256 `6f11c3273419df5ddf5ceb3040f4f402278a1dedde9a4ec6a8637f05421f3476`.
It declares no creative-set target, transport, or proof body, and receives no statement, anchor, or
proof credit. Its import cannot be certified minimal for an unidentified canonical target.

A bounded name search over the pinned mathlib and repository Lean surfaces found no
computability-theoretic declaration named for creative or productive sets. Mathlib's
`WSeq.Productive` result concerns non-stalling weak sequences and is not the productive complement
of a c.e. set. This is feasibility evidence only, not the downstream immutable anchor audit or a
global absence claim.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided canonical `.lake` symlink
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0746` | 0 | rank 1333; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped reads of the blueprint, execution skill, guidelines, manifest and DAG entries, source records, Stage0 projection, and complete intake dossier | 0 | the catalog denotes a creative-set property family but selects no source-complete proposition; the intake deliberately leaves the canonical statement, binders, imports, and fingerprints null |
| `git blame -L 5500,5505 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over current authority, source, intake, toolchain, lockfile, probe, and pinned computability-source inputs | 0 | current input digests agree with `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0746/check_intake.py` | 1 | historical intake checker expects intake state `[ ]` and zero attempts; integration now records provisional `[_]` and one attempt, so it fails closed before statement artifacts are inspected |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0746/IntakeProbe.lean` | 0 | all twelve adjacent interfaces elaborated; output digest recorded above; no canonical target or local proof declared |
| bounded creative/productive-set name search over pinned mathlib, shared Lean, and other Stage1 Lean files | 1 | expected no-match result for computability-theoretic declarations; unrelated `WSeq.Productive` was separately identified and excluded |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0746/statement-blocker.json` and scoped blocker assertions | 0 | structured blocker syntax, identity, null target/imports/hashes, four undefined mutations, unchanged vector, false completion flags, and absent self-test agree |
| `git diff --check` plus per-added-file `git diff --no-index --check` | 0 aggregate | no whitespace diagnostics; each raw no-index command returned the expected new-file difference status 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable did not pass |

The intake checker is historical phase-local evidence: it freezes the intake-time execution state
and exact nine-file inventory. This phase neither rewrites that checker nor changes intake,
scheduler, blueprint, or DAG state to manufacture freshness.

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must also
preserve and hash a lawful immutable primary or approved authoritative edition, select one exact
creative-set proposition or an explicitly multi-root package, transcribe every incorporated
definition and premise, audit corrections and errata, and independently approve its identity with
`THM-M-0746`. That selection must freeze the carrier and positive-integer transport, c.e. model,
effective numbering, basis/index and witness-function contract, complements, reductions, ordered
binders, hypotheses, conclusion, profiles, transports, and all source-relevant boundary cases.

A later statement run can then encode only that approved claim, establish minimal pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four mutation classes. Until then this node remains `[ ]`; `audit_complete` and
`theorem_complete` are false. Because the assigned phase did not pass its completion gate, no
`.stage1-worker-selftest.json`, statement receipt, proof credit, or master acceptance is claimed.
