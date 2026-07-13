# THM-M-1133 proof-phase validation

Item: `S56-M-1133-PROOF`

Base revision: `0afbf514f9bd5f339943542106f6b811869fe572`

Attempt date: 2026-07-14 (Asia/Shanghai)

## Result

`Proof.lean` closes the exact frozen Lean root without an admission, custom axiom, unsafe
declaration, oracle, or substituted theorem. The proof implements the frozen architecture:

- a compact-cylinder maximizer and the boundary/spatial/time location split;
- nonpositive diagonal second Frechet derivatives and coordinate Laplacian at an interior
  spatial maximum;
- zero interior-time derivative or nonnegative terminal-time derivative;
- contradiction for a strict classical subsolution;
- the perturbation `u(x,t) - epsilon*t` and an epsilon estimate on a compact parabolic boundary;
- exact composition through `root_of_subsolutionMaximumPrinciple`.

The narrow checker compiles `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` as distinct
modules in a temporary output directory using the canonical pinned Lake environment. All eight
material proof declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`.

## Commands

| Command | Exit | Result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-1133/check_proof.sh` | 0 | Exact three-module elaboration passed; eight axiom reports matched; exact root kernel-closed. |
| `python3 Stage1_Instances/THM-M-1133/check_obligation_tree.py` | 0 | Frozen 16-node, 37-edge denominator and pre-proof conditional composition still passed; its intentionally frozen closure message remains the obligation-tree-phase snapshot. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 structural standard passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 ordered targets passed. |
| `python3 scripts/stage1_target.py show THM-M-1133` | 0 | Rank 338; accepted lifecycle remains planned and theorem-complete remains false. |
| `rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|^[[:space:]]*(?:unsafe|opaque)[[:space:]]' Stage1_Instances/THM-M-1133 --glob '*.lean'` | 1 | Expected no-match result. |
| `git diff --check -- Stage1_Instances/THM-M-1133` | 0 | No scoped whitespace diagnostics. |

No `lake update`, `lake build`, dependency fetch/clone, or `.lake` mutation was performed. The
worker proof state is only a provisional `[_]` proposal. The accepted root remains unchanged until
master acceptance, and theorem completion remains false because the later validation, source,
readability, provenance, hermetic, and independent release gates are outside this proof item.
