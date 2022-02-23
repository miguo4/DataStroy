import FactType from '@/constant/FactType';
import ChartType from '@/constant/ChartType';
import FieldType from '@/constant/FieldType';
//权重
export const fact2visRules = [
    //association 
    {
        "fact": FactType.ASSOCIATION,
        "chart": ChartType.SCATTER_PLOT,
        "breakdownType": [FieldType.CATEGORICAL, FieldType.TEMPORAL, FieldType.GEOGRAPHICAL]
    },
    //outlier
    // {
    //     "fact": FactType.OUTLIER,
    //     "chart": ChartType.VERTICAL_BAR_CHART,
    //     "breakdownType": [FieldType.CATEGORICAL, FieldType.CATEGORICAL],
    //     // "rang": [0, 9]
    // },
    {
        "fact": FactType.OUTLIER,
        "chart": ChartType.AREA_CHART,
        "breakdownType": [FieldType.TEMPORAL]
    },
    {
        "fact": FactType.OUTLIER,
        "chart": ChartType.LINE_CHART,
        "breakdownType": [FieldType.TEMPORAL]
    },
    // {
    //     "fact": FactType.OUTLIER,
    //     "chart": ChartType.COLOR_FILLING_MAP,
    //     "breakdownType": [FieldType.GEOGRAPHICAL],
    //     // "rang": [0, 9]
    // },
    // {
    //     "fact": FactType.OUTLIER,
    //     "chart": ChartType.BUBBLE_MAP,
    //     "breakdownType": [FieldType.GEOGRAPHICAL],
    //     // "rang": [0, 9]
    // },
    // {
    //     "fact": FactType.OUTLIER,
    //     "chart": ChartType.BUBBLE_CHART,
    // "rang": [6, 9]
    // },
    //extreme
    {
        "fact": FactType.EXTREME,
        "chart": ChartType.VERTICAL_BAR_CHART,
        "breakdownType": [FieldType.CATEGORICAL, FieldType.CATEGORICAL, FieldType.GEOGRAPHICAL],
        // "rang": [0, 9]
    },
    // {
    //     "fact": FactType.EXTREME,
    //     "chart": ChartType.TEXT_CHART,
    //     "breakdownType": [FieldType.CATEGORICAL],
    // },
    {
        "fact": FactType.EXTREME,
        "chart": ChartType.LINE_CHART,
        "breakdownType": [FieldType.TEMPORAL],
    },
    {
        "fact": FactType.EXTREME,
        "chart": ChartType.AREA_CHART,
        "breakdownType": [FieldType.TEMPORAL],
    },
    // {
    //     "fact": FactType.EXTREME,
    //     "chart": ChartType.COLOR_FILLING_MAP,
    //     "breakdownType": [FieldType.GEOGRAPHICAL],
    // },
    // {
    //     "fact": FactType.EXTREME,
    //     "chart": ChartType.BUBBLE_MAP,
    //     "breakdownType": [FieldType.GEOGRAPHICAL],
    // },
    //proportion
    {
        "fact": FactType.PROPORTION,
        "chart": ChartType.PROGRESS_BAR_CHART,
        "breakdownType": [FieldType.CATEGORICAL, FieldType.GEOGRAPHICAL],
    },
    // {
    //     "fact": FactType.PROPORTION,
    //     "chart": ChartType.RING_CHART,
    //     "breakdownType": [FieldType.CATEGORICAL],
    // },
    {
        "fact": FactType.PROPORTION,
        "chart": ChartType.PIE_CHART,
        "breakdownType": [FieldType.CATEGORICAL, FieldType.GEOGRAPHICAL],
    },
    // {
    //     "fact": FactType.PROPORTION,
    //     "chart": ChartType.COLOR_FILLING_MAP,
    //     "breakdownType": [FieldType.GEOGRAPHICAL],
    // },
    // {
    //     "fact": FactType.PROPORTION,
    //     "chart": ChartType.BUBBLE_MAP,
    //     "breakdownType": [FieldType.GEOGRAPHICAL],
    // },
    // {
    //     "fact": FactType.PROPORTION,
    //     "chart": ChartType.VERTICAL_BAR_CHART,
    //"rang": [0, 9]
    // },
    // {
    //     "fact": FactType.PROPORTION,
    //     "chart": ChartType.TEXT_CHART,
    // },

    //rank
    {
        "fact": FactType.RANK,
        "chart": ChartType.HORIZONTAL_BAR_CHART,
        "breakdownType": [FieldType.CATEGORICAL, FieldType.GEOGRAPHICAL],
    },
    // {
    //     "fact": FactType.RANK,
    //     "chart": ChartType.COLOR_FILLING_MAP,
    //     "breakdownType": [FieldType.GEOGRAPHICAL],
    // },
    // {
    //     "fact": FactType.RANK,
    //     "chart": ChartType.BUBBLE_MAP,
    //     "breakdownType": [FieldType.GEOGRAPHICAL],
    // },
    // {
    //     "fact": FactType.RANK,
    //     "chart": ChartType.LINE_CHART,
    //     "breakdownType": [FieldType.CATEGORICAL, FieldType.TEMPORAL],
    // },
    //distribution
    // {
    //     "fact": FactType.DISTRIBUTION,
    //     "chart": ChartType.COLOR_FILLING_MAP,
    //     "breakdownType": [FieldType.GEOGRAPHICAL],
    // },
    // {
    //     "fact": FactType.DISTRIBUTION,
    //     "chart": ChartType.BUBBLE_MAP,
    //     "breakdownType": [FieldType.GEOGRAPHICAL],
    // },
    {
        "fact": FactType.DISTRIBUTION,
        "chart": ChartType.AREA_CHART,
        "breakdownType": [FieldType.TEMPORAL],
    },
    // {
    //     "fact": FactType.DISTRIBUTION,
    //     "chart": ChartType.TREE_MAP,
    //     "breakdownType": [FieldType.CATEGORICAL],
    //     "rang": [6, 10000]
    // },
    {
        "fact": FactType.DISTRIBUTION,
        "chart": ChartType.VERTICAL_BAR_CHART,
        "breakdownType": [FieldType.CATEGORICAL, FieldType.GEOGRAPHICAL],
       // "rang": [0, 9]
    },
    // {
    //     "fact": FactType.DISTRIBUTION,
    //     "chart": ChartType.HORIZONTAL_BAR_CHART,
    // },
    // {
    //     "fact": FactType.DISTRIBUTION,
    //     "chart": ChartType.BUBBLE_MAP,
    // },
    // {
    //     "fact": FactType.DISTRIBUTION,
    //     "chart": ChartType.PIE_CHART,
    // },
    // //difference
    // {
    //     "fact": FactType.DIFFERENCE,
    //     "chart": ChartType.COLOR_FILLING_MAP,
    //     "breakdownType": [FieldType.GEOGRAPHICAL],
    // },
    // {
    //     "fact": FactType.DIFFERENCE,
    //     "chart": ChartType.VERTICAL_BAR_CHART,
    //     "breakdownType": [FieldType.CATEGORICAL],
    // },
    // {
    //     "fact": FactType.DIFFERENCE,
    //     "chart": ChartType.TEXT_CHART,
    //     "breakdownType": [FieldType.CATEGORICAL],
    // },
    // {
    //     "fact": FactType.DIFFERENCE,
    //     "chart": ChartType.PIE_CHART,
    // },
    {
        "fact": FactType.DIFFERENCE,
        "chart": ChartType.HORIZONTAL_BAR_CHART,
        "breakdownType": [FieldType.CATEGORICAL, FieldType.GEOGRAPHICAL,FieldType.TEMPORAL],
    },
    //categorization
    // {
    //     "fact": FactType.CATEGORIZATION,
    //     "chart": ChartType.COLOR_FILLING_MAP,
    //     "breakdownType": [FieldType.GEOGRAPHICAL],
    // },
    // {
    //     "fact": FactType.CATEGORIZATION,
    //     "chart": ChartType.TREE_MAP,
    //     "breakdownType": [FieldType.CATEGORICAL],
    //     "rang": [6, 10000]
    // },
    {
        "fact": FactType.CATEGORIZATION,
        "chart": ChartType.VERTICAL_BAR_CHART,
        "breakdownType": [FieldType.CATEGORICAL, FieldType.GEOGRAPHICAL],
        //"rang": [0, 9]
    },
    // {
    //     "fact": FactType.CATEGORIZATION,
    //     "chart": ChartType.BUBBLE_CHART,
    //     "breakdownType": [FieldType.CATEGORICAL],
    //     "rang": [6, 9]
    // },
    //trend
    {
        "fact": FactType.TREND,
        "chart": ChartType.LINE_CHART,
        "breakdownType": [FieldType.TEMPORAL],
    },
    {
        "fact": FactType.TREND,
        "chart": ChartType.AREA_CHART,
        "breakdownType": [FieldType.TEMPORAL],
    },
    // {
    //     "fact": FactType.TREND,
    //     "chart": ChartType.VERTICAL_BAR_CHART,
    //     "rang": [0, 9]
    // },
    // {
    //     "fact": FactType.TREND,
    //     "chart": ChartType.BUBBLE_CHART,
    //"rang": [6, 9]
    // },

    //value
    // {
    //     "fact": FactType.VALUE,
    //     "chart": ChartType.TEXT_CHART,
    //     "breakdownType": [],
    // },
    // {
    //     "fact": FactType.VALUE,
    //     "chart": ChartType.HORIZONTAL_BAR_CHART,
    // },
    {
        "fact": FactType.VALUE,
        "chart": ChartType.VERTICAL_BAR_CHART,
    },
    // {
    //     "fact": FactType.VALUE,
    //     "chart": ChartType.BUBBLE_MAP,
    // },
    // {
    //     "fact": FactType.VALUE,
    //     "chart": ChartType.COLOR_FILLING_MAP,
    // }
]