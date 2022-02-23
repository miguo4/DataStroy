import pickFactTemplate from './fact-templates';
import pickRelationTemplate from './relation-templates';
import FactType from '@/constant/FactType'
import { isValid } from '@/tool/fact2vis/helper'
import AggregationType from '@/constant/AggregationType'
import _ from 'lodash'

const plur = require('plur');
const convertAggregation = function (aggType) {
    switch (aggType) {
        case AggregationType.SUM:
            return 'total'

        case AggregationType.MAX:
            return 'maximum'

        case AggregationType.MIN:
            return 'minimum'

        case AggregationType.AVG:
            return 'average'

        case AggregationType.COUNT:
            return 'count'

        case AggregationType.NONE:
            return ''

        default:
            return ''
    }
}

const convertMeasure = function (measure) {
    if (measure.aggregate === "count") return ""
    else return measure.field.toLowerCase();
}

const convertGroupby = function (groupby, param = 'single') {
    let gb = groupby[0]

    if (param === 'single')
        return gb.toLowerCase()
    else if (param === 'plural') {
        if (gb.indexOf(' of ') !== -1) {
            let gbWords = gb.split(" ")
            let gbWordIndex = gbWords.indexOf("of") - 1
            if (gbWordIndex > -1) {
                let plurWord = plur(gbWords[gbWordIndex], 2)
                return gb.replace(gbWords[gbWordIndex], plurWord)
            }
        } else
            return plur(gb, 2).toLowerCase()
    }
}

// for value/difference/categorization
export const formatNum = function (num) {
    num = (num || 0).toString();
    let number = 0,
        floatNum = '',
        intNum = '';
    if (num.indexOf('.') > 0) {
        num = num.toFixed(2)
        number = num.indexOf('.');
        floatNum = num.substr(number);
        intNum = num.substring(0, number);
    } else {
        intNum = num;
    }
    let result = [],
        counter = 0;
    intNum = intNum.split('');

    for (let i = intNum.length - 1; i >= 0; i--) {
        counter++;
        result.unshift(intNum[i]);
        if (!(counter % 3) && i !== 0) { result.unshift(','); }
    }
    return result.join('') + floatNum || '';
}

const genFactSubspace = function (fact, template) {
    let subspace = '';
    if (fact.subspace.length) {
        fact.subspace.map((key, i) => { return subspace += `${i === 0 ? ' ' : ' and '}the ${key.field} is ${key.value}` })
        template = template.replace("{{subspace}}", subspace);
    } else {
        template = template.replace(", when {{subspace}}", '');
        template = template.replace(" when {{subspace}}", '');
        template = template.replace(" in case of {{subspace}}", '');
        template = template.replace(" given {{subspace}}", '');
        template = template.replace("When {{subspace}}, ", '');
        template = template.replace("Given {{subspace}}, ", '');
        template = template.replace("In case of {{subspace}}, ", '');
    }
    return template
}

export const genFactSentence = function (_fact) {
    if (!isValid(_fact))
        return ''
    let fact = _.cloneDeep(_fact)
    let template = pickFactTemplate(fact.type);
    let aggregate = AggregationType.NONE;
    if (fact.measure.length > 0) {
        aggregate = fact.measure[0].aggregate;
    }
    switch (fact.type) {
        case FactType.ASSOCIATION:
            template = template.replace("{{measure1}}", convertMeasure(fact.measure[0]));
            template = template.replace("{{measure2}}", convertMeasure(fact.measure[1]));
            template = template.replace("{{agg1}}", convertAggregation(fact.measure[0].aggregate));
            template = template.replace("{{agg2}}", convertAggregation(fact.measure[1].aggregate));
            template = genFactSubspace(fact, template)
            if (fact.parameter !== '') {
                template = template.replace("{{parameter}}", formatNum(Number.parseFloat(fact.parameter).toFixed(3)));
            }
            break;

        case FactType.CATEGORIZATION:
            template = template.replace("{{groupby}}s", convertGroupby(fact.groupby, 'plural'));
            template = template.replace("{{groupby}}s", convertGroupby(fact.groupby, 'plural'));
            template = genFactSubspace(fact, template)
            if (fact.parameter.length) {
                template = template.replace("{{parameter}}", formatNum(fact.parameter.length));
                let parameterList = ''
                fact.parameter.forEach((d, i) => {
                    parameterList += `${i === 0 ? '' : ','} ${d}`
                });
                template = template.replace("{{no.1}}, {{no.2}}, {{no.3}}", parameterList);
                // template = template.replace("{{no.1}}", fact.parameter[0]);
                // template = template.replace("{{no.2}}", fact.parameter[1]);
                // if (fact.parameter.length === 3) {
                //     template = template.replace("{{no.3}}", fact.parameter[2]);
                // } else if (fact.parameter.length > 3) {
                //     template = template.replace("{{no.3}}", fact.parameter[2] + ', etc');
                // } else if (fact.parameter.length === 2) {
                //     template = template.replace(", {{no.3}}", '');
                // }
            }
            if (fact.focus.length) {
                if (template.indexOf(". {{focus}}") > -1) {
                    let focusValue = fact.focus[0].value.slice(0, 1).toUpperCase() + fact.focus[0].value.slice(1)
                    template = template.replace("{{focus}}", focusValue);
                } else {
                    template = template.replace("{{focus}}", fact.focus[0].value);
                }
            } else {
                template = template.replace(", and {{focus}} needs to pay attention", "");
                template = template.replace(", among which {{focus}} needs to pay attention", "");
                template = template.replace(". {{focus}} needs to pay attention", "");
            }
            break;

        case FactType.DIFFERENCE:
            template = template.replace("{{measure}}", convertMeasure(fact.measure[0]));
            template = template.replace("{{agg}}", convertAggregation(aggregate));
            if (fact.focus.length >= 2) {
                template = template.replace("{{focus1}}", fact.focus[0].value);
                template = template.replace("{{focus2}}", fact.focus[1].value);
            }
            template = genFactSubspace(fact, template)
            if (fact.parameter !== '') template = template.replace("{{parameter}}", formatNum(fact.parameter));
            break;

        case FactType.DISTRIBUTION:
            template = template.replace("{{measure}}", convertMeasure(fact.measure[0]));
            template = template.replace("{{measure}}", convertMeasure(fact.measure[0]));
            template = template.replace("{{agg}}", convertAggregation(aggregate));
            template = template.replace("{{groupby}}s", convertGroupby(fact.groupby, 'plural'));
            template = template.replace("{{groupby}}", convertGroupby(fact.groupby));
            template = genFactSubspace(fact, template)
            if (fact.focus.length) {
                template = template.replace("{{focus}}", fact.focus[0].value);
            } else {
                template = template.replace(" and {{focus}} needs to pay attention", "");
            }
            break;

        case FactType.EXTREME:
            template = template.replace("{{measure}}", convertMeasure(fact.measure[0]));
            template = template.replace("{{agg}}", convertAggregation(aggregate));
            template = template.replace("{{groupby}}s", convertGroupby(fact.groupby, 'plural'));
            template = template.replace("{{groupby}}", convertGroupby(fact.groupby));
            template = template.replace("{{groupby}}", convertGroupby(fact.groupby));
            template = genFactSubspace(fact, template)
            if (fact.focus.length) {
                if (fact.focus[0].extremeFocus !== undefined && fact.focus[0].extremeValue !== undefined) {
                    if (fact.focus[0].extremeFocus === 'min') { template = template.replace("{{focus}}", 'minimum'); }
                    else { template = template.replace("{{focus}}", 'maximum'); }
                    template = template.replace("{{parameter[0]}}", fact.focus[0].value);
                    template = template.replace("{{parameter[1]}}", formatNum(Math.round(fact.parameter[1] * 100) / 100));

                } else if (fact.parameter.length) {
                    if (fact.parameter[0] === 'min') { template = template.replace("{{focus}}", 'minimum'); }
                    else { template = template.replace("{{focus}}", 'maximum'); }
                    template = template.replace("{{parameter[0]}}", fact.focus[0].value);
                    template = template.replace("{{parameter[1]}}", formatNum(fact.parameter[1]));
                }
            }
            break;

        case FactType.OUTLIER:
            template = template.replace("{{measure}}", convertMeasure(fact.measure[0]));
            template = template.replace("{{measure}}", convertMeasure(fact.measure[0]));
            template = template.replace("{{groupby}}s", convertGroupby(fact.groupby, 'plural'));
            template = template.replace("{{agg}}", convertAggregation(aggregate));
            template = genFactSubspace(fact, template)
            if (fact.focus.length) template = template.replace("{{focus}}", fact.focus[0].value);
            break;

        case FactType.PROPORTION:
            template = template.replace("{{measure}}", convertMeasure(fact.measure[0]));
            template = template.replace("{{agg}}", convertAggregation(aggregate));
            template = template.replace("{{measure}}", convertMeasure(fact.measure[0]));
            template = template.replace("{{agg}}", convertAggregation(aggregate));
            template = genFactSubspace(fact, template)
            if (fact.focus.length) template = template.replace("{{focus}}", fact.focus[0].value);
            if (fact.parameter) template = template.replace("{{parameter}}", fact.parameter);
            break;

        case FactType.RANK:
            template = template.replace("{{measure}}", convertMeasure(fact.measure[0]));
            template = template.replace("{{agg}}", convertAggregation(aggregate));
            template = template.replace("{{groupby}}s", convertGroupby(fact.groupby, 'plural'));
            template = template.replace("{{groupby}}s", convertGroupby(fact.groupby, 'plural'));
            template = genFactSubspace(fact, template)
            if (fact.parameter.length >= 3) {
                template = template.replace("{{parameter}}", formatNum(fact.parameter.length));
                template = template.replace("{{no.1}}", fact.parameter[0]);
                template = template.replace("{{no.2}}", fact.parameter[1]);
                if (fact.parameter.length === 3) {
                    template = template.replace("{{no.3}}", fact.parameter[2]);
                } else if (fact.parameter.length > 3) {
                    template = template.replace("{{no.3}}", fact.parameter[2]);
                } else if (fact.parameter.length === 2) {
                    template = template.replace(", {{no.3}}", '');
                }
            } else {
                template = ''
            }
            break;

        case FactType.TREND:
        
            template = template.replace("{{measure}}", convertMeasure(fact.measure[0]));
            template = template.replace("{{agg}}", convertAggregation(aggregate));
            template = template.replace("{{groupby}}s", convertGroupby(fact.groupby, 'plural'));
            template = genFactSubspace(fact, template)
            if (fact.parameter) {
                template = template.replace("{{parameter}}", fact.parameter);
                if (fact.parameter === 'increasing') {
                    template = template.replace("a/an", 'an');
                } else {
                    template = template.replace("a/an", 'a');
                }
            }
            if (fact.focus.length) {
                template = template.replace("{{focus}}", fact.focus[0].value);
            } else {
                template = template.replace(" and the value of {{focus}} needs to pay attention", "");
            }
            break;

        case FactType.VALUE:
            template = template.replace("{{measure}}", convertMeasure(fact.measure[0]));
            template = template.replace("{{agg}}", convertAggregation(aggregate));
            template = genFactSubspace(fact, template)
            if (fact.focus.length) template = template.replace("{{focus}}", fact.focus[0].value);
            if (fact.parameter !== '') template = template.replace("{{parameter}}", formatNum(fact.parameter));
            break;

        default:
            break;
    }
    template = template.slice(0, 1).toUpperCase() + template.slice(1)
    return template;
}


export const genStoryText = function (facts, relations) {
    let template;
    let storyText = '';
    let pairLength = parseInt(facts.length / 2)
    //console.log("relations", facts, relations)
    for (let i = 0; i < pairLength; i++) {
        if (facts[i]) {
            template = pickRelationTemplate(relations[i * 2 + 1])
            // template = template.replace("{{Sentence A}}", facts[i * 2].script());
            // template = template.replace("{{Sentence B}}", facts[i * 2 + 1].script());
            template = template.replace("{{Sentence A}}", facts[i * 2].generatedScript);
            template = template.replace("{{Sentence B}}", facts[i * 2 + 1].generatedScript);
            storyText += template + ' '
        }
    }
    if (facts.length % 2) {
        //storyText += facts[facts.length - 1].script()
        storyText += facts[facts.length - 1].generatedScript
    }
    //console.log("storyText", storyText)
    return storyText
}

export const genSubtitle = function (fact) {
    let title;
    if (!isValid(fact))
        return ''

    title = 'The ' + fact.type
    switch (fact.type) {
        case FactType.ASSOCIATION:
            title += ' of ' + fact.measure[0].field + ' and ' + fact.measure[1].field
            break;
        case FactType.CATEGORIZATION:
            // title += ' of ' + fact.groupby[0]
            title = fact.groupby[0]
            break;

        case FactType.DIFFERENCE:
            title += ' between ' + fact.focus[0].value + ' and ' + fact.focus[1].value
            break;
        case FactType.DISTRIBUTION:
            title += ' of ' + fact.measure[0].field
            break;
        case FactType.EXTREME:
            title += ' of ' + fact.measure[0].field
            break;
        case FactType.OUTLIER:
            title += ' of ' + fact.measure[0].field
            break;
        case FactType.PROPORTION:
            title += ' of ' + fact.focus[0].value
            break;
        case FactType.RANK:
            title += ' of ' + fact.measure[0].field
            break;
        case FactType.TREND:
            title += ' of ' + fact.measure[0].field
            break;
        case FactType.VALUE:
            title = 'The ' + convertAggregation(fact.measure[0].aggregate) + ' ' + fact.measure[0].field
            break;
        default:
            break;
    }
    if (fact.subspace.length) {
        let subspace = '';
        fact.subspace.map((key, i) => { return subspace += ` in ${key.value}` })
        title += subspace;
    }

    return title;
}

export const genTitle = function (fileName) {
    let title;
    switch (fileName) {
        case 'CarSales.csv':
            title = 'Car Sales'
            break;

        case 'nCoV2020.csv':
            title = 'COVID-19'
            break;

        case 'deadstartup.csv':
            title = 'Startup Failures'
            break;

        default:
            if (fileName.indexOf('.') > 0) {
                let number = fileName.indexOf('.');
                // let csv = fileName.substr(number);
                title = fileName.substring(0, number);
            } else {
                title = fileName
            }
            break;
    }
    return title
}