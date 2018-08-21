import java.util.*;
import java.util.regex.*;
import java.io.*;

public class Generator
{

static boolean DEBUG = false;

static final int MAXDEPTH = 10;

// Following should be consistent with the classify method 
// It is assumed that each of these is on a separate line
static enum Tag {
BLOCKQUOTE_,
_BLOCKQUOTE,
BODY_,
_BODY,
CENTER,
CENTER_,
_CENTER,
DIV,
DOCTYPE,
HEADER,
HR,
HTML_,
_HTML,
P,
PRE_,
_PRE,
STYLE_,
_STYLE,
TABLE_,
_TABLE,
TEXT,
TITLE,
TITLE_,
_TITLE,
// Special cases
ABSTRACT,
CHANGELIST,
SEMNOTES,
};

static enum ClassTag {
APPENDIX,
BREAK,
SECTION,
TITLE,
TOC,
};

static class Line
{
    Tag tag = Tag.TEXT;
    ClassTag classtag = null;	 
    String text = null; // original line text
    int lineno = 0; // in original file

    // Parsed values

    // <h{depth} class="{section|appendix}">{headtext}</h{depth}>
    int depth = 0;
    String section = null;
    String headtext = null;

    // <a name="{anchor}"><{headtext}></a>
    // Assumes only one occurrence per line
    String anchor = null;

    public Line() {}
    public Line(String text) {this(text,-1);}
    public Line(String text, int lineno) {this.text = text; this.lineno = lineno;}
}

static final Line blankline = new Line("");

static String[] alphalevels
  = new String[]{"","A","B","C","D","E","F","G","H","I"};

// Parsing Patterns

// Parse <div class="">...</div>; 1=classtext 2=divtext
static Matcher parsediv
  = Pattern.compile("[ ]*<div class=\"([^\"]*)\">(.*)</div>.*")
    .matcher("");

// Parse <hDD class="">...</hDD>;  1=depth 2=classdecl 3=classname 4=headtext
static Matcher parsehdr
  = Pattern.compile("[ ]*<h([0-9]+)([ ]+class=\"([^\"]*)\")?[ ]*>(.*)</h[0-9]+>.*")
    .matcher("");

// <a name=...; 1=anchor 2=anchortext
static Matcher parseanchor
    = Pattern.compile("<a[ ]+name=\"([^\"]*)\">(.*)</a>")
      .matcher("");

// <a href=...; 1=anchor 2=anchortext
static Matcher refanchor
    = Pattern.compile("<a[ ]+href=\"[#]([^\"]*)\">(.*)</a>")
      .matcher("");

// <a href="http:...; 1=externalurl 2=text
static Matcher externalanchor
    = Pattern.compile("<a[ ]+href=\"(http[s]?:[^\"]*)\"[ ]*>(.*)</a>")
      .matcher("");

static Matcher cite
	= Pattern.compile("\\[cite(:([0-9]+))?\\]")
	  .matcher("");

static Matcher changelist
	= Pattern.compile("<h1>[ ]*Change[ ]*List.*</h1>")
	  .matcher("");

static Matcher semnotes
	= Pattern.compile("<h3>[ ]*Semantic[ ]*Notes.*</h3>")
	  .matcher("");

static Matcher abstractheader
  = Pattern.compile("<h([0-9]+)[ ]+class=\"abstract\">(.*)</h[0-9]+>")
    .matcher("");

/*
// appendix: 1=depth 2=aname 3=text
static Pattern appendixpat
  = Pattern.compile("[ ]*<h([0-9]+)[ ]+class=\"appendix\"[ ]*>[ ]*<a[ ]+name=\"([^\"]*)\">(.+)</a>[ ]*</h[0-9]+>.*");
static Matcher appendix = appendixpat.matcher("");

static Pattern aclosepat = Pattern.compile("</a>");
static Matcher aclose = aclosepat.matcher("");

static Pattern tocendpat
  = Pattern.compile("<div class=\"tocend\"></div>.*");
static Matcher tocend = tocendpat.matcher("");

// Look for appendix or sectionnumber
static Pattern sectionnopat
  = Pattern.compile("[0-9]+([.][0-9]+)* ");
static Matcher sectionno = sectionnopat.matcher("");

static Pattern appendixnopat
  = Pattern.compile("Appendix [A-Z][.] ");
static Matcher appendixno = appendixnopat.matcher("");

// 1=depth 2=head text 
static Pattern titleclasspat
  = Pattern.compile("<h([0-9]+)[ ]+class=\"title\">(.*)</h[0-9]+>");
static Matcher titleclass = titleclasspat.matcher("");

*/

//////////////////////////////////////////////////
// -D options
static int sectionlevels = MAXDEPTH;
static int appendixlevels = 1;

static enum Format {HTML,WIKI,GOOGLEDOCS,WORD;};
static Format DEFAULTFORMAT = Format.HTML;

static Format format = DEFAULTFORMAT;

// Input html document
static List<Line> document = null;

// Table of contents
static List<String> toc = null;

// Processing state
static int[] depthstack = null;
static int stacktop = 0;

static public void main(String[] argv)
{
    try {
	getlevels();
	getformat();
	String filename = (argv.length > 0 ? argv[0] : null);
	document = getinput(filename);
	classify(document);
	assignsections(document);
	buildtoc(document);
	output(document);
    } catch (Exception e) {
	e.printStackTrace();
	System.exit(1);
    }
}


static void
getlevels()
    throws Exception
{
    String prop;
    prop = System.getProperty("level");
    if(prop != null) sectionlevels = Integer.parseInt(prop);
    prop = System.getProperty("applevel");
    if(prop != null) appendixlevels = Integer.parseInt(prop);
}

static void
getformat()
{
    String prop = System.getProperty("format");
    if(prop == null)
	format = DEFAULTFORMAT;
    else if(prop.equalsIgnoreCase("html"))
	format = Format.HTML;	
    else if(prop.equalsIgnoreCase("wiki"))
	format = Format.WIKI;
    else if(prop.equalsIgnoreCase("google"))
	format = Format.GOOGLEDOCS;
    else if(prop.equalsIgnoreCase("word"))
	format = Format.WORD;
    else
	fail("Unknown format: "+prop);
}

static void internal() {fail("Internal error",null,null);}

static void fail(String msg) {fail(msg,null,null);}

static void fail(String msg, String cxt) {fail(msg,new Line(cxt),null);}

static void
fail(String msg, Line line, Exception e)
{
    if(msg == null) msg = "failure";
    if(line == null) line = blankline;
    System.err.println("fail: "+msg+"; "+line.text);
    if(e == null) e = new Exception();
    e.printStackTrace(System.err);
    System.err.flush();
    System.exit(1);
}

static List<Line>
getinput(String filename)
    throws IOException
{
    Reader rdr;
    if(filename == null)
	rdr = new InputStreamReader(System.in);
    else
	rdr = new FileReader(filename);
    BufferedReader buf = new BufferedReader(rdr);
    List<Line> lines = new ArrayList<Line>();
    String text;
    for(int i=0;(text=buf.readLine()) != null; i++) {
	text.replace('\t',' ');
	lines.add(new Line(text,i));
    }
    return lines;
}

static void
classify(List<Line> lines)
{
    for(Line line: lines) {
	String text = cleantext(line.text); /* Simplify the line for testing */
	// Figure out what kind of line this is.
	if(text.matches("<style[^>]*>"))
	    line.tag = Tag.STYLE_;
	else if(text.matches("</style>"))
	    line.tag = Tag._STYLE;
	else if(text.matches("<p>"))
	    line.tag = Tag.P;
	else if(text.matches("<hr>"))
	    line.tag = Tag.HR;
	else if(text.matches("<blockquote>"))
	    line.tag = Tag.BLOCKQUOTE_;
	else if(text.matches("</blockquote>"))
	    line.tag = Tag._BLOCKQUOTE;
	else if(text.matches("<pre>"))
	    line.tag = Tag.PRE_;
	else if(text.matches("</pre>"))
	    line.tag = Tag._PRE;
	else if(text.matches("<!DOCTYPE.*"))
	    line.tag = Tag.DOCTYPE;
	else if(text.matches("<body>"))
	    line.tag = Tag.BODY_;
	else if(text.matches("</body>"))
	    line.tag = Tag._BODY;
	else if(text.matches("<html>"))
	    line.tag = Tag.HTML_;
	else if(text.matches("</html>"))
	    line.tag = Tag._HTML;
	else if(text.matches("<title>"))
	    line.tag = Tag.TITLE_;
	else if(text.matches("</title>"))
	    line.tag = Tag._TITLE;
	else if(text.matches("<title>.*</title>"))
	    line.tag = Tag.TITLE;
	else if(text.matches("<center>.*</center>"))
	    line.tag = Tag.CENTER;
	else if(text.matches("<center>"))
	    line.tag = Tag.CENTER_;
	else if(text.matches("</center>"))
	    line.tag = Tag._CENTER;
	else if(text.matches("<table[^>]*>"))
	    line.tag = Tag.TABLE_;
	else if(text.matches("</table>"))
	    line.tag = Tag._TABLE;
	else if(text.matches("<div[^>]*>.*</div>"))
	    line.tag = Tag.DIV;
	else if(text.matches("<h[0-9]+[^>]*>.*</h[0-9]+>"))
	    line.tag = Tag.HEADER;
        else
            line.tag = Tag.TEXT;

	// Parse some lines to extract info
	switch (line.tag) {
	case DIV:
	    if(!parsediv.reset(line.text).matches()) internal();
	    line.classtag = classtagfor(parsediv.group(1));
	    break;
	
	case HEADER:
	    // re-tag special cases
	    if(text.matches("<h1>[ ]*Change[ ]*List.*</h1>")) {
		line.tag = Tag.CHANGELIST;
		break;
	    }
	    if(text.matches("<h3>[ ]*Semantic[ ]*Notes.*</h3>")) {
		line.tag = Tag.SEMNOTES;
		break;
	    }
	    if(text.matches("<h1>[ ]*Abstract.*</h1>")) {
		line.tag = Tag.ABSTRACT;
		break;
	    }

            if(!parsehdr.reset(line.text).matches())
                internal();
            try {line.depth = Integer.parseInt(parsehdr.group(1));}
            catch (NumberFormatException nfe) {fail("Illegal depth",line,nfe);}
            if(parsehdr.group(2) != null)
                line.classtag = classtagfor(parsehdr.group(3));
            line.headtext  = parsehdr.group(4);
            // Some headers may contain anchors; parse and rebuild headtext
            if(parseanchor.reset(line.headtext).find()) {
                line.anchor = parseanchor.group(1);
                line.headtext = parseanchor.group(2);
            }
	    break;
	default:
	    // Misc fixups
	    // Fix all the [cites:...]
	    while(cite.reset(line.text).find()) {
		line.text = line.text.substring(0,cite.start())
			    + "["+cite.group(2)+"]"
			    + line.text.substring(cite.end(),line.text.length());
	    }
	    break;
	}
    }
}

static String
cleantext(String text)
{
    text = text.replaceAll("[ ]+"," ");
    text = text.trim();
    return text;
}

static ClassTag
classtagfor(String s)
{
    for(ClassTag ct: ClassTag.values())
	if(s.equalsIgnoreCase(ct.name()))
	    return ct;
    fail("Illegal class tag: "+s);
    return null;
}

static void
assignsections(List<Line> lines)
{
    // Assign toc section strings
    depthstack = new int[MAXDEPTH];
    stacktop = 0;

    for(int i=0;i<lines.size();i++) {
	Line line = lines.get(i);
	if(line.tag == Tag.DIV && line.classtag == ClassTag.APPENDIX) {
            continue;
	}
	if(line.classtag != ClassTag.SECTION
	   && line.classtag != ClassTag.APPENDIX) {
	    continue;
	}
	if(line.depth > stacktop) {
	    depthstack[++stacktop] = 1;
	} else if(line.depth < stacktop) {
	    stacktop = line.depth;
	    depthstack[stacktop]++;
	} else {
	    depthstack[stacktop]++;
	}
        line.section = makesectionnumber();
    }	     
}

static void
buildtoc(List<Line> lines)
    throws Exception
{
    toc = new ArrayList<String>();
    int depth = 0;
    // prefix
    switch (format) {
    case GOOGLEDOCS:
	toc.add("<h1>Table of Contents</h1>");
	toc.add("<table>");
	depth = 1;
	break;
    case WIKI:
	toc.add("{| width=\"85%\"");
	toc.add("|+ '''Table of Contents'''");
	depth = 1;
	break;
    default:
	toc.add("<h1 class=\"toc\">Table of Contents</h1>");
    }
    // Do section headers first
    for(Line line: lines) {
	if(line.tag != Tag.HEADER) continue;
        if(line.classtag != ClassTag.SECTION)
	    continue;
	if(line.depth > sectionlevels)
	    continue;
	switch (format) {

	case HTML:
	    // Do nested tables only if format == HTML
	    if(line.depth > depth) {
		toc.add(depth==0?"<table>":"<tr><td><td><table>");
	    } else if(line.depth < depth)
		toc.add("</table>");
	    depth = line.depth;
	    String entry = String.format("<tr><td>%s<td><a href=\"#%s\">%s</a>",
		    line.section,line.anchor,line.headtext);
            toc.add(entry);
	    break;

	case WIKI:
	    toc.add("|-");
	    toc.add("| "+line.section);
	    toc.add(String.format("| [[#%s|%s]]",
			line.headtext,line.headtext));
	    break;
	case GOOGLEDOCS:
	    toc.add(String.format("<tr><td width=\"10%%\">%s<td><a href=\"#%s\">%s</a>",
		    line.section,line.anchor,line.headtext));
	    break;
	default:
	    toc.add(String.format("<tr><td>%s<td><a href=\"#%s\">%s</a>",
		    line.section,line.anchor,line.headtext));
	    break;
	}
    }	     
    while(depth > 0) {
	toc.add(format == Format.WIKI ? "|}" : "</table>");
	depth--;
    }
    
    // Now do the appendices
    boolean foundappendix = false;
    for(Line line: lines) {
	if(line.tag != Tag.HEADER) continue;
	if(line.classtag != ClassTag.APPENDIX)
	    continue;
	if(line.depth > appendixlevels)
	    continue;
	if(!foundappendix) {
	    toc.add(format == Format.WIKI ? "{|" : "<table>");
	    foundappendix = true;
	}
	switch (format) {
	case WIKI:
	    toc.add("|-");
	    toc.add("| "+line.section);
	    toc.add(String.format("| [[#%s|%s]]",
			line.headtext,line.headtext));
	    break;
	case GOOGLEDOCS:
	    toc.add(String.format("<tr><td width=\"20%%\">%s<td><a href=\"#%s\">%s</a>",
		line.section,line.anchor,line.headtext));
	    break;
	default:
	    toc.add(String.format("<tr><td>%s<td><a href=\"#%s\">%s</a>",
		line.section,line.anchor,line.headtext));
	    break;
	}
    }
    if(foundappendix)
	toc.add(format == Format.WIKI ? "|}" : "</table>");
}

static String
makesectionnumber()
{
    String section = "";
    for(int i=1;i<=stacktop;i++) {
	int n = depthstack[i];
	String s = Integer.toString(n);
	if(i > 1) section += '.';
	section += s;
    }
    return section;
}

static String
makeappendixnumber()
{
    String appendix = "";
    for(int i=1;i<=stacktop;i++) {
	int n = depthstack[i];
	String s = Integer.toString(n);
	if(i==1) {
	    s = "Appendix " + alphalevels[n] + ".";
	} else {
	    if(i > 2) appendix += '.';
	}
	appendix += s;
    }
    return appendix;
}

static String
makewikilead(int depth)
{
    return "====================".substring(0,depth+1);
}

static String
makeheader(Line line)
{
    String newtext = null;
    switch (format) {
    case GOOGLEDOCS:
	newtext = String.format(
	    "<h%d>%s %s</h%d>",
	    line.depth,line.section,line.headtext,line.depth);
	break;
    case WIKI:
	switch (line.classtag) {
	case SECTION:
	case APPENDIX:
	    if(line.depth > sectionlevels) {
		newtext = String.format("<i><u><span id=\"%s\">%s</span></u></i>",
					line.headtext,line.headtext);
	    } else {
		newtext=String.format("%s%s%s",
				makewikilead(line.depth),line.headtext,makewikilead(line.depth));
	    }
	    break;
	default:
	    newtext=String.format("==<ins>%s</ins>==",line.headtext);
	    break;
	}
	break;
    case WORD:
	newtext = String.format("<h%d><a name=\"%s\">%s</a></h%d>",
			line.depth,line.section,line.headtext,line.depth);
	break;
    default:
	newtext = String.format(
	    "<h%d class=\"%s\"><a name=\"%s\">%s %s</a></h%d>",
	    line.depth,(line.classtag==ClassTag.APPENDIX?"appendix":"section"),
	    line.anchor,line.section,line.headtext,line.depth);
    }
    return newtext;
}

static void
outputtoc(List<String> toc)
{
    for(int i=0;i<toc.size();i++) {
	System.out.println(toc.get(i));
    }
}	

static Line
findheader(String anchor)
{
    if(anchor != null)
    for(Line line: document) {
	if(line.classtag != ClassTag.SECTION && line.classtag != ClassTag.APPENDIX)
	    continue;
	if(line.anchor == null) continue;
	if(anchor.equalsIgnoreCase(line.anchor))
	    return line;
    }
    fail("Unknown anchor","|"+anchor+"|");
    return null;
}

static void
output(List<Line> lines)
{
    switch (format) {
    case GOOGLEDOCS:
	outputgoogledocs(document);
	break;
    case WIKI:
	outputwiki(document);
	break;
    case WORD:
	outputword(document);
	break;
    default:
	outputhtml(document);
    }
}

static void
outputhtml(List<Line> lines)
{
    for(Line line: lines) {
        String prefix = null;
        String suffix = null;

	String text = line.text;
	switch (line.tag) {

	case DIV:
	    if(line.classtag == ClassTag.TOC) {
		outputtoc(toc);
	        continue; // to skip the <div class="toc" line
	    } else if(line.classtag == ClassTag.APPENDIX) {
		text = "<h1 style=\"font-size:18pt\"><u>Appendices</u></h1>";
		break;
	    }
	    break;

	case HEADER:
           if(line.classtag == ClassTag.SECTION
	       || line.classtag == ClassTag.APPENDIX)
	        text = makeheader(line);
	    else
	        text = line.text;
	    break;

	case ABSTRACT:
	    text = "<h1 class=\"abstract\">Abstract</h1>";
	    break;

	default:
	    text = line.text;
	    break;
	}
	if(refanchor.reset(text).find()) {
	    String anchor = refanchor.group(1);
	    Line hdr = findheader(anchor);
	    String newhref = String.format("<a href=\"#%s\">%s</a>",
				hdr.anchor,hdr.section) ;
	    text = text.substring(0,refanchor.start())
			+ newhref
			+text.substring(refanchor.end(),text.length());
	}
	if(text == null) internal();
	if(prefix != null)
	    System.out.println(prefix);
	System.out.println(text);
	if(suffix != null)
	    System.out.println(suffix);
    }
}

static Matcher
makepattern(String pat)
{
    Pattern p = Pattern.compile(pat);
    Matcher m = p.matcher("");
    return m;
}

static void
removepattern(Matcher m, Line line)
{
    String text = line.text;
    while(m.reset(text).find()) {
	text = text.substring(0,m.start())
		+ text.substring(m.end(),text.length());
    }
    line.text = text;
}

/**
For google docs:
*/
static void
outputgoogledocs(List<Line> lines)
{
    for(Line line: lines) {
	String text = null;
	switch (line.tag) {
	case HEADER:
	    if(line.classtag == null)
                text = line.text;
            else switch (line.classtag) {
	    case SECTION:
	    case APPENDIX:
		text = makeheader(line);	
		break;
	    case TITLE:
		text = String.format("<font size=\"18pt\"><b>%s</b></font><br/>",
				line.headtext);
	    default:
		break;
	    }

	// Ignore these cases
	case DIV:
	    continue; // ignore

	case TEXT:
	default:
	    text = line.text;
	    break;
	}
	System.out.println(text);
    }
}

/**
For Media Wiki Markup
* remove <style>...</style>
* blockquotes around tables
* remove lines with
   <!DOCTYPE | <title> | <html> | </html> | <body> | </body>
* remove all <hr> and <p>
* Fix <a></a> for media wiki
* remove header markers for abstract and change list
...
*/
static void
outputwiki(List<Line> lines)
{
    int i;

    // Output prolog
    System.out.println("[[Category:Development|Development]][[Category:DAP4|DAP4]]");
    System.out.println("[[OPULS_Development| << Back to OPULS Development]]");

    for(i=0;i<lines.size();i++) {
        String prefix = null;
        String suffix = null;

        Line line = lines.get(i);
	String text = line.text;

	switch (line.tag) {

	case DIV:
	    if(line.classtag != ClassTag.APPENDIX)
		continue;
	    prefix = "<div style=\"font-size:18pt\">";
	    text = "'''Appendices'''";
	    suffix = "</div>";
	    break;

	case HEADER:
	    if(line.classtag != null)
            switch (line.classtag) {
	    case APPENDIX:
	    case SECTION:
		text = makeheader(line);	
		break;
	    case TITLE:
		text = String.format("<font size=\"18pt\">'''%s'''</font><br />",
			    line.headtext);
		break;
	    default:
		break;
	    }
	    break;

	case BLOCKQUOTE_:
	    if(lines.get(i+1).tag == Tag.TABLE_)
		continue; // skip
	    break;

	case _BLOCKQUOTE:
	    if(lines.get(i-1).tag == Tag._TABLE)
		continue; // skip
	    break;

	case P:
	    text = "";
	    break;

	case STYLE_:
	   // Skip the style section
	   do {
		line = lines.get(++i);
	   } while(line.tag != Tag._STYLE);
	   continue;

	case ABSTRACT:
	    text = "'''''Abstract'''''";
	    break;
	case CHANGELIST:
	    text = "'''Change List'''";
	    break;
	case SEMNOTES:
	    text = "''<ins>Semantic Notes</ins>''";
	    break;

	case HR:
	case DOCTYPE:
	case BODY_:
	case _BODY:
	case HTML_:
	case _HTML:
	case TITLE:
	case TITLE_:
	case _TITLE:
	case CENTER:
	case CENTER_:
	case _CENTER:
	    // kill it
	    continue;

	default:
	    break;
	}
	// Process the text to fix anchor references (href=)
	if(refanchor.reset(text).find()) {
	    // convert the href to wiki form
	    String anchor = refanchor.group(1);
	    Line hdr = findheader(anchor);
	    text = text.substring(0,refanchor.start())
			+"[[#"+hdr.headtext+"|"+hdr.section+"]]"
			+ text.substring(refanchor.end(),text.length());
	} else if(externalanchor.reset(text).find()) {
	    text = text.substring(0,externalanchor.start())
			+ externalanchor.group(2)
			+text.substring(externalanchor.end(),text.length());
	}
	if(text == null) internal();
	if(prefix != null)
	    System.out.println(prefix);
	System.out.println(text);
	if(suffix != null)
	    System.out.println(suffix);
    }
}

/**
For word:
*/
static void
outputword(List<Line> lines)
{
    boolean inpre = false;

    for(Line line: lines) {
        String prefix = null;
        String suffix = null;

	String text = line.text;

	switch (line.tag) {

	case PRE_:
	    inpre = true;
	    break;

	case _PRE:
	    inpre = false;
	    break;

	case DIV:
	    if(line.classtag == ClassTag.TOC) {
		text = "<h5>Insert TOC Here</h5>";
		break;
	    } else if(line.classtag == ClassTag.APPENDIX) {
		text = "<h6>Appendices</h6>";
		break;
	    }
	    continue;

	case HEADER:
	    if(line.classtag != null)
	    switch (line.classtag) {
	    case SECTION:
                text = makeheader(line);
                break;
	    case APPENDIX:
		text = makeheader(line);
		break;

	    case TITLE:
		text = "<h6>" + line.headtext + "</h6>";
		break;

	    default:
		break;
	    }
            break;

        case ABSTRACT:
            text = "<h5><center><i><b>Abstract</b></i></center></h5>";
            break;
        case SEMNOTES:
            text = "<h5>Semantic Notes</h5>";
            break;
        case CHANGELIST:
            text = "<h6>Change List</h6>";
            break;

	default:
	    break;
	}
	if(refanchor.reset(text).find()) {
	    String anchor = refanchor.group(1);
	    Line hdr = findheader(anchor);
	    String newhref = String.format("<a href=\"#%s\">%s</a>",
		    hdr.section,hdr.section) ;
	    text = text.substring(0,refanchor.start())
	           + newhref
	           +text.substring(refanchor.end(),text.length());
	}
	if(text == null) internal();
	if(prefix != null)
	    System.out.println(prefix);
	System.out.println(text);
	if(suffix != null)
	    System.out.println(suffix);
    }
}

}//Toc

