#!/usr/bin/perl   
print "upisi liniju koju ces printati: ";
$linija = <STDIN>;
print "upisi broj ponavljanja: ";
$broj_ponavljanja = <STDIN>;

while ($broj_ponavljanja > 0) {
   print "$linija";
   $broj_ponavljanja -= 1;
}