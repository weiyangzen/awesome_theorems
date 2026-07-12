# Exact-statement gate: blocked

Item: `S56-M-1210-STATEMENT`  
Theorem: `THM-M-1210`  
Base revision: `7c261cad5ed43a724864ac5581564164750b865c`

## Decision

The repository record does not identify a unique truth-valued mathematical claim that can be
elaborated exactly in Lean. Its complete mathematical wording is "local smoothing of solutions to
dispersive equations." This describes a family of results, not one theorem. It does not determine:

- the dispersive equation, propagator, coefficient class, or solution notion;
- the scalar field, spatial dimension, time interval, or initial-data class;
- whether "local" means a compact spatial cutoff, a weight, a bounded time interval, or a
  microlocal restriction;
- the Sobolev or Fourier multiplier used to express smoothing, the derivative gain, or the
  spacetime norms and exponent range;
- endpoint exclusions, homogeneous versus inhomogeneous form, or the dependence of the estimate's
  constant.

These choices produce inequivalent propositions. In particular, selecting a free Schrodinger,
wave, Kato, variable-coefficient, or manifold local-smoothing estimate would invent scope absent
from the source. Selecting the separately listed Sogge local-smoothing theorem or local-smoothing
conjecture would substitute a neighboring target. The repository status label `已验证` is explicitly
untrusted metadata and supplies neither a source statement nor a proof.

The intake therefore correctly records `H4/M4`, a null canonical Lean target, and an open primary-
source decision. The phase fails at canonical human-claim identity, before a minimal import set,
elaborated expression, expression fingerprint, or environment fingerprint can be truthfully
produced. There is also no source-relative alternate encoding or meaningful removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutation suite.

## Validation evidence

Commands ran from the worker clone on 2026-07-12. The existing pinned Lean artifacts were used
read-only; no update, build, fetch, clone, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1210` | 0 | rank 403, planned, hard anchor/wrapper lane, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | toolchain `651c8acc...b1d2`; manifest `321626c8...2d81` |

No theorem file was sent to Lean: there is no exact proposition to put in such a file. Elaborating
an arbitrary representative would check a broadened or substituted theorem and would not satisfy
this statement node.

## Retry condition

An accountable source reviewer must first select a stable primary source and record an immutable
edition, exact theorem/page and wording, all definitions, ordered binders, hypotheses, restrictions,
conclusion, constant dependencies, and errata. The scope decision must explicitly distinguish this
generic entry from the separately listed Sogge theorem and local-smoothing conjecture. A later
statement worker can then encode that exact claim, minimize its pinned imports, serialize its
elaborated expression and environment fingerprint, check any alternate transports, and run the
four required mutation classes.

First failed gate: exact source-statement identity. This artifact does not complete the statement
node, accept a receipt, or claim audit/theorem completion. The assigned deliverable is not genuinely
self-tested, so no `.stage1-worker-selftest.json` is emitted.
