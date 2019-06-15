import * as tslib_1 from "tslib";
import { Component, Vue } from 'vue-property-decorator';
import Tag from '@/components/Tag.vue';
let TagsPanel = class TagsPanel extends Vue {
    constructor() {
        super(...arguments);
        this.tags = [];
    }
    created() {
        this.tags = ['test1', 'test2'];
    }
};
TagsPanel = tslib_1.__decorate([
    Component({
        components: {
            Tag,
        },
    })
], TagsPanel);
export default TagsPanel;
//# sourceMappingURL=TagsPanel.vue.js.map