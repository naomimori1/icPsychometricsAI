from langchain_community.llms import Ollama

"""
PENDÊNCIAS:
pip install langchain

python3 -m venv ollama
source ollama/bin/activate
"""

"""
llm = Ollama(model="mistral")
llm("The first man on the summit of Mount Everest, the highest peak on Earth, was ...")
"""
ollama = Ollama(base_url='http://localhost:11434', model='llama3.1', system='For the following task, respond in a way that matches this description:  “I love kids and dogs. I like to go shoppingwith my daughters. I like to cook. I love to chat with my friends“.  Please respond only with the single number that represents your answer.')

prompt = (
    "Please indicate the extent to which you agree or disagree with the following statement: "
    "“I am someone who is outgoing, sociable”\n"
    "1: Disagree strongly\n"
    "2: Disagree a little\n"
    "3: Neutral\n"
    "4: Agree a little\n"
    "5: Agree strongly\n"
    "Answer:"
)

print(ollama.invoke(prompt))
