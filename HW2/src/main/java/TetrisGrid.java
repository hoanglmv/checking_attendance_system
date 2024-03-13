//
// TetrisGrid encapsulates a tetris board and has
// a clearRows() capability.

public class TetrisGrid {
	private boolean[][] grid;
	/**
	 * Constructs a new instance with the given grid.
	 * Does not make a copy.
	 * @param grid .
	 */
	public TetrisGrid(boolean[][] grid) {
		this.grid = grid;
	}

	
	/**
	 * Does row-clearing on the grid (see handout).
	 */
	public void clearRows() {
		for (int i = 0; i < grid.length; i++) {
			boolean check = true;
			for (int j = 0; j < grid[i].length; j++) {
				if (!grid[i][j]) {
					check = false;
					break;
				}
			}
			if (check) {
				for (int k = i; k > 0; k--) {
					grid[k] = grid[k-1];
				}
				grid[0] = new boolean[grid[0].length];
			}
		}
	}
	
	/**
	 * Returns the internal 2d grid array.
	 * @return 2d grid array
	 */
	boolean[][] getGrid() {
		return this.grid;
	}

}
