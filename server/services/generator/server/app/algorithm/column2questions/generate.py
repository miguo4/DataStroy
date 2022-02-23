from BottomupGenerator import BottomupQuestionGenerator
from TopdownGenerator import TopdownQuestionGenerator
from SQGenerator import SimpleQuestionGenerator
import os
import json
import csv
from copy import deepcopy
import shutil

def json_csv_writer (file_name,json_name,table_name) :

    jsonFile = open('./output/%s.json'%(file_name), 'a')
    jsonFile.write(json.dumps(json_name))
    jsonFile.close()

    csvFile = open('./output/%s.csv'%(file_name), 'a')
    csv_writer = csv.writer(csvFile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    

    if json_name == sq_template_json:
        for index, q in enumerate(json_name):
            csv_writer.writerow([table_name , '%s_%d'%(table_name,index), q['fact']['type'], q['question'], json.dumps(q['fact'])])
    elif json_name == topdown_question_json :
        for index, q in enumerate(json_name):
            csv_writer.writerow([table_name , '%s_%d'%(table_name,index), q['question'], q['fact']])
    elif json_name == bott_up_question_json :
        for index, q in enumerate(json_name):
            csv_writer.writerow([table_name , '%s_%d'%(table_name,index), q['type'], q['question'], q['facts'], q['entity']])
    else:
        for index, q in enumerate(json_name):
            csv_writer.writerow([table_name , '%s_%d'%(table_name,index), q['type'], q['question'], q['sub-question-1'], q['sub-question-2']])
    
    csvFile.close()



def is_json_file(filename):
    return any(filename.endswith(extension) for extension in ['.json'])

shutil.rmtree('./output') 

if not os.path.isdir('./output'):
    os.mkdir('./output')

csvFile = open('./output/sq_template.csv', 'a')
csv_writer = csv.writer(csvFile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
csv_writer.writerow(['table_name' , '_id', 'type', 'question', 'fact'])

csvFile = open('./output/top_down_dataset.csv', 'a')
csv_writer = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
csv_writer.writerow(['table_name' , '_id', 'question', 'fact'])

csvFile = open('./output/bottom_up_dataset.csv', 'a')
csv_writer = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
csv_writer.writerow(['table_name' , '_id', 'type', 'question', 'supporting_facts', 'entity'])

csvFile = open('./output/paired_dataset.csv', 'a')
csv_writer = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
csv_writer.writerow(['table_name' , '_id', 'type', 'question', 'sub-question-1', 'sub-question-2'])


file_path='./schema'
for table in [x for x in os.listdir(file_path) if is_json_file(x)]:
    with open('schema/%s'%(table)) as f:
        schema = json.load(f)
        table_name = deepcopy(table).replace('.json','')
    sg = SimpleQuestionGenerator()
    sg.load(schema)
    sq_template_json=sg.generate() 
    json_csv_writer('sq_template',sq_template_json,table_name)

    # cg_topdown = TopdownQuestionGenerator()
    # cg_topdown.load(schema)
    # topdown_question_json=cg_topdown.generate()
    # json_csv_writer('top_down_dataset',topdown_question_json,table_name)

    # cg_bottomup = BottomupQuestionGenerator()
    # cg_bottomup.load(schema)
    # bott_up_question_json=cg_bottomup.generate()
    # json_csv_writer('bottom_up_dataset',bott_up_question_json,table_name)
    # bott_up_paired=cg_bottomup.generate_paired()
    # json_csv_writer('paired_dataset',bott_up_paired,table_name)


  


# fact={
#     'type': 'distribution', 
#     'subspace':[
#         {
#             'field':'Brand',
#             'value':'BMW',
#             'type':'categorical'
#         }
#     ],
#     'measure':[
#         {
#             'field':'Category',
#             'aggregate':'sum'
#         }
#     ],
#     'breakdown':[
#         {
#             'field':'DATE',
#             'type':'temporal'
#         }
#     ],
#     'focus':[
#         # {
#         #     'field':'Brand',
#         #     'value':'BMW',
#         # }
#     ]
# }
# sg.generate_from_fact(fact)


