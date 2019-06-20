import {createLocalVue, mount, shallowMount, RouterLinkStub} from '@vue/test-utils'
import {VuexModule, getModule} from 'vuex-module-decorators'
import Vuex from 'vuex'
import User from '@/vo/User'

import UserModule, { userMod } from '@/stores/modules/user'
import Header from '@/views/Header.vue'
describe('SET USER', () => {
  let userMod: any

  beforeEach(() => {
      userMod = new VuexModule({
        state: UserModule.state,
        mutations: UserModule.mutations,
        getters: UserModule.getters
      })
      const localVue = createLocalVue()
      localVue.use(Vuex)
  })

  it('adds a user to the state', () => {
    const user = new User()
    user.email = 'test@email.com'
    user.token = 'test token'

    const state = {
      token: null,
      user: null
    }

    userMod.mutations.SET_USER(state, user)
    expect(state.user).toEqual(
      user
    )
    expect(state.token).toBe('test token')
  })

  it('get a user state', () => {
    fail('no implemented')
  })
})


describe('get user', () => {
  const localVue = createLocalVue()
  localVue.use(Vuex)


  it('renders a username using a real Vuex store', () => {
    const user = new User()
    user.email = 'vuex-email'
    userMod.SET_USER(user)
    const wrapper = mount(Header)

    expect(wrapper.find('p').text()).toBe('Hi! vuex-email')
  })

})