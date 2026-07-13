# THM-M-0583 proof-phase recheck at base 4e632139

Item: `S56-M-0583-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `4e632139f5060edf088cd107551caac63981263b`

Base tree: `7a87a6b3f6b71cfb0b2d98872327edc8fe8620e6`

## Verdict

`blocked`. No eligible retained Lean 4 proof body was found for the exact
frozen proposition
`Stage1Instances.THM_M_0583.FourDimensionalTopologicalPoincareTarget`.
This recheck adds no proof source and leaves the root vector at
`[H2, M2, R4]`. The proof item remains `[ ]`; the audit, root, and theorem
remain incomplete.

The machine-critical open chain remains:

- `M0583-R-HOMOTOPY-DATA`, extracting the required invariants;
- `M0583-C-TOPOLOGICAL-MODEL`, constructing the surgery model;
- `M0583-L-DISK-EMBEDDING`, the four-dimensional disk-embedding theorem;
- `M0583-L-SURGERY`, topological surgery;
- `M0583-L-S-COBORDISM`, topological s-cobordism;
- `M0583-C-HOMEOMORPHISM`, constructing the final homeomorphism;
- `M0583-X-FREEDMAN-CORE`, composing the complete result.

The local theorem `canonicalRoot_of_freedmanTopologicalCore` checks only an
identity-preserving adapter. `FreedmanTopologicalCore` and `CanonicalRoot` are
definitionally identical, so the adapter consumes the complete theorem as a
premise rather than constructing any of its mathematical content. It earns no
proof-body or root-closure credit.

Pinned mathlib states the generalized topological Poincare result only with
`proof_wanted`. Batteries elaborates such syntax under `withoutModifyingEnv`
and removes the temporary declaration, specifically preventing its use as an
axiom. A trust-zero `#check_failure` probe confirmed that the generalized and
three-dimensional Poincare names are absent after import. A scoped retained-
declaration search found no alternate local or pinned body.

The immutable candidates recorded by the prerequisite audit still provide
only a dimension-zero proof or an explicit `sorry` body for dimension four.
A fresh global Lean source search found no eligible exact proof. The only new
Freedman-shaped candidate was
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`,
`Atlas/GeometryOfManifolds/code/FourManifoldsClassification.lean:47`. Its
`freedman_homeomorphic_of_same_invariants` declaration ends `:= by sorry` at
line 57. It is neither eligible nor in the pinned dependency closure. No
assumption, axiom, placeholder, weaker theorem, or substituted smooth result
was introduced.

## Validation

All commands ran in this worker clone. No `lake update`, `lake build`,
dependency clone/fetch, or `.lake` mutation was performed. The automation-
provided untracked `.lake` symlink was reused read-only, so this is nonrelease
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0583` | 0 | rank 116; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0583/check_obligation_tree.py` | 0 | 16 obligations and 32 typed edges passed; denominator `910aad119639e1751b6f8c0ad6d04f98a030acdc0e00c951cd46f6efff18cccd`; root remains open M2 |
| `python3 Stage1_Instances/THM-M-0583/check_anchor_audit.py` | 0 | pinned mathlib remained source-only; immutable candidates remained dimension-zero-only or `sorry`; root remained M2 |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0583/Statement.lean` | 0 | exact target and checked expansion elaborated |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0583/ObligationTree.lean` | 0 | conditional adapter elaborated; its axiom report was `[propext, Classical.choice, Quot.sound]`; it constructed no terminal core |
| trust-zero `#check_failure` probe for the three Poincare `proof_wanted` names | 0 | all three names were confirmed absent from the imported environment |
| forbidden-construct scan of `Statement.lean`, `AnchorAudit.lean`, and `ObligationTree.lean` | 1 | expected no match for `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, or `external` |
| scoped retained-declaration search | 0 | only statement/interface definitions matched; no terminal proof body was found |
| Sourcegraph exact-name search for `freedman_homeomorphic_of_same_invariants` | 0 | one exhaustive result, with `skipped=[]`, at immutable atlas-lean commit `34ffed396...fb50` |
| immutable raw inspection of atlas-lean `FourManifoldsClassification.lean` | 0 | source SHA-256 `991fbe779b590e4b7d83ac590ccc88a7dae595eae5564c99805fb128c031b01e`; the candidate body is `by sorry` |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0583/check_statement.py` | 128 | its narrow elaboration subchecks ran, then Lake reported that the pinned optional `flt-regular` artifact is absent and could not resolve its `HEAD`; no dependency was fetched |
| `python3 -m json.tool` plus scoped blocker invariant assertions | 0 | fresh blocker JSON is valid; proof/root/theorem remain open; no receipt or self-test was created |
| `git diff --check -- Stage1_Instances/THM-M-0583 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The proof-relevant input hashes were:

```text
Statement.lean              ce7668cd0bd07aaf54ed7d60bb9eb74253b6ab48ab97e38c12d1446d99eec6d8
ObligationTree.lean         c94f747e03bfce01c35a1c3e571230b6c2153bb721701ee85cd36a1100b00076
obligation-registry.json    1db09a273d7c989f950c0c346a6317b84d593f784d4027b82d51a4c0e37c9ef2
typed-graphs.json           69eb81febc06de38ef6eb8ff23ada7ef6a2c3d0192f027bdbcb2601055690bef
anchor-audit.json           0921114daab79180db4817dcf6ab1f6957ac9eede62497e4406b72538f750396
```

The pinned mathlib revision/tree were
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The optional
`flt-regular` package recorded in `lake-manifest.json` is absent from the
canonical artifact tree. That missing artifact affects the statement mutation
checker only after its elaboration passes; it does not provide or conceal a
four-dimensional Poincare proof. Per worker policy it is recorded as a blocker,
not fetched or repaired.

## Retry Condition

Resume only after placeholder-free local implementations of the seven open
machine obligations, or after discovery and approved pinning of a licensed,
immutable Lean 4 proof with a compatible dependency lock and exact checked
transport to the canonical root. The resulting body must pass exact-type,
kernel, axiom, placeholder, provenance, trust, and composition gates. Restore
the already pinned `flt-regular` artifact separately if the full statement
mutation checker must be replayed; do not fetch a moving dependency.

This is an owned blocker artifact, not a proof receipt. It does not satisfy
`S56-M-0583-PROOF`, propose a state change, or support audit or theorem
completion. Because the assigned positive proof phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` remains absent.
