# THM-M-1356 proof blocker at `a60b47b4` (slot57)

Item: `S56-M-1356-PROOF`

Intent: `prove`

Recorded: `2026-07-15` (`Asia/Shanghai`)

Base revision: `a60b47b4551b044fd5fad26599908ccef4000024`

Base tree: `58186bfbc3502322297e8d601fc091da540ba77b`

## Verdict

`blocked`. No eligible placeholder-free Lean 4 body was implemented or found
for the exact arbitrary-degree root
`Stage1Instances.THM_M_1356.RouthHurwitzTarget`. The proof item remains `[ ]`,
the lifecycle remains `planned`, and the root vector remains `[H1, M3, R4]`.
No frozen obligation, audit endpoint, or theorem endpoint closes.

The existing `Proof.lean` is genuine partial work: it proves the complete
degree-one coefficient adapter, root characterization, Hurwitz-minor formula,
and stability/minor equivalence. Its four declarations replay successfully at
trust level zero and contain no prohibited proof device. But the canonical
root quantifies over every positive degree, so this specialization cannot
satisfy the assigned proof phase or receive root-relevant proof credit.

## Failed Gate

The first failed gate is arbitrary-degree proof-body availability upstream of
both exact directional cut nodes:

- `M1356-B-STABLE-TO-MINORS`
- `M1356-B-MINORS-TO-STABLE`

All 45 machine-required obligations in the frozen 50-obligation registry still
have a null `terminal_proof_body_id`. The conditional declarations in
`ObligationTree.lean` take both complete directions as premises and therefore
prove neither direction. Pinned mathlib and `flt-regular` contain useful
polynomial, complex-root, matrix, and determinant substrate, but the scoped
exact-topic scan found no Routh-Hurwitz, Hermite-Biehler, or Hurwitz-matrix
criterion terminal.

The previously audited near-candidate
`PerAlexandersson/RealRooted@634a949d31683785b4181efbba6faff31e81e006`
does not unblock this item. Its root-critical Hermite-Biehler and Hurwitz
matrix declarations contain explicit `sorry`, and its infinite
total-nonnegativity/right-half-plane formulation is not the frozen finite
strict-minor target.

## Statement Sanity

No definitional contradiction, vacuity, or indexing defect was found. The
frozen entry `a_(2*j+1-i)` is the transpose convention for the usual Hurwitz
matrix; leading principal determinants are unchanged by transpose. Low-degree
expansion agrees with the standard criterion:

- At degree two the matrix is `[[a1, 0], [a0, a2]]`, with minors `a1` and
  `a1*a2`.
- At degree three the matrix is
  `[[a1, a3, 0], [a0, a2, 0], [0, a1, a3]]`, with minors `a1`,
  `a1*a2-a0*a3`, and `a3*(a1*a2-a0*a3)`.

For `(z+1)^2` the minors are `(2, 2)`; for `(z+1)^3` they are `(3, 8, 8)`.
These checks support the frozen convention only. They are not numerical or
finite substitutes for the all-degree theorem.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to the
canonical pinned artifacts was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed. Temporary Lean objects were written under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1356` | 0 | Rank 966; lifecycle `planned`; hard-statement-first-partial-verification lane; theorem incomplete. |
| `python3 -B Stage1_Instances/THM-M-1356/check_statement.py` | 0 | Exact expression SHA-256 `7901eb74...98bf`; all four mutations distinguished; all three direct-import deletions rejected; pinned mathlib revision agreed. |
| `python3 -B Stage1_Instances/THM-M-1356/check_anchor_audit.py` | 0 | Exact local statement only; pinned mathlib topic inventory empty; external candidate inventory empty; root `M3`. |
| `python3 -B Stage1_Instances/THM-M-1356/check_obligation_tree.py` | 1 | The predecessor checker stops at its stale hard-pinned base revision (`431e77db...`) versus current HEAD; this is a freshness failure, not proof evidence. |
| Disposable ordered Lean replay of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` using the executable selected by `lake env`, explicit pinned `LEAN_PATH`, and `--trust=0 -t0` | 0 | All three modules elaborated. All printed local declarations depend exactly on `propext`, `Classical.choice`, and `Quot.sound`; `Proof.olean` SHA-256 is `dbd13ed0...e66cf`; replay-log SHA-256 is `2e2b16af...e59d`. |
| Parser-oriented prohibited-device scan of `Proof.lean` | 0 | No `sorry`, `admit`, `sorryAx`, axiom/constant/opaque/unsafe/extern declaration, `native_decide`, `implemented_by`, or `run_tac` was found outside comments and strings. |
| Exact-topic `rg` over pinned mathlib and `flt-regular` Lean sources | 1 expected | No Routh-Hurwitz, Hermite-Biehler, Hurwitz-matrix, or Hurwitz-determinant proof candidate was found. |
| Frozen registry inspection | 0 | Registry `THM-M-1356-OBLIGATIONS-v1` has 50 obligations, 45 machine-required, and all 45 machine-required terminal body IDs are null. |

The successful replay recipe was:

```bash
tmp=$(mktemp -d /tmp/thm1356-replay.XXXXXX)
cp Stage1_Instances/THM-M-1356/{Statement,ObligationTree,Proof}.lean "$tmp/"
lean=$(cd Formalizations/Lean && lake env which lean)
base_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
for src in Statement ObligationTree Proof; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout 600 \
    "$lean" --trust=0 -t0 --root="$tmp" -o "$tmp/$src.olean" "$tmp/$src.lean"
done
```

## Reopen Condition

Implement the frozen alternating even/odd, signed Euclidean/Sturm, Hermite
hodograph, Cauchy-index, regular and nonregular Routh, Hurwitz elimination, and
minor-product packages without placeholders, then close both exact directional
cut nodes and compose them to the unchanged root. Alternatively, integrate an
immutable, license-compatible exact Lean 4 terminal into the pinned closure
with complete type, trust, dependency, provenance, and placeholder evidence.

This current-base blocker report does not satisfy `S56-M-1356-PROOF`, promote
scheduler state, or claim audit completion, validation, release, theorem
completion, receipt acceptance, or master acceptance. Because the assigned
proof phase is not genuinely complete, `.stage1-worker-selftest.json` is
deliberately absent.
