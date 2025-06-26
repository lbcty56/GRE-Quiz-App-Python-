# app/widgets/results_chart.py
from PyQt6.QtWidgets import QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ResultsChart(FigureCanvas):
    """A custom widget to display a Matplotlib bar chart with improved labels."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('#353535')
        self.axes = fig.add_subplot(111)
        self.axes.tick_params(axis='x', colors='white')
        self.axes.tick_params(axis='y', colors='white')
        self.axes.spines['bottom'].set_color('white')
        self.axes.spines['left'].set_color('white')
        self.axes.spines['top'].set_color('#353535')
        self.axes.spines['right'].set_color('#353535')
        super(ResultsChart, self).__init__(fig)

    def plot(self, results_by_topic):
        """Plots the bar chart based on quiz results."""
        topics = list(results_by_topic.keys())
        percentages = [(data['correct'] / data['total']) * 100 if data['total'] > 0 else 0 for data in results_by_topic.values()]
        
        self.axes.clear()
        bars = self.axes.bar(topics, percentages, color='#2a82da')
        self.axes.set_ylabel('Percentage Correct (%)', color='white', fontsize=10)
        self.axes.set_title('Performance by Topic', color='white', fontsize=14, weight='bold')
        self.axes.set_ylim(0, 105)

        for bar in bars:
            height = bar.get_height()
            vertical_alignment = 'bottom'
            label_position = height + 1
            
            if height < 5:
                label_position = 2
            elif height > 95:
                label_position = 98
                vertical_alignment = 'top'

            self.axes.text(
                bar.get_x() + bar.get_width() / 2.0,
                label_position,
                f'{height:.0f}%',
                ha='center',
                va=vertical_alignment,
                color='white',
                weight='bold'
            )
        self.draw()