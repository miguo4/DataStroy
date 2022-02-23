const datafilter = (data, subspace) => {
    let filteredData = data;
    for (const sub of subspace) {
        filteredData = filteredData.filter((x)=>x[sub.field]===sub.value)
    }
    return filteredData
}

export default datafilter;