# Exact-statement gate: blocked

Item: `S56-M-1423-STATEMENT`

Theorem: `THM-M-1423`

Base revision: `ffe94ac84965dc19f4923f88b7566072ddee37ae` (tree
`876a17f277d84dcf06ca672e5cd351edaa294495`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the technique label `耦合方法` ("coupling method"), the attribution
`众多数学家` ("many mathematicians"), the period `20世纪`, and the gloss `随机系统的同步`
("synchronization of random systems"). It supplies no bibliography, stable source identifier,
formula, definitions, ordered binders, hypotheses, conclusion, proof boundary, or errata. Stage0
explicitly leaves the exact definitions and premises, proof process, dependencies, alternate forms,
axioms, and machine artifact open. The catalog label `已验证` is untrusted under rev-5.6.

The words do not select one proposition. A coupling may be a joint law with fixed marginals, a
common-noise construction, a co-adapted coupling, a successful coupling, or a comparison method.
Synchronization may mean finite-time coalescence, almost-sure or in-probability distance
convergence, convergence in law, attraction to an invariant random point, or a singleton random
attractor. These alternatives have different hypotheses and conclusions. The intake's three
bibliographic examples are ambiguity witnesses only; none is an approved source for this target.

The following proposition-changing inputs therefore remain unresolved:

- the primary or authoritative source, exact theorem/page, incorporated definitions, proof
  boundary, corrections, errata, and independent source review;
- the probability/noise, state, and time spaces, universes, measurable/topological/metric
  structures, and filtration or regularity assumptions;
- the stochastic process, Markov kernel, random map, flow, cocycle, or stochastic equation and its
  initial-state and solution conventions;
- the joint law or coupling construction, marginal equations, common-noise, adaptedness, Markovian,
  or coalescence requirements;
- the synchronization predicate, quantifier order, exceptional-set scope, convergence mode and
  rate, or coupling-time conclusion; and
- empty or singleton states, identical initial states, degenerate noise, nonunique solutions,
  infinite coupling time, pseudometric zero, and other boundary cases.

Selecting a familiar coupling inequality, successful-coupling theorem, common-noise contraction,
weak synchronization result, or singleton-attractor theorem would invent or substitute missing
mathematics. An abstract structure that assumes synchronization as a field, a tautological
one-state system, or a definition restated as a theorem would do the same. Section 5 of the
rev-5.6 blueprint makes statement ambiguity and a missing expression fingerprint hard blockers.
There is consequently no canonical expression on which to certify minimal target imports, checked
alternate transports, or removed-hypothesis, changed-domain, changed-binder-scope, and boundary
mutations. Those four tests are undefined, not passed. The first failed gate is exact source-
statement identity, and the root remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` imports four pinned modules and checks ten adjacent APIs for
kernels, Markov kernels, kernel composition and powers, identical distributions, product-measure
marginals, measure maps, filter convergence, and distance. It elaborates successfully in the
pinned environment but states no target theorem. Those imports are discovery candidates only and
cannot be called minimal for a target that does not exist.

A bounded source-name search of pinned mathlib found no declaration for random-system
synchronization or probabilistic coupling under the searched phrases. The only synchronization
match was an unrelated tactic implementation comment. This is narrow discovery evidence, not an
anchor audit or proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The `lean-toolchain`, `lake-manifest.json`, and
probe SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`f9579659fbf111a30b6fea4fe968b5252f199622ac9424d9683c79fe0c8900dd`.

The automation-provided `Formalizations/Lean/.lake` link existed before this phase and points to
the canonical checkout's pinned artifacts. It was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1423` | 0 | rank 921, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all && git rev-parse HEAD && git rev-parse HEAD^{tree}` | 0 | before statement edits, only the pre-existing untracked `.lake` link was present; base revision and tree are recorded above |
| source-record and dossier `rg`/`nl` inspection | 0 | found only the method label and synchronization gloss; the intake leaves the canonical statement and formal target null |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD && git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD^{tree}` | 0 | pinned mathlib revision and tree recorded above; package status clean |
| `sha256sum Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Blueprint_rev-5.6.md skills/execute-stage1-rev56/SKILL.md Stage1_Instances/THM-M-1423/IntakeProbe.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | target manifest `02eec284...ab2c`, blueprint `234af60c...8ae`, skill `26d47a66...52b8`, and environment hashes recorded |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1423/IntakeProbe.lean` | 0 | ten adjacent pinned APIs elaborated; no target theorem was stated |
| bounded pinned-mathlib source search for synchronization/coupling phrases | 0 | one unrelated tactic-comment match; no target declaration found; discovery-only evidence |
| `python3 Stage1_Instances/THM-M-1423/check_intake.py` | 1 | known intake-only checker failure: it requires the root intake self-test manifest, which the integration commit did not retain; this statement run does not recreate an intake receipt or self-test |
| structured blocker JSON parse and scoped invariant checks | 0 | blocker identity, null target, all four undefined mutation classes, false completion flags, and no-self-test boundary agree |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `opaque`, `constant`, or `unsafe` declaration |
| scoped tracked and added-file whitespace checks | 0 | no whitespace diagnostics; the added-file checks normalize `git diff --no-index --check`'s expected difference status |
| `test ! -e .stage1-worker-selftest.json` | 0 | required no-self-test boundary is preserved because the statement deliverable is blocked |

The statement run does not rewrite the intake manifest, receipt, checker, historical hashes, task
DAG, generated blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first accept the provisional intake dependency. An accountable reviewer
must then preserve an immutable primary or authoritative source, select one exact truth-valued
passage with a page or section locator, transcribe every incorporated definition, binder,
hypothesis, conclusion, convergence or coupling-time convention, exceptional-set rule, and
boundary case, check corrections and errata, and justify why this proposition represents
`THM-M-1423` rather than a neighboring target. A second reviewer must approve the mapping.

A later statement worker can then encode that same claim with real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted and no statement
receipt or master acceptance is claimed.
