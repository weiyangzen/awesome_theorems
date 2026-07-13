# Intake validation

Base revision: `9c75282d42a7ef447d885d1d56997a79418bcd8a`; base tree:
`cc5285432a02107fadffb68c698690d1b98ac5f2`. Validation date: 2026-07-13
(Asia/Shanghai); exact timestamps are recorded in the provisional receipt.

This validation covers target membership, the planned dossier and open task DAG, the three
repository-source records and Stage0 boundary, bibliographic identity, variant discrimination, JSON
and scoped invariants, a narrow pinned Lean substrate probe, bounded repository/mathlib discovery,
prohibited-construct hygiene, and whitespace. It does not validate a canonical McDiarmid statement
or proof because the catalog supplies no exact proposition.

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
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source discovery boundary

All three identical catalog records originate at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; none cites a source or states a formula. Crossref and
Cambridge metadata identify McDiarmid's 1989 chapter, pages 148-188, DOI
`10.1017/CBO9781107359949.008`. No full source was added, no exact theorem or proof passage was
accepted, and no independent review occurred. The bibliographic lead supports `H1`, not `H0`.

A bounded search found adjacent Hoeffding/Azuma infrastructure but no usable exact McDiarmid
declaration. The historical repo-local Hoeffding wrapper explicitly excludes a McDiarmid theorem.
This supports the provisional `M4` boundary but is not an exhaustive anchor audit or an absence
proof.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0976` | 0 | rank 1510; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame` on the three catalog records | 0 | all 18 uncited lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref and Cambridge Core metadata inspection | 0 | chapter title, author, year, pages, publisher, DOI, and ISBNs confirmed; no exact theorem admitted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above; package status clean |
| `sha256sum` on manifests, source records, toolchain, lock, probed mathlib modules, and neighboring Hoeffding wrapper | 0 | hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0976/IntakeProbe.lean)` | 0 | eight adjacent APIs elaborated; adjacent Hoeffding-sum axiom report was `propext`, `Classical.choice`, `Quot.sound`; output SHA-256 `bb6bde64a3e5db9190f8d848ba06ea051dc5161cca547de88a9d06e5f3136874`; no target declaration or proof body |
| bounded exact-topic `rg` search in repo-local Lean and pinned mathlib | 0 with unrelated matches | no usable exact McDiarmid target found; discovery only |
| `python3 -m json.tool` on the three owned JSON records and `.stage1-worker-selftest.json` | 0 | every structured artifact parsed after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0976-pycache python3 -m py_compile Stage1_Instances/THM-M-0976/check_intake.py` | 0 | scoped validator compiled without generated owned-path files |
| `python3 -B Stage1_Instances/THM-M-0976/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency hashes, H1/M4/R4 null target, inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0976/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| `sha256sum` on all nine non-receipt changed artifacts | 0 | raw hashes are recorded under `untracked_input_hashes` and replay-checked; the mutable receipt is excluded from its own digest map to avoid self-reference |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 expected | no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0976 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; per-file no-index checks cover untracked artifacts |

## Known open gates

An independently approved immutable source edition and exact result; complete mapping of coordinate
spaces and laws, independence, function and replacement relation, sensitivity bounds, integrability,
centering, event and exponent, ordered binders, proof boundary, corrections, and degenerate cases;
and independent source review remain open. So do the canonical Lean target and minimal imports,
expression/environment fingerprints, checked transports, statement mutations, exhaustive anchor
audit, discovery protocol, obligation registry, typed graphs, proof and composition, trust and
provenance closure, readable reconstruction, hermetic replay, deterministic bundle, independent
verification, master acceptance, audit completion, and theorem completion.

These open gates prevent statement and theorem progress but do not invalidate a truthful,
self-tested `planned` intake.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0976-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
