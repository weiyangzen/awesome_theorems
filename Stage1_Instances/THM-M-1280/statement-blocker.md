# Exact-statement gate: blocked

Item: `S56-M-1280-STATEMENT`  
Theorem: `THM-M-1280`  
Base revision: `6bcd5f977dc26298be5f77327a2616e726454eb7`

## Decision

The intake fixes the intended root as the solution of the Yamabe problem: every smooth closed
Riemannian manifold of dimension at least three admits a conformal metric of constant scalar
curvature. That exact target cannot yet be elaborated with the pinned Lean environment.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides smooth-manifold and
Riemannian-metric infrastructure, but source searches found no concrete Ricci tensor, scalar
curvature, conformal scalar-curvature transformation, or Yamabe-equation declaration. Thus the
mathematical conclusion cannot be stated over the pinned library's concrete geometric objects.
Replacing these missing notions by arbitrary `Prop` fields or uninterpreted functions would prove
only an abstract wrapper, not the Yamabe theorem, and receives no statement credit.

The source boundary also leaves connectedness, the exact dimension encoding, fractional-power
conventions, and curvature/Laplacian signs unresolved. These choices affect binders, hypotheses,
the conclusion, and the PDE transport, so selecting them without a source-level freeze would invent
mathematics.

## Checked Lean boundary

`StatementProbe.lean` uses the single import
`Mathlib.Geometry.Manifold.Riemannian.Basic`. It checks the available Riemannian metric,
smoothness, manifold, compactness, connectedness, and finite-dimension interfaces and elaborates a
positive continuous real-valued factor type. This is substrate evidence only; the file contains no
canonical theorem, axiom, proof placeholder, or surrogate curvature predicate.

Environment fingerprint:

- validation date: 2026-07-12;
- Lean toolchain: `leanprover/lean4:v4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`;
- mathlib checked revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`;
- canonical pinned `.lake` artifacts were reused without update, fetch, clone, or build.

## Validation record

All commands ran in this worker clone; the Lean command ran from `Formalizations/Lean`.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1280/StatementProbe.lean` | 0 | pinned manifold substrate and positive factor boundary elaborated |
| `lake env lean --version` | 0 | Lean 4.29.0, commit shown above |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | exact pinned mathlib revision shown above |
| `rg -n -i 'scalar.?curvature|ricci|yamabe' .lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching concrete API; exit 1 means no matches |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard consistent; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1280` | 0 | rank 451, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1280/statement-blocker.json >/dev/null` | 0 | blocker record is valid JSON |
| `rg -n '\\b(sorry|axiom|admit)\\b' Stage1_Instances/THM-M-1280/StatementProbe.lean` | 1 | expected: no prohibited declarations |
| `git diff --check -- Stage1_Instances/THM-M-1280` | 0 | no whitespace errors |

## Gate result and retry condition

First failed gate: exact Lean statement. Machine status remains `M4`; there is no canonical
declaration, elaborated expression hash, checked alternate transport, or meaningful mutation suite.
Retry after compatible pinned concrete curvature and conformal-rescaling APIs exist and the listed
source choices are frozen.

The assigned phase is blocked, not self-tested complete, so no `.stage1-worker-selftest.json` is
emitted. This advances no anchor-audit, obligation-tree, proof, validation, release, or theorem-
completion state.
