# S56-M-1153-STATEMENT blocker

Item: `S56-M-1153-STATEMENT`  
Theorem: `THM-M-1153` (Wiener criterion)  
Base revision: `2ee637ed8d67dca4a6ad2a70053fe8bd6955c5d3`

## Verdict

The exact-statement gate is blocked. No canonical Lean target is claimed, and this worker does not
claim the statement node as self-tested.

The accepted intake deliberately leaves the selected primary-source theorem location and several
statement-changing choices open. In particular, it does not fix:

- the exact edition, theorem/page, wording, and errata for the source theorem;
- whether the domain is bounded and the precise Perron boundary-data and regularity predicates;
- the concrete Newtonian-capacity definition and normalization;
- annular endpoint conventions and geometric scale; or
- the exact normalized series (including its codomain and treatment of empty obstacles).

These choices affect hypotheses and the proposition itself. Selecting them from the theorem name or
from a modern remembered formulation would invent missing mathematics and violate the rev-5.6 exact
statement gate. The retry condition is a source-phase amendment that supplies a stable primary-source
copy and a reviewed row-by-row statement crosswalk resolving every choice above.

## Lean boundary checked

The legacy discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_143.lean` elaborates with its two pinned direct
imports, but it cannot serve as the canonical target. Its `StatementShape` quantifies over
`WienerCriterionData`, whose fields assume an abstract `VariationalCapacityAPI`, an abstract
`DirichletPerronRegularityModel`, and a weak/classical bridge. Thus it states a criterion for
caller-supplied interfaces rather than the intake claim using concrete Newtonian capacity and Perron
regularity. Crediting it would be a broadened/substituted theorem.

No `Statement.lean`, statement fingerprint, checked alternate transport, or statement receipt was
created. No `sorry`, axiom, placeholder theorem, or fake result was introduced.

## Commands and exact results

All commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` using the
pre-existing pinned `.lake` symlink; no dependency update or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1153` | 0 | rank 143; `planned`; `L0 / rework_required`; `theorem_complete: false` |
| `lake env lean AwesomeTheorems/Stage1/S1_M_143.lean` | 0 | no output; the legacy discovery module elaborated |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum AwesomeTheorems/Stage1/S1_M_143.lean lean-toolchain lake-manifest.json` | 0 | `0d9bd4f987d3983504faaa9990beb7187cb2087d593265c7bd5c38c4dbfdca8c`, `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`, `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C .lake/packages/flt-regular rev-parse HEAD` | 0 | `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` |

The first failed gate is rev-5.6 section 5/5.1 exact statement identity. The root vector therefore
remains `[H2, M4, R4]`, and theorem completion remains false.
