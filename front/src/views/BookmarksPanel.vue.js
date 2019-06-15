import * as tslib_1 from "tslib";
import { Component, Vue } from 'vue-property-decorator';
import RegisterBookMark from '@/components/RegisterBookMark.vue';
import BookMark from '@/components/BookMark.vue';
import BookMarkModel from '@/vo/BookMark';
let BookmarksPanel = class BookmarksPanel extends Vue {
    constructor() {
        super(...arguments);
        this.bookmarks = [new BookMarkModel('title', '#', 'https://cdn.qiita.com/assets/qiita-fb-2887e7b4aad86fd8c25cea84846f2236.png')];
    }
};
BookmarksPanel = tslib_1.__decorate([
    Component({
        components: {
            RegisterBookMark,
            BookMark
        }
    })
], BookmarksPanel);
export default BookmarksPanel;
//# sourceMappingURL=BookmarksPanel.vue.js.map