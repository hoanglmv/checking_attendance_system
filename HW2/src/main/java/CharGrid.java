// HW1 2-d array Problems
// CharGrid encapsulates a 2-d grid of chars and supports
// a few operations on the grid.

public class CharGrid {
	private char[][] grid;

	/**
	 * Constructs a new CharGrid with the given grid.
	 * Does not make a copy.
	 * @param grid .
	 */
	public CharGrid(char[][] grid) {
		this.grid = grid;
	}
	
	/**
	 * Returns the area for the given char in the grid. (see handout).
	 * @param ch char to look for .
	 * @return area for given char .
	 */
	public int charArea(char ch) {
		int cnt = 0;
		boolean find = false;
		int minX = Integer.MAX_VALUE;
		int minY = Integer.MAX_VALUE;
		int maxX = Integer.MIN_VALUE;
		int maxY = Integer.MIN_VALUE;
		for (int i = 0; i < grid.length; i++) {
			for (int j = 0; j < grid[i].length; j++) {
				if (grid[i][j] == ch) {
					minX = Math.min(minX, i);
					minY = Math.min(minY, j);
					maxX = Math.max(maxX, i);
					maxY = Math.max(maxY, j);
					find = true;
				}
			}
		}
		return (maxX - minX + 1) * (maxY - minY + 1);
	}
	
	/**
	 * Returns the count of '+' figures in the grid (see handout).
	 * @return number of + in grid
	 */
	private boolean check(int i, int j) {
		char c = grid[i][j];
		int up = i, down = i, left = j, right = j;
		while (up >= 0 && grid[up][j] == c) {
			up--;
		}
		while (down < grid.length && grid[down][j] == c) {
			down++;
		}
		while (left >= 0 && grid[i][left] == c) {
			left--;
		}
		while (right < grid[i].length && grid[i][right] == c) {
			right++;
		}
		int temp = Math.min(Math.min(i - up, down - i), Math.min(j - left, right - j));
		return temp > 1;
	}
	/** dem so chu thap */
	public int countPlus() {
		int count = 0;
		for (int i = 0; i < grid.length; i++) {
			for (int j = 0; j < grid[i].length; j++) {
				if (check(i, j)) {
					count++;
				}
			}
		}
		return count;
	}
	
}
