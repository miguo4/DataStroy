from q2f import Question2Fact
from schema import Schema

schema = Schema()
schema.add_column(field="Income", dtype="numerical")
schema.add_column(field="Sales", dtype="numerical")
schema.add_column(field="Brand", dtype="categorical", values=["BMW", "Ford", "Honda"])
schema.add_column(field="Category", dtype="categorical", values=["SUV", "Sporty"])
schema.add_column(field="Country", dtype="geographical", values=["Japan", "America", "Europe"])
schema.add_column(field="Year", dtype="temporal", values=["2007", "2008", "2009", "2010", "2011"])

q2f = Question2Fact(schema)
# facts = q2f.generate("show me the distribution of the income by brand in Japan")
# facts = q2f.generate("What is the trend of car sales in Japan")


input_sentence = ''
while(1):
    try:
        # Get input sentence
        input_sentence = input('> question to facts:')

        # Check if it is quit case
        if input_sentence == 'q' or input_sentence == 'quit': break

        facts = q2f.generate(input_sentence)
        print('===========================')
        print('facts: ')
        for fact in facts:
            print(fact)

    except KeyError:
        print("Error: Encountered unknown word.")