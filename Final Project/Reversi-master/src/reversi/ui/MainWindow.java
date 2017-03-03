/*
 * Copyright (c) 2010 Georgios Migdos <cyberpython@gmail.com>, Filia Dova
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
package reversi.ui;

import java.awt.event.ItemEvent;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.ArrayDeque;
import java.util.List;

import javax.swing.DefaultListModel;
import javax.swing.JFileChooser;
import javax.swing.JLabel;
import javax.swing.JRadioButton;
import javax.swing.UIManager;

import com.opencsv.CSVReader;
import com.opencsv.CSVWriter;

import ai.MiniMax;
import reversi.Board;
import reversi.GameController;
import reversi.GameLogger;
import reversi.GameUndoRedoListener;
import reversi.Move;
import reversi.Utils;
import reversi.ai.ReversiEvaluator.EvaluationMethod;

public class MainWindow extends javax.swing.JFrame implements GameUndoRedoListener, GameLogger {

	private GameController gameController;
	private DefaultListModel gamelogListModel;
	private ArrayDeque<String> redoMessages;
	private JRadioButton[] P1AlgButtons = new JRadioButton[5];
	private JRadioButton[] P2AlgButtons = new JRadioButton[5];
	private JRadioButton[] P1MethButtons = new JRadioButton[4];
	private JRadioButton[] P2MethButtons = new JRadioButton[4];
	private int i = 0, j = 0, m = 0, n = 0;
	private boolean automate = false;
	private BoardPanel boardPanel2;
	private MiniMax.SearchAlgorithm algorithm2;
	private MiniMax.SearchAlgorithm algorithm1;

	/** Creates new form MainWindow */
	public MainWindow() {
		try {
			UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
		} catch (Exception e) {
			try {
				UIManager.setLookAndFeel(UIManager.getCrossPlatformLookAndFeelClassName());
			} catch (Exception e2) {
			}
		}
		initComponents();
		this.gamelogListModel = new DefaultListModel();
		this.jList1.setModel(gamelogListModel);
		this.jPanel4.setVisible(false);

		this.setSize(600, 400);
		this.setLocationRelativeTo(null);

		this.gameController = null;
		this.redoMessages = new ArrayDeque<String>();
		this.updateUndoRedoControls();
	}

	public void newGame() {

		this.redoMessages.clear();

		if (this.gameController != null) {
			this.gameController.removeGameUndoRedoListener(this);
			this.gameController.removeGameLogger(this);
		}

		this.gameController = null;

		int P1Color;
		if (this.jRB_P1ColorBlack.isSelected()) {
			P1Color = Utils.BLACK;
		} else {
			P1Color = Utils.WHITE;
		}
		
		boolean isP1Human;
		isP1Human = this.jRB_P1Human.isSelected();
		boolean isP2Human;
		isP2Human = this.jRB_P2Human.isSelected();
		
		int d2 = (Integer) this.jSpinnerP2.getModel().getValue();
		int d1 = (Integer) this.jSpinnerP1.getModel().getValue();
		
		EvaluationMethod evalMethod2;
		EvaluationMethod evalMethod1;

		if (this.jRB_P2Meth1.isSelected()) {
			evalMethod2 = EvaluationMethod.VALID_MOVES_AND_TOTAL_SCORE;
		} else if (this.jRB_P2Meth2.isSelected()) {
			evalMethod2 = EvaluationMethod.VALID_MOVES_AND_SIDES_COUNT;
		} else if (this.jRB_P2Meth3.isSelected()) {
			evalMethod2 = EvaluationMethod.VALID_MOVES_AND_CORNERS;
		} else {
			evalMethod2 = EvaluationMethod.UTIL_FUNCTION;
		}
		
		if (this.jRB_P1Meth1.isSelected()) {
			evalMethod1 = EvaluationMethod.VALID_MOVES_AND_TOTAL_SCORE;
		} else if (this.jRB_P1Meth2.isSelected()) {
			evalMethod1 = EvaluationMethod.VALID_MOVES_AND_SIDES_COUNT;
		} else  if (this.jRB_P1Meth3.isSelected()) {
			evalMethod1 = EvaluationMethod.VALID_MOVES_AND_CORNERS;
		} else {
			evalMethod1 = EvaluationMethod.UTIL_FUNCTION;
		}

		if (this.jRB_P2AlgMM.isSelected()) {
			algorithm2 = MiniMax.SearchAlgorithm.MINIMAX;
		} else if (this.jRB_P2AlgABP.isSelected()) {
			algorithm2 = MiniMax.SearchAlgorithm.ALPHA_BETA_PRUNING;
		} else if (this.jRB_P2AlgID.isSelected()) {
			algorithm2 = MiniMax.SearchAlgorithm.ITERATIVE_DEEP;
		} else if (this.jRB_P2AlgRS.isSelected()) {
			algorithm2 = MiniMax.SearchAlgorithm.RANDOM_SEARCH;
		} else {
			algorithm2 = MiniMax.SearchAlgorithm.GREEDY_SEARCH;
		}
		
		if (this.jRB_P1AlgMM.isSelected()) {
			algorithm1 = MiniMax.SearchAlgorithm.MINIMAX;
		} else if (this.jRB_P1AlgABP.isSelected()) {
			algorithm1 = MiniMax.SearchAlgorithm.ALPHA_BETA_PRUNING;
		} else if (this.jRB_P1AlgID.isSelected()) {
			algorithm1 = MiniMax.SearchAlgorithm.ITERATIVE_DEEP;
		} else if (this.jRB_P1AlgRS.isSelected()) {
			algorithm1 = MiniMax.SearchAlgorithm.RANDOM_SEARCH;
		} else {
			algorithm1 = MiniMax.SearchAlgorithm.GREEDY_SEARCH;
		}
		System.out.println("Algorithm 1 = " + algorithm1);
		System.out.println("Algorithm 2 = " + algorithm2);
		updateUndoRedoControls();

		this.jPanel7.removeAll();
		boardPanel2 = new BoardPanel();
		this.jPanel7.add(boardPanel2);
		this.gameController = new GameController(this, isP1Human, isP2Human, P1Color, new Board(), boardPanel2, 
				d1, d2, algorithm1, algorithm2, evalMethod1, evalMethod2, Utils.WAIT_FOR_MILLIS);
		this.gameController.addGameUndoRedoListener(this);
		this.gameController.addGameLogger(this);
		this.gameController.startGame();
	}

	public void automateNext() {
		//record data
		String filePath = "analysis.csv";
		try {
				String score = "" + this.boardPanel2.getBoard().getScore().x;
				System.out.println(score);
				this.updateCSV(filePath, score, i*4+j+3, n*4+m+3);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		m++;
		if (m == 1) {
			m = 0;
			n++;
		}
		if (n == 2) {
			n = 0;
			j++;
		}
		if (j == 1) {
			j = 0;
			i++;
		}
		if (i == 2) {
			i = 0;
			this.automate = false;
		}
		
		
		this.jPanel1.setVisible(true);
		if (this.automate) { 
			P1AlgButtons[i].setSelected(true);
			P1MethButtons[j].setSelected(true);
			P2AlgButtons[n].setSelected(true);
			P2MethButtons[m].setSelected(true);
		} else {
			jPanel1.setVisible(false);
			i = 0;
			j = 0;
			m = 0;
			n = 0;
		}
		
	}
	
	/**
	 * Update CSV by row and column
	 * 
	 * @param fileToUpdate CSV file path to update e.g. D:\\chetan\\test.csv
	 * @param replace Replacement for your cell value
	 * @param row Row for which need to update 
	 * @param col Column for which you need to update
	 * @throws IOException
	 */
	public static void updateCSV(String fileToUpdate, String replace,
	    int row, int col) throws IOException {

		File inputFile = new File(fileToUpdate);

		// Read existing file 
		CSVReader reader = new CSVReader(new FileReader(inputFile), ',');
		List<String[]> csvBody = reader.readAll();
		// get CSV row column  and replace with by using row and column
		csvBody.get(row)[col] = replace;
		reader.close();

		// Write to CSV file which is open
		CSVWriter writer = new CSVWriter(new FileWriter(inputFile), ',');
		writer.writeAll(csvBody);
		writer.flush();
		writer.close();
	}
	
	private void undo() {
		if (this.gameController != null) {
			this.gameController.undo();
		}
	}

	private void redo() {
		if (this.gameController != null) {
			this.gameController.redo();
		}
	}

	private void updateUndoRedoControls() {
		if (this.gameController != null) {
			this.jMenuItem3.setEnabled(this.gameController.canUndo());
			this.jMenuItem4.setEnabled(this.gameController.canRedo());
		} else {
			this.jMenuItem3.setEnabled(false);
			this.jMenuItem4.setEnabled(false);
		}
	}

	public void undoableEventHappened() {
		this.updateUndoRedoControls();
	}

	private void setComputerAI1ControlsEnabled(boolean enabled) {
		this.jLabelP1Meth.setEnabled(enabled);
		this.jLabelP1Tree.setEnabled(enabled);
		this.jLabelP1Alg.setEnabled(enabled);
		this.jRB_P1Meth1.setEnabled(enabled);
		this.jRB_P1Meth2.setEnabled(enabled);
		this.jRB_P1Meth3.setEnabled(enabled);
		this.jRB_P1AlgMM.setEnabled(enabled);
		this.jRB_P1AlgABP.setEnabled(enabled);
		this.jRB_P1AlgRS.setEnabled(enabled);
		this.jRB_P1AlgID.setEnabled(enabled);
		this.jRB_P1AlgGS.setEnabled(enabled);
		this.jSpinnerP1.setEnabled(enabled);
	}
	
	private void setComputerAI2ControlsEnabled(boolean enabled) {
		this.jLabelP2Meth.setEnabled(enabled);
		this.jLabelP2Tree.setEnabled(enabled);
		this.jLabelP2Alg.setEnabled(enabled);
		this.jRB_P2Meth1.setEnabled(enabled);
		this.jRB_P2Meth2.setEnabled(enabled);
		this.jRB_P2Meth3.setEnabled(enabled);
		this.jRB_P2AlgMM.setEnabled(enabled);
		this.jRB_P2AlgABP.setEnabled(enabled);
		this.jRB_P2AlgRS.setEnabled(enabled);
		this.jRB_P2AlgID.setEnabled(enabled);
		this.jRB_P2AlgGS.setEnabled(enabled);
		this.jSpinnerP2.setEnabled(enabled);
	}

	public void newGameStarted() {
		this.gamelogListModel.clear();
		this.gamelogListModel.addElement("New game started");
	}

	public void gameOver() {
		this.gamelogListModel.addElement("Game over!");
	}

	public void newMove(Move m) {
		this.gamelogListModel.addElement(
				Utils.getPlayerName(m.getColour()) + " plays: " + (char) ('a' + m.getX()) + "," + (m.getY() + 1));
		this.redoMessages.clear();
		int index = this.gamelogListModel.getSize() - 1;
		this.jList1.setSelectedIndex(index);
		this.jList1.ensureIndexIsVisible(index);
	}

	public void moveUndone() {
		// this.gamelogListModel.addElement("Undo");
		this.redoMessages.push((String) this.gamelogListModel.remove(this.gamelogListModel.size() - 1));
		int index = this.gamelogListModel.getSize() - 1;
		this.jList1.setSelectedIndex(index);
		this.jList1.ensureIndexIsVisible(index);
	}

	public void moveRedone() {
		if (!this.redoMessages.isEmpty()) {
			this.gamelogListModel.addElement(this.redoMessages.pop());
			int index = this.gamelogListModel.getSize() - 1;
			this.jList1.setSelectedIndex(index);
			this.jList1.ensureIndexIsVisible(index);
		}
	}

	private void saveGameLog() {
		final JFileChooser fc = new JFileChooser();
		int retval = fc.showSaveDialog(this);

		if (retval == JFileChooser.APPROVE_OPTION) {
			try {
				BufferedWriter writer = new BufferedWriter(
						new OutputStreamWriter(new FileOutputStream(fc.getSelectedFile())));

				for (int i = 0; i < this.gamelogListModel.size(); i++) {
					try {
						writer.write((String) this.gamelogListModel.get(i));
						writer.newLine();
					} catch (IOException ioe) {
						ioe.printStackTrace();
					}
				}

				try {
					writer.flush();
					writer.close();
				} catch (IOException ioe) {
					ioe.printStackTrace();
				}

			} catch (FileNotFoundException fnfe) {
				fnfe.printStackTrace();
			}

		}
	}

	/**
	 * This method is called from within the constructor to initialize the form.
	 * WARNING: Do NOT modify this code. The content of this method is always
	 * regenerated by the Form Editor.
	 */
	@SuppressWarnings("unchecked")
	// <editor-fold defaultstate="collapsed" desc="Generated
	// Code">//GEN-BEGIN:initComponents
	private void initComponents() {
		
		jRB_P1Human = new javax.swing.JRadioButton();
		jRB_P1Comp = new javax.swing.JRadioButton();
		jRB_P1Meth1 = new javax.swing.JRadioButton();
		jRB_P1Meth2 = new javax.swing.JRadioButton();
		jRB_P1Meth3 = new javax.swing.JRadioButton();
		jRB_P1Meth4 = new javax.swing.JRadioButton();
		jRB_P1AlgMM = new javax.swing.JRadioButton();
		jRB_P1AlgABP = new javax.swing.JRadioButton();
		jRB_P1AlgRS = new javax.swing.JRadioButton();
		jRB_P1AlgID = new javax.swing.JRadioButton();
		jRB_P1AlgGS = new javax.swing.JRadioButton();
		jSpinnerP1 = new javax.swing.JSpinner();
		jLabelP1 = new javax.swing.JLabel();
		jLabelP1Alg = new javax.swing.JLabel();
		jLabelP1Meth = new javax.swing.JLabel();
		jLabelP1Tree = new javax.swing.JLabel();
		buttonGroupColor = new javax.swing.ButtonGroup();
		buttonGroupP2 = new javax.swing.ButtonGroup();
		buttonGroupP2Meth = new javax.swing.ButtonGroup();
		buttonGroupP2Alg = new javax.swing.ButtonGroup();
		buttonGroupP1 = new javax.swing.ButtonGroup();
		buttonGroupP1Meth = new javax.swing.ButtonGroup();
		buttonGroupP1Alg = new javax.swing.ButtonGroup();
		jPanel6 = new javax.swing.JPanel();
		jPanel3 = new javax.swing.JPanel();
		jPanel1 = new javax.swing.JPanel();
		jButton1 = new javax.swing.JButton();
		jLabelP1Color = new javax.swing.JLabel();
		jRB_P1ColorBlack = new javax.swing.JRadioButton();
		jRB_P1ColorWhite = new javax.swing.JRadioButton();
		jLabelP2 = new javax.swing.JLabel();
		jRB_P2Human = new javax.swing.JRadioButton();
		jRB_P2Comp = new javax.swing.JRadioButton();
		jLabelP2Meth = new javax.swing.JLabel();
		jSeparator1 = new javax.swing.JSeparator();
		jPanelNewGame = new javax.swing.JPanel();
		jButton2 = new javax.swing.JButton();
		jLabel5 = new javax.swing.JLabel();
		jSpinnerP2 = new javax.swing.JSpinner();
		jRB_P2Meth1 = new javax.swing.JRadioButton();
		jRB_P2Meth2 = new javax.swing.JRadioButton();
		jRB_P2Meth3 = new javax.swing.JRadioButton();
		jRB_P2Meth4 = new javax.swing.JRadioButton();
		jLabelP2Tree = new javax.swing.JLabel();
		jLabelP2Alg = new javax.swing.JLabel();
		jRB_P2AlgMM = new javax.swing.JRadioButton();
		jRB_P2AlgABP = new javax.swing.JRadioButton();
		jRB_P2AlgRS = new javax.swing.JRadioButton();
		jRB_P2AlgID = new javax.swing.JRadioButton();
		jRB_P2AlgGS = new javax.swing.JRadioButton();
		jPanel4 = new javax.swing.JPanel();
		jPanel5 = new javax.swing.JPanel();
		jButton3 = new javax.swing.JButton();
		jLabel6 = new javax.swing.JLabel();
		jButton4 = new javax.swing.JButton();
		jScrollPane1 = new javax.swing.JScrollPane();
		jList1 = new javax.swing.JList();
		jPanel7 = new javax.swing.JPanel();
		boardPanel1 = new reversi.ui.BoardPanel();
		jMenuBar1 = new javax.swing.JMenuBar();
		jMenu1 = new javax.swing.JMenu();
		jMenuItem1 = new javax.swing.JMenuItem();
		jSeparator2 = new javax.swing.JPopupMenu.Separator();
		jMenuItem2 = new javax.swing.JMenuItem();
		jMenu2 = new javax.swing.JMenu();
		jMenuItem3 = new javax.swing.JMenuItem();
		jMenuItem4 = new javax.swing.JMenuItem();
		jMenu3 = new javax.swing.JMenu();
		jCheckBoxMenuItem1 = new javax.swing.JCheckBoxMenuItem();
		automateButt = new javax.swing.JButton();

		setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
		setTitle("Reversi");
		setMinimumSize(new java.awt.Dimension(1280, 720));
		getContentPane().setLayout(new javax.swing.BoxLayout(getContentPane(), javax.swing.BoxLayout.LINE_AXIS));

		jButton1.setText("Play!");
		jButton1.addActionListener(new java.awt.event.ActionListener() {
			public void actionPerformed(java.awt.event.ActionEvent evt) {
				jButton1ActionPerformed(evt);
			}
		});

		jLabelP1Color.setText("<html><b>Color:</b></html>");

		automateButt.setText("Automate");
		automateButt.addActionListener(new java.awt.event.ActionListener() {
			public void actionPerformed(java.awt.event.ActionEvent evt) {
				automateButtActionPerformed(evt);
			}
		});
		
		P1AlgButtons[0] = jRB_P1AlgMM;
		P1AlgButtons[1] = jRB_P1AlgABP;
		P1AlgButtons[2] = jRB_P1AlgID;
		P1AlgButtons[3] = jRB_P1AlgGS;
		P1AlgButtons[4] = jRB_P1AlgRS;
		
		P2AlgButtons[0] = jRB_P2AlgMM;
		P2AlgButtons[1] = jRB_P2AlgABP;
		P2AlgButtons[2] = jRB_P2AlgID;
		P2AlgButtons[3] = jRB_P2AlgGS;
		P2AlgButtons[4] = jRB_P2AlgRS;
		
		P1MethButtons[0] = jRB_P1Meth1;
		P1MethButtons[1] = jRB_P1Meth2;
		P1MethButtons[2] = jRB_P1Meth3;
		P1MethButtons[3] = jRB_P1Meth4;
		
		P2MethButtons[0] = jRB_P2Meth1;
		P2MethButtons[1] = jRB_P2Meth2;
		P2MethButtons[2] = jRB_P2Meth3;
		P2MethButtons[3] = jRB_P2Meth4;
		
		buttonGroupColor.add(jRB_P1ColorBlack);
		jRB_P1ColorBlack.setSelected(true);
		jRB_P1ColorBlack.setText("Black");

		buttonGroupColor.add(jRB_P1ColorWhite);
		jRB_P1ColorWhite.setText("White");

		jLabelP2.setText("<html><b>Player 2:</b></html>");
		jLabelP1.setText("<html><b>Player 1:</b></html>");

		buttonGroupP2.add(jRB_P2Human);
		jRB_P2Human.setText("Human");
		
		buttonGroupP1.add(jRB_P1Human);
		jRB_P1Human.setText("Human");

		buttonGroupP2.add(jRB_P2Comp);
		jRB_P2Comp.setSelected(true);
		jRB_P2Comp.setText("Computer");
		jRB_P2Comp.addItemListener(new java.awt.event.ItemListener() {
			public void itemStateChanged(java.awt.event.ItemEvent evt) {
				jRB_P2CompItemStateChanged(evt);
			}
		});
		
		buttonGroupP1.add(jRB_P1Comp);
		jRB_P1Comp.setSelected(true);
		jRB_P1Comp.setText("Computer");
		jRB_P1Comp.addItemListener(new java.awt.event.ItemListener() {
			public void itemStateChanged(java.awt.event.ItemEvent evt) {
				jRB_P1CompItemStateChanged(evt);
			}
		});

		jLabelP2Meth.setText("<html><b>Evaluation method:</b></html>");
		jLabelP1Meth.setText("<html><b>Evaluation method:</b></html>");

		jButton2.setText("✕");
		jButton2.addActionListener(new java.awt.event.ActionListener() {
			public void actionPerformed(java.awt.event.ActionEvent evt) {
				jButton2ActionPerformed(evt);
			}
		});

		jLabel5.setBackground(javax.swing.UIManager.getDefaults().getColor("textHighlight"));
		jLabel5.setForeground(javax.swing.UIManager.getDefaults().getColor("textHighlightText"));
		jLabel5.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
		jLabel5.setText("<html><b>New Game</b></html>");
		jLabel5.setBorder(javax.swing.BorderFactory.createLineBorder(new java.awt.Color(0, 0, 0)));
		jLabel5.setOpaque(true);

		javax.swing.GroupLayout jPanelNewGameLayout = new javax.swing.GroupLayout(jPanelNewGame);
		jPanelNewGame.setLayout(jPanelNewGameLayout);
		jPanelNewGameLayout.setHorizontalGroup(jPanelNewGameLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
				.addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanelNewGameLayout.createSequentialGroup()
						.addComponent(jLabel5, javax.swing.GroupLayout.DEFAULT_SIZE, 727, Short.MAX_VALUE)
						.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED).addComponent(jButton2)));
		jPanelNewGameLayout.setVerticalGroup(jPanelNewGameLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
				.addGroup(jPanelNewGameLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
						.addComponent(jButton2).addComponent(jLabel5, javax.swing.GroupLayout.PREFERRED_SIZE, 23,
								javax.swing.GroupLayout.PREFERRED_SIZE)));

		jSpinnerP2.setModel(new javax.swing.SpinnerNumberModel(3, 2, 6, 1));
		jSpinnerP1.setModel(new javax.swing.SpinnerNumberModel(3, 2, 6, 1));

		buttonGroupP2Meth.add(jRB_P2Meth1);
		jRB_P2Meth1.setText("Score");

		buttonGroupP2Meth.add(jRB_P2Meth2);
		jRB_P2Meth2.setText("Num Sides");

		buttonGroupP2Meth.add(jRB_P2Meth3);
		jRB_P2Meth3.setSelected(true);
		jRB_P2Meth3.setText("Num Corners");
		
		buttonGroupP2Meth.add(jRB_P2Meth4);
		jRB_P2Meth4.setText("Utility Function");

		buttonGroupP1Meth.add(jRB_P1Meth1);
		jRB_P1Meth1.setText("Score");

		buttonGroupP1Meth.add(jRB_P1Meth2);
		jRB_P1Meth2.setText("Num Sides");

		buttonGroupP1Meth.add(jRB_P1Meth3);
		jRB_P1Meth3.setSelected(true);
		jRB_P1Meth3.setText("Num Corners");
		
		buttonGroupP1Meth.add(jRB_P1Meth4);
		jRB_P1Meth4.setText("Utility Function");
		
		jLabelP2Tree.setText("<html><b>Search tree depth :</b></html>");
		jLabelP1Tree.setText("<html><b>Search tree depth :</b></html>");

		jLabelP2Alg.setText("<html><b>Algorithm:</b></html>");
		jLabelP1Alg.setText("<html><b>Algorithm:</b></html>");

		buttonGroupP2Alg.add(jRB_P2AlgMM);
		jRB_P2AlgMM.setText("MiniMax");

		buttonGroupP2Alg.add(jRB_P2AlgABP);
		jRB_P2AlgABP.setSelected(true);
		jRB_P2AlgABP.setText("Alpha-Beta Pruning");

		buttonGroupP2Alg.add(jRB_P2AlgRS);
		jRB_P2AlgRS.setSelected(false);
		jRB_P2AlgRS.setText("Random Selection");
		
		buttonGroupP2Alg.add(jRB_P2AlgID);
		jRB_P2AlgID.setSelected(false);
		jRB_P2AlgID.setText("Iterative Deep");

		buttonGroupP2Alg.add(jRB_P2AlgGS);
		jRB_P2AlgGS.setSelected(false);
		jRB_P2AlgGS.setText("Greedy Selection");
		
		buttonGroupP1Alg.add(jRB_P1AlgMM);
		jRB_P1AlgMM.setText("MiniMax");

		buttonGroupP1Alg.add(jRB_P1AlgABP);
		jRB_P1AlgABP.setSelected(true);
		jRB_P1AlgABP.setText("Alpha-Beta Pruning");

		buttonGroupP1Alg.add(jRB_P1AlgRS);
		jRB_P1AlgRS.setSelected(false);
		jRB_P1AlgRS.setText("Random Selection");
		
		buttonGroupP1Alg.add(jRB_P1AlgID);
		jRB_P1AlgID.setSelected(false);
		jRB_P1AlgID.setText("Iterative Deep");

		buttonGroupP1Alg.add(jRB_P1AlgGS);
		jRB_P1AlgGS.setSelected(false);
		jRB_P1AlgGS.setText("Greedy Selection");


		javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
		jPanel1.setLayout(jPanel1Layout);
		jPanel1Layout
				.setHorizontalGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
						.addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
								.addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
										.addGroup(jPanel1Layout.createSequentialGroup()
												.addComponent(jLabelP2, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P2Human)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P2Comp))
										.addGroup(jPanel1Layout.createSequentialGroup()
												.addComponent(jLabelP2Alg, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P2AlgMM)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P2AlgABP)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P2AlgID)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P2AlgGS)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P2AlgRS))
										.addGroup(jPanel1Layout.createSequentialGroup()
												.addComponent(jLabelP2Tree, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jSpinnerP2, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addGap(30)
												.addComponent(jLabelP2Meth, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P2Meth1)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P2Meth2)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P2Meth3)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P2Meth4))
										.addGroup(jPanel1Layout.createSequentialGroup()
												.addComponent(jLabelP1, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P1Human)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P1Comp)
												.addGap(30)
												.addComponent(jLabelP1Color, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P1ColorBlack)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P1ColorWhite))
										.addGroup(jPanel1Layout.createSequentialGroup()
												.addComponent(jLabelP1Alg, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P1AlgMM)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P1AlgABP)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P1AlgID)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P1AlgGS)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P1AlgRS))
										.addGroup(jPanel1Layout.createSequentialGroup()
												.addComponent(jLabelP1Tree, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jSpinnerP1, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addGap(30)
												.addComponent(jLabelP1Meth, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P1Meth1)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P1Meth2)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P1Meth3)
												.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
												.addComponent(jRB_P1Meth4)))
								.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, 231,
										Short.MAX_VALUE)
								.addComponent(automateButt, javax.swing.GroupLayout.PREFERRED_SIZE, 84,
										javax.swing.GroupLayout.PREFERRED_SIZE)
								.addComponent(jButton1, javax.swing.GroupLayout.PREFERRED_SIZE, 84,
										javax.swing.GroupLayout.PREFERRED_SIZE)
								.addContainerGap())
						.addComponent(jPanelNewGame, javax.swing.GroupLayout.Alignment.TRAILING,
								javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE,
								Short.MAX_VALUE)
						.addGroup(jPanel1Layout.createSequentialGroup().addContainerGap()
								.addComponent(jSeparator1, javax.swing.GroupLayout.DEFAULT_SIZE, 737, Short.MAX_VALUE)
								.addContainerGap()));
		jPanel1Layout.setVerticalGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
				.addGroup(jPanel1Layout.createSequentialGroup()
						.addComponent(jPanelNewGame, javax.swing.GroupLayout.PREFERRED_SIZE,
								javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
						.addGap(12, 12, 12)
						.addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
								.addComponent(automateButt, javax.swing.GroupLayout.DEFAULT_SIZE, 80, Short.MAX_VALUE)
								.addComponent(jButton1, javax.swing.GroupLayout.DEFAULT_SIZE, 80, Short.MAX_VALUE)
								.addGroup(jPanel1Layout.createSequentialGroup()
										.addGroup(jPanel1Layout
												.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
												.addComponent(jLabelP1, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addComponent(jRB_P1Human).addComponent(jRB_P1Comp)
												.addComponent(jLabelP1Color, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addComponent(jRB_P1ColorBlack).addComponent(jRB_P1ColorWhite))
										.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
										.addGroup(jPanel1Layout
												.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
												.addComponent(jLabelP1Alg, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addComponent(jRB_P1AlgMM).addComponent(jRB_P1AlgABP)
												.addComponent(jRB_P1AlgID).addComponent(jRB_P1AlgGS).addComponent(jRB_P1AlgRS))
										.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
										.addGroup(jPanel1Layout
												.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
												.addComponent(jLabelP1Tree, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addComponent(jSpinnerP1, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addComponent(jLabelP1Meth, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addComponent(jRB_P1Meth1).addComponent(jRB_P1Meth2)
												.addComponent(jRB_P1Meth3).addComponent(jRB_P1Meth4))
										.addGap(10)
										.addGroup(jPanel1Layout
												.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
												.addComponent(jLabelP2, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addComponent(jRB_P2Human).addComponent(jRB_P2Comp))
										.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
										.addGroup(jPanel1Layout
												.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
												.addComponent(jLabelP2Alg, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addComponent(jRB_P2AlgMM).addComponent(jRB_P2AlgABP)
												.addComponent(jRB_P2AlgID).addComponent(jRB_P2AlgGS).addComponent(jRB_P2AlgRS))
										.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
										.addGroup(jPanel1Layout
												.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
												.addComponent(jLabelP2Tree, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addComponent(jSpinnerP2, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addComponent(jLabelP2Meth, javax.swing.GroupLayout.PREFERRED_SIZE,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addComponent(jRB_P2Meth1).addComponent(jRB_P2Meth2)
												.addComponent(jRB_P2Meth3).addComponent(jRB_P2Meth4))))
						.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED).addComponent(jSeparator1,
								javax.swing.GroupLayout.PREFERRED_SIZE, 10, javax.swing.GroupLayout.PREFERRED_SIZE)
						.addContainerGap()));

		jButton3.setText("✕");
		jButton3.addActionListener(new java.awt.event.ActionListener() {
			public void actionPerformed(java.awt.event.ActionEvent evt) {
				jButton3ActionPerformed(evt);
			}
		});

		jLabel6.setBackground(javax.swing.UIManager.getDefaults().getColor("textHighlight"));
		jLabel6.setForeground(javax.swing.UIManager.getDefaults().getColor("textHighlightText"));
		jLabel6.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
		jLabel6.setText("<html><b>Game Log</b></html>");
		jLabel6.setBorder(javax.swing.BorderFactory.createLineBorder(new java.awt.Color(0, 0, 0)));
		jLabel6.setOpaque(true);

		jButton4.setText("Save");
		jButton4.addActionListener(new java.awt.event.ActionListener() {
			public void actionPerformed(java.awt.event.ActionEvent evt) {
				jButton4ActionPerformed(evt);
			}
		});

		javax.swing.GroupLayout jPanel5Layout = new javax.swing.GroupLayout(jPanel5);
		jPanel5.setLayout(jPanel5Layout);
		jPanel5Layout.setHorizontalGroup(jPanel5Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
				.addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel5Layout.createSequentialGroup()
						.addContainerGap()
						.addComponent(jLabel6, javax.swing.GroupLayout.DEFAULT_SIZE, 218, Short.MAX_VALUE)
						.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED).addComponent(jButton4)
						.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED).addComponent(jButton3)));
		jPanel5Layout.setVerticalGroup(jPanel5Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
				.addGroup(jPanel5Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
						.addComponent(jButton3).addComponent(jLabel6, javax.swing.GroupLayout.PREFERRED_SIZE, 23,
								javax.swing.GroupLayout.PREFERRED_SIZE)
						.addComponent(jButton4)));

		jList1.setBackground(javax.swing.UIManager.getDefaults().getColor("TextPane.background"));
		jList1.setSelectionMode(javax.swing.ListSelectionModel.SINGLE_SELECTION);
		jScrollPane1.setViewportView(jList1);

		javax.swing.GroupLayout jPanel4Layout = new javax.swing.GroupLayout(jPanel4);
		jPanel4.setLayout(jPanel4Layout);
		jPanel4Layout.setHorizontalGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
				.addComponent(jPanel5, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE,
						Short.MAX_VALUE)
				.addGroup(jPanel4Layout.createSequentialGroup().addGap(12, 12, 12).addComponent(jScrollPane1,
						javax.swing.GroupLayout.DEFAULT_SIZE, 295, Short.MAX_VALUE)));
		jPanel4Layout.setVerticalGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
				.addGroup(jPanel4Layout.createSequentialGroup()
						.addComponent(jPanel5, javax.swing.GroupLayout.PREFERRED_SIZE,
								javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
						.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
						.addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 276, Short.MAX_VALUE)));

		jPanel7.setLayout(new javax.swing.BoxLayout(jPanel7, javax.swing.BoxLayout.LINE_AXIS));

		javax.swing.GroupLayout boardPanel1Layout = new javax.swing.GroupLayout(boardPanel1);
		boardPanel1.setLayout(boardPanel1Layout);
		boardPanel1Layout.setHorizontalGroup(boardPanel1Layout
				.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING).addGap(0, 448, Short.MAX_VALUE));
		boardPanel1Layout.setVerticalGroup(boardPanel1Layout
				.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING).addGap(0, 308, Short.MAX_VALUE));

		jPanel7.add(boardPanel1);

		javax.swing.GroupLayout jPanel3Layout = new javax.swing.GroupLayout(jPanel3);
		jPanel3.setLayout(jPanel3Layout);
		jPanel3Layout.setHorizontalGroup(jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
				.addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE,
						Short.MAX_VALUE)
				.addGroup(javax.swing.GroupLayout.Alignment.TRAILING,
						jPanel3Layout.createSequentialGroup()
								.addComponent(jPanel7, javax.swing.GroupLayout.DEFAULT_SIZE, 448, Short.MAX_VALUE)
								.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
								.addComponent(jPanel4, javax.swing.GroupLayout.PREFERRED_SIZE,
										javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)));
		jPanel3Layout.setVerticalGroup(jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
				.addGroup(jPanel3Layout.createSequentialGroup()
						.addComponent(jPanel1, javax.swing.GroupLayout.PREFERRED_SIZE,
								javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
						.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
						.addGroup(jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
								.addComponent(jPanel7, javax.swing.GroupLayout.DEFAULT_SIZE, 308, Short.MAX_VALUE)
								.addComponent(jPanel4, javax.swing.GroupLayout.DEFAULT_SIZE,
										javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))));

		javax.swing.GroupLayout jPanel6Layout = new javax.swing.GroupLayout(jPanel6);
		jPanel6.setLayout(jPanel6Layout);
		jPanel6Layout.setHorizontalGroup(jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
				.addGroup(jPanel6Layout.createSequentialGroup().addContainerGap().addComponent(jPanel3,
						javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
						.addContainerGap()));
		jPanel6Layout.setVerticalGroup(jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
				.addGroup(jPanel6Layout.createSequentialGroup().addContainerGap().addComponent(jPanel3,
						javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
						.addContainerGap()));

		getContentPane().add(jPanel6);

		jMenu1.setText("Game");

		jMenuItem1.setText("New Game");
		jMenuItem1.addActionListener(new java.awt.event.ActionListener() {
			public void actionPerformed(java.awt.event.ActionEvent evt) {
				jMenuItem1ActionPerformed(evt);
			}
		});
		jMenu1.add(jMenuItem1);
		jMenu1.add(jSeparator2);

		jMenuItem2.setText("Exit");
		jMenuItem2.addActionListener(new java.awt.event.ActionListener() {
			public void actionPerformed(java.awt.event.ActionEvent evt) {
				jMenuItem2ActionPerformed(evt);
			}
		});
		jMenu1.add(jMenuItem2);

		jMenuBar1.add(jMenu1);

		jMenu2.setText("Edit");

		jMenuItem3.setText("Undo");
		jMenuItem3.addActionListener(new java.awt.event.ActionListener() {
			public void actionPerformed(java.awt.event.ActionEvent evt) {
				jMenuItem3ActionPerformed(evt);
			}
		});
		jMenu2.add(jMenuItem3);

		jMenuItem4.setText("Redo");
		jMenuItem4.addActionListener(new java.awt.event.ActionListener() {
			public void actionPerformed(java.awt.event.ActionEvent evt) {
				jMenuItem4ActionPerformed(evt);
			}
		});
		jMenu2.add(jMenuItem4);

		jMenuBar1.add(jMenu2);

		jMenu3.setText("View");

		jCheckBoxMenuItem1.setText("Game log");
		jCheckBoxMenuItem1.addActionListener(new java.awt.event.ActionListener() {
			public void actionPerformed(java.awt.event.ActionEvent evt) {
				jCheckBoxMenuItem1ActionPerformed(evt);
			}
		});
		jMenu3.add(jCheckBoxMenuItem1);

		jMenuBar1.add(jMenu3);

		setJMenuBar(jMenuBar1);

		pack();
	}// </editor-fold>//GEN-END:initComponents

	private void jMenuItem1ActionPerformed(java.awt.event.ActionEvent evt) {// GEN-FIRST:event_jMenuItem1ActionPerformed
		this.jPanel1.setVisible(true);
	}// GEN-LAST:event_jMenuItem1ActionPerformed

	private void jButton1ActionPerformed(java.awt.event.ActionEvent evt) {// GEN-FIRST:event_jButton1ActionPerformed
		this.jPanel1.setVisible(false);
		this.newGame();
	}// GEN-LAST:event_jButton1ActionPerformed
	
	private void automateButtActionPerformed(java.awt.event.ActionEvent evt) {// GEN-FIRST:event_automateButtActionPerformed
		P1AlgButtons[0].setSelected(true);
		P2AlgButtons[0].setSelected(true);
		P1MethButtons[0].setSelected(true);
		P2MethButtons[0].setSelected(true);
		this.automate = true;
		this.jPanel1.setVisible(false);
		this.newGame();
	}// GEN-LAST:event_automateButtActionPerformed

	private void jMenuItem2ActionPerformed(java.awt.event.ActionEvent evt) {// GEN-FIRST:event_jMenuItem2ActionPerformed
		System.exit(0);
	}// GEN-LAST:event_jMenuItem2ActionPerformed

	private void jButton2ActionPerformed(java.awt.event.ActionEvent evt) {// GEN-FIRST:event_jButton2ActionPerformed
		this.jPanel1.setVisible(false);
	}// GEN-LAST:event_jButton2ActionPerformed

	private void jMenuItem3ActionPerformed(java.awt.event.ActionEvent evt) {// GEN-FIRST:event_jMenuItem3ActionPerformed
		this.undo();
	}// GEN-LAST:event_jMenuItem3ActionPerformed

	private void jMenuItem4ActionPerformed(java.awt.event.ActionEvent evt) {// GEN-FIRST:event_jMenuItem4ActionPerformed
		this.redo();
	}// GEN-LAST:event_jMenuItem4ActionPerformed

	private void jButton3ActionPerformed(java.awt.event.ActionEvent evt) {// GEN-FIRST:event_jButton3ActionPerformed
		this.jPanel4.setVisible(false);
		this.jCheckBoxMenuItem1.setSelected(false);
	}// GEN-LAST:event_jButton3ActionPerformed

	private void jCheckBoxMenuItem1ActionPerformed(java.awt.event.ActionEvent evt) {// GEN-FIRST:event_jCheckBoxMenuItem1ActionPerformed
		this.jPanel4.setVisible(this.jCheckBoxMenuItem1.isSelected());
	}// GEN-LAST:event_jCheckBoxMenuItem1ActionPerformed

	private void jRB_P2CompItemStateChanged(java.awt.event.ItemEvent evt) {// GEN-FIRST:event_jRB_P2CompItemStateChanged
		this.setComputerAI2ControlsEnabled(evt.getStateChange() == ItemEvent.SELECTED);
	}// GEN-LAST:event_jRB_P2CompItemStateChanged
	
	private void jRB_P1CompItemStateChanged(java.awt.event.ItemEvent evt) {// GEN-FIRST:event_jRB_P2CompItemStateChanged
		this.setComputerAI1ControlsEnabled(evt.getStateChange() == ItemEvent.SELECTED);
	}// GEN-LAST:event_jRB_P2CompItemStateChanged

	private void jButton4ActionPerformed(java.awt.event.ActionEvent evt) {// GEN-FIRST:event_jButton4ActionPerformed
		this.saveGameLog();
	}// GEN-LAST:event_jButton4ActionPerformed

	public boolean getAutomate() {
		return automate;
	}
	
	public void setAutomate(boolean auto) {
		this.automate = auto;
	}
	
	public JRadioButton[] getP1AlgButtons() {
		return P1AlgButtons;
	}

	public void setP1AlgButtons(JRadioButton[] p1AlgButtons) {
		P1AlgButtons = p1AlgButtons;
	}

	public JRadioButton[] getP2AlgButtons() {
		return P2AlgButtons;
	}

	public void setP2AlgButtons(JRadioButton[] p2AlgButtons) {
		P2AlgButtons = p2AlgButtons;
	}

	public JRadioButton[] getP1MethButtons() {
		return P1MethButtons;
	}

	public void setP1MethButtons(JRadioButton[] p1MethButtons) {
		P1MethButtons = p1MethButtons;
	}

	public JRadioButton[] getP2MethButtons() {
		return P2MethButtons;
	}

	public void setP2MethButtons(JRadioButton[] p2MethButtons) {
		P2MethButtons = p2MethButtons;
	}

	public javax.swing.JPanel getjPanel1() {
		return jPanel1;
	}

	public void setjPanel1(javax.swing.JPanel jPanel1) {
		this.jPanel1 = jPanel1;
	}

	public int getI() {
		return i;
	}

	public void setI(int i) {
		this.i = i;
	}

	public int getJ() {
		return j;
	}

	public void setJ(int j) {
		this.j = j;
	}

	public int getN() {
		return n;
	}

	public void setN(int n) {
		this.n = n;
	}

	public int getM() {
		return m;
	}

	public void setM(int m) {
		this.m = m;
	}

	public MiniMax.SearchAlgorithm getAlgorithm1() {
		return algorithm1;
	}

	public void setAlgorithm1(MiniMax.SearchAlgorithm algorithm1) {
		this.algorithm1 = algorithm1;
	}

	public MiniMax.SearchAlgorithm getAlgorithm2() {
		return algorithm2;
	}

	public void setAlgorithm2(MiniMax.SearchAlgorithm algorithm2) {
		this.algorithm2 = algorithm2;
	}

	public javax.swing.JRadioButton getjRB_P1AlgRS() {
		return jRB_P1AlgRS;
	}

	public void setjRB_P1AlgRS(javax.swing.JRadioButton jRB_P1AlgRS) {
		this.jRB_P1AlgRS = jRB_P1AlgRS;
	}

	public javax.swing.JRadioButton getjRB_P1AlgMM() {
		return jRB_P1AlgMM;
	}

	public void setjRB_P1AlgMM(javax.swing.JRadioButton jRB_P1AlgMM) {
		this.jRB_P1AlgMM = jRB_P1AlgMM;
	}

	public javax.swing.JRadioButton getjRB_P2AlgRS() {
		return jRB_P2AlgRS;
	}

	public void setjRB_P2AlgRS(javax.swing.JRadioButton jRB_P2AlgRS) {
		this.jRB_P2AlgRS = jRB_P2AlgRS;
	}

	/**
	 * @param args
	 *            the command line arguments
	 */
	public static void main(String args[]) {
		java.awt.EventQueue.invokeLater(new Runnable() {

			public void run() {
				new MainWindow().setVisible(true);
			}
		});
	}

	// Variables declaration - do not modify//GEN-BEGIN:variables
	private reversi.ui.BoardPanel boardPanel1;
	private javax.swing.ButtonGroup buttonGroupColor;
	private javax.swing.ButtonGroup buttonGroupP2;
	private javax.swing.ButtonGroup buttonGroupP2Meth;
	private javax.swing.ButtonGroup buttonGroupP2Alg;
	private javax.swing.ButtonGroup buttonGroupP1;
	private javax.swing.ButtonGroup buttonGroupP1Meth;
	private javax.swing.ButtonGroup buttonGroupP1Alg;
	private javax.swing.JButton jButton1;
	private javax.swing.JButton jButton2;
	private javax.swing.JButton jButton3;
	private javax.swing.JButton jButton4;
	private javax.swing.JCheckBoxMenuItem jCheckBoxMenuItem1;
	private javax.swing.JLabel jLabelP1Color;
	private javax.swing.JLabel jLabelP2;
	private javax.swing.JLabel jLabelP2Meth;
	private javax.swing.JLabel jLabelP2Tree;
	private javax.swing.JLabel jLabel5;
	private javax.swing.JLabel jLabel6;
	private javax.swing.JLabel jLabelP2Alg;
	private javax.swing.JLabel jLabelP1;
	private javax.swing.JLabel jLabelP1Alg;
	private javax.swing.JLabel jLabelP1Meth;
	private javax.swing.JLabel jLabelP1Tree;
	private javax.swing.JList jList1;
	private javax.swing.JMenu jMenu1;
	private javax.swing.JMenu jMenu2;
	private javax.swing.JMenu jMenu3;
	private javax.swing.JMenuBar jMenuBar1;
	private javax.swing.JMenuItem jMenuItem1;
	private javax.swing.JMenuItem jMenuItem2;
	private javax.swing.JMenuItem jMenuItem3;
	private javax.swing.JMenuItem jMenuItem4;
	private javax.swing.JPanel jPanel1;
	private javax.swing.JPanel jPanelNewGame;
	private javax.swing.JPanel jPanel3;
	private javax.swing.JPanel jPanel4;
	private javax.swing.JPanel jPanel5;
	private javax.swing.JPanel jPanel6;
	private javax.swing.JPanel jPanel7;
	private javax.swing.JRadioButton jRB_P1ColorBlack;
	private javax.swing.JRadioButton jRB_P1ColorWhite;
	private javax.swing.JRadioButton jRB_P2Human;
	private javax.swing.JRadioButton jRB_P2Comp;
	private javax.swing.JRadioButton jRB_P2Meth1;
	private javax.swing.JRadioButton jRB_P2Meth2;
	private javax.swing.JRadioButton jRB_P2Meth3;
	private javax.swing.JRadioButton jRB_P2Meth4;
	private javax.swing.JRadioButton jRB_P2AlgMM;
	private javax.swing.JRadioButton jRB_P2AlgABP;
	private javax.swing.JRadioButton jRB_P2AlgRS;
	private javax.swing.JRadioButton jRB_P2AlgID;
	private javax.swing.JRadioButton jRB_P2AlgGS;
	private javax.swing.JRadioButton jRB_P1Human;
	private javax.swing.JRadioButton jRB_P1Comp;
	private javax.swing.JRadioButton jRB_P1Meth1;
	private javax.swing.JRadioButton jRB_P1Meth2;
	private javax.swing.JRadioButton jRB_P1Meth3;
	private javax.swing.JRadioButton jRB_P1Meth4;
	private javax.swing.JRadioButton jRB_P1AlgMM;
	private javax.swing.JRadioButton jRB_P1AlgABP;
	private javax.swing.JRadioButton jRB_P1AlgRS;
	private javax.swing.JRadioButton jRB_P1AlgID;
	private javax.swing.JRadioButton jRB_P1AlgGS;
	private javax.swing.JButton automateButt;
	private javax.swing.JScrollPane jScrollPane1;
	private javax.swing.JSeparator jSeparator1;
	private javax.swing.JPopupMenu.Separator jSeparator2;
	private javax.swing.JSpinner jSpinnerP2;
	private javax.swing.JSpinner jSpinnerP1;
	// End of variables declaration//GEN-END:variables
}
