proba="ovo je proba"
echo $proba

echo

lista_datoteka=(*)
echo "${lista_datoteka[@]}"

echo

proba3="$proba. $proba. $proba. "
echo $proba3

echo

a=4
b=3
c=7
d=$(((a+4)*b%c))
echo "a: $a"
echo "b: $b"
echo "c: $c"
echo "d: $d"

echo

broj_rijeci=$(wc -w *.txt)
echo $broj_rijeci

echo

echo ~