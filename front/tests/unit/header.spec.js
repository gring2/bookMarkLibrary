import { shallowMount } from '@vue/test-utils';
import Header from '@/views/Header.vue';
describe('Header.vue', () => {
    it('renders default props.email', () => {
        const defaultEmail = 'email';
        const wrapper = shallowMount(Header, {});
        expect(wrapper.text()).toMatch(defaultEmail);
    });
    it('render props.email when passed', () => {
        const email = 'test email';
        const wrapper = shallowMount(Header, {
            propsData: {
                email
            }
        });
        expect(wrapper.text()).toMatch(email);
    });
});
//# sourceMappingURL=header.spec.js.map