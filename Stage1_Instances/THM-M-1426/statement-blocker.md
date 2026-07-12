# Exact-statement gate: blocked

Item: `S56-M-1426-STATEMENT`

Theorem: `THM-M-1426`

Base revision: `5ac2d33ee4b1a16fd90dca63313cd900ffc4bb50` (tree
`59b19df4105f58fc10c3e924c32320a284145b7c`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the topic label `multivalued random dynamical systems`, the attribution
"many mathematicians," the period "21st century," and the gloss "random systems with nonunique
solutions." It supplies no stable source identifier, formula, definitions, ordered binders,
hypotheses, conclusion, proof boundary, or errata. Stage0 explicitly leaves the exact definitions
and premises, proof process, dependencies, alternate forms, axioms, and machine artifact open. The
catalog label `verified` is untrusted metadata under rev-5.6.

An MRDS is a framework rather than one theorem. Compatible but inequivalent roots include:

- a definition or characterization of a measurable set-valued cocycle;
- construction of an MRDS from a stochastic differential or parabolic inclusion;
- perfection of an almost-sure multivalued cocycle;
- measurability, compactness, closed-graph, or semicontinuity results;
- existence, uniqueness, invariance, minimality, or measurability of a random attractor; and
- model-specific asymptotic results for stochastic inclusions or PDEs.

Those readings require different state and probability spaces, time domains, value conventions,
solution concepts, measurable-multifunction definitions, equality or inclusion cocycle laws,
exceptional-set scopes, hypotheses, conclusions, and boundary cases. They also require an explicit
boundary against the separately scheduled random dynamical systems (`THM-M-1424`) and random
attractors (`THM-M-1425`) targets.

The intake inspected Caraballo, Langa, and Valero's 2002 paper as source-selection evidence. That
paper contains Definition 1, Proposition 2, and Theorems 3, 8, 12, 16, and 17, covering several of
the incompatible roots above. The catalog does not cite the paper or select one passage, and no
independent reviewer has approved a source-to-canonical-statement mapping. Selecting Definition 1,
an attractor theorem, or a stochastic-inclusion theorem would therefore invent or substitute
missing mathematics rather than elaborate the received target.

Section 5.1 of the rev-5.6 blueprint fails before proof evidence may be inspected. There is no
canonical expression on which to certify minimal imports, serialize an elaborated expression and
environment fingerprint, compile checked alternate transports, or run removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations. Those four mutation classes are
undefined, not passed. The first failed substantive gate is exact source-statement identity, and
the root remains `[H5, M4, R4]`.

The intake dependency itself is only `[_]`, provisional worker evidence pending master acceptance.
It is not treated as an accepted prerequisite here.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` imports `Mathlib.Data.Rel` and
`Mathlib.Dynamics.Ergodic.MeasurePreserving`. Under the pinned environment it elaborates `SetRel`,
relation composition and image, measurable spaces and measures, and measure-preserving iteration.
These are adjacent substrate APIs only. The probe states no MRDS theorem, and its two imports cannot
be called minimal for a target that does not exist.

A bounded name search over repo-local and pinned-mathlib Lean sources found no declaration under
the searched multivalued/set-valued random-dynamics phrases. This is narrow discovery evidence, not
an anchor audit or proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The `lean-toolchain`, `lake-manifest.json`, and probe
SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`47bc9cff63a94182671004895c4efaf210f61f1e2a9f076e787756935403f739`.

The automation-provided `Formalizations/Lean/.lake` link existed before this phase and points to
the canonical checkout's pinned artifacts. It was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1426` | 0 | rank 924, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all; git rev-parse HEAD; git rev-parse 'HEAD^{tree}'; readlink Formalizations/Lean/.lake` | 0 | before statement edits, only the pre-existing `.lake` link was untracked; base revision and tree are recorded above |
| bounded source-record, Stage0, blueprint, and dossier inspection | 0 | only a topic and gloss exist; the canonical statement and formal target remain null |
| `cd Formalizations/Lean && lake env lean --version && lake --version && lake env lean ../../Stage1_Instances/THM-M-1426/IntakeProbe.lean` | 0 | Lean and Lake versions identified; all eight adjacent APIs elaborated; no MRDS target was stated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` plus tree and status checks | 0 | pinned revision and tree above; package worktree clean |
| `sha256sum` on the target manifest, blueprint, skill, probe, toolchain, and Lake manifest | 0 | hashes agree with `statement-blocker.json` |
| bounded repo-local and pinned-mathlib source-name search | 1 | expected no-match exit; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-1426/check_intake.py` | 1 | known historical checker failure: it expects the intake execution item at `[ ]`, while current authority records provisional `[_]`; it also models an intake-only artifact inventory and was not rewritten to manufacture agreement |
| `python3 -m json.tool Stage1_Instances/THM-M-1426/statement-blocker.json` | 0 | structured blocker parsed as JSON |
| scoped statement-blocker invariant check | 0 | item identity, `[ ]` state, null target/imports, four undefined mutations, unchanged debt vector, false completion flags, changed paths, and no-self-test boundary agree |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped tracked and added-file whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the assigned statement deliverable is blocked |

## Retry Condition And Status Boundary

The integration lane must first accept the intake dependency. Accountable reviewers must then
preserve an immutable primary or authoritative source, select and independently approve one exact
truth-valued theorem passage, transcribe every incorporated definition, ordered binder, hypothesis,
conclusion, null-set convention, cocycle and solution convention, and boundary case, check
corrections and errata, and justify the boundary with `THM-M-1424` and `THM-M-1425`.

A later statement worker can then encode that same claim with real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This is blocked-attempt evidence, not completion of the statement node or any downstream node. The
root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt-
vector change is proposed. Because the assigned phase is not genuinely self-tested to its
completion gate, no `.stage1-worker-selftest.json` is emitted and no worker `[_]` or master-
acceptance receipt is claimed.
