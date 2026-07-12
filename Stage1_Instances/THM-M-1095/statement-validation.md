# Exact-statement gate: blocked

Item: `S56-M-1095-STATEMENT`  
Theorem: `THM-M-1095`  
Base revision: `af3ab2139ee7b58a502efdf255f659aff45a2f9b`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
Its entire claim is `扩散过程的理论` (the theory of diffusion processes), attributed only to
"many mathematicians" in the twentieth century. This describes a field, not a proposition. It
does not identify a primary source, theorem locator, domains, ordered binders, hypotheses, or
conclusion.

The accepted intake records three materially different candidate families: a martingale-problem
characterization, SDE existence or uniqueness, and a transition-semigroup or generator result.
Each family itself contains inequivalent statements. The missing choices include:

- state space, time horizon, probability space, filtration, initial condition, and path regularity;
- weak versus strong solutions and existence versus pathwise, distributional, or semigroup
  uniqueness;
- coefficient regularity, growth, nondegeneracy, boundary behavior, and explosion assumptions;
- test-function or generator domain, Markov/Feller hypotheses, and transition-kernel conventions;
- the exact conclusion and its boundary from the separately scheduled martingale-problem,
  Krylov-estimate, Kolmogorov-equation, and diffusion-ergodicity targets.

Choosing conventional values would manufacture a theorem and could duplicate a neighboring target.
Encoding a generic interface that assumes an unspecified desired property would not establish
statement identity. Consequently no canonical expression, minimal-import claim, expression hash,
checked alternate transport, or meaningful mutation suite exists. Machine state remains `M4`;
statement acceptance and theorem completion are false.

## Lean boundary

The existing pinned Lean environment is usable. A scoped source search found general probability,
process, martingale, kernel, and integration substrate, plus historical artifacts for the distinct
`THM-M-1049` and `THM-M-1050` targets. A search of pinned mathlib's `Probability` and
`MeasureTheory` trees found no theorem-specific occurrence under the searched English terms
`diffusion process`, `stochastic differential equation`, `infinitesimal generator`, or
`martingale problem`. This is limited feasibility evidence only, not the later anchor audit and not
a substitute for the missing source proposition.

There is no applicable `lake env lean <canonical-target>.lean` check. Creating that file before a
source proposition is identified would violate the exact-statement gate rather than validate it.

## Validation record

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai). Existing `.lake` artifacts were
read only; no update, build, clone, fetch, or dependency mutation command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1095` | 0 | rank 535, planned, legacy artifacts unaccepted, theorem incomplete |
| target-scoped repository `rg` search for the ID, exact Chinese heading, and English gloss | 0 | only the underspecified catalog record, generated scheduling metadata, and this dossier; no exact proposition or target-specific Lean declaration |
| pinned-mathlib `rg` search for the four diffusion/SDE/generator/martingale-problem terms | 1 | no matches in the searched `Mathlib/Probability` and `Mathlib/MeasureTheory` trees; exit 1 means no match |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | SHA-256 values `651c8a...1d2` and `321626...d81`, fully recorded in `statement-blocker.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

## Retry condition

An accountable reviewer must pin an immutable primary-source edition, transcribe an exact numbered
proposition with stable page or section locators, audit corrections, and independently approve a
premise-by-premise crosswalk. The selection must resolve every domain, binder, assumption,
conclusion, and neighboring-target boundary above. A later statement run can then encode that claim,
minimize its pinned imports, serialize the elaborated expression and environment, check alternate
transports, and run all four required mutation classes.

This is the first failed gate. It does not complete the statement node or any later node. The
assigned deliverable is not genuinely self-tested to completion, so no
`.stage1-worker-selftest.json` is emitted.
