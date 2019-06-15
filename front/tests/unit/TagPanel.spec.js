import { mount } from '@vue/test-utils';
import TagsPanel from '@/views/TagsPanel.vue';
describe('TagPenel Test', () => {
    it('render TagPenel view', () => {
        const wrapper = mount(TagsPanel, {
            data: () => {
                return {
                    tags: ['test tag1', 'test tag2']
                };
            }
        });
        expect(wrapper.text().indexOf('test tag1')).toBeTruthy();
        expect(wrapper.text().indexOf('test tag2')).toBeTruthy();
        expect(wrapper).toMatchSnapshot();
    });
});
//# sourceMappingURL=TagPanel.spec.js.map