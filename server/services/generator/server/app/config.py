import dataclasses

@dataclasses.dataclass
class Config:
    DEBUG = True
    Word2Vec:str = 'trainedmodels/search/GoogleNews-vectors-negative300.bin'
    BERT:str = 'trainedmodels/bert-base-uncased'
    FactClassificationModel: str = 'trainedmodels/search/fact_classification.model'
    SentenceBERT:str = 'trainedmodels/search/paraphrase-distilroberta-base-v1'
    CheckPoints:str = 'trainedmodels/decompose/1600_checkpoint.tar'
    QuestionClassificationModel: str = 'trainedmodels/decompose/topbottom_classification.model'
    model_name: str = 'decompose_model'
    attn_model: str = 'dot' # 'general' or 'concat'
    copy_model: str = 'copy' # generate or copy
    search_size: int = 3
    max_length: int = 60
    candidate_size: int = 30
    hidden_size: int = 256
    sub_hidden_size: int = 256 # half of the hidden_size
    encoder_n_layers: int = 2
    decoder_n_layers: int = 2
    dropout: float = 0.1
    batch_size: int = 512

    clip: float = 50.0
    learning_rate:  float = 0.0001
    decoder_learning_ratio: float = 5.0
    n_iteration: int = 1600 # optimal 3000
    print_every: int = 1
    save_every: int = 50

    train_ratio: float = 0.95 # 80% train
    val_ratio: float = 0.03 # 10% val
    test_ratio: float = 0.02 # 10% test
