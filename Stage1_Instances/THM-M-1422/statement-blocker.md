# Exact-statement gate: blocked

Item: `S56-M-1422-STATEMENT`

Theorem: `THM-M-1422`

Base revision: `ffe94ac84965dc19f4923f88b7566072ddee37ae` (tree
`876a17f277d84dcf06ca672e5cd351edaa294495`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record gives only the label `Young塔` (`Young tower`), Lai-Sang Young, the year 1998, and the
gloss `非一致双曲系统的工具` (`a tool for nonuniformly hyperbolic systems`). It supplies no
truth-valued conclusion, definition, ordered binders, hypotheses, theorem/page locator, proof
boundary, or errata. The metadata label `已验证` is untrusted under rev-5.6.

The provisional intake identifies Young's 1998 paper *Statistical Properties of Dynamical Systems
with Some Hyperbolicity* as a strong primary-source candidate. It correctly does not accept a
canonical claim. The paper constructs a Markov extension over a variable return-time map and then
states several inequivalent results: Theorem 1 derives an SRB measure from P1-P5 and return-time
integrability; Theorem 2 derives exponential correlation decay from an exponential tail and total
ergodicity; and Theorem 3 gives a central limit theorem and a zero-variance coboundary criterion.
The catalog does not choose the construction, one of these results, an example theorem, or a later
abstract Young-tower theorem.

The following proposition-changing choices also remain unresolved:

- the phase space, discrete map, regularity or singularity class, invariant set, and invertibility
  convention;
- the hyperbolic product structure, stable and unstable families, branch partition, return map,
  separation time, contraction, distortion, and absolute-continuity hypotheses;
- the return-time codomain, positivity, measurability, integrability or precise tail condition, and
  reference measure;
- the tower space and map, projection, lifted measure, normalization, and exact SRB convention;
- the aperiodicity or total-ergodicity condition, correlation definition, observable norm,
  constants, and rate if mixing is selected;
- the observable class, centering, convergence-in-distribution convention, variance, and
  coboundary space if the central limit theorem is selected; and
- the exact quantifier order, conclusion, and empty-base, zero-return, nonintegrable, periodic,
  constant-observable, zero-variance, and projection boundary cases.

Selecting one familiar result or introducing an abstract structure with the desired conclusion as
a field would invent or substitute mathematics. Section 5 of the rev-5.6 blueprint treats this
ambiguity and a missing expression fingerprint as hard blockers. There is therefore no canonical
expression on which to certify minimal imports, checked alternate transports, or meaningful
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations. Those tests
are undefined, not passed. The first failed gate is exact source-statement identity, and machine
state remains `M4`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` imports four pinned modules and re-elaborates seven adjacent APIs:
function iteration, iterated semiconjugacy, Birkhoff sums, set and measure restriction,
measure-preserving maps, and ergodicity. These checks establish that the pinned Lean environment is
usable and document possible substrate. They do not state a Young-tower theorem. The probe imports
cannot be claimed minimal for a target that does not exist.

A bounded search of pinned mathlib found no source-name occurrence for Young towers, Gibbs-Markov
towers, return-time towers, or inducing schemes across concatenated, dotted, underscored, spaced,
and hyphenated spelling variants. This is narrow discovery evidence, not a complete anchor audit
and not proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain`, `lake-manifest.json`, and probe
SHA-256 values are respectively `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`00da96b009fb9bc622396b4a0bbbaf69dba45a7d246ebbd7a8edc2f8d764cdc4`.

The automation-provided `Formalizations/Lean/.lake` link existed before this phase and points to
the canonical checkout's pinned artifacts. It was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1422` | 0 | rank 920, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all && git rev-parse HEAD && git rev-parse HEAD^{tree}` | 0 | before statement edits, only the pre-existing untracked `.lake` link was present; base revision and tree are recorded above |
| `rg` across the catalog, Stage0, manifest, intake manifest, and source crosswalk | 0 | found only the construction label and underspecified role gloss; the provisional intake leaves the exact claim and Lean target null |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1422/IntakeProbe.lean` | 0 | hashes agree with the environment fingerprint above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1422/IntakeProbe.lean` | 0 | seven adjacent pinned APIs elaborated; no target theorem was stated |
| bounded pinned-mathlib source search for Young towers, Gibbs-Markov towers, return-time towers, and inducing schemes | 1 | expected no-match exit; discovery-only feasibility evidence, not an anchor audit |
| `python3 Stage1_Instances/THM-M-1422/check_intake.py` | 1 | known stale intake-checker failure already present at the base: it unconditionally loads the intake worker's now-absent root self-test manifest; after this phase its closed intake-only artifact inventory is stale as well |
| `python3 -m json.tool Stage1_Instances/THM-M-1422/statement-blocker.json` and scoped Python assertions | 0 | blocker JSON parsed; target identity, null target, blocked gate, four undefined mutations, unchanged debt vector, false completion flags, and changed paths agree |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `opaque`, `constant`, or `unsafe` declaration |
| tracked and added-file whitespace checks | 0 | both blocker artifacts passed `git diff --check` / `git diff --no-index --check` |
| `test ! -e .stage1-worker-selftest.json` | 0 | required no-self-test boundary is preserved because the statement deliverable is blocked |

The historical `check_intake.py` already exits 1 at this base because it unconditionally loads the
intake worker's now-absent root self-test manifest. After these blocker artifacts are added, its
closed intake-only file inventory is stale as well. This statement run does not rewrite the intake
receipt, intake artifact list, historical hashes, or authoritative DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first accept the intake dependency. An accountable source reviewer must
then issue and independently approve a truth-valued target correction selecting exactly one
immutable source proposition, transcribe and crosswalk every incorporated definition, assumption,
conclusion, proof boundary, correction, and erratum, and freeze all system, tower, return-time,
measure, tail or integrability, aperiodicity, observable, binder, and boundary conventions relevant
to that choice.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. The root remains `[H5, M4, R4]`, with `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted and no receipt or
master acceptance is claimed.
