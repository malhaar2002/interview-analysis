import pandas as pd
import os
import sys
sys.path.append('../')
import paths

df_labels = pd.read_csv("../"+paths.labels_path)
df_labels = df_labels.rename(columns={'Participant': 'InterviewID'})
df_labels = df_labels.drop(columns=['Worker'])
df_labels = df_labels.groupby('InterviewID').mean().reset_index()
df_labels['InterviewID'] = df_labels['InterviewID'].str.upper()

medians = df_labels.median(numeric_only=True)

def prepare_data(required_label):
    # create folder if not exists
    if not os.path.exists(f"../data/classify/{required_label}"):
        os.mkdir(f"../data/classify/{required_label}")
        os.mkdir(f"../data/classify/{required_label}/positive")
        os.mkdir(f"../data/classify/{required_label}/negative")

    ids = df_labels['InterviewID']

    for i in ids:
        file = f'../data/Videos/{i}.avi'
        if df_labels[df_labels['InterviewID'] == i][required_label].values[0] >= medians[required_label]:
            os.system(f'cp {file} ../data/classify/{required_label}/positive')
        else:
            os.system(f'cp {file} ../data/classify/{required_label}/negative')

prepare_data('NotStressed')