# Statement gate blocker

Item: `S56-M-0432-STATEMENT`  
Theorem: `THM-M-0432`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The repository metadata does not contain an exact mathematical proposition. It gives the title
"function-field Langlands correspondence", the proposer Vladimir Drinfeld, the year 1974, and the
gloss "the Langlands correspondence for function fields". This distinguishes the intended target
from the neighboring Laurent Lafforgue `GL_n` entry, but it still does not identify a primary-source
theorem, theorem number, or complete statement of Drinfeld's result. In particular, it does not
freeze:

- whether the root is the cuspidal `GL_2` correspondence or one direction of it;
- the global function field and constant-field hypotheses;
- the coefficient field, continuity, irreducibility, and determinant condition on the Galois side;
- the automorphic equivalence relation and central-character condition; or
- the exceptional-place quantifier and Frobenius/Satake normalization used for local compatibility.

Those choices change ordered binders, hypotheses, and conclusion. Choosing them from a standard
modern paraphrase would substitute an inferred theorem for the metadata rather than elaborate its
exact claim. The intake record already leaves this source identity open, so the prerequisite has not
provided a frozen claim that this statement node can elaborate. Under rev-5.6's fail-closed exact
statement gate, the machine state remains `M4`.

The legacy discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_060.lean` cannot close the gap. Its
`StatementShape` quantifies over abstract `Param`, `Auto`, conversion functions, and an unconstrained
`corresponds` predicate. Its local compatibility predicate is only equality of two stored natural
number ranks, and its conclusion is one-way existence without uniqueness. The module itself calls
these objects placeholders and records `terminalCorrespondenceStatement := false`. Treating that
shape as the target would materially weaken the correspondence and is therefore forbidden.

Pinned mathlib supplies useful function-field, Galois, representation, and local-field substrate,
but the scoped source search found no terminal Drinfeld or function-field Langlands declaration.
No abstract proxy predicate, axiom, proof placeholder, narrower special case, or Lafforgue `GL_n`
substitute was added.

## Environment fingerprint

- Repository base revision: `8bfedc3e8fd013fc57dbc65383ae2896cdda78e5`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Legacy discovery module SHA-256:
  `4ccf33366955894287ab2a1c0b20529f5eecb7ac4bd7703fc5bc13bb9d751849`.

## Validation evidence

Commands ran inside this worker clone using only the existing pinned Lake environment. No update,
build, dependency fetch, or clone was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0432` | 0 | Rank 60, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_060.lean` | 0 | Legacy discovery module elaborated; `#check` output confirms its abstract statement shape and its explicit no-completion gates |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'Langlands\|Drinfeld\|Lafforgue\|automorphic.*representation\|Satake' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Only unrelated Lafforgue attribution and Drinfeld-center results matched; no terminal correspondence declaration was found |

The successful Lean run validates only the availability and actual type of the discovery scaffold.
It is not exact-statement evidence for the theorem.

## Retry condition

Supply an immutable primary-source page and theorem label for the intended Drinfeld result, with
all definitions and assumptions needed to choose the correspondence's direction, object classes,
equivalence relations, character restrictions, exceptional places, and local normalization. A
pinned Lean object model must then represent those notions concretely enough that the target does
not quantify over an unconstrained proposition standing in for the correspondence. The next
statement run can freeze the binders and expression, elaborate it with minimal imports, and perform
meaningful domain, hypothesis, scope, and boundary mutations.

Until then, statement acceptance and theorem completion are false. Because the assigned phase did
not reach its completion gate, no `.stage1-worker-selftest.json` is emitted.
