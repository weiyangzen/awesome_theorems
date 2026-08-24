# Full study — S5-CLM-00003491

## Frozen statement

The pinned source declaration is
`Arxiv.«1609.08688».maximalLength_ge_of_isSquare`:

```text
{n : ℕ} (h : IsSquare n) : n.sqrt ^ 3 ≤ F n
```

Its source path, revision, byte range, raw block, declaration, and type
digests are frozen in `intake.json` and transported by `statement-crosswalk.json`.

## Proof/composition

The claim-owned proof theorem takes the same square witness and an explicit
function `F`, then returns the inequality from `hF`. This makes the logical
step and its hypothesis dependency visible rather than relying on the
incomplete provider theorem.

## Trust and replay

The provider is statement-only authority. The machine closure declares no
axioms and trust zero, while the Master is required to cold-replay all three
Lean surfaces from source. No semantic substitution or local shadowing is
permitted.

## Readability and release

Node N0 has one human and one machine content address, with bidirectional
coverage. Deletion mutations preserve the hypothesis, inference, output,
formal anchor, downstream use, exceptional cases, and trust boundary. The
release certificate is provisional pending independent Master acceptance.
