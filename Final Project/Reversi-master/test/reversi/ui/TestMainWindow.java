package reversi.ui;

import ai.MiniMax;
import junit.framework.TestCase;

public class TestMainWindow extends TestCase {

	MainWindow mw = new MainWindow();
	
	protected void setUp() throws Exception {
		java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                mw.setVisible(true);
            }
        });
	}

	protected void tearDown() throws Exception {
		super.tearDown();
		mw.setVisible(false);
		mw.dispose();
	}

	public void testAutomateNext() {
		mw.getP1AlgButtons()[0].setSelected(true);
		mw.getP2AlgButtons()[0].setSelected(true);
		mw.getP1MethButtons()[0].setSelected(true);
		mw.getP2MethButtons()[0].setSelected(true);
		mw.getjPanel1().setVisible(false);
		
		assertEquals(mw.getI(), 0);
		assertEquals(mw.getJ(), 0);
		assertEquals(mw.getN(), 0);
		assertEquals(mw.getM(), 0);
		
		mw.newGame();
		mw.setAutomate(true);
		mw.automateNext();
		mw.setAutomate(false);
		
		assertEquals(mw.getAlgorithm1(), MiniMax.SearchAlgorithm.MINIMAX);
		assertEquals(mw.getAlgorithm2(), MiniMax.SearchAlgorithm.MINIMAX);
		assertEquals(mw.getI(), 0);
		assertEquals(mw.getJ(), 0);
		assertEquals(mw.getN(), 1);
		assertEquals(mw.getM(), 0);
		
		mw.newGame();
		mw.setAutomate(true);
		mw.automateNext();
		mw.setAutomate(false);
		
		assertEquals(mw.getAlgorithm1(), MiniMax.SearchAlgorithm.MINIMAX);
		assertEquals(mw.getAlgorithm2(), MiniMax.SearchAlgorithm.ALPHA_BETA_PRUNING);
		assertEquals(mw.getI(), 0);
		assertEquals(mw.getJ(), 0);
		assertEquals(mw.getN(), 2);
		assertEquals(mw.getM(), 0);
		
		mw.newGame();
		mw.setAutomate(true);
		mw.automateNext();
		mw.setAutomate(false);
		
		assertEquals(mw.getAlgorithm1(), MiniMax.SearchAlgorithm.MINIMAX);
		assertEquals(mw.getAlgorithm2(), MiniMax.SearchAlgorithm.ITERATIVE_DEEP);
		assertEquals(mw.getI(), 0);
		assertEquals(mw.getJ(), 0);
		assertEquals(mw.getN(), 3);
		assertEquals(mw.getM(), 0);
		
		mw.newGame();
		mw.setAutomate(true);
		mw.automateNext();
		mw.setAutomate(false);
		
		assertEquals(mw.getAlgorithm1(), MiniMax.SearchAlgorithm.MINIMAX);
		assertEquals(mw.getAlgorithm2(), MiniMax.SearchAlgorithm.GREEDY_SEARCH);
		assertEquals(mw.getI(), 0);
		assertEquals(mw.getJ(), 0);
		assertEquals(mw.getN(), 4);
		assertEquals(mw.getM(), 0);
		
		mw.newGame();
		assertEquals(mw.getI(), 0);
		assertEquals(mw.getJ(), 0);
		assertEquals(mw.getN(), 4);
		assertEquals(mw.getM(), 0);
		assertEquals(mw.getP1AlgButtons()[mw.getI()], mw.getjRB_P1AlgMM());
		assertEquals(mw.getP2AlgButtons()[mw.getN()], mw.getjRB_P2AlgRS());
		assertTrue(mw.getjRB_P1AlgMM().isSelected());
		assertEquals(mw.getAlgorithm1(), MiniMax.SearchAlgorithm.MINIMAX);
		assertEquals(mw.getAlgorithm2(), MiniMax.SearchAlgorithm.RANDOM_SEARCH);
		mw.setAutomate(true);
		mw.automateNext();
		mw.setAutomate(false);
		
		
		assertEquals(mw.getI(), 0);
		assertEquals(mw.getJ(), 0);
		assertEquals(mw.getN(), 0);
		assertEquals(mw.getM(), 0);
	}
}
