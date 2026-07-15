# THM-M-0072 proof validation

Item: `S56-M-0072-PROOF`

## Result

`Proof.lean` implements the exact outside-maximal branch and closes
`Stage1Instances.THM_M_0072.ThompsonTransferLemmaTarget` through the frozen
`ObligationTree.root_of_outsideTransfer` composition. The proof follows Thompson's printed route:
a maximal subgroup of the Sylow 2-subgroup is normal of index two; transfer to its quotient is
trivial because a nontrivial transfer would have an index-two kernel; the transfer orbit product
is nevertheless the nonidentity quotient element because the Sylow index is odd.

Both terminal declarations elaborate at `--trust=0 -t0`, are sorry-free, and report only
`propext`, `Classical.choice`, and `Quot.sound`. This supports a provisional `M0-L` proposal.
Accepted state remains `H1/M3/R4` until the integration lane accepts this node. Source H0,
independently reviewed readable R0, validation, release, AUDIT-Z, and THEOREM-Z remain open.

## Validation

| Command | Exit | Exact result and boundary |
|---|---:|---|
| `python3 -B Stage1_Instances/THM-M-0072/check_proof.py` | 0 | frozen inputs and pins matched; fresh temporary `Statement`, `ObligationTree`, `Proof`, and exact-type probe elaborated with `--trust=0 -t0`; both terminals were sorry-free and had only the allowed axioms |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0072-proof-pycache python3 -m py_compile Stage1_Instances/THM-M-0072/check_proof.py` | 0 | checker compiled without repository cache output |
| `python3 -m json.tool Stage1_Instances/THM-M-0072/proof-receipt.json` | 0 | provisional receipt parsed |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | worker packet parsed |
| prohibited-construct scan in `check_proof.py` | 0 | no `sorry`, `admit`, `sorryAx`, axiom/bodyless/opaque/unsafe declaration, external implementation, native shortcut, or tactic-time code execution in the three replayed Lean modules |
| `git diff --check -- Stage1_Instances/THM-M-0072 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

The checker obtains the pinned Lean executable and `LEAN_PATH` through `lake env`, copies all three
target modules into a fresh temporary directory, creates temporary `.olean` files in dependency
order, and then compiles a separate exact-type, `assert_no_sorry`, `#print sorries`, and
`#print axioms` probe. It neither writes to nor updates `.lake`.

## Known failures

The predecessor's generated graph bundle is deliberately a frozen pre-proof snapshot. Its
generator/checker now also observes unrelated authoritative execution-DAG drift and therefore is
not replayed as proof evidence. The proof checker instead hashes those frozen inputs and performs
an independent Lean replay. The shared automation-provided `.lake` symlink also makes this a warm,
nonrelease run. All master-acceptance, source/readability, validation, hermetic, independent, and
release gates remain outside this proof node.
