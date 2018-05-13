
if [[ $# != 2 ]]
then
  echo "usage: $0 FILE1 FILE2"
  exit 1
fi

cmp -l "$1" "$2" | gawk '{printf "%08X %02X %02X\n", $1, strtonum(0$2), strtonum(0$3)}'
