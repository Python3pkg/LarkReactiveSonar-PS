#!/usr/bin/perl

#use strict;
if(!defined $ARGV[0]){
	die ("ERROR: No Project name provided!");
}else{
	get_ls_sitelist($ARGV[0], $ARGV[1]);
}
