# THM-M-0123 statement recheck: blocked

Item: `S56-M-0123-STATEMENT`

Base revision: `90a1d52c43113012c8aa0e2b110da02e58ce1724` (tree
`bc399f3ba59411f2a72d4f29d98eb85e7689b28c`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 71.

## Decision

The exact-statement gate remains blocked. The frozen claim quantifies over an
arbitrary number field `K` and a smooth, proper, geometrically connected curve
`X / K` of relative dimension one, assumes `2 <= genus X`, and concludes that
the type of sections `Spec K -> X` is finite.

The pinned Lean closure still has no general genus invariant derived from such
a scheme curve. A bounded search found no `genus`, `arithmeticGenus`, or
`geometricGenus` spelling in the 8374 tracked mathlib Lean sources, and the 32
tracked `flt-regular` Lean sources contain no genus, Mordell, Faltings, or
rational-point-finiteness spelling. The available sheaf-cohomology substrate
does not by itself define the source geometric genus or provide the necessary
comparison theorem.

The legacy
`AwesomeTheorems.Stage1.S1_M_042.CurvePredicateSlots.genusAtLeastTwo`
is an arbitrary `Prop` supplied by the caller, not a fact derived from `X`.
Adding a free natural-number genus field, reusing that proposition, or omitting
the genus hypothesis would substitute or broaden the theorem. The similarly
named `THM-M-0395` dossier also stores unresolved predicate fields and supplies
no checked transport for this target. None receives exact-statement credit.

Consequently there is no honest canonical Lean expression whose direct
imports can be minimized or whose elaborated expression and environment can
be fingerprinted. Checked alternate transports and the removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations remain
undefined, not passed. The first failed gate is
`native_curve_derived_genus_invariant`.

No authoritative target input has resolved this blocker since the integrated
attempt. The target manifest, catalog and Stage0 records, legacy Stage1
blueprint, execution skill, guidelines, intake dossier, legacy Lean module,
statement infrastructure, toolchain, and dependency lock are unchanged. The
rev-5.6 blueprint and execution DAG changed only for unrelated integration
state; the `THM-M-0123` intake remains provisional `[_]` with one attempt and
this statement node remains `[ ]` with zero attempts.

Lifecycle remains `planned`, the root vector remains `H4 / M4 / R4`, and no
proof, receipt, debt change, audit completion, or theorem completion is
claimed. The provisional intake has no master acceptance receipt, which also
prevents statement acceptance.

## Pinned Lean Boundary

`StatementInfrastructure.lean` was replayed with the existing pinned Lake
artifacts. Its four direct imports expose the number-field base scheme,
rational points as sections, smooth relative dimension one, properness, and
geometric connectedness. The file elaborated with empty output and declares no
canonical target, genus proxy, checked genus transport, axiom, or proof body.
Those imports are a boundary-probe basis, not minimal imports for the absent
canonical target.

The legacy `S1_M_042.lean` module also elaborated. Its output confirms the
generic statement shape and its explicit false completion gates, but the
genus slot remains arbitrary and gets no exact-target or proof credit.

The replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`), and `flt-regular` revision
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` (tree
`32c9eace926573a9981787ae97643e520353c893`). Both dependency worktrees were
clean. The automation-provided `Formalizations/Lean/.lake` symlink was reused
read-only. No update, build, clone, fetch, or other dependency mutation was
performed.

## Validation Record

Commands ran from this isolated worker clone unless a working directory is
stated otherwise.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0123` | 0 | rank 42; planned; legacy slot `S1-M-042`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` symlink; base revision and tree match this record |
| explicit `sed` and `find` inspection of the standard, skill, manifest, catalog, Stage0/legacy blueprint records, complete target dossier, infrastructure, blocker, and legacy module | 0 | the frozen scope and exclusions remain unchanged; the integrated blocker remains substantively correct |
| `git diff --quiet b11e1f5a1a404420eee7320a845fdb9df48bec0c..HEAD -- ...` over enumerated authoritative target inputs; target-projection diff piped to an exact `THM-M-0123` search | 0; 1 expected no match | no target-source, intake, legacy Lean, infrastructure, toolchain, or dependency-lock change; no changed `THM-M-0123` blueprint/DAG projection |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0123/StatementInfrastructure.lean` | 0 | empty stdout and stderr; adjacent native substrate elaborated; no canonical target |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_042.lean` | 0 | 71 stdout lines, 5750 bytes, SHA-256 `bc4ccdbace8b25770b16baf75801921b9de2d708b153f820ddd968976b21b289`; empty stderr; arbitrary-genus-slot legacy boundary only |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | Lean and Lake versions match the pinned environment above |
| explicit `git -C ... status --porcelain=v1 --untracked-files=all` and `rev-parse HEAD 'HEAD^{tree}'` for mathlib and `flt-regular` | 0 | both package worktrees clean at the pinned revisions and trees above |
| bounded curve-genus search over pinned mathlib | 1, expected no match | no `genus`, arithmetic-genus, or geometric-genus spelling in 8374 tracked Lean sources |
| bounded genus/Faltings search over pinned `flt-regular` | 1, expected no match | no matching genus or terminal-theorem spelling in 32 tracked Lean sources |
| prohibited-construct scan over owned infrastructure and legacy Lean module | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, or `native_decide` occurrence |
| `python3 -m json.tool` on the recheck JSON | 0 | structured current-HEAD blocker record parsed |
| explicit Python JSON assertions over item/base identity, state/vector, null canonical fields, four mutation values, exact changed paths, and self-test absence | 0 | `statement blocker invariant check: ok` |
| explicit shell wrapper around scoped tracked and per-new-file `git diff --check` | 0 normalized (`tracked=0`, `new_json=1`, `new_markdown=1`) | the wrapper required expected no-index difference exits and empty diagnostic logs |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is absent because the exact-statement gate failed |

## Retry Condition And Boundary

Retry after the intake is master-accepted, accountable reviewers preserve and
approve the exact source statement and modern curve-convention crosswalk, and
the pinned closure gains an audited curve-derived genus invariant with checked
comparison and `g > 1` versus `2 <= g` normalization. A fresh statement worker
can then encode only the same claim, minimize imports, fingerprint the
elaborated expression and environment, compile every credited transport, and
run all four mutation classes.

This is fresh current-HEAD target-scoped blocker evidence only. Because the
positive statement deliverable did not pass, `.stage1-worker-selftest.json` is
intentionally absent and no worker `[_]` or master acceptance is requested.
The stable merge target is `Stage1_Instances/THM-M-0123`; the integration lane
may reconcile this slot-named handoff there rather than retain it as a
long-term public interface.
