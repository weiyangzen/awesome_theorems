# THM-M-0861 obligation-tree validation

Item: `S56-M-0861-OBLIGATION_TREE`

Base revision: `b243ebc0f9058ba5afafef8240b92c2dfb2edc6e`

Base tree: `b4b092069141ac54ea1ab5a6ea946192a30ec78c`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Frozen result

The version-1 registry freezes 54 source-faithful root-relevant obligations. It separates the exact
upper/lower assembly, fixed-`k` Satz C induction, source-shaped small-edge-count base, identity-
preserving edge deletion, missing-color argument, finite maximal alternating trail, bipartition
parity, Kempe swap, lower-bound cardinality route, and all source/provenance/trust/readability/
workflow boundaries. The denominator SHA-256 is
`1272c7806d6c29040abda962a5fd83037c2f57a04631ddd5507b6e84c46af230`.

The seven typed graph families contain 244 edges. Four reverse proof edges typed `composes` form
the kernel-checked upper/lower-to-assembly and transport/assembly-to-root harness. Sixty-one other internal
source-shaped reverse relations are explicitly `logical_decomposition` until later proof work supplies exact composition declarations.
The evidence graph is empty. There are no accepted closed obligations.

## Commands and exact results

The initial worker status contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. Existing canonical pinned artifacts were reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, checkout, network access, or `.lake` mutation
was performed.

| Command | Exit | Exact result and boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0861` | 0 | rank 1415; planned; legacy artifacts unaccepted; theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0861/build_obligation_artifacts.py` | 0 | deterministically wrote 54 obligations and 244 typed edges; denominator `1272c780...f230` |
| `python3 -B Stage1_Instances/THM-M-0861/check_obligation_tree.py` | 0 | regenerated artifacts agreed; schemas, hashes, eligibility, mandatory layers, 54 ledgers, anchors, recipes, graph endpoints/reciprocity/reachability/acyclicity, pins, hygiene, exact Lean composition, receipt, and packet passed; 61 decompositions remain unverified; root H1/M4/R4 |
| `python3 -m json.tool` on the registry, graph bundle, validation specs, receipt, and worker packet | 0 | every structured artifact parsed |
| temporary `Statement.olean` compilation plus `lake env lean` on `ObligationTree.lean`, performed by the checker | 0 | exact `DegreeBound`, bounded Satz C, upper, lower, bundled assembly, expanded assembly, explicit root transport, and combined root declarations elaborated; all five printed composition/transport declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound`; stdout SHA-256 `fc7ec023...f5db` |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0861-obligation-pycache python3 -m py_compile Stage1_Instances/THM-M-0861/build_obligation_artifacts.py Stage1_Instances/THM-M-0861/check_obligation_tree.py` | 0 | builder and checker compiled without owned-path cache output |
| comment-aware prohibited-construct scan over `ObligationTree.lean` | expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `unsafe`, `implemented_by`, `native_decide`, `extern`, or `opaque` declaration/shortcut |
| `git diff --check -- Stage1_Instances/THM-M-0861 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The exact compound finalization commands were:

```bash
for f in Stage1_Instances/THM-M-0861/obligation-registry.json Stage1_Instances/THM-M-0861/typed-graphs.json Stage1_Instances/THM-M-0861/validation-specs.json Stage1_Instances/THM-M-0861/obligation-tree-receipt.json .stage1-worker-selftest.json; do python3 -m json.tool "$f" >/dev/null || exit; done
PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0861-obligation-pycache python3 -m py_compile Stage1_Instances/THM-M-0861/build_obligation_artifacts.py Stage1_Instances/THM-M-0861/check_obligation_tree.py
python3 - <<'PY'
from pathlib import Path
import re
s = Path("Stage1_Instances/THM-M-0861/ObligationTree.lean").read_text()
s = re.sub(r"/-.*?-/", "", s, flags=re.S)
s = re.sub(r"--.*", "", s)
m = re.search(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b", s)
if m:
    raise SystemExit(f"prohibited Lean construct: {m.group(0)}")
print("prohibited Lean construct scan: no matches")
PY
git diff --check -- Stage1_Instances/THM-M-0861 .stage1-worker-selftest.json
```

## Evidence and trust boundary

The Lean harness consumes exact abstract upper and lower propositions and returns the canonical
statement; it proves neither abstract premise. Its classical axiom report comes through the exact
statement transport and is an observation, not accepted transitive trust closure. Pinned mathlib
provides representation and adjacent support only. No exact terminal proof body was found, no
proof-body location is credited, and no graph node is promoted to M0.

The worker receipt is non-content-addressed dirty-worker evidence pending dependency-ordered master
acceptance. Release-grade source snapshots, patch/untracked digests, full TCB/SBOM, cold offline
replay, second runner, and independent verifier belong to later gates.

## Status boundary

This phase self-tests the obligation registry and typed architecture only. The minimal open machine
proof cut is `M0861-T-UPPER` plus `M0861-T-LOWER`. Primary-source H0 and independent review,
readable R0 and independent review, internal composition, transitive provenance/trust, hermetic and
independent validation, `AUDIT-Z`, `THEOREM-Z`, and master acceptance remain open. The accepted root
stays `[H1, M4, R4]`; `audit_complete=false` and `theorem_complete=false`.
