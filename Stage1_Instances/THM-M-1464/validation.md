# Intake validation

## Scope

This record validates only the `planned` dossier, scope map, source-statement crosswalk, open task
DAG, external-source observation metadata, and discovery-only pinned Lean API probe. It does not
validate an exact mathematical statement, a DG formalization, a proof, an accepted receipt, audit
completion, or theorem completion.

The worker tree was nonrelease-dirty throughout: the canonical `.lake` link was already untracked,
and this intake's owned artifacts plus the root self-test packet were new. No dependency content,
authority file, or other target path was modified.

## Environment

- Repository base: `2d82479e32843fd52283dcd9bb305954729c1199`
- Base tree: `30134b43ab41e973d2558be90371bf18d6edb259`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- Platform: Linux `7.0.0-27-generic`, `x86_64`
- Timezone/date: Asia/Shanghai, 2026-07-13

The external Reed-Hill source was retrieved for intake inspection with a bounded `wget` request to
the OSTI full-text URL. The successful response contained 591,992 bytes, 23 PDF leaves, and SHA-256
`ec04436524f01ad10647398d8d8c81cd21f2b15a69cbcb5d3e9f1f70c22c2d89`.
The source is not vendored; this is nonrelease observation evidence.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1464` | 0 | rank 1141, planned, L0/rework_required, no legacy slot, theorem_complete false |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing untracked canonical `.lake` link; preserved |
| `wget` bounded retrieval of OSTI 4491151 plus `pdfinfo` and `sha256sum` | 0 | complete 591,992-byte, 23-leaf Reed-Hill PDF observed and hashed |
| bounded exact-topic `rg` over pinned mathlib and repo-local Lean | 0/1 by query | no source-selected DG terminal declaration located; adjacent affine-simplex, integration, and Lax-Milgram APIs identified; not an absence proof |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1464/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; three axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem introduced |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=<temporary-cache> python3 -m py_compile Stage1_Instances/THM-M-1464/check_intake.py` | 0 | scoped validator parses without writing cache files under the owned path |
| `python3 -B Stage1_Instances/THM-M-1464/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, null target, H5/M4/R4 boundary, source and pin hashes, receipt/packet agreement, exact inventory, and six open tasks agree |
| prohibited-construct `rg` over `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` token |
| `git diff --check -- Stage1_Instances/THM-M-1464 .stage1-worker-selftest.json` plus per-new-file no-index whitespace checks | 0 | no whitespace diagnostics |

The final structural and whitespace results are recorded after receipt and worker-packet creation.
The Lean probe's exact stdout SHA-256 is
`9d65a47407fb9cafa84aa711ae30a950b617a5ba664f95e94a429c554f5d9e99`.

## Known failures and boundary

Master acceptance is pending. The catalog label still lacks a selected exact proposition. Source
admission, independent source/DG review, formal target and mutation certificate, exhaustive anchor
audit, obligation registry, typed graphs, proof, composition, trust closure, readable
reconstruction, hermetic replay, deterministic bundle, and independent verification remain open.

Verdict: `no_state_change`. This self-tested worker proposal may be handed off as `[_]`; it remains
unfinished and unaccepted. `audit_complete=false` and `theorem_complete=false`.
