# Intake validation

## Scope and environment

Validation was run on 2026-07-13 in an isolated dirty worker clone at base revision
`d750776142c633e42858cebfc67c5c2664d419d7`. The only pre-existing untracked path was the
automation-provided `Formalizations/Lean/.lake` symlink to the canonical pinned Lake artifacts; it
was used read-only. No dependency was updated, fetched, cloned, built, or modified.

The pinned environment was Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`), on x86_64 Linux.

## Commands and results

| Command | Exit | Result and exact boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0017` | 0 | rank 1066, planned, L0/rework required, no accepted legacy artifacts, theorem complete false |
| `git status --short` before edits | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git blame -L 142,147 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error 'https://api.crossref.org/works/10.1515%2Fcrll.1910.137.167'` | 0 | 2265-byte metadata response, SHA-256 `52ba578e58c15b07b6bd61aab46e0b724ef43d2dd3e094ea05ba3d669a453b7b`; confirms Steinitz, title, 1910, issue 137, pages 167-309 only |
| `curl -L --fail --silent --show-error 'https://manifests.sub.uni-goettingen.de/iiif/presentation/PPN243919689_0137/manifest?version=7a696723'` | 0 | 416394-byte IIIF manifest, SHA-256 `ade1f1fd0d4527503c95732422288f34ec99dd14f78f613a52e78b5420c5d351`; maps print pages 261, 286, and 287 to stable canvases |
| `curl -L --fail --silent --show-error 'https://gdz.sub.uni-goettingen.de/fulltext/PPN243919689_0137/00000291.xml'` | 0 | 18983-byte page-287 OCR, SHA-256 `ad1f4f92e22f7ecc6f1e8ca25495f9d8af26cba94f1d6aaa2ea3c151ebfba4c6`; directly locates Satz 9; analogous page-261 and page-286 commands located Satz 2 and Satz 8 |
| immutable nLab revision 31 inspection | 0 | 61494-byte response, SHA-256 `7872a2c7e4fbae7183f0971bc12e7630b58f7366a7050ba3c62e70ee6cc3e98f`; modern classification candidate and proof sketch, secondary only |
| PlanetMath `steinitztheorem` inspection | 0 | 5357-byte response, SHA-256 `353508f5fc370cff0a1e1247b0bb82e575339fc788350a77f2ac30f9a5c24ec3`; identifies algebraic-closure existence namesake, secondary only |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision and tree match the values above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0017/IntakeProbe.lean)` | 0 | thirteen adjacent algebraic-closure, classification, transcendence-basis, cardinality, and primitive-element namesake interfaces elaborated; no theorem was declared |
| bounded `Steinitz`, algebraically-closed classification, and transcendence-degree search in pinned mathlib | 0 | located the classification module and the incompatible primitive-element namesake; discovery snapshot only, not the downstream anchor audit |

The final JSON checks, scoped validator in public and worker-packet modes, prohibited-construct
scan, and whitespace checks are recorded in `intake-receipt.json` after artifact finalization.

## Result boundary

The intake node is self-tested as a `planned` dossier proposal. Its source, scope, namesake, and
formal-candidate boundaries are internally consistent, and the discovery-only Lean probe truly
elaborates in the pinned environment. This does not freeze or prove a canonical proposition. The
first downstream failure is accountable catalog-to-primary-`Satz` selection and independent review,
followed by Lean elaboration, fingerprints, transports, mutations, anchor audit, obligation and
graph freezes, proof, composition, readable reconstruction, hermetic replay, independent
validation, deterministic release evidence, and master acceptance.
