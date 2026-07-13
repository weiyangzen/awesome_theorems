# Exact-statement gate: blocked

Item: `S56-M-1595-STATEMENT`

Theorem: `THM-M-1595`

Base revision: `db6914155f1f63e835364b89ba0a3b25f1d7f936` (tree
`a5488edccb2687c4ff0bbdccf4650e06b2e45337`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1595-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this
dependency-ordered attempt, so pending acceptance did not prevent the investigation. The intake
receipt is unsigned and non-content-addressed, declares `accepted: false`, has no accepted receipt
ID, and deliberately leaves the canonical mathematical statement and Lean target null. Master
acceptance remains necessary before any eventual accepted statement transition.

Independently, the exact-statement gate cannot pass from the authoritative repository record. It
supplies only the title `Polar码` (polar codes), Erdal Arikan, 2009, and the gloss
`达到香农限的码` (codes achieving the Shannon limit). It supplies no citation, exact theorem,
channel or capacity model, code, decoder, ordered binders, hypotheses, conclusion, proof boundary,
correction history, or boundary cases. Stage0 explicitly leaves the precise definitions and
premises open, and the catalog's `已验证` field is untrusted under rev-5.6.

The matching primary source exposes material alternatives rather than selecting one root. Arikan
2009 Theorem 1 is a channel-polarization limit. Theorem 2 supplies many good synthesized channels
below symmetric capacity. Theorem 3 gives a block-error asymptotic averaged over frozen-vector
choices for a binary-input discrete memoryless channel. Theorem 4 gives the fixed-arbitrary-frozen-
vector form only for symmetric channels, where symmetric capacity equals Shannon capacity.
Theorem 5 separately gives `O(N log N)` encoding and successive-cancellation decoding complexity.
The paper's abstract compounds several of these results, while later literature strengthens other
parameters. These are not interchangeable propositions.

The catalog does not decide whether "Shannon limit" means symmetric capacity for a general B-DMC
or Shannon capacity for the symmetric subclass. It also does not choose averaged or fixed frozen
bits, exact information-set construction, block or bit error, average or maximal error, strict rate
boundary, block-length indexing, asymptotic quantifier order, bound or limit form, complexity
conclusion, or any conjunction. Selecting a familiar formulation, conjoining results, or
substituting the neighboring channel-capacity or Shannon-coding targets would invent, narrow,
broaden, or replace mathematics rather than elaborate the exact received target.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing expression
fingerprint hard blockers. There is no honest canonical expression for which a minimal import set,
checked alternate transport, or the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can be certified. Those mutations are undefined,
not passed. No `Statement.lean`, theorem declaration, axiom, placeholder, weakened special case, or
broadened interface was added.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates in the pinned environment. Its six
direct imports expose ten adjacent probability-mass, stochastic-kernel, binary-entropy, Hamming,
and matrix interfaces. All checks pass. The probe defines no mutual information, symmetric or
Shannon capacity, synthesized channel, polar code, encoder, decoder, asymptotic proposition,
canonical target, checked transport, or proof body. Its imports therefore cannot be certified
minimal for an absent canonical statement.

A bounded lexical search of pinned mathlib and repository-local Lean found no target declaration
under polar-code, polar-coding, channel-polarization, mutual-information, successive-cancellation,
or symmetric-capacity terms. This is discovery-only feasibility evidence, not the downstream
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
| `python3 scripts/stage1_target.py show THM-M-1595` | 0 | rank 1215; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped blueprint, manifest, skill, catalog, Stage0, intake, and Arikan-source inspection | 0 | confirmed the sparse gloss, inequivalent candidate roots, explicit null canonical target, and unresolved proposition choices |
| `sha256sum` over authority, source, intake, probe, toolchain, lockfile, and relevant pinned mathlib inputs | 0 | exact current hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-1595/check_intake.py` | 1 | historical intake replay stops because its receipt freezes a pre-integration blueprint hash; its original nine-file inventory also becomes historical after this phase |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1595/IntakeProbe.lean` | 0 | ten adjacent APIs elaborated; stdout SHA-256 `bf36075a82086b7a090af1854ad7164578d486a0b38e576896b5ef4bb22300db`; no canonical target or proof body |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 1 | expected no match; no target declaration was located |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1595/statement-blocker.json` | 0 | the finalized structured blocker parsed as valid JSON |
| inline `python3 -B -` scoped statement-blocker assertions | 0 | printed `statement blocker invariant check: ok (THM-M-1595 blocked; H1/M4/R4; no self-test)` after checking item/theorem identity, open blocked state, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact two-file change scope, and absent self-test |
| `git diff --check -- Stage1_Instances/THM-M-1595` plus per-added-file `git diff --no-index --check /dev/null <file>` | 0 for the scoped check; expected new-file status 1 with empty output for each no-index check | no whitespace diagnostics in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is frozen to its original authority inputs and intake-only artifact
inventory. This statement run records that limitation instead of rewriting the intake checker,
receipt, instance, task DAG, generated blueprint, or authoritative execution DAG to manufacture
agreement. Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the
structured blocker beside this report.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash one lawful immutable primary or authoritative source
edition, select one truth-valued Arikan theorem or explicit composition, and independently approve
a crosswalk of every incorporated definition, ordered binder, hypothesis, conclusion, proof
boundary, correction, erratum, and degenerate case. They must resolve Theorems 1 through 5, general
B-DMC symmetric capacity versus Shannon capacity for symmetric B-DMCs, transform and bit-channel
conventions, information and frozen sets, decoder and error semantics, rate and block-length
indexing, asymptotic quantifiers and bounds, and any complexity claim. The integration lane must
also master-accept the intake dependency and reconcile the duplicate `THM-C-0386` boundary before
accepting a future statement transition.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
