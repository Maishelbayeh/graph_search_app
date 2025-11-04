# Graph Search Visualizer

An interactive web application for visualizing graph search algorithms, designed for educational purposes in Artificial Intelligence.

## Features

- **Modern Web Interface** using Streamlit
- **Three Search Algorithms**:
  - 🔍 **DFS** (Depth-First Search)
  - 🔍 **BFS** (Breadth-First Search)
  - 🔄 **Bidirectional Search**
- **Visual Representation** showing:
  - Exploration path (visited nodes)
  - Solution path (from start to goal)
- **Color Coding**:
  - 🟠 Orange: Start and Goal nodes
  - 🔵 Light Blue: Unvisited nodes
  - 🟢 Green: Visited nodes
  - 🟡 Amber: Current node being explored
  - 🔴 Red: Solution path nodes
  - 🟣 Purple: Intersection point (Bidirectional Search)

## Local Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at: `http://localhost:8501`

## Deployment on Streamlit Cloud (Free)

### Steps:

1. **Create a GitHub Account**
   - Go to [GitHub.com](https://github.com)
   - Create a new account (free)

2. **Create a New Repository**
   - Click "New repository"
   - Name it: `graph-search-visualizer`
   - Select "Public" (for free tier)
   - Click "Create repository"

3. **Upload Files to GitHub**
   ```bash
   cd C:\Users\maysh\Desktop\graph_search_app
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/graph-search-visualizer.git
   git push -u origin main
   ```
   
   Or use GitHub Desktop (easier)

4. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select repository: `graph-search-visualizer`
   - Main file path: `app.py`
   - Click "Deploy"

5. **Access Your Application**
   - You'll get a URL like: `https://your-app-name.streamlit.app`
   - Share this link with others!

## Project Files

- `app.py` - Main application (Streamlit)
- `graph_search_visualizer.py` - Standalone version (desktop)
- `requirements.txt` - Required dependencies
- `README.md` - This file

## Usage

1. Select a search algorithm from the sidebar buttons
2. Watch the graph update as the algorithm progresses
3. Review the tested path list on the right
4. Click "Reset" to start over

## Technical Details

### Algorithms Implemented

- **Depth-First Search (DFS)**: Explores as far as possible along each branch before backtracking
- **Breadth-First Search (BFS)**: Explores all neighbors at the present depth before moving to the next level
- **Bidirectional Search**: Simultaneously searches from start and goal nodes until they meet

### Requirements

- Python 3.8 or higher
- Streamlit
- NetworkX
- Matplotlib

## Support

If you encounter any issues, ensure:
- All dependencies from `requirements.txt` are installed
- Python 3.8 or newer is being used
- Internet connection is available when deploying

---

**Developed for educational purposes in Artificial Intelligence**
