# Statement gate blocker

Item: `S56-M-0132-STATEMENT`
Theorem: `THM-M-0132`
Verdict: blocked; no exact canonical Lean target is claimed.

This target-owned negative result is normalized to the HEAD statement contract. The selected
roles are `statement.json`, `Statement.lean`, `source_statement_crosswalk.md`, and exactly one
`stage1-node-receipt/1.0` phase receipt. The validator's typed semantic result is blocked with
`phase_accepted=false`; a successful validation run proves the blocker packet internally
consistent, not the positive statement deliverable. No declared statement validator existed at
the worker base, so the HEAD contract also forbids this new candidate validator from supporting
master acceptance until an authority-owned base validator is available in a fresh claim.

The v2 claim order is `(v2_execution_rank=283, phase_layer=1,
phase_item_id=S56-M-0132-STATEMENT)`. Its complete `parent_inspection_order` is `[]`: there are no
direct hard parents, transitive hard ancestors, reuse hints, or shared groups. The refreshed
schema-1.1 ledger records that empty traversal. No declaration, proof body, receipt, or acceptance
is reused or transferred.

## First failed gate

The intake identifies the human root precisely as BCDT Theorem A: every elliptic curve over the
rationals is modular. But neither the repository nor pinned mathlib defines the mathematical
relation "is modular" for a rational elliptic curve. The pinned APIs provide Weierstrass curves,
nonsingularity, congruence subgroups, modular forms, cusp forms, and q-expansions. Repository-wide
pinned-source searches found no newform/eigenform structure and no declaration relating an elliptic
curve to a modular form through its conductor, L-series, Frobenius traces, or Galois representation.

The legacy `AwesomeTheorems.Stage1.S1_M_049.StatementShape` cannot pass the exact-statement gate.
Its witness permits an arbitrary positive natural number, an arbitrary subgroup, an arbitrary cusp
form, and three freely supplied propositions, only one of which must be inhabited. It does not
require a normalized weight-two newform, conductor-level equality, or any concrete arithmetic
compatibility. Treating that boundary as BCDT Theorem A would strictly weaken and substitute the
source theorem.

In particular, its placeholder L-series, Frobenius-trace, and Galois-representation fields are
not source-admitted mathematical relations. The source's Gamma1/X1 convention likewise has no
checked transport to the available Gamma0 cusp-form surface.

Defining a fresh opaque compatibility proposition would have the same defect. Consequently an
exact normalized expression, expression hash, checked alternate transports, and meaningful
removed-condition mutations cannot truthfully be produced with the pinned object model. The gate
therefore remains `M3`: the mathematical claim is identified, but its exact Lean encoding is
blocked by formalization infrastructure.

`Statement.lean` checks only the minimal available curve and cusp-form object families. It
introduces no canonical target, theorem proof, axiom, or proxy modularity relation.

## Environment fingerprint

- Repository base revision: `1cc6aa61bb055a5c032297ee457905c849af7608` (tree
  `dc3053b55c5724ccb2e6a247e7deffebca9dbb99`).
- Validation date: 2026-07-17 (`Asia/Shanghai`).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- mathlib Lake pin and checked revision:
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

Commands ran from the worker clone and used only the existing pinned `.lake` artifacts. No update,
fetch, clone, or build command was used.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0132/Statement.lean` | 0 | Minimal pinned object-model probe elaborated; four expected declaration types printed; no canonical target |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_049.lean` | 0 | Legacy discovery boundary elaborated; this supplies no exact-statement credit |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision equals the manifest pin |
| `rg -n -i 'eigenform\|newform\|hecke.*eigen\|elliptic.*modular\|modular.*elliptic\|hasse.weil\|frobenius.*trace' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/.lake/packages/flt-regular --glob '*.lean'` | 0 | Only an expository Wiles citation matched; no relevant Lean declaration was found |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0132` | 0 | Rank 49, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0132` | 0 | No whitespace errors |

## Retry condition

Provide pinned Lean 4 definitions for a normalized weight-two newform, the elliptic curve's
conductor, and one source-faithful compatibility formulation, together with the representation and
isomorphism transports needed for BCDT Theorem A. The statement phase can then freeze the ordered
binders and conclusion, normalize and hash the elaborated expression, and run domain, hypothesis,
binder-scope, level, weight, normalization, and compatibility mutations.

Until then, statement acceptance and theorem completion are false. The target-owned negative
evidence is self-tested and emitted in `.stage1-worker-selftest.json` with state `[_]`, but that
packet is only a scheduler handoff. It grants no positive statement, master acceptance, audit
completion, or theorem-completion credit.
