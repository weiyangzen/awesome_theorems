# Exact-statement gate: blocked

Item: `S56-M-1221-STATEMENT`  
Theorem: `THM-M-1221`  
Base revision: `bf8f1a403fb8c22395ec64f92f93fed974f23c83`

## Decision

The repository does not identify an exact mathematical statement that can be translated into Lean
without inventing or substituting mathematics. Its complete claim is the label "Segal theorem",
the attribution Irving Segal (1963), and the gloss `NLW的局部适定性` (local well-posedness of
NLW). The Stage0 entry explicitly leaves the precise definitions, premises, proof route, axioms,
and formal artifacts open. The target manifest adds no mathematical detail, and its `已验证` value is
explicitly untrusted metadata rather than source or kernel evidence.

That record does not determine any of the following statement-critical data:

- the wave equation, spatial domain and dimension, scalar field, or sign convention;
- the nonlinearity and its parameter, smoothness, growth, or smallness restrictions;
- the initial-data space, solution space, and weak, mild, or strong solution notion;
- the lifespan quantifiers, maximal-interval policy, or dependence of lifespan on data;
- the precise existence, uniqueness, and continuous-dependence clauses and their topologies;
- endpoint, zero-data, symmetry, finite-energy, and other boundary or degenerate cases.

Different choices give inequivalent nonlinear-wave theorems. In particular, choosing a generic
abstract semilinear evolution theorem, a modern Sobolev-space power NLW theorem, or a later
Ginibre-Velo/Shatah-Struwe result would broaden or replace the unidentified source claim. The
repository provides neither a primary-paper title nor a theorem/page/equation pinpoint with the
definitions needed to decide among those choices.

Consequently there is no truthful canonical human statement, ordered binder list, or Lean `Prop`
to elaborate. Minimal imports and an elaborated-expression hash are properties of a particular
expression, so they also cannot be determined. Checked alternate transports and the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations would be
meaningless before that expression exists. No placeholder Lean declaration was created.

## Validation record

Commands were run in this worker clone on 2026-07-12. The existing pinned Lake environment was
inspected only for its version fingerprint; no `lake update`, build, dependency fetch, or `.lake`
mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1221` | exit 0; rank 412, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `git diff --check -- Stage1_Instances/THM-M-1221` | exit 0; no output |

## Required unblock

An accountable source reviewer must identify an authoritative stable edition by exact title,
theorem/page, equation, and imported definitions, and crosswalk every assumption and conclusion.
Only then can a statement worker freeze the canonical claim, encode and elaborate its exact Lean
target under minimal pinned imports, serialize the expression and environment fingerprints, check
credited transports, and run all four mutation classes.

First failed gate: exact source-statement identity. The statement node is not complete, no receipt
is accepted, and no downstream or theorem-completion credit is claimed. Because the requested
deliverable cannot be genuinely self-tested, no `.stage1-worker-selftest.json` is emitted.
