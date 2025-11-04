import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Patch, Circle
import networkx as nx
import time
from collections import deque
import heapq

# Page config - Responsive
st.set_page_config(
    page_title="Graph Search Visualizer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# Professional CSS styling for AI Master's level design
st.markdown("""
    <style>
    /* Responsive Design - Base Styles */
    * {
        box-sizing: border-box;
    }
    
    /* Main Header - Responsive */
    .main-header {
        font-size: clamp(1.8rem, 5vw, 2.8rem);
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: clamp(0.8rem, 2vw, 1.5rem) 0;
        margin-bottom: clamp(0.5rem, 2vw, 1rem);
        letter-spacing: -0.5px;
    }
    
    /* Button Styling - Responsive */
    .stButton>button {
        width: 100%;
        height: clamp(2.5rem, 5vw, 2.8rem);
        font-size: clamp(0.85rem, 2vw, 1rem);
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Sidebar Header Styling - Responsive */
    .sidebar .sidebar-content h2 {
        font-size: clamp(1.2rem, 3vw, 1.5rem);
        margin-bottom: clamp(0.5rem, 2vw, 1rem);
    }
    
    /* Sidebar Subheader Styling - Responsive */
    .sidebar .sidebar-content h3 {
        font-size: clamp(0.95rem, 2.5vw, 1.1rem);
        margin-top: clamp(0.5rem, 2vw, 1rem);
        margin-bottom: clamp(0.3rem, 1vw, 0.5rem);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Main Container - Responsive Padding */
    .main .block-container {
        padding-top: clamp(1rem, 3vw, 2rem);
        padding-bottom: clamp(1rem, 3vw, 2rem);
        padding-left: clamp(1rem, 3vw, 2rem);
        padding-right: clamp(1rem, 3vw, 2rem);
    }
    
    /* Info Boxes - Responsive */
    .stInfo {
        background-color: #e8f4f8;
        border-left: 4px solid #2196F3;
        padding: clamp(0.7rem, 2vw, 1rem);
        border-radius: 4px;
        font-size: clamp(0.85rem, 2vw, 1rem);
    }
    
    /* Success Messages - Responsive */
    .stSuccess {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: clamp(0.7rem, 2vw, 1rem);
        border-radius: 4px;
        font-size: clamp(0.85rem, 2vw, 1rem);
    }
    
    /* Code Blocks - Responsive */
    .stCodeBlock {
        background-color: #f5f5f5;
        border-radius: 6px;
        padding: clamp(0.7rem, 2vw, 1rem);
        font-size: clamp(0.75rem, 1.8vw, 0.9rem);
    }
    
    /* Footer - Responsive */
    footer {
        text-align: center;
        color: #666;
        padding: clamp(0.5rem, 2vw, 1rem) 0;
        font-size: clamp(0.8rem, 2vw, 1rem);
    }
    
    /* Responsive Columns - Stack on Mobile */
    @media screen and (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .main-header {
            font-size: 1.8rem;
            padding: 1rem 0;
        }
        
        /* Make graph responsive */
        .element-container img {
            max-width: 100%;
            height: auto;
        }
    }
    
    /* Tablet Adjustments */
    @media screen and (min-width: 769px) and (max-width: 1024px) {
        .main-header {
            font-size: 2.2rem;
        }
    }
    
    /* Large Screen Optimizations */
    @media screen and (min-width: 1920px) {
        .main .block-container {
            max-width: 1600px;
            margin: 0 auto;
        }
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
        # Responsive figure size - adapts to screen
        import matplotlib.pyplot as plt
        # Use larger figure for better visibility on all screens
        fig, ax = plt.subplots(figsize=(14, 9), dpi=100)
        fig.patch.set_facecolor('white')
        
        # Draw solution path edges first with enhanced styling
        if highlight_path_edges:
            path_edge_list = list(zip(highlight_path_edges[:-1], highlight_path_edges[1:]))
            nx.draw_networkx_edges(self.graph, self.pos, ax=ax,
                                  edgelist=path_edge_list,
                                  edge_color='#E53935', width=6, alpha=0.95, style='solid',
                                  arrows=True, arrowsize=25, arrowstyle='->', connectionstyle='arc3,rad=0.1')
        
        # Draw all edges with professional styling
        nx.draw_networkx_edges(self.graph, self.pos, ax=ax, 
                              edge_color='#757575', width=3, alpha=0.6, style='solid',
                              connectionstyle='arc3,rad=0.1')
        
        # Draw nodes with professional color scheme
        # Priority: current > path > start/goal > intersection > forward/backward > visited > unvisited
        node_colors = []
        node_sizes = []
        node_edgewidths = []
        
        for node in self.graph.nodes():
            if highlight_current and node == highlight_current:
                # Current node being explored - make it stand out
                node_colors.append('#FFC107')  # Bright amber
                node_sizes.append(3200)  # Larger size
                node_edgewidths.append(4)  # Thicker border
            elif highlight_path and node in highlight_path:
                # Solution path nodes
                node_colors.append('#F44336')  # Red
                node_sizes.append(2800)
                node_edgewidths.append(3)
            elif node == self.start_node or node == self.goal_node:
                # Start and goal nodes
                node_colors.append('#FF6B35')  # Vibrant orange
                node_sizes.append(2800)
                node_edgewidths.append(3)
            elif (forward_visited and node in forward_visited and 
                  backward_visited and node in backward_visited):
                # Intersection in bidirectional search
                node_colors.append('#9C27B0')  # Purple
                node_sizes.append(2800)
                node_edgewidths.append(3)
            elif forward_visited and node in forward_visited:
                # Forward search nodes
                node_colors.append('#2196F3')  # Blue
                node_sizes.append(2800)
                node_edgewidths.append(2.5)
            elif backward_visited and node in backward_visited:
                # Backward search nodes
                node_colors.append('#4CAF50')  # Green
                node_sizes.append(2800)
                node_edgewidths.append(2.5)
            elif highlight_visited and node in highlight_visited:
                # Visited nodes
                node_colors.append('#66BB6A')  # Light green
                node_sizes.append(2800)
                node_edgewidths.append(2.5)
            else:
                # Unvisited nodes
                node_colors.append('#90CAF9')  # Light blue
                node_sizes.append(2800)
                node_edgewidths.append(2.5)
        
        # Draw nodes with varying sizes and edge widths
        for i, node in enumerate(self.graph.nodes()):
            nx.draw_networkx_nodes(self.graph, self.pos, ax=ax, nodelist=[node],
                                  node_color=[node_colors[i]], node_size=node_sizes[i],
                                  alpha=0.95, edgecolors='#212121', linewidths=node_edgewidths[i])
        
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
                               font_size=15, font_weight='bold', 
                               font_color='#FFFFFF', font_family='Arial')
        
        # Draw visit numbers above visited nodes with improved professional design
        if visited_order_map:
            for node in visited_order_map.keys():
                x, y = self.pos[node]
                visit_num = visited_order_map[node]
                
                # Calculate optimal position above node (avoid overlap with labels)
                # Position at 0.75 units above node center for better spacing
                badge_y = y + 0.75
                
                # Create a professional badge design
                # Outer circle - white border
                outer_circle = Circle((x, badge_y), 0.22, color='#FFFFFF', fill=True, 
                                     zorder=5, linewidth=0, alpha=0.95)
                ax.add_patch(outer_circle)
                
                # Inner circle - colored badge
                inner_circle = Circle((x, badge_y), 0.19, color='#E53935', fill=True, 
                                     zorder=6, linewidth=0)
                ax.add_patch(inner_circle)
                
                # Add subtle shadow effect
                shadow_circle = Circle((x + 0.02, badge_y - 0.02), 0.19, 
                                     color='#B71C1C', fill=True, 
                                     zorder=4, alpha=0.3)
                ax.add_patch(shadow_circle)
                
                # Draw number text with better styling
                ax.text(x, badge_y, str(visit_num), fontsize=12, fontweight='bold',
                       color='#FFFFFF', ha='center', va='center', zorder=7,
                       family='Arial', style='normal')
                
                # Add a subtle connecting line to node for better visual connection
                ax.plot([x, x], [y + 0.45, badge_y - 0.19], 
                       color='#BDBDBD', linewidth=1.5, alpha=0.4, 
                       linestyle='--', zorder=3, dashes=(3, 2))
        
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
                     fontsize=11, framealpha=0.98, fancybox=True,
                     shadow=True, edgecolor='#BDBDBD', facecolor='#FAFAFA',
                     frameon=True, borderpad=0.8, labelspacing=0.8)
        
        ax.set_title('Graph Search Visualization', fontsize=18, fontweight='600', 
                    pad=20, color='#424242', fontfamily='Arial')
        ax.axis('off')
        ax.set_facecolor('#FFFFFF')
        
        plt.tight_layout()
        return fig

# Initialize visualizer
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = GraphSearchVisualizer()
    st.session_state.visited_order = []
    st.session_state.solution_path = []
    st.session_state.animation_running = False
    st.session_state.animation_step = 0
    st.session_state.animation_complete = False
    st.session_state.forward_visited = set()
    st.session_state.backward_visited = set()

visualizer = st.session_state.visualizer

# Header
st.markdown('<div class="main-header">🔍 Graph Search Visualizer</div>', unsafe_allow_html=True)

# Sidebar for controls with improved design
with st.sidebar:
    st.header("🎮 Controls")
    
    # Algorithm selection buttons - single column to prevent wrapping
    st.subheader("Algorithms", divider="gray")
    
    if st.button("🔍 DFS", use_container_width=True, type="primary"):
        # Reset state when switching algorithms
        st.session_state.visited_order = []
        st.session_state.solution_path = []
        st.session_state.forward_visited = set()
        st.session_state.backward_visited = set()
        st.session_state.algorithm = "DFS"
        st.session_state.animation_running = True
        st.session_state.animation_step = 0
        st.session_state.animation_complete = False
        st.session_state.current_animation_node = None
        if 'full_visited_order' in st.session_state:
            del st.session_state['full_visited_order']
        if 'full_solution_path' in st.session_state:
            del st.session_state['full_solution_path']
        st.session_state.auto_play = False
        st.session_state.auto_play_initialized = False
        st.rerun()
    
    if st.button("🔍 BFS", use_container_width=True):
        # Reset state when switching algorithms
        st.session_state.visited_order = []
        st.session_state.solution_path = []
        st.session_state.forward_visited = set()
        st.session_state.backward_visited = set()
        st.session_state.algorithm = "BFS"
        st.session_state.animation_running = True
        st.session_state.animation_step = 0
        st.session_state.animation_complete = False
        st.session_state.current_animation_node = None
        if 'full_visited_order' in st.session_state:
            del st.session_state['full_visited_order']
        if 'full_solution_path' in st.session_state:
            del st.session_state['full_solution_path']
        st.session_state.auto_play = False
        st.session_state.auto_play_initialized = False
        st.rerun()
    
    if st.button("🔄 Bidirectional", use_container_width=True):
        # Reset state when switching algorithms
        st.session_state.visited_order = []
        st.session_state.solution_path = []
        st.session_state.forward_visited = set()
        st.session_state.backward_visited = set()
        st.session_state.algorithm = "Bidirectional"
        st.session_state.animation_running = True
        st.session_state.animation_step = 0
        st.session_state.animation_complete = False
        st.session_state.current_animation_node = None
        if 'full_visited_order' in st.session_state:
            del st.session_state['full_visited_order']
        if 'full_solution_path' in st.session_state:
            del st.session_state['full_solution_path']
        st.session_state.auto_play = False
        st.session_state.auto_play_initialized = False
        st.rerun()
    
    # Animation controls section
    if st.session_state.get('animation_running'):
        st.markdown("---")
        st.subheader("Animation", divider="gray")
        
        # Use two columns for better layout
        col_play, col_step = st.columns(2)
        with col_play:
            if st.button("▶️ Play", use_container_width=True):
                st.session_state.auto_play = True
                st.rerun()
        with col_step:
            if st.button("⏭️ Step", use_container_width=True):
                st.session_state.auto_play = False
                st.session_state.animation_step = st.session_state.get('animation_step', 0) + 1
                st.rerun()
        
        if st.button("⏸️ Pause", use_container_width=True):
            st.session_state.auto_play = False
            st.rerun()
    
    # Reset button
    st.markdown("---")
    if st.button("🔄 Reset", use_container_width=True, type="secondary"):
        st.session_state.visited_order = []
        st.session_state.solution_path = []
        st.session_state.forward_visited = set()
        st.session_state.backward_visited = set()
        st.session_state.animation_running = False
        st.session_state.animation_step = 0
        st.session_state.animation_complete = False
        st.session_state.current_animation_node = None
        if 'full_visited_order' in st.session_state:
            del st.session_state['full_visited_order']
        if 'full_solution_path' in st.session_state:
            del st.session_state['full_solution_path']
        st.session_state.auto_play = False
        st.session_state.auto_play_initialized = False
        st.rerun()
    
    # Info section
    st.markdown("---")
    st.info("👆 Select an algorithm to visualize graph traversal")

# Main content area - Responsive layout
# On mobile, stack vertically; on larger screens, use side-by-side
col1, col2 = st.columns([2, 1], gap="medium")

with col1:
    # Run algorithm if selected and not yet computed
    if st.session_state.get('algorithm') and st.session_state.animation_running:
        if 'full_visited_order' not in st.session_state:
            algorithm = st.session_state.algorithm
            
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
                st.session_state.full_visited_order = visited_order
                st.session_state.full_solution_path = solution_path
                st.session_state.forward_visited = set()
                st.session_state.backward_visited = set()
            
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
                st.session_state.full_visited_order = visited_order
                st.session_state.full_solution_path = solution_path
                st.session_state.forward_visited = set()
                st.session_state.backward_visited = set()
            
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
                    st.session_state.full_visited_order = visited_order
                    st.session_state.full_solution_path = solution_path
                    st.session_state.forward_visited = forward_visited
                    st.session_state.backward_visited = backward_visited
                else:
                    st.session_state.full_visited_order = []
                    st.session_state.full_solution_path = []
        
        # Animate step by step
        full_visited_order = st.session_state.get('full_visited_order', [])
        animation_step = st.session_state.get('animation_step', 0)
        
        if full_visited_order:
            # Show progress up to current step
            if animation_step < len(full_visited_order):
                current_visited = full_visited_order[:animation_step + 1]
                current_node = full_visited_order[animation_step]
            else:
                current_visited = full_visited_order
                current_node = None
            
            st.session_state.visited_order = current_visited
            st.session_state.current_animation_node = current_node
            
            # Check if animation is complete
            if animation_step >= len(full_visited_order) - 1:
                st.session_state.animation_complete = True
                st.session_state.solution_path = st.session_state.get('full_solution_path', [])
                st.session_state.current_animation_node = None
            else:
                # Auto-play mode - start automatically
                if not st.session_state.get('auto_play_initialized', False):
                    st.session_state.auto_play = True
                    st.session_state.auto_play_initialized = True
                
    
    # Create graph placeholder for animation
    graph_placeholder = st.empty()
    
    # Draw graph with current animation state
    visited_order = st.session_state.get('visited_order', [])
    solution_path = st.session_state.get('solution_path', [])
    forward_visited = st.session_state.get('forward_visited', set())
    backward_visited = st.session_state.get('backward_visited', set())
    
    # For bidirectional, show current state
    if forward_visited or backward_visited:
        visited_set = None
    else:
        # Show visited nodes (excluding current node for clarity)
        visited_set = set(visited_order) if visited_order else set()
    
    # Get current node for highlighting - use stored value
    current_node = st.session_state.get('current_animation_node', None)
    
    # If we have a current node in animation, remove it from visited set to show it separately
    if current_node is not None and visited_set:
        visited_set = visited_set - {current_node}
    
    # Show status message during animation
    status_placeholder = st.empty()
    if st.session_state.get('animation_running') and not st.session_state.get('animation_complete', False):
        animation_step = st.session_state.get('animation_step', 0)
        full_visited_order = st.session_state.get('full_visited_order', [])
        if current_node is not None and animation_step < len(full_visited_order):
            node_letter = visualizer.node_to_letter.get(current_node, str(current_node))
            status_placeholder.info(f"🔍 **Exploring Node {node_letter}** (Node {current_node}) - Step {animation_step + 1}/{len(full_visited_order)}")
        else:
            status_placeholder.empty()
    else:
        status_placeholder.empty()
    
    # Draw and display graph
    fig = visualizer.draw_graph(
        highlight_visited=visited_set,
        highlight_path=solution_path if st.session_state.get('animation_complete', False) else [],
        highlight_current=current_node,
        highlight_path_edges=solution_path if (solution_path and st.session_state.get('animation_complete', False)) else None,
        visited_order_list=visited_order,
        forward_visited=forward_visited if forward_visited else None,
        backward_visited=backward_visited if backward_visited else None
    )
    
    # Display graph in placeholder for smooth animation updates
    with graph_placeholder.container():
        st.pyplot(fig, use_container_width=True, clear_figure=True)
    
    # Handle auto-play animation after graph is shown
    if st.session_state.get('animation_running') and not st.session_state.get('animation_complete', False):
        full_visited_order = st.session_state.get('full_visited_order', [])
        animation_step = st.session_state.get('animation_step', 0)
        
        if st.session_state.get('auto_play', False) and animation_step < len(full_visited_order) - 1:
            # Advance to next step after showing current frame
            time.sleep(1.2)  # Visible delay
            st.session_state.animation_step += 1
            st.rerun()
    
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
st.markdown(
    "<div style='text-align: center; color: #757575; padding: 1rem 0;'>"
    "<strong>Graph Search Visualizer</strong> | "
    "Interactive Visualization of Graph Search Algorithms | "
    "Built with Streamlit"
    "</div>", 
    unsafe_allow_html=True
)

