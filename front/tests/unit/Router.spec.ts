import { mount, createLocalVue } from '@vue/test-utils'
import VueRouter from 'vue-router'
import Library from '@/views/Library.vue'
import SignUp from '@/views/SignUp.vue'
import SignIn from '@/views/SignIn.vue'
import App from '@/App.vue'

describe('Router rendering views', () => {
  let localVue: any;
  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(VueRouter)

  })

  it('renders a SignUp Views via routing', () => {
    const router = new VueRouter({
      mode: 'history',
          base: process.env.BASE_URL,
          routes: [
            {
              path: '/signup',
              name: 'signup',
              component: SignUp,
            },
      ],
    })
    SignUp
    const wrapper = mount(App, { localVue, router })

    router.push('/signup')
    wrapper.vm.$nextTick(() => {
      expect(wrapper.find(SignUp).exists()).toBeTruthy()
      expect(wrapper.element).toMatchSnapshot()
  
    })
  })

  it('renders a Library view via routing', () => {

    const router = new VueRouter({
      mode: 'history',
          base: process.env.BASE_URL,
          routes: [
            {
              path: '/bookmarks',
              name: 'bookmarks',
              component: Library,
            },
      ],
    })

    const wrapper = mount(App, { localVue, router })

    router.push('/bookmarks')
    expect(wrapper.find(Library).exists()).toBeTruthy()
    expect(wrapper.element).toMatchSnapshot()
  })

  it('renders a SignIn view via routing', () => {

    const router = new VueRouter({
      mode: 'history',
          base: process.env.BASE_URL,
          routes: [
            {
              path: '/signin',
              name: 'signin',
              component: SignIn,
            },
      ],
    })

    const wrapper = mount(App, { localVue, router })

    router.push('/signin')
    expect(wrapper.find(SignIn).exists()).toBeTruthy()
    expect(wrapper.element).toMatchSnapshot()
  })

})