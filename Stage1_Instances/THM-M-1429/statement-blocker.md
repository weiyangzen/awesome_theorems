# Exact-statement gate: blocked

Item: `S56-M-1429-STATEMENT`

Theorem: `THM-M-1429`

Base revision: `d1bb69e506d568ec4852bd68cc5bda1d61702852` (tree
`d9681ef41935162296b57b0170641d66404a53a9`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the title `Fatou集` ("Fatou set"), attributes it to Pierre Fatou in 1917,
and gives the gloss `复动力学的稳定集` ("the stable set of complex dynamics"). This names a
dynamical object and an informal interpretation, not a truth-valued proposition. It gives no
primary-source locator, formula, definitions, ordered binders, hypotheses, conclusion, or boundary
cases. Stage0 explicitly leaves the exact definitions and premises open, and the catalog label
`已验证` is untrusted under rev-5.6.

Even the object is relative to unselected data. The record does not choose a rational, polynomial,
entire, meromorphic, or other map; the complex plane, Riemann sphere, or a relative domain; the
Euclidean or spherical topology and metric; treatment of poles, singularities, or infinity; or a
normality, equicontinuity, subsequential-convergence, compact-divergence, or other stability
predicate. It also does not select a theorem about the resulting set. A normal-family definition,
openness, forward/backward/complete invariance, complementarity with a Julia set, a component
classification, and a basin theorem are inequivalent roots with different contexts and
obligations. A tautology obtained by unfolding an invented definition would not repair the source
gap. Any such choice would broaden or substitute the received target.

The intake records Pierre Fatou's 1919-1920 *Sur les equations fonctionnelles* memoirs only as
nonselected historical discovery leads. The catalog does not cite one of them or select a passage;
there is no accepted immutable copy, pinpoint proposition, incorporated-definition and assumption
crosswalk, errata disposition, or independent source approval. Their dates also do not reconcile
the catalog's unexplained 1917 date. They therefore cannot silently choose the canonical root.

Section 5.1 of the rev-5.6 blueprint fails at exact source-statement identity. There is no
canonical expression on which to certify minimal imports, preserve an elaborated-expression and
environment fingerprint, compile checked alternate transports, or run the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations. Those four
mutation classes are undefined, not passed. No theorem declaration, assumed interface, axiom,
placeholder, weakened example, or neighboring target was introduced. The root remains
`[H5, M4, R4]`.

The intake dependency is recorded as `[_]` in the generated blueprint but has no master-acceptance
receipt. It is not treated as an accepted prerequisite here.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` imports:

- `Mathlib.Analysis.Meromorphic.Basic`;
- `Mathlib.Dynamics.PeriodicPts.Defs`; and
- `Mathlib.Topology.UniformSpace.LocallyUniformConvergence`.

Using the pinned environment, it re-elaborates seven generic iteration, periodic-point,
meromorphic, locally-uniform convergence, and topology interfaces. These APIs demonstrate possible
substrate only. The probe states no Fatou-set theorem, its locally-uniform convergence predicate is
not silently identified with a source-specific normal-family convention, and its imports cannot be
called minimal for a target that does not exist. A bounded repo-local and pinned-mathlib name search
found no Fatou-set, Julia-set, complex-dynamics, or normal-family declaration. This is narrow
discovery evidence, not an anchor audit or proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The `lean-toolchain`, `lake-manifest.json`, and probe
SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`46fe24b783abc5dd2c4462cbeca34dc252d72d83eedac226abb2d85fe8868d97`.

The automation-provided `Formalizations/Lean/.lake` link existed before this phase and points to
the canonical checkout's pinned artifacts. It was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1429` | 0 | rank 927, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short; git rev-parse HEAD; git rev-parse 'HEAD^{tree}'` | 0 | before statement edits, only the pre-existing `.lake` link was untracked; base revision and tree are recorded above |
| source-record, Stage0, blueprint, and dossier inspection | 0 | only an object label and gloss exist; canonical statement and formal target remain null |
| `cd Formalizations/Lean && lake env lean --version && lake --version && lake env lean ../../Stage1_Instances/THM-M-1429/IntakeProbe.lean` | 0 | Lean and Lake versions identified; all seven adjacent APIs elaborated; no target theorem was stated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` plus tree and status checks | 0 | pinned revision and tree above; package worktree clean |
| `sha256sum` on the target manifest, blueprint, skill, probe, toolchain, and Lake manifest | 0 | hashes agree with `statement-blocker.json` |
| bounded repo-local and pinned-mathlib source-name search | 1 | expected no-match exit; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-1429/check_intake.py` | 1 | known historical checker failure: it requires the intake worker's now-absent root self-test manifest and models an intake-only closed artifact inventory; it was not rewritten to manufacture agreement |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque)[[:space:]]\|\bunsafe\b' Stage1_Instances/THM-M-1429 --glob '*.lean'` | 1 | expected no-match exit; no prohibited proof escape or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1429/statement-blocker.json` plus scoped `jq` assertions | 0 | JSON parsed; item identity, null target/imports, four undefined mutations, unchanged debt, false completion flags, and no-self-test boundary agree |
| scoped tracked and added-file whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the assigned statement deliverable is blocked |

## Retry Condition And Status Boundary

The integration lane must first accept the intake dependency. Accountable reviewers must then
preserve an immutable primary or authoritative source, select and independently approve one exact
truth-valued theorem passage, transcribe every incorporated definition, ordered binder,
hypothesis, conclusion, normality or stability convention, and boundary case, check corrections
and errata, reconcile the catalog's 1917 date, and justify the boundary with neighboring targets.

A later statement worker can then encode that same claim with real Lean definitions, minimize its
pinned imports, serialize the elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

This is blocked-attempt evidence, not completion of the statement node or any downstream node. The
node remains `[ ]`; the root remains `[H5, M4, R4]`, with `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the assigned phase is not
genuinely self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted and no
worker `[_]` or master-acceptance receipt is claimed.
