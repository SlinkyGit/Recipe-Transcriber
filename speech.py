import whisper
import re
import json

model = whisper.load_model("base")
# res = model.transcribe("mp3/recipe.mp3")
res = model.transcribe("mp3/cake-ingredients.mp3")
# res = model.transcribe("mp3/recipe-cake.mp3")

print(res['text'])

# Extract ingredients from the transcribed text
def extract_ingredients(transcript):
    # pattern = r'(\d+\s(?:tablespoon|teaspoon|gallon|cup|ml|liter|ounce|gram)s?\s+of\s+[a-zA-Z\s]+)'
    # pattern = r'(?:(\d+(?:/\d+)?|\d+\.\d+|a pinch|some|a handful|just a bit)\s*)?' \
    #           r'(?:(tablespoon|teaspoon|gallon|cup|ml|liter|litre|ounce|oz|gram|pound)s?)?\s*' \
    #           r'(?:of\s+)?([a-zA-Z][a-zA-Z\s\-]+?)(?=,| and |\.|$)'
    pattern = r'(\d+(?:/\d+)?|\d+\.\d+|one half|half|a half|quarter|a quarter|one fourth|a pinch|some|a handful|lil|little|a little|a little bit|pinch|a pinch|just a bit)' \
              r'(?:(tablespoon|tablespoons|teaspoon|teaspoons|gallon|gallons|cup|cups|ml|milliliter|milliliters|liter|liters|litre|ounce|oz|gram|pound)s?)?\s*' \
              r'(?:of\s+)?([a-zA-Z][a-zA-Z\s\-]+?)(?=,| and |\.|$)'
    matches = re.findall(pattern, transcript.lower())

    ingredients = []

    for amount, unit, item in matches:
        # Clean up the item name
        item = re.sub(r'\s+', ' ', item).strip()

        # Remove any trailing commas or periods
        item = re.sub(r'[,.]$', '', item)

        # Create a dictionary for the ingredient
        ingredient = {
            "quantity": amount.strip() if amount else None,
            "unit": unit.strip() if unit else None,
            "item": item
        }
        ingredients.append(ingredient)

    return ingredients


def jsonify():
    with open("recipe.json", "w") as f:
        # Write the JSON data to the file
        f.write(json.dumps({
            "text": res["text"],
            "ingredients": extract_ingredients(res["text"]),
            "instructions": extract_instructions(res["text"])
        }, indent=2))

def extract_instructions(text):
    # This function should be implemented based on the specific format of the recipe instructions
    cooking_verbs = r'\b(mix|add|stir|bake|boil|let|cook|heat|combine|pour|serve|chop|whisk)\b'
    chunks = text.split('.')
    # chunks = re.split(r'[.?!]\s+', text)

    instructions = []
    found_recipe_start = False 

    for chunk in chunks:
        if re.search(cooking_verbs, chunk, re.IGNORECASE):
            cleaned = chunk.strip().capitalize()
            if cleaned:
                instructions.append(cleaned)
    return instructions

def recipe_generator():
    # This function should be implemented to generate a recipe based on the extracted ingredients
    with open('recipe.md', 'w') as f:

        f.write("# Recipe\n")
        f.write("### Ingredients\n")
        for ingredient in extract_ingredients(res["text"]):
            quantity = ingredient["quantity"] if ingredient["quantity"] else ""
            unit = ingredient["unit"] if ingredient["unit"] else ""
            item = ingredient["item"] if ingredient["item"] else ""
            f.write(f"- {quantity} {unit} {item}\n")

        f.write("\n")

        f.write("### Instructions\n")

        step_number = 1
        for instruction in extract_instructions(res["text"]):

            f.write(f"{step_number}. {instruction}\n")
            step_number += 1



# Tests 
text = res["text"]
ingredients = extract_ingredients(text)

print("Extracted ingredients:")
print(ingredients)

# test = "We need 1 tablespoon of sugar. Mix it well with the flour. Add some water. Let it sit for 10 minutes."
# instructions = extract_instructions(test)
# print("Extracted instructions:")
# print(instructions)

jsonify()
recipe_generator()
