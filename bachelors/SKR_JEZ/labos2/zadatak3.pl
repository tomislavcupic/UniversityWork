#!/usr/bin/perl

sub prebroji_pristupe {
   my ($file) = @_;
   my %broj;
   open(my $fh, '<', $file) or die "Nemoguće otvoriti '$file' $!";

   while (my $line = <$fh>) {
      if ($line =~ /^\S+ \S+ \S+ \[([^\]]+)\]/) {
         my $timestamp = $1;
         print "$timestamp";
         if ($timestamp =~ /\d{2}\/\w{3}\/\d{4}:(\d{2})/) {
               my $hour = $1;
               $broj{$hour}++;
         }
      }
   }
   close($fh);
   return \%broj;
}

sub print_pristupi {
   my ($broj_pristupa, $date) = @_;
   my %broj = %$broj_pristupa;

   print "Datum: $date\n";
   print "sat : broj pristupa\n";
   print "-------------------------------\n";

   foreach my $hour (sort {$a <=> $b} keys %broj) {
      printf "%02d : %d\n", $hour, $broj{$hour};
   }
}

sub main {
   if (@ARGV == 0) {
      print "unesite datum u formatu YYYY-MM-DD: \n";
      $date = <STDIN>;
      chomp($date);
      print "unesite pristupe:\n";
      my %broj;
      while (my $linija = <STDIN>) {
         chomp($linija);
         last if $linija eq "STOP";
         if ($linija =~ /\d{2}\/\w{3}\/\d{4}:(\d{2})/) {
            my $hour = $1;
            $broj{$hour}++;
         }
      }
      print_pristupi(\%broj, $date);
   } else {
      foreach my $file (@ARGV) {
         my ($date) = $file =~ /(\d{4}-\d{2}-\d{2})/;
         my $broj_pristupa = prebroji_pristupe($file);
         print_pristupi($broj_pristupa, $date);
      }
   }
}

main();