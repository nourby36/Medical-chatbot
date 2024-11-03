from imblearn.over_sampling import SMOTE
import pandas as pd
import numpy as np
import tensorflow as tf
import torch
from data_balanced import data_list
from textattack.transformations import WordSwap
from textattack.augmentation import CheckListAugmenter
from textattack.augmentation import EasyDataAugmenter

# Function to augment data using CheckListAugmenter

def augmenter_donnees(phrases, num_replacements=2, transformations_per_example=1):  # Adjust num_replacements as needed
    augmenter = EasyDataAugmenter(pct_words_to_swap=0.2, transformations_per_example=transformations_per_example)
    phrases_augmentees = []
    for phrase in phrases:
        phrases_augmentees.append(augmenter.augment(phrase))
        print('la phrase originale est:')
        print(phrase)
    print(len(phrases_augmentees))
    return phrases_augmentees

df = pd.DataFrame(data_list, columns=["sentence_en", "sentence_zh", "label"])

# Calculer le nombre d'échantillons de chaque classe
class_counts = df['label'].value_counts()
print(class_counts)




majority_class = 'prevention'
majority_count = class_counts[majority_class]
desired_majority_samples = 2700  

if majority_count > desired_majority_samples:
    indices_to_remove = df[df['label'] == majority_class].sample(n=majority_count - desired_majority_samples, random_state=42).index
    df = df.drop(indices_to_remove)



# 7. Save balanced data (adapt saving logic as needed)
balanced_data = [(row['sentence_en'], row['sentence_zh'], row['label']) for _, row in df.iterrows()]
class_counts = df['label'].value_counts()
print(class_counts)

with open("data_balanced.py", 'w', encoding='utf-8') as f:
  f.write("data_list = [\n")
  for item in balanced_data:
    f.write(f"    ({repr(item[0])}, {repr(item[1])}, {repr(item[2])}),\n")
  f.write("]\n")
