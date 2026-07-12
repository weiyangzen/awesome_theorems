# Exact-statement gate: blocked

Item: `S56-M-1261-STATEMENT`  
Theorem: `THM-M-1261`  
Base revision: `9144fc9aa3522671a4cda7de9d460d01f382367a`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire mathematical claim is the label "Fourier integral operator" together with the description
"a tool for solving hyperbolic equations." This names a large operator calculus and its use, not
one proposition. The intake locates Lars Hormander, "Fourier integral operators. I", *Acta
Mathematica* 127 (1971), 79-183, DOI `10.1007/BF02392052`, only as a candidate source family; the
repository does not select or transcribe a numbered theorem from it.

Consequently the record does not determine any of the following statement data:

- a local oscillatory-integral theorem, a composition theorem, a mapping theorem, or a hyperbolic
  parametrix/solution theorem;
- the manifolds, dimensions, bundles, scalar field, Fourier normalization, or quantifier order;
- the phase class, homogeneity and nondegeneracy conditions, amplitude/symbol class and order, or
  equivalence convention;
- the canonical relation, support/properness assumptions, and function or distribution spaces;
- whether the conclusion is local, microlocal, or global, and exact or modulo a smoothing
  operator;
- the PDE operator, initial or boundary data, regularity conclusion, endpoint restrictions, and
  degenerate-case policy.

These choices produce inequivalent propositions. Choosing a familiar FIO boundedness,
composition, or parametrix result would substitute newly selected mathematics for the unidentified
root. A generic Fourier-transform or pseudodifferential-operator fact would be a still broader
substitution. The untrusted metadata value `已验证` supplies neither source-statement identity nor
kernel evidence.

The first failed gate is therefore rev-5.6 section 5 canonical human-claim identity, before a
minimal import list can be meaningful. There is no canonical declaration or expression to
elaborate, serialize, or hash, no checked alternate encoding, and no valid removed-hypothesis,
changed-domain, changed-binder-scope, or boundary mutation suite. Machine debt remains `M4`.

## Lean and repository boundary

There is no legacy Lean slot for this target (`legacy_priority_slot` is null) and no Lean file in
the owned directory. A case-insensitive search of the pinned mathlib source found no declaration or
definition matching `Fourier integral operator`, `FourierIntegralOperator`, `oscillatory integral`,
or `oscillatoryIntegral`. This negative search is not an anchor audit and does not identify the
missing human claim; it only confirms that no obvious existing declaration can serve as an exact
statement probe.

The existing pinned environment is usable: Lean is version `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and mathlib is pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. No `lake update`, build, dependency clone/fetch, or
mutation of `.lake` was performed.

## Validation evidence

Commands ran from this worker clone on 2026-07-12 unless the table states a subdirectory.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1261` | 0 | rank 438, planned, no legacy slot, `L0/rework_required`, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | SHA-256 `651c8acc...b1d2` and `321626c8...2d81` respectively |
| pinned-mathlib `rg` search for the four FIO/oscillatory-integral terms above | 1 | no matching Lean source; exit 1 is ripgrep's no-match result |

## Retry condition

An accountable source reviewer must select an immutable primary-source edition and exact
theorem/page, transcribe its claim, and crosswalk every operator convention, binder, hypothesis,
conclusion, qualification, and boundary case. A later statement worker can then encode that claim,
minimize its pinned imports, fingerprint the elaborated expression and environment, check credited
transports, and run all four required mutation classes.

This artifact records a blocker only. It does not complete the statement node, accept a receipt,
modify an execution state, or claim audit/theorem completion. The assigned phase is not genuinely
self-tested, so no `.stage1-worker-selftest.json` is emitted.
