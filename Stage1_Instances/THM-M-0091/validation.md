# Intake validation

Base revision: `b99cf0ffec59c781f8bd25309bdfa53e77372a0a` (tree
`e015394246c3919236f2c6ba1a8184c37130f1e4`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source and non-substitution
boundaries, adjacent pinned interfaces, the open task DAG, scoped intake invariants, and a narrow
Lean API probe. It does not validate a canonical Weyl dimension proposition or proof because
neither is frozen. The automation-provided canonical `.lake` symlink was pre-existing and used
read-only; no dependency update, build, clone, fetch, or other `.lake` mutation was performed. This
dirty worker run is nonrelease evidence.

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
- Root-system base module SHA-256:
  `2d789b8189200f032e3906e738194e3d58efa0a0186dc24bbe72e37758e6b1b5`.
- Lie-weight root-system module SHA-256:
  `1912f5af53a4f749aa6715946c7583045495e8ca45a11953c1ced44ea784d5e8`.
- Character module SHA-256:
  `fba5f95dd3b9346579b3ac042b9d8cb84bc7de8e400e4dc6c17ecf9e3b6a3b77`.
- Lie-group module SHA-256:
  `2ecc19306d5132c15b9bd988324aa6fc4ce39574648d5b6878bef76a1a8162c0`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0091` | exit 0; rank 1108, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink existed before intake |
| `git blame -L 670,675 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded Crossref query for Weyl's representation-theory paper | exit 0; authenticated part I, *Mathematische Zeitschrift* 23(1), 1925, pages 271-309, DOI `10.1007/BF01506234`, plus later part/correction metadata; recorded only as bibliographic leads |
| bounded attempt to retrieve the part-I content link | exit 0 transport; response identified as HTML access page rather than PDF, so no theorem text was inspected or credited |
| bounded repo-local and pinned-mathlib `rg` plus source inspection | exit 0; adjacent root, Lie-weight, representation, character-at-one, and Lie-group interfaces found; no relevant Weyl-dimension declaration or complete bridge found |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0091/IntakeProbe.lean)` | exit 0; twelve adjacent APIs elaborated; five inspected theorem interfaces reported only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem was declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0091-pycache python3 -m py_compile Stage1_Instances/THM-M-0091/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0091/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, H1/M3/R4 planned boundary, null target, source and pin hashes, exact artifact inventory, provisional receipt/packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped `git diff --no-index --check /dev/null <new-file>` loop, followed by `git diff --check -- Stage1_Instances/THM-M-0091 .stage1-worker-selftest.json` | exit 0; every new owned file and the worker packet passed explicit whitespace validation, with no tracked-diff diagnostics |

## Known open gates

A lawful authoritative source edition and exact theorem or formula passage, page, complete
definition and assumption crosswalk, translation/correction/errata audit, modern compact-group
transport, and independent source review remain open. So do the connectedness and reductivity
boundary, representation category, maximal torus and root data, positive roots, dominant highest
weight, Weyl vector, pairing/coroot normalization, product codomain, coercions, denominator proof,
binder order, and boundary cases. Exact target elaboration and mutations, exhaustive anchor and
provenance audits, discovery and obligation freezes, typed graphs, proof and composition, readable
reconstruction, hermetic replay, deterministic evidence bundle, independent verification, master
acceptance, audit completion, and theorem completion also remain open. These open gates do not
invalidate a truthful self-tested `planned` intake.
