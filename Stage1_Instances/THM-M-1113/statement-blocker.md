# Exact-statement gate: blocked

Item: `S56-M-1113-STATEMENT`  
Theorem: `THM-M-1113`  
Base revision: `d6c8d69dcdc00307a764772787a5e3d4d895147b`

## Decision

The exact Lean 4 target cannot be truthfully selected from the accepted intake or the repository
source record. The complete catalogue wording is `随机图的相变现象` ("the phase-transition
phenomenon in random graphs"), attributed to Erdos and Renyi in 1960. It does not identify a
numbered result, model, asymptotic regime, quantifiers, or conclusion. The intake accordingly left
the exact source theorem and formal statement open; its proposed two-regime `G(n,p)` description
is a scope hypothesis, not a source-certified statement.

The historical primary-source candidate, Erdos and Renyi, "On the evolution of random graphs",
studies the uniform graph process usually expressed as `G(n,m)`. The pinned mathlib API instead
defines the binomial law `SimpleGraph.binomialRandom`, explicitly noting that this is a related but
different model from the one introduced by Erdos and Renyi. Choosing that API and the familiar
modern scaling `p = c/n` would therefore require a source-audited and checked model transport; it
cannot be treated as a notational restatement.

Several proposition-changing choices remain unresolved:

- whether the root uses `G(n,m)`, `G(n,p)`, or the coupled random-graph process;
- whether it asserts only the threshold location or quantitative component-size laws;
- the exact fixed or varying parameter sequence and all rounding conventions;
- the probability mode and its ordered asymptotic quantifiers;
- the subcritical bound, the supercritical giant fraction, uniqueness, and bounds on other
  components;
- inclusion or exclusion of the critical window and all boundary cases.

Freezing any conventional version would substitute an inferred theorem for the unknown root.
Encoding the missing content behind an abstract predicate would be a placeholder. Both are
forbidden. Consequently there is no canonical proposition on which minimal imports, an elaborated
expression fingerprint, checked transports, or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary mutations can be established. Machine debt remains `M4`; no
statement or theorem completion is claimed.

## Lean boundary

The existing pinned environment is usable. Pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` contains
`Mathlib.Probability.Combinatorics.BinomialRandomGraph.Defs`, which defines the binomial random
graph measure and elementary distribution facts. A scoped source search found no phase-transition
or giant-component theorem. This is feasibility evidence only, not an anchor audit and not an
exact target. No synthetic Lean probe was created because elaborating a locally invented
proposition would provide false statement evidence.

## Validation record

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai). The canonical `.lake` tree was
read only; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1113` | 0 | rank 553, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | SHA-256 values `651c8a...1d2` and `321626...d81` |
| `git -C /home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| pinned-mathlib `rg` search for `random graph`, `giant component`, and `phase transition` | 0 | binomial-random-graph definitions found; no phase-transition or giant-component theorem |

## Retry condition

An accountable reviewer must preserve an immutable primary-source copy, record its content hash,
transcribe a specific theorem and all imported definitions with page locators, audit errata, and
independently approve the crosswalk. The statement phase can then freeze every binder and model
convention, implement or import the real Lean substrate, minimize imports, serialize the
elaborated expression and environment, check the `G(n,m)`/`G(n,p)` transport if applicable, and run
all four mutation classes.

This records the first failed gate and does not complete this or any downstream node. The assigned
deliverable is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
