from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

reference = """1. Boron has the capacity to absorb neutrons. Hence, its isotope 10B5
 is used as moderator in 
nuclear reactors. 
2. Amorphous boron is used as a rocket fuel igniter. 
3. Boron is essential for the cell walls of plants. 
4. Compounds of boron have many applications. For example eye drops, antiseptics, washing 
powders etc.. contains boric acid and borax. In the manufacture of Pyrex glass , boric oxide 
is used."""
generated = """1. Neutron Absorption: Its isotope, 
10B5, is capable of absorbing neutrons, making it useful as a moderator in nuclear reactors.
2. Rocket Fuel Igniter: Amorphous boron is employed as an igniter for rocket fuels.
3. Plant Cell Walls: Boron is a crucial element for the formation of cell walls in plants.
4. Compound Applications: Boron compounds find many applications. For instance, boric acid and borax are found in eye drops, antiseptics, and washing powders. Boric oxide is used in the manufacturing process of Pyrex glass."""

emb1 = model.encode(reference, convert_to_tensor=True)
emb2 = model.encode(generated, convert_to_tensor=True)

similarity = util.cos_sim(emb1, emb2).item()

accuracy = round(similarity * 100, 2)

print(f"Semantic Similarity: {similarity:.2f}")
print(f"Approx. Accuracy (%): {accuracy}%")
