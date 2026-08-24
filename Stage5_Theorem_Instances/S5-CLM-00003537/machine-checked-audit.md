# Machine-checked audit

Root: `Bugeaud06.pollington_de_mathan` at the exact frozen declaration type
SHA-256 `9ece9d4869cc149e0f56990757d00b6376e6940f20e40230e91fb54c26cfac32`.

The claim-owned `Statement.lean`, `Proof.lean`, and `Audit.lean` surfaces each
contain the exact provider-module import spelling and a qualified reference to
the frozen declaration, contain no local definitions, abbreviations, parser
extensions, instances, aliases, opaque declarations, unsafe declarations, or
placeholders, and elaborate under `lean --trust=0`.

The machine record binds the provider revision, source bytes, declaration type
and body hashes, semantic environment, dependency edges, observed axioms,
empty machine cut set, and cold replay bit. The independent Master remains
responsible for recomputation after integration.
