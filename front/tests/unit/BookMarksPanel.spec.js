import { mount } from '@vue/test-utils';
import BookMarksPanel from '@/views/BookmarksPanel.vue';
import BookMark from '@/vo/BookMark';
describe('BookMarksPenel Test', () => {
    it('render BookMarksPenel view', () => {
        const wrapper = mount(BookMarksPanel, {
            data: () => {
                return {
                    bookmarks: [new BookMark('tes_title1', 'test_url1', 'test_thumbnail1'),
                        new BookMark('tes_title2', 'test_url2', 'test_thumbnail2')
                    ]
                };
            }
        });
        expect(wrapper.text().indexOf('tes_title1')).toBeTruthy();
        expect(wrapper.text().indexOf('test_url1')).toBeTruthy();
        expect(wrapper.text().indexOf('test_thumbnail1')).toBeTruthy();
        expect(wrapper.text().indexOf('test_url2')).toBeTruthy();
        expect(wrapper.text().indexOf('tes_title2')).toBeTruthy();
        expect(wrapper.text().indexOf('test_thumbnail2')).toBeTruthy();
        expect(wrapper).toMatchSnapshot();
    });
});
//# sourceMappingURL=BookMarksPanel.spec.js.map