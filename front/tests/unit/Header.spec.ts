import {shallowMount, mount, RouterLinkStub, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Header from '@/views/Header.vue'
import {userMod} from '@/stores/modules/user'
import User from '@/vo/User'

describe('Header.vue', () => {

  it('renders default props.email', () => {

    const defaultEmail = 'email'
    const wrapper = shallowMount(Header, {
      stubs: {
        RouterLink: RouterLinkStub
      }
    })
    expect(wrapper.text()).toMatch(defaultEmail)
  })


  it('render sign in button when user is  null', () => {
    const wrapper = mount(Header, {
      stubs: {
        RouterLink: RouterLinkStub
      },
      methods: {
        calculateisMobile: jest.fn()
      },
    })
    expect(wrapper.find('.login').exists()).toBeTruthy()

  })

  it('no render buttons if isMobile is true', () => {

    const wrapper = mount(Header, {
      stubs: {
        RouterLink: RouterLinkStub
      },
      methods: {
        calculateisMobile: jest.fn()
      },
      data:() => {
        return { isMobile: true}
      }
    })

    expect(wrapper.find('.authenticate').exists()).toBeFalsy()

  })


})

describe('Header.vue do not render sign in button when user is not null', ()=> {
  beforeEach(()=> {
    const localVue = createLocalVue()
    localVue.use(Vuex)

  })
  it('user is not null', () => {
    const user = new User('vuex-email')
    userMod.SET_USER(user)
    const wrapper = mount(Header,{
      stubs: {
        RouterLink: RouterLinkStub
      },

    })

    expect(wrapper.find('.login').exists()).toBeFalsy()
  })

})

describe('Store integration Test', () => {
  it('sign up method call action module SIGN_UP action', () => {
    const wrapper = shallowMount(Header, {
      stubs: {
        RouterLink: RouterLinkStub
      },
    })
    userMod.SIGN_UP = jest.fn()
    const vm: any = wrapper.vm

    vm.signUp()
    expect(userMod.SIGN_UP).toBeCalled()
  })

  it('log out button fire log out action', () => {
    const wrapper = mount(Header, {
      methods: {
        calculateisMobile: jest.fn()
      },
      stubs: {
        RouterLink: RouterLinkStub
      },
    })
    userMod.LOG_OUT = jest.fn()
    wrapper.find('.logout').element.click()

    expect(userMod.LOG_OUT).toBeCalled()
  })
})
