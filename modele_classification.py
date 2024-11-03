import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
from data_balanced import data_list

# Prétraitement des données (exemple)
# Assurez-vous d'adapter cette partie à vos données spécifiques

df = pd.DataFrame(data_list, columns=["sentence_en", "sentence_zh", "label"])

texts = df["sentence_zh"].tolist()  # Vos textes
labels = df["label"].tolist()  # Vos étiquettes

tokenizer = BertTokenizer.from_pretrained('hfl/chinese-bert-wwm')
max_len = 128  # Longueur maximale des séquences
inputs = tokenizer(texts, padding=True, truncation=True, max_length=max_len, return_tensors="pt")

# Convertir les étiquettes en nombres entiers
label_to_id = {label: idx for idx, label in enumerate(set(labels))}


output_file = "labels_to_ids.txt"

# Ouvrir le fichier en mode écriture
with open(output_file, "w") as file:
    # Écrire chaque paire clé-valeur dans le fichier
    for label, idx in label_to_id.items():
        file.write(f"{label}: {idx}\n")

labels = [label_to_id[label] for label in labels]

# Séparation des données en ensembles d'entraînement et de validation
train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Prétraitement des données pour les ensembles d'entraînement et de validation
train_inputs = tokenizer(train_texts, padding=True, truncation=True, max_length=max_len, return_tensors="pt")
val_inputs = tokenizer(val_texts, padding=True, truncation=True, max_length=max_len, return_tensors="pt")

# Convertir les étiquettes en tenseurs PyTorch
train_labels = torch.tensor(train_labels)
val_labels = torch.tensor(val_labels)

# Chargement du modèle pré-entraîné
model = BertForSequenceClassification.from_pretrained('hfl/chinese-bert-wwm', num_labels=len(label_to_id))

# Entraînement du modèle
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
train_dataset = TensorDataset(train_inputs['input_ids'], train_inputs['attention_mask'], train_labels)
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)

optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
criterion = torch.nn.CrossEntropyLoss()

epochs = 1
for epoch in range(epochs):
    model.train()
    for batch in train_loader:
        batch = [item.to(device) for item in batch]
        inputs, masks, targets = batch
        optimizer.zero_grad()
        outputs = model(inputs, attention_mask=masks, labels=targets)
        loss = outputs.loss
        loss.backward()
        optimizer.step()

# Évaluation du modèle
val_dataset = TensorDataset(val_inputs['input_ids'], val_inputs['attention_mask'], val_labels)
val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False)

model.eval()
predicted_labels = []
true_labels = []

with torch.no_grad():
    for batch in val_loader:
        batch = [item.to(device) for item in batch]
        inputs, masks, targets = batch
        outputs = model(inputs, attention_mask=masks)
        _, predicted = torch.max(outputs.logits, dim=1)
        predicted_labels.extend(predicted.cpu().numpy())
        true_labels.extend(targets.cpu().numpy())


# Définir le chemin où enregistrer le modèle
output_model_dir = "C:\\Users\\MSI\\Desktop\\IDS4\\sem2\\NLP\\PROJET\\modeles\\modele_classification1"


# Enregistrer le modèle
model.save_pretrained(output_model_dir)

# Calcul des métriques
accuracy = accuracy_score(true_labels, predicted_labels)
precision = precision_score(true_labels, predicted_labels, average='weighted')
recall = recall_score(true_labels, predicted_labels, average='weighted')
f1 = f1_score(true_labels, predicted_labels, average='weighted')

print("Accuracy: {:.2f}%".format(accuracy * 100))
print("Precision: {:.2f}%".format(precision * 100))
print("Recall: {:.2f}%".format(recall * 100))
print("F1 Score: {:.2f}%".format(f1 * 100))
