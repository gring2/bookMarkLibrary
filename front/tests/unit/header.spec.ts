import {shallowMount, mount, RouterLinkStub, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Header from '@/views/Header.vue'
import { getModule, VuexModule } from 'vuex-module-decorators'
import {userMod} from '@/stores/modules/user'
import store from '@/stores'
import User from '@/vo/User';


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
        calculateisMobile: () => {

        }
      },
    })
    expect(wrapper.find('.login').exists()).toBeTruthy()

  })

  it('no render sign if isMobile is true', () => {

    const wrapper = mount(Header, {
      stubs: {
        RouterLink: RouterLinkStub
      },
      methods: {
        calculateisMobile: () => {
        }
      },
      data:() => {
        return { isMobile: true}
      }
    })

    expect(wrapper.find('.login').exists()).toBeFalsy()

  })
})

describe('Header.vue do not render sign in button when user is not null', ()=>{
  beforeEach(()=> {
    const localVue = createLocalVue()
    localVue.use(Vuex)
  
  })
  it('user is not null', () => {
    const user = new User()
    user.email = 'vuex-email'
    userMod.SET_USER(user)
    const wrapper = mount(Header,{
      stubs: {
        RouterLink: RouterLinkStub
      },

    })

    expect(wrapper.find('.login').exists()).toBeFalsy()
  })

})