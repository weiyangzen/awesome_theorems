# THM-M-0751 rev-5.6 statement blocker

## Decision

`S56-M-0751-STATEMENT` remains `[ ]`. Its prerequisite `S56-M-0751-INTAKE` is provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt has `accepted: false`, is not
content-addressed, and names no accepted receipt. Rev-5.6 permits provisional preparation of this
blocker, but master closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The catalog records only the
title `图灵度的上确界` (supremum of Turing degrees), a collective twentieth-century attribution,
the gloss `图灵度的格结构` (lattice structure of Turing degrees), importance "high," and an
untrusted `已验证` label. It gives no citation, formula, degree model, incorporated definition,
ordered binder, hypothesis, conclusion, proof boundary, correction history, formal declaration, or
reviewer. Stage0 explicitly leaves the formal system, precise definitions and premises, proof
route, dependencies, alternate forms, axiom policy, machine status, and artifacts open.

The wording identifies a theorem family, not one binder-complete proposition. Materially different
roots fit it:

- a binary join of two Turing degrees;
- all finite nonempty joins;
- countable joins under a uniformity condition;
- arbitrary suprema or a completeness assertion; and
- a full lattice assertion including binary meets.

The inspected source leads support only the upper-semilattice family. Kleene and Post's 1954 paper
*The Upper Semi-Lattice of Degrees of Recursive Unsolvability* is a strong primary bibliographic
lead, but intake admitted only Crossref and OpenAlex metadata. Its theorem text, incorporated
definitions, assumptions, proof, corrections, errata, and source-to-catalog identity were not
inspected or independently reviewed. The immutable Encyclopedia of Mathematics revision 46619 says
that set and function degrees form isomorphic upper semilattices, but gives no exact join formula or
proof. Neither source authorizes silently repairing the catalog's broader "lattice" gloss.

Even a binary root requires proposition-changing mathematical choices. The admitted source and
review must fix whether degrees are represented by subsets, characteristic functions, total
functions, or partial functions; the reducibility and oracle semantics; the input family; both
upper-bound relations; leastness; and every boundary convention. It must also make clear whether a
particular representative construction is part of the claim or only a proof route. The statement
freeze must then choose a faithful Lean encoding, such as an explicit existential proposition,
`IsLUB`, a `sup` operation with laws, or a `SemilatticeSup` instance, and check any credited
transports. A historical source need not use Lean vocabulary. Representative independence and
quotient descent are downstream proof obligations unless the approved claim itself includes a
construction.

Sections 5 and 5.1 of the rev-5.6 standard require that exact claim before a canonical Lean
expression, minimal imports, fixed context, expression and environment fingerprints, alternate
transports, or mutation tests can be credited. The execution skill hard-stops when source identity
would require inventing missing mathematics. Accordingly, no `Statement.lean`, statement receipt,
or `.stage1-worker-selftest.json` was emitted.

## Lean boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with the pinned toolchain. Its one
direct import, `Mathlib.Computability.TuringDegree`, exposes:

- `TuringReducible`;
- `TuringEquivalent`;
- `TuringDegree`; and
- `TuringDegree.instPartialOrder`.

The probe exited 0. Its exact stdout is 167 bytes with SHA-256
`2db08bbaa506acb518138880a5839687278bd0ddb20a2a8327b5aa916140802c`; stderr was empty. The
pinned `TuringDegree.lean` file has 132 lines and ends at the partial-order instance. A bounded
repository-local and pinned mathlib search found no source matching `TuringDegree` together with
supremum, join, LUB, semilattice, or lattice terminology. The 132-line source declares no
`TuringDegree`-specific join or supremum operation, `SemilatticeSup`, `SupSet`, or `Lattice`
instance, or LUB theorem. Generic order declarations such as `SemilatticeSup`, `Lattice`, `sSup`,
`iSup`, and `IsLUB` are available transitively, but they do not supply this target.

These checks authenticate adjacent substrate only. `Mathlib.Computability.TuringDegree` is
sufficient for that probe, but it cannot be certified as the minimal import of an absent canonical
target. The negative searches are scoped feasibility observations, not the downstream anchor audit
or a global absence claim.

## Required retry inputs

Before a fresh statement run, the integration lane and accountable independent reviewers must:

1. Master-accept refreshed intake evidence.
2. Preserve and hash one lawful immutable primary or approved authoritative source with an exact
   theorem locator, incorporated definitions, proof boundary, corrections, and errata.
3. Approve the source-to-catalog identity and choose the exact mathematical degree carrier,
   reducibility and oracle model, input family, ordered binders, hypotheses, upper-bound and
   leastness clauses, and degenerate cases; decide whether a representative construction belongs to
   the claim or remains a downstream proof route.
4. Decide whether bottom, meets, top, distributivity, completeness, or jump compatibility is in
   scope, rather than infer any of them from the word "lattice."
5. Choose a faithful Lean encoding of only the approved proposition, minimize its pinned imports,
   serialize and hash the elaborated expression and environment, compile every credited transport,
   and run the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
   mutations.

## Validation

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0751` | 0 | rank 1337; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (pre-edit) | 0 | only `?? Formalizations/Lean/.lake`; preserved and used read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base `8a13381618b241479a4786ca67704af7322f77aa`; tree `0cc75f807f4c75d2a0aa8a72062e025083bd18ad` |
| `git blame -L 5535,5540 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| exact `sha256sum` command recorded in `statement-blocker.json` | 0 | all current authoritative, intake, toolchain, manifest, and pinned-source fingerprints recorded |
| `python3 -B Stage1_Instances/THM-M-0751/check_intake.py` | 1 | historical checker expects intake `[ ]`; integrated DAG records `[_]` with one attempt; historical evidence was not rewritten |
| `lake env lean --version` (`cwd=Formalizations/Lean`) | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `lake --version` (`cwd=Formalizations/Lean`) | 0 | Lake `5.0.0-src+98dc76e` |
| `git rev-parse HEAD 'HEAD^{tree}' 'HEAD:Mathlib/Computability/TuringDegree.lean'` (`cwd=mathlib`) | 0 | pinned revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, source blob `e321ed033ccef4c29c9611e4d27e58116c021544` |
| `git status --short --untracked-files=all` (`cwd=mathlib`) | 0 | empty; dependency worktree clean |
| `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0751/IntakeProbe.lean` (`cwd=Formalizations/Lean`) | 0 | four adjacent APIs elaborated; exact output hash recorded above; no canonical target or proof body |
| bounded `TuringDegree` plus supremum/join/LUB search recorded in JSON | 1 | expected no match; scoped discovery observation only |
| exact generic-identifier search in pinned `TuringDegree.lean` | 1 | expected no textual match in that 132-line source; generic order APIs remain available transitively |
| prohibited Lean declaration and placeholder scan | 1 | expected no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| `python3 -m json.tool Stage1_Instances/THM-M-0751/statement-blocker.json` | 0 | structured blocker parsed |
| `jq -e` over identity, dependency, null target/imports, H1/M4/R4, mutation, completion, scope, and receipt flags, followed by three filesystem absence checks | 0 | blocked `[ ]`, provisional dependency, null statement surface, unchanged vector, four undefined mutations, exact two-file scope, and absent `.stage1-worker-selftest.json`, `statement-receipt.json`, and `statement_receipt.json` agree |
| `for f in ...; do test -s "$f"; test "$(tail -c 1 "$f" \| od -An -tuC \| tr -d ' ')" = 10; ! LC_ALL=C grep -n $'\r' "$f"; ! grep -n '[[:blank:]]$' "$f"; ! od -An -v -tx1 "$f" \| tr -s ' ' '\n' \| rg -x '00' >/dev/null; done` | 0 | both blocker artifacts are nonempty and have final newlines, LF line endings, no trailing whitespace, and no NUL bytes |
| `git diff --check -- Stage1_Instances/THM-M-0751 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0751/statement-blocker.json` | 1 | expected new-file difference; empty diagnostic output and no whitespace error |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0751/statement-blocker.md` | 1 | expected new-file difference; empty diagnostic output and no whitespace error |
| `test ! -e .stage1-worker-selftest.json` | 0 | intentionally absent because the exact-statement phase did not pass |
| `test ! -e Stage1_Instances/THM-M-0751/statement-receipt.json` | 0 | intentionally absent because no canonical target was elaborated |
| `test ! -e Stage1_Instances/THM-M-0751/statement_receipt.json` | 0 | alternate statement-receipt spelling also absent |

## Status boundary

This is an unsigned, nonrelease worker observation of the first hard blocker. The lifecycle remains
`planned`, the vector remains `[H1, M4, R4]`, and all six tasks from statement through release remain
in the root cut set. It is not an exact statement, minimal-import result, expression fingerprint,
checked transport, mutation certificate, statement-node receipt, worker `[_]` completion claim,
proof, anchor audit, audit completion, theorem completion, or master acceptance. Full evidence-packet
conformance is not claimed: this blocker is not content-addressed and does not contain per-action
start/end times, complete input/output/log hashes, signatures, or release evidence.
