# THM-M-0420 proof-phase validation

Item: `S56-M-0420-PROOF`. Base revision:
`e888b46b5446c80ddfa863a4f1b7b521141f9b90`.

`Proof.lean` implements frozen obligation `M0420-N1`: finite-prime
unramifiedness in the exact target is equivalent to ramification index one at
every prime above every nonzero finite base prime. The proof uses the pinned
mathlib theorem `Algebra.isUnramifiedAt_iff_of_isDedekindDomain` and the
`Ideal.primesOver`/`Ideal.under` API. Lean reports only `propext`,
`Classical.choice`, and `Quot.sound`; there is no placeholder or added axiom.

This local body does not prove the Hilbert class field theorem. The first
unresolved execution gate is `M0420-X1`: the pinned dependency closure has no
placeholder-free global class-field construction or global Artin reciprocity
theorem. Thus `M0420-C`, `M0420-L1`, `M0420-L2`, `M0420-L3`, and `M0420-L4`
remain the root cut set, the root stays `[H1, M3, R3]`, and
`theorem_complete=false`.

## Validation record

| Command | Result |
|---|---|
| `cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-0420/check_proof.sh` | exit 0; printed the exact normalization theorem and axioms `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0420/check_proof.py` | exit 0; `PASS THM-M-0420 proof phase: M0420-N1 local body checked`; root reported open |
| `python3 Stage1_Instances/THM-M-0420/check_obligation_tree.py` | exit 0; 16 frozen obligations and 54 typed edges; root open |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-0420/{Proof.lean,proof-phase.json,check_proof.py}` | exit 1; expected no matches |
| `git diff --check -- Stage1_Instances/THM-M-0420 .stage1-worker-selftest.json` | exit 0; no output |

The replay reused the clone's existing pinned Lake artifacts. No update, build,
clone, fetch, or dependency mutation was performed. Master acceptance remains
outstanding.
