import * as tslib_1 from "tslib";
import { Component, Prop, Vue } from 'vue-property-decorator';
let Input = class Input extends Vue {
};
tslib_1.__decorate([
    Prop()
], Input.prototype, "change", void 0);
tslib_1.__decorate([
    Prop()
], Input.prototype, "placeholder", void 0);
tslib_1.__decorate([
    Prop({ default: () => Object.create({}) })
], Input.prototype, "styles", void 0);
Input = tslib_1.__decorate([
    Component
], Input);
export default Input;
//# sourceMappingURL=Input.vue.js.map