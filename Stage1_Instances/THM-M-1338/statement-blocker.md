# Exact-statement gate: blocked

Item: `S56-M-1338-STATEMENT`

Theorem: `THM-M-1338`

Base revision: `5a057abd0705ba3f4cadbff1712f2bb7467e6354` (tree
`e6499183859cf75043a1ab13bcce0ca7470a2df6`)

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1338-INTAKE` has only a provisional
worker receipt (`accepted: false`), not master acceptance. Independently, the authoritative
repository record does not identify one binder-complete Bihari-LaSalle proposition that can be
encoded without inventing mathematics. It gives only the name, the attribution Bihari/LaSalle,
the year 1956, and the gloss `非线性Gronwall不等式` ("nonlinear Gronwall inequality"). Stage0
explicitly leaves the precise definitions and assumptions open, and the catalog's `已验证` label
is untrusted under rev-5.6.

The intake authenticates I. Bihari's 1956 paper, *A generalization of a lemma of Bellman and its
application to uniqueness problems of differential equations*, DOI `10.1007/BF02022967`, only at
the bibliographic level. The available publisher response did not supply the article body or exact
generalized-lemma text. Crossref's reference metadata contains isolated notes and formulas, but
not the lemma with its definitions, premises, quantifier scope, conclusion, or proof boundary.
J. LaSalle's 1949 paper is likewise only a bibliographic candidate; the combined catalog name does
not justify conflating the two formulations.

The following proposition-changing choices remain unresolved:

- the exact Bihari or LaSalle result, source edition, page or result locator, and errata;
- interval endpoints, orientation, locality, and the regularity of the unknown function;
- regularity and pointwise or almost-everywhere nonnegativity of the time weight;
- positivity, continuity, monotonicity, and zero behavior of the nonlinear response;
- normalization and domain of the reciprocal-response transform;
- ordinary versus generalized inverse and the finite-range or blow-up cutoff; and
- zero initial value, zero response, empty or reversed intervals, endpoints, and strictness.

A familiar modern integral inequality is not a source-selected root. Choosing it, a differential
version, a uniqueness corollary, linear Gronwall, or Osgood's criterion would broaden or substitute
the theorem. Section 5 of the rev-5.6 blueprint makes statement ambiguity and a missing expression
fingerprint hard blockers. Thus no minimal target imports, canonical expression, checked alternate
transport, or removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations can
be certified. Those mutations are undefined, not passed. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

`IntakeProbe.lean` was re-elaborated with the pinned environment. It imports linear Gronwall and
interval-integral integration-by-parts modules and checks six adjacent APIs. It states no
Bihari-LaSalle target and receives no statement or proof credit. Its imports cannot be called
minimal for a canonical target that has not been selected.

A bounded name search in pinned mathlib found no Bihari, LaSalle, nonlinear Gronwall, or generalized
Gronwall declaration. This is discovery-only feasibility evidence, not the later anchor audit and
not proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `Formalizations/Lean/.lake`
symlink was used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1338` | 0 | rank 949; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all && git rev-parse HEAD && git rev-parse 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository `rg` search for the ID, names, gloss, DOI, and source title | 0 | found only underspecified catalog/Stage0 metadata and the intake's explicit null target; no source-selected proposition |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` and `rev-parse 'HEAD^{tree}'` | 0 each | pinned mathlib revision and tree recorded above; package status was clean |
| `sha256sum` over authority, source, intake, probe, and toolchain inputs | 0 | hashes recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1338/IntakeProbe.lean` | 0 | six adjacent Gronwall and interval-integral APIs elaborated; no target theorem declared |
| pinned-mathlib `rg` name search for Bihari, LaSalle, and nonlinear/generalized Gronwall | 1 | expected no-match result; bounded discovery evidence only |
| `python3 -B Stage1_Instances/THM-M-1338/check_intake.py` (before blocker files) | 0 | planned intake invariants passed with null target, `H1/M4/R4`, and six open tasks |
| prohibited-construct `rg` scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1338/statement-blocker.json` and scoped invariant check | 0 each | blocker identity, null target/imports, four undefined mutations, unchanged vector, false completion flags, and no-self-test boundary agree |
| scoped whitespace checks for both new files and `git diff --check -- Stage1_Instances/THM-M-1338` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

After blocker files are added, the historical `check_intake.py` rejects its now-stale exact
nine-file intake inventory. This statement run does not rewrite the intake checker, receipt,
historical hashes, task DAG, generated blueprint, or authoritative execution DAG to manufacture
agreement.

## Retry Condition And Status Boundary

The integration lane must first accept the intake dependency. Accountable reviewers must then
preserve and hash a lawful immutable primary or authoritative edition, select the exact Bihari or
LaSalle result and variant, transcribe every incorporated definition, binder, premise, conclusion,
range restriction, boundary case, proof boundary, correction, and erratum, and independently
approve the source-to-target crosswalk.

A later statement worker can encode that same claim with real Lean definitions, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
