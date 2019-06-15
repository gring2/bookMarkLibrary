import * as tslib_1 from "tslib";
import { Component, Vue, Prop } from 'vue-property-decorator';
import BookMarkModel from '@/vo/BookMark';
let BookMark = class BookMark extends Vue {
    search() {
        console.log('search');
    }
};
tslib_1.__decorate([
    Prop({ default: () => new BookMarkModel('', '', '') })
], BookMark.prototype, "bookmark", void 0);
BookMark = tslib_1.__decorate([
    Component({})
], BookMark);
export default BookMark;
//# sourceMappingURL=BookMark.vue.js.map