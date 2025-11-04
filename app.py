import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Patch, Circle
import networkx as nx
import time
from collections import deque
import heapq

# Page config
st.set_page_config(
    page_title="Graph Search Visualizer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1976D2;
        text-align: center;
        padding: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        height: 3rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

class GraphSearchVisualizer:
    def __init__(self):
        # Create graph structure
        self.graph = nx.Graph()
        
        # Define edges from the image - nodes 0-14
        edges = [
            (0, 4), (1, 4), (2, 5), (3, 5),
            (4, 6), (5, 6), (6, 7), (7, 8),
            (8, 9), (8, 10), (9, 11), (9, 12),
            (10, 13), (10, 14),
        ]
        
        self.graph.add_edges_from(edges)
        
        # Define start and goal nodes
        self.start_node = 0
        self.goal_node = 14
        
        # Position nodes for visualization
        self.pos = {
            0: (0, 1), 1: (0, 2), 2: (0, 0), 3: (0, -1),
            4: (1, 1.5), 5: (1, -0.5), 6: (2, 0.5), 7: (3, 0.5),
            8: (4, 0.5), 9: (5, 1.5), 10: (5, -0.5),
            11: (6, 2), 12: (6, 1), 13: (6, 0), 14: (6, -1),
        }
        
        # Static node-to-letter mapping (A-P for nodes 0-14)
        self.node_to_letter = {}
        for i, node in enumerate(sorted(self.graph.nodes())):
            self.node_to_letter[node] = chr(65 + i)
    
    def draw_graph(self, highlight_visited=None, highlight_path=None, 
                   highlight_current=None, highlight_path_edges=None,
                   visited_order_list=None, forward_visited=None, backward_visited=None):
        """Draw the graph with optional highlighting"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Draw solution path edges first
        if highlight_path_edges:
            path_edge_list = list(zip(highlight_path_edges[:-1], highlight_path_edges[1:]))
            nx.draw_networkx_edges(self.graph, self.pos, ax=ax,
                                  edgelist=path_edge_list,
                                  edge_color='#D32F2F', width=5, alpha=0.9, style='solid',
                                  arrows=True, arrowsize=20, arrowstyle='->')
        
        # Draw all edges
        nx.draw_networkx_edges(self.graph, self.pos, ax=ax, 
                              edge_color='#666666', width=2.5, alpha=0.7, style='solid')
        
        # Draw nodes
        node_colors = []
        for node in self.graph.nodes():
            if node == self.start_node:
                node_colors.append('#FF8C00')
            elif node == self.goal_node:
                node_colors.append('#FF8C00')
            elif (forward_visited and node in forward_visited and 
                  backward_visited and node in backward_visited):
                node_colors.append('#FF1493')
            elif forward_visited and node in forward_visited:
                node_colors.append('#4169E1')
            elif backward_visited and node in backward_visited:
                node_colors.append('#32CD32')
            elif highlight_visited and node in highlight_visited:
                node_colors.append('#90EE90')
            elif highlight_current and node == highlight_current:
                node_colors.append('#FFD700')
            elif highlight_path and node in highlight_path:
                node_colors.append('#FF6347')
            else:
                node_colors.append('#87CEEB')
        
        nx.draw_networkx_nodes(self.graph, self.pos, ax=ax,
                              node_color=node_colors, node_size=2500,
                              alpha=0.98, edgecolors='black', linewidths=3)
        
        # Create mapping for visited nodes
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
        
        # Draw labels
        labels = {}
        for node in self.graph.nodes():
            letter = self.node_to_letter[node]
            if node == self.start_node:
                label_text = f"{letter}\nSTART"
            elif node == self.goal_node:
                label_text = f"{letter}\nGOAL"
            else:
                label_text = letter
            labels[node] = label_text
        
        nx.draw_networkx_labels(self.graph, self.pos, labels, ax=ax,
                               font_size=14, font_weight='bold', 
                               font_color='white', font_family='Arial')
        
        # Draw visit numbers above visited nodes
        if visited_order_map:
            for node in visited_order_map.keys():
                x, y = self.pos[node]
                visit_num = visited_order_map[node]
                circle = Circle((x, y + 0.4), 0.18, color='#D32F2F', fill=True, 
                              zorder=5, edgecolor='white', linewidth=2)
                ax.add_patch(circle)
                ax.text(x, y + 0.4, str(visit_num), fontsize=11, fontweight='bold',
                       color='white', ha='center', va='center', zorder=6)
                ax.text(x + 0.3, y + 0.4, '✕', fontsize=18, fontweight='bold',
                       color='#D32F2F', ha='center', va='center', zorder=6)
        
        # Add legend
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
            ax.legend(handles=legend_elements, loc='upper left', 
                     fontsize=10, framealpha=0.95, fancybox=True,
                     shadow=True, edgecolor='#333333', facecolor='white')
        
        ax.set_title('🔍 Graph Search Visualizer', fontsize=20, fontweight='bold', 
                    pad=25, color='#1976D2')
        ax.axis('off')
        ax.set_facecolor('#FAFAFA')
        
        plt.tight_layout()
        return fig

# Initialize visualizer
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = GraphSearchVisualizer()
    st.session_state.visited_order = []
    st.session_state.solution_path = []
    st.session_state.animation_running = False

visualizer = st.session_state.visualizer

# Header
st.markdown('<div class="main-header">🔍 Graph Search Visualizer</div>', unsafe_allow_html=True)

# Sidebar for controls
with st.sidebar:
    st.header("🎮 Controls")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 DFS", use_container_width=True, type="primary"):
            st.session_state.algorithm = "DFS"
            st.session_state.animation_running = True
            st.rerun()
        
        if st.button("🔄 Bidirectional", use_container_width=True):
            st.session_state.algorithm = "Bidirectional"
            st.session_state.animation_running = True
            st.rerun()
    
    with col2:
        if st.button("🔍 BFS", use_container_width=True):
            st.session_state.algorithm = "BFS"
            st.session_state.animation_running = True
            st.rerun()
        
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.visited_order = []
            st.session_state.solution_path = []
            st.session_state.animation_running = False
            st.rerun()
    
    st.markdown("---")
    st.info("👆 اختر خوارزمية البحث من الأزرار أعلاه")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Run algorithm if selected
    if st.session_state.get('algorithm') and st.session_state.animation_running:
        algorithm = st.session_state.algorithm
        st.session_state.animation_running = False
        
        if algorithm == "DFS":
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
            
            visited_order, solution_path = dfs(visualizer.graph, visualizer.start_node, visualizer.goal_node)
            st.session_state.visited_order = visited_order
            st.session_state.solution_path = solution_path
        
        elif algorithm == "BFS":
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
            
            visited_order, solution_path = bfs(visualizer.graph, visualizer.start_node, visualizer.goal_node)
            st.session_state.visited_order = visited_order
            st.session_state.solution_path = solution_path
        
        elif algorithm == "Bidirectional":
            def bidirectional_search(graph, start, goal):
                forward_queue = deque([(start, [start])])
                forward_visited = {start: [start]}
                forward_visited_set = {start}
                
                backward_queue = deque([(goal, [goal])])
                backward_visited = {goal: [goal]}
                backward_visited_set = {goal}
                
                intersection = None
                forward_intersection_path = []
                backward_intersection_path = []
                
                while forward_queue or backward_queue:
                    if forward_queue:
                        current, current_path = forward_queue.popleft()
                        forward_visited_set.add(current)
                        
                        if current in backward_visited_set:
                            intersection = current
                            forward_intersection_path = current_path
                            backward_intersection_path = backward_visited[current][::-1]
                            break
                        
                        for neighbor in sorted(graph.neighbors(current)):
                            if neighbor not in forward_visited:
                                forward_visited[neighbor] = current_path + [neighbor]
                                forward_visited_set.add(neighbor)
                                forward_queue.append((neighbor, current_path + [neighbor]))
                    
                    if backward_queue:
                        current, current_path = backward_queue.popleft()
                        backward_visited_set.add(current)
                        
                        if current in forward_visited_set:
                            intersection = current
                            forward_intersection_path = forward_visited[current]
                            backward_intersection_path = current_path[::-1]
                            break
                        
                        for neighbor in sorted(graph.neighbors(current)):
                            if neighbor not in backward_visited:
                                backward_visited[neighbor] = current_path + [neighbor]
                                backward_visited_set.add(neighbor)
                                backward_queue.append((neighbor, current_path + [neighbor]))
                
                if intersection:
                    solution_path = forward_intersection_path[:-1] + backward_intersection_path
                    visited_all = list(set(list(forward_visited_set) + list(backward_visited_set)))
                    return visited_all, solution_path, forward_visited_set, backward_visited_set
                
                visited_all = list(set(list(forward_visited_set) + list(backward_visited_set)))
                return visited_all, [], forward_visited_set, backward_visited_set
            
            result = bidirectional_search(visualizer.graph, visualizer.start_node, visualizer.goal_node)
            if len(result) == 4:
                visited_order, solution_path, forward_visited, backward_visited = result
                st.session_state.visited_order = visited_order
                st.session_state.solution_path = solution_path
                st.session_state.forward_visited = forward_visited
                st.session_state.backward_visited = backward_visited
            else:
                st.session_state.visited_order = []
                st.session_state.solution_path = []
    
    # Draw graph
    visited_order = st.session_state.get('visited_order', [])
    solution_path = st.session_state.get('solution_path', [])
    forward_visited = st.session_state.get('forward_visited', set())
    backward_visited = st.session_state.get('backward_visited', set())
    
    visited_set = set(visited_order) if visited_order else set()
    
    fig = visualizer.draw_graph(
        highlight_visited=visited_set if not forward_visited else None,
        highlight_path=solution_path,
        highlight_path_edges=solution_path if solution_path else None,
        visited_order_list=visited_order,
        forward_visited=forward_visited if forward_visited else None,
        backward_visited=backward_visited if backward_visited else None
    )
    
    st.pyplot(fig)
    
    # Algorithm info
    if visited_order:
        algorithm_name = st.session_state.get('algorithm', 'Unknown')
        st.success(f"✅ {algorithm_name} completed! Found {len(visited_order)} visited nodes.")
        if solution_path:
            path_letters = [visualizer.node_to_letter[node] for node in solution_path]
            st.info(f"🎯 Solution Path: {' → '.join(path_letters)} ({len(solution_path)-1} edges)")

with col2:
    st.header("📝 Tested Path List")
    
    visited_order = st.session_state.get('visited_order', [])
    solution_path = st.session_state.get('solution_path', [])
    
    if visited_order:
        tested_path_text = "═══ TESTED PATH ═══\n"
        tested_path_text += "════════════════════════════════\n\n"
        tested_path_text += "📋 Exploration Order:\n"
        tested_path_text += "─" * 35 + "\n"
        
        for idx, node in enumerate(visited_order):
            letter = visualizer.node_to_letter[node]
            if (idx + 1) % 5 == 0:
                tested_path_text += f"{idx+1:2d}. {letter:2s} ({node:2d})\n"
            else:
                tested_path_text += f"{idx+1:2d}. {letter:2s} ({node:2d})  "
                if idx == len(visited_order) - 1:
                    tested_path_text += "\n"
        
        tested_path_text += "─" * 35 + "\n"
        tested_path_text += f"📊 Total Nodes Tested: {len(visited_order)}\n"
        tested_path_text += "════════════════════════════════\n"
        
        if solution_path:
            tested_path_text += "\n═══ SOLUTION PATH ═══\n"
            tested_path_text += "════════════════════════════════\n"
            tested_path_text += "✅ Path Found:\n"
            tested_path_text += "─" * 35 + "\n"
            path_letters = [visualizer.node_to_letter[node] for node in solution_path]
            tested_path_text += " → ".join(path_letters) + "\n"
            tested_path_text += "─" * 35 + "\n"
            for idx, node in enumerate(solution_path):
                letter = visualizer.node_to_letter[node]
                tested_path_text += f"{idx+1}. {letter} (Node {node})\n"
            tested_path_text += "─" * 35 + "\n"
            tested_path_text += f"📏 Path Length: {len(solution_path)-1} edges\n"
            tested_path_text += "════════════════════════════════\n"
        
        st.code(tested_path_text, language=None)
    else:
        st.info("⏳ No nodes tested yet.\n\n👆 Click a search algorithm button to start the search.")

# Footer
st.markdown("---")
st.markdown("**Graph Search Visualizer** - Created with ❤️ using Streamlit")

