# Exact-statement gate: blocked

Item: `S56-M-1580-STATEMENT`

Theorem: `THM-M-1580`

Base revision: `bdb4ee4eb79433800f3b28633d046959f18b57e9` (tree
`8a7b02bd1c876c4f44ab2e5863e71534155c2629`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1580-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this
dependency-ordered attempt, so pending acceptance did not prevent the investigation. The intake
receipt is non-content-addressed, declares `accepted: false`, has no accepted receipt ID, and
deliberately leaves the canonical mathematical statement and Lean target null. Master acceptance
remains necessary before any eventual accepted statement transition.

Independently, the exact-statement gate cannot pass from the authoritative repository record. It
supplies the title `香农噪声信道编码定理` (Shannon noisy-channel coding theorem), Claude Shannon,
the year 1948, and only the gloss `信道编码的存在性` (existence of channel coding). It supplies no
citation, source or channel model, capacity definition, code, decoder, reliability criterion,
ordered binders, hypotheses, conclusion, proof boundary, correction history, or boundary cases.
Stage0 explicitly leaves the precise definitions and premises open, and the catalog's `已验证`
label is untrusted under rev-5.6.

The inspected matching source exposes material alternatives rather than selecting one root.
Shannon's 1948 Section 13, Theorem 11 combines a below-capacity reliable-coding clause with an
above-capacity equivocation bound and converse for the paper's discrete source and finite-state
channel framework. Theorem 12 instead characterizes capacity through the asymptotic logarithm of
the largest reliably distinguishable equal-probability signal set. A modern finite-alphabet
memoryless-channel theorem would be narrower and would quantify over block codes at rates strictly
below mutual-information capacity. These are not interchangeable propositions.

Even Theorem 11's direct clause is not ready for exact transcription: its displayed statement uses
`H <= C`, while the random-coding argument later works with a transmitted rate `R < C`. The
repository does not decide whether to preserve, correct, or reformulate that boundary. Nor does it
choose error frequency versus equivocation, average versus maximal block error, finite-state versus
memoryless channels, source-channel coding versus a channel-only theorem, the capacity and rate
normalization, quantifier order, or whether converse and separation clauses are included.

Selecting a familiar formulation, conjoining the direct and converse results, or substituting the
neighboring channel-capacity or noiseless-coding targets would invent, narrow, broaden, or replace
mathematics rather than elaborate the exact received target. The intake therefore classifies the
catalog claim as not one stable proposition at `[H5, M4, R4]`.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing expression
fingerprint hard blockers. There is no honest canonical expression for which a minimal import set,
checked alternate transport, or the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can be certified. Those mutations are undefined,
not passed. No `Statement.lean`, theorem declaration, axiom, placeholder, weakened special case, or
broadened interface was added.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates in the pinned environment. Its six
direct imports expose ten adjacent probability-mass, stochastic-kernel, binary-entropy,
Kullback-Leibler, uniquely-decodable-code, and Hamming interfaces. All checks pass. The probe
defines no source entropy rate, channel capacity, block code, decoder, reliability predicate,
canonical target, checked transport, or proof body. Its imports therefore cannot be certified
minimal for an absent canonical statement.

A bounded lexical search of pinned mathlib and repository-local Lean found no target declaration
under channel-capacity, channel-coding, noisy-channel, mutual-information, or Shannon-coding terms.
One repo-local metadata string names an unrelated external `channel-capacity` repository; it is not
a declaration or proof candidate. This is discovery-only feasibility evidence, not the downstream
immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1580` | 0 | rank 1027; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, and intake inspection | 0 | confirmed the sparse existence gloss, inequivalent source formulations, explicit null canonical target, and unresolved proposition choices |
| `sha256sum` over authority, source, intake, probe, toolchain, manifest, and relevant pinned mathlib inputs | 0 | exact current hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-1580/check_intake.py` | 1 | historical intake replay stops because it freezes the intake authority state as `[ ]`, while integration records provisional `[_]`; its original nine-file inventory is also historical after this phase |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1580/IntakeProbe.lean` | 0 | ten adjacent APIs elaborated; stdout SHA-256 `771e7e299be77968df4ad109582be2c9a1a023e4a931c01cfac9493b26c894fe`; no canonical target or proof body |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 0 | the only hit was an unrelated metadata string; no target declaration was located |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1580/statement-blocker.json` | 0 | the finalized structured blocker parsed as valid JSON |
| scoped statement-blocker invariant assertions | 0 | item and theorem identity, open blocked state, null target and imports, unchanged H5/M4/R4 vector, four undefined mutations, false completion flags, exact two-file change scope, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-1580` plus per-added-file `git diff --no-index --check /dev/null <file>` | 0 for the scoped check; expected new-file status 1 with empty output for each no-index check | no whitespace diagnostics in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is frozen to its original authority state and intake-only artifact
inventory. This statement run records that limitation instead of rewriting the intake checker,
receipt, instance, task DAG, generated blueprint, or authoritative execution DAG to manufacture
agreement. Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the
structured blocker beside this report.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash one lawful immutable primary or authoritative source
edition, select or correct one truth-valued proposition, and independently approve a crosswalk of
every incorporated definition, ordered binder, hypothesis, conclusion, proof boundary,
correction, erratum, and degenerate case. They must resolve Theorem 11 versus Theorem 12 versus a
modern finite-DMC formulation, the `H <= C` versus strict-rate boundary, the channel and source
classes, capacity, code, decoder, reliability convention, quantifier order, and included converse
or separation clauses. The integration lane must also master-accept the intake dependency before
accepting a future statement transition.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
