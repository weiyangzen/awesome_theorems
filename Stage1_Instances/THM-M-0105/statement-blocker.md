# Exact-statement gate: blocked

Item: `S56-M-0105-STATEMENT`

Theorem: `THM-M-0105`

Base revision: `d5771f240b8fe26277d018c90fec963af76ed7f2`

## Decision

No exact Lean 4 target can yet be truthfully elaborated for the intake-selected
Riemann--Roch formula. The statement item remains `[ ]`; lifecycle remains
`planned`; the root remains `[H5, M5, R4]`; `audit_complete` and
`theorem_complete` remain false.

The intake selects the intended human formula for a smooth projective
geometrically integral curve over an arbitrary field,

`l(D) - l(K_X - D) = deg(D) + 1 - g(X)`,

with `l(E) = dim_k H^0(X, O_X(E))`. But it explicitly records the formal
target as `not_frozen`, leaves both target fingerprints null, and identifies
several proposition-changing choices for this phase. Its only source lead is
Hartshorne, Chapter IV, Section 1, Theorem 1.3; the edition/page, definition
chain, assumptions, errata, and independent review have not been accepted.
In particular, the arbitrary-field geometrically-integral scheme
normalization is not yet bridged to that source's conventions.

The exact definitions of divisor, canonical divisor and its witness,
`O_X(D)`, degree, genus, and `l(D)` are not selected. Neither are the natural-
versus-integer codomain/coercion convention, projective-versus-proper boundary,
universe policy, or empty/nonempty curve boundary. Selecting those from
mathematical memory would invent part of the target rather than elaborate the
intake record.

The prerequisite `S56-M-0105-INTAKE` has provisional worker state `[_]`, not
master-accepted `[x]`. Dependency-ordered investigation is permitted, but an
accepted statement transition remains dependency-blocked as well.

## Rejected Legacy Substitute

`AwesomeTheorems.Stage1.S1_M_027.THM_M_0105_StatementShapeTarget` is discovery
input only. It assumes `IsIntegral`, `Smooth`, and `IsProper`, then stores
dimension and geometric connectedness as arbitrary proposition fields. It
omits the field-base restriction, concrete geometric integrality,
projectivity, divisors on the selected curve, canonicality, `O_X(D)`, global
sections, finiteness, and actual degree/genus definitions.

Its conclusion existentially chooses `RiemannRochDivisorData`, whose divisor
type, subtraction, degree, linear-series dimension, genus, and canonical
divisor are all unconstrained. That package can encode the desired equality
instead of stating Riemann--Roch for the input curve. Compiling or renaming it
would therefore be a broadened substitute and receives no statement credit.

## Pinned Lean Boundary

`StatementProbe.lean` uses five direct imports and checks only adjacent pinned
interfaces: `Scheme`, `Spec`, `Smooth`, `IsProper`,
`GeometricallyIntegral`, scheme modules and their presheaves, `Sheaf.H`, and
`Module.finrank`. It elaborates under the existing pinned environment, but it
contains no canonical target, proof, axiom, placeholder, or assumed
Riemann--Roch conclusion.

A bounded search of pinned mathlib source found no algebraic-geometry module
or declaration for Riemann--Roch, Cartier/Weil divisors on schemes, a canonical
or dualizing divisor/sheaf, or arithmetic genus. Existing function-field,
scheme-module, and sheaf-cohomology APIs are substrate only. Consequently the
probe imports are not claimed minimal for the absent canonical expression.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` at tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No dependency update,
build, clone, fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-15 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0105` | 0 | rank 27, planned, legacy artifacts unaccepted, theorem incomplete |
| pre-edit `git status --short`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base and tree are recorded in the JSON blocker |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions above |
| mathlib `rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | pinned revision/tree above; dependency worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0105/StatementProbe.lean` | 0 | nine adjacent interfaces elaborated; stdout SHA-256 `73b1db98...4e29`; no canonical target or proof body |
| bounded exact-topic search in pinned mathlib | 0 | no matching algebraic Riemann--Roch/divisor/genus interface; discovery evidence only |
| prohibited construct scan over owned Lean files | 0 | no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless constant, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0105/statement-blocker.json` | 0 | blocker JSON is valid |
| `git diff --check -- Stage1_Instances/THM-M-0105` | 0 | no whitespace diagnostics |

Without a canonical target, minimal imports cannot be certified, no expression
fingerprint can be produced, alternate transports cannot be credited, and the
required removed-hypothesis, changed-domain, binder-scope, and boundary-case
mutations are undefined rather than passed.

## Retry Condition

The integration lane must first master-accept the intake. An accountable
source reviewer must then preserve and hash an immutable source edition and
approve the exact arbitrary-field statement plus every incorporated
definition, convention, hypothesis, conclusion, and degenerate case. A future
statement worker can then encode precisely that reviewed claim using concrete
Lean objects, minimize imports, serialize its elaborated expression and
environment, compile every credited transport, and run all four mutation
classes.

This artifact records the first failed gate. Because the requested statement
deliverable is not genuinely self-tested, no statement receipt or
`.stage1-worker-selftest.json` is emitted.
