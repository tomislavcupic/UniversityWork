#!/usr/bin/perl

sub jeli_komentar {
   $_[0] == "#";
}

my $file = shift || die "Wrong number of arguments";

open my $fh, '<' , $file or die "cannot open";
$prvi_prolaz = 0;
%rang_lista;
while (my $linija = <$fh>) {
   if ($prvi_prolaz == 0) {
      if (jeli_komentar($linija)){
         next;
      }
      else{
         $prvi_prolaz = 1;
         @koeficijenti = split /;/, $linija;
         next;
      }
   }
   if (jeli_komentar($linija)){
      next;
   }
   chomp $linija;
   my ($jmbag, $prezime , $ime, @rezultati ) = split /;/, $linija;
   my $zbroj = 0;
   foreach(0..$#koeficijenti){
      @rezultati[$_] *= @koeficijenti[$_];
      $zbroj += @rezultati[$_];
   }
   $rang_lista{$prezime . ", " . $ime . " (" . $jmbag . ")"} = $zbroj;
}
print "\nLista po rangu: \n";
print "-------------------\n";
my @sortani_rang = reverse sort { $rang_lista{$a} <=> $rang_lista{$b} } keys %rang_lista;
foreach $stud (@sortani_rang){
   print "$stud : @rang_lista{$stud}\n";
}