import RelationType from '@/constant/RelationType';
import similarity from './similarity';
import contrast from './contrast';
import temporal from './temporal';
import cause from './cause-effect';
import elaboration from './elaboration';
import generalization from './generalization';

const templateCount = 3;

const pickRelationTemplate = function(type, id=-1) {
    // pick randomly when id == -1
    let templates = []
    switch (type) {
        case RelationType.SIMILARITY:
            templates = similarity;
            break;

        case RelationType.CONTRAST:
            templates = contrast;
            break;

        case RelationType.CAUSE:
            templates = cause;
            break;

        case RelationType.TEMPORAL:
            templates = temporal;
            break;

        case RelationType.ELABORATION:
            templates = elaboration;
            break;

        case RelationType.GENERALIZATION:
            templates = generalization;
            break;
    
        default:
            templates = Array(templateCount).fill({
                'template': '{{Sentence A}} {{Sentence B}}',
            });
            break;
    }
    if (id === -1) {
        id = Math.floor(Math.random() * 10)%templateCount    
    }
    let sentence = '';
    try {
        sentence = templates[id].template;
    }
    catch(error) {
        console.error(error);
        console.log('wrong type:'+type)
        console.log('wrong templates:'+templates)
        console.log('wrong id:'+id)
    }
    return sentence;
}

export default pickRelationTemplate;