# Statement phase blocker

Item: `S56-M-0445-STATEMENT`  
Base revision: `129c68bce8fd58065c4af147e92a1975267f0279`

## Gate result

The exact Lean 4 target cannot be truthfully selected from the repository source. The complete
human statement attached to this target is `椭圆曲线的BSD` (BSD for elliptic curves), while the
target name is Rubin-Kolyvagin theorem. The source gives no theorem citation, curve hypotheses,
analytic-rank restriction, CM/Iwasawa or Heegner-point assumptions, or precise conclusion. In
particular, it does not decide between:

- equality of analytic and Mordell-Weil ranks plus finiteness of the Tate-Shafarevich group in an
  analytic-rank-at-most-one setting; and
- the stronger full BSD leading-term formula.

Selecting either candidate would add unstated hypotheses and choose an unstated conclusion. This
is the exact-statement hard blocker described by section 5 of
`Docs/Stage1_Blueprint_rev-5.6.md`. Consequently no canonical expression hash, minimal-import
claim, checked alternate transport, or semantic mutation suite can be produced in this phase.

The historical module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_091.lean` does elaborate,
but its own documentation identifies `StatementShape` and `FullBSDStatementShape` as abstract,
competing discovery boundaries. Their proposition-valued fields stand in for the missing
elliptic-curve L-function, Mordell-Weil rank, Tate-Shafarevich group, and Euler/Kolyvagin-system
APIs. Elaboration of that module therefore is environment evidence only, not elaboration of the
exact target.

Required unblocker: an authoritative source crosswalk must identify an edition, theorem and page,
ordered hypotheses, precise conclusion, and applicable errata for the intended Rubin and/or
Kolyvagin result. Statement work can then encode that claim and test it without substitution.

## Commands and results

Commands were run from the repository root unless a working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 1546 uniform-L0 Lean 4 targets and 15 assurance groups |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0445` | 0 | rank 91, `planned`, L0/rework required, theorem incomplete |
| `lake env lean AwesomeTheorems/Stage1/S1_M_091.lean` (cwd `Formalizations/Lean`) | 0 | Historical discovery module elaborated; it printed the expected checked declaration types and no errors |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_091.lean` | 0 | SHA-256 values: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`, `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, `755068effda6d0d7c2047b5b35db9376c2851f391c3543a971aafbae80bc49e5` |

No dependency update, build, fetch, or mutation of the shared `.lake` artifacts was performed. No
statement-phase self-test manifest is emitted because the assigned deliverable is blocked rather
than self-tested.
