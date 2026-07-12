# Exact-statement gate: blocked

Item: `S56-M-1059-STATEMENT`  
Base revision: `76c08cb569093ff0ea02564e80dced5284ebd59d`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
complete mathematical wording is "large deviations of sums of independent random variables". It
does not determine a single proposition, because it leaves open:

- independent versus identically distributed independent variables, and the law or array model;
- real-valued, finite-dimensional, or another state space;
- sums versus empirical means and the speed/normalization of the asymptotic;
- a one-sided tail limit versus a full large-deviation principle;
- the moment-generating-function domain and finiteness assumptions;
- the rate function's extended-real representation and boundary conventions;
- the topology and the open/closed-set formulation used for a full LDP.

These choices give inequivalent theorems. Selecting the modern real-valued i.i.d. LDP from Dembo
and Zeitouni, Cramer's historical scalar tail theorem, or a convenient special case would invent or
substitute mathematics. The intake dependency explicitly records the same ambiguity and leaves its
canonical module, declaration, expression hash, and environment fingerprint null. It requires an
exact source audit before the statement phase selects a target.

Consequently the phase fails at canonical human-claim identity, before a minimal import set,
elaborated expression fingerprint, checked alternate transports, or meaningful removed-hypothesis,
domain, binder-scope, and boundary mutations can be established. The metadata label `已验证` is
untrusted and supplies neither source identity nor kernel evidence.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_251.lean` was inspected and elaborated only as
legacy discovery input. It does not repair the source ambiguity. Its plain-real `StatementShape`
chooses a full LDP for real-valued i.i.d. variables with exponential integrability for every real
parameter. Moreover, its `CramerData` contains `terminalCramerConclusion` as a field, so the target
conclusion is already an input datum. Other fields named `exponentialTightnessBridge`,
`convexDualityBridge`, and `lowerBoundBridge` are unconstrained propositions. This is an abstract
boundary/package shape, not a source-backed canonical Cramer theorem.

The same legacy file separately describes a custom `EReal` terminal-scale candidate, confirming
that even it has not frozen one representation. Its four imports are therefore not evidence of a
minimal import set for the exact target. Successful elaboration proves only that this historical
candidate file is well typed in the pinned environment; rev-5.6 gives it no inherited statement or
proof credit.

## Required unblock

An accountable source reviewer must pin a stable primary or authoritative modern source by
edition, theorem/page, and exact wording, then freeze the random-variable model, independence and
identical-distribution premises, state space, normalization and speed, moment assumptions,
extended-real conventions, rate function, topology, conclusion form, and degenerate cases. A later
statement worker can then encode that exact claim, minimize imports, print and hash its elaborated
expression, check any transport from an alternate encoding, and run structural mutations.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12. The existing canonical `.lake` artifacts
were used read-only; no update, build, clone, or fetch was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1059` | exit 0; rank 251, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_251.lean)` | exit 0; legacy candidate declarations and audit probes elaborated and printed; no canonical-statement credit |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |
| `git diff --check -- Stage1_Instances/THM-M-1059` | exit 0 before this artifact was added; no whitespace errors in the existing owned dossier |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked transport, and mutation tests. The
assigned phase is therefore blocked rather than self-tested, and no `.stage1-worker-selftest.json`
is emitted. No theorem completion or downstream-node credit is claimed.
