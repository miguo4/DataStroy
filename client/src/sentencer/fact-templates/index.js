import FactType from '../../constant/FactType';
import association from './association';
import categorization from './categorization';
import difference from './difference';
import distribution from './distribution';
import extreme from './extreme';
import outlier from './outlier';
import proportion from './proportion';
import rank from './rank';
import trend from './trend';
import value from './value';

const templateCount = 3;

const pickFactTemplate = function(type, id=-1) {
    // pick randomly when id == -1
    let templates = []
    switch (type) {
        case FactType.ASSOCIATION:
            templates = association;
            break;

        case FactType.CATEGORIZATION:
            templates = categorization;
            break;

        case FactType.DIFFERENCE:
            templates = difference;
            break;

        case FactType.DISTRIBUTION:
            templates = distribution;
            break;

        case FactType.EXTREME:
            templates = extreme;
            break;

        case FactType.OUTLIER:
            templates = outlier;
            break;

        case FactType.PROPORTION:
            templates = proportion;
            break;

        case FactType.RANK:
            templates = rank;
            break;

        case FactType.TREND:
            templates = trend;
            break;

        case FactType.VALUE:
            templates = value;
            break;
    
        default:
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
        console.log('wrong id:'+id)
    }
    return sentence;
}

export default pickFactTemplate;