# Statement validation record

Item: `S56-M-0002-STATEMENT`  
Base revision: `b84b20757e6df1fd404e2c642bced3de70194984`

## Frozen target

`Stage1Instances.THM_M_0002.FiveLemmaTarget` is the category-theoretic five lemma selected by the
accepted intake scope: a morphism between exact `ComposableArrows C 4` rows in an abelian category,
with epi/iso/iso/mono outer hypotheses, has an isomorphism at component 2. Its sole direct import is
`Mathlib.CategoryTheory.Abelian.DiagramLemmas.Four`.

The checked `Iff.rfl` transport connects the frozen target to a direct expansion of the legacy
`S1_M_097.StatementShape`. This records statement identity only. It neither imports proof credit
from the legacy wrapper nor performs the later terminal-body/provenance audit. The repository's
one-line Chinese gloss has no more precise source hypotheses, so the statement follows the exact
conventional family fixed at intake; pinpoint primary-source fidelity remains open H debt.

## Commands and results

All commands ran in this worker clone on 2026-07-12. Lean ran from `Formalizations/Lean` using the
existing pinned `.lake` artifacts. No update, build, clone, or fetch command was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0002/Statement.lean` | 0 | target, definitional source-shape transport, and four mutation declarations elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0002/check_statement.py` | 0 | expression SHA-256 `1eb7624d3b1cc72251bde5b5b60ecfc85b57324e0866348d91725d74acafb7b6`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0002/Statement.lean lean-toolchain lake-manifest.json` | 0 | `c0da80...c88c`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |

## Scope boundary

The mutation validator rejects removal of lower-row exactness, strengthening either one-sided outer
hypothesis to `IsIso`, and changing the middle conclusion index. No zero-object endpoints,
nontriviality premises, or concrete module specialization are introduced. This is statement-only
evidence pending master acceptance; anchor audit, obligation expansion, proof, release validation,
and theorem completion remain open.
