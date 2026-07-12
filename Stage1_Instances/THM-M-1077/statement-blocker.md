# Exact-statement gate: blocked

Item: `S56-M-1077-STATEMENT`  
Theorem: `THM-M-1077`  
Base revision: `a17f2bfe82ce19994b641db8436a12b449276a23`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record supplies only the title "Blackwell renewal theorem," the gloss "asymptotics of the renewal
function," the author and year, and an untrusted `verified` label. The intake names Blackwell's 1948
paper and Feller as discovery leads, but it records no inspected immutable edition, theorem/page
transcription, errata disposition, or source-accepted statement.

The intake's two-branch prose is a deliberately provisional theorem-family boundary, not an exact
source statement. In particular, the available evidence does not decide:

- whether the interarrival distribution is supported on `[0, infinity)` or `(0, infinity)`, and
  whether an atom at zero is allowed;
- whether the renewal measure includes the order-zero convolution term;
- the open/closed interval endpoint convention for the nonarithmetic increment;
- the exact definition of arithmeticity, maximal span, and the origin of the supporting lattice;
- the lattice branch's indexed cell or point-mass formula and quantifier order;
- whether the authoritative root contains both branches or only the nonarithmetic theorem;
- the source's finiteness, positivity, and normalization conventions for the mean.

These choices change domains, hypotheses, binders, and conclusions. Choosing familiar modern
conventions would invent the missing source crosswalk. Likewise, elaborating an abstract predicate
which assumes the desired renewal limit would substitute a tautological interface for Blackwell's
theorem. No `Statement.lean`, axiom, placeholder, weakened special case, or broadened target is
introduced.

The exact human claim therefore fails before minimal imports, expression serialization, checked
alternate transports, or meaningful removed-hypothesis, changed-domain, binder-scope, and boundary
mutations can be established. Machine state remains `M4`; statement acceptance and theorem
completion are false.

## Pinned environment and validation

Commands ran inside this worker clone on 2026-07-12 (Asia/Shanghai). The existing `.lake` symlink
and pinned artifacts were read only. No update, build, clone, fetch, or dependency mutation was
performed.

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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1077` | 0 | Rank 519, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for `Blackwell`, the Chinese title/gloss, renewal measures, and interarrivals | 0 | Found only underspecified catalog metadata, the provisional intake, and adjacent dossiers; no source-frozen proposition |
| pinned-mathlib `rg` search for `Blackwell`, renewal theorem/measure/process/function, `interarrival`, and `nonarithmetic` | 1 | No matching theorem-specific API (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` check: the exact target expression required by
the gate does not exist. Creating a guessed target merely to obtain exit 0 would be false evidence.

## Retry condition

An accountable source review must preserve and inspect an immutable primary-source edition, record
the exact theorem/page and wording, dispose of errata, and resolve every distribution, renewal,
endpoint, arithmetic-span, branch, binder, and normalization choice above. A later statement run
can then crosswalk every source component, elaborate that exact proposition with minimal pinned
imports, serialize its expression and environment, compile checked alternate transports, and run
all four mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
