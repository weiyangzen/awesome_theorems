# Intake validation

Base revision: `56cce0660d633175f8e66c4a538e5c7dce64652e` (tree
`94920deccabd41cd711821885fe08d62eed67a4e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, open
task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does not validate a
canonical root-space-decomposition proposition or proof because neither has been frozen. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

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

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0095` | 0 | rank 1112, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight contained only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 698,703 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 30 -o /tmp/mit18_745_f20_lec_full.pdf https://ocw.mit.edu/courses/18-745-lie-groups-and-lie-algebras-i-fall-2020/mit18_745_f20_lec_full.pdf` followed by `sha256sum`, `pdftotext -layout`, and bounded `rg` | 0 | inherited assumptions plus Section 19.4, Proposition 19.11 and its proof reference on printed page 103 inspected; PDF digest `908b49bd938da6b28f2bceb01311028c8f453c721af6830ce0e32a1e52b6b929`; H1 lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and scoped package status | 0 | pinned revision and tree recorded above; package worktree clean |
| bounded `rg` inspection of root-space and Cartan-decomposition declarations in repo-local Lean and pinned mathlib | 0 | substantive generalized weight/root-space APIs and stronger `IsKilling` ordinary-root bridges found; no source-selected exact target; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0095/IntakeProbe.lean)` | 0 | nine adjacent pinned ordinary/generalized weight-space, independence, spanning, Cartan, bracket, and Killing APIs elaborated; stdout SHA-256 `1e9dcca24da0029f252fed189c2372a4181e422ea4ce771fd9c49414641c0018`; no target or proof body |
| `python3 -m json.tool` on the three owned JSON files and root worker packet | 0 | all structured artifacts are valid JSON after finalization |
| `python3 -c` with `ast.parse` on `check_intake.py` | 0 | validator parsed without writing generated files into the owned path |
| `python3 -B Stage1_Instances/THM-M-0095/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, pins and hashes, H1/M3/R4 null target, inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0095/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| `rg -n '(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)' Stage1_Instances/THM-M-0095/IntakeProbe.lean` | 1, expected | no prohibited proof escape or declaration |
| per-new-file `git diff --no-index --check /dev/null` plus scoped `git diff --check` | 0 aggregate | no whitespace diagnostics |

## Known open gates

Exact source and clause selection remain open, as do a complete definition, assumption,
conclusion, proof-node, correction, historical-attribution, lawful preservation, and independent
review map. Field, characteristic, finite-dimensionality, splitting, semisimplicity, source and
mathlib Cartan definitions, ordinary versus generalized roots, root index, direct-sum encoding,
companion clauses, and boundary cases are not frozen.

Pinned mathlib provides meaningful M3 infrastructure, but its root spaces are generalized and its
ordinary-root results use a stronger nondegenerate-Killing-form premise. The documented missing
semisimple-to-`IsKilling` converse and the Cartan-definition bridge cannot be bypassed by narrowing
the source theorem. Canonical Lean target, minimal imports, expression and environment fingerprints,
checked transports, statement mutations, exhaustive anchor audit, discovery protocol, obligation
registry, typed graphs, proof and composition, trust and provenance closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion all remain open.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0095-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
