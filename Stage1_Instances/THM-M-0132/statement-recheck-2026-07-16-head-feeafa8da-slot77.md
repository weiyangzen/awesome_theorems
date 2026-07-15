# THM-M-0132 statement recheck: blocked

Item: `S56-M-0132-STATEMENT`

Base revision: `feeafa8da0ece8fe2373281ba28fa51c3155ec32` (tree
`5f1a0a2612a8cf94c60e247ae94e80975910bb1a`). Rechecked on 2026-07-16
(`Asia/Shanghai`) in worker slot 77.

## Decision

The exact-statement gate remains blocked. BCDT Theorem A states: "If `E/Q` is an elliptic curve,
then `E` is modular." Printed pages 845-846 define modularity through six equivalent conditions:
equality with an eigenform L-series; the weight-two, level-`N(E)` refinement; modularity of some or
all Tate-module representations; and holomorphic or rational modular parametrizations from
`X_1(N)`.

The pinned Lean closure can express `WeierstrassCurve Rat`, `E.IsElliptic`, analytic cusp forms,
`Gamma0`, `Gamma1`, and q-expansion substrate. It lacks the interfaces required to state any of
those source routes faithfully: an elliptic-curve conductor and L-series, a normalized weight-two
newform or eigenform, the conductor/level relation, the necessary curve/form Galois or Frobenius
compatibility, and modular curves or modular parametrizations. The source defines level using
`Gamma1(N)` and parametrizations using `X_1(N)`; the local probe's `Gamma0` cusp-form shape is only
adjacent infrastructure, with no selected or checked convention transport.

The legacy `AwesomeTheorems.Stage1.S1_M_049.StatementShape` cannot fill the gap. Its witness chooses
an arbitrary positive natural number, arbitrary subgroup, arbitrary cusp form, and three freely
supplied propositions, only the selected one of which needs a proof. This can be populated without
encoding elliptic-curve modularity. Reusing it, introducing an opaque `IsModular` predicate, or
asserting an unrelated cusp form would weaken and substitute BCDT Theorem A. The semistable
Wiles/Taylor-Wiles branch likewise cannot replace the unrestricted root.

Consequently there is no truthful canonical Lean target, target-minimal import set, elaborated
expression hash, canonical-target environment fingerprint, checked alternate transport, or
meaningful removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutation suite.
The first failed statement gate is `exact_source_faithful_modularity_relation_unavailable`.
Lifecycle remains `planned`, debt remains `H1 / M3 / R3`, and the statement node remains `[ ]`.
No proof, receipt, debt change, audit completion, theorem completion, or master acceptance is
claimed. The predecessor intake is only provisional `[_]`, not dependency-accepted `[x]`.

## Source Boundary

The current `/tmp/bcdt.pdf` has SHA-256
`1e34130e55a0ef39d7ef2566cc7d518e2b69048dece36328a0b6530e92044cf2`. It corroborates Theorem A
on printed page 843 and the six-condition definition surface on printed pages 845-846. This is
current-run source evidence only. It is not an admitted immutable H0 packet, complete convention
and errata audit, assumptions-to-node map, or independent acceptance, so source debt stays `H1`.

No substantive target input changed since the integrated slot-74 recheck. Current HEAD integrates
that blocker pair and unrelated evidence or task states. The target manifest, catalog and Stage0
record, legacy Stage1 blueprint, execution skill, guidelines, pre-existing dossier and probe,
legacy Lean module, toolchain, and dependency lock are unchanged. The `THM-M-0132` projections
remain intake `[_]` with one attempt and statement `[ ]` with zero attempts and no children.

## Pinned Lean Boundary

Fresh elaboration of `StatementInfrastructure.lean` emitted the three expected API types, 207
bytes, at SHA-256
`f0c8f435355cda30057d64773163f7294fdb9749f52e99b30d87a33b19042a22`; stderr was empty. The probe
declares no canonical target, checked convention transport, or proof body. It currently has three
direct imports. Deletion checks establish that Weierstrass and `ModularForms.Basic` are needed for
the probe, while explicit `ModularForms.CongruenceSubgroups` is redundant because `Basic` exposes
`Gamma0` transitively. The redundant import is intentionally left untouched so this blocked
handoff contains only fresh collision-free report files. Minimal imports for the unavailable
canonical target remain unassessable.

Fresh elaboration of the legacy module returned exit 0 with empty output. Its two `native_decide`
uses prove planning-list lengths only and receive no target-proof credit. A bounded pinned-source
search returned one line, solely an expository Wiles citation in
`Mathlib/NumberTheory/FLT/Basic.lean`, at SHA-256
`bd7d21b7628a98883926bd705a975b38aafb5d608df1dfb3f2841709a817f2ae`. No relevant Lean declaration
was located. These are boundary checks, not a downstream exhaustive anchor audit.

The replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`), and `flt-regular` revision
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` (tree
`32c9eace926573a9981787ae97643e520353c893`). Both dependency worktrees were clean. The
automation-provided canonical `.lake` symlink was reused read-only. No update, build, clone, fetch,
or other dependency mutation was performed.

## Validation Record

Commands ran from this worker clone unless a working directory is stated.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0132` | 0 | rank 49; planned; legacy slot `S1-M-049`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --branch --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` symlink; base revision and tree match this record |
| scoped comparison from `c4715a2b...` to `HEAD` | 0 | substantive target inputs and target projections are unchanged; the prior recheck is integrated |
| `pdftotext -f 1 -l 4 -layout /tmp/bcdt.pdf -`; `sha256sum /tmp/bcdt.pdf` | 0 | exact Theorem A and definition surface corroborated at the hash above; no H0 acceptance claimed |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0132/StatementInfrastructure.lean` | 0 | current three-direct-import probe elaborated; stdout 3 lines/207 bytes at the hash above; empty stderr; no canonical target or proof body |
| temporary import-deletion elaborations using the pinned Lake environment | expected results | Weierstrass and `Basic` deletions failed; explicit `CongruenceSubgroups` deletion succeeded; no owned source changed |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_049.lean` | 0 | legacy abstract compatibility boundary elaborated with empty stdout and stderr; no exact-target credit applies |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | Lean and Lake versions match the pinned environment above |
| mathlib and `flt-regular` status plus revision/tree checks | 0 | both dependency worktrees were clean at the pinned revisions and trees above |
| bounded exact-topic `rg` over pinned mathlib and `flt-regular` Lean sources | 0 | one expository Wiles citation and no relevant declaration; not a completed anchor audit |
| prohibited-construct scan excluding separately classified `native_decide` planning checks | 1, expected no match | no `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe declaration, or backend replacement occurrence |

The companion JSON is the structured blocker packet. Final JSON parsing, scoped invariants,
whitespace checks, and confirmation that the completion self-test is absent are performed after
this pair is finalized. This is unsigned nonrelease evidence, not a node-specific receipt.

## Retry Condition And Boundary

Retry after the intake is dependency-ordered and master-accepted and source-faithful conductor,
normalized weight-two newform, level-matching, and arithmetic compatibility interfaces are
implemented or pinned. The chosen source-equivalent formulation must include checked `Gamma1` to
`Gamma0` convention and curve-representation transports where applicable. A fresh worker can then
elaborate only the approved universal claim, minimize its imports, fingerprint the expression and
environment, compile every credited transport, and execute all four mutation classes.

This is fresh current-HEAD target-scoped blocker evidence only. It does not satisfy
`S56-M-0132-STATEMENT`, propose worker `[_]`, change scheduler state, or claim an elaborated target,
target-minimal imports, master acceptance, audit completion, or theorem completion. Because the
positive statement deliverable did not pass, `.stage1-worker-selftest.json` is intentionally
absent.
