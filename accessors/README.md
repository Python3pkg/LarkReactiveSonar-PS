INTRODUCTION 

This python wrapper module contains a mechanisms for interacting with the
HTCondor system and perfSonar client libraries.

BUILDING



USAGE


PerfSonarAccessor usage

[akoerner]$ python

>>> import PerfSonarAccessor

Once the PerfSonarAccessor is imported it can be instantiated.
The following is an example of the default configuration:

>>> perfSonarAccessor = PerfSonarAccessor.PerfSonarAccessor()

The default project is "Internet2" and the default Global Lookup Service is "ps4.es.net:9990". In the default configureation one of two thing is done. First the project list for "ps4.es.net:9990/perfSONAR_PS/services/gLS" if fetched. Next, this project site list for "Internet2" is fetched at the global lookup service.

The PerfSonarAccessor can also be instantiated specifying a Project name and Global Lookup Service. The first argument of the constructor is the project followed by the global lookup service. The following is an example of instantiating the PerfSonarAccessor specifying the project and global lookup service:

>>> perfSonarAccessor = PerfSonarAccessor.PerfSonarAccessor("Wisconsin", "ps4.es.net:9990/perfSONAR_PS/services/gLS")

The PerfSonarAccessor can also be instantiated specifying only a Project name. If only a project name is given then the Global Lookup Service used to fetch project information is "ps4.es.net:9990/perfSONAR_PS/services/gLS". The following is an example of instantiating the PerfSonarAccessor with only a project name:

>>> perfSonarAccessor = PerfSonarAccessor.PerfSonarAccessor("Wisconsin");

Once initialized the project site list and global lookup service project list will be available The following is an example of the global lookup service project list for "ps4.es.net:9990/perfSONAR_PS/services/gLS":

>>> perfSonarAccessor.getProjectList()

['SUNET', 'PoP-SC/RNP', 'GT-Mediciones-CLARA-RAAP-UNI', 'LHCTier1', 'WLCG', 'NOAA', 'Atlas', 'USCMS', 'LONI', 'CENIC', 'Internet2', 'RedCLARA', 'UFSC', 'perfSONAR', 'UCInet', 'HEPnet-Canada', 'Blue Waters', 'uhnet', 'UT Austin TACC', 'GPN', 'LHC', 'INFN', 'ALICE', 'APAN-JP', 'perfSONAR_KVN', 'Fermilab', 'MCNC', 'PoP-SC', 'CalREN', 'MAX', 'ICCN', 'ESNet', 'Sailor', 'pS-NPToolkit-3.2.1', 'pS-NPToolkit-3.2.2', 'NRC-CNRC', 'SANReN', 'Viawest', 'MSUperfTest', 'PERN2', 'ESnet', 'TWAREN', 'LHCTier2', 'GridPP', 'CMS', 'PSU-EMS', 'IllinoisNet', 'Wisconsin', 'internet2', 'XSEDE', 'Purdue', 'LSU', 'GAMMON', 'MWT2', 'OmniPOP', 'public', 'University of Minnesota', 'FIBRE', 'ATLASIT', 'CANARIE', 'TransPAC', 'SHI', 'ConnecticutEducationNetwork', 'NCHC', 'Cenic', 'pS-NPToolkit-3.2', 'geant', 'UTSystem', 'SDSC', 'NCREN', 'UNC-CH', 'GT-Mediciones-CLARA', 'NOX', 'UCSD', 'uark', 'FIBRE-BR', 'RNP', 'sdc-hosting', 'PSU', 'NgREN', 'uci-oit-netops', 'USATLAS', 'Utah Univ-of-Utah/UEN', 'KDL', 'ORAU', 'IGTMD', 'AARNet', 'NERSC', 'DOE Sites', 'DOE-SC-LAB', 'NLR', 'JGN-X', 'CNRS', 'DES', 'Atmospheric', 'AREON', 'CalREN-HPR', 'NORDUnet', 'SCinet', 'esnet', 'perfSONAR-PS', 'OSHEAN', 'ASUNet', 'PennState', 'Northern-Lights', 'Funet', 'upenn', 'zelab_ro', 'ThaiREN', 'LHCONE', 'University of Alaska', 'POP-SC', 'NRNet-II', 'TLPW', 'ATALAS', 'LEARN', 'ATLAS', 'Univ-of-Utah/UEN', 'StarLight', 'Utah', 'RENATER', 'LHCb', 'ACORN', 'SOX', 'Main-Campus', 'FRGP', 'MREN', 'GEANT', 'MaineREN', 'REANNZ', 'AGLT2', 'Internet 2', 'LHCOPN', 'IN2P3', 'KREONET', 'SDSC-Colo', 'Florida LambdaRail', 'UCR', 'Ecenter', 'Univ. of Michigan', 'Connecticut Education Network', 'Merit', 'KanREN', 'GIGA', 'NCSA']
The following is an example of the project site list for "Wisconsin":

>>> perfSonarAccessor.getProjectSiteList()

['perfsonar02.hep.wisc.edu', 'larkps.chtc.wisc.edu', 'larkps.chtc.wisc.edu', 'perfsonar02.discovery.wisc.edu', 'hcc-ps02.unl.edu']
The global lookup service can be changed at any time by the following:

>>> perfSonarAccessor.setGlobalLookupService("ps4.es.net:9990/perfSONAR_PS/services/gLS")

Once the global lookup service is changed the project list must be externally fetched and then a project must be set. The following is an example of fetching the project list for the changed global looukup service and then setting the project:

>>> perfSonarAccessor.fetchProjectList() If the project name is already known this step can be skipped

>>> perfSonarAccessor.setProjectName("Wisconsin")

Project names are case sensitive and must be identical to how they are indexed in the Global Lookup Service e.g., "Internet 2" != "Internet2". Once a project is set the site list for the project must be fetched at the Global Lookup Service. The following is an example of fetching the project site list:

>>> perfSonarAccessor.fetchProjectSiteList() If the site associated with the set project is already known this step can be skipped

After the project site list has been set it can be retrieved by the following:

>>> perfSonarAccessor.getProjectSiteList()

['perfsonar02.hep.wisc.edu', 'larkps.chtc.wisc.edu', 'larkps.chtc.wisc.edu', 'perfsonar02.discovery.wisc.edu', 'hcc-ps02.unl.edu']
After a project has been set and the associated site list has been fetched sites can be queried for throughput data. To do this a site must be set and then the endpoint pair list must be fetched. The following is and example of setting a site and fetching the associated endpoint pair list. For the project "Wisconsin" there is a site "hcc-ps02.unl.edu":

>>> perfSonarAccessor.setCurrentSite("hcc-ps02.unl.edu")

The current site can be viewed at any time by the following:

>>> perfSonarAccessor.getCurrentSite()

hcc-ps02.unl.edu
Once the site is set then the endpoint pair list for the site must be fetched. This can be done by the following:

>>> perfSonarAccessor.fetchSiteEndPointPairList() If the endpoints of interest associated with the current site are already known this can be skipped

Here is an example of the endpoint pair list fetched for the site "hcc-ps02.unl.edu":

>>> perfSonarAccessor.getSiteEndPointPairList()

[{'source': 'hcc-ps02.unl.edu', 'destination': 'perfsonar-bw.farm.particle.cz'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'perfsonar-ps-02.desy.de'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'perfsonar-1.t2.ucsd.edu'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'psum02.aglt2.org'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'perfsonar02.hep.wisc.edu'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'perfsonar.rcac.purdue.edu'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'cmsperfsonar01.fnal.gov'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'perfsonar2.ihepa.ufl.edu'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'perfsonar-ps.cern.ch'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'ps-bandwidth.lhcopn-mon.triumf.ca'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'psonar2.lal.in2p3.fr'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'perfsonar.caltech.edu'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'ps-bandwidth.scinet.utoronto.ca'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'perfsonar.na.infn.it'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'lynnperf.itns.purdue.edu'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'perfsonar-bw.sprace.org.br'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'psndt2.accre.vanderbilt.edu'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'psmsu02.aglt2.org'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'larkps.chtc.wisc.edu'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'perfsonar.ihepa.ufl.edu'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'perfsonar2.icepp.jp'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'mannperf2.itns.purdue.edu'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'lhc-bandwidth.twgrid.org'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'perfsonar-ps-bandwidth.pic.es'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'perfsonar.hep.caltech.edu'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'perfsonar.ultralight.org'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'perfsonar-bw.hepgrid.uerj.br'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'perfsonar02.cmsaf.mit.edu'}, {'source': 'hcc-ps02.unl.edu', 'destination': 'lhcmon.bnl.gov'}, {'source': 'perfsonar-bw.farm.particle.cz', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'perfsonar-bw.farm.particle.cz', 'destination': '129.93.239.163'}, {'source': 'perfsonar-ps-02.desy.de', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'perfsonar-ps-02.desy.de', 'destination': '129.93.239.163'}, {'source': 'perfsonar-1.t2.ucsd.edu', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'perfsonar-1.t2.ucsd.edu', 'destination': '129.93.239.163'}, {'source': 'psum02.aglt2.org', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'psum02.aglt2.org', 'destination': '129.93.239.163'}, {'source': 'perfsonar02.hep.wisc.edu', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'perfsonar02.hep.wisc.edu', 'destination': '129.93.239.163'}, {'source': 'perfsonar.rcac.purdue.edu', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'cmsperfsonar01.fnal.gov', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'cmsperfsonar01.fnal.gov', 'destination': '129.93.239.163'}, {'source': 'perfsonar2.ihepa.ufl.edu', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'perfsonar2.ihepa.ufl.edu', 'destination': '129.93.239.163'}, {'source': 'perfsonar-ps.cern.ch', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'perfsonar-ps.cern.ch', 'destination': '129.93.239.163'}, {'source': 'ps-bandwidth.lhcopn-mon.triumf.ca', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'ps-bandwidth.lhcopn-mon.triumf.ca', 'destination': '129.93.239.163'}, {'source': 'psonar2.lal.in2p3.fr', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'perfsonar.caltech.edu', 'destination': 'hcc-ps02.unl.edu'}, {'source': '129.93.239.163', 'destination': 'perfsonar-ps-02.desy.de'}, {'source': '129.93.239.163', 'destination': 'perfsonar-1.t2.ucsd.edu'}, {'source': '129.93.239.163', 'destination': 'psum02.aglt2.org'}, {'source': '129.93.239.163', 'destination': 'perfsonar02.hep.wisc.edu'}, {'source': '129.93.239.163', 'destination': 'cmsperfsonar01.fnal.gov'}, {'source': '129.93.239.163', 'destination': 'perfsonar2.ihepa.ufl.edu'}, {'source': '129.93.239.163', 'destination': 'perfsonar-ps.cern.ch'}, {'source': '129.93.239.163', 'destination': 'ps-bandwidth.lhcopn-mon.triumf.ca'}, {'source': '129.93.239.163', 'destination': 'psonar2.lal.in2p3.fr'}, {'source': '129.93.239.163', 'destination': 'ps-bandwidth.scinet.utoronto.ca'}, {'source': '129.93.239.163', 'destination': 'perfsonar.na.infn.it'}, {'source': '129.93.239.163', 'destination': 'perfsonar-bw.sprace.org.br'}, {'source': '129.93.239.163', 'destination': 'psmsu02.aglt2.org'}, {'source': '129.93.239.163', 'destination': 'psndt2.accre.vanderbilt.edu'}, {'source': '129.93.239.163', 'destination': 'perfsonar2.icepp.jp'}, {'source': '129.93.239.163', 'destination': 'mannperf2.itns.purdue.edu'}, {'source': '129.93.239.163', 'destination': 'lhc-bandwidth.twgrid.org'}, {'source': '129.93.239.163', 'destination': 'perfsonar-ps-bandwidth.pic.es'}, {'source': '129.93.239.163', 'destination': 'perfsonar.ultralight.org'}, {'source': '129.93.239.163', 'destination': 'perfsonar02.cmsaf.mit.edu'}, {'source': '129.93.239.163', 'destination': 'lhcmon.bnl.gov'}, {'source': '2600:901::1124', 'destination': 'larkps.chtc.wisc.edu'}, {'source': 'ps-bandwidth.scinet.utoronto.ca', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'ps-bandwidth.scinet.utoronto.ca', 'destination': '129.93.239.163'}, {'source': 'perfsonar.na.infn.it', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'perfsonar.na.infn.it', 'destination': '129.93.239.163'}, {'source': 'lynnperf.itns.purdue.edu', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'perfsonar-bw.sprace.org.br', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'perfsonar-bw.sprace.org.br', 'destination': '129.93.239.163'}, {'source': 'psndt2.accre.vanderbilt.edu', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'psndt2.accre.vanderbilt.edu', 'destination': '129.93.239.163'}, {'source': 'psmsu02.aglt2.org', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'psmsu02.aglt2.org', 'destination': '129.93.239.163'}, {'source': 'larkps.chtc.wisc.edu', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'larkps.chtc.wisc.edu', 'destination': '2600:901::1124'}, {'source': 'perfsonar.ihepa.ufl.edu', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'perfsonar2.icepp.jp', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'perfsonar2.icepp.jp', 'destination': '129.93.239.163'}, {'source': 'mannperf2.itns.purdue.edu', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'mannperf2.itns.purdue.edu', 'destination': '129.93.239.163'}, {'source': 'lhc-bandwidth.twgrid.org', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'lhc-bandwidth.twgrid.org', 'destination': '129.93.239.163'}, {'source': 'perfsonar.hep.caltech.edu', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'perfsonar-ps-bandwidth.pic.es', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'perfsonar-ps-bandwidth.pic.es', 'destination': '129.93.239.163'}, {'source': 'perfsonar.ultralight.org', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'perfsonar-bw.hepgrid.uerj.br', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'perfsonar02.cmsaf.mit.edu', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'perfsonar02.cmsaf.mit.edu', 'destination': '129.93.239.163'}, {'source': 'lhcmon.bnl.gov', 'destination': 'hcc-ps02.unl.edu'}, {'source': 'lhcmon.bnl.gov', 'destination': '129.93.239.163'}]
Once a site has been set and and endpoint pair list has been fetch for the site verious endpoints can be interrogated for throughput data. Here is an example of the following endpoint pair being interrogated 'source': 'hcc-ps02.unl.edu', 'destination': 'perfsonar02.hep.wisc.edu':

>>> perfSonarAccessor.fetchThroughputResults("hcc-ps02.unl.edu", "perfsonar02.hep.wisc.edu")

fetchThroughputResults accepts three arguments: source address, destination address and how many seconds in the past to fetch throughput data for. The previous example is the default configuration with no seconds in the past specified. If no seconds in the past are specified then throughput data for the last hour or last 3600 seconds will be fetched. Here is an example of specifying throughput data for source = 'hcc-ps02.unl.edu' and destination = 'perfsonar02.hep.wisc.edu' for two hours or 7200 seconds in the past:

>>> perfSonarAccessor.fetchThroughputResults("hcc-ps02.unl.edu", "perfsonar02.hep.wisc.edu", 7200)

After a site has been queried for throughput data for a source and destination pair the data can be obtained by calling getCurrentThroughputResults(). The following throughput results is an example of throughput data between "hcc-ps02.unl.edu" and "perfsonar02.hep.wisc.edu" for the last two hours:

>>> perfSonarAccessor.getCurrentThroughputResults()

[{'throughput': '9.24389e+07'}]
PerfSonarAccessor things to note

Every time fetch is called there is a latency overhead associated. If a project name is known there is no reason to fetch the project list. If a site is known there is no reason to fetch the site list. The associated set methods can be called to set known values i.e., setGlobalLookupService, setProjectName, setCurrentSite.

For extended documentation and the project WIKI visit:

https://github.com/akoerner/LarkReactiveSonar-PS/wiki/_pages

For PYDOCs visit:

http://akoerner.github.io/LarkReactiveSonar-PS/pydocs/accessors/PerfSonarAccessor.html
