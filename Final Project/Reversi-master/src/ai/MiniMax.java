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
package ai;

import java.util.ArrayDeque;
import java.util.Random;
import java.util.Timer;
import java.util.Vector;

import ai.Node.NodeType;
import reversi.ai.ReversiNode;

public class MiniMax {
	static int seconds;
	static Timer timer = new Timer();

	public enum SearchAlgorithm {

		RANDOM_SEARCH, MINIMAX, ALPHA_BETA_PRUNING, ITERATIVE_DEEP, GREEDY_SEARCH
	}

	public void apply(Node n, int maxDepth, SearchAlgorithm algorithm, Evaluator eval) {

		if (algorithm == SearchAlgorithm.MINIMAX) {
			minimax(n, maxDepth, eval);
		} else if (algorithm == SearchAlgorithm.ALPHA_BETA_PRUNING) {
			alphaBetaPruning(n, maxDepth, eval);
		} else if (algorithm == SearchAlgorithm.RANDOM_SEARCH) {
			randomSearch(n);
		} else if (algorithm == SearchAlgorithm.GREEDY_SEARCH) {
			greedySearch(n, eval);
		} else if (algorithm == SearchAlgorithm.ITERATIVE_DEEP) {
			iterativeDeep(n, eval, 5000);
		}
	}

	// Randomly chooses moves
	private void randomSearch(Node n) {

		Vector<Node> children = n.getChildren();
		if (children.size() == 0) {
			// no possible moves
			return;
		}
		int random_index = new Random().nextInt(children.size());
		Node next_node = children.get(random_index);
		Move next_move = next_node.getMoveLeadingHere();
		n.setNextMove(next_move);
	}

	// Chooses the move which increases the score (based on evaluation method)
	// the most
	private void greedySearch(Node n, Evaluator eval) {
		if (n.isEndGameNode()) {
			System.out.println("H1");
			return;
		}
		Vector<Node> children = n.getChildren();
		if (children.size() == 0) {
			// no possible moves
			return;
		}
		int maxVal = eval.evaluate(children.get(0));
		Vector<Node> choices = new Vector<Node>(children.size());
		choices.add(children.get(0));
		for (int i = 1; i < children.size(); i++) {
			if (maxVal < eval.evaluate(children.get(i))) {
				choices.removeAllElements();
				choices.add(children.get(i));
			} else if (maxVal == eval.evaluate(children.get(i))) {
				choices.add(children.get(i));
			}
		}
		int random_index = new Random().nextInt(choices.size());
		Node next_node = children.get(random_index);
		Move next_move = next_node.getMoveLeadingHere();
		n.setNextMove(next_move);
	}

	private void minimax(Node n, int maxDepth, Evaluator eval) {

		if (n.isEndGameNode()) {
			System.out.println("H1");
			return;
		}
		ArrayDeque<Node> searchStack = new ArrayDeque<Node>();
		searchStack.push(n);

		while (searchStack.isEmpty() == false) {
			Node node = searchStack.pop();

			Move nextMove = node.getNextMove();
			boolean isRoot = node.isRoot();

			if (node.isTerminal(maxDepth)) {
				node.setValue(eval.evaluate(node));
				if (!isRoot) {
					Node parent = node.getParent();
					if (parent.setValue(node.getValue())) {
						parent.setNextMove(node.getMoveLeadingHere());
					}
				}
			} else {
				if (node.hasMoreChildren()) {
					searchStack.push(node);
					searchStack.push(node.getNextChild());
				} else {
					if (nextMove != null) {
						if (!isRoot) {
							Node parent = node.getParent();
							if (parent.setValue(node.getValue())) {
								parent.setNextMove(node.getMoveLeadingHere());
							}
						}
					}
				}
			}

			node.setVisited(true);
			// print(node);
		}
	}

	private void alphaBetaPruning(Node n, int maxDepth, Evaluator eval) {
		if (n.isEndGameNode()) {
			System.out.println("H1");
			return;
		}
		ArrayDeque<Node> searchStack = new ArrayDeque<Node>();
		searchStack.push(n);

		while (searchStack.isEmpty() == false) {

			Node node = searchStack.pop();

			Move nextMove = node.getNextMove();
			boolean isRoot = node.isRoot();

			if (node.isTerminal(maxDepth)) {
				node.setValue(eval.evaluate(node));
				if (!isRoot) {
					Node parent = node.getParent();
					if (parent.setValue(node.getValue())) {
						parent.setNextMove(node.getMoveLeadingHere());
					}
				}
			} else {
				if (node.hasMoreChildren()) {
					if (!isRoot) {
						Integer nodeValue = node.getValue();
						if (nodeValue != null) {
							Node parent = node.getParent();
							Integer parentValue = parent.getValue();
							if (parentValue == null) {
								searchStack.push(node);
								searchStack.push(node.getNextChild());
							} else {
								NodeType type = parent.getType();
								if (type == NodeType.MAX) {
									// Pruning:
									if (node.getValue() >= parentValue) {
										searchStack.push(node);
										searchStack.push(node.getNextChild());
									}
								} else {
									// Pruning:
									if (node.getValue() <= parentValue) {
										searchStack.push(node);
										searchStack.push(node.getNextChild());
									}
								}
							}
						} else {
							searchStack.push(node);
							searchStack.push(node.getNextChild());
						}
					} else {
						searchStack.push(node);
						searchStack.push(node.getNextChild());
					}
				} else {
					if (nextMove != null) {
						if (!isRoot) {
							Node parent = node.getParent();
							if (parent.setValue(node.getValue())) {
								parent.setNextMove(node.getMoveLeadingHere());
							}
						}
					}
				}
			}

			// node.setVisited(true);
			// print(node);
		}
	}

	// Iterative deepening function. Is time based instead of
	private void iterativeDeep(Node n, Evaluator eval, int time_limit) {

		long startTime = System.currentTimeMillis();

		int i = 1;
		ReversiNode temp = new ReversiNode(((ReversiNode) n).getState(), ((ReversiNode) n).getCurrentPlayer());
		ReversiNode temp2 = new ReversiNode(((ReversiNode) n).getState(), ((ReversiNode) n).getCurrentPlayer());

		while ((System.currentTimeMillis() - startTime) <= time_limit) {

			temp2 = new ReversiNode(((ReversiNode) temp).getState(), ((ReversiNode) temp).getCurrentPlayer());
			long startTrackTime = System.currentTimeMillis();
			this.alphaBetaPruning(temp2, i, eval);
			long endTrackTime = System.currentTimeMillis();
			long difference = endTrackTime - startTrackTime;

			System.out.println("Difference: " + difference + " Time Remaining: "
					+ (time_limit - (System.currentTimeMillis() - startTime)));
			if (3 * difference >= time_limit - (System.currentTimeMillis() - startTime)) {
				break;
			}

			i++;
		}

		n.Gclone(temp2);

	}

	public Node deepClone(Node n) {
		return n.Gclone(n);
	}

	private void print(Node n) {
		System.out.println(n.toString());
	}
}
