# Statement validation

Base revision: `9ca62658cb1c22f4da89356b73946aeea3313521`.

The canonical target uses ambient functions restricted to `K`. This avoids falsely giving an
arbitrary convex-set subtype the affine-space structure required by `ContinuousAffineMap`. Affinity
is instead stated exactly on convex combinations of points of `K`; invariance makes both
compositions in the commutation hypothesis meaningful on `K`.

The minimal direct import is `Mathlib.Topology.Algebra.Module.LocallyConvex`. The check reused the
existing pinned `.lake` artifacts and did not update, build, fetch, clone, or mutate dependencies.
The run is scoped worker evidence, not hermetic release evidence.

| Command | Result |
|---|---|
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0321/Statement.lean)` | exit 0; canonical target, checked `EqOn` transport, four structural mutations, and empty-family boundary elaborated |
| `python3 Stage1_Instances/THM-M-0321/check_statement.py` | exit 0; no forbidden proof tokens; four mutation equality probes each failed as required; exact declaration print captured; expression SHA-256 `7a9628fca04eb72d787efad1f852517f4385377b3ad16f3eba662ccea4bb86a5`; Lean `4.29.0`; statement checks passed |
| `python3 -m json.tool Stage1_Instances/THM-M-0321/statement.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0321` | exit 0; no output |

The mutations remove compactness, specialize both domains, move the map family under an
existential binder, and exclude the empty indexing boundary. They are separately named, elaborated
noncanonical propositions and receive no equivalence witness or proof credit. The canonical target
retains all frozen hypotheses and the arbitrary (including empty) family.

Historical theorem/page/errata inspection, anchor discovery, obligations, proof, trust closure,
hermetic replay, and independent review remain downstream. No theorem-completion claim is made.
