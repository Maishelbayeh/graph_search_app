import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Button
import networkx as nx
import time
from collections import deque
import heapq

class GraphSearchVisualizer:
    def __init__(self):
        # Create graph structure based on the image
        self.graph = nx.Graph()
        
        # Define edges from the image - nodes 0-14
        edges = [
            (0, 4),      # Node 0 to node 4
            (1, 4),      # Node 1 to node 4
            (2, 5),      # Node 2 to node 5
            (3, 5),      # Node 3 to node 5
            (4, 6),      # Node 4 to node 6
            (5, 6),      # Node 5 to node 6
            (6, 7),      # Node 6 to node 7
            (7, 8),      # Node 7 to node 8
            (8, 9),      # Node 8 to node 9
            (8, 10),     # Node 8 to node 10
            (9, 11),     # Node 9 to node 11
            (9, 12),     # Node 9 to node 12
            (10, 13),    # Node 10 to node 13
            (10, 14),    # Node 10 to node 14
        ]
        
        self.graph.add_edges_from(edges)
        
        # Define start and goal nodes
        self.start_node = 0  # Start node (left side)
        self.goal_node = 14  # Goal node (right side)
        
        # Setup matplotlib figure with subplots
        self.fig = plt.figure(figsize=(16, 10))
        self.fig.canvas.manager.set_window_title('Graph Search Visualizer')
        
        # Main graph area (left side)
        self.ax = plt.subplot2grid((1, 2), (0, 0), colspan=1, fig=self.fig)
        
        # Text area for tested path (right side)
        self.ax_text = plt.subplot2grid((1, 2), (0, 1), fig=self.fig)
        self.ax_text.axis('off')
        
        # Position nodes for visualization - horizontal layout with branches
        self.pos = {
            0: (0, 1),    # Left branch
            1: (0, 2),    # Left branch
            2: (0, 0),    # Left branch
            3: (0, -1),   # Left branch
            4: (1, 1.5),  # Left middle
            5: (1, -0.5), # Left middle
            6: (2, 0.5),  # Center left
            7: (3, 0.5),  # Center
            8: (4, 0.5),  # Center right
            9: (5, 1.5),  # Right middle
            10: (5, -0.5), # Right middle
            11: (6, 2),   # Right branch
            12: (6, 1),   # Right branch
            13: (6, 0),   # Right branch
            14: (6, -1),  # Right branch (goal)
        }
        
        # Static node-to-letter mapping (A-P for nodes 0-14)
        self.node_to_letter = {}
        for i, node in enumerate(sorted(self.graph.nodes())):
            self.node_to_letter[node] = chr(65 + i)  # A, B, C, D, ...
        
        # Animation state
        self.visited_nodes = set()
        self.exploration_path = []
        self.solution_path = []
        self.current_animation = None
        
        # Draw initial graph
        self.draw_graph(visited_order_list=None)
        
        # Create buttons
        self.create_buttons()
        
    def draw_graph(self, highlight_visited=None, highlight_path=None, 
                   highlight_current=None, highlight_path_edges=None,
                   visited_order_list=None, forward_visited=None, backward_visited=None):
        """Draw the graph with optional highlighting"""
        self.ax.clear()
        
        # Draw solution path edges first (if provided) with thicker red lines
        if highlight_path_edges:
            path_edge_list = list(zip(highlight_path_edges[:-1], highlight_path_edges[1:]))
            nx.draw_networkx_edges(self.graph, self.pos, ax=self.ax,
                                  edgelist=path_edge_list,
                                  edge_color='#D32F2F', width=5, alpha=0.9, style='solid',
                                  arrows=True, arrowsize=20, arrowstyle='->')
        
        # Draw all edges - better styling
        nx.draw_networkx_edges(self.graph, self.pos, ax=self.ax, 
                              edge_color='#666666', width=2.5, alpha=0.7, style='solid')
        
        # Draw nodes
        node_colors = []
        for node in self.graph.nodes():
            if node == self.start_node:
                node_colors.append('#FF8C00')  # Orange for start
            elif node == self.goal_node:
                node_colors.append('#FF8C00')  # Orange for goal
            # Bidirectional search - intersection node (visited by both)
            elif (forward_visited and node in forward_visited and 
                  backward_visited and node in backward_visited):
                node_colors.append('#FF1493')  # Deep pink for intersection
            # Bidirectional search - different colors for forward and backward
            elif forward_visited and node in forward_visited:
                node_colors.append('#4169E1')  # Royal blue for forward search
            elif backward_visited and node in backward_visited:
                node_colors.append('#32CD32')  # Lime green for backward search
            elif highlight_visited and node in highlight_visited:
                node_colors.append('#90EE90')  # Light green for visited
            elif highlight_current and node == highlight_current:
                node_colors.append('#FFD700')  # Gold for current
            elif highlight_path and node in highlight_path:
                node_colors.append('#FF6347')  # Tomato red for solution path
            else:
                node_colors.append('#87CEEB')  # Light blue for unvisited
        
        nx.draw_networkx_nodes(self.graph, self.pos, ax=self.ax,
                              node_color=node_colors, node_size=2500,
                              alpha=0.98, edgecolors='black', linewidths=3)
        
        # Create mapping for visited nodes (visit order number)
        visited_order_map = {}
        if visited_order_list:
            for idx, node in enumerate(visited_order_list):
                if node not in visited_order_map:
                    visited_order_map[node] = idx + 1
        
        # Create mapping for solution path numbers
        solution_path_numbers = {}
        if highlight_path:
            for idx, node in enumerate(highlight_path):
                solution_path_numbers[node] = idx + 1
        
        # Draw labels with static letters
        labels = {}
        for node in self.graph.nodes():
            letter = self.node_to_letter[node]  # Static letter (A, B, C, ...)
            
            # Build label text - cleaner format
            if node == self.start_node:
                label_text = f"{letter}\nSTART"
            elif node == self.goal_node:
                label_text = f"{letter}\nGOAL"
            else:
                label_text = letter
            
            labels[node] = label_text
        
        nx.draw_networkx_labels(self.graph, self.pos, labels, ax=self.ax,
                               font_size=14, font_weight='bold', 
                               font_color='white', font_family='Arial')
        
        # Draw visit numbers above visited nodes - better design
        if visited_order_map:
            for node in visited_order_map.keys():
                x, y = self.pos[node]
                visit_num = visited_order_map[node]
                # Draw visit number in a circle above the node
                circle = plt.Circle((x, y + 0.4), 0.18, color='#D32F2F', fill=True, 
                                  zorder=5, edgecolor='white', linewidth=2)
                self.ax.add_patch(circle)
                self.ax.text(x, y + 0.4, str(visit_num), fontsize=11, fontweight='bold',
                           color='white', ha='center', va='center', zorder=6)
                # Draw X mark next to the number
                self.ax.text(x + 0.3, y + 0.4, '✕', fontsize=18, fontweight='bold',
                           color='#D32F2F', ha='center', va='center', zorder=6)
        
        # Draw solution path numbers (if different from visit numbers)
        if solution_path_numbers:
            for node in solution_path_numbers.keys():
                if node not in visited_order_map:  # Only if not already marked
                    x, y = self.pos[node]
                    path_num = solution_path_numbers[node]
                    circle = plt.Circle((x, y + 0.4), 0.18, color='#B71C1C', fill=True, 
                                      zorder=5, edgecolor='white', linewidth=2)
                    self.ax.add_patch(circle)
                    self.ax.text(x, y + 0.4, str(path_num), fontsize=11, fontweight='bold',
                               color='white', ha='center', va='center', zorder=6)
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = []
        if forward_visited or backward_visited:
            legend_elements = [
                Patch(facecolor='#4169E1', label='Forward Search'),
                Patch(facecolor='#32CD32', label='Backward Search'),
                Patch(facecolor='#FF1493', label='Intersection'),
            ]
        elif highlight_visited:
            legend_elements = [
                Patch(facecolor='#87CEEB', label='Unvisited'),
                Patch(facecolor='#90EE90', label='Visited'),
                Patch(facecolor='#FFD700', label='Current'),
                Patch(facecolor='#FF6347', label='Solution Path'),
            ]
        else:
            legend_elements = [
                Patch(facecolor='#87CEEB', label='Unvisited Node'),
                Patch(facecolor='#FF8C00', label='Start/Goal'),
            ]
        
        if legend_elements:
            self.ax.legend(handles=legend_elements, loc='upper left', 
                          fontsize=10, framealpha=0.95, fancybox=True,
                          shadow=True, edgecolor='#333333', facecolor='white')
        
        self.ax.set_title('🔍 Graph Search Visualizer', fontsize=20, fontweight='bold', 
                         pad=25, color='#1976D2')
        self.ax.axis('off')
        # Add subtle background
        self.ax.set_facecolor('#FAFAFA')
        
        # Update tested path display
        self.update_tested_path_display(visited_order_list)
        
        plt.tight_layout()
    
    def update_tested_path_display(self, visited_order_list=None):
        """Display the tested path (exploration path) in a text box"""
        self.ax_text.clear()
        self.ax_text.axis('off')
        
        if visited_order_list and len(visited_order_list) > 0:
            # Format the tested path using static node letters - better organized
            tested_path_text = "═══ TESTED PATH ═══\n"
            tested_path_text += "════════════════════════════════\n\n"
            tested_path_text += "📋 Exploration Order:\n"
            tested_path_text += "─" * 35 + "\n"
            
            # Group nodes in rows for better readability
            for idx, node in enumerate(visited_order_list):
                letter = self.node_to_letter[node]  # Static letter
                if (idx + 1) % 5 == 0:
                    tested_path_text += f"{idx+1:2d}. {letter:2s} ({node:2d})\n"
                else:
                    tested_path_text += f"{idx+1:2d}. {letter:2s} ({node:2d})  "
                    if idx == len(visited_order_list) - 1:
                        tested_path_text += "\n"
            
            tested_path_text += "\n" + "─" * 35 + "\n"
            tested_path_text += f"📊 Total Nodes Tested: {len(visited_order_list)}\n"
            tested_path_text += "════════════════════════════════\n"
            
            # Display the text with better styling
            self.ax_text.text(0.05, 0.95, tested_path_text, 
                            transform=self.ax_text.transAxes,
                            fontsize=10, 
                            verticalalignment='top',
                            fontfamily='monospace',
                            bbox=dict(boxstyle='round,pad=1', facecolor='#f0f8ff', 
                                    edgecolor='#4169e1', linewidth=2, alpha=0.95))
            self.ax_text.set_title('📝 Tested Path List', fontsize=16, fontweight='bold', 
                                  pad=20, color='#4169e1')
        else:
            self.ax_text.text(0.5, 0.5, "═══ TESTED PATH ═══\n\n" + 
                            "════════════════════════════════\n\n" +
                            "⏳ No nodes tested yet.\n\n" +
                            "👆 Click a search algorithm button\n" +
                            "   to start the search.\n\n" +
                            "════════════════════════════════",
                            transform=self.ax_text.transAxes,
                            fontsize=11,
                            verticalalignment='center',
                            horizontalalignment='center',
                            fontfamily='monospace',
                            bbox=dict(boxstyle='round,pad=1', facecolor='#f5f5f5', 
                                    edgecolor='#cccccc', linewidth=2, alpha=0.9))
            self.ax_text.set_title('📝 Tested Path List', fontsize=16, fontweight='bold', 
                                  pad=20, color='#666666')
        
    def create_buttons(self):
        """Create control buttons with better styling"""
        # Button positions - centered at bottom (4 buttons now)
        button_width = 0.15
        button_height = 0.07
        button_spacing = 0.02
        total_width = 4 * button_width + 3 * button_spacing
        start_x = (1 - total_width) / 2  # Center buttons
        start_y = 0.01
        
        # DFS Button
        ax_dfs = plt.axes([start_x, start_y, button_width, button_height])
        self.btn_dfs = Button(ax_dfs, '🔍 DFS', color='#2196F3', hovercolor='#1976D2')
        self.btn_dfs.on_clicked(lambda x: self.run_dfs())
        
        # BFS Button
        ax_bfs = plt.axes([start_x + button_width + button_spacing, start_y, 
                          button_width, button_height])
        self.btn_bfs = Button(ax_bfs, '🔍 BFS', color='#4CAF50', hovercolor='#388E3C')
        self.btn_bfs.on_clicked(lambda x: self.run_bfs())
        
        # Bidirectional Button
        ax_bidir = plt.axes([start_x + 2*(button_width + button_spacing), start_y,
                            button_width, button_height])
        self.btn_bidir = Button(ax_bidir, '🔄 Bidirectional', color='#9C27B0', hovercolor='#7B1FA2')
        self.btn_bidir.on_clicked(lambda x: self.run_bidirectional())
        
        # Reset Button
        ax_reset = plt.axes([start_x + 3*(button_width + button_spacing), start_y,
                            button_width, button_height])
        self.btn_reset = Button(ax_reset, '🔄 Reset', color='#F44336', hovercolor='#D32F2F')
        self.btn_reset.on_clicked(lambda x: self.reset())
    
    def reset(self):
        """Reset the visualization"""
        self.visited_nodes = set()
        self.exploration_path = []
        self.solution_path = []
        self.draw_graph(visited_order_list=None)
        self.update_tested_path_display(None)
        plt.draw()
    
    def animate_bidirectional_search(self, animation_frames, solution_path, 
                                     forward_visited_set, backward_visited_set):
        """Animate bidirectional search with different colors for forward and backward"""
        visited_order = []
        
        # Animate exploration
        for i, frame in enumerate(animation_frames):
            current = frame['current']
            direction = frame['direction']
            forward_visited = frame['forward']
            backward_visited = frame['backward']
            
            if current:
                visited_order.append(current)
            
            # Create letter mapping for visited nodes (remove duplicates)
            visited_all = list(set(list(forward_visited) + list(backward_visited)))
            visited_to_letter = {}
            for idx, node in enumerate(visited_all):
                if node not in visited_to_letter:
                    visited_to_letter[node] = chr(65 + len(visited_to_letter))
            
            self.draw_graph(highlight_visited=None,
                          highlight_current=current,
                          highlight_path=[],
                          highlight_path_edges=None,
                          visited_order_list=visited_all,
                          forward_visited=forward_visited,
                          backward_visited=backward_visited)
            
            dir_text = "Forward" if direction == 'forward' else "Backward"
            if current is not None:
                self.ax.set_title(f'Bidirectional Search - {dir_text} exploring Node {current} '
                                f'({i+1}/{len(animation_frames)})', 
                                fontsize=14, fontweight='bold')
            else:
                self.ax.set_title(f'Bidirectional Search - {dir_text} search '
                                f'({i+1}/{len(animation_frames)})', 
                                fontsize=14, fontweight='bold')
            
            # Add legend for bidirectional search
            if forward_visited or backward_visited:
                from matplotlib.patches import Patch
                legend_elements = [
                    Patch(facecolor='#4169E1', label='Forward Search'),
                    Patch(facecolor='#32CD32', label='Backward Search'),
                    Patch(facecolor='#FF1493', label='Intersection'),
                    Patch(facecolor='#FF8C00', label='Start/Goal'),
                    Patch(facecolor='#FFD700', label='Current Node')
                ]
                self.ax.legend(handles=legend_elements, loc='upper right', fontsize=9)
            
            # Update tested path display for bidirectional search
            # Show forward and backward separately - better organized
            tested_path_text = "═══ TESTED PATH ═══\n"
            tested_path_text += "════════════════════════════════\n\n"
            
            tested_path_text += "🔵 FORWARD SEARCH:\n"
            tested_path_text += "─" * 35 + "\n"
            forward_nodes = sorted(list(forward_visited))
            for idx, node in enumerate(forward_nodes):
                letter = self.node_to_letter[node]
                if (idx + 1) % 4 == 0:
                    tested_path_text += f"{idx+1:2d}. {letter:2s} ({node:2d})\n"
                else:
                    tested_path_text += f"{idx+1:2d}. {letter:2s} ({node:2d})  "
                    if idx == len(forward_nodes) - 1:
                        tested_path_text += "\n"
            
            tested_path_text += "\n🟢 BACKWARD SEARCH:\n"
            tested_path_text += "─" * 35 + "\n"
            backward_nodes = sorted(list(backward_visited))
            for idx, node in enumerate(backward_nodes):
                letter = self.node_to_letter[node]
                if (idx + 1) % 4 == 0:
                    tested_path_text += f"{idx+1:2d}. {letter:2s} ({node:2d})\n"
                else:
                    tested_path_text += f"{idx+1:2d}. {letter:2s} ({node:2d})  "
                    if idx == len(backward_nodes) - 1:
                        tested_path_text += "\n"
            
            tested_path_text += "─" * 35 + "\n"
            tested_path_text += f"📊 Forward: {len(forward_nodes)} | Backward: {len(backward_nodes)}\n"
            tested_path_text += f"📊 Total: {len(visited_all)} nodes\n"
            tested_path_text += "════════════════════════════════"
            
            self.ax_text.clear()
            self.ax_text.axis('off')
            self.ax_text.text(0.05, 0.95, tested_path_text,
                            transform=self.ax_text.transAxes,
                            fontsize=9,
                            verticalalignment='top',
                            fontfamily='monospace',
                            bbox=dict(boxstyle='round,pad=1', facecolor='#f0f8ff', 
                                    edgecolor='#4169e1', linewidth=2, alpha=0.95))
            self.ax_text.set_title('📝 Tested Path List', fontsize=16, fontweight='bold', 
                                  pad=20, color='#4169e1')
            
            plt.draw()
            plt.pause(0.5)
        
        # Show final solution path with numbered sequence
        if solution_path:
            # Animate solution path with numbers
            for step in range(len(solution_path)):
                path_so_far = solution_path[:step+1]
                visited_all = list(set(list(forward_visited_set) + list(backward_visited_set)))
                self.draw_graph(highlight_visited=None,
                              highlight_path=path_so_far,
                              highlight_path_edges=path_so_far,
                              visited_order_list=visited_all,
                              forward_visited=forward_visited_set,
                              backward_visited=backward_visited_set)
                path_letters = [self.node_to_letter[node] for node in path_so_far]
                self.ax.set_title(f'Bidirectional Search - Solution Path: '
                                f'{" → ".join(path_letters)} '
                                f'({step+1}/{len(solution_path)})', 
                                fontsize=12, fontweight='bold')
                # Update tested path display
                self.update_tested_path_display(visited_all)
                plt.draw()
                plt.pause(0.4)
            
            # Final display
            visited_all = list(set(list(forward_visited_set) + list(backward_visited_set)))
            self.draw_graph(highlight_visited=None,
                          highlight_path=solution_path,
                          highlight_path_edges=solution_path,
                          visited_order_list=visited_all,
                          forward_visited=forward_visited_set,
                          backward_visited=backward_visited_set)
            solution_path_letters = [self.node_to_letter[node] for node in solution_path]
            self.ax.set_title(f'Bidirectional Search - Solution Path Found! '
                            f'Path: {" → ".join(solution_path_letters)} '
                            f'({len(solution_path)-1} edges)', 
                            fontsize=14, fontweight='bold')
            
            # Update tested path display with solution path info - better format
            solution_info = "\n\n═══ SOLUTION PATH ═══\n"
            solution_info += "════════════════════════════════\n"
            solution_info += "✅ Path Found:\n"
            solution_info += "─" * 35 + "\n"
            path_letters = [self.node_to_letter[node] for node in solution_path]
            solution_info += " → ".join(path_letters) + "\n"
            solution_info += "─" * 35 + "\n"
            for idx, node in enumerate(solution_path):
                letter = self.node_to_letter[node]
                solution_info += f"{idx+1}. {letter} (Node {node})\n"
            solution_info += "─" * 35 + "\n"
            solution_info += f"📏 Path Length: {len(solution_path)-1} edges\n"
            solution_info += "════════════════════════════════\n"
            
            # Show both tested path and solution path
            tested_path_text = "═══ TESTED PATH ═══\n"
            tested_path_text += "════════════════════════════════\n\n"
            
            tested_path_text += "🔵 FORWARD SEARCH:\n"
            tested_path_text += "─" * 35 + "\n"
            forward_nodes = sorted(list(forward_visited_set))
            for idx, node in enumerate(forward_nodes):
                letter = self.node_to_letter[node]
                if (idx + 1) % 4 == 0:
                    tested_path_text += f"{idx+1:2d}. {letter:2s} ({node:2d})\n"
                else:
                    tested_path_text += f"{idx+1:2d}. {letter:2s} ({node:2d})  "
                    if idx == len(forward_nodes) - 1:
                        tested_path_text += "\n"
            
            tested_path_text += "\n🟢 BACKWARD SEARCH:\n"
            tested_path_text += "─" * 35 + "\n"
            backward_nodes = sorted(list(backward_visited_set))
            for idx, node in enumerate(backward_nodes):
                letter = self.node_to_letter[node]
                if (idx + 1) % 4 == 0:
                    tested_path_text += f"{idx+1:2d}. {letter:2s} ({node:2d})\n"
                else:
                    tested_path_text += f"{idx+1:2d}. {letter:2s} ({node:2d})  "
                    if idx == len(backward_nodes) - 1:
                        tested_path_text += "\n"
            
            tested_path_text += "─" * 35 + "\n"
            tested_path_text += f"📊 Forward: {len(forward_nodes)} | Backward: {len(backward_nodes)}\n"
            tested_path_text += f"📊 Total: {len(visited_all)} nodes\n"
            tested_path_text += solution_info
            
            self.ax_text.clear()
            self.ax_text.axis('off')
            self.ax_text.text(0.05, 0.95, tested_path_text,
                            transform=self.ax_text.transAxes,
                            fontsize=9,
                            verticalalignment='top',
                            fontfamily='monospace',
                            bbox=dict(boxstyle='round,pad=1', facecolor='#f0f8ff', 
                                    edgecolor='#32cd32', linewidth=2, alpha=0.95))
            self.ax_text.set_title('📝 Tested Path & Solution', fontsize=16, 
                                  fontweight='bold', pad=20, color='#32cd32')
            
            plt.draw()
            plt.pause(1.5)
    
    def animate_search(self, visited_order, solution_path, algorithm_name):
        """Animate the search process"""
        visited_set = set()
        
        # Animate exploration
        for i, node in enumerate(visited_order):
            visited_set.add(node)
            # Get visited order up to current point for letter mapping
            current_visited_order = visited_order[:i+1]
            self.draw_graph(highlight_visited=visited_set, 
                          highlight_current=node,
                          highlight_path=[],
                          highlight_path_edges=None,
                          visited_order_list=current_visited_order)
            letter = self.node_to_letter[node]  # Static letter
            self.ax.set_title(f'{algorithm_name} - Exploring Node {letter} (Node {node}) '
                            f'({i+1}/{len(visited_order)})', 
                            fontsize=14, fontweight='bold')
            # Update tested path display
            self.update_tested_path_display(current_visited_order)
            plt.draw()
            plt.pause(0.5)
        
        # Show final solution path with numbered sequence
        if solution_path:
            # Animate solution path with numbers
            for step in range(len(solution_path)):
                path_so_far = solution_path[:step+1]
                self.draw_graph(highlight_visited=visited_set,
                              highlight_path=path_so_far,
                              highlight_path_edges=path_so_far,
                              visited_order_list=visited_order)
                path_letters = [self.node_to_letter[node] for node in path_so_far]
                self.ax.set_title(f'{algorithm_name} - Solution Path: '
                                f'{" → ".join(path_letters)} '
                                f'({step+1}/{len(solution_path)})', 
                                fontsize=12, fontweight='bold')
                # Update tested path display
                self.update_tested_path_display(visited_order)
                plt.draw()
                plt.pause(0.4)
            
            # Final display
            self.draw_graph(highlight_visited=visited_set,
                          highlight_path=solution_path,
                          highlight_path_edges=solution_path,
                          visited_order_list=visited_order)
            solution_path_letters = [self.node_to_letter[node] for node in solution_path]
            self.ax.set_title(f'{algorithm_name} - Solution Path Found! '
                            f'Path: {" → ".join(solution_path_letters)} '
                            f'({len(solution_path)-1} edges)', 
                            fontsize=14, fontweight='bold')
            # Update tested path display with solution path info
            solution_info = "\n\n═══ SOLUTION PATH ═══\n"
            solution_info += "════════════════════════════════\n"
            solution_info += "✅ Path Found:\n"
            solution_info += "─" * 35 + "\n"
            path_letters = [self.node_to_letter[node] for node in solution_path]
            solution_info += " → ".join(path_letters) + "\n"
            solution_info += "─" * 35 + "\n"
            for idx, node in enumerate(solution_path):
                letter = self.node_to_letter[node]
                solution_info += f"{idx+1}. {letter} (Node {node})\n"
            solution_info += "─" * 35 + "\n"
            solution_info += f"📏 Path Length: {len(solution_path)-1} edges\n"
            solution_info += "════════════════════════════════\n"
            
            # Combine with tested path
            tested_path_text = "═══ TESTED PATH ═══\n"
            tested_path_text += "════════════════════════════════\n\n"
            tested_path_text += "📋 Exploration Order:\n"
            tested_path_text += "─" * 35 + "\n"
            for idx, node in enumerate(visited_order):
                letter = self.node_to_letter[node]
                if (idx + 1) % 5 == 0:
                    tested_path_text += f"{idx+1:2d}. {letter:2s} ({node:2d})\n"
                else:
                    tested_path_text += f"{idx+1:2d}. {letter:2s} ({node:2d})  "
                    if idx == len(visited_order) - 1:
                        tested_path_text += "\n"
            tested_path_text += "─" * 35 + "\n"
            tested_path_text += f"📊 Total: {len(visited_order)} nodes\n"
            tested_path_text += solution_info
            
            self.ax_text.clear()
            self.ax_text.axis('off')
            self.ax_text.text(0.05, 0.95, tested_path_text,
                            transform=self.ax_text.transAxes,
                            fontsize=9,
                            verticalalignment='top',
                            fontfamily='monospace',
                            bbox=dict(boxstyle='round,pad=1', facecolor='#f0f8ff', 
                                    edgecolor='#32cd32', linewidth=2, alpha=0.95))
            self.ax_text.set_title('📝 Tested Path & Solution', fontsize=16, 
                                  fontweight='bold', pad=20, color='#32cd32')
            plt.draw()
            plt.pause(1.5)
    
    def run_dfs(self):
        """Run Depth-First Search"""
        self.reset()
        
        def dfs(graph, start, goal):
            visited = set()
            path = []
            solution_path = []
            
            def dfs_recursive(node, current_path):
                if node in visited:
                    return False
                
                visited.add(node)
                path.append(node)
                current_path = current_path + [node]
                
                if node == goal:
                    solution_path[:] = current_path[:]
                    return True
                
                for neighbor in sorted(graph.neighbors(node)):
                    if neighbor not in visited:
                        if dfs_recursive(neighbor, current_path):
                            return True
                
                return False
            
            dfs_recursive(start, [])
            return path, solution_path
        
        visited_order, solution_path = dfs(self.graph, self.start_node, self.goal_node)
        self.animate_search(visited_order, solution_path, 'Depth-First Search (DFS)')
    
    def run_bfs(self):
        """Run Breadth-First Search"""
        self.reset()
        
        def bfs(graph, start, goal):
            queue = deque([(start, [start])])
            visited = set([start])
            path = [start]
            
            while queue:
                current, current_path = queue.popleft()
                
                if current == goal:
                    return path, current_path
                
                for neighbor in sorted(graph.neighbors(current)):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        path.append(neighbor)
                        queue.append((neighbor, current_path + [neighbor]))
            
            return path, []
        
        visited_order, solution_path = bfs(self.graph, self.start_node, self.goal_node)
        self.animate_search(visited_order, solution_path, 'Breadth-First Search (BFS)')
    
    def run_bidirectional(self):
        """Run Bidirectional Search with alternating animation and different colors"""
        self.reset()
        
        def bidirectional_search_animated(graph, start, goal):
            # Forward search from start
            forward_queue = deque([(start, [start])])
            forward_visited = {start: [start]}
            forward_path = [start]
            forward_visited_set = {start}
            
            # Backward search from goal
            backward_queue = deque([(goal, [goal])])
            backward_visited = {goal: [goal]}
            backward_path = [goal]
            backward_visited_set = {goal}
            
            intersection = None
            forward_intersection_path = []
            backward_intersection_path = []
            visited_order = []  # Track order of exploration with direction
            
            # Animation frames
            animation_frames = []
            
            while forward_queue or backward_queue:
                # Forward step
                if forward_queue:
                    current, current_path = forward_queue.popleft()
                    forward_visited_set.add(current)
                    
                    if current not in [n for n, _ in visited_order]:
                        visited_order.append((current, 'forward'))
                    
                    # Save frame for animation
                    animation_frames.append({
                        'forward': set(forward_visited_set),
                        'backward': set(backward_visited_set),
                        'current': current,
                        'direction': 'forward'
                    })
                    
                    if current in backward_visited_set:
                        intersection = current
                        forward_intersection_path = current_path
                        backward_intersection_path = backward_visited[current][::-1]
                        break
                    
                    for neighbor in sorted(graph.neighbors(current)):
                        if neighbor not in forward_visited:
                            forward_visited[neighbor] = current_path + [neighbor]
                            forward_path.append(neighbor)
                            forward_visited_set.add(neighbor)
                            forward_queue.append((neighbor, current_path + [neighbor]))
                            if neighbor not in [n for n, _ in visited_order]:
                                visited_order.append((neighbor, 'forward'))
                    
                    # Save frame after exploring neighbors
                    animation_frames.append({
                        'forward': set(forward_visited_set),
                        'backward': set(backward_visited_set),
                        'current': None,
                        'direction': 'forward'
                    })
                
                # Backward step
                if backward_queue:
                    current, current_path = backward_queue.popleft()
                    backward_visited_set.add(current)
                    
                    if current not in [n for n, _ in visited_order]:
                        visited_order.append((current, 'backward'))
                    
                    # Save frame for animation
                    animation_frames.append({
                        'forward': set(forward_visited_set),
                        'backward': set(backward_visited_set),
                        'current': current,
                        'direction': 'backward'
                    })
                    
                    if current in forward_visited_set:
                        intersection = current
                        forward_intersection_path = forward_visited[current]
                        backward_intersection_path = current_path[::-1]
                        break
                    
                    for neighbor in sorted(graph.neighbors(current)):
                        if neighbor not in backward_visited:
                            backward_visited[neighbor] = current_path + [neighbor]
                            backward_path.append(neighbor)
                            backward_visited_set.add(neighbor)
                            backward_queue.append((neighbor, current_path + [neighbor]))
                            if neighbor not in [n for n, _ in visited_order]:
                                visited_order.append((neighbor, 'backward'))
                    
                    # Save frame after exploring neighbors
                    animation_frames.append({
                        'forward': set(forward_visited_set),
                        'backward': set(backward_visited_set),
                        'current': None,
                        'direction': 'backward'
                    })
            
            # Combine paths
            if intersection:
                solution_path = forward_intersection_path[:-1] + backward_intersection_path
                return animation_frames, solution_path, forward_visited_set, backward_visited_set
            
            return animation_frames, [], forward_visited_set, backward_visited_set
        
        animation_frames, solution_path, forward_visited_set, backward_visited_set = bidirectional_search_animated(
            self.graph, self.start_node, self.goal_node)
        
        # Animate bidirectional search
        self.animate_bidirectional_search(animation_frames, solution_path, 
                                         forward_visited_set, backward_visited_set)
    
    def show(self):
        """Display the visualization"""
        plt.show()

if __name__ == '__main__':
    visualizer = GraphSearchVisualizer()
    visualizer.show()

