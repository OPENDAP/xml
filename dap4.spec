<!DOCTYPE html>
<!-- Copyright 2012, UCAR/Unidata -->
<!-- See the COPYRIGHT file for more information. -->
<!-- When inserting text, AVOID the following situations: -->
<!-- * multiple occurrences of <a href=...> on a single line. -->
<!-- * <a ...> and the closing </a> on different lines. -->

<style type="text/css">
<!-- Global -->
.break { page-break-before: always; }
.center { text-align: center; }
.section { font-size: 12pt; }
.appendix { font-size: 12pt; }
.title { font-size: 18pt; font-style: bold; text-align: center; margin-top: 0pt; }
body { font-size: 12pt; }
h1 { font-size: 16pt; }
div.tocbegin { }
div.tocend { }
h1.section { font-size: 14pt; }
h1.appendix { font-size: 14pt;}
h1.toc {font-size: 16pt; margin-bottom: 0pt; padding: 0pt; }
h1.abstract { font-size: 18pt; font-style: italic; font-weight: bold; text-align: center; }
p.italic {font-style:italic}

</style>

<title>DAP4 Specification</title>

<html>
<body>
<h1 class="title">The Data Access Protocol: DAP Version 4.0</h1>
<h1 class="title">Volume 1: Data Model and Serialized Representation</h1>
<p>
<p>
<center>
<table border=1 width="85%">
<tr><td width="20%">Date:<td>May 31, 2012
<tr><td width="20%">Last Revised:<td>November 23, 2012
<tr><td width="20%">Status:<td>Draft
<tr><td width="20%">Authors:<td>John Caron (Unidata)
<tr><td width="20%"><td>Ethan Davis (Unidata)
<tr><td width="20%"><td>David Fulker (OPeNDAP)
<tr><td width="20%"><td>James Gallagher (OPeNDAP)
<tr><td width="20%"><td>Dennis Heimbigner (Unidata)
<tr><td width="20%"><td>Nathan Potter (OPeNDAP)
<tr><td width="20%">Copyright:<td>2012 University Corporation for Atmospheric Research and Opendap.org
</table>
</center>
<p>
<p>
<p>
<h1>Abstract</h1>
<p>
<i>This document defines the Data Access Protocol (DAP) version
4.0 (referred to also as DAP4). This data transmission
protocol is intended to supersede all previous versions of
the DAP protocol. DAP4 is designed specifically for science
data. The protocol relies on the widely used and stable
standards, and is capable of representing a wide variety of
scientific data types.</i>
<p>
Distribution of this document is unlimited.
<p>
This document takes material from the DAP2 specification and
the OPULS Wiki page.
<p>
DO NOT EDIT: This document was generated automatically from the
official DAP4 Specification Document.

<h1>Change List</h1>

<table border=1 width="85%">
<tr><td width="25%">2012.05.24:
    <td>Initial Draft
<tr><td width="25%">2012.05.27
    <td>Added specification of chunk order
<tr><td width="25%">2012.05.28
    <td>Added specification and interpretation of simple queries
<tr><td width="25%">2012.05.28
    <td>Added discussion about nested sequences.
<tr><td width="25%">2012.05.29
    <td>Formatting changes
<tr><td width="25%">2012.6.05
    <td>Removed serialized representation sections and constraint sections until James provides direction.
<tr><td width="25%">2012.6.24
    <td>Merge all changes from Gallagher, Potter, and Caron, except as noted.
<tr><td width="25%">2012.6.24
    <td>Removed all references to Sequences.
<tr><td width="25%">2012.6.24
    <td>Inserted James' version of serialized representation.
<tr><td width="25%">2012.6.25
    <td>Added DMR RELAX-NG Grammar.
<tr><td width="25%">2012.6.24
    <td>Added (semi-)formal description of the DAP4 serialization scheme.
<tr><td width="25%">2012.6.26
    <td>Added: (1) Revised Char type (2) Revised unlimited dimension rules (3) revised MAP rules. (4) Removed HTTP references
<tr><td width="25%">2012.7.09
    <td>Added discussion of identifier
<tr><td width="25%">2012.7.10
    <td>Added discussion of XML escaping
<tr><td width="25%">2012.7.10
    <td>Fix discrepancies between the formal definition of the on-th-wire format and the examples.
<tr><td width="25%">2012.7.12
    <td>Removed UByte and made Byte == UInt8
<tr><td width="25%">2012.8.21
    <td>Added draft constraints section
<tr><td width="25%">2012.8.25
    <td>Improved the discussion of named slices in constraints.
<tr><td width="25%">2012.9.4
    <td>Minor change to the grammar for simple constraints.
<tr><td width="25%">2012.9.6
    <td>Updated the Data Response section so that it no longer mentions Multipart MIME; edited the sections on FQNs and Attributes. I've added nested attributes' back into the text. I also added Sequence' in several places where we will need it once we've worked out how those are to be handled. 
<tr><td width="25%">2012.11.1
    <td>Integrate Jame's changes with recent changes
<tr><td width="25%">2012.11.9
    <td>Rebuild the .docx because of repeated Word crashes; minor formatting info changed/lost.
<tr><td width="25%">2012.11.23
    <td>Add a Dataset construct to make the root group concept clear syntactically.
<tr><td width="25%">2013.3.8
    <td>Made unlimited into a boolean attribute because it does have a size.
</table>
<p>
<p>
<p>
<div class="toc"></div>

<div class="section"></div>
<h1 class="section"><a name="introduction">Introduction</a></h1>
This specification defines the protocol referred to as the Data Access Protocol, version 4.0 ("DAP4").  In this document 'DAP' refers to DAP4 unless otherwise noted.
<p>
DAP is intended to be the successor to all previous versions of the DAP (specifically DAP version 2.0). The goal is to provide a very general data model capable of representing a wide variety of existing data sets.
<p>
The DAP builds upon a number of existing data representation schemes. Specifically, it is influenced by
CDM [cite:1], HDF5 [cite:2], DAP version 2.0 [cite:3], and netCDF-4 [cite:5].
<p>
The DAP is a protocol for access to data organized as variables. It is particularly suited to accesses by a client computer to data stored on remote (server) computers that are networked to the client computer.  DAP was designed to hide the implementation of different collections of data. The assumption is that a wide variety of data sets using a wide variety of data schemas can be translated into the DAP protocol for transmission from the server holding that dataset to a client computer for processing.
<p>
It is important to stress the discipline neutrality of the DAP and the relationship between this and adoption of the DAP in disciplines other than the Earth sciences. Because the DAP is agnostic as relates to discipline, it can be used across the very broad range of data types encountered in oceanography - biological, chemical, physical and geological. There is nothing that constrains the use of the DAP to the Earth sciences. 

<h1 class="section"><a name="requirements">Requirements</a></h1>

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY" and "OPTIONAL" in this document are to be interpreted as described in RFC 2119 [cite:7].

<h1 class="section"><a name="operation">Overall Operation</a></h1>

The DAP is a stateless protocol that governs clients making requests from servers, and servers issuing responses to those requests. This section provides an overview of the requests and responses (i.e. the messages) that DAP-compliant software MUST support. These messages are used to request information about a server and data made accessible by that server, as well as requesting data values themselves.
<p>
The DAP uses two responses to represent a data source.  One response, the DMR returns metadata information describing the structure of a request for data. That is, it characterizes the variables, their datatypes, names and attributes. The second response, the Data Response, returns both the metadata about the request, but also the data that was requested. The DMR and the metadata part of the Data Response are represented using a specific XML [cite:16] representation. The syntax of that representation is defined previously (Section <a href="#fqn">fqn</a>).
<p>
The DAP returns error information using an Error response. If a request for any of the three basic responses cannot be completed then an Error response is returned in its place.
<p>
The two responses (DMR and Data Response) are complete in and of themselves so that, for example, a client can use the data response without ever requesting either of the two other responses. In many cases, client programs will request the DMR response first before requesting the Data Response but there is no requirement they do so and no server SHALL require that behavior on the part of clients.
<p>
Operationally, communication between a DAP client and a DAP server uses some underlying already existing protocol. Volume 2 discusses the appropriate choices for the underlying protocol.
<p>
In addition to these data objects, a DAP server MAY provide additional "services" which clients may find useful.  For example, many DAP-compliant servers provide HTML-formatted representations or ASCII representations of a data source's structure and data. Such additional services are discussed in Volume 2 of this specification.

<h1 class="section"><a name="datasource">Characterization of a Data Source</a></h1>

The DAP characterizes a data source as a collection of variables, dimensions, and enumeration types. Each variable consists of a name, a type, a value, and a collection of Attributes. Dimensions have a name and a size. Enumerations list names and values of the enumeration constants. These elements may be grouped into collections using the concept of a "group" that has an identifier and defines a naming scope for the elements within it. Groups may contain other groups.
<p>
The distinction between information in a variable and in an Attribute is somewhat arbitrary. However, the intention is that Attributes hold information that aids in the interpretation of data held in a variable. Variables, on the other hand, hold the primary content of a data source.
<p>
Section <a href="#relaxng">relaxng</a> provides a formal syntax for DAP DMR characterizations. It is defined using the RelaxNG standard [cite:13] for describing the context-free syntax of a class of XML documents, the DMR in this case. It should be noted that any syntax specification requires a specification of the lexical elements of the syntax.
The XML specification [cite:16] provides most of the lexical context for the syntax, but there are certain places where additional lexical elements must be used. Section <a href="#lexical">lexical</a> describes those additional lexical elements, and those elements are discussed at appropriate points in the following discussion.
<p>
Since the syntax is context-free, there are semantic limitations on what is legal in a DMR. These semantic limitations are noted at appropriate places in the following documentation. It should also be noted that if there are conflicts between what is described here and the RelaxNG syntax, then the syntax takes precedence.

<h1 class="section"><a name="declarations">DMR Declarations</a></h1>

<h2 class="section"><a name="escaping">XML Escaping Within the DMR</a></h2>

Any string of characters appearing within an XML attribute in the DMR must apply the standard XML escapes.  Specifically, any attribute value containing any of the following characters must replace them with the corresponding XML escape form.
<p>
<blockquote>
<table border=1 width="30%">
<tr><th>Character<th>Escaped Form
<tr><td>&amp;<td>&amp;amp;
<tr><td>&lt;<td>&amp;lt;
<tr><td>&gt;<td>&amp;gt;
c<tr><td>"<td>&amp;quot;
</table>
</blockquote>
<p>
So for example, given the occurrence of the attribute 
'name="&amp;&lt;&gt;"'
it must be re-written to this form
'name="&amp;amp;&amp;lt;&amp;gt;"'.

<h2 class="section"><a name="names">Names</a></h2>

A name (aka identifier) in DAP4 consists of a sequence of any legal non-control UTF-8 characters. A control character is any UTF-8 character in the inclusive range 0x00 &mdash; 0x1F.

<h2 class="section"><a name="fqn">Fully Qualified Names</a></h2>

Every object in a DAP4 Dataset has a Fully Qualified Name (FQN), which provides a way to unambiguously reference declarations in a dataset and which can be used in several contexts such as in the DMR in a constraint expression
(see Section <a href="#constraints">constraints</a>).
These FQNs follow the common conventions of names for lexically scoped identifiers.  In DAP4 three kinds of lexical items provide lexical scoping: Dataset, Groups and Structures . Just as with hierarchical file systems or variables in many programming languages, a simple grammar formally defines how the names are built using the names of the FQN's components (see Section <a href="#fqnsemantics">fqnsemantics</a>). Consider the following simple dataset, which contains a structure name "inner" within a Structure named "outer" all contained in the Dataset "D".

<blockquote>
<hr>
<pre>
&lt;Dataset name="D"&gt;
    &lt;Structure name="places"&gt;
        &lt;String name="name"/&gt;
        &lt;Structure name="weather"&gt;
            &lt;Float64 name="temperature"/&gt;
            &lt;Float64 name="dew_point"/&gt;
        &lt;/Structure&gt;
    &lt;/Structure&gt;
&lt;/Dataset&gt;
</pre>
<hr>
</blockquote>
<p>
The FQN for the field 'temperature' is
<blockquote>
'/places.weather.temperature'.
</blockquote>
As is the case with Structure variables, Groups can be nested to form hierarchies, too, and this example shows that case. 

<blockquote>
<hr>
<pre>
&lt;Dataset name="D"&gt;
    &lt;Group name="environmental_data"&gt;
        &lt;Structure name="places"&gt;
            &lt;String name="name"/&gt;
            &lt;Structure name="weather"&gt;
                &lt;Float64 name="temperature"/&gt;
                &lt;Float64 name="dew_point"/&gt;
            &lt;/Structure&gt;
        &lt;/Structure&gt;
     &lt;/Group&gt;
     &lt;Group name="demographic_data"&gt;
         ...
     &lt;/Group&gt;
&lt;/Dataset&gt;
</pre>
<hr>
</blockquote>
<p>
The FQN to the field 'temperature' in the dataset shown is
<blockquote>
'/environmental _data/places.weather.temperature'.
</blockquote>
<p>
Notes:
<ol>
<li>Every dataset has a single outermost &lt;Dataset&gt; declaration,
which semantically, acts like the root group.
Whatever name that dataset has is ignored for the purposes of forming the FQN and instead is treated as if it has the empty name ("").
<li>There is no limit to the nesting of groups or the nesting of Structures.
</ol>
<p>
The characters "/" and "." have special meaning in the context of a fully qualified name. This means that if a name is added to the FQN and that name contains either of those two characters, then those characters must be specially escaped so that they will not be misinterpreted. The defined escapes are as follows.
<p>
<blockquote>
<table border=1 width="25%">
<tr><th>Character<th>Escaped Form
<tr><th>.<th>\.
<tr><th>/<th>\/
<tr><th>\<th>\\
</table>
</blockquote>
<p>
Note that the escape character itself must be escaped. Also note that this form of escape using '\' is independent of any required XML escape
(Section <a href="#escaping">escaping</a>).

<h2 class="section"><a name="references">FQN References</a></h2>
DAP4 imposes the rule that the definition of any object (e.g. dimension,
group, or enumeration) must occur before any reference to that object.
This rule also applies within a group, which in turn implies that,
for example, all dimensions must be declared before all variables
that reference them.

<h2 class="section"><a name="declarationtypes">Definitional Declarations versus Data-Bearing Declarations</a></h2>

The declarations in a DMR can be grouped into two classes.
One class is <i>definitional</i>. That is, it defines metadata that is
used in the rest of the DMR.
These definitional declarations are Groups (including the outer Dataset),
Dimensions, and Enumerations.
Such declarations do not contain data values themselves, although they may define constants such as the dimension size.
The data-bearing declarations are Variables and Attributes.
These elements of the data model are used to house data values or semantic metadata read from the dataset (or, in the latter case) synthesized from the values and standards/conventions that the dataset is known to follow.

<h2 class="section"><a name="dataset">Dataset</a></h2>
Every DMR contains exactly one Dataset declaration. It is the outermost
XML element of the DMR.
<p>
A dataset is specified using this XML form:
<blockquote>
<hr>
<pre>
&lt;Dataset name="..." dapVersion="..." dmrVersion="..." base="..."&gt;
...
&lt;/Dataset&gt;
</pre>
</blockquote>
<p>
The <i>name</i>, <i>dapVersion</i>, <i>dmrVersion</i>, and <i>base</i>
attributes are required. Optionally, a namespace attribute (<i>ns="..."</i>)
may be specified.
The attributes have the following semantics:
<ul>
<li> <i>name</i> &ndash; an identifier specifying  the name of the dataset.
Its content is determined solely by the Server and is completely uninterpreted
with respect to DAP4.
<li> <i>dapVersion</i> &ndash; the string &quot;4.0&quot; currently.
<li> <i>dmrVersion</i> &ndash; the string &quot;1.0&quot; currently.
<li> <i>base</i> &ndash; currently uninterpreted.
<li> <i>ns</i> &ndash an XML namespace URl.
</ul>
<p>
The body of the Dataset is the same
as the body of a <a href="#groups">Group declaration</a>,
and semantically the Dataset acts like the outermost, root, group.

<h2 class="section"><a name="groups">Groups</a></h2>
A group is specified using this XML form:

<blockquote>
<hr>
<pre>
&lt;Group name="name"&gt;
...
&lt;Group&gt;
</pre>
<hr>
</blockquote>
<p>
A group defines a name space and contains other DAP elements. Specifically, it can contain groups, variables, dimensions, and enumerations. The fact that groups can be nested means that the set of groups in a DMR form a tree structure. For any given DMR, there exists a root group that is the root of this tree.
<p>
A nested set of groups defines a variety of name spaces and access to the contents of a group is specified using a notation of the form "/g1/g2/.../gn". This is called a "path". By convention "/" refers to the root group (the Dataset declaration). Thus the path "/g1/g2/g3" indicates that one should start in the root group, move to group g1 within that root group, then to group g2 within group g1, and finally to group g3. This is more fully described in the section on Fully Qualified names
(Section <a href="#fqn">fqn</a>).
<p>
For comparison purposes, DAP groups correspond to netCDF-4 groups and not to the more complex HDF5 Group type: i.e. the set of groups must form a tree.

<h3>Semantic Notes</h3>
<ol>
<li>If declared, Groups must be named.
<p>
<li>A Group can contain any number of objects, including other Groups.
<p>
<li>Each Group declares a new lexical scope for the objects it contains. 
<p>
<li>A Group cannot have dimensions and a Group cannot be defined within a Structure.
</ol>

<h2 class="section"><a name="dimensions">Dimensions</a></h2>

A dimension declaration is specified using this XML form.

<blockquote>
<hr>
<pre>
&lt;Dimension name="name" size="size" unlimited="true|false"/&gt;
</pre>
<hr>
</blockquote>
<p>
The size is a positive integer with a maximum value of 2<sup>63-1</sup>. A dimension declaration will be referenced elsewhere in the DMR by specifying its name. It should also be noted that anonymous dimensions also exist. They have a size but no name. Anonymous dimensions SHOULD NOT be declared.
Optionally, a dimension may be tagged as being unlimited (in the netcdf-4 sense).

<h3>Semantic Notes</h3>
<ol>
<li> Dimension declarations are not associated with a data type.
<p>
<li> Dimension sizes that are not 'anonymous' MUST be a capable of being represented as a signed 64-bit integer.
</ol>

<h2 class="section"><a name="enumeration">Enumeration Types</a></h2>

An enumeration type defines a set of names with specific values: enumeration constants. As will be seen in Section <a href="#variables">variables</a>, enumeration types may be used as the type for variables or attributes. The values that can be assigned to such typed objects must come from the set of enumeration constants.
<p>
An enumeration type specifies a set of named, integer constants. When a data source has a variable of type 'Enumeration' a DAP 4 server MUST represent that variable using a specified integer type, up to an including a 64-bit unsigned integer. 
<p>
An Enumeration type is declared using this XML form.

<blockquote>
<hr>
<pre>
&lt;Enumeration name="name"&gt;
                basetype="Byte|Int8|UInt8|Int16|UInt16
                         |Int32|UInt32|Int64|UInt64"/&gt;
    &lt;EnumConst name="name" value="integer"/&gt;
    ...
&lt;/Enumeration&gt;
</pre>
<hr>
</blockquote>

<h3>Semantic Notes</h3>
<ol>
<li> The optional "basetype" XML attribute defines the type for the value XML attribute of each enumeration constant. This basetype must be one of the integer types (see Section <a href="#integer">integer</a>). If unspecified, then it defaults to the Atomic type "Int32".
</ol>

<h2 class="section"><a name="atomic">Atomic Types</a></h2>

The DAP4 specification assumes the existence of certain pre-defined, declared types called atomic types. As their name suggests, atomic data types are conceptually indivisible.  Atomic variables are used to store integers, real numbers, strings and URLs. There are five classes of atomic types, with each family containing one or more variations: integer, floating-point, string, enumerations, and opaque.

<h3 class="section"><a name="integer">Integer Types</a></h3>

The integer types are summarized in the following table.
The lexical structure for integer constants is defined in
Section <a href="#numericconst">numericconst</a>.
<p>
<center><b>Table 1. The DAP Integer Data types.</b></center>
<table border=1 width="85%">
<tr><th>Type Name<th>Description<th>Range of Legal Values
<tr><td>Int8<td>Signed 8-bit integer<td>[-(2<sup>7</sup>), (2<sup>7</sup>) - 1]
<tr><td>UInt8<td>Unsigned 8-bit integer<td>[0, (2<sup>8</sup>) - 1]
<tr><td>Byte<td>Synonym for UInt8<td>[0, (2<sup>8</sup>) - 1]
<tr><td>Char<td>Synonym for UInt8<td>[0, (2<sup>8</sup>) - 1]
<tr><td>Int16<td>Signed 16-bit integer<td>[-(2<sup>15</sup>), (2<sup>15</sup>) - 1]
<tr><td>UInt16<td>Unsigned 16-bit integer<td>[0, (2<sup>16</sup>)  - 1]
<tr><td>Int32<td>Signed 32-bit integer<td>[-(2<sup>31</sup>), (2<sup>31</sup>) - 1]
<tr><td>UInt32<td>Unsigned 32-bit integer<td>[0, (2<sup>32</sup>)  - 1]
<tr><td>Int64<td>Signed 64-bit integer<td>[-(2<sup>63</sup>), (2<sup>63</sup>) - 1]
<tr><td>UInt64<td>Unsigned 64-bit integer<td>[0, (2<sup>64</sup>)  - 1]
</table>
<p>
Note that for historical reasons, the Char type is defined to be a synonym of UInt8, this mean that technically, the Char type has no associated character set encoding. However, servers and clients are free to infer typical character semantics to this type. The inferred character set encoding is chosen purely at the discretion of the server or client using whatever conventions they agree to use.

<h3 class="section"><a name="floating">Floating Point Types</a></h3>

The floating-point data types are summarized in Table 2. The two floating-point data types use IEEE 754 [cite:6] to represent values. The two types correspond to ANSI C's float and double data types. The lexical structure for floating point constants is defined in Section <a href="#numericconst">numericconst</a>.
<p>
<center><b>Table 2. The DAP Floating Point Data types.</b></center>
<table border=1 width="85%">
<tr><th>Type Name<th>Description<th>Range of Legal Values
<tr><td>Float32<td>32-bit Floating-point number<td>Refer to the IEEE Floating Point Standard [cite:6]
<tr><td>Float64<td>64-bit Floating-point number<td>Refer to the IEEE Floating Point Standard [cite:6]
</table>

<h3 class="section"><a name="string">String Types</a></h3>

The string data types are summarized in Table 3.  Again, the lexical structure for these is defined in Section <a href="#stringconst">stringconst</a>
<p>
Strings are individually sized. This means that in an array of strings, for example, each instance of that string MAY be of a different size.
<p>
<center><b>Table 3. The DAP String Data types.</b></center>
<table border=1 width="85%">
<tr><th>Type Name<th>Description<th>Range of Legal Values
<tr><td>String<td>A variable length string of UTF-8 characters<td>As defined in [cite:14]
<tr><td>URI<td>A Uniform Resource Identifier<td>As defined in IETF RFC 2396 [cite:8]
</table>

<h3 class="section"><a name="opaque">The Opaque Type</a></h3>

The XML scheme for declaring an Opaque type is as follows.

<blockquote>
<hr>
<pre>
&lt;Opaque&gt;
</pre>
<hr>
</blockquote>
<p>
The Opaque type is use to hold objects like JPEG images and other Binary Large Object (BLOB) data that have significant internal structure which might be understood by clients (e.g., an image display program) but that would be very cumbersome to describe using the DAP4 built-in types. Defining a variable of type "Opaque" does not communicate any information about its content, although an attribute could be used to do that.

<h3>Semantic Notes</h3>
<ol>
<li> The content of an opaque object is completely un-interpreted by the DAP4 implementation. The Opaque type is an Atomic Type, which might seem odd because instances of Opaque can be of different sizes. However, by thinking of Opaque as equivalent to a byte-string type, the analogy with strings makes it clear that it should be an Atomic type.
</ol>

<h3 class="section"><a name="enum">The Enum Type</a></h3>

The XML scheme for declaring an Enum type is as follows.
<blockquote>
<hr>
<pre>
&lt;Enum enum="FQN"&gt;
</pre>
<hr>
</blockquote>
<p>

<h3>Semantic Notes</h3>
<ol>
<li> The Enum typed requires the an attribute that references a previously defined &lt;Enumeration&gt; declaration.
</ol>

<h3 class="section"><a name="implementation">A Note Regarding Implementation of the Atomic Types</a></h3>

When implementing the DAP, it is important to match information in a data source or read from a DAP response to the local data type which best fits those data. In some cases an exact match may not be possible. For example Java lacks unsigned integer types [cite:4]. Implementations faced with such limitations MUST ensure that clients will be able to retrieve the full range of values from the data source. If this is impractical, then the server or client may implement this rule by hiding the variable in question or returning an error.

<h2 class="section"><a name="containertype">Container Types</a></h2>

There is currently one container type, namely the Structure type.

<h3 class="section"><a name="structuretype">The Structure Type</a></h3>

A Structure groups a list of variables so that the collection can be manipulated as a single item. The variables in a Structure may also be referred to as "fields" to conform to conventional use of that term, but there is otherwise no distinction between fields and variables.  The Structure's fields MAY be of any type, including the Structure type.  The order of items in the Structure is significant only in relation to the serialized representation of that Structure.

<h2 class="section"><a name="variables">Variables</a></h2>

Each variable in a data source MUST have a name, a type and one or more values. Using just this information and armed with an understanding of the definition of the DAP data types, a program can read any or all of the information from a data source.
<p>
The DAP variables come in several different types. There are several atomic types, the basic indivisible types representing integers, floating point numbers and the like, and a container type &ndash; the Structure type &ndash; that supports aggregation of other variables into a single unit. A container type may contain both atomic typed variable as well as other container typed variables, thus allowing nested type definitions.
<p>
The DAP variables describe the data when it is being transferred from the server to the client.  It does not necessarily describe the format of the data inside the server or client. The DAP defines, for each data type described in this document, a serialized representation, which is the information actually communicated between DAP servers and DAP clients.  The serialized representation consists of two parts:  the declaration of the type and the serialized encoding of its value(s). The data representation is presented in
Section <a href="#binarydata">binarydata</a>".

<h3 class="section"><a name="arrays">Arrays</a></h3>

Most (but not all) types may be arrays. An Array is a multi-dimensional indexed data structure. An Array's member variable MUST be of some DAP data type. Array indexes MUST start at zero. Arrays MUST be stored in row-magjor order (as is the case with ANSI C), which means that the order of declaration of dimensions is significant. The size of each Array's dimensions MUST be given, except for variable length dimensions. The total number of elements in an Array MUST NOT exceed 2<sup>64</sup>-1. There is no prescribed limit on the number of dimensions an Array may have except that the foregoing limit on the total number of elements MUST NOT be exceeded. The number of elements in an Array is fixed as that given by the size(s) of its dimension(s), except when the array has a variable length dimension.

<h3>Semantic Notes</h3>
<ol>
<li> Simple variables (see below) MAY be arrays.
<p>
<li> Structures MAY be arrays.
</ol>

<h3 class="section"><a name="simple">Simple Variables</a></h3>

A simple, dimensioned variable is declared using this XML form.

<blockquote>
<hr>
<pre>
&lt;Int32 name="name"&gt;
  &lt;Dim name="{fqn};"/&gt;
  ...
  &lt;Dim size="{integer}"/&gt;
  ...
  &lt;Dim size="*"/&gt;
&lt;/Int32&gt;
</pre>
<hr>
</blockquote>
<p>
Note the use of three types of dimensions.
<ol>
<li> name="{fqn}" &ndash; specify the fully qualified name of a dimensions
declared previously,
<li> size="{integer}" &ndash; specify an anonymous dimension of a given size, 
<li> size="*" &ndash; specify a variable length dimension.
</ol>
<p>
A simple variable is one whose type is one of the Atomic Types
(see Section <a href="#atomic">atomic</a>). The name of the Atomic Type (Int32 in this example) is used as the XML element name. Within the body of that element, it is possible to specify zero or more dimension references. A dimension reference (&lt;Dim.../&gt;) MAY refer to a previously defined dimension declaration. It MAY also define an anonymous dimension with no name, but with a size. It MAY also define a single variable length dimension using a size of "*". This variable length dimension, if present,
must be the last declared dimension.

<h3>Semantic Notes</h3>
<ol>
<li> N.A.
</ol>

<h3 class="section"><a name="ordering">Dimension Ordering</a></h3>
<p>
Consider this example.

<blockquote>
<hr>
<pre>
&lt;Int32  name="i"&gt;
    &lt;Dim name="/d1"/&gt;
    &lt;Dim name="/d2"/&gt;
    ...
    &lt;Dim name="/dn"/&gt;
&lt;/Int32&gt;
</pre>
<hr>
</blockquote>
<p>
The dimensions are considered ordered from top to bottom. From this, a corresponding left-to-right order [d1][d2]...[dn] can be inferred where the top dimension is the left-most and the bottom dimension is the right-most. The assumption of row-major order means that in enumerating all possible combinations of these dimensions, the right-most is considered to vary the fastest. The terms "right(most)" or "left(most") refer to this left-to-right ordering of dimensions.
<p>
Additionally, a list of dimensions MAY contain at most one variable length
dimension and that dimension MUST occur as the right-most dimension.

<h3 class="section"><a name="structurevariables">Structure Variables</a></h3>

As with simple variables, a structure variable specifies a type as well as any dimension for that variable. The type, however, is a Structure.

<h4 class="section"><a name="structures">Structures</a></h4>

The XML scheme for a Structure typed variable is as follows.

<blockquote>
<hr>
<pre>
&lt;Structure name="name"&gt;
  {variable definition}
  {variable definition}
  ...
  {variable definition}
  &lt;Dim ... /&gt;
  ...
  &lt;Dim ... /&gt;
&lt;/Structure&gt;
</pre>
<hr>
</blockquote>
<p>
The Structure contains within it a list of variable definitions
(Section <a href="#variables">variables</a>).
For discussion convenience, each such variable may be referred to as a "field" of the Structure. The list of fields may optionally be followed with a list of dimension references indicating the dimensions of the Structure typed variable.

<h3>Semantic Notes</h3>
<ol>
<li> Structures MAY be dimensioned.
</ol>

<h3 class="section"><a name="coverage">Coverage Variables and Maps</a></h3>

A "Discrete Coverage" is a concept commonly found in many disciplines, where the term refers to a sampled function with both its domain and range explicitly enumerated by variables. DAP2 uses the name 'Grid' to denote what the OGC calls a 'rectangular grid' [cite:12]. DAP4 expands on this so that other types of discrete coverages (hereafter 'coverage(s)') can be explicitly represented.
<p>
In DAP4, the range for a coverage is the values of a (simple or container) variable that includes a specific set of 'maps' or 'coordinate variables' that define the domain for the sampled function. Taken as whole, this type of variable is called a "grid" for convenience sake.
<p>
Using OGC coverage terminology, we have this.
<ol>
<li> The maps specify the "Domain"
<p>
<li> The array specifies the "Range"
<p>
<li> The Grid itself is a "Coverage" per OGC.
<p>
<li> The Domain and Range are sampled functions
</ol>
<p>
A map is defined using the following XML scheme.

<blockquote>
<hr>
<pre>
&lt;Map name="{FQN for some variable defined in the DMR}"/&gt;
</pre>
<hr>
</blockquote>
<p>
An example might look like this.

<blockquote>
<hr>
<pre>
&lt;Float32 name="A"&gt;
  &lt;Dim name="/lat"/&gt;
  &lt;Dim name="/lon"/&gt;
  &lt;Map name="/lat"/&gt;
  &lt;Map name="/lon"/&gt;
&lt;/Float32&gt;
</pre>
<hr>
</blockquote>
Where the map variables are defined elsewhere like this.

<blockquote>
<hr>
<pre>
&lt;Float32 name="lat"&gt;
  &lt;Dim name="/lat"/&gt;
&lt;/Float32&gt;

&lt;Float32 name="/lon"&gt;
  &lt;Dim name="/lon"/&gt;
&lt;/Float32&gt;
</pre>
<hr>
</blockquote>
<p>
The containing variable, A in the example, will be referred to as the "array variable".

<h3>Semantic Notes</h3>
<ol>
<li> Each map variable MUST have a rank no more than that of the array.
<p>
<li> An array variable can have as many maps as desired.
<p>
<li> The dimensions of the array variable may not contain duplicates so A[x,x] is disallowed.
<p>
<li> Any map duplicates are ignored and the order of declaration of the maps is irrelevant.
<p>
<li> A Map variable may not have a variable length dimension.
<p>
<li> The fully qualified name of a map must either be in the same lexical scope as the array variable, or the map must be in some enclosing scope.
<p>
<li> The set of named "associated dimensions for a map must be a subset of the set of named "associated dimensions" for the array variable.
</ol>
<p>
The term "associated dimensions" is computed as follows.
<ol>
<li> The set of associated dimensions is initialized to empty.
<p>
<li> For each element mentioned in the fully qualified name (FQN) of the map or the array variable, add any named dimensions associated with FQN element to the set of associated dimensions (removing duplicates, of course).
</ol>
<p>
In practice, the means that an array variable or map variable must take into account any dimensions associated with any enclosing dimensioned Structure.

<h2 class="section"><a name="attributesandxml">Attributes and Arbitrary XML</a></h2>

<h3 class="section"><a name="attributes">Attributes</a></h3>

Attributes are defined using the following XML scheme.

<blockquote>
<hr>
<pre>
&lt;Attribute name="name" type="{atomic type name}"&gt;
  &lt;Namespace href="http://netcdf.ucar.edu/cf"/&gt;
  &lt;Value value="value"/&gt;
  ...
  &lt;Value value="value"/&gt;
&lt;/Attribute&gt;

&lt;Attribute name="name" type="{container name}"&gt;
  &lt;Namespace href="http://netcdf.ucar.edu/cf"/&gt;

  &lt;Attribute name="name" type="..."&gt;
    ...
  &lt;/Attribute&gt;

  ...

  &lt;Attribute name="name" type="..."&gt;
    ...
  &lt;/Attribute&gt;

&lt;/Attribute&gt;
</pre>
<hr>
</blockquote>
<p>
In DAP4, Attributes (not to be confused with XML attributes) are tuples with four components: 
<ul>
<li> Name 
<p>
<li> Type (one of the defined atomic types such as Int16, String, etc.), or a child attribute container
<p>
<li> Vector of values
<p>
<li> One or more Namespaces (optional)
</ul>
<p>
This differs slightly from DAP2 Attributes because the namespace feature has been added, although clients can choose to ignore it. For more about namespaces, refer to Section <a href="#namespaces">namespaces</a>. The intent of including the namespace information is to simplify interactions with semantic web applications where certain schemas or standards have formal definitions of attributes. 
<p>
Attributes are typically used to associate semantic metadata with the variables in a data source. Attributes are similar to variables in their range of types and values, except that they are somewhat limited when compared to those for variables: they cannot use structure types
<p>
Attributes defined at the top-level within a group are also referred to as "group attributes". Attributes defined at the root group (i.e. Dataset) are "global attributes," which many file formats such as HDF4 or netCDF formally recognize. 
<p>
While the DAP does not require any particular Attributes, some may be required by various metadata conventions. The semantic metadata for a data source comprises the Attributes associated with that data source and its variables. Thus, Attributes provide a mechanism by which semantic metadata may be represented without prescribing that a data source use a particular semantic metadata convention or standard.

<h3>Semantic Notes</h3>
<ol>
<li> DAP4 explicitly treats an attribute with one value as an attribute whose value is a one-element vector. 
<p>
<li> All of the Atomic types as well as containers are allowed as the type for an attribute
<li> If the attribute has type Enum, it must also have an attribute that references a previously defined &lt;Enumeration&gt; declaration.
<p>
<li> Attribute value constants MUST conform to the appropriate constant format for the given attribute type and as defined in
Section <a href="#lexical">lexical</a>.
<p>
<li> Attributes may themselves have attributes: effectively leading to nested attributes. Such attributes are called container attributes. However container attributes may not have values; only lowest level (leaf) attributes may have values.
</ol>

<h3 class="section"><a name="xmlcontent ">Arbitrary XML content </a></h3>
<p>
By supporting an explicit type to hold "arbitrary XML" markup, DAP4 provides a way for the protocol to transport information encoded in XML along with the attributes read from the dataset itself. This has proved very useful in work with semantic web software. 
<p>
The form on an otherXML declaration is as follows.

<blockquote>
<hr>
<pre>
&lt;otherXML name="name"&gt;
{arbitrary xml}
&lt;/otherXML&gt;
</pre>
<hr>
</blockquote>
<p>
There are no &lt;value/&gt; elements because the value of otherXML
is the xml inside the &lt;otherXML&gt;...&lt;/otherXML&gt;.
The text content of the otherXML element must be valid XML and must be distinct from the XML markup used to encode elements of the DAP4 data model (i.e., in a practical sense, the content of an &lt;OtherXML&gt; attribute will be in a namespace other than DAP4). XML content may appear anywhere that an attribute may appear.

<h3 class="section"><a name="placement">Attribute and OtherXML Specification and Placement</a></h3>

Attribute and OtherXML declarations MAY occur within the body of the following XML elements: Group, Dataset, Dimension, Variable, Structure, and Attribute.

<h2 class="section"><a name="namespaces">Namespaces</a></h2>

All elements of the DMR &ndash; Dataset, Groups, Dimensions, Variables, and Attributes &ndash; can contain an associated Namespace element. The namespace's value is defined in the form of an XML style URI string defining the context for interpreting the element containing the namespace. Suppose, hypothetically, that we wanted to specify that an Attribute is to be interpreted as a CF convention [cite:15]. One might specify this as follows.

<blockquote>
<hr>
<pre>
&lt;Attribute name="latitude"&gt;
  &lt;Namespace href="http://cf.netcdf.unidata.ucar.edu"/&gt;
  ...
&lt;/Attribute&gt;
</pre>
<hr>
</blockquote>
<p>
Note that this is not to claim that this is how to specify a CF convention [cite:15].; this is purely illustrative.

<h1 class="section"><a name="data">Data Representation</a></h1>

Data can be an elusive concept. Data may exist in some storage format on some disk somewhere, on paper somewhere else, in active memory on some server, or transmitted along some wire between two computers. All these can still represent the same data. That is, there is an important distinction to be made between the data and its representation. The data can consist of numbers: abstract entities that usually represent measurements of something, somewhere. Data also consist of the relationships between those numbers, as when one number defines a time at which some quantity was measured.
<p>
The abstract existence of data is in contrast to its concrete representation, which is how we manipulate and store it. Data can be stored as ASCII strings in a file on a disk, or as twos-complement integers in the memory of some computer, or as numbers printed on a page.  It can be stored in HDF5 [cite:2], netCDF [cite:5], GRIB[cite:17], a relational database, or any number of other digital storage forms.
<p>
The DAP specifies a particular representation of data, to be used in transmitting that data from one computer to another. This representation of some data is sometimes referred to as the serialized representation of that data, as distinguished from the representations used in some computer's memory. The DAP standard outlined in this document has nothing at all to say about how data is stored or represented on either the sending or the receiving computer. The DAP transmission format is completely independent of these details.

<h2 class="section"><a name="response">Response Structure</a></h2>

The DAP4 Data Response uses a format very similar to that used for DAP2; the data payload is broken into two logical parts. The first part holds metadata describing the names and types of the variables in the response while the second part holds the values of those variables. DAP4 provides several improvements over the DAP2 response, however.
<p>
The metadata information, sent as a preface to the Data Response, is the DMR limited to just those variables included in the response. DAP attributes may be included, but MAY be ignored by the receiving client.
<p>
Data values in the binary part of the Data Response consist of a byte order indicator followed by the binary data for each variable in the order they are listed in the DMR given as the response preface. DAP4 uses a receiver makes it right encoding, so the servers simply write out binary data as they store it with the exceptions that floating-point data must be encoded according to IEEE 754[cite:6] and Integer data must use twos-compliment notation for signed types. Clients are responsible for performing byte-swapping operations needed to compute using the values retrieved.
<p>
The Data Response is encoded using chunking scheme that breaks it into N parts where each part is prefixed with a chunk type and chunk byte count header. Chunk types include data and error types, making it simple for servers to indicate to clients that an error occurred during the transmission of the Data Response and (relatively) simple for clients to detect that error.
<p>
As with DAP2, the response describe here is a document that can be stored on disk or sent as the payload using a number of network transport protocols, HTTP being the primary transport in practice. However, any protocol that can transmit a document can be used to transmit these responses. As such, all critical information needed to decode the response is completely self-contained.
<p>
In the rest of this section we will describe the Data Response in the context of DAP4 using HTTP as its transport protocol.

<h3 class="section"><a name="preface">Structure of the DMR Preface</a></h3>

The first part of the Data Response always contains the DMR.
The Data Response, when DAP is using HTTP as a transport protocol, is the payload for an HTTP response, is separated from the last of the HTTP response's MIME headers by a single blank line, which MIME defines as a carriage return
(ASCII value 13) followed by a line feed (ASCII value 10). This combination
can be abbreviated as CRLF.
<p>
The DMR Data Response itself uses this as a separator between the
DMR count and the DMR and between the DMR preface and the binary data.
<p>
The DMR is preceded by a count indicating the length
of the DMR section (excluding the final CRLF). The count is of the number of bytes, not characters.
because UTF-8 encoding is assumed, which might have multi-byte
characters. The count is of the following form.
<p>
<blockquote>
<pre>
0xXXXX
</pre>
</blockquote>
<p>
which is the ASCII representation of a 32 bit count
where each of the 'X' is a hex digit (i.e. a decimal digit
or a upper or lowercase letter A, B, C, D, E, or F.
Note that this is effectively always big-endian
and given the value '0xABCD' it is converted to the integer value
<blockquote>
(A*2<sup>24</sup> + B*2<sup>16</sup> + C*2<sup>8</sup> + D).
</blockquote>
<p>
The logical organization of the Data Response is shown below.
<blockquote>
<hr>
<pre>
CRLF
{DMR Length}
CRLF
{DMR}
CRLF
{Binary information}
</pre>
<hr>
</blockquote>
<p>
In the above and in the following, the form '{xxx}'
is intended to represent any instance of the xxx.

<h3 class="section"><a name="binarydata">Structure of the Binary Data Part</a></h3>

The binary data part of the Data Response starts with a four-byte byte-order header. This encodes the byte order of the data as sent by the server. The client uses this information to transform the binary data according so it can use those values in computation (i.e., receiver-makes-it-right). Following the byte-order header, the values for each atomic or array variable appear according to their position in the DMR.

<h3 class="section"><a name="chunkedencoding">How the Chunked Encoding Affects the Data Response Format</a></h3>

In a sense, the chunked encoding does not affect the format of the Data Response at all. Conceptually, the entire binary Data Response is built and then passed through a 'chunking encoder' transforming it into one that is broken up into a series of chunks. That 'chunked document' is the sent as the payload of some transport protocol, e.g., HTTP. In practice, that would be a wasteful implementation because a server would need to hold the entire response in memory. A better implementation would, for HTTP, write the initial parts of the HTTP response (its response code and headers) and then use a pipeline of filters to perform the encoding operations. The intent of the chunking scheme is to make it possible for servers to build responses in small chunks, and once they know those parts have been built without error, send them to the client. Thus a server should choose the chunk size to be small enough to fit comfortably in memory but large enough to limit the amount of overhead spent by the software that encodes and decodes those chunks. When an error is detected, the normal flow of building chunks and sending the data along is broken and an error chunk should be sent
(See Section <a href="#errorchunkschema">errorchunkschema</a>).

<h2 class="section"><a name="dsr">The DAP4 Serialized Representation (DSR)</a></h2>

Given a DMR and the corresponding data, the serialized representation is formally described in this section.

<h3 class="section"><a name="ordering2">A Note on Dimension Ordering</a></h3>

Consider this example.
<blockquote>
<hr>
<pre>
&lt;Int32  name="i"&gt;
  &lt;Dimension name="d1"/&gt;
  &lt;Dimension name="d2"/&gt;
  ...
  &lt;Dimension name="dn"/&gt;
&lt;/Int32&gt;
</pre>
<hr>
</blockquote>
<p>
The dimensions are considered ordered the top-to-bottom lexically. This order is linearized into a corresponding left-to-right order [d1][d2]...[dn]. The assumption of row-major order means that in enumerating all possible combinations of these dimensions, the rightmost is considered to vary the fastest. The terms "right(most)" or "left(most") refer to this ordering of dimensions.

<h3 class="section"><a name="serialorder">Order of Serialization</a></h3>

The data appearing in a serialized representation is the concatenation of the variables specified in the tree of Groups within a DMR, where the variables in a group are taken in depth-first, top-to-bottom order. The term "top-to-bottom" refers to the textual ordering of the variables in an XML document specifying a given DMR.
<p>
If a variable is a Structure variable, then its data representation will be the concatenation of the variables it contains, which will appear in top-to-bottom order.
<p>
If a variable has dimensions, then the contents of each dimensioned data item will appear concatenated and taken in row-major order.

<h3 class="section"><a name="varrepresentation">Variable Representation in the Absence of Variable Length Dimensions</a></h3>

Given a dimensioned variable, with no dimension being variable length, it is represented as the N scalar values concatenated in row-major order.
<p>
If the variable is scalar, then it is represented as a single scalar value.

<h4 class="section"><a name="numericscalar">Numeric Scalar Atomic Types</a></h4>

For the numeric atomic types, scalar instances are represented as follows. In all cases a consistent byte ordering is assumed, but the choice of byte order is at the discretion of the program that generates the serial representation, typically a server program.
<p>
<table border=1 width="50%">
<tr><th>Type Name<th>Description<th>Representation
<tr><td>Int8<td>Signed 8-bit integer<td>8 bits 
<tr><td>UInt8<td>Unsigned 8-bit integer<td>8 bits
<tr><td>Byte<td>Unsigned 8-bit integer<td>Same as UInt8 
<tr><td>Char<td>Unsigned 8-bit integer<td>Same as UInt8 
<tr><td>Int16<td>Signed 16-bit integer<td>16 bits
<tr><td>UInt16<td>Unsigned 16-bit integer<td>16 bits
<tr><td>Int32<td>Signed 32-bit integer<td>32-bits
<tr><td>UInt32<td>Unsigned 32-bit integer<td>32-bits
<tr><td>Int64<td>Signed 64-bit integer<td>64-bits
<tr><td>UInt64<td>Unsigned 64-bit integer<td>64-bits
<tr><td>Float32<td>32-bit IEEE floating point<td>32-bits
<tr><td>Float64<td>64-bit IEEE floating point<td>64-bits
</table>
<p>
In narrative form: all numeric quantities are used as a raw, unsigned vector of N bytes, where N is 1 for Char, Int8, and UInt8; it is 2 for Int16 and UInt16; it is 4 for Int32, UInt32, and Float32; and it is 8 for Int64, UInt64, and Float64.

<h4 class="section"><a name="byteswap">Byte Swapping Rules</a></h4>

If the server chooses to byte swap transmitted values, then the following swapping rules are used. Not that a size of 16 bytes is also included. This is used solely to represent checksums as 128-bit unsigned integers
(See Section <a href="#checksums">checksums</a>).
<p>
<table border=1 width="50%">
<tr><th width="20%">Size (bytes)<th>Byte Swapping Rules<th>
<tr><th>1<td>Not Applicable.<td>
<tr><th>2<td>Byte 0 -> Byte 1<br>
Byte 1 ->Byte 0<td>
<tr><th>4<td>Byte 0 -> Byte 3<br>
Byte 1 ->Byte 2<br>
Byte 2 -> Byte 1<br>
Byte 3 ->Byte 0<td>
<tr><th>8<td>Byte 0 -> Byte 7<br>
Byte 1 ->Byte 6<br>
Byte 2 -> Byte 5<br>
Byte 3 ->Byte 4
<td>Byte 4 -> Byte 3<br>
Byte 5 ->Byte 2<br>
Byte 6 -> Byte 1<br>
Byte 7 ->Byte 0
<tr><th>16<td>Byte 0 -> Byte 15<br>
Byte 1 ->Byte 14<br>
Byte 2 -> Byte 13<br>
Byte 3 ->Byte 12<br>
Byte 4 -> Byte 11<br>
Byte 5 ->Byte 10<br>
Byte 6 -> Byte 9<br>
Byte 7 ->Byte 8
<td>Byte 8 -> Byte 7<br>
Byte 9 ->Byte 6<br>
Byte 10 -> Byte 5<br>
Byte 11 ->Byte 4<br>
Byte 12 -> Byte 3<br>
Byte 13 ->Byte 2<br>
Byte 14 -> Byte 1<br>
Byte 15 ->Byte 0
</table>

<h4 class="section"><a name="variablelengthscalar">Variable-Length Scalar Atomic Types</a></h4>

<table border=1 width="85%">
<tr><th>Type Name<th>Description<th>Representation
<tr><td>String<td>Vector of 8-bit bytes representing a UTF-8 String<td>The number of bytes in the string (in UInt64 format) followed by the bytes.
<tr><td>URL<td>Vector of 8-bit bytes representing a URL<td>Same as String
<tr><td>Opaque<td>Vector of un-interpreted 8-bit bytes<td>The number of bytes in the vector (in UInt64 format) followed by the bytes.
</table>
<p>
In narrative form, instances of String, Opaque, and URL types are represented as a 64 bit length (treated as UInt64) of the instance followed by the vector of bytes comprising the value.

<h4 class="section"><a name="structurerepresentation">Structure Variable Representation</a></h4>

A Structure typed variable is represented as the concatenation of the representations of the variables contained in the Structure taken in textual top-to-bottom order. This representation may be nested if one of the variables itself is a Structure variable. Dimensioned structures are represented in a form analogous to dimensioned variables of atomic type. The Structure array is represented by the concatenation of the instances of the dimensioned Structure, where the instances are listed in row-major order. 

<h3 class="section"><a name="vardimrepresentation">Variable Representation in the Presence of a Variable-Length Dimension</a></h3>

Given a dimensioned variable, with the last dimension being variable length, it is represented as follows.
<p>
The variable is represented as the concatenation of N "variable length vectors". N is determined by taking the cross product of the dimensions sizes, left to right, up to, but not including, the variable length dimension. For example, an array of the form Int32 A[2][3][*] has an element count (N) of 2x3 = 6.
<p>
In our example, there will be 6 (2*3) variable-length vectors concatenated together. Note that the length, L, of each of the variable length vectors may be different for each vector. Section <a href="#exampleresponses">exampleresponses</a>
provides some examples in detail.
<p>
Each variable length vector consists of a length, L say, in UInt64 form and giving the number of elements for a specific occurrence of the variable-length dimension. The count, L, is then followed by L instances of the type of the variable (Int32 in this case because the type of the array A is Int32). 

<h3 class="section"><a name="checksums">Checksums</a></h3>

Checksums will be computed for the values of all the variables at the top-level of each Group in the response. The checksum value will follow the value of the variable. The checksum algorithm defaults to MD5 (chosen primarily for performance reasons).
<p>
Checksum values will be written as 128-bit values using the endian representation specified for the serialized form.

<h3 class="section"><a name="historicalnote">Historical Note</a></h3>

The encoding described in Section <a href="#binarydata">binarydata</a>
is similar to the serialization form of the DAP2 protocol [cite:3], but has been extended to support arrays with a varying dimension and stripped of redundant information added by various XDR implementations.
<p>
The DAP4 Serialization rules are derived from, but not the same as, XDR [cite:10]. The differences are as follows.
<ol>
<li> Values are encoded using the byte order of the server. This is the so-called "receiver makes it right" rule.
<p>
<li> No padding is used.
<p>
<li> Floating point values always use the IEEE 754 standard.
<p>
<li> One and two-byte values are not converted to four byte values.
</ol>

<h2 class="section"><a name="exampleresponses">Example responses</a></h2>

In these examples, spaces and newlines have been added to make them easier to read. The real responses are more compact. Since this proposal is just about the form of the response - and it really focuses on the BLOB part - there is no mention of 'chunking.' For information on how this BLOB will/could be chunked.
see Section <a href="#chunkedrepresentation">chunkedrepresentation</a>.
NB: Some poetic license used in the following and the checksums for single integer values seems silly, but these are really simple examples.

<h3 class="section"><a name="example1">A single scalar</a></h3>

<blockquote>
<hr>
<pre>
...
Content-Type: application/vnd.opendap.org.dap4.data
CRLF
{DMR-length-integer}
&lt;Dataset name="foo"&gt;
&lt;Int32 name="x"/&gt;
&lt;/Dataset&gt;
CRLF
{count+tag}
x
{checksum}
</pre>
<hr>
</blockquote>

<h3 class="section"><a name="example2">A single array</a></h3>

<blockquote>
<hr>
<pre>
...
Content-Type: application/vnd.opendap.org.dap4.data
CRLF
{DMR-length-integer}
&lt;Dataset name="foo"&gt;
&lt;Int32 name="x"&gt;
&lt;Dim size="2"&gt;
&lt;Dim size="4"&gt;
&lt;/Int32&gt;
&lt;/Dataset&gt;
CRLF
{count+tag}
x00 x01 x02 x03 x10 x11 x12 x13
{checksum}
</pre>
<hr>
</blockquote>

<h3 class="section"><a name="example3">A single structure</a></h3>

<blockquote>
<hr>
<pre>
...
Content-Type: application/vnd.opendap.org.dap4.data
CRLF
{DMR-length-integer}
&lt;Dataset name="foo"&gt;
  &lt;Structure name="S"&gt;
    &lt;Int32 name="x"&gt;
      &lt;Dim size="2"&gt;
      &lt;Dim size="4"&gt;
    &lt;/Int32&gt;
    &lt;Float64 name="y"/&gt;
  &lt;/Structure&gt;
&lt;/Dataset&gt;
CRLF
{chunk count+tag}
x00 x01 x02 x03 x10 x11 x12 x13
y
{checksum}
</pre>
<hr>
</blockquote>
<p>
Note that in this example, there is a single variable at the top-level of the root Group, and that is S; so it is S for which we compute the checksum.

<h3 class="section"><a name="example4">An array of structures</a></h3>

<blockquote>
<hr>
<pre>
...
Content-Type: application/vnd.opendap.org.dap4.data
CRLF
{DMR-length-integer}
&lt;Dataset name="foo"&gt;
  &lt;Structure name="s"&gt;
    &lt;Int32 name="x"&gt;
      &lt;Dim size="2"/&gt;
      &lt;Dim size="4"/&gt;
    &lt;/Int32&gt;
    &lt;Float64 name="y"/&gt;
    &lt;Dim size="3"/&gt;
  &lt;/Structure&gt;
&lt;/Dataset&gt;
CRLF
{chunk count+tag}
x00 x01 x02 x03 x10 x11 x12 x13 y x00 x01 x02 x03 x10 x11 x12 x13 y x00 x01 x02 x03 x10 x11 x12 x13 y
{checksum}
</pre>
<hr>
</blockquote>

<h3 class="section"><a name="example5">single varying array (one varying dimension)</a></h3>

<blockquote>
<hr>
<pre>
...
Content-Type: application/vnd.opendap.org.dap4.data
CRLF
{DMR-length-integer}
&lt;Dataset name="foo"&gt;
  &lt;String name="s"/&gt;
  &lt;Int32 name="a"&gt;
    &lt;Dim size="*"/&gt;
  &lt;/Int32&gt;
  &lt;Int32 name="x"&gt;
    &lt;Dim size="2"/&gt;
    &lt;Dim size="*"/&gt;
  &lt;/Int32&gt;
&lt;/Dataset>
CRLF
{chunk count+tag}
16 This is a string
{checksum}
5 a0 a1 a2 a3 a4
{checksum}
3 x00 x01 x02 6 x00 x01 x02 x03 x04 x05
{checksum}
</pre>
<hr>
</blockquote>
<p>
Notes:
<ol>
<li> The checksum calculation includes only the values of the variable, not the prefix length bytes.
<p>
<li> The varying dimensions are treated 'like strings' and prefixed with a length count. In the last of the three variables, the array x is a
2 X 'varying' array with the example's first 'row' containing 3 elements and the second 6.
</ol>

<h3 class="section"><a name="example6">A single varying array (two varying dimensions)</a></h3>

The array 'x' has two dimensions, both of which vary in size. In the example, at the time of serialization 'x' has three elements in its outer dimension and those have three, six and one element, respectively. Because these are 'varying' dimentions, the size of each much prefix the actual values.

<blockquote>
<hr>
<pre>
...
Content-Type: application/vnd.opendap.org.dap4.data
CRLF
{DMR-length-integer}
&lt;Dataset name="foo"&gt;
  &lt;Int32 name="x"&gt;
    &lt;Dim size="*"/&gt;
    &lt;Dim size="*"/&gt;
  &lt;/Int32&gt;
&lt;/Dataset&gt;
CRLF
{chunk count+tag}
33 x00 x01 x02 6 x10 x11 x12 x3 x14 x15 1 x20
{checksum}
</pre>
<hr>
</blockquote>

<h3 class="section"><a name="example7">A varying array of structures</a></h3>
<blockquote>
<hr>
<pre>
...
Content-Type: application/vnd.opendap.org.dap4.data
CRLF
{DMR-length-integer}
&lt;Dataset name="foo"&gt;
  &lt;Structure name="s"&gt;
    &lt;Int32 name="x"&gt;
      &lt;Dim size="4"/&gt;
      &lt;Dim size="4"/&gt;
    &lt;/Int32&gt;
    &lt;Float64 name="y"/&gt;
    &lt;Dim size="*"/&gt;
  &lt;/Structure&gt;
&lt;/Dataset&gt;
CRLF
{chunk count+tag}
2x00 x01 x02 x03 x10 x11 x12 x13y x00 x01 x02 x03 x10 x11 x12 x13 y
{checksum}
</pre>
<hr>
</blockquote>
<p>
Note that two rows are assumed.

<h3 class="section"><a name="example8">A varying array of structures with fields that have varying dimensions</a></h3>

<blockquote>
<hr>
<pre>
...
Content-Type: application/vnd.opendap.org.dap4.data
CRLF
{DMR-length-integer}
&lt;Dataset name="foo"&gt;
  &lt;Structure name="s"&gt;
    &lt;Int32 name="x"&gt;
      &lt;Dim size="2"/&gt;
      &lt;Dim size="*"/&gt;
    &lt;/Int32&gt;
    &lt;Float64 name="y"/&gt;
    &lt;Dim size="*"/&gt;
  &lt;/Structure&gt;
&lt;/Dataset&gt;
CRLF
{chunk count+tag}
31 x00 4 x10 x11 x12 x13 y 3 x00 x01 x02 2 x10 x11y 2 x00 x01 2 x10 x11 y
{checksum}
</pre>
<hr>
</blockquote>

<h1 class="section"><a name="chunkedrepresentation">DAP4 Chunked Data Representation</a></h1>

An important capability for DAP4 is supporting client in determining when a data transmission fails. This is especially difficult when sending binary data
(Section <a href="#binarydata">binarydata</a>).
In order to support such a capability, the DAP4 protocol uses a simplified variation on the HTTP/1.1 chunked transmission format [cite:9] to serialize the data part of the response document so that errors are simple to detect. Furthermore, this format is independent of the form or content of that part of the response, so the same format can be used with different response forms or dropped when/if DAP is used with protocols that support out-of-band error signaling, simplifying our ongoing refinement of the protocol.
<p>
The data part of a response document is "chunked" in a fashion similar to that outlined in HTTP/1.1. However, in addition to a prefix indicating the size of the chunk, DAP4 includes a chunk-type code. This provides a way for the receiver to know if the next chunk is part of the data response or if it contains an error response
(Section <a href="#errorchunkschema">errorchunkschema</a>).
In the latter case, the client should assume that the data response has ended, even though the correct closing information was not provided.
<p>
Each chunk is prefixed by a chunk header consisting of a chunk type and byte count, all contained in a single four-byte word and encoded using network byte order. The chunk type will be encoded in the high-order byte of the four-byte word and chunk size will be given by the three remaining bytes of that word. The maximum chunk size possible is 2<sup>24</sup> bytes. Immediately following the four-byte chunk header will be chunk-count bytes followed by another chunk header. More precisely the initial four bytes of the chunk are decoded using the following steps.
<ol>
<li> Treat the 32 bit header a single unsigned integer.
<p>
<li> Convert the integer from network byte order to the local machine byte order by swapping bytes as necessary
(Section <a href="#byteswap">byteswap</a>).
Let the resulting integer be called H.
<p>
<li> Compute the chunk type by the following expression: type = (H &gt;&gt; 24) &amp; 0xff (Using C-language operators).
<p>
<li> Compute the chunk length by the following expression: length = (H &amp; 0x00ffffff) (Using C-language operators).
</ol>
<p>
Three chunk-type types are defined in this proposal:
<p>
<ul>
<li> Data &ndash; This chunk header prefixes the next chunk in the current data response
<p>
<li> Error &ndash; This chunk header prefixes an error message; the current data response has ended 
<p>
<li> End &ndash; This chunk header is the last one for the current data response 
</ul>
It is possible for a chunk to have more than one of the type. So, for example,
if the data fits into a single chunk, then its chunk type
would be Data+End. Error implies End.

<h2 class="section"><a name="chunkedgrammar">Chunked Format Grammar</a></h2>

<blockquote>
<pre>
chunked_response: chunklist ;
chunklist: chunk | chunklist chunk ;
chunk: CHUNKTYPE SIZE CHUNKDATA ;
</pre>
</blockquote>
<p>
Note that there is semantic limitation in the definition of 'chunk':
the number of bytes in the CHUNKDATA must be equal to SIZE.

<h2 class="section"><a name="lexicalstructure">Lexical Structure</a></h2>

<blockquote>
<pre>
/* A single 8-bit byte,
   with the encoding 0 = data, 1 = error, 2 = end */
CHUNKTYPE = '\x01'|'\x02'|'\0x03'
/* A sequence of three 8-bit bytes,
  interpreted as an integer on network byte order */
SIZE = [\0x00-\0xFF][\0x00-\0xFF][\0x00-\0xFF]
CHUNKDATA = [\0x00-\0xFF]*
</pre>
</blockquote>

<h1 class="section"><a name="constraints">Constraints</a></h1>

A request to a DAP4 server for either metadata (the DMR) or data may include a constraint expression. This constraint expression specifies which variables are to be returned and what subset of the data for each variable is to be returned.
<p>
It is important to define a minimal request language &ndash;
a constraint language &ndash; to select information from a dataset on a server and obtaining in response a DMR and data corresponding to that request.
<p>
This section defines the syntax and semantics of the minimal request language that MUST be supported by all implementations. The method by which a server is provided with a constraint is specified in Volume 2.
But as a typical example, if such a constraint were to be embedded in a URL, then it is presumed that it is prefixed with a
"?CE={constraint}"
and is appended to the end of the URL.

<h2 class="section"><a name="constraintsyntax">Syntax</a></h2>

The syntax of the minimal constraint language, also referred to as the "simple constraint" language, is as follows.
<p>
<blockquote>
<pre>
simpleconstraint: /*empty*/ | constraintlist ;

constraintlist: constraint | constraintlist ',' constraint ;

constraint: variablesubset | namedslice ;

variablesubset: PATH structpath ;

structpath: ID dimset | structpath NAME dimset ;

dimset: /*empty*/ | slicelist ;

slicelist: slice | slicelist slice ;

slice:    '[' INTEGER ']'
        | '[' INTEGER ':' INTEGER ']'
        | '[' INTEGER ':' INTEGER ':' INTEGER ']'
        | '[' slicename ']' ;

namedslice: slicename '=' slice ;

slicename: ID ;
</pre>
</blockquote>

The variablesubset rule specifies a subset of values for a variable as specified by the slices. The PATH lexical element is the same as the FQN path as defined in Section <a href="#fqnsemantics">fqnsemantics</a>.
<p>
The structpath is almost the same as the FQN prefix as defined in that same Section. The difference is that each component (between '.' separators) of the structpath can have an optional dimset indicating the set of dimension slices to apply.
<p>
A dimset is either empty or is a slicelist.
<p>
A slicelist is a non-empty list of slices, where a slice indicates a subset of dimension indices. The first case of a slice (e.g. '[5]') indicates a single dimension value, 5 in this case. The second case (e.g. '[5:9]' indicates the range of dimension values 5,6,7,8,9. The third case (e.g. '[5:2:11]') indicates a range of dimension values separated by the stride (the middle values. Thus the example would be the dimension values 5,7,9,11. The fourth case (e.g. '[time]', shows the use of a named slice.
<p>
Note that unlike a suffix, intermediate structures in the structlist can have associated dimsets Thus we might have something like this.

<blockquote>
<hr>
<pre>
/g/S1[5][5:9].v[5:2:11].
</pre>
<hr>
</blockquote>
<p>
A 'namedslice' provides a way to define a slice and give it a slice name.
The slice name has lexical type ID. The name, when enclosed in "[]" can be used anywhere a slice is legal. The goal of the 'namedslice' is to ensure that the same slice is used consistently across multiple 'variablesubsets' as a way to impose shared dimension semantics.
<p>
There are certain context sensitive constraints on 'structpaths' and 'slicelists'.
<ol>
<li> The terminal variable in the 'structpath' must be an atomic-typed variable.
<p>
<li> The number of slices associated with a component in the 'structpath' must correspond to the arity of that structure or the last, atomic-typed variable.
<p>
<li> A slice name must be defined before it is used.
</ol>

<h2 class="section"><a name="constraintsemantics">Interpretation</a></h2>

Consider the following Array.

<blockquote>
<hr>
<pre>
&lt;Int32 name="A"&gt;
  &lt;Dim size="d1"/&gt;
  &lt;Dim size="d2"/&gt;
  ...
  &lt;Dim size="dn"/&gt;
&lt;/Int32&gt;
</pre>
<hr>
</blockquote>
where all of the dimension sizes, di, are integers. 
<p>
Consider the following array subset constraint, where for the purposes of interpretation, all named slices are assumed to have been replaced with their defined slice.

<blockquote>
<hr>
<pre>
A[start1:stride1:end1]...[startn:striden:endn]
</pre>
<hr>
</blockquote>
Where
<p>
<blockquote>
    for i=1 .. n, starti &lt; di &amp; endi &lt; di &amp; starti &lt; endi &amp; starti &gt;= 0 &amp; stridei &gt;= 1 &amp; endi &gt;= 0.
</blockquote>
The constraint selects the elements A[i1][i2]...[in] from A where ii is in the set {starti+stridei*j} and where j=0..k such that starti+stridei*k &lt;= endi and starti+stridei*(k+1) &gt; endi.
<p>
Now consider the same array embedded in a dimensioned Structure.
<p>
<blockquote>
<hr>
<pre>
&lt;Structure name="S"&gt;
  &lt;Int32 name="A"&gt;
    &lt;Dim size="d3"/&gt;
    ...
    &lt;Dim size="dn"/&gt;
  &lt;/Int32&gt;
  &lt;Dim size="d1"/&gt;
  &lt;Dim size="d2"/&gt;
&lt;/Structure&gt;
</pre>
<hr>
</blockquote>
where all of the dimension sizes, di , are again integers.
<p>
Consider the following subset constraint.
<p>
<blockquote>
S[start1:stride1:end1][start2:stride2:end2].A[start3:stride3:end3]...[startn:striden:endn]
</blockquote>
with conditions as before.
<p>
This constraint selects the Structure instances
<p>
<blockquote>
S[i1][i2]
</blockquote>
where ii
is in the set {starti+stridei*j} and where j=0..k such that starti+stridei*k &lt;= endi and starti+stridei*(k+1) &gt; endi.
<p>
Then for each selected structure, the elements
A[i3]...[in] are selected from that instance of A
where ii is in the set {starti+stridei*j} and where j=0..k such that starti+stridei*k &lt;= endi and starti+stridei*(k+1) &gt; endi.
<p>
The results of all of the selections of the instances of A are concatenated as the value of the whole constraint.

<h1 class="section"><a name="references">References</a></h1>

<ol>
<li><!--1-->
Caron, J.,
<i>Unidata's Common Data Model Version 4</i>, 2012
<a href="http://www.unidata.ucar.edu/software/netcdf-java/CDM/">(http://www.unidata.ucar.edu/software/netcdf-java/CDM/).</a>
<p>
<li><!--2-->
Folk, M. and E. Pourmal,
<i>HDF5 Data Model, File Format and Library &mdash; HDF5 1.6</i>,
Category: Recommended Standard January 2007
NASA Earth Science Data Systems Recommended Standard ESDS-RFC-007, 2007
<a href="http://earthdata.nasa.gov/sites/default/files/esdswg/spg/rfc/ese-rfc-007/ESDS-RFC-007v1.pdf">(http://earthdata.nasa.gov/sites/default/files/esdswg/spg/rfc/ese-rfc-007/ESDS-RFC-007v1.pdf).</a>
<p>
<li><!--3-->
Gallagher J., N. Potter, T. Sgouros, S. Hankin, and G. Flierl,
<i>The Data Access Protocol&mdash;DAP 2.0</i>,
NASA Earth Science Data Systems Recommended Standard ESE-RFC-004.1.2
<a href="http://opendap.org/pdf/ESE-RFC-004v1.2.pdf">(http://opendap.org/pdf/ESE-RFC-004v1.2.pdf).</a>
<p>
<li><!--4-->
Gosling, J., B. Joy, G. Steele, G. Bracha, A Buckley,
<i>The Java™ Language Specification &mdash; 7th Editition</i>
Oracle Corporation, 2012,
<a href="http://docs.oracle.com/javase/specs/jls/se7/html/">(http://docs.oracle.com/javase/specs/jls/se7/html/).</a>
<p>
<li><!--5-->
Hartnett, E.,
<i>netCDF-4/HDF5 File Format</i>,
NASA Earth Science Data Systems Recommended Standard ESDS-RFC-022, 2011
<a href="http://earthdata.nasa.gov/sites/default/files/field/document/ESDS-RFC-022v1.pdf">(http://earthdata.nasa.gov/sites/default/files/field/document/ESDS-RFC-022v1.pdf).</a>
<p>
<li><!--6-->
IEEE, <i>IEEE Standard for Binary Floating-Point Arithmetic, ANSI/IEEE Std 754-1985</i>, Digital Object Identifier: 10.1109/IEEESTD.1985.82928, 1985.
<p>
<li><!--7-->
The Internet Society, <i>IETF RFC 2119:
Key words for use in RFCs to Indicate Requirement Levels
</i>, 1997
<a href="http://tools.ietf.org/html/rfc2119">(http://tools.ietf.org/html/rfc2119).</a>
<p>
<li><!--8-->
The Internet Society, <i>IETF RFC 2396:
Uniform Resource Identifiers (URI): Generic Syntax
</i>, 1998
<a href="http://tools.ietf.org/html/rfc2396">(http://tools.ietf.org/html/rfc2396).</a>
<p>
<li><!--9-->
The Internet Society, <i>IETF RFC 2616:
Hypertext Transfer Protocol &mdash; HTTP/1.1
</i>, 1999
<a href="http://tools.ietf.org/html/rfc2616">(http://tools.ietf.org/html/rfc2616).</a>
<p>
<li><!--10-->
The Internet Society, <i>IETF RFC 4506: XDR: External Data Representation Standard</i>, 2006
<a href="http://tools.ietf.org/html/rfc4506">(http://tools.ietf.org/html/rfc4506).</a>
<p>
<li><!--11-->
ISO/IEC,
<i>Information technology &mdash; Portable Operating System Interface (POSIX) &mdash; Part 2: Shell and Utilities</i>,
ISO/IEC 9945-2,1993
<a href="http://www.iso.org/iso/catalogue_detail.htm?csnumber=17841">(http://www.iso.org/iso/catalogue_detail.htm?csnumber=17841).</a>
<p>
<li><!--12-->
The Open Geospatial Consortium Inc.,
<i>Abstract Specifications</i>,
<a href="http://www.opengeospatial.org/standards/as">(http://www.opengeospatial.org/standards/as).</a>
<p>
<li><!--13-->
The Organization for the Advancement of Structured Information Standards,
<i>RELAX NG Specification</i>,
Committee Specification: 2001,
J. Clark, M. Makoto (eds.)
<a href="http://relaxng.org/spec-20011203.html">(http://relaxng.org/spec-20011203.html).</a>
<p>
<li><!--14-->
The Unicode Consortium. <i>The Unicode Standard, Version 6.2.0</i>,  ISBN 978-1-936213-07-8, 2012.
<p>
<li><!--15-->
Unidata,
<i>CF Metadata</i>,
<a href="http://www.cfconventions.org/">(http://www.cfconventions.org/).</a>
<p>
<li><!--16-->
W3C, <i>Extensible Markup Language (XML) 1.0</i>,
T. Bray, J. Paoli, C. M. Sperberg-McQueen, E. Maler, F. Yergeau (eds.),
Fifth Edition. 2008
<a href="http://www.w3.org/TR/2008/REC-xml-20081126/">(http://www.w3.org/TR/2008/REC-xml-20081126/).</a>
<p>
<li><!--17-->
World Meteorological Organization,
<i>FM 92 GRIB</i>,
edition 2, version 2, 2003
<a href="http://www.wmo.int/pages/prog/www/DPS/FM92-GRIB2-11-2003.pdf">(http://www.wmo.int/pages/prog/www/DPS/FM92-GRIB2-11-2003.pdf).007</a>
</ol>

<div class="appendix"></div>

<h1 class="appendix"><a name="fqnsemantics">FQN Syntax</a></h1>

An FQN has two parts. First, there is the path, which refers to Group traversal, and second is the suffix, which refers to the traversal of Structures. An FQN is the concatenation of the path with the suffix and separated by the '/' Character. The suffix may not exist if O is a group or is not a Structure typed variable.
<p>
Fully qualified names conform to the following syntax.
<p>
<blockquote>
<pre>
FQN:   grouppath
     | grouppath '/' name
     | grouppath '/' structurepath
     | grouppath '/' structurepath '.' name

grouppath: /*empty*/ | grouppath '/' groupname

structurepath: /*empty*/ | structurepath '.' structname
</pre>
</blockquote>
<p>
To write a path for an object O, follow these steps.
<ol>
<li><!--0-->
Locate the closest enclosing group G for O.  If O is a group, then O and G will be the same.
<p>
<li> Create the scope prefix for O by traversing a path through the Group tree,
starting with the Dataset and continuing down to and including G. Concatenate the group names on that path and separating them with '/'. The name for Dataset is ignored, hence the FQN will begin with "/".
</ol>
<p>
If O is not a Structure typed variable, then we are done and the FQN for O is just the path. Otherwise, the suffix must be computed as follows.
<p>
<ol>
<li> Traverse the nested Structure declarations from G to O, including O, but not including G in the path. Traversal here means following the enclosing Structure typed variables until O is reached.
<p>
<li> Concatenate the names on that suffix path and separating them with '.' to create a suffix.
<p>
<li> Create the final FQN as the concatenation of the path, the character '/', and the suffix.
</ol>

<h1 class="appendix"><a name="lexical">DAP4 Lexical Elements</a></h1>
This section describes the lexical elements that occur in the DAP4 DMR.
<p>
Within the RELAXNG DAP4 grammar
(Section <a href="#relaxng">relaxng</a>)
there are markers for occurrences of primitive type such as integers, floats, or strings (ignoring case). The markers typically look like this when defining an attribute that can occur in the DAP4 DMR.

<blockquote>
<hr>
<pre>
&lt;attribute name="Principal_Investigator"&gt;
&lt;datatype="dap4_string"/&gt;
&lt;/attribute&gt;
</pre>
<hr>
</blockquote>
The "&lt;data type="dap4_string"/&gt;" specifies the lexical class for the values that this attribute can have. In this case, the "Principal_Investigator" attribute is defined to have a DAP4 string value. Similar notation is used for values occurring as text within an xml element.
<p>
The lexical specification later in this section defines the legal lexical structure for such items. Specifically, it defines the format of the following lexical items.
<ol>
<li> Constants, namely: string, float, integer, character, and opaque.
<p>
<li> Identifiers
<p>
<li> Fully qualified names (also referred to as FQNs)
(Section <a href="#fqn">fqn</a>).
</ol>
The specification is written using the extended POSIX regular expression notation [cite:11] with some additions.
<ol>
<li> Names are assigned to regular expressions using the notation "name = {regular expression}"
<p>
<li> Named expressions can be used in subsequent regular expressions by using the notation "{name}". Such occurrences are equivalent to textually substituting the expression associated with name for the "{name}" occurrence.
</ol>
Notes:
<ol>
<li> The definition of {UTF8} is deferred to the next section.
<p>
<li> Comments are indicated using the "//" notation. Standard xml escape formats (&amp;x#DDD; or &amp;{name};) are assumed to be used as needed.
</ol>

<h2 class="appendix"><a name="charsetdef">Basic character set definitions</a></h2>
<blockquote>
<pre>
CONTROLS   = [\x00-\x1F] // ASCII control characters

WHITESPACE = [ \r\n\t\f]+

HEXCHAR    = [0-9a-zA-Z]

// ASCII printable characters

ASCII = [0-9a-zA-Z !"#$%&amp;'()*+,-./:;&lt;=&gt;?@[\\\]\\^_`|{}~]
</pre>
</blockquote>

<h2 class="appendix"><a name="unescapedascii">Ascii characters that may appear unescaped in Identifiers</a></h2>

This is assumed to be basically all ASCII printable characters except these characters: '.', '/', '"', '&#39;',  and '&amp;'. Occurrences of these characters are assumed to be representable using the standard xml &amp;{name}; notation (e.g. &amp;amp;). In this expression, backslash is interpreted as an escape character.
<p>
<blockquote>
<pre>
IDASCII=[0-9a-zA-Z!#$%()*+:;<=>?@\[\]\\^_`|{}~]
</pre>
</blockquote>

<h2 class="appendix"><a name="numericconst">The Numeric Constant Classes: integer and float</a></h2>
<blockquote>
<pre>
INTEGER    = {INT}|{UINT}|{HEXINT}

INT        = [+-][0-9]+{INTTYPE}?

UINT       = [0-9]+{INTTYPE}?

HEXINT     = {HEXSTRING}{INTTYPE}?

INTTYPE    = ([BbSsLl]|"ll"|"LL")

HEXSTRING  = (0[xX]{HEXCHAR}+)

FLOAT      = ({MANTISSA}{EXPONENT}?)|{NANINF}

EXPONENT   = ([eE][+-]?[0-9]+)

MANTISSA   = [+-]?[0-9]*\.[0-9]*

NANINF     = (-?inf|nan|NaN)B.1.4 The String Constant Class

STRING     = ([^"&amp;&lt;&gt;]|{XMLESCAPE})*

CHAR       = ([^'&amp;&lt;&gt;]|{XMLESCAPE})

URL        = (http|https|[:][/][/][a-zA-Z0-9\-]+
             ([.][a-zA-Z\-]+)+([:][0-9]+)?
             ([/]([a-zA-Z0-9\-._,'\\+%)*
             ([?].+)?([#].+)?
</pre>
</blockquote>

<h2 class="appendix"><a name="stringconst">The String/URL Constant Class</a></h2>
<blockquote>
<pre>
STRING = "\({SIMPLESTRING}{ESCAPEDQUOTE}?\)*"
SIMPLESTRING = [^"\\]
ESCAPEDQOTE=\\"
</pre>
</blockquote>

<h2 class="appendix"><a name="opaqueconst">The Opaque Constant Class</a></h2>
<blockquote>
<pre>
OPAQUE = 0x([0-9A-Fa-f] [0-9A-Fa-f])+
</pre>
</blockquote>
<p>
There is a semantic constraint that if there is an odd
number of hex digits in the opaque constant, a zero hex digit
will be added to the end to ensure that the constant represents
a set of 8-bit bytes.

<h2 class="appendix"><a name="idclass">The Identifier Class</a></h2>
<blockquote>
<pre>
ID         = {IDCHAR}+

IDCHAR     = ({IDASCII}|{XMLESCAPE}|{UTF8})

XMLESCAPE  = [&amp;][#][0-9]+;
</pre>
</blockquote>

<h2 class="appendix"><a name="atomicclass">The Atomic Type Class</a></h2>
<blockquote>
<pre>
ATOMICTYPE =   Char | Byte
             | Int8 | UInt8 | Int16 | UInt16
             | Int32 | UInt32 | Int64 | UInt64
             | Float32 | Float64
             | String | URL
             | Enum
             | Opaque ;
</pre>
</blockquote>
This list should be consistent with the atomic types in the grammar. 

<h2 class="appendix"><a name="fqnclass">The Fully Qualified Name Class</a></h2>
<blockquote>
<pre>
FQN      = ([/]{EID})+([.]{EID})*
EID      = {EIDCHAR}+
EIDCHAR  =  ({EIDASCII}|{XMLESCAPE}|{UTF8})
EIDASCII = [0-9a-zA-Z!#$%()*+:;<=>?@\[\]\\^_`|{}~]
</pre>
</blockquote>
This should be consistent with the definition in Section <a href="#fqn">fqn</a>.

<h2 class="appendix"><a name="dap4_type">DAP4 Type Definitions</a></h2>

The RELAXNG [cite:13] grammar references the following specific types. For each type, the following table give the lexical format as defined by the patterns previously given or by specific patterns as listed.
<p>
<blockquote>
<table border=1 width="50%">
<tr><th>RELAXNG Data Type Name<th>Lexical Pattern
<tr><td>dap4_integer<td>{INTEGER}
<tr><td>dap4_float<td>{FLOAT}
<tr><td>dap4_char<td>{CHAR}
<tr><td>dap4_string<td>{STRING}
<tr><td>dap4_opaque<td>{OPAQUE}
<tr><td>dap4_vdim<td>[*]
<tr><td>dap4_id<td>{ID}
<tr><td>dap4_fqn<td>{FQN}
<tr><td>dap4_uri<td>{URL}
<tr><td>dap4_dim<td>[0-9]+
</table>
</blockquote>
<p>
Note that the above lexical element classes are not disjoint.  The type element "&lt;datatype=.../&gt;" should be sufficient to interpret the type within the DMR.

<h2 class="appendix"><a name="utf8">UTF-8</a></h2>

The UTF-8 specification [cite:14] defines several ways to validate a UTF-8 string of characters.
<p>
The full (most correct) validating version of UTF8 character set is as follows.
<p>
<blockquote>
<pre>
UTF8 =   ([\xC2-\xDF][\x80-\xBF])
       | (\xE0[\xA0-\xBF][\x80-\xBF])
       | ([\xE1-\xEC][\x80-\xBF][\x80-\xBF])
       | (\xED[\x80-\x9F][\x80-\xBF])
       | ([\xEE-\xEF][\x80-\xBF][\x80-\xBF])
       | (\xF0[\x90-\xBF][\x80-\xBF][\x80-\xBF])
       | ([\xF1-\xF3][\x80-\xBF][\x80-\xBF][\x80-\xBF])
       | (\xF4[\x80-\x8F][\x80-\xBF][\x80-\xBF])
</pre>
</blockquote>
The lines of the above expression cover the UTF-8 characters as follows:
<p>
<ol>
<li> non-overlong 2-byte
<li>  excluding overlongs
<li> straight 3-byte
<li> excluding surrogates
<li> straight 3-byte
<li> planes 1-3
<li> planes 4-15
<li> plane 16
</ol>
Note that values from 0 through 127 (ASCII and control characters)
are not included in this any of these definitions.
<p>
The above reference also defines some alternative regular expressions.
<p>
There is what is termed the partially relaxed version of UTF8 defined by this regular expression.
<p>
<blockquote>
<pre>
UTF8 =    ([\xC0-\xD6][\x80-\xBF])
        | ([\xE0-\xEF][\x80-\xBF][\x80-\xBF])
        | ([\xF0-\xF7][\x80-\xBF][\x80-\xBF][\x80-\xBF])
</pre>
</blockquote>
Second, there is what is termed the most-relaxed version of UTF8 defined by this regular expression.
<p>
<blockquote>
<pre>
UTF8 = ([\xC0-\xD6]...)|([\xE0-\xEF)...)|([\xF0 \xF7]...)
</pre>
</blockquote>
Any conforming DAP4 implementation MUST use at least the most-relaxed expression for validating UTF-8 character strings, but MAY use either the partially-relaxed or the full validation expression. 

<h1 class="appendix"><a name="errorchunkschema">DAP4 Error Response Format</a></h1>
The Error Response  is defined to be an XML document
with media type <i>application/vnd.org.opendap.dap4.error.xml</i>.
The specific format of the error response is defined in this
document:
<a href="http://docs.opendap.org/index.php/DAP4_Web_Services_v3#DAP4_Error_Response">http://docs.opendap.org/index.php/DAP4_Web_Services_v3#DAP4_Error_Response</a>

<h1 class="appendix"><a name="relaxng">DAP4 DMR Syntax as a RELAX NG Schema</a></h1>
The RELAX NG grammar for the DMR currently resides at this URL.
<a href="https://scm.opendap.org/svn/trunk/dap4/dap4.rng">https://scm.opendap.org/svn/trunk/dap4/dap4.rng</a>

</body>
</html>

&lt;define name="errorresponse"&gt;
  &lt;element name="Error"&gt;
    &lt;optional&gt;
      &lt;attribute name="httpcode"&gt;&lt;data type="dap4_integer"/&gt;&lt;/attribute&gt;
    &lt;/optional&gt;
    &lt;optional&gt;
      &lt;interleave&gt;
        &lt;element name = "Message"&gt;&lt;text/&gt;&lt;/Message&gt;
        &lt;element name = "Context"&gt;&lt;text/&gt;&lt;/Message&gt;
        &lt;element name = "OtherInformation"&gt;&lt;text/&gt;&lt;/Message&gt;
      &lt;/interleave&gt;
    &lt;/optional&gt;
  &lt;/element&gt;
&lt;/define&gt;
