# Exact-statement gate: blocked

Item: `S56-M-0208-STATEMENT`

Theorem: `THM-M-0208`

Base revision: `b243ebc0f9058ba5afafef8240b92c2dfb2edc6e` (tree
`b4b092069141ac54ea1ab5a6ea946192a30ec78c`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0208-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt has `accepted: false`, is explicitly
non-content-addressed, and supplies no accepted receipt ID. Rev-5.6 permits dependency-ordered
inspection of provisional work, but master closure remains dependency ordered.

The exact-statement gate also fails independently. The catalog supplies only the name Viviani's
theorem, the attribution and year, and the gloss that for a point inside an equilateral triangle the
sum of the distances to the three sides is constant. It supplies no bibliography, distance
definition, formula, ordered binders, hypotheses, conclusion, proof boundary, correction history,
or reviewer. Its `已验证` label is untrusted metadata.

The intake located Viviani's 1659 primary theorem and proof at Appendix Lemma II Proposition II,
printed pages 146-147. That source is broader: it says the sums of perpendiculars at arbitrary
points inside or on the perimeter of any regular polygon are equal. It does not literally state
the catalog's strict-interior triangle specialization or identify the common value as an altitude.
The familiar altitude formula is derived by specializing to a triangle and comparing with a
boundary point.

No independent review has accepted the working Latin translation, corrections and errata, exact
regular-polygon-to-triangle specialization, or source-to-Lean map. The following
proposition-changing choices also remain open:

- a Euclidean plane or a dimension-independent affine simplex in a larger ambient space;
- strict versus closed simplex interior;
- distance to finite side segments, supporting lines, or opposite-face affine spans;
- nonnegative metric distance, absolute signed distance, or consistently oriented signed distance;
- point-independence, an existential constant, or equality to one selected altitude;
- vertex order, altitude index, reindexing, binder order, typeclass context, and fixed options; and
- side and vertex points, exterior points, repeated or collinear vertices, zero side length,
  orientation reversal, and other boundary cases.

Selecting the convenient candidate

```text
sum i : Fin 3, |t.signedInfDist i p| = t.height 0
```

would therefore insert a domain, side object, distance convention, constant, vertex index, and
boundary policy that the accepted source record has not frozen. Rev-5.6 sections 5 and 5.1 make
this ambiguity and the missing expression fingerprint hard blockers. No `Statement.lean`, exact
Lean target, minimal-import claim, checked transport, or mutation suite was created. The required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. The provisional vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` re-elaborates thirteen pinned interfaces for affine triangles,
equilateral simplices, strict and closed interiors, signed face distance, absolute metric-distance
conversion, and simplex altitude. Its direct imports are:

```lean
import Mathlib.Geometry.Euclidean.Altitude
import Mathlib.Geometry.Euclidean.SignedDist
import Mathlib.Geometry.Euclidean.Simplex
```

`Affine.Simplex.signedInfDist_affineCombination` and
`Affine.Simplex.abs_signedInfDist_eq_dist_of_mem_affineSpan_range` each report only `propext`,
`Classical.choice`, and `Quot.sound`. The deterministic probe output is 3,804 bytes with SHA-256
`8e09f674f02561bfd5bf7071ff8656a48b3beb376788f3b10fda3a461e35b9b9`.

This is real pinned feasibility evidence, but it authenticates interfaces rather than a
source-selected root. In particular, absolute signed distance is to an opposite-face affine span,
not automatically a finite side segment, and `height` selects a vertex while the source-selected
constant remains open. The probe's imports cannot be certified minimal for an absent expression
and receive no statement or proof credit.

A bounded search found no Viviani-named declaration or packaged three-face-distance sum theorem in
repository-local Lean or pinned mathlib. The only broad sum/signed-distance matches were internal
uses in the unrelated incenter module. This is discovery evidence, not the downstream immutable
anchor audit or a global absence theorem.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No update, build, clone, fetch, or other
dependency mutation ran, and the pinned mathlib worktree remained clean.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0208` | 0 | rank 1539; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` before editing | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| blueprint, skill, manifest, DAG, catalog, Stage0, primary excerpt, and complete intake-dossier inspection | 0 | confirmed the broader primary theorem, narrower sparse catalog gloss, open semantic choices, provisional dependency, and null canonical target |
| `sha256sum` over authority, intake, source, toolchain, lock, and pinned mathlib inputs | 0 | exact digests are recorded in `statement-blocker.json` |
| `git blame -L 1499,1504 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib `rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | pinned revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0208/IntakeProbe.lean` | 0 | thirteen interfaces elaborated; two axiom reports contain only the recorded standard foundations; output hash recorded above; no target or proof body |
| bounded exact-topic `rg` over repository-local Lean, pinned mathlib, and Archive | 0 | no packaged Viviani root found; discovery only |
| `python3 -B Stage1_Instances/THM-M-0208/check_intake.py` | 1 | historical checker freezes intake state `[ ]` and attempts 0, while current authority records provisional `[_]` and attempts 1; it was not rewritten or used as statement evidence |

Final scoped checks parse the blocker JSON, assert the blocked-state invariants, scan the owned Lean
probe for prohibited declarations, check whitespace and the exact two-file change scope, and confirm
that `.stage1-worker-selftest.json` is absent.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Independent source and
scope reviewers must then approve the preserved primary transcription and translation, correction
and errata disposition, exact triangle specialization, distance and interior semantics, canonical
constant form, ambient domain, binders, alternate encodings, and every boundary case. A fresh
statement attempt may then encode precisely that claim, minimize pinned imports, serialize and hash
the elaborated expression and environment, compile every credited transport, and execute all four
required mutation classes.

This blocker is the assigned phase's truthful result, not completion. Lifecycle remains `planned`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, proof credit, or master acceptance is claimed.
