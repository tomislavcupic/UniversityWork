#!/usr/bin/perl

use strict;
use warnings;
use open ':locale';
use locale;
use utf8;

if (@ARGV < 1) {
    die "Upotreba: $0 [datoteka ...] duljina_prefiksa\n";
}

my $prefix_len = pop @ARGV;

die "Zadani prefiks mora biti pozitivan broj\n" unless $prefix_len =~ /^\d+$/ && $prefix_len > 0;

my @lines;
if (@ARGV) {
    while (<>) {
        push @lines, $_;
    }
} else {
    while (<STDIN>) {
        push @lines, $_;
    }
}

my $text = join ' ', @lines;
$text =~ s/[[:punct:]]+/ /g;
$text =~ s/\s+/ /g;

my %prefix_count;

foreach my $word (split(/\s+/, $text)) {
    next if $word eq '';
    $word = lc($word);
    next if length($word) < $prefix_len;
    my $prefix = substr($word, 0, $prefix_len);
    $prefix_count{$prefix}++;
}

foreach my $prefix (sort keys %prefix_count) {
    print "$prefix : $prefix_count{$prefix}\n";
}
