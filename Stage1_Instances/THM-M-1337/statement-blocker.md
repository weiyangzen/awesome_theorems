# Exact-statement gate: blocked

Item: `S56-M-1337-STATEMENT`

Theorem: `THM-M-1337`

Base revision: `8bbb7ffdbb5e6e8e3e1ffaba9955137f6b68c76c` (tree
`ade61913e5912b1160e25afe096df7f5b3b0cfed`)

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1337-INTAKE` has only provisional
worker evidence (`accepted: false`), not master acceptance. Independently, the authoritative
repository record does not identify one binder-complete proposition that can be encoded without
inventing mathematics. It gives only the name, Thomas Gronwall, the year 1919, and the gloss
`微分不等式的积分形式` ("integral form of a differential inequality"). Stage0 explicitly leaves
the precise definitions and assumptions open, and the catalog's `已验证` label is untrusted under
rev-5.6.

The intake identifies T. H. Gronwall's 1919 article, *Note on the Derivatives with Respect to a
Parameter of the Solutions of a System of Differential Equations*, DOI `10.2307/1967124`, only at
the bibliographic level. Crossref metadata does not supply the article body, exact result, formula,
dependent definitions, premises, conclusion, or proof boundary. The relation between Gronwall's
original differential result and later Gronwall-Bellman integral formulations is therefore not
settled by the received source.

The following proposition-changing choices remain unresolved:

- the exact historical or later source result, edition, page or result locator, and errata;
- scalar ordered codomain versus a norm-valued reduction and all nonnegativity assumptions;
- time domain, base point, interval orientation, endpoint inclusion, and locality or globality;
- continuity, measurability, integrability, absolute continuity, and pointwise or almost-everywhere
  conventions;
- constant versus variable coefficient and its sign and integrability;
- constant initial bound, nondecreasing inhomogeneous term, or additive forcing; and
- the exponential conclusion and equal-endpoint, empty or reversed interval, zero, equality,
  signed, exceptional-set, and nonintegrable boundary cases.

A familiar scalar formula is not a source-selected root. Choosing it, mathlib's derivative or
right-slope theorem, a norm estimate, a discrete version, or an ODE corollary would broaden or
substitute the theorem. Section 5 of the rev-5.6 blueprint makes statement ambiguity and a missing
expression fingerprint hard blockers. Thus no minimal target imports, canonical expression,
checked alternate transport, or removed-hypothesis, changed-domain, changed-binder-scope, and
boundary mutations can be certified. Those mutations are undefined, not passed. The root remains
`[H1, M3, R4]`.

## Pinned Lean Boundary

`IntakeProbe.lean` was re-elaborated with the pinned environment. It imports
`Mathlib.Analysis.ODE.Gronwall` and checks `gronwallBound`, its zero-parameter identities, and the
scalar and norm-valued derivative/right-slope theorems. It states no integral-hypothesis target and
receives no statement or proof credit. Its import cannot be called minimal for a canonical target
that has not been selected.

A bounded source search in pinned mathlib found no Lean line matching Gronwall and integral in
either order. This is discovery-only feasibility evidence, not the later anchor audit and not proof
of global absence.

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
| `python3 scripts/stage1_target.py show THM-M-1337` | 0 | rank 948; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all && git rev-parse HEAD && git rev-parse 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository `rg` search for the ID, name, gloss, DOI, and source title | 0 | found only underspecified catalog/Stage0 metadata and the intake's explicit null target; no source-selected proposition |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` and `rev-parse 'HEAD^{tree}'` | 0 each | pinned mathlib revision and tree recorded above; package status was clean |
| `sha256sum` over authority, source, intake, probe, and toolchain inputs | 0 | hashes recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1337/IntakeProbe.lean` | 0 | five adjacent Gronwall APIs elaborated; no canonical integral target declared |
| pinned-mathlib `rg` source search for Gronwall and integral | 1 | expected no-match result; bounded discovery evidence only |
| `python3 -B Stage1_Instances/THM-M-1337/check_intake.py` (before blocker files) | 0 | planned intake invariants passed with null target, `H1/M3/R4`, and six open tasks |
| prohibited-construct `rg` scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1337/statement-blocker.json` and scoped invariant check | 0 each | blocker identity, null target/imports, four undefined mutations, unchanged vector, false completion flags, and no-self-test boundary agree |
| scoped whitespace checks for both new files and `git diff --check -- Stage1_Instances/THM-M-1337` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

After these blocker files are added, the historical `check_intake.py` rejects its now-stale exact
nine-file intake inventory. This statement run does not rewrite the intake checker, receipt,
historical hashes, task DAG, generated blueprint, or authoritative execution DAG to manufacture
agreement.

## Retry Condition And Status Boundary

The integration lane must first accept the intake dependency. Accountable reviewers must then
preserve and hash a lawful immutable primary or authoritative edition, select the exact Gronwall or
Gronwall-Bellman result and variant, transcribe every incorporated definition, binder, premise,
conclusion, exceptional and boundary case, proof boundary, correction, and erratum, and
independently approve the source-to-target crosswalk.

A later statement worker can encode that same claim with real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
