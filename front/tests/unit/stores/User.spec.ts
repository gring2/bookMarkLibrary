import {createLocalVue, mount, shallowMount, RouterLinkStub} from '@vue/test-utils'
import { VuexModule } from 'vuex-module-decorators'
import Vuex from 'vuex'
import User from '@/vo/User'

import UserModule, { userMod } from '@/stores/modules/user'
import Header from '@/views/Header.vue'

import axios from 'axios'
jest.mock('axios')


describe('SET USER', () => {
  let userMod: any

  beforeEach(() => {
      userMod = new VuexModule({
        state: UserModule.state,
        mutations: UserModule.mutations,
        getters: UserModule.getters,
        actions: UserModule.actions
      })
      const localVue = createLocalVue()
      localVue.use(Vuex)
  })

  it('mutation SET_UP adds a user to the state', () => {
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

  it('mutation IS_SIGNUP change error to true when null is passed', () => {
    const state = {
      error: false
    }

    userMod.mutations.IS_SIGNUP(state, null)
    expect(state.error).toBeTruthy()
  })

  it('mutation IS_SIGNUP change error to false when null is User', () => {
    const state = {
      error: true,
    }
    const user = new User()
    user.email = 'test@email.com'
    user.token = 'test token'

    userMod.mutations.IS_SIGNUP(state, user)
    expect(state.error).toBeFalsy()
  })

  it('get a user state', () => {
    const user = new User()
    user.email = 'test@email.com'
    user.token = 'test token'

    const state = {
      token: null,
      user
    }

    userMod.state = state
    const actual = userMod.state.user
    expect(actual).toBe(user)

  })

  it('action sign up works', async () =>{
    let url = ''
    let body = {}
    const myAxios: jest.Mocked<any> = axios as any;
    myAxios.post.mockImplementation(
      (_url: string, _body: string) => { 
        return new Promise((resolve) => {
          url = _url
          body = _body
          resolve(true)
        })
      }
    )
    const commit = jest.fn()
    const user = new User()
    user.email = 'test@email.com'
    user.token = 'test_token'

    await userMod.actions.SIGN_UP({commit}, user)
    

    expect(url).toBe("/api/authenticate")
    await expect(commit).toHaveBeenCalledWith(
      "IS_SIGNUP", user)

    await expect(commit).toHaveBeenCalledWith(
      "SET_USER", user)
  
    expect(userMod.state.error).toBe(false)
  
  })

})


describe('get user', () => {
  const localVue = createLocalVue()
  localVue.use(Vuex)


  it('renders a username using a real Vuex store', () => {
    const user = new User()
    user.email = 'vuex-email'
    userMod.SET_USER(user)
    const wrapper = mount(Header,{
      stubs: {
        RouterLink: RouterLinkStub
      },

    }
      )

    expect(wrapper.find('p').text()).toBe('Hi! vuex-email')
  })

})