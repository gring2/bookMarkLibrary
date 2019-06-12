import * as tslib_1 from "tslib";
;
"search" > {};
{
    tag;
}
/span>
    < /template>
    < script;
lang = "ts" >
;
import { Component, Vue, Prop } from 'vue-property-decorator';
let Tag = class Tag extends Vue {
    search() {
        console.log('search');
    }
};
tslib_1.__decorate([
    Prop()
], Tag.prototype, "tag", void 0);
Tag = tslib_1.__decorate([
    Component({})
], Tag);
export default Tag;
/script>
    < style;
scoped;
lang = "scss" >
    span;
{
    cursor: pointer;
        & ;
    hover;
    {
        color: blue;
    }
}
/style>;
//# sourceMappingURL=Tag.vue.js.map