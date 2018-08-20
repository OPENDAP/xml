package org.opendap.xml.datatypes.dap4;

import org.relaxng.datatype.*;
import org.relaxng.datatype.helpers.ParameterlessDatatypeBuilder;
import org.relaxng.datatype.helpers.StreamingValidatorImpl;

import java.util.regex.*;
import java.util.*;

public class Dap4DatatypeLibrary implements DatatypeLibrary,
		DatatypeLibraryFactory {
	static boolean debug = true;

	static final String uri = "http://xml.opendap.org/datatypes/dap4";

	// Define helper validation patterns
	// Assume all XML escapes (&xxx;) have been translated out

	static final Pattern decimal_integer = Pattern
			.compile("[+-]?\\d+([BbSsLl]|(ll)|(LL))?");
	static final Pattern hex_integer = Pattern.compile("0[xX][0-9a-fA-F]+");
	static final Pattern nan_float = Pattern.compile("[-]?inf|nan|NaN");
	static final Pattern decimal_float = Pattern
			.compile("[+-]?(([0-9]+[.][0-9]*)|([.][0-9]+))([eE][+-]?[0-9]+)?");
	static final Pattern string_pattern = Pattern
			.compile("(([^\\\"])|([\\\\][\\\"]))*");

	static final Pattern id_pattern = Pattern.compile(".+");

	// FQN pattern Sorry for the complexity
	static final Pattern fqn_pattern = Pattern
			.compile("([/](([^/.]|([\\\\][./\\\\]))+))+([.](([^/.]|([\\\\][./\\\\]))+))*");

	// XML escape recognizer
	static final Pattern xml_escape = Pattern
			.compile("[&](amp|lt|gt|quot)|[#](\\d+)[;]");

	// Define an enumeration of possible type names
	static enum DAP4type {
		dap4_unknown, dap4_integer, dap4_float, dap4_char, dap4_string,
		dap4_opaque, dap4_vdim, dap4_id, dap4_fqn, dap4_uri;

		static DAP4type fromString(String name) {
			if (name != null) {
				for (DAP4type t : DAP4type.values()) {
					if (t == DAP4type.dap4_unknown)
						continue; // never legal
					if (t.toString().equals(name)) {
						return t;
					}
				}
			}
			return DAP4type.dap4_unknown;
		}
	};

	// ////////////////////////////////////////////////
	// Per-datatype validator

	static public class Dap4Datatype implements Datatype {
		DAP4type datatype;

		public Dap4Datatype(String typename) {
			datatype = DAP4type.fromString(typename);
		}

		public String toString() {
			return datatype.toString();
		}

		public void checkValid(String literal, ValidationContext context)
				throws DatatypeException {
			if (!isValid(literal, context)) {
				throw new DatatypeException();
			}
		}

		public DatatypeStreamingValidator createStreamingValidator(
				ValidationContext context) {
			return new StreamingValidatorImpl(this, context);
		}

		public Object createValue(String literal, ValidationContext context) {
			if (!isValid(literal, context))
				return null;
			return literal;
		}

		public boolean sameValue(Object obj1, Object obj2) {
			return obj1.equals(obj2);
		}

		public int valueHashCode(Object obj) {
			return obj.hashCode();
		}

		public int getIdType() {
			return ID_TYPE_NULL;
		}

		public boolean isContextDependent() {
			return false;
		}

		// Define an XMl &xxx; unescape function
		static String unescapexml(String s) {
			String result = "";
			Matcher matcher = xml_escape.matcher(s);
			while (s.length() > 0) {
				if (matcher.lookingAt()) {
					// 1. Get matching piece; one of these should be null
					String namecase = matcher.group(1);
					String numbercase = matcher.group(2);
					if (namecase != null) {
						if ("amp".equals(namecase))
							result = result + "&";
						else if ("lt".equals(namecase))
							result = result + "<";
						else if ("gt".equals(namecase))
							result = result + ">";
						else if ("quot".equals(namecase))
							result = result + "\"";
					} else {
						assert (numbercase != null);
						try {
							int i = Integer.parseInt(numbercase);
							if (i == 0 || i > (65535))
								return "";
							result = result + ((char) i);
						} catch (NumberFormatException nfe) {
							return ""; /* Will force failure to validate */
						}
					}
					// skip past match
					s = s.substring(matcher.group().length());
				} else {
					result = result + s.charAt(0);
					s = s.substring(1);
				}
			}
			return result;
		}

		// Define a debug function
		static void report(DAP4type dap4type, String literal, boolean tf) {
			if (debug) {
				System.err.printf("validate: %s: |%s| = %s\n",
						dap4type.toString(), literal, (tf ? "true" : "false"));
			}
		}

		// Locate the last chunk preceded by a non-escaped separator
		// ugh!
		static String lastpiece(String s, char separator) {
			int i, j, len = s.length();
			// Walk s backward to locate the first non-escaped separator
			for (i = len - 1; i >= 0;) {
				if (s.charAt(i) != separator) {
					i--;
					continue;
				}
				// Now walk from separator back to first non-'\\'
				// Locate the index of the last non '\\'
				int count = 0;
				for (j = i - 1; j >= 0;) {
					if (s.charAt(j) == '\\')
						count++;
					else
						break;
				}
				if ((count % 2) == 0) {// i is a non-escaped separator
					String last = s.substring(i + 1, len);
					if (last.length() == 0)
						last = null;
					// if(debug) System.err.printf("accum=|%s|\n",last);
					return last;
				}
				// else this is an escaped separator
				i = j;
			}
			return s; // no non-escaped separators
		}

		// Note that the strings we have shipped to us (literal0)
		// will have any XML escapes converted.

		public boolean isValid(String literal0, ValidationContext context) {
			boolean valid = false;
			Matcher matcher = null;
			String literal = literal0.trim(); // remove leading|trailing blanks

			if (literal == null || literal.length() == 0) {
				report(datatype, "", false);
				return false;
			}

			switch (datatype) {
			case dap4_unknown:
				valid = false;
				break;
			case dap4_integer:
				matcher = decimal_integer.matcher(literal);
				valid = matcher.matches();
				if (!valid) {
					matcher = hex_integer.matcher(literal);
					valid = matcher.matches();
				}
				break;
			case dap4_float:
				matcher = nan_float.matcher(literal);
				valid = matcher.matches();
				if (!valid) {
					matcher = decimal_float.matcher(literal);
					valid = matcher.matches();
				}
				break;
			case dap4_opaque:
				matcher = hex_integer.matcher(literal);
				valid = matcher.matches();
				break;
			case dap4_string:
				matcher = string_pattern.matcher(literal);
				valid = matcher.matches();
				break;
			case dap4_vdim:
				valid = "*".equals(literal);
				break;
			case dap4_char:
				valid = (literal.length() == 1);
				break;
			case dap4_id:
				matcher = id_pattern.matcher(literal);
				valid = matcher.matches();
				break;
			case dap4_fqn:
				matcher = fqn_pattern.matcher(literal);
				valid = matcher.matches();
				break;
			case dap4_uri:
				try {
					java.net.URI uri = new java.net.URI(literal);
					valid = true;
				} catch (java.net.URISyntaxException use) {
					valid = false;
				}
				break;
			}
			report(datatype, literal, valid);
			return valid;
		}

	} // class Dap4Datatype

	public Dap4DatatypeLibrary() {
	}

	// ////////////////////////////////////////////////
	// DatatypeLibraryFactory interface

	public DatatypeLibrary createDatatypeLibrary(String uri) {
		return uri.equals(uri) ? this : null;
	}

	// ////////////////////////////////////////////////
	// DatatypeLibrary interface

	public DatatypeBuilder createDatatypeBuilder(String typename)
			throws DatatypeException {
		if (DAP4type.fromString(typename) == DAP4type.dap4_unknown)
			throw new DatatypeException("Unknown DAP4 datatype: " + typename);
		return new ParameterlessDatatypeBuilder(createDatatype(typename));
	}

	public Datatype createDatatype(String typename) throws DatatypeException {
		Datatype t = new Dap4Datatype(typename);
		return t;
	}

}
