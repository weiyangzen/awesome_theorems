# S56-M-1324-STATEMENT blocker

## Verdict

The exact Lean 4 statement gate is blocked. No `Statement.lean` has been created because doing so
from the available evidence would require choosing assumptions and a comparison theorem that the
intake explicitly leaves unresolved. Such a declaration would be a broadened or substituted target,
not an elaboration of the exact Cheng theorem.

The intake identifies only a theorem family. Its provisional root is the Ricci-lower-bound
comparison

`lambda_1(B_M(p,r)) <= lambda_1(B_K(r))`,

but it also records that Cheng's paper contains a distinct sectional-curvature comparison with the
opposite inequality. The primary text's theorem number, ordered hypotheses, dimension assumptions,
radius/cut-locus restrictions, curvature normalization, and Laplacian convention have not been
frozen. These differences are proposition-changing and cannot be represented as harmless Lean
encoding choices.

This is the first failed gate in Blueprint section 5.1: there is no exact canonical mathematical
claim to map to an elaborated expression. Consequently an expression fingerprint, mutation tests,
and checked alternate-form transports would be misleading. Machine debt remains `M4`; no proof or
theorem-completion credit is claimed.

## Environment and validation evidence

Base revision: `1cad5fb04b4f845438a8105579b15a830b03b7e7`.

Commands were run from the worker repository root on 2026-07-12.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard consistent: 1546 uniform-L0 Lean 4 targets and execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1324` | 0 | Rank 486, planned, target lane `hard_mathlib_anchor_and_wrapper` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `curl -L --fail --max-time 20 -sS https://link.springer.com/content/pdf/10.1007/BF01214381.pdf -o /tmp/cheng.pdf` | 0 | The endpoint returned an HTML access page, not the paper PDF; `file /tmp/cheng.pdf` reported `HTML document, ASCII text` |
| `curl -L --fail --max-time 20 -sS https://api.crossref.org/works/10.1007/BF01214381` | 0 | Confirmed only bibliographic metadata: Cheng, *Math. Z.* 143 (1975), pp. 289-297; no theorem text or assumptions |

The pinned `.lake` symlink was only read. No dependency update, fetch, clone, or build was run.
`lake env lean` was limited to identifying the pinned executable because there is no exact
proposition that can truthfully be submitted for elaboration.

## Unblocking requirement

An integration/source-audit lane must provide an immutable copy of Cheng (1975), a checksum and
page/theorem pinpoint, a verbatim statement with conventions and errata disposition, and an
independent decision selecting the intended member of the theorem family. The statement phase can
then encode exactly that claim, minimize imports, serialize the elaborated expression and
environment fingerprint, and run the four required mutation classes.

No `.stage1-worker-selftest.json` is emitted because the assigned statement phase is not
self-tested or complete.
