if [ $# -ne 1 ]; then
    echo "Upotreba: $0 <ime_direktorija>"
    exit 1
fi

directory="$1"

if [ ! -d "$directory" ]; then
    echo "Direktorij '$1' ne postoji."
    echo "Upotreba: $0 <ime_direktorija>"
    exit 1
fi

for datoteka in "$directory"/*.txt; do
    datum=$(basename "$datoteka" | grep -E -o '[0-9]{2}-[0-9]{2}-[0-9]{4}')
    novi_datum="$datum"
    if echo "$datum" | grep -qE '^[0-9]{2}-02-[0-9]{4}$'; then
        echo "datum: $novi_datum"
        echo "--------------------------------------------------"
        grep -oE '"[A-Z]+ [^"]+"' "$datoteka" | sort | uniq -c | sort -nr
        echo
    fi
done