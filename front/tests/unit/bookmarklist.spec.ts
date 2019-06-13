import { createLocalVue, mount } from '@vue/test-utils'
import BookMarkList from '@/views/BookMarkList.vue'
import VueRouter from 'vue-router'
import App from '@/App.vue'


describe('BookMarkList.vue', () => {
  it('renders a component via routing', () => {
    const localVue = createLocalVue()
    localVue.use(VueRouter)

    const router = new VueRouter({
      mode: 'history',
          base: process.env.BASE_URL,
          routes: [
            {
              path: '/bookmarks',
              name: 'bookmarks',
              // route level code-splitting
              // this generates a separate chunk (about.[hash].js) for this route
              // which is lazy-loaded when the route is visited.
              component: BookMarkList,
            },
            {
              path: '/',
              name: 'home',
            }
      ],
    })

    const wrapper = mount(App, { localVue, router })

    router.push('bookmarks')
    expect(wrapper.find('aside').exists()).toBeTruthy()
    expect(wrapper.element).toMatchSnapshot()
  })

  it('render tag list panel', () => {

    const wrapper = mount(BookMarkList, {
    })
    expect(wrapper.find('aside').exists()).toBeTruthy()
  })

  it('render bookmarks panel', () => {
    const wrapper = mount(BookMarkList, {
    })
    expect(wrapper.find('main').exists()).toBeTruthy()

  })


})
