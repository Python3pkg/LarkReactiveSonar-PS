#!/usr/bin/perl


use lib "../../lib";

use threads;
use perfSONAR_PS::Client::LS;
use XML::LibXML;
use XML::DOM;
use perfSONAR_PS::Common qw( find findvalue );



sub get_ls_sitelist
{
	my $project_name;
	my $gLs;
	($project_name, $gLs) = @_;

	my @sitelist_list = ();
	my $array_size = 0;

	my $xls_gls_sitelist = get_gls_sitelist("project:".$project_name);
	my $xls_hls_sitelist = get_hls_sitelist("project:".$project_name); 

	my $gLSClient = initiate_gls($gLs);

	my $gLSResult = query_to_gls($gLSClient,$xls_gls_sitelist);
	
	if ($gLSResult eq "")
	{
		return -1;
	} 

	my $parser = XML::LibXML->new();
	
	my $gLSDoc = $parser->parse_string($gLSResult);
	my $hLSList = find($gLSDoc->getDocumentElement, "./*[local-name()='accessPoint']", 0);


	# Loop through each home lookup service
	for(my $i = 0; $i < $hLSList->size(); $i++)
	{ 
		my $hLSUrl =  $hLSList->get_node($i)->string_value();
		#async { #120
		my $hlsClient = new perfSONAR_PS::Client::LS(
		{
		instance => $hLSUrl
		}
		);

		# Send request to home lookup service
		my $hLSResult = $hlsClient->queryRequestLS(
		{
		query => $xls_hls_sitelist,
		format => 1 #want response to be formated as XML
		}
		);

		my $resParser = XML::LibXML->new();

		if($hLSResult->{response} && $hLSResult->{response} =~ /^</)
		{
			# Print list of matching bwctl server addresses
			my $hLSDoc = $resParser->parse_string($hLSResult->{response});
			my $bwctlList = find($hLSDoc->getDocumentElement, "./*[local-name()='address']", 0);
			for(my $j = 0; $j < $bwctlList->size(); $j++)
			{
				my $output = $bwctlList->get_node($j)->string_value();
				my $find = "tcp://";
				my $replace = "";
				$find = quotemeta $find; # escape regex metachars if present
				$output =~ s/$find/$replace/g;


				print $output."\n";
				push(@sitelist_list,$bwctlList->get_node($j)->string_value()); 
			}
		}
	}
	$array_size = @sitelist_list;

}

sub get_gls_projects
{
	my $gLs;
	$gLs = @_;

	my @project_list = ();
	my $array_size = 0;

	my $xls_keyword = get_gls_keyword();
	print $gLs;
	my $gLSClient = initiate_gls($gLs);
	
	my $gLSResult = query_to_gls($gLSClient,$xls_keyword);

	if ($gLSResult eq "")
	{
		return -1;
	}

	@project_list = parse_query_keyword($gLSResult);

	for my $element_1(@project_list)
	{
		print $element_1 . "\n";
	}

}


sub parse_query_keyword
{
	my $result;
	($result) = @_;
	
	my $xml_parser = XML::DOM::Parser->new();

	my $doc = $xml_parser->parse($result) or die "Unable to parse document";
	my $flag = 0;
	my @prj_array;
	my $text1;
	my $text2;

	foreach my $node($doc->getElementsByTagName("nmwg:parameter"))
	{ 
		$flag = 0;
		$text1 = $node->getAttribute("value");
		$text2 = chomp($text1);
		my $size_array = @project_list;
		if ($size_array > 0)
		{
			foreach my $element(@project_list)
			{
				if ($element eq $text1)
				{
					$flag = 1;	
				}
			}
		}

		if ($flag eq 0)
		{
			@prj_array = split(":",$text1);
			if ($prj_array[0] eq "project")
			{
				push(@project_list,$node->getAttribute("value"));
			}
		}


	}

	return @project_list;

}




sub initiate_gls
{

	my $gLs;

	($gLs) = @_;
	
	if($gLs eq "")
	{
	$gLs = 'http://ps4.es.net:9990/perfSONAR_PS/services/gLS';
	}
	
	my $glsClient = new perfSONAR_PS::Client::LS
	(
		{
			instance => $gLs
		}
	)  or die "Invalid Global Lookup Service address";
	print $gLs;
	return $glsClient;
}

sub query_to_gls
{

	($glsClient,$query_keyword) = @_;

	my $gLSResult = $glsClient->queryRequestLS(
		{
		    query => $query_keyword,
		    format => 1 #want response to be formated as XML
		}
	);

	return $gLSResult->{response};

}

sub get_hls_sitelist
{
	my $sitename;

	($sitename) = @_;
	my $hLSXquery = "declare namespace nmwg=\"http://ggf.org/ns/nmwg/base/2.0/\";\n";
	$hLSXquery .= "declare namespace perfsonar=\"http://ggf.org/ns/nmwg/tools/org/perfsonar/1.0/\";\n";
	$hLSXquery .= "declare namespace psservice=\"http://ggf.org/ns/nmwg/tools/org/perfsonar/service/1.0/\";\n";
	$hLSXquery .= "declare namespace nmtb=\"http://ogf.org/schema/network/base/20070828/\";\n";
	$hLSXquery .= "for \$metadata in /nmwg:store[\@type=\"LSStore\"]/nmwg:metadata\n";
	$hLSXquery .= "    let \$metadata_id := \$metadata/\@id  \n";
	$hLSXquery .= "    let \$data := /nmwg:store[\@type=\"LSStore\"]/nmwg:data[\@metadataIdRef=\$metadata_id]\n";
	$hLSXquery .= "    let \$keyword := \$data/nmwg:metadata/nmwg:parameters/nmwg:parameter[\@name=\"keyword\"]";
	$hLSXquery .= "    where \$metadata/perfsonar:subject/nmtb:service/nmtb:type=\"bwctl\" and (\$keyword=\"$sitename\")";

	$hLSXquery .= "    return \$metadata/perfsonar:subject/nmtb:service/nmtb:address";
	return $hLSXquery;
}

sub get_gls_keyword
{

	my $xls_global_query_lookup = "declare namespace nmwg=\"http://ggf.org/ns/nmwg/base/2.0/\";\n";
	$xls_global_query_lookup .= "/nmwg:store[\@type=\"LSStore\"]/nmwg:data/nmwg:metadata/summary:parameters/nmwg:parameter[\@name=\"keyword\"]";
	return $xls_global_query_lookup;
}

sub get_gls_sitelist
{
	my $sitename;

	($sitename) = @_;

	my $gLSXquery = "declare namespace nmwg=\"http://ggf.org/ns/nmwg/base/2.0/\";\n";
	$gLSXquery .= "declare namespace perfsonar=\"http://ggf.org/ns/nmwg/tools/org/perfsonar/1.0/\";\n";
	$gLSXquery .= "declare namespace psservice=\"http://ggf.org/ns/nmwg/tools/org/perfsonar/service/1.0/\";\n";
	$gLSXquery .= "declare namespace summary=\"http://ggf.org/ns/nmwg/tools/org/perfsonar/service/lookup/summarization/2.0/\";\n";
	$gLSXquery .= "for \$metadata in /nmwg:store[\@type=\"LSStore\"]/nmwg:metadata\n";
	$gLSXquery .= "    let \$metadata_id := \$metadata/\@id  \n";
	$gLSXquery .= "    let \$data := /nmwg:store[\@type=\"LSStore\"]/nmwg:data[\@metadataIdRef=\$metadata_id]\n";
	$gLSXquery .= "    let \$keyword := \$data/nmwg:metadata/summary:parameters/nmwg:parameter[\@name=\"keyword\"]/\@value\n ";
	$gLSXquery .= "    let \$eventTypeParam := \$data/nmwg:metadata/summary:parameters/nmwg:parameter[\@name=\"eventType\"]/\@value\n ";
	$gLSXquery .= "    where (\$metadata/perfsonar:subject/psservice:service/psservice:serviceType=\"ls\" or ";
	$gLSXquery .= "       \$metadata/perfsonar:subject/psservice:service/psservice:serviceType=\"hLS\") and ";
	$gLSXquery .= "        (\$eventTypeParam=\"http://ggf.org/ns/nmwg/tools/bwctl/1.0\")";
	$gLSXquery .= "        and (\$keyword=\"$sitename\")";
	$gLSXquery .= "    return \$metadata/perfsonar:subject/psservice:service/psservice:accessPoint";
	return $gLSXquery;

}

sub get_hls_sitelist
{
	my $sitename;

	($sitename) = @_;
	my $hLSXquery = "declare namespace nmwg=\"http://ggf.org/ns/nmwg/base/2.0/\";\n";
	$hLSXquery .= "declare namespace perfsonar=\"http://ggf.org/ns/nmwg/tools/org/perfsonar/1.0/\";\n";
	$hLSXquery .= "declare namespace psservice=\"http://ggf.org/ns/nmwg/tools/org/perfsonar/service/1.0/\";\n";
	$hLSXquery .= "declare namespace nmtb=\"http://ogf.org/schema/network/base/20070828/\";\n";
	$hLSXquery .= "for \$metadata in /nmwg:store[\@type=\"LSStore\"]/nmwg:metadata\n";
	$hLSXquery .= "    let \$metadata_id := \$metadata/\@id  \n";
	$hLSXquery .= "    let \$data := /nmwg:store[\@type=\"LSStore\"]/nmwg:data[\@metadataIdRef=\$metadata_id]\n";
	$hLSXquery .= "    let \$keyword := \$data/nmwg:metadata/nmwg:parameters/nmwg:parameter[\@name=\"keyword\"]";
	$hLSXquery .= "    where \$metadata/perfsonar:subject/nmtb:service/nmtb:type=\"bwctl\" and (\$keyword=\"$sitename\")";

	$hLSXquery .= "    return \$metadata/perfsonar:subject/nmtb:service/nmtb:address";
	return $hLSXquery;


}





1;