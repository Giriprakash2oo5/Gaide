from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer

references = ["""1. Boron has the capacity to absorb neutrons. Hence, its isotope 10B5
 is used as moderator in 
nuclear reactors. 
2. Amorphous boron is used as a rocket fuel igniter. 
3. Boron is essential for the cell walls of plants. 
4. Compounds of boron have many applications. For example eye drops, antiseptics, washing 
powders etc.. contains boric acid and borax. In the manufacture of Pyrex glass , boric oxide 
is used."""]
generated = ["""1. Neutron Absorption: Its isotope, 
10B5, is capable of absorbing neutrons, making it useful as a moderator in nuclear reactors.
2. Rocket Fuel Igniter: Amorphous boron is employed as an igniter for rocket fuels.
3. Plant Cell Walls: Boron is a crucial element for the formation of cell walls in plants.
4. Compound Applications: Boron compounds find many applications. For instance, boric acid and borax are found in eye drops, antiseptics, and washing powders. Boric oxide is used in the manufacturing process of Pyrex glass."""]

# BLEU Score
bleu_score = sentence_bleu([ref.split() for ref in references], generated[0].split())

# ROUGE Score
scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
scores = scorer.score(references[0], generated[0])

print("BLEU Score:", round(bleu_score, 2))
print("ROUGE-1:", round(scores['rouge1'].fmeasure, 2))
print("ROUGE-L:", round(scores['rougeL'].fmeasure, 2))

accuracy = (bleu_score + scores['rouge1'].fmeasure) / 2 * 100
print("Approx. Accuracy (%):", round(accuracy, 2))
