import { shallowMount, createLocalVue, mount } from '@vue/test-utils';
import BookMarkList from '@/views/BookMarkList.vue';
import VueRouter from 'vue-router';
import App from '@/App.vue';


describe('BookMarkList.vue', () => {
  it('renders BookMarkList', () => {
    const wrapper = shallowMount(BookMarkList, {
    });

    let mainEle = wrapper.find('main');
    let asideEle = wrapper.find('aside');
    expect(mainEle.exists()).toBeTruthy();
    expect(asideEle.exists()).toBeTruthy();
    expect(mainEle.text()).toBe('BookMarks');
    expect(asideEle.text()).toBe('Tags');

  });


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
              component: () => import(/* webpackChunkName: "about" */ '@/views/BookMarkList.vue'),
            },
      ],
    });

    const wrapper = mount(App, { localVue, router });

    router.push('bookmarks');

    // set expect on latest event queue
    setTimeout(
         () => {
          expect(wrapper.find(BookMarkList).exists()).toBe(true);

        }, 0,
    );
  });

});
