# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6763-6768` supplies exactly the title `斐波那契数列`, attribution
to Leonardo Fibonacci, year 1202, gloss `递推序列的经典例子`, importance `高`, and status
`已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no formula, bibliography,
edition, page, definition, ordered binders, hypotheses, conclusion, proof boundary, correction or
errata history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:25228-25253` repeats the gloss while explicitly leaving the formal
system, foundation, exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links unresolved. The rev-5.6 manifest assigns rank 1466,
baseline `L0 / rework_required`, no legacy slot, `lifecycle_mode: planned`, and
`theorem_complete: false`. Its `已验证` field is explicitly untrusted.

## Literal clause crosswalk

| Catalog component | Mathematical information fixed | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `斐波那契数列` | identifies a familiar sequence family | `Nat.fib` or a future source-selected characterization | object name, not a proposition |
| `递推序列` | suggests some recursive presentation | `Nat.fib_zero`, `Nat.fib_one`, `Nat.fib_add_two` | formula, index convention, carrier, and claim role absent |
| `经典例子` | descriptive classification | none | no truth-valued conclusion |
| Leonardo Fibonacci / 1202 | historical catalog metadata | provenance only | no cited edition or passage; earlier Indian history also needs disposition |
| `已验证` | untrusted inventory value | accepted source and kernel receipts would be required | no H or M completion credit |

## Modern statement and historical leads

The strongest inspected historical witness is Baldassarre Boncompagni's 1857 transcription,
*Scritti di Leonardo Pisano, matematico del secolo decimoterzo*, volume 1, *Il Liber Abbaci*, in an
authenticated Bayerische Staatsbibliothek IIIF scan (`bsb10525679`). Printed pages 283-284,
canvases 289-290, are headed `Quot paria coniculorum in uno anno ex uno pario germinentur`. They
describe one enclosed rabbit pair, monthly reproduction, and offspring reproducing from their
second month; compute one initial pair followed by monthly totals `2, 3, 5, 8, ...`, ending at 377;
and instruct the reader to continue by adding successive numbers, for indefinitely many months.

The BSB IIIF manifest was 399,319 bytes with SHA-256
`2b265efa274c23a265cfa60910bc0b69629131cf914dc82ad836cb971c53b81e`. OCR responses for canvases
289 and 290 were respectively 53,002 and 64,310 bytes with SHA-256
`eb0e47ee147fad613d9cac3cdc6d8622d3fa935c90f51934892242ab874caee2` and
`b0acbf4f82645030752a6414be4fa837e7e33fd17f6ac1d46d3f2b3225597f0d`; the canvas-289 image was
883,160 bytes with SHA-256
`e71de1f16c08586f9ad6af916cafdf236ac90be68e3194aa6f8a096e26fba162`. This transcription witness
is much closer to the historical text than a modern sequence database, but it is not the original
1202 manuscript. Edition fidelity, transcription variants, translation, proof/model mapping, and
independent review remain open. Its indexing also demonstrates that the rabbit total after modern
month `n` would require an explicit shift such as `Nat.fib (n + 2)`, not an unreviewed identification
with `Nat.fib n`.

T. C. Scott and P. Marketos, *On the Origin of the Fibonacci Sequence*, MacTutor History of
Mathematics, was inspected in a 46-page PDF dated 2014-03-23. Page 2 reproduces the rabbit problem,
displays `1, 1, 2, 3, ...`, notes that Fibonacci omitted the first term, and separately writes the
modern convention `F(0) = 0`, `F(1) = 1`, `F(n) = F(n-1) + F(n-2)` for `n > 1`. It explicitly says
Fibonacci gave the sequence rather than the recurrence formula. The PDF was 2,246,994 bytes with
SHA-256 `78585a06b28b31dad1400111328e6bff5297454fe2e4f83f1fe500a2ece469ed`.

Kurt Vogel's *Fibonacci* biography from the *Dictionary of Scientific Biography*, in a
MacTutor-hosted nine-page PDF, describes the one-month maturity and subsequent monthly reproduction
assumptions and gives the general recurrence `k_n = k_(n-1) + k_(n-2)`. It was 239,538 bytes with
SHA-256 `36bb6bbc340a57cf04da8a5ef204885e5af7f81bd8617143fb6a64d01f9608ad`.
The MacTutor Fibonacci biography itself quotes the model, displays `1, 1, 2, 3, ...`, notes the
omitted first term, and distinguishes the 1202 and 1228 editions; its observed 76,091-byte HTML had
SHA-256 `0b6fdc363c504ae034cea426cd2cf811ae7ed9a41cfa2ecc3bb2e4b640f1a62c`.
These three modern historical accounts sharpen the model and indexing boundary but are secondary,
not H0 evidence.

OEIS entry A000045, observed on 2026-07-13, labels the Fibonacci numbers by
`F(n) = F(n-1) + F(n-2)` with `F(0) = 0` and `F(1) = 1`. Its current page also records that related
numbers appeared in Indian metrical work before Fibonacci, cites Leonardo of Pisa's 1202
*Liber Abaci*, and says that the rabbit problem appears on pages 404-405 of Laurence Sigler's
English translation.

The observed A000045 HTML response was 218,934 bytes with SHA-256
`75edfbb494709bada5251fa3fb63d427c4c9456a8d2fed8cc356918f0d8f0c3e`. This digest is response
provenance only: OEIS is a live, collaboratively edited secondary database, not an immutable
edition or a primary proof source. Its current comment names remark `[27]` on page 637, while its
bibliography names `[26]` on page 627. That unresolved inconsistency prevents treating the page as
a pinpoint source crosswalk.

Crossref metadata and the Springer book page confirm Laurence Sigler,
*Fibonacci's Liber Abaci: A Translation into Modern English of Leonardo Pisano's Book of
Calculation*, Springer New York, DOI `10.1007/978-1-4613-0079-3`, published 2002. The observed
Crossref response was 1,977 bytes with SHA-256
`12262f404a459d4b5ad527641eae87ae590b256b9de6ad5371f15c926d4a1287`. The translation's relevant
pages were not accessed or preserved in this intake, and no original manuscript, exact rabbit
model, recurrence extraction, proof, translation audit, correction history, or independent review
was performed. These are bibliographic and statement leads only, not H0 evidence.

The historical record is especially important here: the catalog's simple attribution does not
decide whether the root should formalize Fibonacci's rabbit model, the modern zero-based sequence,
or a recurrence characterization. A target correction must make that choice explicitly.

## Pinned Lean candidate crosswalk

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, source
`Mathlib/Data/Nat/Fib/Basic.lean` defines the natural Fibonacci function using stream iteration and
documents the convention `F_0 = 0`, `F_1 = 1`, `F_(n+2) = F_n + F_(n+1)`.

| Declaration | Candidate role | Intake boundary |
|---|---|---|
| `Nat.fib` | natural-valued zero-based sequence definition | exact object candidate; not a selected truth-valued root |
| `Nat.fib_zero` | initial value at zero | statement component only |
| `Nat.fib_one` | initial value at one | statement component only |
| `Nat.fib_two` | first derived value | boundary probe, not a root theorem |
| `Nat.fib_add_two` | all-natural recurrence theorem | strong exact-looking candidate; source identity and root role open |
| `Nat.fib_add_one` | predecessor spelling away from zero | alternate candidate with a nonzero hypothesis and truncated subtraction |

`IntakeProbe.lean` checks these definitions and statements with the pinned Lean executable. It does
not declare a target wrapper, normalize a canonical expression, audit terminal provenance or
transitive trust, or assign M0 proof credit. The provisional machine status is `M3`: useful formal
definition/statement interfaces exist, but the catalog has not selected a proposition for them to
match.

## First downstream gate

Before ordinary statement work can pass, accountable reviewers must approve a target correction or
redirection, preserve one immutable mathematical source, select one exact proposition, map every
definition, binder, hypothesis, conclusion, indexing convention, boundary case, proof dependency,
translation, and correction, and independently approve fidelity to `THM-M-0925`. Only then may the
statement phase choose minimal imports, serialize the elaborated expression and environment
fingerprint, check alternate encodings, and run removed-hypothesis, changed-domain, binder-scope,
and boundary-case mutations. H5 applies to the received catalog wording, not to established
Fibonacci mathematics.
