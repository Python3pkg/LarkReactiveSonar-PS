#!/usr/bin/perl

require perfSonar;
#use strict;
if((!defined $ARGV[0] || $ARGV[0]=="") && !defined $ARGV[1] && !defined $ARGV[2]) {
	die ("ERROR: No site provided!");
}else{
	get_ls_endpoint_pair($ARGV[0], $ARGV[1], $ARGV[2]);
}
