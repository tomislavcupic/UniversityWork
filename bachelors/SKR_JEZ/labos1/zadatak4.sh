if [ $# -ne 1 ]; then
    echo "Upotreba: $0 <ime_direktorija>"
    exit 1
fi

direktorij="$1"
counter=1
if [ ! -d "$direktorij" ]; then
    echo "Direktorij '$1' ne postoji."
    echo "Upotreba: $0 <ime_direktorija>"
    exit 1
fi

while read -r datoteka; do
   datoteka=$(basename "$datoteka")
   datum=$(echo "$datoteka" | grep -E -o '[0-9]{6}' | head -c 6)

   if [ "$datum" != "$stari_datum" ]; then
      if [ "$counter" != 1 ]; then
         ((counter=counter-1))
         echo "--- Ukupno: $counter slika -----"
      fi         
      echo "$datum: "
      echo "----------"
      ((counter=1))
   fi
   
   stari_datum="$datum"
   
   echo "$counter. $datoteka"
   
   counter=$(($counter + 1))

done <<<$(find "$direktorij" -type f -name "*.jpg")
((counter=counter-1))
echo "--- Ukupno: $counter slika -----"
