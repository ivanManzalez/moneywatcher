import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

#####################################################################################

def line_plot(x, y, x_label="", y_label="", title="", savefile=None, show = False, fig = None, x_label_spacing=None, color=None, label=None):
  
  if not fig:
    fig, ax = plt.subplots()
  else:
    ax = fig.gca()

  if color and label:
    ax.plot(x, y, label=label, color=color)
  elif label:
    ax.plot(x, y, label=label)
  elif color:
    ax.plot(x, y, color=color)
  else:
    ax.plot(x, y)

  if(x_label or  y_label):
    ax.set(
      xlabel=x_label, 
      ylabel=y_label,
      title=title
      )
  


  ax.grid()

  # Customize x-axis ticks and labels
  if(x_label_spacing):
    x_ticks = x[::x_label_spacing]  
    x_tick_labels = x[::x_label_spacing]  
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_tick_labels)

  
  if(savefile):
    fig.savefig(savefile)

  if(show):
    plt.show()

  return fig

def bar_plot(x, y, x_label="", y_label="", title="", savefile=None, show = False, fig = None, x_label_spacing=None, color=None, label=None):
  
  if not fig:
    fig, ax = plt.subplots()
  else:
    ax = fig.gca()

  if label and color:
    ax.bar(x, y, label=label, color=color)
  elif label:
    ax.bar(x, y, label=label)
  elif color:
    ax.bar(x, y, color=color)
  else:
    ax.bar(x, y)

  if(x_label or  y_label):
    ax.set(
      xlabel=x_label, 
      ylabel=y_label,
      title=title
      )

  ax.grid()

  # Customize x-axis ticks and labels
  if(x_label_spacing):
    x_ticks = x[::x_label_spacing]  
    x_tick_labels = x[::x_label_spacing]  
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_tick_labels)

  
  if(savefile):
    fig.savefig(savefile)

  if(show):
    plt.show()

  return fig

def smooth_curve(y, window):
  # Apply a smoothing filter (e.g., Savitzky-Golay filter)
  window_length = window  # Adjust the window length as needed
  polyorder = 2  # Adjust the polynomial order as needed
  smoothed_y = savgol_filter(y, window_length, polyorder)
  return smoothed_y

def poly_fit(x, y, degree):
  coefficients = np.polyfit(x, y, degree)
  equation = np.poly1d(coefficients)
  return equation




#####################################################################################
def display_total_v_time(dataframe, show=True):
  window = 6 #months
  y_running_total = dataframe["RUNNING_TOTAL"]
  y_smooth_running_total_6 = smooth_curve(y_running_total, window=window*30)
  y_smooth_running_total_3 = smooth_curve(y_running_total, window=window*15)
  y_deltas = dataframe["TOTAL_DELTA"]
  time = dataframe['TRANS DATE']

  x_label="Transaction Date"
  y_label="$ (CAD)"
  title = " CAD $ v Day-to-Day Transactions"

  fig, ax = plt.subplots()
  line_fig = line_plot(time, y_running_total, show=False, fig=fig, label="Running Total", color="b")
  line_fig = line_plot(time, y_smooth_running_total_6, show=False, fig=fig, label=f"{window} month Avg (Savitzky-Golay)", color="r")
  line_fig = line_plot(time, y_smooth_running_total_3, show=False, fig=fig, label=f"{window//2} month Avg (Savitzky-Golay)", color="g")
  # bar_fig = bar_plot(time, y_deltas, show=False, fig=fig, label="Daily Deltas", color="g")
  
  ax.set(
    xlabel=x_label, 
    ylabel=y_label,
    title=title
    )

  x_label_spacing=40
  x_ticks = time[::x_label_spacing]  
  x_tick_labels = time[::x_label_spacing]  
  ax.set_xticks(x_ticks)
  ax.set_xticklabels(x_tick_labels)

  plt.legend()

  if(show):
    plt.show()
