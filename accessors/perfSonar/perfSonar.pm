#!/usr/bin/perl


use lib "../../lib";

require perfSonar;
use threads;
use perfSONAR_PS::Client::LS;
use perfSONAR_PS::Client::MA;
use XML::LibXML;
use XML::Twig;
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

	for(my $i = 0; $i < $hLSList->size(); $i++)
	{ 
		my $hLSUrl =  $hLSList->get_node($i)->string_value();

		my $hlsClient = new perfSONAR_PS::Client::LS(
		{
		instance => $hLSUrl
		}
		);
		my $hLSResult = $hlsClient->queryRequestLS(
		{
		query => $xls_hls_sitelist,
		format => 1
		}
		);

		my $resParser = XML::LibXML->new();

		if($hLSResult->{response} && $hLSResult->{response} =~ /^</)
		{

			my $hLSDoc = $resParser->parse_string($hLSResult->{response});
			my $bwctlList = find($hLSDoc->getDocumentElement, "./*[local-name()='address']", 0);
			for(my $j = 0; $j < $bwctlList->size(); $j++)
			{
				my $output = $bwctlList->get_node($j)->string_value();
				my $find = "tcp://";
				my $replace = "";
				$find = quotemeta $find;
				$output =~ s/$find/$replace/g;
				$find = ":4823";
				$output =~ s/$find/$replace/g;
				
				$find = "http://";
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
		return;
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

sub get_ls_endpoint_pair
{

	($site, $start_timestamp, $end_timestamp) = @_;
	
	my $array_size = 0;
	my @tmp_src_dst;
	my @metadata_files;
	my $src_dst_pair;

	my @src = ();
	my @dst = ();
	my $count = 0;
	my $flag_src_dst;

	my $xls_pairlist = get_xls_pairlist();

	my $data_sitename = $site;

	my $data_http_name = "http://" . $site . ":8085/perfSONAR_PS/services/pSB ";

	# Set eventType
	my @eventTypes = ('http://ggf.org/ns/nmwg/tools/iperf/2.0');

	my $is_data_empty = 0;

	my $ma = new perfSONAR_PS::Client::MA( { instance => "$data_http_name" } );

	# Send request
	my $result = $ma->setupDataRequest(
	{
	subject    => $xls_pairlist,
	eventTypes => \@eventTypes,
	start      => $start_timestamp,
	end        => $end_timestamp,
	}
	); 
	
	my $parser = XML::LibXML->new();
	my $twig= XML::Twig->new(pretty_print => 'indented');
	$resultString = "";
	foreach $metadata(@{$result->{"metadata"}})
	{
		$twig->parse($metadata);
		
		$resultString .= $twig->sprint;
	}
	
	$resultString = "<data>\n".$resultString."\n</data>";


	
	my $parser = XML::LibXML->new();
	
	my $doc = $parser->parse_string($resultString);

	@tmp_src_dst = ();

	foreach my $node($doc->getElementsByTagName("nmwg:metadata"))
	{


		push(@metadata_files,$node->getAttribute("id"));


		foreach my $tnode($node->getElementsByTagName("nmwgt:src"))
		{

			$src[$count] = $tnode->getAttribute("value");
		}

		foreach my $tnode($node->getElementsByTagName("nmwgt:dst"))
		{
			$dst[$count] = $tnode->getAttribute("value");
		}
	
		print $src[$count] . " " . $dst[$count++]."\n";

	}
}

sub get_one_way_latency_for_last_day
{

	($site, $source, $destination) = @_;
    
    print "QUERY: site:".$site." src:".$source." des:".$destination;
	my $resource = ":8085/perfSONAR_PS/services/pSB";

	my $ma = new perfSONAR_PS::Client::MA( { instance => "http://".$site.$resource } );

	my $subject = "<owamp:subject xmlns:owamp=\"http://ggf.org/ns/nmwg/tools/owamp/2.0/\" id=\"subject\">\n";
	$subject .=   "    <nmwgt:endPointPair xmlns:nmwgt=\"http://ggf.org/ns/nmwg/topology/2.0/\">";
	$subject .=   "        <nmwgt:src type=\"ipv4\" value=\"$source\"/>";
	$subject .=   "        <nmwgt:dst type=\"ipv4\" value=\"$destination\"/>";
	$subject .=   "    </nmwgt:endPointPair>";
	$subject .=   "</owamp:subject>\n";

	my @eventTypes = ();

	# Set time range
	my $end = time;
	my $start = $end - 24*3600; #1 day ago

	# Send the request
	my $result = $ma->setupDataRequest(
			{
				subject    => $subject,
				eventTypes => \@eventTypes,
				start      => $start,
				end        => $end,
			}
		);


	my $twig= XML::Twig->new(pretty_print => 'indented');
	foreach $metadata(@{$result->{"metadata"}}){
		$twig->parse($metadata);
		$twig->print();
	}
	foreach $data(@{$result->{"data"}}){
		$twig->parse($data);
		$twig->print();
	}
}

sub get_throughput_results{

	($site, $source, $destination, $secondsAgo) = @_;

	print $source
	print $destination
	
	
my $resource = ":8085/perfSONAR_PS/services/pSB";

# Create client
my $ma = new perfSONAR_PS::Client::MA( { instance => "http://".$site.$resource } );

# Define subject
my $subject = "<iperf:subject xmlns:iperf=\"http://ggf.org/ns/nmwg/tools/iperf/2.0\" id=\"subject\">\n";
$subject .=   "    <nmwgt:endPointPair xmlns:nmwgt=\"http://ggf.org/ns/nmwg/topology/2.0/\">";
$subject .=   "        <nmwgt:src type=\"hostname\" value=\"".$source."\"/>";
$subject .=   "        <nmwgt:dst type=\"hostname\" value=\"".$destination."\"/>";
$subject .=   "    </nmwgt:endPointPair>";
$subject .=   "</iperf:subject>\n";

# Set eventType
my @eventTypes = ();

# Set time range
my $end = time;
my $start = $end - $secondsAgo;

# Send request
my $result = $ma->setupDataRequest(
        {
            subject    => $subject,
            eventTypes => \@eventTypes,
            start      => $start,
            end        => $end,
        }
    );

#Output XML
my $parser = XML::LibXML->new();

my $twig= XML::Twig->new(pretty_print => 'indented');
foreach $metadata(@{$result->{"metadata"}}){
	$twig->parse($metadata);
	#SS$twig->print();
}
foreach $data(@{$result->{"data"}}){
	#print $data;
	my $doc = $parser->parse_string($data);
	
	foreach my $node($doc->getElementsByTagName("iperf:datum"))
	{
		print $node->getAttribute("throughput");
		print "\n";
	}
	#$twig->parse($data);
	#$twig->print();
}

#$result = "<data>\n".$result."\n</data>";

#my $doc = $parser->parse_string($result);
#print $doc;

#foreach my $node($doc->getElementsByTagName("nmwg:data"))
#	{

#		print "tag".$node;
		
#}


}

sub initiate_gls
{

	my $gLs;

	($gLs) = @_;

	if($gLs==1 || $gLs == '')
	{
	
		$gLs = 'http://ps1.es.net:9990/perfSONAR_PS/services/gLS';
	}
	
	my $glsClient = new perfSONAR_PS::Client::LS
	(
		{
			instance => $gLs
		}
	)  or die "Invalid Global Lookup Service address";
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

sub get_xls_pairlist
{
	my $subject = "<iperf:subject xmlns:iperf=\"http://ggf.org/ns/nmwg/tools/iperf/2.0\" id=\"subject\">\n";
	$subject .=   "    <nmwgt:endPointPair xmlns:nmwgt=\"http://ggf.org/ns/nmwg/topology/2.0/\" />\n";
	$subject .=   "</iperf:subject>\n";

	return $subject;

}





1;