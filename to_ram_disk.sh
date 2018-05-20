FILES=('myfuzzer.py' 'compare.sh' 'converter_static' 'testinput.img')
TARGET='/run/user/1000/fuzzer'

rm -rf "$TARGET"
mkdir -p "$TARGET/crash"

for FILE in "${FILES[@]}"
do
  BASENAME=$(basename "$FILE")
  cp "$FILE" "$TARGET/$BASENAME"
done

cd "$TARGET"
