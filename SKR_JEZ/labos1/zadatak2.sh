grep -iE "banana|jabuka|jagoda|dinja|lubenica" namirnice.txt

echo

grep -viE "banana|jabuka|jagoda|dinja|lubenica" namirnice.txt 

echo

grep -rE "\b[A-Z]{3}[0-9]{6}\b"  ~/projekti/

echo

echo $(find . -type f -mtime +6 -mtime -15 -exec ls -l {} +)

echo

for i in $(seq 1 15); do echo -n "$i "; done
echo

echo

kraj=15
for i in {1..$kraj}; do echo -n "$i "; done
echo
for i in $(seq 1 $kraj); do echo -n "$i "; done
echo


