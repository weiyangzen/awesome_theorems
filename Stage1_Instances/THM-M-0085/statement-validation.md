# THM-M-0085 statement validation

Base revision: `c2687431b1d86bac7bd509c9abbfdc1e763c060c`.

The frozen target selects the creates-`G`-split-coequalizers form of Beck's theorem. For categories
`C` and `D`, functors `F : C ⥤ D` and `G : D ⥤ C`, and a fixed adjunction `adj : F ⊣ G`,
the sole mathematical hypothesis is `Monad.CreatesColimitOfIsSplitPair G`; the conclusion is that
the comparison functor `Monad.comparison adj` is an equivalence. This fixes the comparison functor
of the supplied adjunction and avoids silently conflating the other mathlib criteria.

The direct import is `Mathlib.CategoryTheory.Monad.Monadicity`, the module that declares the
creates-`G`-split predicate. Lean is pinned at 4.29.0 (commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`) and mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The pre-existing canonical `.lake` artifacts were
reused; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0085` | exit 0; rank 140, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0085/Statement.lean` | exit 0; canonical target, checked expansion, mutations, and explicit expression elaborated |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0085/check_statement.py` | exit 0; expression hash `f647a14de2662246e57da67c10b9831370a89ecf919974a096e55fe51b162a2d`; four mutations distinguished |
| `python3 -m json.tool Stage1_Instances/THM-M-0085/statement.json` | exit 0 |
| scoped statement assertions | exit 0; hashes, item identity, import, elaboration state, and four mutations agree |
| `git diff --check -- Stage1_Instances/THM-M-0085 .stage1-worker-selftest.json` | exit 0; no output |

`check_statement.py` separately prints each mutation with the pinned elaborator and compares its
serialized proposition with the canonical one. It rejects removal of the creates hypothesis,
changing its functor from `G` to `F`, moving the adjunction binder beneath the implication, and
excluding the empty-category boundary via `[Nonempty D]`.

This is statement-phase evidence pending master acceptance. It supplies no proof of the target and
does not claim source audit, anchor provenance, obligation closure, audit completion, or theorem
completion.
