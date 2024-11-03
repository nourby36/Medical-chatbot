# Importation des modules nécessaires
from transformers import MarianMTModel, MarianTokenizer
import torch

# Initialize the model and tokenizer for translation
model_name = "Helsinki-NLP/opus-mt-en-zh"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

#translate from rnglish to chinese
def traduire_en_ch(texte):
    # Tokenize input text
    texte_tokenise = tokenizer(texte, return_tensors="pt")
    # Remove 'token_type_ids' if present
    texte_tokenise.pop("token_type_ids", None)
    with torch.no_grad():
        # Generate translation
        traduction = model.generate(**texte_tokenise)
    # Decode the translation
    texte_traduit = tokenizer.decode(traduction[0], skip_special_tokens=True)
    return texte_traduit



#translate from chinese to english

def traduire_zh_en(text, source_lang="zh", target_lang="en"):
    # Load the tokenizer and model for the desired language pair
    model_name = f'Helsinki-NLP/opus-mt-{source_lang}-{target_lang}'
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    
    # Encode and translate the text
    inputs = tokenizer.encode(text, return_tensors="pt")
    translated = model.generate(inputs)
    
    # Decode the translated text
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_text
































