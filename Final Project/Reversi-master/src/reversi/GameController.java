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
package reversi;

import java.util.ArrayDeque;
import java.util.Iterator;
import java.util.Vector;
import ai.MiniMax;
import reversi.ai.ReversiEvaluator;
import reversi.exceptions.InvalidMoveException;
import reversi.ui.MainWindow;
import reversi.ai.ReversiNode;

public class GameController implements IdleObject {
    
    private int currentPlayerColour;
    private Board board;
    private GameView view;
    private int player1Colour;
    private boolean isP1Human;
    private boolean isP2Human;
    private long waitFor;
    private int maxDepth1;
    private int maxDepth2;
    private MiniMax.SearchAlgorithm algorithm1;
    private MiniMax.SearchAlgorithm algorithm2;
    private ReversiEvaluator.EvaluationMethod evalMethod1;
    private ReversiEvaluator.EvaluationMethod evalMethod2;
    private ArrayDeque<HistoryItem> history;
    private ArrayDeque<HistoryItem> future;
    private Vector<GameUndoRedoListener> gameUndoRedoListeners;
    private boolean undoRedoAllowed;
    private Vector<GameLogger> gameLoggers;
    private MainWindow mainWindow;

    public GameController() {
        this.currentPlayerColour = Utils.BLACK;
        this.board = null;
        this.view = null;
        this.player1Colour = this.currentPlayerColour;
        this.waitFor = Utils.WAIT_FOR_MILLIS;
        this.maxDepth2 = Utils.MAX_DEPTH;
        this.isP1Human = true;
        this.isP2Human = false;
        this.algorithm2 = MiniMax.SearchAlgorithm.ALPHA_BETA_PRUNING;
        this.evalMethod2 = ReversiEvaluator.EvaluationMethod.VALID_MOVES_AND_SIDES_COUNT;

        this.history = new ArrayDeque<HistoryItem>();
        this.future = new ArrayDeque<HistoryItem>();
        this.gameUndoRedoListeners = new Vector<GameUndoRedoListener>();
        this.undoRedoAllowed = true;

        this.gameLoggers = new Vector<GameLogger>();
    }

    public GameController(int playerColour, int maxDepth, long waitForMillis) {
        if ((playerColour == Utils.BLACK) || (playerColour == Utils.WHITE)) {
            this.player1Colour = playerColour;
        } else {
            this.player1Colour = Utils.BLACK;
        }
        this.currentPlayerColour = Utils.BLACK;
        this.waitFor = waitForMillis;
        this.maxDepth2 = maxDepth;
        this.board = null;
        this.view = null;
        this.isP1Human = true;
        this.isP2Human = false;
        this.algorithm2 = MiniMax.SearchAlgorithm.ALPHA_BETA_PRUNING;
        this.evalMethod2 = ReversiEvaluator.EvaluationMethod.VALID_MOVES_AND_SIDES_COUNT;

        this.history = new ArrayDeque<HistoryItem>();
        this.future = new ArrayDeque<HistoryItem>();
        this.gameUndoRedoListeners = new Vector<GameUndoRedoListener>();
        this.undoRedoAllowed = true;

        this.gameLoggers = new Vector<GameLogger>();
    }

    public GameController(MainWindow mw, boolean isP1Human, boolean isP2Human, int P1Color, Board b, GameView view, int maxDepth1, int maxDepth2, MiniMax.SearchAlgorithm algorithm1, MiniMax.SearchAlgorithm algorithm2, ReversiEvaluator.EvaluationMethod evalMethod1, ReversiEvaluator.EvaluationMethod evalMethod2, long waitForMillis) {
        this.mainWindow = mw;
    	if ((P1Color == Utils.BLACK) || (P1Color == Utils.WHITE)) {
            this.player1Colour = P1Color;
        } else {
            this.player1Colour = Utils.BLACK;
        }
        this.currentPlayerColour = Utils.BLACK;
        this.isP1Human = isP1Human;
        this.isP2Human = isP2Human;
        this.maxDepth1 = maxDepth1;
        this.maxDepth2 = maxDepth2;
        this.algorithm1 = algorithm1;
        this.algorithm2 = algorithm2;
        this.evalMethod1 = evalMethod1;
        this.evalMethod2 = evalMethod2;
        this.waitFor = waitForMillis;
        this.gameUndoRedoListeners = new Vector<GameUndoRedoListener>();
        this.gameLoggers = new Vector<GameLogger>();
        this.setBoard(b);
        this.setGameView(view);
        this.undoRedoAllowed = true;
    }

    public void setBoard(Board b) {
        this.board = b;

        this.history = new ArrayDeque<HistoryItem>();
        this.future = new ArrayDeque<HistoryItem>();

        if (this.view != null) {
            this.view.setBoard(b);
        }
    }

    public void setGameView(GameView v) {
        this.view = v;
        if (this.view != null) {
            this.view.setController(this);
            this.view.setBoard(this.board);
        }
    }

    public int getCurrentPlayerColour() {
        return this.currentPlayerColour;
    }

    public void startGame() {
        notifyGameLoggers(GameLogger.GameLoggerEvent.GAME_STARTED, null);
        if ((!this.isP1Human) && (this.player1Colour == Utils.BLACK)) {
            this.AI1StartMove();
        } else if ((!this.isP2Human) && (this.player1Colour == Utils.WHITE)) {
        	this.AI2StartMove();
        }
    }

    private void AI1StartMove() {
        this.undoRedoAllowed = false;
        this.notifyGameUndoRedoListeners();
        this.view.setAI1IsPlaying(true);
        ReversiNode n = new ReversiNode(this.board.getState(), this.currentPlayerColour);
        AIPlayer tmp = new AIPlayer(this, n, this.maxDepth1, this.algorithm1, this.evalMethod1, this.waitFor);
        tmp.start();
    }
    
    private void AI2StartMove() {
        this.undoRedoAllowed = false;
        this.notifyGameUndoRedoListeners();
        this.view.setAI2IsPlaying(true);
        ReversiNode n = new ReversiNode(this.board.getState(), this.currentPlayerColour);
        AIPlayer tmp = new AIPlayer(this, n, this.maxDepth2, this.algorithm2, this.evalMethod2, this.waitFor);
        tmp.start();
    }

    public void AIEndMove(ReversiNode n) throws InvalidMoveException {
        Move next = (Move)n.getNextMove();
        if (next != null) {
            this.play(next.getX(), next.getY());            
        }
        
        if (this.view.getAI1IsPlaying()) {
        	this.view.setAI1IsPlaying(false);
        }
        if (this.view.getAI2IsPlaying()) {
        	this.view.setAI2IsPlaying(false);
        }
        
        this.undoRedoAllowed = true;
        this.notifyGameUndoRedoListeners();
    }

    public void play(int x, int y) {
        if (this.board != null) {
            if (!this.board.isTheGameOver()) {
                State prev = new State(this.board.getState());

                try {
                    this.board.put(x, y, this.currentPlayerColour);
                    this.history.push(new HistoryItem(prev, this.currentPlayerColour));
                    this.future.clear();
                    this.notifyGameUndoRedoListeners();
                    this.notifyGameLoggers(GameLogger.GameLoggerEvent.NEW_MOVE, new Move(x, y, this.currentPlayerColour));

                    this.changePlayer();
                    this.view.notifyGameChanged(this);

                    if((this.board.getValidMoves(currentPlayerColour).size() == 0)&&(!this.board.isTheGameOver())){
                        this.skipTurn();
                    }

                    if ((!this.isP1Human) && (this.currentPlayerColour == player1Colour)&&(!this.board.isTheGameOver())) {
                        this.AI1StartMove();
                    } else if ((!this.isP2Human) && (this.currentPlayerColour != player1Colour)&&(!this.board.isTheGameOver())) {
                        this.AI2StartMove();
                    }

                } catch (InvalidMoveException ime) {
                    System.err.println(ime.toString());
                }
            }
            if (this.board.isTheGameOver() && mainWindow.getAutomate()) {
            	mainWindow.automateNext();
            	mainWindow.getjPanel1().setVisible(false);
            	if (mainWindow.getAutomate()) {
        			mainWindow.newGame();
            	}
            }
        }
    }

    private void changePlayer() {
        this.currentPlayerColour = Utils.getOpponentsColour(this.currentPlayerColour);
    }

    private void skipTurn() {
        String playerName = Utils.getPlayerName(this.currentPlayerColour);
        this.showNoMovesAlert(playerName);
    }

    public void resume() {
        this.view.setPlayerHasNoMovesAvailable(false, "");
        this.changePlayer();
        this.view.notifyGameChanged(this);
        if ((!this.isP1Human) && (this.player1Colour == Utils.BLACK)) {
            this.AI1StartMove();
        } else if ((!this.isP2Human) && (this.player1Colour == Utils.WHITE)) {
        	this.AI2StartMove();
        }
    }

    private void showNoMovesAlert(String playerName) {
        this.view.setPlayerHasNoMovesAvailable(true, playerName);
        IdleTimeConsumer p = new IdleTimeConsumer(this, 2000);
        p.start();
    }

    public void undo() {
        if (this.undoRedoAllowed) {
            if (!this.history.isEmpty()) {
                this.future.push(new HistoryItem(new State(this.board.getState()), this.currentPlayerColour));
                HistoryItem i = this.history.pop();
                this.board.setState(i.getState());
                this.currentPlayerColour = i.getPlayer();
                //System.out.println("Now playing: " + Utils.getPlayerName(this.currentPlayerColour));
                this.view.notifyGameChanged(this);
                this.notifyGameUndoRedoListeners();
                this.notifyGameLoggers(GameLogger.GameLoggerEvent.UNDO, null);
            }
        }
    }

    public void redo() {
        if (this.undoRedoAllowed) {
            if (!this.future.isEmpty()) {
                this.history.push(new HistoryItem(new State(this.board.getState()), this.currentPlayerColour));
                HistoryItem i = this.future.pop();
                this.board.setState(i.getState());
                this.currentPlayerColour = i.getPlayer();
                this.view.notifyGameChanged(this);
                this.notifyGameUndoRedoListeners();
                this.notifyGameLoggers(GameLogger.GameLoggerEvent.REDO, null);
            }
        }
    }

    public boolean canUndo() {
        return (!this.history.isEmpty() && this.undoRedoAllowed);
    }

    public boolean canRedo() {
        return (!this.future.isEmpty() && this.undoRedoAllowed);
    }

    public void addGameUndoRedoListener(GameUndoRedoListener listener) {
        this.gameUndoRedoListeners.add(listener);
    }

    public void removeGameUndoRedoListener(GameUndoRedoListener listener) {
        this.gameUndoRedoListeners.remove(listener);
    }

    public void notifyGameUndoRedoListeners() {
        for (Iterator<GameUndoRedoListener> it = gameUndoRedoListeners.iterator(); it.hasNext();) {
            GameUndoRedoListener listener = it.next();
            listener.undoableEventHappened();
        }
    }

    public void addGameLogger(GameLogger logger) {
        this.gameLoggers.add(logger);
    }

    public void removeGameLogger(GameLogger logger) {
        this.gameLoggers.remove(logger);
    }

    private void notifyGameLoggers(GameLogger.GameLoggerEvent evt, Object param) {

        for (Iterator<GameLogger> it = gameLoggers.iterator(); it.hasNext();) {
            GameLogger gameLogger = it.next();
            if (evt.equals(GameLogger.GameLoggerEvent.GAME_STARTED)) {
                gameLogger.newGameStarted();
            } else if (evt.equals(GameLogger.GameLoggerEvent.GAME_OVER)) {
                System.out.println("game over");
            	gameLogger.gameOver();
            } else if (evt.equals(GameLogger.GameLoggerEvent.NEW_MOVE)) {
                gameLogger.newMove((Move) param);
            } else if (evt.equals(GameLogger.GameLoggerEvent.UNDO)) {
                gameLogger.moveUndone();
            } else {
                gameLogger.moveRedone();
            }
        }

    }

    private void printHistory() {
        for (Iterator<HistoryItem> it = history.iterator(); it.hasNext();) {
            State state = it.next().getState();
            state.print(System.out);
        }
    }
}
