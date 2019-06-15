import * as tslib_1 from "tslib";
;
class {
}
"$style.container" >
    v - ;
for ( = "bookmark in bookmarks" >
; ; )
    : bookmark = "bookmark" > /BookMark>
        < /li>
        < /ul>
        < /div>
        < /template>
        < script;
lang = ts >
;
import { Component, Vue } from 'vue-property-decorator';
import BookMark from '@/components/BookMark.vue';
import BookMarkModel from '@/vo/BookMark';
let BookmarkList = class BookmarkList extends Vue {
    constructor() {
        super(...arguments);
        this.bookmarks = [new BookMarkModel('title', '#', 'https://cdn.qiita.com/assets/qiita-fb-2887e7b4aad86fd8c25cea84846f2236.png')];
    }
};
BookmarkList = tslib_1.__decorate([
    Component({
        components: {
            BookMark
        }
    })
], BookmarkList);
export default BookmarkList;
/script>
    < style;
"scss" >
;
import "@/styles/mixins.scss";
container;
{
    margin - top;
    2;
    rem;
    border - top;
    1;
    px;
    solid;
    e4e6e8;
    ul;
    {
        padding: 0;
        list - style - type;
        none;
        width: 100 % ;
        height: 100 % ;
        align - items;
        center;
        flex;
        flex - wrap;
        wrap;
        -webkit - flex - flow;
        row;
        wrap;
        justify - content;
        space - between;
        li;
        {
            display: block;
            margin - bottom;
            2;
            rem;
        }
    }
}
/style>;
//# sourceMappingURL=BookmarkList.vue.js.map