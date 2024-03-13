import org.junit.Test;

import java.util.Arrays;

import static junit.framework.TestCase.assertTrue;

public class TetrisGridTest {
	
	// Provided simple clearRows() test
	// width 2, height 3 grid
	@Test
	public void testClear1() {
		boolean[][] before =
		{	
			{true, true, false, },
			{true, true, true, },
			{false, true, true, },
			{true, true, true, }
		};
		
		boolean[][] after =
		{
			{ false , false , false, },
			{ false , false , false, },
			{true, true, false},
			{false, true, true},

		};
		
		TetrisGrid tetris = new TetrisGrid(before);
		tetris.clearRows();

		assertTrue( Arrays.deepEquals(after, tetris.getGrid()) );
	}
	
}
