# THM-M-0412 exact-statement gate: blocked

Item: `S56-M-0412-STATEMENT`

Base revision: `4d389eb47e043f6f44925a418baee0d034f764ba` (tree
`64faabd76665273032b8cb1554b90655b5c94256`). Attempt date: 2026-07-15
(`Asia/Shanghai`).

## Decision

The exact Lean 4 target cannot be elaborated truthfully from the received source record. The
complete catalog entry supplies only the Chinese label `皮尔斯猜想` (literally "Pierce
conjecture"), attribution to Trygve Nagell, year 1948, and the gloss `某些三次曲线的整数点`
("integer points on certain cubic curves"). It supplies no original-language name, publication,
theorem or page, equation or curve family, parameter and point domains, ordered binders,
hypotheses, conclusion, proof boundary, correction history, or boundary cases. Stage0 explicitly
leaves the exact definitions and premises open.

The repository's intake dossier already freezes this as `unresolved_source_identity` rather than
guessing. The legacy `S1_M_021.lean` module is discovery input only. Its abstract
`NagellLutzBranchData` predicate and its prose correction to the Nagell-Lutz theorem do not encode
an arithmetic curve, and the intake found no primary-source evidence for that correction. Replacing
this target with Nagell-Lutz, the Ramanujan-Nagell equation, the Markov equation, a generic
Siegel-finiteness theorem, or any selected cubic would be a substituted theorem.

A bounded bibliographic check did not resolve the mismatch. OpenAlex's Trygve Nagell author record
lists cubic-related work in 1925, 1929, 1936, 1937, and 1950, but no 1948 item selecting this
catalog claim. Exact English and Chinese web queries returned no pertinent
mathematical identity. These are negative discovery observations, not an assertion that no such
source exists.

Consequently there is no canonical human proposition or Lean expression for which imports can be
certified minimal. There is no expression or environment fingerprint, approved alternate encoding,
or meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation.
Those tests are undefined, not passed. No `Statement.lean`, proxy proposition, theorem declaration,
transport, or proof body was created. The root remains `H5 / M4 / R4`, and the statement item
remains `[ ]`.

## Pinned Lean Boundary

`StatementProbe.lean` uses the single direct import
`Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point` and checks six adjacent interfaces: the
Weierstrass-curve type, discriminant, two-torsion polynomial and its discriminant identity, affine
points, and their commutative-group instance. The probe elaborates in the pinned environment, but it
does not select a curve equation or theorem and cannot establish a minimal import for an absent
target. It receives no statement, anchor-audit, or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-15 (`Asia/Shanghai`). Exact final results
are also serialized in `statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0412` | 0 | rank 21; planned; legacy slot S1-M-021; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 2989,2994 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and `git status --short` | 0 | revision and tree recorded above; package worktree clean |
| initial `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/StatementProbe.lean` | 1 | Lean rejected the first probe because its import followed the module doc comment; stdout SHA-256 `db27c2ef9df86fc6574ccab13c207707974733b6853786699bd9166c9887189b`; the import was moved to the required leading position |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/StatementProbe.lean` | 0 | six adjacent APIs elaborated; no canonical target, transport, or proof body |
| exact-topic searches over repository sources plus OpenAlex and Bing RSS queries | 0 | repository search reproduced only the sparse metadata and rejected legacy correction; bounded public search did not identify a matching source or exact proposition |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| structured blocker JSON parse and invariant check | 0 | item identity, blocked/open state, null target fields, unchanged vector, false completion fields, four undefined mutation classes, and absent worker self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-0412`; per-file no-index checks for new files | 0 | no whitespace diagnostics; no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest is absent as required for a blocked phase |

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve an immutable primary or approved authoritative source,
reconcile the title, author, and date, select and independently approve one exact proposition, and
crosswalk every incorporated definition, ordered binder, hypothesis, conclusion, proof boundary,
correction, and degenerate case. A fresh statement worker can then encode precisely that claim,
minimize its pinned imports, serialize and hash the elaborated expression and environment, compile
every credited transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of this node or a downstream
node. Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt
change, node receipt, worker `[_]`, proof credit, or master acceptance is claimed. Because the
statement deliverable did not pass, no `.stage1-worker-selftest.json` is emitted.
