export default class Relation {
    constructor(type, difference) {
        this.type = type;
        this.difference = difference;
        this.script = ""; //TODO: script for transition
        this.possibility = 1;
    }
}