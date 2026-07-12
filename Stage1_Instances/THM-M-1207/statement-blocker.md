# Exact-statement gate: blocked

Item: `S56-M-1207-STATEMENT`  
Theorem: `THM-M-1207`  
Base revision: `446f3e80e7a93deeca70150fa80d9ee079ee0586`

## Decision

The repository source record does not contain a truth-valued mathematical claim that can be
elaborated exactly in Lean. Its complete content is the label `色散方程` ("dispersive equations")
and the phrase `Schrodinger方程等` ("Schrodinger equations, etc."). This identifies a broad family
of equations, not a proposition. In particular, it does not determine:

- an equation, sign convention, linear or nonlinear regime, or potential/coefficient class;
- spatial dimension, scalar field, time domain, initial/boundary data, or solution notion;
- function spaces, regularity and integrability assumptions, or endpoint restrictions;
- whether the conclusion is existence, uniqueness, decay, a spacetime estimate, smoothing,
  well-posedness, or scattering;
- a norm inequality, decay exponent, constant dependence, or excluded boundary cases.

These choices yield inequivalent propositions. Choosing the familiar free-Schrodinger
`L^1 -> L^infinity` decay estimate would invent an unstated root; choosing a Strichartz or local
smoothing estimate would additionally substitute neighboring targets `THM-M-1208` or
`THM-M-1210`. The discovery citation to Journe-Soffer-Sogge in the intake crosswalk is not a
pinpointed, accepted source statement and cannot supply the missing claim.

The intake dependency records this ambiguity as `H4/M4` and deliberately leaves the module,
expression, expression hash, and environment fingerprint null. Consequently this phase fails at
canonical human-claim identity, before minimal imports can be determined or a Lean expression can
be meaningfully elaborated. There is likewise no source-relative alternate encoding or valid
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutation suite.

## Validation evidence

Commands ran from the worker clone on 2026-07-12. The existing canonical `.lake` directory was
used read-only; no update, build, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1207` | 0 | rank 400, planned, hard anchor/wrapper lane, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1207/intake.json` | 0 | intake record is valid JSON and confirms the blocked exact-statement gate |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |

No theorem file was sent to Lean because the required exact proposition does not exist. Elaborating
an arbitrary probe would validate a substituted statement, not this node's deliverable.

## Retry condition

An accountable source reviewer must first select a stable primary source and record an immutable
edition, exact theorem/page and wording, all definitions, binders, hypotheses, restrictions,
conclusions, constant dependencies, and errata, while preserving the boundaries with
`THM-M-1208` through `THM-M-1210`. A later statement worker can then encode that claim, minimize its
pinned imports, serialize the elaborated expression and environment fingerprint, check alternate
transports, and run all four mutation classes.

First failed gate: exact source-statement identity. This artifact does not complete the statement
node, accept a receipt, or claim audit/theorem completion. The assigned deliverable is not genuinely
self-tested, so no `.stage1-worker-selftest.json` is emitted.
