import { shallowMount } from '@vue/test-utils';
import BookMark from '@/components/BookMark.vue';
import BookMarkModel from '@/vo/BookMark';
describe('BookMark Test', () => {
    let wrapper;
    beforeEach(() => {
        const bookmark = new BookMarkModel('tes_title', 'tes_url', 'test_thumbnail');
        wrapper = shallowMount(BookMark, {
            propsData: {
                bookmark
            }
        });
    });
    it('bookmark img src should be props bookmark thumbnail property', () => {
        const imgEl = wrapper.find('img').element;
        expect(imgEl.getAttribute('src')).toBe('test_thumbnail');
    });
    it('bookmark a href should be props bookmark url property', () => {
        const aEle = wrapper.find('a').element;
        expect(aEle.getAttribute('href')).toBe('tes_url');
    });
    it('bookmark should show props bookmark title property', () => {
        expect(wrapper.text()).toContain('tes_title');
    });
});
//# sourceMappingURL=BookMark.spec.js.map