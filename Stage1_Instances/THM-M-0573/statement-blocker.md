# Exact-statement gate: blocked

Item: `S56-M-0573-STATEMENT`  
Theorem: `THM-M-0573`  
Base revision: `8267bd5da13d65cb188fb02dc0d206996f85df2d`

## Decision

No exact Lean 4 target can yet be truthfully elaborated. The authoritative repository wording is
only `G-指标定理` ("G-index theorem") with the gloss `等变椭圆算子的指标` ("the index of
equivariant elliptic operators"). The accepted intake deliberately leaves the canonical target
blocked because this wording does not select one proposition. It could denote:

- equality of analytic and topological equivariant indices in `R(G)`;
- equality of their characters at every `g : G`; or
- a fixed-point formula for a character value.

Those formulations have different conclusions and require different data. The source record also
does not freeze the category of `G`, the smooth action and compact-manifold boundary convention,
the operator class, the complex bundle and symbol models, the representation-ring construction,
or the equivariant K-theory pushforward. Selecting any of these choices here would invent missing
mathematics or substitute a special case, contrary to sections 5 and 5.1 of the rev-5.6 standard.

The two intake citations remain discovery candidates rather than a selected statement. The
repository record provides no theorem number or page range within Atiyah--Segal, *The Index of
Elliptic Operators: II*, or Atiyah--Singer, *The Index of Elliptic Operators: III*, and no inspected
wording or errata disposition. The current metadata's two-person attribution is itself
insufficient to decide whether Part II or Part III supplies the intended result.

## Lean boundary

Pinned mathlib was searched for terminal equivariant-index and equivariant-elliptic APIs. The only
match for the scoped query was an unrelated explanatory use of "equivariant" in the group-action
API. Consequently there is no concrete pinned substrate in which to encode the analytic index,
topological equivariant index, and their equality without defining major missing mathematics.

The legacy `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_108.lean` is for the distinct
Atiyah--Bott target `THM-M-0576`. Its operator, ellipticity predicate, index character, fixed
components, and local contributions are unconstrained structure fields. Reusing that abstract
interface would assume the semantic content that this target must state and would not supply a
source-to-Lean crosswalk. It therefore receives no statement credit.

There is no applicable `lake env lean <target>.lean` check: the canonical expression does not
exist. Creating an abstract record with the desired equality as a field merely to obtain a green
elaboration would be fake evidence. Minimal imports, normalized expression serialization, checked
alternate transports, and the required removed-hypothesis, changed-domain, changed-scope, and
boundary mutations all depend on first identifying that expression.

The canonical formal target therefore remains absent and machine debt remains `M4`. No theorem,
axiom, placeholder, broadened target, special-case substitute, statement acceptance, audit
completion, or theorem completion is claimed. Because the assigned phase did not pass its gate,
no `.stage1-worker-selftest.json` is emitted.

## Narrow validation evidence

Commands ran in the worker clone on 2026-07-12. The pre-existing untracked
`Formalizations/Lean/.lake` artifact was read only. No update, build, clone, fetch, or other
dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0573` | 0 | rank 619, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | SHA-256 `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -ni 'equivariant.{0,40}(index\|elliptic)\|(index\|elliptic).{0,40}equivariant\|EquivariantK\|RepresentationRing\|Grothendieck.*representation' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | one unrelated group-action comment; no terminal theorem or required concrete index API |

## Retry condition

An accountable source reviewer must select an immutable primary-source edition and exact
theorem/page, record its complete wording and errata status, and freeze the group, manifold,
action, bundle, operator, symbol, K-theory, representation, and normalization conventions. The
review must explicitly decide whether the root is the representation-ring equality, its
character-valued consequence, or a fixed-point formula. A later statement run can then implement
the required concrete definitions (or use audited pinned ones), elaborate the exact target, find
the minimal imports, serialize its expression and environment, and execute the four mutation
classes.
