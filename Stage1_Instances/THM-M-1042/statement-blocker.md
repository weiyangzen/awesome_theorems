# Exact-statement gate: blocked

Item: `S56-M-1042-STATEMENT`

## Decision

The exact Lean 4 target cannot yet be truthfully elaborated. The accepted intake record freezes the
conventional stopped-process family

`E_x[f(X_tau)] = f(x) + E_x[integral_0^tau (A f)(X_s) ds]`,

but explicitly leaves the source variant and its hypotheses unresolved. The repository has not
provided an inspected, immutable primary-source theorem/page transcription. Consequently the
following choices remain underdetermined and mathematically non-equivalent:

- the class of Markov processes and the filtration/initial-law conventions;
- the definition and domain of the infinitesimal generator;
- bounded stopping times versus localization or uniform-integrability hypotheses;
- the measurability and integrability assumptions on `f`, `A f`, the stopped value, and the time
  integral;
- equality of finite real expectations versus an extended-integral formulation.

Choosing any one of these formulations from convention would invent assumptions and substitute a
nearby theorem for the unidentified source target. Section 5 of the rev-5.6 standard makes statement
ambiguity a hard blocker. The intake crosswalk also explicitly forbids replacing the root with the
deterministic-time semigroup formula or the discrete-time analogue.

## Lean boundary checked

`StatementProbe.lean` elaborates the closest independent interfaces exposed by the pinned
environment: Markov kernels, filtrations, stopping times and stopped processes, martingales,
interval integration, and right-derivative infrastructure. These types do not identify the missing
source choices or provide a canonical continuous-time Markov-process/generator package.

The legacy file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_235.lean` is discovery material,
not an exact target. It replaces the stopped-time claim by a deterministic-time semigroup identity
and stores `markovProcessRealization` as an unconstrained `Prop`. Its own documentation says that it
lacks a concrete continuous-time Markov-generator object. Crediting its `StatementShape` would
therefore violate the intake boundary and the prohibition on broadened or substituted theorems.

## Validation record

Base revision: `e1aeca70d414df009dea3559577ea90aa9834089`.

Commands were run from this worker clone; the Lean commands used the existing pinned `.lake`
artifacts, without updating or fetching dependencies.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1042` | exit 0; rank 235, planned, L0/rework-required, theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-1042/StatementProbe.lean` (from `Formalizations/Lean`) | exit 0; all eight substrate interfaces elaborated |
| `lake env lean AwesomeTheorems/Stage1/S1_M_235.lean` (from `Formalizations/Lean`) | exit 0; legacy discovery artifact elaborated, without proving its assumed `StatementShape` |
| `lake env lean --version` (from `Formalizations/Lean`) | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git diff --check -- Stage1_Instances/THM-M-1042` | exit 0; no output |

Environment: pinned toolchain `leanprover/lean4:v4.29.0`; pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Gate result and retry condition

First failed gate: section 5 exact statement identity. Without a source-exact proposition, no honest
canonical-expression hash, checked transport, or removed-hypothesis/domain/binder-scope/boundary
mutation suite exists. Machine debt remains `M4`.

Retry after an authoritative primary-source transcription pins the exact stopped Dynkin formula,
ordered assumptions, and conventions above, and after a concrete Lean object model encodes those
assumptions rather than accepting the desired stochastic facts as opaque propositions.

The assigned statement phase is not self-tested as complete, so no
`.stage1-worker-selftest.json` is emitted. No proof, downstream audit, or theorem completion is
claimed.
