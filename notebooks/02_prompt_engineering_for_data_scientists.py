# %% [markdown]
# # Prompt Engineering for Data Scientists
# This script covers advanced prompting techniques specifically useful for data science tasks.
# It aligns with the **Building with the Claude API** and Jupyter notebook course materials.
# 
# ## Objectives:
# 1. Use XML tags to structure data inputs and instructions.
# 2. Implement Few-Shot prompting for custom text classification.
# 3. Instruct Claude to output structured data (JSON) and parse it.

# %%
import os
import json
import pandas as pd
from anthropic import Anthropic

# %%
# Initialize Client
api_key = os.environ.get("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key if api_key else "YOUR_API_KEY_HERE")
MODEL_NAME = "claude-3-5-sonnet-latest"

# %% [markdown]
# ## 1. Using XML Tags for Data Segmentation
# Anthropic models are trained to pay special attention to XML tags (e.g. `<dataset>`, `<instructions>`). 
# They prevent the model from confusing data text with instructions.

# %%
data_snippet = """id,feedback
1,"The product broke on the first use. Terrible build quality."
2,"Amazing service, fast delivery, and the widget works exactly as advertised!"
3,"It is okay, nothing special. A bit overpriced for what it offers."
"""

prompt = f"""
You are an NLP model training assistant. Your job is to label customer sentiment.

<instructions>
Classify the sentiment of each feedback item into one of three categories: Positive, Negative, or Neutral.
Provide your response inside a markdown table.
</instructions>

<dataset>
{data_snippet}
</dataset>

Please output the table now.
"""

print("Prompt structured with XML tags:")
print(prompt)

# %% [markdown]
# ## 2. Few-Shot Prompting
# Few-shot prompting provides Claude with concrete examples of the desired input/output mapping.
# This is extremely useful for specialized data processing tasks.

# %%
few_shot_prompt = """
You are a feature engineering assistant. Your task is to extract medical symptoms from patient notes.

Here are some examples:

<example>
<patient_note>Patient reports running a high fever since Tuesday and a dry cough, but no headache.</patient_note>
<extracted_features>
- fever: True
- cough: True
- headache: False
</extracted_features>
</example>

<example>
<patient_note>Subject has a severe migraine. No signs of fever or runny nose.</patient_note>
<extracted_features>
- fever: False
- cough: False
- headache: True
</extracted_features>
</example>

Now extract features for this patient note:
<patient_note>The patient is coughing severely and complaining of a sore throat, but has no fever.</patient_note>
"""

# %% [markdown]
# ## 3. Requesting and Parsing JSON Outputs
# When automating pipelines, you need structured formats.
# Let's ask Claude to analyze text and output a JSON array, then parse it back into a Pandas DataFrame.

# %%
json_generation_prompt = """
Analyze the following patient review and extract:
1. Product name.
2. The rating (on a scale of 1-5).
3. Listed pros (as a list).
4. Listed cons (as a list).

Review:
"I bought the FitGlow Smartwatch last month. It has excellent battery life lasting up to 5 days, and the heart rate tracker is highly accurate. However, the screen is quite dim in direct sunlight and the strap is a bit stiff."

Output your response strictly as a JSON object, with keys: "product", "rating", "pros", and "cons". Do not include any explanation or markdown formatting other than the JSON itself.
"""

try:
    if api_key:
        print("Calling Claude for JSON output...")
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=500,
            messages=[{"role": "user", "content": json_generation_prompt}]
        )
        
        raw_output = response.content[0].text.strip()
        print("\nRaw output from Claude:")
        print(raw_output)
        
        # Parse output (handling potential markdown code block wrappers)
        if raw_output.startswith("```json"):
            raw_output = raw_output[7:-3].strip()
        elif raw_output.startswith("```"):
            raw_output = raw_output[3:-3].strip()
            
        parsed_json = json.loads(raw_output)
        print("\nSuccessfully parsed JSON:")
        print(parsed_json)
        
        # Load into Pandas
        df_pros_cons = pd.DataFrame({
            "Product": [parsed_json["product"]],
            "Rating": [parsed_json["rating"]],
            "Pros": [", ".join(parsed_json["pros"])],
            "Cons": [", ".join(parsed_json["cons"])]
        })
        print("\nPandas DataFrame:")
        print(df_pros_cons)
        
except Exception as e:
    print(f"\nExecution failed: {e}")
