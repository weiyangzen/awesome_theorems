# THM-M-0957 obligation-tree validation

Item: `S56-M-0957-OBLIGATION_TREE`.

Base revision: `dc600635160cace0916df5234bf8808c39dc656d`.

Base tree: `8ee34b31ec38be1ef067aaab38c9a4cb4935b75a`.

Validation date: `2026-07-14` (`Asia/Shanghai`).

## Frozen result

Registry version 1 freezes 45 canonical architecture records with denominator
`84f7eaea7de3659e4324dc64f7849fde4024dd057d4d320c879b0b59dd692a63`. Twenty-eight records are
required machine obligations; the others are explicit statement, imported-body, source, trust,
documentation, or workflow overlays and confer no independent machine proof credit. The bundle has
140 directed edges across separate proof, refinement, provenance, evidence, trust, documentation,
and workflow graphs, 89 architecture ledger steps, and twelve checked conditional composition
certificates. No nonleaf proof decomposition lacks a certificate.

The root proof route uses the exact pinned `Behrend.bound_aux` construction bridge, an inclusive
Roth-number monotonicity adapter, and twelve final open mathematical leaves after recursively
splitting the high-risk proxy, reciprocal, linear, and subleading packages. Their ordered proof
plans are explicitly `unchecked`; the step allocations are not proof or leaf-budget closure. The sphere
and digit-map internals are informational refinements sharing the imported terminal body. The
fixed constant-four theorem is excluded from the root route because it is too weak at the
admissible value `epsilon = 1`.

All Lean validation reused the manifest-pinned, automation-provided canonical `.lake` symlink
read-only. No `lake update`, `lake build`, dependency clone/fetch, checkout, installation, or
`.lake` mutation ran. The evidence is therefore warm and nonrelease.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0957` | 0 | rank 1491; planned; L0/rework-required; theorem incomplete |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree matched the identities above |
| `python3 -B Stage1_Instances/THM-M-0957/build_obligation_artifacts.py` | 0 | wrote 45 architecture records and 140 typed edges; denominator `84f7eaea...d692a63`; repeated generation was byte-identical |
| `LC_ALL=C LANG=C TZ=UTC NO_COLOR=1 lake env lean --trust=0 ../../Stage1_Instances/THM-M-0957/ObligationTree.lean` from `Formalizations/Lean` | 0 | 16 owned declarations reported sorry-free; closure covered 19,495 declarations with only `propext`, `Classical.choice`, and `Quot.sound`, no bodyless nonaxioms, and no unsafe declaration |
| checker-composed `Statement.lean` plus `ObligationTree.lean` under the same pinned Lean command | 0 | 17 declarations reported sorry-free; `Canonical.Root = Stage1Instances.THM_M_0957.BehrendConstructionTarget` checked by `rfl`; combined Lean stdout SHA-256 `9c08c428...e302f` |
| `python3 -B Stage1_Instances/THM-M-0957/check_obligation_tree.py --worker-packet .stage1-worker-selftest.json` | 0 | deterministic generation, registry and instance authority, node ledgers, seven graph types and indexes, reciprocal proof edges, reachability, certificates, pins, composed Lean identity, receipt, packet, open closure, and byte hygiene passed |
| `python3 -m json.tool` on `instance.json`, the three generated JSON artifacts, the receipt, and the worker packet | 0 | every structured artifact parsed successfully |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0957-obligation-pycache python3 -m py_compile Stage1_Instances/THM-M-0957/build_obligation_artifacts.py Stage1_Instances/THM-M-0957/check_obligation_tree.py` | 0 | both Python tools compiled outside the repository tree |
| comment/string-aware prohibited-construct scan of `ObligationTree.lean` | 0 | no placeholder, bodyless declaration, unsafe/opaque construct, oracle, external implementation, or generated proof shortcut |
| `env PYTHONOPTIMIZE=1 python3 -B Stage1_Instances/THM-M-0957/check_obligation_tree.py` | 1 (expected) | fail-closed guard rejected disabled assertions |
| `git diff --check -- Stage1_Instances/THM-M-0957 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence pending dependency-ordered master acceptance. It
freezes the architecture and validates exact conditional interfaces; it does not prove or accept
the twelve final mathematical leaves, install the pinned candidate route, or promote any obligation to M0. The
accepted closure remains empty and the root remains `[H1, M3, R3]`. H0 source admission, R0
independent reconstruction, complete release trust and provenance, cold hermetic replay,
independent verification, `AUDIT-Z`, and theorem completion remain open.
