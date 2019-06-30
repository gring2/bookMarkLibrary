import { mount } from '@vue/test-utils'
import Library from '@/views/Library.vue'

describe('Library.vue', () => {

  it('Tagpanel exists in Library', () => {

    const wrapper = mount(Library, {
    })
    expect(wrapper.find('aside').exists()).toBeTruthy()
  })

  it('BookMarkPanel exits in Library', () => {
    const wrapper = mount(Library, {
    })
    expect(wrapper.find('main').exists()).toBeTruthy()

  })


})


