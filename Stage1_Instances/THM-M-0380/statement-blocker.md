# Exact-statement gate: blocked

Item: `S56-M-0380-STATEMENT`  
Theorem: `THM-M-0380`  
Base revision: `562c428c3d520ab42bba305174b7cad9409d7c0b`

## Decision

The repository does not contain enough source information to determine an exact mathematical
proposition, so no exact Lean 4 target can be truthfully elaborated. The complete target-specific
wording is the title "Sogge local smoothing theorem", the attribution Christopher Sogge, the year
1991, and the gloss "local smoothing of solutions of the wave equation". It gives neither a
primary-source theorem/page nor the definitions and errata needed to resolve the statement.

In particular, the record does not fix:

- the Euclidean wave propagator or a variable-coefficient Fourier integral operator;
- the spatial domain and dimension, scalar field, time interval, or localization cutoffs;
- the phase, amplitude, nondegeneracy, support, or curvature assumptions;
- the `L^p` exponent range and endpoint policy;
- the Sobolev/Bessel-potential convention and exact derivative gain or epsilon loss;
- the ordering of space-time norms or the allowed dependencies of the estimate's constant.

Each choice changes the domains, ordered binders, hypotheses, or conclusion. The intake mentions
the 1991 Seeger-Sogge-Stein paper and Sogge's monograph only as discovery candidates, without an
inspected theorem pinpoint. The inventory also schedules a second same-name target,
`THM-M-1211`, as well as generic local-smoothing and local-smoothing-conjecture targets; it does not
state which proved formulation distinguishes this root from them. Selecting a familiar Euclidean
estimate, a general FIO estimate, or a later sharp range would therefore substitute for or broaden
the unknown claim.

Consequently there is no source-faithful expression on which to perform minimal-import reduction,
kernel-expression fingerprinting, checked alternate transports, or the required removed-hypothesis,
changed-domain, binder-scope, and boundary mutations. An abstract predicate or a structure field
assuming the desired estimate would merely hide the missing statement. No such proxy, declaration,
`sorry`, axiom, or placeholder was added. The machine state remains `M4`; statement acceptance,
audit completion, and theorem completion remain false.

## Pinned validation evidence

Validation date: `2026-07-12` (`Asia/Shanghai`). The existing canonical `.lake` link was used
read-only. No update, build, dependency clone, fetch, or other mutation of `.lake` was run.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0380` | 0 | rank 868, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | produced the pinned Lean version and commit above |
| `cd Formalizations/Lean && lake --version` | 0 | produced the Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision above |
| repository `rg` search for the title and both source glosses | 0 | found only underspecified metadata, the two intakes, and duplicate scheduled targets; no exact proposition |
| pinned-mathlib `rg` search for Sogge, local smoothing, cinematic curvature, and Fourier integral operators | 1 | expected no-match exit; no theorem-specific declaration was found |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0380 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom in the owned Lean source |

There is no applicable `lake env lean <statement>.lean` command: no exact target expression exists.
Compiling an invented interface would validate that interface rather than the assigned theorem.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact theorem/page,
including referenced definitions and an errata check. It must freeze every operator, domain,
dimension, cutoff, curvature assumption, exponent, Sobolev order, norm ordering, constant dependency,
and endpoint convention above, and distinguish this target from `THM-M-1211`, `THM-M-0379`, and the
generic local-smoothing entries. A later statement run can then encode that precise result, minimize
its imports, fingerprint the elaborated expression, check alternate transports, and execute all four
mutation classes.

The assigned deliverable is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted. This artifact claims only a concrete first failed gate;
it does not alter the authoritative DAG or claim master acceptance.
