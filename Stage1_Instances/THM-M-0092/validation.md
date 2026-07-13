# Intake validation

Base revision: `cea7a197878ce23e819b006b2780b0bb1702fbbe`; base tree:
`079dc70c0b48278054700d1b4d45efee14a3bd04`. Validation date: 2026-07-13
(Asia/Shanghai); exact start and end timestamps are recorded in the provisional receipt.

This validation covers target membership, the planned dossier and open task DAG, catalog-source
provenance, theorem-family and neighbor disambiguation, JSON and scoped invariants, a narrow pinned
Lean substrate probe, bounded repository/mathlib search, prohibited-construct hygiene, and
whitespace. It does not validate a canonical Cartan-Weyl statement or proof because the catalog
does not supply a binder-complete proposition or choose among its classification and representation
readings.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean before and after the
  probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source discovery boundary

The catalog record and its Stage0 projection were inspected at the pinned repository revision. They
identify a classical semisimple-Lie classification/representation topic but no exact theorem.
Immutable Encyclopedia of Mathematics revisions 53489 and 33105 were inspected as secondary leads;
their raw digests are `2ddc65e191216d2e652e17f302bec8253bb4c5396c0133307a504efcace58cbd`
and `d0aabfaeccf32578ae3f38037fa0052f9e2d09c24b49b9ab9ba338fb0611e863`.
Crossref metadata for Weyl's 1925 paper, DOI `10.1007/BF01506234`, had digest
`b68eed7e55be3a3414bcff73d0a36143f0b0d4dfdf77996af494846b695c901b`.
These secondary/metadata records expose materially different classification, complete-reducibility,
and Cartan-Weyl-basis readings, and the 1925 bibliographic date conflicts with the catalog's
unexplained 1913 label.

Bibliographic references embedded in pinned mathlib source were also inspected as locators for
Bourbaki's plates, Humphreys Chapter 11, and Seligman's semisimplicity terminology. No external
source was added, and no complete primary source edition, exact theorem passage, assumption map,
proof boundary, translation/correction record, historical attribution, or independent review was
accepted. Accordingly, those leads support only `H1`, not `H0`.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0092` | 0 | rank 1109; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 677,682 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 30 --retry 2 'https://encyclopediaofmath.org/index.php?title=Lie_algebra,_semi-simple&oldid=53489&action=raw'` | 0 | immutable secondary overview retrieved to `/tmp`; digest `2ddc65e191216d2e652e17f302bec8253bb4c5396c0133307a504efcace58cbd`; no file added or H0 credited |
| `curl -L --fail --max-time 30 --retry 2 'https://encyclopediaofmath.org/index.php?title=Cartan-Weyl_basis&oldid=33105&action=raw'` | 0 | immutable secondary basis entry retrieved to `/tmp`; digest `d0aabfaeccf32578ae3f38037fa0052f9e2d09c24b49b9ab9ba338fb0611e863`; no file added or H0 credited |
| `curl -L --fail --max-time 30 --retry 2 -H 'Accept: application/json' 'https://api.crossref.org/works/10.1007/BF01506234'` | 0 | 1925 Weyl paper metadata retrieved to `/tmp`; digest `b68eed7e55be3a3414bcff73d0a36143f0b0d4dfdf77996af494846b695c901b`; metadata only |
| inspection of bibliography/comments and partial-construction boundaries in pinned mathlib Lie modules | 0 | classical source locators, competing semisimplicity conventions, directional constructions, and explicit TODOs recorded; no source admitted or H0 credited |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above; package status clean |
| `sha256sum` on authoritative manifests, source records, toolchain, lock, and six probed mathlib modules | 0 | hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0092/IntakeProbe.lean)` | 0 | nine adjacent pinned APIs elaborated; complete output SHA-256 recorded in the receipt; no target declaration or proof body |
| bounded case-insensitive exact-topic `rg` search in repo-local Lean and pinned mathlib | 0 | three documentation/context matches for Cartan-Dynkin-Killing classification, but no declaration named for the broad Cartan-Weyl classification/representation target; intake discovery only |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | every structured artifact is valid JSON after finalization |
| `python3 -c` with `ast.parse` on `Stage1_Instances/THM-M-0092/check_intake.py` | 0 | scoped intake validator parsed without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0092/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency hashes, H1/M3/R4 null target, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0092/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| `sha256sum` on the root worker packet and eight non-receipt owned intake files | 0 | raw nonrelease input digests recorded and replay-checked by the receipt; the receipt output is excluded from its own digest map |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no prohibited declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0092 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; per-file no-index checks cover all untracked artifacts |

## Known open gates

Exact source and standard-name selection, algebra/group boundary, field and finite-dimensionality,
semisimplicity encoding, classification data and equivalence, representation conclusion, complete
definition/premise/conclusion/proof-boundary crosswalk, attribution/translation/errata audit,
immutable source admission, and independent review remain open. So do the canonical Lean target and
minimal imports, expression/environment fingerprints, checked transports, four statement mutation
classes, exhaustive anchor audit, discovery protocol, obligation registry, typed graphs, proof and
composition, source/provenance/trust closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These failures prevent statement and theorem progress, but do not invalidate a truthful
self-tested `planned` intake.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0092-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
