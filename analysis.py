import mne
import numpy as np
from scipy import stats

ss_list, sd_list, ds_list = [], [], []

# Loop for preprocessing ERPCORE MMN data
for subject_id in range(1, 41):

    filepath = '../ERPCORE_MMN_SET_FILES/%i_MMN.set' % subject_id

    raw = mne.io.read_raw_eeglab(filepath, preload=True)

    raw = raw.filter(0.1, 20)

    raw.resample(256)

    mne.set_eeg_reference(raw, ref_channels=['P9', 'P10'])

    raw = raw.pick(['FCz'])

    events, event_id = mne.events_from_annotations(raw)

    split_events = []

    for i in range(1, events.shape[0]):

        if events[i-1, 2] == event_id['80'] and events[i, 2] == event_id['80']: # sS
            split_events.append([events[i][0], 0, 1])

        if events[i-1, 2] == event_id['80'] and events[i, 2] == event_id['70']: # sD
            split_events.append([events[i][0], 0, 2])

        if events[i-1, 2] == event_id['70'] and events[i, 2] == event_id['80']: # dS
            split_events.append([events[i][0], 0, 3])

    split_events = np.array(split_events)  

    annotations = mne.annotations_from_events(split_events, raw.info['sfreq'])

    raw.set_annotations(annotations)

    events, event_id = mne.events_from_annotations(raw)

    epochs = mne.Epochs(raw,
                        events = events,
                        tmin = -0.1,
                        tmax = 0.5,
                        baseline = (-0.1,0),
                        event_id = event_id,
                        reject = {'eeg': 150e-6})

    ss = epochs['1'].average(picks=['FCz'])
    sd = epochs['2'].average(picks=['FCz'])
    ds = epochs['3'].average(picks=['FCz'])

    ss_list.append(ss.data[0])
    sd_list.append(sd.data[0])
    ds_list.append(ds.data[0])

ss_array = np.array(ss_list)
sd_array = np.array(sd_list)
ds_array = np.array(ds_list)

times = np.linspace(-100, 500, num = ss_array.shape[1])

# Remove subject 7
ss_array = np.delete(ss_array, 6, axis=0)
sd_array = np.delete(sd_array, 6, axis=0)
ds_array = np.delete(ds_array, 6, axis=0)

# Measure mean amplitude from 125 to 225 ms
measure_window = np.logical_and(times>=125, times<=225)
ss_measure = ss_array[:, measure_window].mean(1)
sd_measure = sd_array[:, measure_window].mean(1)
ds_measure = ds_array[:, measure_window].mean(1)

# Save ERP measurements to .csv file
# (for calculating Bayes factors in R)
data = np.c_[ss_measure, sd_measure, ds_measure]
np.savetxt('erpcore_mean_amp.csv', data, delimiter=',')

# Paired t-tests
tssVsd, pssVsd = stats.ttest_rel(ss_measure, sd_measure)
tssVds, pssVds = stats.ttest_rel(ss_measure, ds_measure)
tsdVds, psdVds = stats.ttest_rel(sd_measure, ds_measure)

# Bonferroni corrections
_, corrected_ps = mne.stats.bonferroni_correction([pssVsd, pssVds, psdVds])
pssVsd_bc, pssVds_bc, psdVds_bc = corrected_ps

# Show results
print('sS vs. sD: t(38) = %.3f, p = %.3e' % (tssVsd, pssVsd_bc))
print('sS vs. dS: t(38) = %.3f, p = %.3f' % (tssVds, pssVds_bc))
print('sD vs. dS: t(38) = %.3f, p = %.3e' % (tsdVds, psdVds_bc))
