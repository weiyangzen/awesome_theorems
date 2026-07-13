# THM-M-0914 validation history

Current statement-phase validation is recorded in `statement-validation.md`. The intake record
below is historical discovery evidence and its mutable replay was superseded when the canonical
statement changed the dossier authority.

Validation date: 2026-07-13 (Asia/Shanghai). This is nonrelease evidence from an isolated dirty
worker clone at base commit `db4b8793e70ce8af74c9c9490acfa50aa3684d5e`, tree
`6434a20532ae7c523ad293e67a6228ab384bfb8a`. The initial worktree contained only the
automation-provided untracked `Formalizations/Lean/.lake` symlink. It was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was run.

This validation covers target membership, the planned dossier and open task DAG, literal catalog
provenance, modern-source and formal-candidate discrimination, JSON and scoped invariants, a narrow
pinned Lean API and axiom probe, prohibited-construct hygiene, and whitespace. It does not validate
a canonical `Fin (n + 1) -> Fin n` statement, source transport, proof body, or theorem completion.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status was clean before and after probing.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source discovery boundary

The repository record is uncited and all six lines originate at
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Lehman, Leighton, and Meyer's 2018
*Mathematics for Computer Science*, Section 15.8 and Rule 15.8.1, was inspected from the MIT
course-hosted PDF. It gives both the objects-and-holes slogan and the precise finite-set total-
function collision rule on printed pages 676-677. The 1,048-page PDF had SHA-256
`ea4ced500d4a4bae7beb7a72ae9784abb96ed656ad905976f54c828cf6337dc1`. These external bytes were
used only for dated discovery and were not added as an accepted immutable source. The catalog's
Dirichlet/1834 attribution, the source of record, proof passage, correction history, exact
specialization, and independent review remain open; no H0 credit is claimed. Crossref and public
Springer metadata for Rittaud and Heeffer's 2014 history article were also inspected. Its title
challenges exclusive Dirichlet attribution and its references point to Dirichlet passages from
1842 and 1863. The paywalled article body and those primary passages were not inspected, so this
adds only a provenance warning.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Exit | Result and boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, exactly 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0914` | 0 | rank 1456; planned; no legacy slot; legacy artifacts unaccepted; theorem-complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base commit and tree shown above |
| `git blame -L 6686,6691 -- Docs/researches/math_theorems.md` | 0 | all uncited catalog fields originate at the repository source-record commit |
| bounded download and `pdfinfo`/`pdftotext` inspection of the modern source lead | 0 | exact slogan and Rule 15.8.1 located; PDF identity recorded; discovery only, no source admission |
| Crossref and public Springer metadata inspection for DOI `10.1007/s00283-013-9389-1` | 0 | history citation and its 1842/1863 Dirichlet reference locators recorded; article body inaccessible, provenance warning only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake identities shown above; no build or update |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | recorded pinned revision/tree; clean package source |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 0 | direct finite, strong, infinite, measure, and cardinal pigeonhole surfaces classified; bounded discovery, not an exhaustive external audit |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0914/IntakeProbe.lean)` | 0 | five finite-cardinality/pigeonhole APIs elaborated; axiom output `[propext, Classical.choice, Quot.sound]`; exact output SHA-256 `e891d92bbced439f8e52701c76a5705d9b28eed214cdcdf0124a638ab3fe9370` |
| `python3 -m json.tool` on the instance, open DAG, receipt, and worker packet | 0 | all structured artifacts parse after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0914-pycache python3 -m py_compile Stage1_Instances/THM-M-0914/check_intake.py` | 0 | scoped validator compiled without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0914/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, source and dependency pins, H1/M3/R4 null-target boundary, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0914/check_intake.py` | 0 | public replay mode passed without the scheduler-only packet |
| prohibited Lean construct scan over the owned path | expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the discovery-only probe |
| `git diff --check` plus per-new-file `git diff --no-index --check /dev/null FILE` | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |

## Known open gates at intake time

Master acceptance, an admitted source of record, the historical attribution/date audit, complete
source proof and errata mapping, independent review, concrete-versus-general domain selection,
total-placement definition, ordered binders, collision/fiber choice, and zero-box semantics remain
open. So do the canonical Lean target and minimal imports, expression/environment fingerprints,
checked transports, all four statement mutation classes, exhaustive anchor and terminal-body
provenance audit, discovery and obligation freezes, typed graphs, proof and composition, source/
trust closure, readable reconstruction, hermetic replay, deterministic bundle, and independent
release verification.

## Status boundary

This is historical provisional worker self-test evidence for `S56-M-0914-INTAKE` only. It supported a truthful
`planned` dossier with an H1 source lead and an uncredited M3 formal candidate, not an accepted node
receipt. It is superseded for current dossier replay by `statement-receipt.json`. This intake
snapshot claimed no canonical statement, H0, M0, R0, proof, audit completion, theorem completion,
or master acceptance.
