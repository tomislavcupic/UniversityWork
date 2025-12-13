echo "$@"

if [ $# -ne 2 ]; then
   echo "Pogrešan broj argumenata. Upotreba: $0 <kazalo> <oblik_datoteke>"
   exit 1
fi

lines=0
total_lines=0
while read -r file; do
   lines=$(wc -l < "$file")
   export total_lines=$(($total_lines + $lines))
done <<<$(find "$1" -type f -name "*$2")

echo "Ukupan broj redaka u datotekama: $total_lines"