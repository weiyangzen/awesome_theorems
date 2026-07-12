# Exact-statement gate: blocked

Item: `S56-M-0345-STATEMENT`  
Theorem: `THM-M-0345`  
Base revision: `cc46a50150dae27c90dca0938294d8da17db9109`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical statement is the title "Hardy's uncertainty principle" and the gloss "a limit
on the decay of a function and its Fourier transform". It supplies no immutable primary-source
edition, theorem/page, formula, Fourier convention, hypotheses, or conclusion. Stage0 separately
marks the precise definitions and prerequisites as still to be supplied, while rev-5.6 treats its
`已验证` label as untrusted metadata.

The accepted intake correctly leaves the canonical claim null. The unresolved choices are
proposition-changing, not merely notational:

- one real dimension versus a higher-dimensional Euclidean space;
- pointwise Gaussian bounds versus almost-everywhere, big-O, or weighted-`L2` hypotheses;
- real- or complex-valued functions and the required measurability/integrability assumptions;
- the Fourier kernel, sign, measure, and `2 * pi` normalization, which change the critical constant;
- one shared decay-bound constant versus separate constants;
- only supercritical vanishing versus inclusion of critical Gaussian classification;
- literal, almost-everywhere, or `L2` equality and the treatment of the zero function.

Selecting a familiar one-dimensional pointwise formulation, an `L2` variant, or a
higher-dimensional theorem would therefore invent or substitute mathematics. Consequently the
phase fails at canonical human-claim identity, before ordered binders, minimal imports, normalized
expression serialization, alternate-form transports, or meaningful removed-hypothesis,
changed-domain, binder-scope, and boundary mutation tests can be established. No Lean declaration,
axiom, placeholder, weakened special case, or broadened target was introduced. Machine state
remains `M4`; statement acceptance and theorem completion are false.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports
`Mathlib.Analysis.SpecialFunctions.Gaussian.FourierTransform` and checks the general Fourier
integral, mathlib's real Fourier character, complex exponential, and `fourier_gaussian_pi`. It
elaborates successfully in the pinned environment. The last declaration proves that a Gaussian
transforms to a Gaussian under mathlib's normalization; it does not state Hardy's converse
rigidity or supercritical vanishing result and receives no statement or proof credit. Narrow
repository and pinned-mathlib searches found no source-frozen proposition or declaration named for
Hardy's uncertainty principle.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. Existing `.lake`
artifacts were used read-only; no update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran inside this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0345` | 0 | rank 838, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| repository `rg` search for the theorem names and Fourier/decay wording | 0 | found only underspecified metadata and this intake dossier; no exact proposition |
| pinned-mathlib `rg` search for Hardy uncertainty and Gaussian/Fourier decay formulations | 1 | no theorem-specific match (`rg` exit 1 means no match) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0345/IntakeProbe.lean` | 0 | all four pinned Fourier/Gaussian API checks elaborated |

There is no applicable exact-target `lake env lean` check: the source-dependent target expression
does not exist. Treating the Gaussian transform formula or an abstract proposition parameter as
the target would be fake evidence.

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary source, select and
transcribe an exact theorem with its incorporated definitions and assumptions, dispose of errata,
and independently approve the source mapping. The review must freeze the domain, codomain,
function class, Fourier normalization, decay bounds and constants, threshold, strict/critical
cases, equality mode, ordered binders, and degenerate cases listed above. A later statement run can
then encode that exact claim, minimize pinned imports, serialize and hash the elaborated expression,
compile checked transports, and run all four required mutation classes.

This is the first failed gate, not completion of the statement node or any downstream node. The
assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
