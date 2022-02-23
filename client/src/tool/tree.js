export const getLeafNodes = (tree) => {
    let nodes = []
    if (!tree) {
        return nodes
    }
    if (tree.size > 2) {
        let leftLeafNodes = getLeafNodes(tree.left);
        let rightLeafNodes = getLeafNodes(tree.right);
        nodes.push(...leftLeafNodes);
        nodes.push(...rightLeafNodes);
    } else if (tree.size === 2) {
        nodes.push([tree.left.value, tree.right.value]);
    } else {
        nodes.push([tree.value]);
    }
    return nodes;
}