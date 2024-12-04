from langchain_ollama import OllamaLLM  # Import the OllamaLLM model from langchain_ollama
from langchain.prompts import ChatPromptTemplate  # Import ChatPromptTemplate for creating the prompt template

# Initialize the Ollama model (LLM) with the specified model version
model = OllamaLLM(model="llama3.2")

# Define a template for the prompt that will guide the model to extract specific information
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Define the function to parse content using the Ollama model
def parse_with_ollama(dom_chunks, parse_description):
    # Create a ChatPromptTemplate from the defined template, replacing placeholders with actual values
    prompt = ChatPromptTemplate.from_template(template)
    
    # Create a chain that combines the prompt and the model
    chain = prompt | model

    # List to store the parsed results from each chunk of DOM content
    parsed_results = []

    # Loop over each chunk of DOM content to parse it
    for i, chunk in enumerate(dom_chunks, start=1):
        # Invoke the chain with the current chunk and the description provided by the user
        response = chain.invoke({"dom_content": chunk, 'parse_description': parse_description})
        
        # Print progress for each batch of DOM content being parsed
        print(f'Parsed batch {i} of {len(dom_chunks)}')
        
        # Append the response (parsed content) to the results list
        parsed_results.append(response)
    
    # Return the parsed results as a string, with each result separated by a newline
    return "\n".join(parsed_results)
