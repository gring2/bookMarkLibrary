import * as tslib_1 from "tslib";
/>
    < BookmarkList /  >
    /main>
    < /template>
    < script;
lang = ts >
;
import { Component, Vue } from 'vue-property-decorator';
import RegisterBookMark from '@/components/RegisterBookMark.vue';
import BookmarkList from '@/views/BookmarkList.vue';
let BookmarksPanel = class BookmarksPanel extends Vue {
};
BookmarksPanel = tslib_1.__decorate([
    Component({
        components: {
            RegisterBookMark,
            BookmarkList
        }
    })
], BookmarksPanel);
export default BookmarksPanel;
/script>
    < style;
scoped;
lang = "scss" >
    main;
{
    width: 70 % ;
    margin - right;
    5 % ;
}
/style>;
//# sourceMappingURL=BookmarksPanel.vue.js.map