import re
import random
import heapq
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
import msvcrt  # Windows-specific module for keyboard input
import time


class TextGraph:
    def __init__(self):
        self.graph = defaultdict(dict)  # Adjacency list representation
        self.nodes = set()              # All unique words/nodes
        self.pagerank = {}              # PageRank values

    def process_text(self, text):
        """Process raw text into words, ignoring punctuation and case"""
        # Replace all non-alphabetic characters with spaces and lowercase
        text = re.sub(r'[^a-zA-Z]', ' ', text).lower()
        words = text.split()
        return words

    def build_graph(self, file_path):
        """Build the directed graph from a text file"""
        try:
            with open(file_path, 'r') as file:
                text = file.read()
                words = self.process_text(text)

                if not words:
                    print("Error: File is empty or contains no valid words.")
                    return False

                # Build edges between consecutive words
                for i in range(len(words) - 1):
                    word1, word2 = words[i], words[i + 1]
                    self.nodes.add(word1)
                    self.nodes.add(word2)

                    # Update edge weight (count of consecutive occurrences)
                    if word2 in self.graph[word1]:
                        self.graph[word1][word2] += 1
                    else:
                        self.graph[word1][word2] = 1

                return True
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return False
        except Exception as e:
            print(f"Error reading file: {e}")
            return False

    def build_graph_from_text(self, text):
        """Build graph directly from a raw text string"""
        words = self.process_text(text)
        if not words:
            return False
        for i in range(len(words) - 1):
            word1, word2 = words[i], words[i + 1]
            self.nodes.add(word1)
            self.nodes.add(word2)
            self.graph[word1][word2] = self.graph[word1].get(word2, 0) + 1
        return True

    def show_directed_graph(self, save_to_file=False):
        """Display the directed graph (CLI or optionally save as image)"""
        if not self.graph:
            print("Graph is empty. Please build the graph first.")
            return

        print("\nDirected Graph Representation:")
        for source in self.graph:
            for target, weight in self.graph[source].items():
                print(f"{source} -> {target} [weight={weight}]")

        # Optional: Save as image using NetworkX and Matplotlib
        if save_to_file:
            try:
                nx_graph = nx.DiGraph()
                for source in self.graph:
                    for target, weight in self.graph[source].items():
                        nx_graph.add_edge(source, target, weight=weight)

                plt.figure(figsize=(12, 8))
                pos = nx.spring_layout(nx_graph)
                nx.draw(nx_graph, pos, with_labels=True, node_size=2000, node_color='skyblue',
                        font_size=10, font_weight='bold', arrowsize=20)
                edge_labels = nx.get_edge_attributes(nx_graph, 'weight')
                nx.draw_networkx_edge_labels(
                    nx_graph, pos, edge_labels=edge_labels)

                plt.title("Directed Graph Visualization")
                plt.savefig("graph_visualization.png")
                print("\nGraph visualization saved as 'graph_visualization.png'")
            except Exception as e:
                print(f"Warning: Could not generate graph image. {e}")

    def query_bridge_words(self, word1, word2):
        """Find bridge words between word1 and word2"""
        word1 = word1.lower()
        word2 = word2.lower()

        if word1 not in self.nodes or word2 not in self.nodes:
            return f"No {word1} or {word2} in the graph!"

        bridge_words = []
        # Find all words that word1 points to
        if word1 in self.graph:
            for potential_bridge in self.graph[word1]:
                # Check if potential_bridge points to word2
                if word2 in self.graph.get(potential_bridge, {}):
                    bridge_words.append(potential_bridge)

        if not bridge_words:
            return f"No bridge words from {word1} to {word2}!"
        else:
            bridge_list = ", ".join(bridge_words[:-1])
            if len(bridge_words) > 1:
                bridge_list += f" and {bridge_words[-1]}"
            else:
                bridge_list = bridge_words[0]
            return f"The bridge words from {word1} to {word2} are: {bridge_list}."

    def generate_new_text(self, input_text):
        """Generate new text by inserting bridge words"""
        words = self.process_text(input_text)

        if not words:  # ✅ 加这一句来防止访问空列表
            return ""

        new_text = []

        for i in range(len(words) - 1):
            word1, word2 = words[i], words[i + 1]
            new_text.append(word1)

            # Find bridge words
            bridge_words = []
            if word1 in self.graph:
                for potential_bridge in self.graph[word1]:
                    if word2 in self.graph.get(potential_bridge, {}):
                        bridge_words.append(potential_bridge)

            # Insert a random bridge word if any exist
            if bridge_words:
                new_text.append(random.choice(bridge_words))

        new_text.append(words[-1])  # Add the last word
        return ' '.join(new_text)

    def calc_shortest_path(self, word1, word2=None):
        """Calculate shortest path between two words or from one word to all others"""
        word1 = word1.lower()
        if word2:
            word2 = word2.lower()

        if word1 not in self.nodes:
            return f"{word1} not found in graph!"
        if word2 and word2 not in self.nodes:
            return f"{word2} not found in graph!"

        # Dijkstra's algorithm
        distances = {node: float('inf') for node in self.nodes}
        distances[word1] = 0
        previous = {node: None for node in self.nodes}
        visited = set()

        priority_queue = [(0, word1)]

        while priority_queue:
            current_dist, current_node = heapq.heappop(priority_queue)

            if current_node in visited:
                continue
            visited.add(current_node)

            if word2 and current_node == word2:
                break

            for neighbor, weight in self.graph.get(current_node, {}).items():
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        # Handle single word case (find all shortest paths from word1)
        if not word2:
            result = []
            for target in self.nodes:
                if target != word1 and distances[target] != float('inf'):
                    path = []
                    node = target
                    while node is not None:
                        path.append(node)
                        node = previous[node]
                    path.reverse()
                    result.append(
                        f"Shortest path from {word1} to {target}: {
                            ' -> '.join(path)} (length: {
                            distances[target]})")
            return '\n'.join(
                result) if result else f"No paths found from {word1} to other nodes."

        # Handle two word case
        if distances[word2] == float('inf'):
            return f"No path exists from {word1} to {word2}!"

        # Reconstruct path
        path = []
        node = word2
        while node is not None:
            path.append(node)
            node = previous[node]
        path.reverse()

        return f"Shortest path from {word1} to {word2}: {' -> '.join(path)} (length: {distances[word2]})"

    def calc_pagerank(self, word=None, damping=0.85, iterations=100):
        """Calculate PageRank for all nodes or a specific node"""
        if not self.graph:
            return "Graph is empty. Please build the graph first."

        # Initialize PR values
        N = len(self.nodes)
        pr = {node: 1 / N for node in self.nodes}

        for _ in range(iterations):
            new_pr = {}
            # Calculate total PR from dangling nodes (nodes with no outgoing
            # edges)
            dangling_pr = 0
            for node in self.nodes:
                # Node is dangling if it has no outgoing edges or isn't in the
                # graph as a source
                if node not in self.graph or not self.graph[node]:
                    dangling_pr += pr[node]
            # Distribute dangling PR equally among all nodes
            dangling_contribution = dangling_pr / N if N > 0 else 0

            for node in self.nodes:
                # Calculate sum of PR of incoming nodes divided by their
                # out-degree
                incoming_sum = 0
                for incoming_node in [
                        n for n in self.graph if node in self.graph[n]]:
                    outgoing_links = sum(self.graph[incoming_node].values())
                    if outgoing_links > 0:
                        incoming_sum += pr[incoming_node] * \
                            (self.graph[incoming_node][node] / outgoing_links)

                # Apply PageRank formula with dangling node contribution
                new_pr[node] = (1 - damping) / N + damping * \
                    (incoming_sum + dangling_contribution)

            pr = new_pr

        self.pagerank = pr

        if word:
            word = word.lower()
            if word in self.pagerank:
                return f"PageRank for '{word}': {self.pagerank[word]:.4f}"
            else:
                return f"Word '{word}' not found in graph."
        else:
            # Return top 10 nodes by PageRank
            sorted_pr = sorted(
                self.pagerank.items(),
                key=lambda x: x[1],
                reverse=True)
            result = "Top 10 nodes by PageRank:\n"
            for i, (node, score) in enumerate(sorted_pr[:10], 1):
                result += f"{i}. {node}: {score:.4f}\n"
            return result

    def random_walk(self):
        """Perform a random walk until a repeated edge is encountered or no outgoing edges"""
        if not self.graph:
            return "Graph is empty. Please build the graph first."

        # Choose a random starting node
        current_node = random.choice(list(self.graph.keys()))
        path = [current_node]
        visited_edges = set()

        print("Random walk started. Press Enter to stop at any time.")

        try:
            while True:
                # Check if current node has outgoing edges
                if current_node not in self.graph or not self.graph[current_node]:
                    print(
                        f"Stopping: Node '{current_node}' has no outgoing edges.")
                    break

                # Get all possible next nodes and their weights
                next_nodes = list(self.graph[current_node].items())
                total_weight = sum(weight for _, weight in next_nodes)

                # Choose next node based on edge weights
                rand_val = random.uniform(0, total_weight)
                cumulative = 0
                for node, weight in next_nodes:
                    cumulative += weight
                    if rand_val <= cumulative:
                        next_node = node
                        break

                # Check if we've seen this edge before
                edge = (current_node, next_node)
                if edge in visited_edges:
                    print(
                        f"Stopping: Repeated edge {current_node} -> {next_node} encountered.")
                    break
                visited_edges.add(edge)

                # Move to next node
                current_node = next_node
                path.append(current_node)

                # Check for user input to stop (Windows-compatible)
                if self._check_user_stop():
                    print("User stopped the random walk.")
                    break

                # Small delay to allow user input
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\nUser stopped the random walk.")

        # Save to file
        walk_text = ' '.join(path)
        try:
            with open('random_walk.txt', 'w') as f:
                f.write(walk_text)
            print("Random walk path saved to 'random_walk.txt'")
        except Exception as e:
            print(f"Error saving random walk: {e}")

        return walk_text

    def _check_user_stop(self):
        """Check if user wants to stop the random walk (Windows-compatible)"""
        return msvcrt.kbhit() and msvcrt.getch() == b'\r'  # Enter key pressed


def main():
    print("=== Text Graph Processor ===")
    graph = TextGraph()

    # Get input file
    while True:
        file_path = input(
            "\nEnter the path to the text file (or 'q' to quit): ").strip()
        if file_path.lower() == 'q':
            return

        if graph.build_graph(file_path):
            break

    while True:
        print("\n=== Menu ===")
        print("1. Show directed graph")
        print("2. Query bridge words")
        print("3. Generate new text with bridge words")
        print("4. Calculate shortest path")
        print("5. Calculate PageRank")
        print("6. Perform random walk")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            save = input(
                "Save graph visualization to file? (y/n): ").lower() == 'y'
            graph.show_directed_graph(save_to_file=save)

        elif choice == '2':
            word1 = input("Enter first word: ").strip()
            word2 = input("Enter second word: ").strip()
            print(graph.query_bridge_words(word1, word2))

        elif choice == '3':
            text = input("Enter a line of text: ").strip()
            print("Generated text:", graph.generate_new_text(text))

        elif choice == '4':
            word1 = input("Enter starting word: ").strip()
            word2 = input(
                "Enter target word (leave blank for all reachable nodes): ").strip()
            if word2:
                print(graph.calc_shortest_path(word1, word2))
            else:
                print(graph.calc_shortest_path(word1))

        elif choice == '5':
            word = input(
                "Enter a word to get its PageRank (leave blank for top 10): ").strip()
            print(graph.calc_pagerank(word if word else None))

        elif choice == '6':
            print("Random walk result:", graph.random_walk())

        elif choice == '7':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
