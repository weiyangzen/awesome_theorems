# Exact-statement gate: blocked

Item: `S56-M-1407-STATEMENT`

Theorem: `THM-M-1407`

Base revision: `1f79a3f74a8e206d44c27513f4016a26dd7050e3`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The record gives the title `Bernoulli移位` ("Bernoulli shift"), attributes it collectively to many
mathematicians in the twentieth century, and gives only the gloss `Bernoulli系统的分类`
("classification of Bernoulli systems"). It supplies no proposition, definition, source locator,
ordered binders, hypotheses, conclusion, or boundary conventions. Stage0 explicitly leaves the
precise definitions and assumptions open. The metadata value `已验证` is untrusted inventory
metadata, not a source statement or kernel receipt.

Several inequivalent targets remain compatible with that wording: constructing a one- or two-sided
Bernoulli shift, proving invariance of its product measure, proving ergodicity or mixing, computing
entropy, or classifying shifts up to measure-theoretic isomorphism. These require different
alphabets and base laws, index domains, shift orientations, hypotheses, conclusions, and null-set
conventions. The classification reading is especially unsafe because the adjacent target
`THM-M-1408`, Ornstein's isomorphism theorem, has the identical repository gloss. Choosing that
reading here could duplicate a separately scheduled theorem; choosing any other familiar fact
would likewise substitute mathematics the repository did not select.

Consequently there is no canonical human proposition from which to derive a minimal import,
normalized kernel-expression fingerprint, checked alternate transport, or meaningful
removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations. Section 5.1 of
the rev-5.6 blueprint fails at exact source-statement identity before proof evidence may be
inspected. Machine state remains `M4`; statement and theorem completion are false.

## Pinned Lean boundary

The existing `IntakeProbe.lean` directly imports
`Mathlib.Probability.Independence.InfinitePi` and
`Mathlib.Dynamics.Ergodic.Ergodic`. In the pinned environment it elaborates generic declarations
for infinite product measures, measure-preserving reindexing and coordinate evaluation, the
`MeasurePreserving` predicate, and the `Ergodic` predicate. A bounded source-name search found no
Bernoulli-shift or Bernoulli-system declaration in pinned mathlib.

Those declarations show only that some candidate encodings have substrate. They do not choose
between the incompatible readings above, are not a canonical target, do not establish minimal
imports for an unknown target, and receive no statement or proof credit. No target Lean file
contains `sorry`, `admit`, an `axiom`, or an `opaque` declaration.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. The pre-existing
`Formalizations/Lean/.lake` link points to the canonical checkout's pinned artifacts and was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on `2026-07-12` (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1407` | 0 | rank 906; planned; legacy artifacts unaccepted; theorem incomplete |
| `git status --short && git rev-parse HEAD HEAD^{tree} && readlink Formalizations/Lean/.lake` | 0 | before statement edits, only the pre-existing untracked `.lake` link was present; base revision and tree are recorded above and in `statement-blocker.json` |
| `rg -n -C 4 'Bernoulli移位\|Bernoulli系统的分类' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | 0 | found only the underspecified catalogue and Stage0 records; the identical THM-M-1408 gloss confirms the unresolved overlap |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json ../../Stage1_Instances/THM-M-1407/IntakeProbe.lean && git -C .lake/packages/mathlib rev-parse HEAD` | 0 | hashes and pinned mathlib revision match `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1407/IntakeProbe.lean` | 0 | all five generic infinite-product, reindexing, coordinate, measure-preservation, and ergodicity API checks elaborated; no canonical theorem asserted |
| `cd Formalizations/Lean && rg -n -i 'Bernoulli[ _-]?(shift\|system)\|shift[ _-]?Bernoulli' .lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | expected no-match exit in the bounded pinned source-name search; this is not an exhaustive anchor audit |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*(axiom\|opaque)\\b' Stage1_Instances/THM-M-1407 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder, axiom, or opaque declaration occurs in target Lean source |
| `python3 Stage1_Instances/THM-M-1407/check_intake.py` | 1 | the historical intake checker is stale against the current generated DAG: it expects intake `[ ]`, while the authoritative current DAG records intake `[_]`; this is not statement evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-1407/statement-blocker.json >/dev/null` | 0 | the structured blocker is valid JSON |
| bounded per-file `git diff --no-index --check -- /dev/null <new-blocker-file>` wrapper | 0 | both untracked owned-path artifacts have no whitespace errors; raw exit 1 is accepted only as the normal content-difference result, while exit greater than 1 fails |
| `test ! -e .stage1-worker-selftest.json` | 0 | the required no-self-test boundary is preserved because the statement deliverable is blocked |
| final parse, untracked-whitespace, prohibited-construct, self-test-absence, and scoped-status audit | 0 | only the pre-existing `.lake` link and the two new blocker artifacts are untracked; all statement-phase writes are inside the assigned owned path |

## Retry condition and status boundary

An accountable reviewer must preserve and hash an immutable primary or authoritative source,
select and transcribe one exact theorem with all incorporated definitions and a pinpoint locator,
audit errata, reconcile the selection with `THM-M-1408`, and independently approve the mapping.
The selection must freeze the alphabet and base probability law, one- or two-sided index domain,
product measurable space and measure, shift direction, isomorphism and null-set conventions,
ordered binders, hypotheses, conclusion, and all boundary cases. A later statement worker can then
encode that same claim, minimize the pinned imports, serialize and hash the elaborated expression,
check alternate transports, and run all four required statement mutations.

This is the first failed gate, not completion of the statement node or any downstream node. The
root remains `[H4, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no
debt-vector change is proposed. The assigned phase is not genuinely self-tested, so no
`.stage1-worker-selftest.json` is emitted.
