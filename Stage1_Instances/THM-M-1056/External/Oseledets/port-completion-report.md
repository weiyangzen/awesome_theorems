# M1056 62-module Lean 4.29 compatibility-port report

- Source: `marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`.
- Immutable source archive: `https://codeload.github.com/marcmorningstar/lean4-ergodic-theory/tar.gz/ed3fa6b8a30594eeb791160563942ba115581aa0`, SHA-256 `3c0ef177500430ab55950061cfd73991347f5336b5b3d5032ffe46ac56009a52`.
- Pinned environment: Lean `4.29.0` commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- Ordered closure: 62 modules (`order.txt` SHA-256 `3529944cfaf77a647d3e86c1bf4ab7c19164f828b780a68566bcad4a6f0d1561`).
- All 62 modules compiled under `--trust=0`; terminal `SplittingAssembly.lean` compile log is empty and exit 0.
- Terminal `.olean`: SHA-256 `3f3165b7a9a58ab36f769fa03d68c4d520fec734dc45a7672c6733a3d3067197`.
- Kernel dependency probe: `[propext, Classical.choice, Quot.sound]`.
- Compatibility patch: 26 modified modules, 877 lines, SHA-256 `7984d9e0199f8cbd1540d6fa8411bd931b79ea3431ae4acb0fbe534594d9c529`.
- Source hash-list aggregate: `0168b82b92c5adf6ddf884ad2a3beaf5e305aea5208cd294d754195fd27f4940`.
- Olean hash-list aggregate: `08acecc22f5c8dd7098eb48d7c70a737c2f2f070938a92982f5ea3b25cf6227f`.

## Compile recipe

```bash
ROOT=$(git rev-parse --show-toplevel)
VENDOR="$ROOT/Stage1_Instances/THM-M-1056/External/Oseledets"
LEAN_ROOT="$ROOT/Formalizations/Lean"
SCRATCH=$(mktemp -d)
trap 'rm -rf "$SCRATCH"' EXIT
cp -R "$VENDOR/ErgodicTheory" "$SCRATCH/ErgodicTheory"
cd "$LEAN_ROOT"
BASE_LEAN_PATH="$(lake env printenv LEAN_PATH)"
while read -r mod; do
  src="$SCRATCH/${mod//.//}.lean"
  out="$SCRATCH/${mod//.//}.olean"
  LEAN_PATH="$SCRATCH:$BASE_LEAN_PATH" LEAN_NUM_THREADS=1 \
    lake env lean --trust=0 -R "$SCRATCH" "$src" -o "$out"
done < "$VENDOR/order.txt"
```

## Axiom probe

```bash
printf '%s\n' \
  'import ErgodicTheory.TwoSided.SplittingAssembly' \
  '#print axioms ErgodicTheory.oseledets_splitting' \
  > "$SCRATCH/ProbeOseledetsSplitting.lean"
LEAN_PATH="$SCRATCH:$BASE_LEAN_PATH" LEAN_NUM_THREADS=1 \
  lake env lean --trust=0 -R "$SCRATCH" "$SCRATCH/ProbeOseledetsSplitting.lean"
```

Output: `ErgodicTheory.oseledets_splitting` depends on `[propext, Classical.choice, Quot.sound]`.
