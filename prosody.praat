# Open the audio file
Read from file: "data/Audio/P1.wav"

# Get duration
duration = GetSoundObjectInfo(selection, "dur")

# Extract energy, power
sound = ToSound(selection)
energy = GetEnergy(sound)
power = GetPower(sound)

# Extract pitch features
pitch = ToPitch(selection)
pitchMin = GetMinimum(pitch)
pitchMax = GetMaximum(pitch)
pitchMean = GetMean(pitch)
pitchSD = GetStandardDeviation(pitch)
pitchAbs = ToAbsolute(pitch)
pitchQuant = ToQuantile(pitch)
pitchUvsVRatio = GetUvsVRatio(pitch)
Time8 = GetPitchTierInfo(pitch, "Times")

# Extract intensity features
intensity = ToIntensity(selection)
intensityMin = GetMinimum(intensity)
intensityMax = GetMaximum(intensity)
intensityMean = GetMean(intensity)
intensitySD = GetStandardDeviation(intensity)
intensityQuant = ToQuantile(intensity)

# Calculate intensity difference measures
diffIntMaxMin = intensityMax - intensityMin
diffIntMaxMean = intensityMax - intensityMean
diffIntMaxMode = GetQuantileDifference(intensity, pitchMax)

# Extract other features
iDifference = GetDifference(intensity)
diffPitchMaxMin = pitchMax - pitchMin
diffPitchMaxMean = pitchMax - pitchMean
diffPitchMaxMode = GetQuantileDifference(pitch, pitchMax)
avgVal1, avgVal2, avgVal3 = GetAverageValues(intensity, 3)
avgBand1, avgBand2, avgBand3 = GetAverageValuesByBand(intensity, 3)
fmean1, fmean2, fmean3 = GetMeanFormants(selection, 3)
f2meanf1, f3meanf1 = GetDifferenceFormants(selection, 2, 1)
f1STD, f2STD, f3STD = GetStandardDeviationFormants(selection, 3)
f2STDf1, f2STDf2 = GetDifferenceStandardDeviationFormants(selection, 2)
jitter = GetJitter(pitch)
shimmer = GetShimmer(pitch)
jitterRap = GetJitter(pitch, "rap")
meanPeriod = GetMeanPeriod(pitch)
percentUnvoiced = GetPercentUnvoiced(pitch)
numVoiceBreaks = GetNumberOfVoiceBreaks(pitch)
PercentBreaks = GetPercentVoiceBreaks(pitch)
speakRate = GetSpeakingRate(pitch)
numPause = GetNumberOfPauses(intensity)
maxDurPause = GetMaximumPauseDuration(intensity)
avgDurPause = GetMeanPauseDuration(intensity)
TotDurPause3 = GetTotalPauseDuration(intensity, 3)
iInterval = GetInterval(intensity)
MaxRising3, MaxFalling3, AvgTotRis3, AvgTotFall3 = GetTones(intensity, 3)
numRising, numFall = GetNumberOfTones(intensity)
loudness = GetLoudness(intensity)

# Print results
print("Duration (s):", duration)
print("Energy:", energy)
print("Power (dB):", power)
print("Min pitch (Hz):", pitchMin)
print("Max pitch (Hz):", pitchMax)
print("Mean pitch (Hz):", pitchMean)
print("Pitch SD (Hz):", pitchSD)
print("Pitch absolute", pitchAbs)
print("Pitch quantile:", pitchQuant)
print("Pitch U/V ratio:", pitchUvsVRatio)
print("Time 8:", Time8)
#... Print remaining features