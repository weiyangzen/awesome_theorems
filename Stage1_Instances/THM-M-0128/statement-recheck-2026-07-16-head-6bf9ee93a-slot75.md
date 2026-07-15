# THM-M-0128 statement recheck: blocked

Item: `S56-M-0128-STATEMENT`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff` (tree
`24acf86e69ab2e6fca9480c6269b6429874ba295`). Rechecked on 2026-07-16
(`Asia/Shanghai`) in worker slot 75.

## Decision

The exact-statement gate remains blocked. The repository catalog provides only
the name "Shimura reciprocity law", Goro Shimura attribution, the year 1971,
and the gloss "class field theory of CM fields". It does not identify an exact
edition, theorem/page, incorporated definitions, hypotheses, conclusion,
translation, convention crosswalk, corrections, errata disposition, or
independent review.

The provisional intake chooses a CM-special-point family only as prose scope:
an Artin/Galois translate of a CM special point should agree with the translate
induced by the reflex norm. It explicitly leaves unresolved:

- CM field versus CM algebra and the CM-type/reflex construction;
- reflex-norm variance and codomain;
- the idele versus idele-class domain and quotient descent;
- arithmetic versus geometric Artin reciprocity, including inversion;
- canonical model, component, level, special point, and left/right actions;
- equality of points versus equality of orbits or double cosets.

These choices change binders, hypotheses, domains, quotients, variance, and
possibly the direction of the equation. Freezing a schematic Artin/reflex
equation would invent conventions not authorized by a source. Replacing the
missing objects with arbitrary carriers or functions would substitute a generic
action identity. Assuming the desired identity as a proposition-valued field,
as the legacy discovery module does, would be circular.

Consequently there is no honest canonical Lean expression whose target imports
can be minimized or whose expression and environment can be fingerprinted.
Checked transports and the removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined, not passed.
The first failed gate remains
`exact_source_statement_identity_and_convention_selection`.

The predecessor `S56-M-0128-INTAKE` is still provisional `[_]`, without master
acceptance. Lifecycle stays `planned`, the inherited intake vector remains
`H2 / M4 / R4`, and this statement node stays `[ ]`. No statement receipt,
proof, debt change, audit completion, theorem completion, or master acceptance
is claimed.

## V2 Dependency Audit

The new v2 overlay was inspected at graph digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`.
The target context digest is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The node has no direct hard parents, transitive hard ancestors, incoming hard
edges, reuse hints, or shared groups. The required
`dependency-reuse-ledger.json` records that exact empty closure and passed the
repository ledger validator against this base revision.

This does not resolve the statement. The v2 node explicitly classifies the
dependency audit as `unknown_not_independent_proof_claim`; an empty admitted
context is not evidence of mathematical independence and transfers no
statement or proof credit. Its only reusable artifact is the existing substrate
probe, not a Shimura reciprocity declaration.

## Pinned Lean Boundary

`StatementProbe.lean` was replayed with the existing pinned Lake artifacts. Its
two direct imports expose `NumberField.IsCMField` and
`NumberField.AdeleRing`; the replay exited 0 with three stdout lines, 242 bytes,
and SHA-256
`fd1ab2cf001e4eeee420dd3bae8983f412352238a0bb0ccc14af4a3e44cee620`.
They are adjacent object-model anchors only. A bounded declaration-position
search of pinned Mathlib number-theory, algebraic-geometry, and field-theory
sources found no concrete CM-type, reflex-field/reflex-norm, idele-class,
Shimura datum/variety, special-point, or Artin-reciprocity API. This bounded scan
is not the later exhaustive anchor audit.

The legacy module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_046.lean` also replayed with
exit 0 and empty output. Its documentation and fields identify its
CM/Shimura/reflex/reciprocity layer as placeholders, so it receives no
exact-target credit. A prohibited-token scan found no `sorry`, `admit`, axiom,
unsafe, or oracle token in the probe or legacy module; this hygiene fact does
not cure the semantic placeholder boundary.

The environment used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No update, build,
clone, fetch, or dependency mutation was performed.

## Validation Record

The companion JSON preserves exact argv/results and content hashes. The
smallest relevant checks produced these results:

| Check | Exit | Result |
|---|---:|---|
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0128` | 0 | rank 46, planned, legacy unaccepted, theorem incomplete |
| schema-1.1 dependency-ledger validator with exact graph/base arguments | 0 | empty parent/ancestor/edge/hint/group closure accepted |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | all earlier structural assertions passed, then deterministic regeneration failed because the generator inventories the derived ledger |
| from `Formalizations/Lean`, pinned `lake env lean` replay of `StatementProbe.lean` | 0 | two substrate declarations elaborated; no canonical target declared |
| from `Formalizations/Lean`, pinned `lake env lean` replay of `S1_M_046.lean` | 0 | legacy placeholder-bearing discovery module elaborated |
| bounded pinned-Mathlib declaration scan | 1, expected no match | zero output; no root API found in the searched families |
| prohibited-token scan | 1, expected no match | zero output |
| `python3 Docs/tools/check_stage1_standard.py` | 1 | fail-closed at the same derived-ledger deterministic-regeneration mismatch; no pass claimed |

There is a repository-level v2 validator defect worth preserving explicitly:
the generator excludes `dependency-reuse-ledger.json` from shared-identity
discovery but not from `evidence_inventory`, despite the blueprint saying the
derived ledger is excluded from theorem-DAG discovery. Thus an unmodified
deterministic replay after writing the mandatory ledger reports a fresh-graph
mismatch. A read-only in-memory graph comparison confirmed that the added ledger
path in `THM-M-0128.evidence_inventory.structured_json_files` is the only graph
difference. No authoritative generator, graph, blueprint, or scheduler file was
changed by this worker.

## Retry Condition And Boundary

Retry only after the intake is master accepted and accountable reviewers
preserve and approve one immutable primary or authoritative theorem passage
with its incorporated definitions, edition/theorem/page locator, corrections,
errata, translation, hypotheses, and all reciprocity/action conventions. They
must fix the CM datum, reflex construction, idelic domain, Artin normalization,
canonical-model/level data, action variance, conclusion equality, ordered
binders, and boundary cases. The corresponding concrete Lean object model must
then be implemented or imported at immutable pins. A fresh statement worker can
encode only that approved claim, minimize imports, fingerprint its elaborated
expression and environment, compile every credited transport, and execute all
four mutation classes.

This is fresh current-HEAD target-scoped blocker evidence plus an empty audited
dependency ledger. Because the positive statement deliverable did not pass,
`.stage1-worker-selftest.json` is intentionally absent and no worker `[_]` or
master acceptance is requested.
