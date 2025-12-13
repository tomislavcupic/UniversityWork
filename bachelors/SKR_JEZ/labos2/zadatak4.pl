#!/usr/bin/perl

sub file {
   my $file = shift @ARGV || die "Wrong number of arguments";
   open my $fh, '<' , $file or die "cannot open";
   while (my $linija = <$fh>) {
      chomp $linija;
      my ($jmbag, $prezime, $ime, $termin, $zakljucano) = split /;/, $linija;
      next unless ispod_sat($termin, $zakljucano);
      print "$jmbag $prezime $ime - PROBLEM: $termin --> $zakljucano\n";
   }
}

sub ispod_sat {
   my ($vrijeme1, $vrijeme2) = @_;
   my ($godina1, $mjesec1, $dan1, $pocetni_sat1, $pocetna_minuta1, $zavrsni_sat1, $zavrsna_minuta1) = ($vrijeme1 =~ /^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}) (\d{2}):(\d{2})/);
   my ($godina2, $mjesec2, $dan2, $sat_predaje, $minuta_predaje) = ($vrijeme2 =~ /^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):00$/);
   if ($godina1 == $godina2 and $mjesec1 == $mjesec2 and $dan1 == $dan2) {
      my $vrijeme_poc_minute = $pocetni_sat1 * 60 + $pocetna_minuta1;
      my $vrijeme_kraj_minute = $zavrsni_sat1 * 60 + $zavrsna_minuta1;
      my $vrijeme_predaje_minute = $sat_predaje * 60 + $minuta_predaje;
      return !($vrijeme_predaje_minute > $vrijeme_poc_minute && $vrijeme_predaje_minute < $vrijeme_kraj_minute + 60);
   }
}

sub main{
   if (@ARGV == 0) {
      print "Unesite studente u formatu JMBAG;Prezime;Ime;Termin;Zaključano\n";
      print "Kada ste gotovi, napišite STOP\n";
      while (my $linija = <STDIN>) {
         chomp($linija);
         last if $linija eq "STOP";
         my ($jmbag, $prezime, $ime, $termin, $zakljucano) = split /;/, $linija;
         if (ispod_sat($termin, $zakljucano)){
            print "$jmbag $prezime $ime - PROBLEM: $termin --> $zakljucano\n";
         }
         else{}
      }
   }
   else {
      file(@ARGV);
   }
}
main();