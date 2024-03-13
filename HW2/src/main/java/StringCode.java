import java.util.HashSet;
import java.util.Set;

// CS108 HW1 -- String static methods

public class StringCode {

	/**
	 * Given a string, returns the length of the largest run.
	 * A run is a series of adajcent chars that are the same.
	 * @param str .
	 * @return blown up string .
	 */
	public static int maxRun(String str) {
		if ( str.isEmpty() ) {
			return 0;
		} else if (str.length() == 1) {
			return 1;
		} else {
			int Maxcnt = 0;
			for (int i = 0; i < str.length() - 1; i++) {
				int cnt = 1;
				for (int j = i + 1; j < str.length(); j++) {
					if (str.charAt(i) == str.charAt(j) && str.charAt(j) == str.charAt(j - 1)) {
						cnt++;
					}
					else {
						break;
					}
				}
				if (cnt > Maxcnt) {
					Maxcnt = cnt;
				}
			}
			return Maxcnt;
		}
	}

	
	/**
	 * Given a string, for each digit in the original string,
	 * replaces the digit with that many occurrences of the character
	 * following. So the string "a3tx2z" yields "attttxzzz".
	 * @param str .
	 * @return blown up string
	 */
	public static String blowup(String str) {
		StringBuilder result = new StringBuilder();
		for (int i = 0; i < str.length(); i++) {
			char kytu = str.charAt(i);
			if (Character.isDigit(kytu) && i < str.length() - 1) {
				int count = Character.getNumericValue(kytu);
				for (int j = 0; j < count; j++) {
					result.append(str.charAt(i + 1));
				}
			} else if (!Character.isDigit(kytu)) {
				result.append(kytu);
			}
		}
		return result.toString();

	}
	
	/**
	 * Given 2 strings, consider all the substrings within them
	 * of length len. Returns true if there are any such substrings
	 * which appear in both strings.
	 * Compute this in linear time using a HashSet. Len will be 1 or more.
	 */
	public static boolean stringIntersect(String a, String b, int len) {
		HashSet<String> substrSet = new HashSet<>();
		for (int i = 0; i < a.length() - len + 1; i++) {
			substrSet.add(a.substring(i, i + len));
		}
		for(int i = 0; i < b.length() + 1; i++) {
			if (substrSet.contains(b.substring(i, i + len))) {
				return true;
			}
		}
		return false;
	}
}
