#!/usr/bin/perl
print "upisi brojeve odvojene zarezom: ";
$unos = <STDIN>;
@lista = split /,/, $unos;
foreach $item (@lista) {
   $zbroj += $item;
}
$sredina = $zbroj / ($#lista + 1);
print "aritmeticka sredina: $sredina\n";