from scipy.signal import find_peaks
import numpy as np

def find_peak_trough(df:DataFrame)->list:
  '''
  This function flags peaks and troughs on stress-time curves and strain-time cuvres.

  Parameter:
  - df: a Pandas dataframe containing the stress and strain data. The raw data of 
  mechanical testing (force and displacement) is pre-processed into stress and strain.

  Returns:
  - df with four additional columns flagging the positions of peaks and troughs. 
  In each column, 0 is the default value and 1 marks the flagged position. 
  The value 1 is later used to filtre dataframe for plotting the flagged peak/troughs 
  for visual inspection 
  'strain_peak': marks the peak position in the strain cycle
  'strain_trough': marks the trough position in the strain cycle
  'stress_peak': marks the peak position in the stress cycle
  'stress_trough': marks the trough position in the stress cycle
  - a list of peak and trough positions
  '''
  # below codes show an example flagging the strain peak
  strain_peak_index,_ = find_peaks(df['Strain'], distance=<>, height=<>)
  df['Strain_Peak'] = 0
  df.loc[strain_peak_index,'Strain_Peak'] = 1
  # below codes show an example flagging the strain trough
  strain_trough_index,_ = find_peaks(-1*df['Strain'], distance=<>, height=<>)
  df['Strain_Trough'] = 0
  df.loc[strain_trough_index,'Strain_Trough'] = 1
  return df, [strain_trough_index, ...]

def update_cycle_(df:DataFrame, pos_list:list, cycle_name:str):
  '''
  This function create a new column in the Pandas dataframe to describe the cycle
  number for cyclic tensile tests.

  Parameters:
  - df: the Pandas Dataframe containing cyclic mechanical testing data
  - pos_list: the index of peaks/troughs, determined by find_peak_trough function
  - cycle_name: 'Strain_Cycle' or 'Stress_Cycle'
  '''
  df[cycle_name] = 0
  for i in range(1, len(pos_list)+1):
      # fix the problem of incomplete last cycle
      if i == len(pos_list):
          if cycle_name == 'Strain_Cycle':
              mask = (df['Time (ms)'] > pos_list[i-1])
                     & (df['Time (s)'] <= (pos_list[i-1] + mean_tpc_strain))
          else:
              mask = (df['Time (ms)'] > pos_list[i-1])
                     & (df['Time (s)'] <= (pos_list[i-1] + mean_tpc_stress))
          df.loc[mask, cycle_name] = i + 1
      else:
          mask = (df['Time (ms)'] > pos_list[i-1]) & (df['Time (ms)'] <= pos_list[i])
          df.loc[mask, cycle_name] = i

def plot_calibrate_cycle_first_half(cycle_no:int, cycle_name:str):
  '''
  This function calibrates the start of stress-strain curve in each cycle 
  to the origin (0, 0) for cyclic tensile tests.

  Parameters:
  - cycle_no: the number of cycle under study
  - cycle_name: the type of the cycle (strain or stress)
  '''
  df_cycle = df[df[cycle_name]==cycle_no]
  t_0 = df_cycle['Time (s)'].min()
  # 
  t_end = <customised_input> + t_0
  x = df_cycle.loc[df['Time (s)']<t_end, 'Strain']
  y = df_cycle.loc[df['Time (s)']<t_end, 'Stress (kPa)']
  x_calib = x - x.min()
  y_calib = y - y.min()
  plt.scatter(x_calib, y_calib, s=10, label=f'Cycle {cycle_no}')
