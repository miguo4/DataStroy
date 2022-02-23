import requests
import json

class NL4DVGenerator:

    def __init__(self, schema, file_path):
        self.schema = schema
        self.file_path = file_path


    def __schema2attribute_datatype(self):
        attribute_datatype = {}
        for field in self.schema['fields']:
            if field['type'] == 'temporal':
                attribute_datatype[field['field']] = 'T'
            elif field['type'] == 'numerical':
                attribute_datatype[field['field']] = 'Q'
            else:
                attribute_datatype[field['field']] = 'N'

        return attribute_datatype


    def generate(self, question):
        try:
            attribute_datatype = self.__schema2attribute_datatype()
            response = requests.post(
                url="http://talk-nl4dv/analyze_query",
                headers={
                    "Content-Type": "application/json; charset=utf-8",
                },
                data=json.dumps({
                    "debug": True,
                    "ignore_words": [

                    ],
                    "reserve_words": [

                    ],
                    "label_attribute": "Model",
                    "thresholds": {
                        "synonymity": 95,
                        "string_similarity": 85
                    },
                    "query": question,
                    "importance_scores": {
                        "task": {
                            "implicit": 0.5,
                            "explicit": 1
                        },
                        "attribute": {
                            "attribute_alias_exact_match": 0.8,
                            "attribute_synonym_match": 0.5,
                            "attribute_alias_similarity_match": 0.75,
                            "attribute_similarity_match": 0.9,
                            "attribute_exact_match": 1,
                            "attribute_domain_value_match": 0.5
                        },
                        "vis": {
                            "explicit": 1
                        }
                    },
                    "attribute_datatype": attribute_datatype,
                    "data_url": self.file_path,
                    "dependency_parser_config": {
                        "name": "corenlp",
                        "model": "./assets/jars/stanford-english-corenlp-2018-10-05-models.jar",
                        "parser": "./assets/jars/stanford-parser.jar"
                    }
                })
            )
            print(response)
            code = response.status_code
            if code == 500:
                text = "error"
                status = "failed"
            else:
                text = json.loads(response.text)
                status = "success"

        except requests.exceptions.RequestException as e:
            code = 200
            text = "error"
            status = "failed"


        return code , text, status
