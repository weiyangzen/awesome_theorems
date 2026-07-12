# Exact-statement gate: blocked

Item: `S56-M-1203-STATEMENT`  
Theorem: `THM-M-1203`  
Base revision: `446f3e80e7a93deeca70150fa80d9ee079ee0586`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
Its complete mathematical wording is only "the entropy condition for scalar conservation laws."
The intake identifies Oleinik's 1957 paper as a bibliographic candidate, but the repository has no
stable scan, pinpoint theorem/page/equation, source transcription, translation crosswalk, or errata
review from which to recover the ordered binders, hypotheses, and conclusion.

In particular, the record does not decide:

- whether the target is a local shock admissibility condition, a one-sided spatial estimate, or a
  theorem about weak entropy solutions;
- the flux regularity and convexity assumptions, space-time domain, and solution or trace class;
- the left/right trace orientation and the sign convention for the conservation law;
- the Rankine-Hugoniot speed convention and whether it is a hypothesis or derived quantity;
- the interval orientation, endpoint treatment, strictness, and inequality direction in a
  secant-slope formulation; or
- whether the claimed result is a definition, a necessary condition, an equivalence, an existence
  theorem, or a uniqueness theorem.

These choices produce inequivalent propositions. In particular, a shock chord condition cannot be
silently replaced by the later one-sided estimate or by a Kruzkov entropy formulation. Choosing one
convenient formulation would substitute mathematics rather than elaborate the exact target.
Consequently there is no truthful canonical expression, minimal import set, expression fingerprint,
checked alternate transport, or meaningful removed-hypothesis, changed-domain, changed-binder-scope,
and boundary-case mutation suite.

No Lean declaration or abstract interface assuming the intended conclusion was introduced. The
metadata label `已验证` supplies neither source identity nor kernel evidence. Statement acceptance,
audit completion, and theorem completion remain false; the intake vector `[H3, M4, R3]` is not
upgraded.

## Pinned environment and scoped search

Commands were run inside this worker clone on 2026-07-12 (Asia/Shanghai). Existing `.lake`
artifacts were only read. No dependency update, build, clone, or fetch was performed.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1203` | 0 | Rank 397, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Produced the Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Produced the Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C "$(readlink -f Formalizations/Lean/.lake/packages/mathlib)" rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| `rg -n -i "oleinik\|entropy condition\|entropy solution\|conservation law\|rankine.?hugoniot" Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No textual match in pinned mathlib source |
| repository scoped search for `Oleinik`, its Chinese labels, and `scalar conservation law` | 0 | Found only underspecified metadata, intake material, distinct neighboring targets, and a historical generic conservation-law model; no source-frozen proposition for this target |

There is no applicable `lake env lean <target>.lean` elaboration check: the exact expression does
not exist. Elaborating a selected shock condition or an abstract predicate would be fake statement
evidence rather than the assigned deliverable.

## Retry condition

An accountable source review must provide an immutable primary-source edition, exact page and
equation or theorem, surrounding definitions and assumptions, translation correspondence, and
errata disposition. It must freeze every convention and distinguish the local shock condition from
the one-sided estimate and entropy-solution formulations. A later statement run can then crosswalk
each binder, hypothesis, and conclusion, encode the exact Lean expression, minimize pinned imports,
fingerprint the elaboration and environment, check any alternate transports, and execute all four
required mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
