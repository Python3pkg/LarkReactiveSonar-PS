
#PASTOR: Code generated by XML::Pastor/1.0.3 at 'Wed Jul  1 15:32:04 2009'

use utf8;
use strict;
use warnings;
no warnings qw(uninitialized);

use XML::Pastor;



#================================================================

package OSCARS::ns002::Type::CtrlPlaneTopologyContent;

use OSCARS::ns002::Type::CtrlPlaneDomainContent;
use OSCARS::ns002::Type::CtrlPlaneDomainSignatureContent;
use OSCARS::ns002::Type::CtrlPlanePathContent;
use OSCARS::ns002::domain;
use OSCARS::ns002::path;

our @ISA=qw(XML::Pastor::ComplexType);

OSCARS::ns002::Type::CtrlPlaneTopologyContent->mk_accessors( qw(_id idcId path domain domainSignature));

# Attribute accessor aliases

sub id { &_id; }

OSCARS::ns002::Type::CtrlPlaneTopologyContent->XmlSchemaType( bless( {
                 'attributeInfo' => {
                                    'id' => bless( {
                                                   'class' => 'XML::Pastor::Builtin::string',
                                                   'metaClass' => 'OSCARS::Pastor::Meta',
                                                   'name' => 'id',
                                                   'scope' => 'local',
                                                   'targetNamespace' => 'http://ogf.org/schema/network/topology/ctrlPlane/20080828/',
                                                   'type' => 'string|http://www.w3.org/2001/XMLSchema',
                                                   'use' => 'required'
                                                 }, 'XML::Pastor::Schema::Attribute' )
                                  },
                 'attributePrefix' => '_',
                 'attributes' => [
                                   'id'
                                 ],
                 'baseClasses' => [
                                    'XML::Pastor::ComplexType'
                                  ],
                 'class' => 'OSCARS::ns002::Type::CtrlPlaneTopologyContent',
                 'contentType' => 'complex',
                 'elementInfo' => {
                                  'domain' => bless( {
                                                     'class' => 'OSCARS::ns002::Type::CtrlPlaneDomainContent',
                                                     'definition' => bless( {
                                                                              'baseClasses' => [
                                                                                                 'OSCARS::ns002::Type::CtrlPlaneDomainContent',
                                                                                                 'XML::Pastor::Element'
                                                                                               ],
                                                                              'class' => 'OSCARS::ns002::domain',
                                                                              'isRedefinable' => 1,
                                                                              'metaClass' => 'OSCARS::Pastor::Meta',
                                                                              'name' => 'domain',
                                                                              'scope' => 'global',
                                                                              'targetNamespace' => 'http://ogf.org/schema/network/topology/ctrlPlane/20080828/',
                                                                              'type' => 'CtrlPlaneDomainContent|http://ogf.org/schema/network/topology/ctrlPlane/20080828/'
                                                                            }, 'XML::Pastor::Schema::Element' ),
                                                     'maxOccurs' => 'unbounded',
                                                     'metaClass' => 'OSCARS::Pastor::Meta',
                                                     'minOccurs' => '0',
                                                     'name' => 'domain',
                                                     'nameIsAutoGenerated' => 1,
                                                     'ref' => 'domain|http://ogf.org/schema/network/topology/ctrlPlane/20080828/',
                                                     'scope' => 'local',
                                                     'targetNamespace' => 'http://ogf.org/schema/network/topology/ctrlPlane/20080828/'
                                                   }, 'XML::Pastor::Schema::Element' ),
                                  'domainSignature' => bless( {
                                                              'class' => 'OSCARS::ns002::Type::CtrlPlaneDomainSignatureContent',
                                                              'maxOccurs' => 'unbounded',
                                                              'metaClass' => 'OSCARS::Pastor::Meta',
                                                              'minOccurs' => '0',
                                                              'name' => 'domainSignature',
                                                              'scope' => 'local',
                                                              'targetNamespace' => 'http://ogf.org/schema/network/topology/ctrlPlane/20080828/',
                                                              'type' => 'CtrlPlaneDomainSignatureContent|http://ogf.org/schema/network/topology/ctrlPlane/20080828/'
                                                            }, 'XML::Pastor::Schema::Element' ),
                                  'idcId' => bless( {
                                                    'class' => 'XML::Pastor::Builtin::string',
                                                    'metaClass' => 'OSCARS::Pastor::Meta',
                                                    'name' => 'idcId',
                                                    'scope' => 'local',
                                                    'targetNamespace' => 'http://ogf.org/schema/network/topology/ctrlPlane/20080828/',
                                                    'type' => 'string|http://www.w3.org/2001/XMLSchema'
                                                  }, 'XML::Pastor::Schema::Element' ),
                                  'path' => bless( {
                                                   'class' => 'OSCARS::ns002::Type::CtrlPlanePathContent',
                                                   'definition' => bless( {
                                                                            'baseClasses' => [
                                                                                               'OSCARS::ns002::Type::CtrlPlanePathContent',
                                                                                               'XML::Pastor::Element'
                                                                                             ],
                                                                            'class' => 'OSCARS::ns002::path',
                                                                            'isRedefinable' => 1,
                                                                            'metaClass' => 'OSCARS::Pastor::Meta',
                                                                            'name' => 'path',
                                                                            'scope' => 'global',
                                                                            'targetNamespace' => 'http://ogf.org/schema/network/topology/ctrlPlane/20080828/',
                                                                            'type' => 'CtrlPlanePathContent|http://ogf.org/schema/network/topology/ctrlPlane/20080828/'
                                                                          }, 'XML::Pastor::Schema::Element' ),
                                                   'maxOccurs' => 'unbounded',
                                                   'metaClass' => 'OSCARS::Pastor::Meta',
                                                   'minOccurs' => '0',
                                                   'name' => 'path',
                                                   'nameIsAutoGenerated' => 1,
                                                   'ref' => 'path|http://ogf.org/schema/network/topology/ctrlPlane/20080828/',
                                                   'scope' => 'local',
                                                   'targetNamespace' => 'http://ogf.org/schema/network/topology/ctrlPlane/20080828/'
                                                 }, 'XML::Pastor::Schema::Element' )
                                },
                 'elements' => [
                                 'idcId',
                                 'path',
                                 'domain',
                                 'domainSignature'
                               ],
                 'isRedefinable' => 1,
                 'metaClass' => 'OSCARS::Pastor::Meta',
                 'name' => 'CtrlPlaneTopologyContent',
                 'scope' => 'global',
                 'targetNamespace' => 'http://ogf.org/schema/network/topology/ctrlPlane/20080828/'
               }, 'XML::Pastor::Schema::ComplexType' ) );

1;


__END__



=head1 NAME

B<OSCARS::ns002::Type::CtrlPlaneTopologyContent>  -  A class generated by L<XML::Pastor> . 


=head1 ISA

This class descends from L<XML::Pastor::ComplexType>.


=head1 CODE GENERATION

This module was automatically generated by L<XML::Pastor> version 1.0.3 at 'Wed Jul  1 15:32:04 2009'


=head1 ATTRIBUTE ACCESSORS

=over

=item B<_id>(), B<id>()      - See L<XML::Pastor::Builtin::string>.

=back


=head1 CHILD ELEMENT ACCESSORS

=over

=item B<domain>()      - See L<OSCARS::ns002::Type::CtrlPlaneDomainContent>.

=item B<domainSignature>()      - See L<OSCARS::ns002::Type::CtrlPlaneDomainSignatureContent>.

=item B<idcId>()      - See L<XML::Pastor::Builtin::string>.

=item B<path>()      - See L<OSCARS::ns002::Type::CtrlPlanePathContent>.

=back


=head1 SEE ALSO

L<XML::Pastor::ComplexType>, L<XML::Pastor>, L<XML::Pastor::Type>, L<XML::Pastor::ComplexType>, L<XML::Pastor::SimpleType>


=cut
