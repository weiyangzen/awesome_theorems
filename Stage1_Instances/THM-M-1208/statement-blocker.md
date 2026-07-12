# Statement-phase blocker

Item: `S56-M-1208-STATEMENT`  
Base revision: `446f3e80e7a93deeca70150fa80d9ee079ee0586`

## Verdict

The exact Lean 4 target cannot be elaborated without inventing a theorem that is absent from the
repository source record. This statement node remains blocked and no provisional completion or
machine-proof credit is claimed.

The only literal claims available for this ID are "spacetime estimates for solutions of dispersive
equations" and "spacetime estimates for dispersive equations". They do not determine any of the
following statement-critical fields:

- the dispersive equation or propagator;
- the spatial domain and dimension;
- homogeneous, dual, or inhomogeneous form;
- admissible exponents, endpoint policy, and mixed-norm order;
- data and solution spaces, regularity or derivative loss;
- time interval, constant dependencies, and boundary cases.

These omissions are semantic, not merely missing Lean syntax. For example, choosing a free wave
estimate, a free Schrodinger estimate, or an abstract energy-plus-decay estimate would yield
inequivalent propositions. The last choice would also risk substituting the separately scheduled
Keel-Tao endpoint target `THM-M-1209`. The repository additionally contains `THM-M-0381` with the
same title, attribution, year, and nearly identical wording, but supplies no scope rule that
distinguishes the two IDs. Consequently there is no source-faithful basis for choosing one target.

Under sections 5 and 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md`, the missing canonical human claim
also prevents a declaration/expression, ordered binders, minimal imports, normalized expression
hash, environment fingerprint, alternate-form wrappers, and semantic mutation tests from being
truthfully produced. Running Lean on a made-up surrogate would not validate this node.

## Smallest real validation

Run from the repository root on 2026-07-12 (Asia/Shanghai):

| Command | Exact result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | exit 0; `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1208` | exit 0; rank 401, `L0`, `rework_required: true`, lifecycle `planned`, `theorem_complete: false` |
| `rg -ni "Strichartz|spacetime estimates for (solutions of )?dispersive" . --glob '!Formalizations/Lean/.lake/**' --glob '!Stage1_Instances/THM-M-1208/**'` | exit 0; found the two metadata records, duplicate `THM-M-0381`, neighboring `THM-M-1209`, and incidental/interface references, but no exact THM-M-1208 theorem declaration |
| `test ! -e .stage1-worker-selftest.json` | exit 0; no worker self-test manifest exists |

The pinned dependency directory was only inspected; no `lake update`, build, clone, fetch, or
`.lake` mutation was performed. `lake env lean` was intentionally not run because there is no exact
source-derived proposition to elaborate. This is the first failed gate, rather than a missing Lean
artifact.

## Unblocking condition

An accountable scope/source decision must identify a pinpoint primary-source theorem (edition or
stable revision, theorem/page/equation locator, and errata status), explain its distinction from
`THM-M-0381` and `THM-M-1209`, and freeze every field listed above. Only then can this phase encode
that exact claim, determine minimal pinned imports, elaborate it with `lake env lean`, fingerprint
the expression/environment, and execute the required four classes of mutation test.

Known failures: exact human statement, Lean elaboration, expression/environment fingerprints,
alternate-form checks, and statement mutation tests are all unavailable. Root vector remains
`[H4, M4, R4]`; audit completion and theorem completion remain false.
