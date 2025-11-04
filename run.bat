@echo off
echo Installing required packages...
pip install -r requirements.txt
echo.
echo Starting Graph Search Visualizer...
python graph_search_visualizer.py
pause

