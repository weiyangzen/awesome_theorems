# Exact-statement gate: blocked

Item: `S56-M-1142-STATEMENT`  
Base revision: `fd794b08bc7a68ef5f74c5814822e5a62b63946e`

## Decision

The exact Lean 4 target cannot yet be truthfully elaborated. The repository's entire mathematical
claim is "convergence of a sequence of harmonic functions". The available records provide no
primary-source edition, theorem number, page, definition, hypotheses, or conclusion precise enough
to select one proposition.

In particular, the accepted intake leaves all of the following statement-defining choices open:

- an increasing sequence of positive harmonic functions versus an arbitrary locally bounded
  family or sequence;
- pointwise convergence, locally uniform convergence on compact subsets, convergence of
  derivatives, or a dichotomy allowing locally uniform divergence to positive infinity;
- whether boundedness at one point, local boundedness above, or another convergence-enabling
  hypothesis is assumed;
- the connected open domain, ambient finite-dimensional real space, scalar codomain, sequence
  indexing, and precise harmonicity predicate;
- the finiteness and harmonicity of the limit and the policies for empty, disconnected, and
  zero-dimensional domains.

These variants are not interchangeable statement encodings. Selecting the familiar monotone
Harnack principle, a normal-family compactness theorem, or merely pointwise convergence would add
mathematics absent from the source record. Consequently this phase fails at exact human-claim
identity, before a canonical declaration, minimal-import closure, expression fingerprint, checked
transport, or meaningful statement mutation can be accepted.

## Lean discovery boundary

The pinned mathlib snapshot supplies the predicate
`InnerProductSpace.HarmonicOnNhd` in
`Mathlib.Analysis.InnerProductSpace.Harmonic.Basic`. It describes functions on finite-dimensional
real inner-product spaces that are harmonic in a neighborhood of a set. The module elaborates in
the pinned project environment. A scoped search found elementary harmonic-function APIs, complex
mean-value and Poisson results, and the complex-plane Liouville theorem, but no declaration whose
name or source text identifies a harmonic-function convergence theorem.

This establishes only that one possible harmonicity encoding is available. It neither selects the
human theorem variant nor supplies a convergence conclusion. The import is therefore discovery
evidence, not a claimed minimal import for THM-M-1142, and no mathlib declaration or proof credit is
accepted by this statement phase.

## Required unblock

An accountable source review must select an immutable primary edition or scan and record the exact
theorem/page, wording, definitions, hypotheses, conclusion, and relevant errata. It must resolve the
monotonicity or boundedness premise, convergence topology, divergence alternative, limit
harmonicity, domain assumptions, and degenerate cases. A later statement execution can then encode
that proposition, minimize its pinned imports, print and hash the elaborated expression, check any
alternate encoding, and mutation-test hypotheses, domains, binder scope, and boundary policy.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. Lean commands ran from `Formalizations/Lean`
against the existing `.lake` symlink to the canonical pinned artifacts. No dependency update,
build, clone, or fetch was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1142` | exit 0; rank 347, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake env lean .lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Harmonic/Basic.lean` | exit 0; pinned harmonic-function definition module elaborated with no diagnostics |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |
| scoped `rg` search for harmonic convergence declarations in pinned mathlib | exit 0; harmonic definitions and adjacent results found, but no harmonic-function convergence declaration identified |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked source transport, and mutation tests.
The assigned statement phase is therefore not self-tested or complete, and no
`.stage1-worker-selftest.json` is emitted. This artifact claims no theorem completion and no credit
for any downstream node.
