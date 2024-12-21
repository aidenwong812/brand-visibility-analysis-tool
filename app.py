import os
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key = OPENAI_API_KEY)

prompts_array = []
brand_name = ''
product_type = ''
brand_dic = {}

def generate(system_content, user_content):
    """
    Generate a response from the AI model using provided system and user content.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "developer", "content": system_content},
                {
                    "role": "user",
                    "content": user_content
                }
            ],
            temperature=0.8
        )

        return completion.choices[0].message.content
    except Exception as e:
        print(f'Error generating : {str(e)}')
        return ''

def generate_prompts(product_type):
    """
    Generate unique prompts based on the product type to explore brand names.
    """
    try:
        global prompts_array
        user_content = f'Generate 50 unique human like prompts to get knowledge about brand names of {product_type}'
        system_content = f'You are a helpful human like prompts generator. Generate the prompts separated by semicolons.'
        prompts = generate(system_content, user_content)
        prompts_array = [prompt.strip() for prompt in prompts.split(';') if prompt.strip()]
    except Exception as e:
        print(f'Error generating prompts : {str(e)}')

class ResearchPaperExtraction(BaseModel):
    """
    Define the structure for extracting brands with frequency from a given context.
    """
    brand_name : list[str]
    frequency: list[int]

def extracting_brand_names(context):
    """
    Extract brand names and their frequencies from unstructured text and store them in a dictionary.
    """
    global brand_dic
    system_content = f"Process the following information related to {product_type}:"
    user_content = context
    

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": f"You are an expert at structured brand name extractor with frequency number. You will be given unstructured text and should extract brand name of {product_type} with frequency number appeared in the context into the given structure."},
            {"role": "user", "content": context}
        ],
        response_format=ResearchPaperExtraction,
    )

    result = completion.choices[0].message.parsed
    brands = result.brand_name
    frequencies = result.frequency
    for index, item in enumerate(brands):
        if item.lower() not in brand_dic:
            brand_dic[item.lower()] = frequencies[index]
        else:
            brand_dic[item.lower()] = brand_dic[item.lower()] + frequencies[index]
     
def recommend(context):
    """
    Recommend the best brand name based on the given context.
    """
    try:
        global product_type
        system_content = f'From the following text, recommend me only one best brand name of {product_type}. The output should be only one word - the best brand name'
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "developer", "content": system_content},
                {
                    "role": "user",
                    "content": context
                }
            ],
            max_tokens=20,
            temperature=0
        )

        return completion.choices[0].message.content
    except Exception as e:
        print(f'Error generating the recommend : {str(e)}')
        return ''


def generate_response():
    """
    Generate responses using generated prompts, extract brand names, and update recommendations in the dictionary.
    """
    global brand_dic
    system_content = f'You are a helpful assistant.'
    for prompt in prompts_array:
        result = generate(system_content, prompt)
        extracting_brand_names(result)
        recommended_brand = recommend(result)
        print(f'Recommeding : {recommended_brand}')
        if recommended_brand != '':
            brand_dic[recommended_brand.lower()] = brand_dic[recommended_brand.lower()] + 1

def calculate_visibility_score():
    """
    Calculate the visibility score of the given brand based on its frequency relative to total mentions.
    """
    global brand_dic
    global brand_name
    total = 0
    frequency = 0
    for key, value in brand_dic.items():
        if key == brand_name.lower():
            frequency = value
            total = total + value
        else:
            total = total + value
    result = round( frequency / total * 100)
    print(result)
    return result

def main():
    global brand_name
    global product_type

    brand_name = input("Enter brand name: ")
    product_type = input("Enter product type: ")
    
    generate_prompts(product_type)
    generate_response()
    result = calculate_visibility_score()

if __name__ == "__main__":
    main()
