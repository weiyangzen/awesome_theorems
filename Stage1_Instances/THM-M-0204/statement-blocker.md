# Exact-statement gate: blocked

Item: `S56-M-0204-STATEMENT`

Theorem: `THM-M-0204`

Base revision: `a1c9974d7fb28cd680e6494b968544bf801a93a2` (tree
`1fa287bc821355aca2ca9e3ce107830a3eb58e64`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0204-INTAKE` is only provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt says `accepted: false`, is not content
addressed, and has no accepted receipt ID. Rev-5.6 permits this dependency-ordered inspection, but
the statement transition cannot be accepted before its prerequisite.

The exact-statement gate also fails independently. The repository supplies only the name
`斯图尔特定理` (Stewart's theorem), Matthew Stewart, the year 1746, and the gloss
`三角形中线长度公式` (triangle median-length formula). It supplies no formula, bibliography,
definitions, ordered binders, hypotheses, conclusion, proof boundary, correction history, or
reviewer. The `已验证` label is untrusted metadata.

The title and gloss select materially different conventional scopes. Stewart's theorem normally
means a general cevian identity. The gloss describes only its midpoint/median specialization,
usually called Apollonius's theorem. The intake therefore correctly leaves the canonical human
statement and Lean target null. Selecting the named general identity would broaden the literal
gloss; selecting the midpoint identity could substitute a specialization for the named theorem.

An accepted source decision must additionally freeze:

- the ordered triangle vertices, chosen base, median or cevian, and mapping of every length;
- internal, endpoint, or external division and ordinary versus directed lengths;
- the Euclidean plane or a more general real inner-product affine torsor and its dimension;
- nondegeneracy, distinctness, and collinearity assumptions;
- squared-distance, solved median-square, or square-root length form and equality orientation; and
- coincident vertices, zero lengths, endpoint division, and every other boundary case.

These choices change the proposition. Rev-5.6 sections 5 and 5.1 make the ambiguity and missing
expression fingerprint hard blockers. There is consequently no honest target whose imports can be
certified minimal. No `Statement.lean`, canonical expression, checked transport, or mutation suite
was created. Removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
are undefined, not passed. The provisional vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` imports:

```lean
import Mathlib.Geometry.Euclidean.Triangle
```

It re-elaborates two pinned candidates:

- `EuclideanGeometry.dist_sq_mul_dist_add_dist_sq_mul_dist`, documented by mathlib as Stewart's
  theorem, states the general ordinary-distance identity for four points under
  `∠ b p c = π`.
- `EuclideanGeometry.dist_sq_add_dist_sq_eq_two_mul_dist_midpoint_sq_add_half_dist_sq`, documented
  as Apollonius's theorem, states an unconditional midpoint squared-distance identity.

Both declarations and four adjacent angle/midpoint interfaces elaborate. Each candidate axiom
report is `[propext, Classical.choice, Quot.sound]`. This is real environment and feasibility
evidence, but it authenticates two alternatives rather than one source-selected root. The module is
a direct candidate import, not a certified minimal import for the absent canonical target, and the
probe receives no statement or proof credit.

A bounded search found these declarations only in the pinned triangle module, its downstream
Ptolemy use, and this intake probe; the other repository hit is the unrelated Gale-Stewart game
target. This is discovery-only evidence, not the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No update, build, clone, fetch, or other
dependency mutation was run, and the pinned mathlib worktree remained clean.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0204` | 0 | rank 1536; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| catalog, Stage0, blueprint, skill, target manifest, DAG, and intake dossier inspection | 0 | confirmed the sparse median gloss, general-versus-specialization conflict, and null canonical target |
| `sha256sum` over authorities, intake artifacts, toolchain, lock, and relevant mathlib sources | 0 | exact digests are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0204/IntakeProbe.lean` | 0 | six APIs elaborated; stdout 2,008 bytes, SHA-256 `6150567743a00bd3a290daa3d3ccdd7e4ad7e325ebd2fda418ac8310c2391e86`; no canonical target or proof body |
| bounded exact-topic `rg` search over pinned mathlib and repository Lean | 0 | only the two pinned candidates, one downstream use, this probe, and an unrelated Gale-Stewart target matched |
| `python3 -B Stage1_Instances/THM-M-0204/check_intake.py` | 1 | historical intake checker requires its old base revision; current HEAD differs, so this worker recorded rather than rewrote stale intake evidence |

Final scoped checks parse and validate the blocker JSON, scan the owned Lean probe for prohibited
declarations, check whitespace, confirm the exact two-file change scope, and confirm that
`.stage1-worker-selftest.json` is absent.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then preserve and hash one lawful immutable primary or authoritative source, reconcile the named
general theorem with the median gloss, and independently approve one exact proposition. The source
crosswalk must freeze every definition, point order, division convention, domain, hypothesis,
conclusion, proof boundary, correction, erratum, alternate encoding, and degenerate case.

A fresh statement attempt may then encode precisely that claim, minimize pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and run all
four required mutation classes.

This blocker is the assigned phase's truthful result, not completion. Lifecycle remains `planned`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, proof credit, or master acceptance is claimed.
