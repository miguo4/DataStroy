import _ from 'lodash';
import {hcluster} from './hcluster';
import {getLeafNodes} from './tree';
import {factSimilarity} from './distance';
import {factAggRules} from './factAggRule';
import ChartType from '../constant/ChartType';

export const storyAggregation = function(original_facts, aggregationLevel) {
    let facts = original_facts.slice();
    for (let index = 0; index < facts.length; index++) {
        facts[index].index = index;
        facts[index].aggregated = false;
        facts[index].aggregatedFact = null;
    }
    // Step 1. construct a hierachical cluster tree
    let htree = hcluster(facts);
    // Step 2. get all single leaf and double leaves
    let nodes = getLeafNodes(htree);
    // Step 3. filter double leaves
    let doubleNodes = nodes.filter(x=>x.length>1);
    // Step 4. rank according to fact similarity
    doubleNodes.sort(function(a, b){return factSimilarity(b[0], b[1]) - factSimilarity(a[0], a[1])});
    let aggregationCount = parseInt((doubleNodes.length+1) * aggregationLevel)
    let aggFacts = doubleNodes.slice(0, aggregationCount);
    for (const aggFact of aggFacts) {
        let firstIndex = aggFact[0].index < aggFact[1].index? aggFact[0].index:aggFact[1].index;
        let secondIndex = aggFact[0].index > aggFact[1].index? aggFact[0].index:aggFact[1].index;
        facts[firstIndex] = factAggregation(facts[firstIndex], facts[secondIndex])
        facts[secondIndex].aggregated = true;
        facts[secondIndex].aggregatedFact = null;
    }
    return facts;
}

export const factAggregation = function(f1, f2) {
    let rule = factAggRules.filter(x=>(x['Fact Type 1']===f1.type&&x['Fact Type 2']===f2.type))[0]
    let compoundFact = _.cloneDeep(f1);
    compoundFact.aggregated = true;
    compoundFact.aggregatedFact = _.cloneDeep(f2)
    compoundFact.compoundType = [f1.type, f2.type];
    compoundFact.compoundChart = ChartType.JUXTAPOSITION;
    compoundFact.score += compoundFact.aggregatedFact.score;
    // Step 1. check rule is juxtaposition or not
    if (rule.chart === ChartType.JUXTAPOSITION) {
        return compoundFact;
    }
    // Step 2. process stacked chart
    if (rule.chart === ChartType.STACKED_BAR_CHART) {
        compoundFact.compoundChart = ChartType.STACKED_BAR_CHART;
        return compoundFact;
    }
    if (rule.chart === ChartType.STACKED_LINE_CHART) {
        compoundFact.compoundChart = ChartType.STACKED_LINE_CHART;
        return compoundFact;
    }

    // Step 3. check equal rule
    if (rule['Measure'] === "equal") {
        let measure1 = new Set(f1.measure.map(x=>x["field"]));
        let measure2 = new Set(f2.measure.map(x=>x["field"]));
        if (!eqSet(measure1, measure2)) {
            return compoundFact;
        }
    }
    if (rule['Subspace'] === "equal") {
        let subspace1 = new Set(f1.subspace.map(x=>x["field"]+"++"+x["value"]));
        let subspace2 = new Set(f2.subspace.map(x=>x["field"]+"++"+x["value"]));
        if (!eqSet(subspace1, subspace2)) {
            return compoundFact;
        }
    }
    if (rule['Groupby'] === "equal") {
        let groupby1 = new Set(f1.groupby);
        let groupby2 = new Set(f2.groupby);
        if (!eqSet(groupby1, groupby2)) {
            return compoundFact;
        }
    }
    if (rule['Focus'] === "equal") {
        let focus1 = new Set(f1.focus.map(x=>x["field"]+"++"+x["value"]));
        let focus2 = new Set(f2.focus.map(x=>x["field"]+"++"+x["value"]));
        if (!eqSet(focus1, focus2)) {
            return compoundFact;
        }
    }
    // Step 4. fill fact
    compoundFact.compoundChart = rule['Chart'];
    if (rule['Measure'] !== "equal" && rule['Measure'] !== "") {
        if (f1.type === rule['Measure']) {
            compoundFact.measure = f1.measure;
        } else {
            compoundFact.measure = f2.measure;
        }
    }
    if (rule['Subspace'] !== "equal" && rule['Subspace'] !== "") {
        if (f1.type === rule['Subspace']) {
            compoundFact.subspace = f1.subspace;
        } else {
            compoundFact.subspace = f2.subspace;
        }
    }
    if (rule['Groupby'] !== "equal" && rule['Groupby'] !== "") {
        if (f1.type === rule['Groupby']) {
            compoundFact.groupby = f1.groupby;
        } else {
            compoundFact.groupby = f2.groupby;
        }
    }
    if (rule['Focus'] !== "equal" && rule['Focus'] !== "") {
        if (f1.type === rule['Focus']) {
            compoundFact.focus = f1.focus;
        } else {
            compoundFact.focus = f2.focus;
        }
    }
    
    return compoundFact;
}

function eqSet(as, bs) {
    if (as.size !== bs.size) return false;
    for (var a of as) if (!bs.has(a)) return false;
    return true;
}