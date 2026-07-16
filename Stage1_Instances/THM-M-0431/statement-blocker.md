# Statement gate blocker

Item: `S56-M-0431-STATEMENT`  
Theorem: `THM-M-0431`  
Verdict: blocked; no exact canonical Lean target is claimed.

## Current contract normalization (2026-07-17)

The blocker has been replayed at repository base
`94009a6bebd743588e09c3b45bfbf18bf9b5c5e3` under the HEAD statement contract. The v2 claim key is
`(v2_execution_rank=293, phase_layer=1, phase_item_id=S56-M-0431-STATEMENT)`. The theorem-level
`parent_inspection_order` is exactly `[]`; the schema-1.1 dependency ledger records that empty
closure, so no provider declaration, body, receipt, or acceptance was reused. The intra-theorem
predecessor `S56-M-0431-INTAKE` was separately inspected: its authoritative state is `[_]`, it has
no phase receipt or Lean declaration body, and its dossier is guidance only rather than accepted
scope.

The required negative roles now exist as `statement.json`, `Statement.lean`, the source crosswalk,
and exactly one `stage1-node-receipt/1.0` statement receipt. The target-owned validator emits one
`stage1-validator-semantic-result/1.0` object with `phase_accepted=false`. That validates only the
truth of this blocker; the contract says classified negative findings cannot complete the positive
statement deliverable.

## First failed gate

The authoritative source record identifies only "local Langlands correspondence" and gives the
claim only as "the Langlands correspondence for local fields". It does not select a group, a class
of local fields, a coefficient field, representation and parameter categories, or normalization
conventions. Those choices distinguish materially different theorems. In particular, the source
does not justify silently choosing the intake's proposed characteristic-zero `GL_n` theorem over
local Langlands for another group or over a positive-characteristic formulation.

Even conditional on master acceptance of that proposed scope, the pinned Lean environment has no
concrete types for the required isomorphism classes of irreducible admissible smooth complex
representations of `GL_n(F)` or equivalence classes of Frobenius-semisimple complex Weil-Deligne
representations. It also lacks the local class field theory, twist, contragredient, central
character, local `L`-factor, and epsilon-factor interfaces required by the frozen prose claim.
Consequently there is no source-faithful expression whose binders, hypotheses, conclusion, and
normalizations can be elaborated and fingerprinted.

The historical discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_059.lean` does elaborate, but its
`LocalLanglandsStatementShape` supplies `AutomorphicParameter`, `GaloisParameter`, the defining
predicates, and `Corresponds` as abstract fields. Its `StatementShape` merely asserts nonemptiness
of that user-supplied interface. This does not define either side of the correspondence and can be
inhabited by unrelated proxy data, so it is not the exact theorem and receives no statement
credit. The module itself labels the construction nonterminal.

Under rev-5.6 section 5, both source identity and exact Lean expression are mandatory statement
gates. The ordered binders, expression hash, checked alternate transports, and meaningful mutation
tests therefore cannot truthfully be supplied. The machine state remains `M4`; no `sorry`, axiom,
placeholder predicate, abstract proxy statement, or substituted theorem was introduced.

## Environment fingerprint

Current replay:

- Repository base revision: `94009a6bebd743588e09c3b45bfbf18bf9b5c5e3`; base tree:
  `daabee9f9b2c6e98d84b6290f78a209b950485fc`.
- Validation date: 2026-07-17 (Asia/Shanghai).
- v2 theorem DAG SHA-256:
  `eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153`.
- Dependency-context SHA-256:
  `068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
- Statement-contract SHA-256:
  `1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`.

The following older fingerprint is retained as historical discovery evidence and is superseded for
the current replay wherever its repository base differs:

- Repository base revision: `8bfedc3e8fd013fc57dbc65383ae2896cdda78e5`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Historical discovery module SHA-256:
  `8df3d5f5bb1ee57509be2c352ebc13cab9bffa961809bddee973871372c7faad`.

## Validation evidence

The current replay uses
`LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0431/Statement.lean` from
`Formalizations/Lean`. It elaborates only the concrete local-field, `GL_n`, and ordinary
representation interface probe. The semantic validator is the authoritative worker result for this
packet and reports the positive statement predicate blocked. Exact current commands and exits are
bound in `statement-receipt.json` and `.stage1-worker-selftest.json`.

Historical commands below remain useful discovery context but do not replace the current receipt:

Commands ran from this worker clone using only the existing canonical pinned `.lake` artifacts.
No update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_059.lean` | 0 | Historical abstract interface/discovery module elaborated; it contains no exact terminal target |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'LocalLanglands\|local Langlands\|WeilDeligne\|Weil.Deligne' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No matching declaration or source reference in pinned mathlib; exit 1 means no matches |
| `rg -n -i 'smooth.{0,40}admissible\|admissible.{0,40}smooth' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No matching combined representation-side API in pinned mathlib; exit 1 means no matches |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0431` | 0 | Rank 59, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Retry condition

First obtain an immutable primary-source theorem/page that fixes the exact group, local-field and
coefficient scope, parameter equivalence, and all normalization/compatibility conventions. If it
selects the intake's `GL_n` claim, provide pinned concrete Lean APIs for the smooth admissible
irreducible representation quotient, Weil group and Frobenius-semisimple Weil-Deligne quotient,
and every claimed compatibility law. The next statement run can then elaborate and serialize the
exact expression and mutation-test its rank, characteristic, semisimplicity, and normalization
hypotheses.

Until those conditions are met, statement acceptance and theorem completion are false. A
`.stage1-worker-selftest.json` packet is emitted only to hand off the self-tested negative evidence
with state `[_]`; its semantic result remains blocked and `phase_accepted=false`, so it grants no
statement acceptance.
