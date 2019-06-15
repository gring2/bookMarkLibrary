import * as tslib_1 from "tslib";
import { Component, Vue } from 'vue-property-decorator';
import Input from '@/components/Input.vue';
import Button from '@/components/Button.vue';
let RegisterBookMark = class RegisterBookMark extends Vue {
    setTag(value) {
        this.tag = value;
        console.log(this.tag);
    }
    setUrl(value) {
        this.url = value;
        console.log(this.url);
    }
};
RegisterBookMark = tslib_1.__decorate([
    Component({
        components: {
            Input,
            Button
        }
    })
], RegisterBookMark);
export default RegisterBookMark;
//# sourceMappingURL=RegisterBookMark.vue.js.map