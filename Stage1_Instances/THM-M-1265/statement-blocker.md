# Exact-statement gate: blocked

Item: `S56-M-1265-STATEMENT`  
Theorem: `THM-M-1265`  
Base revision: `58cde546113e54bfa95299c69db6ee1508316872`

## Decision

No exact Lean 4 target can be truthfully elaborated from the frozen intake and repository source
record. The complete mathematical wording is `变分问题的直接求解` ("direct solution of
variational problems"), under the name `直接法` ("direct method"). This names a proof method, not
a proposition. In particular, the record does not determine:

- the ambient topological, metric, normed, Banach, reflexive, or Sobolev space;
- the admissible set, its nonemptiness, boundary/trace conditions, or closure properties;
- the functional's domain and whether its codomain is `Real`, `EReal`, or `ENNReal`;
- the topology or sequential convergence used for compactness and lower semicontinuity;
- whether compactness is assumed for the admissible set, derived from coercive sublevels, or
  obtained weakly from reflexivity and boundedness;
- the precise coercivity, bounded-below, properness, and lower-semicontinuity hypotheses; or
- the exact attainment conclusion and treatment of empty sets, infinite values, and non-Hausdorff
  or nonreflexive cases.

These choices produce inequivalent direct-method theorems. For example, compact-set attainment for
a lower-semicontinuous real function is not the same claim as weak attainment for a coercive weakly
lower-semicontinuous functional on a reflexive Banach space, nor as a PDE-specific Sobolev
minimization theorem. Selecting any one would broaden or substitute the source claim. The intake
record expressly leaves these choices unresolved and requires an authoritative formulation before
the statement phase may choose them.

Consequently the human-claim identity gate fails before ordered binders, minimal imports, a
canonical declaration, an elaborated-expression fingerprint, checked transports, or meaningful
mutation tests can be produced. No `Statement.lean` or `statement.json` is emitted, because either
would falsely imply that the missing mathematics had been fixed.

## Discovery boundary

The pinned mathlib snapshot contains useful but noncanonical special cases. In
`Mathlib.Topology.Order.Compact`, `IsCompact.exists_isMinOn` gives attainment for a continuous
function on a nonempty compact set. Mathlib also exposes lower-semicontinuous compact-minimization
APIs. These establish that candidate encodings are available; they do not identify which candidate
the source intended and receive no statement credit here.

The only repository Lean search hit for the phrase "direct method" is the legacy
`THM-M-1266` Tonelli artifact, not this target. Its abstract proposition fields and compact
lower-semicontinuity wrapper cannot be imported as the statement of `THM-M-1265`. The manifest also
records no legacy priority slot for this target. Under the uniform `L0 / rework_required` rule,
neither neighboring artifacts nor the untrusted source label `已验证` authorize a scope decision.

## Required unblock

An accountable scope owner must bind `THM-M-1265` to an immutable primary-source edition and an
exact theorem/page (or make an explicit master scope decision). The decision must freeze the
ambient and admissible spaces, functional and codomain, convergence topology, compactness or
coercivity mechanism, lower-semicontinuity hypotheses, exact conclusion, and degenerate cases. A
later statement worker can then encode precisely that claim, minimize its pinned imports, serialize
and hash the elaborated expression, add checked alternate transports, and test removed hypotheses,
changed domains, binder scope, and boundary cases.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. Lean used the existing canonical pinned `.lake`
artifact; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1265` | 0 | rank 442, planned, no accepted legacy artifact, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| `rg -n -C 8 'THM-M-1265|直接法|变分问题的直接求解' Formalizations Docs/researches --glob '!**/.lake/**'` | 0 | only the underspecified research wording and a distinct Lyapunov-method entry were found; no exact target or target-owned Lean artifact |
| `rg -n 'direct method|Direct Method|IsCompact.*exists_isMinOn' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | candidate compact-minimum infrastructure found, but no source-identity decision |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked transports, and the required mutation
classes. The assigned phase is therefore blocked rather than self-tested, so no
`.stage1-worker-selftest.json` is emitted. No statement acceptance, downstream-node credit, audit
completion, or theorem completion is claimed.
