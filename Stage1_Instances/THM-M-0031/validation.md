# THM-M-0031 intake validation

Base revision: `9c75282d42a7ef447d885d1d56997a79418bcd8a`; base tree:
`cc5285432a02107fadffb68c698690d1b98ac5f2`. Validation date: 2026-07-13
(Asia/Shanghai). This evidence covers only the planned intake node.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone/fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned outputs and root worker packet make this dirty nonrelease
evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Exact commands and results

All commands ran at repository root unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0031` | 0 | rank 1515; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 242,247 -- Docs/researches/math_theorems.md` | 0 | all six catalogue fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error https://api.crossref.org/works/10.1090/S0002-9947-1946-0016094-3` | 0 | Cohen 1946 bibliographic metadata retrieved; payload SHA-256 `121788f...bc20`; no theorem passage admitted |
| `curl -L --fail --silent --show-error -I` on the AMS publisher PDF | 22 | HTTP 403; exact primary text remains unavailable and is not represented as inspected |
| `curl -L --fail --silent --show-error https://stacks.math.columbia.edu/tag/0323` | 0 | modern Section 10.160 and tagged Theorem `032A` inspected; mutable HTML SHA-256 `9d6b732c...0e86`; source selection and independent review remain open |
| `(cd Formalizations/Lean && lake --version && lake env lean --version)` | 0 | Lake 5.0.0 and Lean 4.29.0 at the pinned toolchain |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; clean package source |
| `sha256sum` on authorities, repository sources, toolchain, lock, and probed mathlib modules | 0 | hashes recorded in `instance.json` and replay-checked by `check_intake.py` |
| `rg -n -i 'Cohen( \|-\|_)?structure\|complete.*Noetherian.*local.*ring' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/.lake/packages/mathlib/Archive --glob '*.lean'` | 1 | expected no match: no exact-topic Lean declaration in the bounded source search |
| `rg -n -i 'Cohen structure theorem' Formalizations/Lean/.lake/packages/mathlib/docs` | 0 | only `docs/1000.yaml` title `Cohen structure theorem`, with no `decl`; documentation metadata is not a formal candidate |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0031/IntakeProbe.lean)` | 0 | sixteen adjacent local/Noetherian/adic/residue/power-series/characteristic APIs elaborated; both printed theorem reports were `[propext, Classical.choice, Quot.sound]`; no canonical target or proof was added |
| `python3 -m json.tool` on structured owned files and root packet | 0 | valid JSON after finalization |
| Python `ast.parse` on `check_intake.py` | 0 | scoped checker parsed without bytecode output |
| `python3 -B Stage1_Instances/THM-M-0031/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, hashes, H1/M4/R4 null target, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0031/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0031 -g '*.lean'` | 1 | expected no match: the discovery probe contains no prohibited proof escape or declaration |
| per-new-file `git diff --no-index --check /dev/null FILE` plus `git diff --check -- Stage1_Instances/THM-M-0031 .stage1-worker-selftest.json` | 0 aggregate | no whitespace diagnostics; no-index exit 1 meant only that each file is new |

The four probe imports are minimal for the grouped interface families checked here. Removing
the relevant import makes at least one associated local/residue, adic, power-series, or
characteristic interface unavailable. This is an API elaboration check, not the section 5.1 exact
statement gate or its mutation tests.

## Source and statement boundary

The repository supplies only a six-line catalogue record. The primary Cohen publication is a
bibliographic lead whose full text could not be retrieved from the publisher during intake. The
Stacks tagged theorem is an inspected modern formulation lead, but it is not the independently
accepted canonical source. Exact definitions, clauses, assumptions, conclusions, proof-node map,
corrections/errata, and source transport remain open. No H0 is credited.

The pinned probe authenticates adjacent APIs only. No coefficient-ring definition or Cohen
structure declaration was found, and the two checked theorems concern completeness/locality rather
than structural presentation. No expression fingerprint, source identity, proof body, or M0/M3 is
credited.

## Boundary and blocker

Validated scope is limited to the planned dossier, theorem-family and non-substitution boundary,
source-statement crosswalk, source leads, adjacent pinned Lean APIs, and six-node open downstream
task DAG. The first failed dependent gate is `S56-M-0031-STATEMENT`: exact source-statement identity
and Lean encoding are unresolved.

Retry requires an immutable lawful primary or authoritative edition, a pinpoint and independently
reviewed theorem/definition selection, all ordered binders and assumptions, exact output and proof
boundary, corrections/errata, and a decision among coefficient-ring, quotient-presentation, and
regular-local forms. Completeness, Noetherian/finite-generation, coefficient-field/Cohen-ring/
truncated `p`-nilpotent branches, variables, quotient, isomorphism, universes, and degenerate cases
must then be frozen in one exact Lean expression with checked transports and all four mutation
classes.

`STATEMENT`, `ANCHOR_AUDIT`, `OBLIGATION_TREE`, `PROOF`, `VALIDATION`, and `RELEASE` remain open.
The provisional receipt is neither content-addressed nor master-accepted, and no audit-complete or
theorem-complete claim is made.
