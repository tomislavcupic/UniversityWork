if [ $# -ne 2 ]; then
   echo "Upotreba: $0 <ime_direktorija_jedan> <ime_direktorija_dva>"
   exit 1
fi

dir1="$1"
dir2="$2"

if [ ! -d "$dir1" ] || [ ! -d "$dir2" ]; then
   echo "Neki od direktorija ne postoji."
   echo "Upotreba: $0 <ime_direktorija_jedan> <ime_direktorija_dva>"
   exit 1
fi

for file in "$dir1"/*; do
   dest_file="$dir2/$(basename "$file")"
   if [ -e "$dest_file" ]; then
      if [ "$file" -nt "$dest_file" ]; then
         echo "$file --> $dir2"
      elif [ "$dest_file" -nt "$file" ]; then
         echo "$dest_file --> $dir1"
      fi
   else
      echo "$file --> $dir2"
   fi
done

for file in "$dir2"/*; do
   dest_file="$dir1/$(basename "$file")"
   if [ ! -e "$dest_file" ]; then
      echo "$file --> $dir1"
   fi
done