import { mount, shallowMount } from '@vue/test-utils';
import TagsPanel from '@/views/TagsPanel.vue';

describe('Tag Penel Test', () => {
  it('render Tag component', () => {
    const wrapper = mount(TagsPanel, {
      data: () => {
        return {
          tags: ['test tag1', 'test tag2']
        }
      }
    });
    expect(wrapper.text().indexOf('test tag1')).toBeTruthy()
    expect(wrapper.text().indexOf('test tag2')).toBeTruthy()
  })
})