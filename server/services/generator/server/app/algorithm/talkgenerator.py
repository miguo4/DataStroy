from .decompose import DecomposerModel
from .search import Searcher
import datetime

class TalkGenerator:
    def __init__(self, scheme,df):
        self.scheme = scheme
        self.df = df
        self.decomposer = DecomposerModel(self.scheme)
        self.searcher = Searcher(self.scheme,self.df)
        self.RAlog = {
            "num_search": 0,
            "num_decompose": 0,
            "searchedQuestion": [],
            "decomposedQuestion": []
        }

    def __recursive_answer(self, question, num_decompose):
        question_facts = self.searcher.search(question)
        if self.RAlog['num_decompose'] > num_decompose:
            return ['cannot find facts'] 

        if len(question_facts) != 0:
            self.RAlog['num_search'] += 1
            self.RAlog['searchedQuestion'].append(question)
            return [{
                "question": question, 
                "facts": question_facts
                }]

        else:
            sub_question1, sub_question2 = self.decomposer.decompose(question)
            self.RAlog['num_decompose'] += 1
            self.RAlog['decomposedQuestion'].append(question)
            return self.__recursive_answer(sub_question1,num_decompose) + self.__recursive_answer(sub_question2,num_decompose)

    def generate(self, question, num_decompose):
        starttime = datetime.datetime.now()
        storylist = []
        question_facts = self.searcher.search(question)
        if len(question_facts) != 0:
            storylist.append({
                "question": question, 
                "facts": question_facts
            })

        sub_question1, sub_question2 = self.decomposer.decompose(question)

        while len(storylist) <= num_decompose and self.RAlog['num_decompose'] < num_decompose  and (self.RAlog['num_search'] != 2 or self.RAlog['num_decompose'] !=1) and (self.RAlog['num_search'] != 1 or self.RAlog['num_decompose'] != 0) :
            
            storylist = storylist + self.__recursive_answer(sub_question1, num_decompose)
            storylist = storylist + self.__recursive_answer(sub_question2, num_decompose)

        storylist_questions = []

        storylist_no_duplicate= []
        for story in storylist:
            if story == "cannot find facts":
                continue
            
            if story['question'] not in storylist_questions and "<" not in story['question']:
                storylist_questions.append(story['question'])
                storylist_no_duplicate.append(story)
        
        endtime = datetime.datetime.now()
        print(endtime - starttime, flush=True)
        return {
            "story": storylist_no_duplicate
            }

