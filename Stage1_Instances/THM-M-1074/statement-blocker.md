# Exact-statement gate: blocked

Item: `S56-M-1074-STATEMENT`  
Theorem: `THM-M-1074`  
Base revision: `25cf50267d347d2c52825407423be2c479090f93`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record supplies only the title "compound Poisson process," the attribution "many mathematicians,"
the period "twentieth century," and the gloss "a generalization of the Poisson process." It gives
no primary-source theorem, page, exact proposition, definitions, hypotheses, or conclusion. The
intake therefore correctly leaves source selection and the formal statement open. Its Kingman and
Applebaum references are discovery candidates whose exact results have not been inspected or
selected; they are not statement evidence.

The title names a construction or class of processes rather than one uniquely determined theorem.
Standard, inequivalent claims under this name include:

- defining `X_t` as the random sum of iid marks through a Poisson count;
- proving stationary independent increments, stochastic continuity, or cadlag paths;
- identifying each marginal as a Poisson mixture of convolution powers;
- proving the characteristic-function identity
  `E[exp(i u X_t)] = exp(lambda * t * (E[exp(i u Y_1)] - 1))`;
- characterizing finite-activity Levy processes as compound Poisson processes, possibly with drift.

The repository text does not select among these. It also does not fix the mark space, time domain,
rate convention, indexing and empty sum, independence notion, measurability or integrability
assumptions, equality versus equality in distribution, Fourier sign, filtration, or whether zero
rate is admitted. These choices alter domains, ordered binders, hypotheses, conclusion, and
boundary cases. Choosing one claim, combining several, or formalizing only the construction would
invent or substitute mathematics rather than elaborate the exact target.

Consequently there is no canonical Lean expression on which to minimize imports, compute an
expression fingerprint, establish checked transports, or run meaningful removed-hypothesis,
changed-domain, binder-scope, and boundary mutations. No Lean declaration, axiom, placeholder,
assumed conclusion, weakened special case, or broadened theorem was introduced. Machine state
remains `M4`; statement acceptance, audit completion, and theorem completion are false.

## Pinned environment and validation

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. The canonical linked `.lake` artifacts were read only; no
update, build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1074` | 0 | Rank 516, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the Chinese/English title and gloss | 0 | Found only the underspecified metadata, generated target listings, intake dossier, and incidental mentions in separately owned targets; no source-frozen proposition |
| pinned-mathlib `rg` search for compound/marked Poisson process and Poisson random-sum names in `Mathlib/Probability` and `Mathlib/MeasureTheory` | 1 | No matching textual declaration (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` command: an exact expression does not exist.
Elaborating an arbitrary member of the theorem family, or an interface which assumes its desired
properties, would be fake statement evidence rather than the assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact theorem or
definition-plus-result, record its page, complete wording, definitions, assumptions, proof boundary,
and errata, and decide which of the inequivalent conclusions above is canonical. It must freeze the
mark space, time and rate domains, iid and independence semantics, finite-sum convention, equality
notion, characteristic-function convention, filtration/path requirements, and degenerate cases.
Only then can a later statement run elaborate that exact claim, minimize pinned imports, fingerprint
the expression, crosswalk it row by row, and run structural mutation tests.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
