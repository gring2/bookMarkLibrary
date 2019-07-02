import * as tslib_1 from "tslib";
import { Component, Prop, Vue } from 'vue-property-decorator';
let Button = class Button extends Vue {
};
tslib_1.__decorate([
    Prop({ default: '' })
], Button.prototype, "className", void 0);
tslib_1.__decorate([
    Prop({ default: () => Object.create({}) })
], Button.prototype, "styles", void 0);
tslib_1.__decorate([
    Prop({ default: () => () => { return; } })
], Button.prototype, "click", void 0);
Button = tslib_1.__decorate([
    Component
], Button);
export default Button;
//# sourceMappingURL=Button.vue.js.map