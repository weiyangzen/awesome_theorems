# Exact-statement gate: blocked

Item: `S56-M-1421-STATEMENT`

Theorem: `THM-M-1421`

Base revision: `ea6d9ac3942ade0c65c13eccb6bcec945e698e69` (tree
`16e4f4fa87955d7ae7392859a6713a56bcfe7b7e`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record gives only the name `Pesin熵公式` (Pesin entropy formula), Yakov Pesin, the year 1977,
and the gloss `熵与Lyapunov指数` ("entropy and Lyapunov exponents"). It supplies no formula,
definitions, ordered binders, hypotheses, theorem/page locator, proof boundary, errata, or formal
artifact. Stage0 explicitly leaves the exact definitions and premises, proof route, dependencies,
alternate forms, axioms, and machine status open. The metadata label `已验证` is untrusted under
rev-5.6.

The provisional intake identifies Ya. B. Pesin's 1977 paper *Characteristic Lyapunov Exponents and
Smooth Ergodic Theory*, Section 5, Theorem 5.1, printed page 81, equation (5.0), as the leading
primary-source candidate. It correctly does not accept that candidate as the canonical claim. The
paper's printed result is expressed as minus an integral of negative forward characteristic
exponents with multiplicities, while Section 1.6 paraphrases a positive-exponent formulation. A
checked inverse/time-reversal, exponent-sign, and entropy-invariance bridge is absent.

The following proposition-changing choices also remain unresolved:

- the compact smooth Riemannian manifold model, universes, charts, boundary, and zero-dimensional
  cases;
- the `C^2` diffeomorphism representation, derivative cocycle, time direction, and invertibility;
- the normalized smooth invariant measure, its exact relation to Riemannian volume, completion,
  probability, ergodicity, and singular-measure boundary;
- the Kolmogorov-Sinai metric entropy definition, logarithm normalization, codomain, and
  finite-versus-infinite policy;
- Lyapunov exponent existence hypotheses, ordinary or extended values, common conull set,
  multiplicity, measurability, integrability, and zero or empty-spectrum conventions; and
- the exact quantifier order, almost-everywhere scope, conclusion, and degenerate cases.

Selecting a familiar modern variant, silently choosing one sign convention, or introducing an
abstract structure that assumes entropy, exponents, and their equality as fields would invent or
substitute mathematics. Section 5 of the rev-5.6 blueprint treats this ambiguity and a missing
expression fingerprint as hard blockers. There is therefore no canonical expression on which to
certify minimal imports, checked alternate transports, or meaningful removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations. Those tests are undefined, not
passed. The first failed gate is exact source-statement identity, and machine state remains `M4`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` imports five pinned modules and re-elaborates eight adjacent APIs:
`MeasurePreserving`, its iterate theorem, topological `Dynamics.coverEntropy`, `mfderiv`, Bochner
integration and almost-everywhere integral congruence, and finite sums including the empty sum.
These checks establish that the pinned Lean environment is usable and document some possible
substrate. They do not state the Pesin entropy formula. In particular, `Dynamics.coverEntropy` is
topological entropy, not the Kolmogorov-Sinai metric entropy required by the likely result. The
probe imports cannot be claimed minimal for a target that does not yet exist.

A bounded search of pinned mathlib found no target-name occurrence for Pesin, Lyapunov, Oseledets,
metric entropy, measure-theoretic entropy, or Kolmogorov-Sinai. This is narrow discovery evidence,
not a complete anchor audit and not proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain`, `lake-manifest.json`, and probe
SHA-256 values are respectively `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`0762fe5546af18064da6ab8fe51f9578ae06c01be4c194806107d90ec2e2a859`.

The automation-provided `Formalizations/Lean/.lake` link existed before this phase and points to
the canonical checkout's pinned artifacts. It was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1421` | 0 | rank 919, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all && git rev-parse HEAD && git rev-parse HEAD^{tree}` | 0 | before statement edits, only the pre-existing untracked `.lake` link was present; base revision and tree are recorded above |
| `rg` across the catalog, Stage0, manifest, intake manifest, and source crosswalk | 0 | found only the underspecified catalog gloss and the fail-closed provisional intake; no exact canonical proposition |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1421/IntakeProbe.lean` | 0 | hashes agree with the environment fingerprint above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1421/IntakeProbe.lean` | 0 | eight adjacent pinned APIs elaborated; no target theorem was stated |
| bounded pinned-mathlib source search for Pesin, Lyapunov, Oseledets, metric entropy, measure-theoretic entropy, and Kolmogorov-Sinai | 1 | expected no-match exit; discovery-only feasibility evidence, not an anchor audit |
| `python3 Stage1_Instances/THM-M-1421/check_intake.py` | 1 | known stale intake-checker failure already present at the base: it expects the intake DAG state to remain `[ ]`, while the authoritative DAG records provisional `[_]`; after this phase its closed intake-only file inventory is stale as well |
| `python3 -m json.tool Stage1_Instances/THM-M-1421/statement-blocker.json` and scoped `jq` assertions | 0 | blocker JSON parsed; target identity, null target, blocked gate, four undefined mutations, false completion flags, and changed paths agree |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `opaque`, `constant`, or `unsafe` declaration |
| tracked and added-file whitespace checks | 0 | both blocker artifacts passed `git diff --check` / `git diff --no-index --check` |
| `test ! -e .stage1-worker-selftest.json` | 0 | required no-self-test boundary is preserved because the statement deliverable is blocked |

The statement run does not rewrite the intake receipt, intake artifact list, historical hashes, or
authoritative DAG to manufacture agreement with that stale intake-only checker.

## Retry Condition And Status Boundary

The integration lane must first accept the intake dependency. An accountable source reviewer must
then preserve an immutable primary edition or accepted translation, transcribe and crosswalk every
incorporated definition and assumption, audit the proof boundary and errata, resolve the two sign
orientations, freeze all domain, measure, entropy, exponent, multiplicity, exceptional-set,
integrability, binder, and boundary conventions listed above, and independently approve the exact
source-to-claim mapping.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. The root remains `[H1, M4, R3]`, with `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted and no receipt or
master acceptance is claimed.
