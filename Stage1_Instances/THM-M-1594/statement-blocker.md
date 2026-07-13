# Exact-statement gate: blocked

Item: `S56-M-1594-STATEMENT`

Theorem: `THM-M-1594`

Base revision: `d257e1e5e5fa003d6e1f26344c0331bf99374fa9` (tree
`fa06b50b528e038d182d5479a18296f63fa5eae5`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1594-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered
attempt, so pending master acceptance did not prevent the inspection. The intake receipt is
non-content-addressed, declares `accepted: false`, has no accepted receipt ID, and intentionally
leaves the canonical mathematical claim and Lean target null. Master acceptance remains required
before any future accepted statement transition.

Independently and decisively, the exact-statement gate cannot pass from the authoritative repository
record. It supplies only the title `Turbo码`, the attribution Claude Berrou / Alain Glavieux, the
year 1993, and the qualitative gloss `接近香农限的码` (codes near the Shannon limit). It contains no
cited truth-valued proposition, formula, definition chain, ordered binder, hypothesis, conclusion,
boundary case, proof boundary, or correction history. Stage0 explicitly leaves the precise
definitions and premises open, and the catalog's `已验证` label is untrusted under rev-5.6.

The strongest bibliographic match is Berrou, Glavieux, and Thitimajshima, *Near Shannon limit
error-correcting coding and decoding: Turbo-codes. 1*, ICC 1993, volume 2, pages 1064-1070, DOI
`10.1109/ICC.1993.397441`. The intake checked bibliographic metadata, not an immutable primary-text
theorem passage. No theorem, equation, section, or page locator; complete definition and premise
crosswalk; proof-versus-simulation classification; correction audit; or independent review has been
accepted. The title itself combines a construction, decoding method, and qualitative performance
claim rather than selecting one root proposition.

The possible roots are materially different: encoder construction or algebraic correctness;
component MAP/BCJR correctness; a finite-iteration or convergence property of iterative decoding;
a finite BER/FER performance point; a later ensemble or distance-spectrum bound; or an asymptotic
threshold or capacity-approaching theorem. Each requires different encoders, interleavers,
termination and puncturing, channels, modulation and SNR conventions, decoders, probability spaces,
error criteria, rates, block lengths, quantifiers, constants, and endpoints. Selecting any familiar
version would invent, narrow, broaden, or substitute mathematics rather than elaborate the exact
received target.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. There is consequently no honest canonical expression for which minimal
imports, checked alternate transports, or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can be certified. Those four mutations are
undefined, not passed. The root vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates in the pinned environment. Its five direct imports
expose generic Hamming distance, deterministic automata, discrete probability mass functions,
stochastic kernels, and real Gaussian measures. All twelve API checks pass. This is real substrate
validation, but the probe defines no turbo encoder, interleaver, trellis decoder, error metric,
capacity claim, canonical target, checked transport, or proof body. Its imports therefore cannot be
certified minimal for an absent target.

A bounded exact-topic search of pinned mathlib and repository-local Lean found no turbo-code, RSC,
parallel-concatenation, BCJR, SOVA, or interleaver declaration. A second search found only an
unrelated channel-capacity metadata string. This is discovery-only feasibility evidence, not the
downstream immutable anchor audit or a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone, fetch,
or dependency mutation was run. The probe's complete stdout has SHA-256
`3db7597b3db88bb80baf4f7451a17c41d31c867014ec8959a1c0a5070cf27e45`.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1594` | 0 | rank 1214; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 11742,11747 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at `bcf3f9fa...`; no later source-statement refinement |
| `sha256sum` over the literal authority, source, intake, toolchain, lockfile, probe, and pinned mathlib inputs recorded in `statement-blocker.json` | 0 | exact current fingerprints recorded; historical intake artifacts were not rewritten |
| `python3 -B Stage1_Instances/THM-M-1594/check_intake.py` | 1 | historical intake replay stops because it expects authoritative intake state `[ ]`, attempts 0; the integrated DAG now records `[_]`, attempts 1, and the original nine-file intake inventory becomes historical after this phase |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1594/IntakeProbe.lean` | 0 | twelve generic APIs elaborated; complete stdout SHA-256 recorded above; no canonical target or proof body |
| bounded exact-topic `rg` over pinned mathlib and repo-local Lean | 1 expected no-match | no turbo/RSC/parallel-concatenation/BCJR/SOVA/interleaver declaration; discovery only |
| prohibited-construct `rg` over owned Lean files | 1 expected no-match | no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1594/statement-blocker.json`; scoped Python assertions | 0 | valid JSON; identity, blocked `[ ]`, unchanged `H5/M4/R4`, null target/imports, four undefined mutations, false completion flags, exact two-file scope, and absent receipt/self-test agree |
| scoped `git diff --check`; per-added-file no-index whitespace checks | 0 / 1 expected differences | no whitespace diagnostics; no-index exit 1 means each new file differs from `/dev/null` |
| `test ! -e .stage1-worker-selftest.json`; `test ! -e Stage1_Instances/THM-M-1594/statement-receipt.json` | 0 | no worker self-test or statement receipt was emitted because the statement gate failed |

The historical intake checker is frozen to its original DAG state and nine-file intake inventory.
Integration subsequently advanced the intake node provisionally. Adding these statement artifacts
also makes that intake-only inventory historical. This statement run records the limitation instead
of rewriting the intake checker, receipt, instance, task DAG, generated blueprint, or authoritative
execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash one immutable primary or approved
authoritative source, select and independently approve one exact Turbo-code theorem or explicit
composition, and transcribe every incorporated definition, convention, ordered binder, hypothesis,
conclusion, proof boundary, correction, erratum, theorem-versus-experiment classification, and
degenerate case while preserving neighboring-target boundaries. They must in particular fix the
encoders, interleaver, termination and puncturing, channel, modulation and SNR convention, decoder,
error measure, probability and averaging order, rate, block length, quantitative limit gap,
asymptotic order, and endpoints. The integration lane must also master-accept the intake dependency
before accepting a future statement transition.

A fresh statement worker can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
