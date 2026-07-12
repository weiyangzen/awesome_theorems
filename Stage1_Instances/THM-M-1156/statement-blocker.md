# Exact-statement gate: blocked

Item: `S56-M-1156-STATEMENT`  
Theorem: `THM-M-1156`  
Base revision: `24c7a19c1a6033b0aed791e0127a3b3e3564a7b0`

## Decision

No exact Lean 4 target can be truthfully elaborated from the repository source record. Its entire
mathematical wording is `Newton位势与对数位势` (Newtonian and logarithmic potentials). This names
two constructions in potential theory, not a proposition, and supplies no pinpoint primary source.
In particular, it does not determine:

- whether the intended root is a definition, a comparison between the two potentials, a
  fundamental-solution identity, a Poisson equation, harmonicity off the support, or a
  representation theorem;
- the ambient dimension and Euclidean space, including whether the logarithmic kernel is confined
  to dimension two and the Newtonian kernel to dimensions at least three;
- the data being integrated (a function, signed measure, or distribution), its scalar field,
  support, measurability, and integrability assumptions;
- kernel constants, signs, Laplacian convention, and behavior at the singularity and at infinity;
- the ordered binders, hypotheses, conclusion, and excluded boundary or degenerate cases.

These choices yield inequivalent propositions. Merely defining one or both potentials would not
turn the topic phrase into a theorem. Choosing a familiar Poisson or harmonicity result would
substitute an invented theorem, and merging this item with the separately scheduled Newton-potential
entry `THM-M-1157` would broaden its identity. The intake therefore correctly leaves
`canonical_statement`, module, declaration, expression hash, and environment fingerprint null.

The first failed gate is canonical human-claim identity under rev-5.6 section 5, before the Lean
statement gate in section 5.1 can run. Without an exact proposition, no import list can be certified
minimal, no expression can be elaborated or fingerprinted, no alternate encoding can be transported,
and removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations have no canonical
baseline. No Lean declaration, axiom, placeholder, abstract assumed interface, weakened special
case, or theorem-completion claim was introduced. Machine status remains `M4`.

## Repository and pinned-environment evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The existing `.lake` link was used
read-only; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1156` | 0 | Rank 359, planned, legacy artifacts unaccepted, theorem incomplete |
| `rg -n -i 'Newton.*potential\|Newtonian potential\|logarithmic potential\|Newton位势\|对数位势\|位势理论\|Potential theory' . --glob '!Formalizations/Lean/.lake/**' --glob '!Stage1_Instances/THM-M-1156/**' --glob '!Docs/Stage1_Blueprint_rev-5.6.md' --glob '!Docs/Stage1_Execution_DAG_rev-5.6.json' --glob '!Docs/Stage1_Targets_rev-5.6.json'` | 0 | Found only the terse Stage0/research wording, the distinct `THM-M-1157` intake, and neighboring potential-theory dossiers; no exact proposition or primary-source pinpoint |
| `rg -n -i 'Newtonian potential\|logarithmic potential\|Newton potential\|potential theory\|fundamental solution.*Laplac' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | No matching declaration or documentation text; exit 1 means no match |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | SHA-256 `651c8acc...b1d2` and `321626c8...2d81` respectively |

There is no applicable `lake env lean <target>.lean` validation because the required exact target
does not exist. Elaborating a hand-selected theorem or an interface that assumes the desired result
would be false statement evidence rather than the assigned deliverable.

After writing the blocker and open task DAG, the following scoped checks all exited 0:

```text
python3 -m json.tool Stage1_Instances/THM-M-1156/task-dag.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-1156/intake.json >/dev/null
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-1156 >/tmp/thm1156-statement-show.json
git diff --check -- Stage1_Instances/THM-M-1156
test ! -e .stage1-worker-selftest.json
```

The first two commands found valid JSON, the standard and target validators returned the results
shown above, the target query returned the same rank and lifecycle, the diff check emitted no
output, and the final command confirmed that no false self-test manifest exists.

## Retry condition

An accountable source review must identify an immutable primary-source edition and exact
theorem/page, resolve errata, and freeze the proposition, dimension, potential definitions, kernel
normalizations, data class, hypotheses, conclusion, and singular/boundary behavior. It must also
state how the claim differs from `THM-M-1157`. A later statement run can then encode that same claim,
minimize its pinned imports, preserve its elaborated expression and environment fingerprint, and
run the four required mutation classes.

The assigned phase is blocked rather than genuinely self-tested, so no
`.stage1-worker-selftest.json` is emitted.
