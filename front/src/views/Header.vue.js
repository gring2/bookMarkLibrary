import * as tslib_1 from "tslib";
import { Component, Prop, Vue } from 'vue-property-decorator';
import Button from '@/components/Button';
let Header = class Header extends Vue {
};
tslib_1.__decorate([
    Prop()
], Header.prototype, "user", void 0);
Header = tslib_1.__decorate([
    Component({
        components: {
            Button,
        },
    })
], Header);
export default Header;
//# sourceMappingURL=Header.vue.js.map