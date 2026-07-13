# THM-M-0034 anchor-audit validation

Item: `S56-M-0034-ANCHOR_AUDIT`

Base revision: `75ab5edd624df749325d391b41b669f8d72774b2`

Base tree: `26562e2b8168d91a92a8164c9d8f0fc55178836e`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

The bounded immutable inventory is fully classified. The pinned Lean probe verifies the exact
target context reaches flatness but not freeness, checks the external PID-statement specialization,
and reports only `propext`, `Classical.choice`, and `Quot.sound` for its checked declarations. The
best exact source candidate matches the field target and current environment, but its prose build
ledger lacks raw kernel evidence and therefore remains `E3/M3`. The older stronger PID candidate has
an immutable successful CI build and supports provisional `E2/M1`, but uses incompatible pins. Both
remain outside the local dependency/kernel closure and lack usable license artifacts. The proposed
candidate vector is `[H1, M1, R4]`; the accepted vector stays `[H1, M3, R4]`. Audit and theorem
completion are false.

All local Lean work used the automation-provided `.lake` symlink read-only. No `lake update`,
`lake build`, dependency clone/fetch/checkout, or `.lake` mutation ran. External source was inspected
through immutable HTTP archives and API/search responses; nothing was installed.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0034` | 0 | rank 1078, planned, L0/rework-required, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight contained only the automation-provided untracked `.lake` symlink; preserved read-only |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | revision `8a178386...ea95`, tree `bdc39a...5c2b`, clean |
| `git -C .../mathlib grep -n -i -E 'quillen.?suslin|suslin.?quillen|serre.?s conjecture|serre conjecture|projective modules? over (a )?polynomial ring|projective module.*polynomial.*free' HEAD -- 'Mathlib/**/*.lean'` | 1 (expected) | no exact alias/phrase hit across 7,871 tracked mathlib Lean files |
| structural `git grep` for `MvPolynomial` with `Module.Projective` or `Module.Free` | 0 | six hits, all specific free objects; no arbitrary finite-projective-to-free theorem |
| scoped `rg` over repo-local Lean and every non-mathlib materialized package | 1 aggregate, except one neighboring prose hit | no repo-local proof body or other pinned-package candidate |
| immutable `git grep` over stored mathlib `master` and seven topic-named refs | 1 for every ref | no target hit; refs were inspected without checkout/fetch and receive no dependency credit |
| Sourcegraph seven-query alias/API ledger | HTTP 200 | six zero results and one two-match Atlas name collision; complete response hashes recorded |
| GitHub REST repository searches | HTTP 200 | found two topic repositories; other searches zero; response hashes recorded |
| GitHub REST code search | HTTP 401, later 403 | access failure/rate limit recorded; no negative result claimed |
| immutable formal-conjectures tree search at `b2e608f...` | 0 | two scoped searches produced no candidate; response hash recorded |
| immutable archive inspection of `edmund-ukaisi/QuillenSuslin@e8d85a6...` | 0 | exact statement/body chain, matching manifest/toolchain, 76-file source boundary, and upstream audit ledger fingerprinted; no license file found |
| `cd` extracted C02 `lean` directory and `python3 scripts/sorries` | 0 | `0 sorry, 0 #exit, 0 native_decide, 0 axiom` |
| immutable archive/CI inspection of `mbkybky/QuillenSuslin@51ed173...` | 0 | stronger PID theorem and successful upstream CI found; incompatible pins and missing referenced license recorded |
| `lake env lean ../../Stage1_Instances/THM-M-0034/Statement.lean` from `Formalizations/Lean` | 0 | exact statement prerequisite re-elaborated |
| `python3 -B Stage1_Instances/THM-M-0034/check_statement.py` | 1 | prior-phase validator rejected its stale frozen blueprint fingerprint; direct statement elaboration and this audit checker instead bind the current exact statement/source hashes; no statement acceptance is claimed |
| `python3 -B Stage1_Instances/THM-M-0034/check_intake.py --worker-packet .stage1-worker-selftest.json` | 1 | prior intake-only validator expected an intake packet and old open intake cursor, so it is inapplicable to this anchor packet; no intake receipt is reissued |
| `lake env lean ../../Stage1_Instances/THM-M-0034/AnchorAudit.lean` from `Formalizations/Lean` | 0 | pinned candidates, flat/not-free boundary, exact field and stronger PID statement transports, axioms, and exact target checked; stdout SHA-256 `4e496fba...a6f3` |
| `python3 -B Stage1_Instances/THM-M-0034/check_anchor_audit.py` | 0 | authority, pins, hashes, inventory, classifications, packet, and narrow Lean replay agreed |
| `python3 -m json.tool` separately over the four owned/root JSON artifacts | 0 each | structured artifacts parsed |
| scoped prohibited-construct scan of `AnchorAudit.lean` | 1 (expected) | no live proof escape, custom axiom, unsafe/opaque body, TODO, or FIXME |
| `git diff --check -- Stage1_Instances/THM-M-0034 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Known limitations

The exact external theorem was not imported or checked locally and its prose upstream build ledger
does not meet E2, so it is classified `M3`. The provisional `M1` route comes only from the older PID
candidate's immutable successful CI, with an explicit toolchain compatibility blocker. License
permission and full transitive
provenance/trust closure remain open. Search coverage is bounded, the statement prerequisite and
this node await master acceptance, and neither `AUDIT-Z` nor theorem completion is claimed. The
legacy intake/statement checkers retain fingerprints and cursor assumptions from their own earlier
worker runs; their failures above do not supply this phase evidence and require later reconciliation
by their owners rather than cross-phase edits here.
