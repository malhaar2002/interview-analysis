import parselmouth
import pickle
from parselmouth.praat import call
import statistics
from scipy.stats.mstats import zscore
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd

def measurePitch(voiceID, f0min, f0max, unit):
    sound = parselmouth.Sound(voiceID) # read the sound
    duration = call(sound, "Get total duration") # duration
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max) #create a praat pitch object
    meanF0 = call(pitch, "Get mean", 0, 0, unit) # get mean pitch
    stdevF0 = call(pitch, "Get standard deviation", 0 ,0, unit) # get standard deviation
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, f0min, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    rapJitter = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    ddpJitter = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer =  call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    localdbShimmer = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq3Shimmer = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    aqpq5Shimmer = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq11Shimmer =  call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    ddaShimmer = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    
    return duration, meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer

# %%
# This function measures formants using Formant Position formula
def measureFormants(sound, wave_file, f0min,f0max):
    sound = parselmouth.Sound(sound) # read the sound
    pitch = call(sound, "To Pitch (cc)", 0, f0min, 15, 'no', 0.03, 0.45, 0.01, 0.35, 0.14, f0max)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    
    formants = call(sound, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
    numPoints = call(pointProcess, "Get number of points")

    f1_list = []
    f2_list = []
    f3_list = []
    f4_list = []
    
    # Measure formants only at glottal pulses
    for point in range(0, numPoints):
        point += 1
        t = call(pointProcess, "Get time from index", point)
        f1 = call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
        f2 = call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')
        f3 = call(formants, "Get value at time", 3, t, 'Hertz', 'Linear')
        f4 = call(formants, "Get value at time", 4, t, 'Hertz', 'Linear')
        f1_list.append(f1)
        f2_list.append(f2)
        f3_list.append(f3)
        f4_list.append(f4)
    
    f1_list = [f1 for f1 in f1_list if str(f1) != 'nan']
    f2_list = [f2 for f2 in f2_list if str(f2) != 'nan']
    f3_list = [f3 for f3 in f3_list if str(f3) != 'nan']
    f4_list = [f4 for f4 in f4_list if str(f4) != 'nan']
    
    # calculate mean formants across pulses
    f1_mean = statistics.mean(f1_list)
    f2_mean = statistics.mean(f2_list)
    f3_mean = statistics.mean(f3_list)
    f4_mean = statistics.mean(f4_list)
    
    # calculate median formants across pulses, this is what is used in all subsequent calcualtions
    # you can use mean if you want, just edit the code in the boxes below to replace median with mean
    f1_median = statistics.median(f1_list)
    f2_median = statistics.median(f2_list)
    f3_median = statistics.median(f3_list)
    f4_median = statistics.median(f4_list)
    
    return f1_mean, f2_mean, f3_mean, f4_mean, f1_median, f2_median, f3_median, f4_median

def runPCA(df):
    # z-score the Jitter and Shimmer measurements
    measures = ['localJitter', 'localabsoluteJitter', 'rapJitter', 'ppq5Jitter', 'ddpJitter',
                'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer', 'apq11Shimmer', 'ddaShimmer']
    x = df.loc[:, measures].values
    print(x)
    x = StandardScaler().fit_transform(x)
    # PCA
    pca = pickle.load(open('../models/pca_model.pkl', 'rb'))
    principalComponents = pca.transform(x)
    principalDf = pd.DataFrame(data = principalComponents, columns = ['JitterPCA', 'ShimmerPCA'])
    return principalDf


def calculate_z_score(x, mean, std):
    return (x-mean)/std


def extract_praat_features(video_path):
    sound = parselmouth.Sound(video_path)
    
    # Measure pitch features
    (duration, meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter,
     localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer) = measurePitch(
        sound, 75, 300, "Hertz")

    # Measure formant features
    (f1_mean, f2_mean, f3_mean, f4_mean, f1_median, f2_median, f3_median, f4_median) = measureFormants(
        sound, video_path, 75, 300)

    # Run PCA on Jitter and Shimmer
    pca_data = runPCA(pd.DataFrame({
        'localJitter': [localJitter],
        'localabsoluteJitter': [localabsoluteJitter],
        'rapJitter': [rapJitter],
        'ppq5Jitter': [ppq5Jitter],
        'ddpJitter': [ddpJitter],
        'localShimmer': [localShimmer],
        'localdbShimmer': [localdbShimmer],
        'apq3Shimmer': [apq3Shimmer],
        'apq5Shimmer': [aqpq5Shimmer],
        'apq11Shimmer': [apq11Shimmer],
        'ddaShimmer': [ddaShimmer],
    }))

    # Calculate vocal-tract length estimates
    pF = (calculate_z_score(f1_median, 496.0428522921353, 41.80788949595729) + calculate_z_score(f2_median, 1626.9758909632872, 89.54888245840672) + calculate_z_score(f3_median, 2603.7923145976265, 107.64036595614571) + calculate_z_score(f4_median, 3660.265503495315, 145.75539455320262)) / 4
    fdisp = (f4_median - f1_median) / 3
    avgFormant = (f1_median + f2_median + f3_median + f4_median) / 4
    mff = (f1_median * f2_median * f3_median * f4_median) ** 0.25
    fitch_vtl = ((1 * (35000 / (4 * f1_median))) +
                  (3 * (35000 / (4 * f2_median))) +
                  (5 * (35000 / (4 * f3_median))) +
                  (7 * (35000 / (4 * f4_median)))) / 4

    xysum = (0.5 * f1_median) + (1.5 * f2_median) + (2.5 * f3_median) + (3.5 * f4_median)
    xsquaredsum = (0.5 ** 2) + (1.5 ** 2) + (2.5 ** 2) + (3.5 ** 2)
    delta_f = xysum / xsquaredsum
    vtl_delta_f = 35000 / (2 * delta_f)

    # Create a dictionary to store the features
    features = {
        'duration': duration,
        'meanF0Hz': meanF0,
        'stdevF0Hz': stdevF0,
        'HNR': hnr,
        'localJitter': localJitter,
        'localabsoluteJitter': localabsoluteJitter,
        'rapJitter': rapJitter,
        'ppq5Jitter': ppq5Jitter,
        'ddpJitter': ddpJitter,
        'localShimmer': localShimmer,
        'localdbShimmer': localdbShimmer,
        'apq3Shimmer': apq3Shimmer,
        'apq5Shimmer': aqpq5Shimmer,
        'apq11Shimmer': apq11Shimmer,
        'ddaShimmer': ddaShimmer,
        'f1_mean': f1_mean,
        'f2_mean': f2_mean,
        'f3_mean': f3_mean,
        'f4_mean': f4_mean,
        'f1_median': f1_median,
        'f2_median': f2_median,
        'f3_median': f3_median,
        'f4_median': f4_median,
        'JitterPCA': pca_data['JitterPCA'].values[0],
        'ShimmerPCA': pca_data['ShimmerPCA'].values[0],
        'pF': pF,
        'fdisp': fdisp,
        'avgFormant': avgFormant,
        'mff': mff,
        'fitch_vtl': fitch_vtl,
        'delta_f': delta_f,
        'vtl_delta_f': vtl_delta_f
    }

    return features 