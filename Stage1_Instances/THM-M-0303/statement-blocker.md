# Exact-statement gate: blocked

Item: `S56-M-0303-STATEMENT`

Theorem: `THM-M-0303`

Base revision: `4b93dbd88c5b39d7b83f2f9278c3371f53703d76` (tree
`a526f0ad0273426336b064730ac8b85143e3e5db`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete mathematical wording is only the family name `索伯列夫嵌入定理` (Sobolev embedding
theorem), the attribution Sergei Sobolev and year 1936, and the gloss `Sobolev空间到连续函数空间的嵌入`
(an embedding from Sobolev space into a continuous-function space). It supplies no bibliography,
formula, incorporated definitions, ordered binders, hypotheses, conclusion, proof boundary,
correction history, errata disposition, or independent review. Stage0 explicitly leaves the exact
definitions and premises open, and rev-5.6 treats the catalog's `已验证` value as untrusted.

Sobolev embedding is a family of inequivalent propositions. An exact statement must select the
ambient dimension and domain, local or global setting, domain and boundary regularity, integer or
fractional differentiability order, homogeneous or inhomogeneous model, weak-derivative or Fourier
encoding, integrability exponent and endpoints, scalar or vector codomain, almost-everywhere
representative relation, continuous versus bounded-continuous or Holder target, domain versus
closure, norm or seminorm estimate, constant dependencies, and all degenerate cases. The received
record selects none of these.

The source inventory also contains a byte-identical Chinese record and a separately retained
mixed-title target, `THM-M-1237`, with the same gloss. No accepted decision makes the targets
aliases, selects distinct variants, or transfers proof-body ownership. Choosing that target's
first-order supercritical bounded-domain formulation would add proposition-changing mathematics.
It would also blur the boundaries of `THM-M-0304` and `THM-M-1242`, which separately own Morrey or
Holder conclusions. Copying a familiar theorem, conjoining several variants, or selecting a
weaker smooth-function case would therefore invent or substitute the target.

The intake correctly leaves the canonical human statement, Lean module and expression, minimal
imports, expression and canonical-target environment fingerprints, binders, hypotheses, and
alternate encodings null at `[H5, M4, R4]`. Without one canonical expression, import minimality
cannot be tested and the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations are undefined rather than passed. No `Statement.lean`, assumed embedding,
axiom, placeholder, special case, or broadened theorem was introduced.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated using the pinned environment. Its two imports,
`Mathlib.Analysis.FunctionalSpaces.SobolevInequality` and
`Mathlib.Topology.MetricSpace.Holder`, expose four Gagliardo-Nirenberg-Sobolev derivative-norm
inequalities and the fact that already-established positive Holder control implies continuity.
All six interfaces elaborate, but they concern smooth functions or consume Holder control. They do
not define the source-selected Sobolev class, bridge an almost-everywhere class to a concrete
representative, or produce Holder control or continuity from Sobolev hypotheses. The imports
therefore cannot be certified minimal for the absent target and receive no statement, transport,
anchor, or proof credit.

A bounded repository-local and pinned-mathlib Lean search found the same adjacent inequalities,
generic Holder APIs, and the separately owned `THM-M-1237` boundary. It found no target-specific
`THM-M-0303` declaration. This is narrow feasibility evidence, not the downstream immutable anchor
audit or a proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink points to canonical pinned artifacts and was used read-only.
No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0303` | 0 | rank 1049; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base identifiers appear above |
| scoped catalog, Stage0, manifest, DAG, intake, crosswalk, scope, duplicate, neighbor, and candidate inspection | 0 | only the family label and gloss are authoritative; all proposition-changing choices and duplicate identity and ownership remain open |
| `sha256sum` over authority, source, intake, toolchain, lockfile, probe, and pinned mathlib inputs | 0 | hashes agree with `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision, tree, and package-status checks | 0 | revision and tree agree with the fingerprint; the package worktree was clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0303/IntakeProbe.lean` | 0 | four adjacent GNS estimates and two Holder interfaces elaborated; no canonical target, transport, or proof body was declared |
| bounded repo-local and pinned-mathlib Lean search for Sobolev embedding or continuity declarations | 0 | found adjacent interfaces and the separate `THM-M-1237` boundary; no target-specific canonical expression |
| `python3 -B Stage1_Instances/THM-M-0303/check_intake.py` | 1 | the historical intake checker freezes authoritative intake state `[ ]`, while the integrated execution DAG now records provisional `[_]`; this phase records rather than rewrites prior evidence |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-0303` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0303/statement-blocker.json` and scoped invariant assertions | 0 each | blocker JSON parses; identity, null target/imports, unchanged debt, four undefined mutations, false completion flags, exact paths, and absent self-test agree |
| scoped tracked and per-added-file whitespace checks | 0 diagnostics | no whitespace errors; no-index exit 1 for each new file is the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable did not pass |

The intake prerequisite has provisional worker state `[_]`, not master-accepted state `[x]`. Its
receipt explicitly has `accepted: false`, is not content-addressed, and has no accepted receipt ID.
Rev-5.6 section 10.2 permits this dependency-ordered inspection while concurrency is enabled, but
master closure remains dependency ordered. The first substantive failure is independently the
missing exact source statement and duplicate-target decision.

## Retry Condition

The integration lane must revalidate and master-accept the intake and decide the identity and
proof-ownership relationship between `THM-M-0303` and `THM-M-1237`. Accountable reviewers must then
preserve and hash one lawful complete primary or authoritative source edition, transcribe one exact
theorem and every incorporated definition with pinpoint locators, audit its translation,
corrections, errata, and proof boundary, and independently approve the mapping. They must freeze
the domain, dimension, order and Sobolev model, exponents and endpoints, regularity assumptions,
value space, representative semantics, target topology, estimate and constants, ordered binders,
hypotheses, conclusion, and every boundary case.

A later statement worker can encode that same claim using real Lean definitions, minimize pinned
imports, serialize and hash its elaborated expression and environment, check every credited
transport, and execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
