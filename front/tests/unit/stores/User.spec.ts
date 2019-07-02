import {createLocalVue, mount, RouterLinkStub} from '@vue/test-utils'
import { VuexModule } from 'vuex-module-decorators'
import Vuex from 'vuex'
import User from '@/vo/User'
import Auth_Token from '@/vo/Auth_Token'
import UserModule, { userMod } from '@/stores/modules/user'
import Header from '@/views/Header.vue'

import axios from 'axios'
jest.mock('axios')


describe('SET USER', () => {
  let userModObj: any

  beforeEach(() => {
      userModObj = new VuexModule({
        state: UserModule.state,
        mutations: UserModule.mutations,
        getters: UserModule.getters,
        actions: UserModule.actions
      })
      const localVue = createLocalVue()
      localVue.use(Vuex)
  })

  it('mutation SET_USER adds a user to the state', () => {
    const user = new User('test@email.com')
    user.token = 'test token'

    const state = {
      token: null,
      user: null
    }

    userModObj.mutations.SET_USER(state, user)
    expect(state.user).toEqual(
      user
    )
    expect(state.token).toBe('test token')
  })

  it('mutation IS_SIGNUP change error to true when null is passed', () => {
    const state = {
      error: false
    }

    userModObj.mutations.IS_SIGNUP(state, null)
    expect(state.error).toBeTruthy()
  })

  it('mutation IS_SIGNUP change error to false when null is User', () => {
    const state = {
      error: true,
    }
    const user = new User('test@email.com')
    user.token = 'test token'

    userModObj.mutations.IS_SIGNUP(state, user)
    expect(state.error).toBeFalsy()
  })

  it('mutation IS_SIGNIN change error to true when null is passed', () => {
    const state = {
      error: false
    }

    userModObj.mutations.IS_SIGNIN(state, new Auth_Token(null))
    expect(state.error).toBeTruthy()
  })

  it('mutation IS_SIGNIN change error to false when null is User', () => {
    const state = {
      error: true,
    }
    const token = new Auth_Token('test token')

    userModObj.mutations.IS_SIGNIN(state, token)
    expect(state.error).toBeFalsy()
  })

  it('get a user state', () => {
    const user = new User('test@email.com')
    user.token = 'test token'

    const state = {
      token: null,
      user
    }

    userModObj.state = state
    const actual = userModObj.state.user
    expect(actual).toBe(user)

  })

  it('action sign up works', async () => {
    let url = ''
    let body = {}
    const myAxios: jest.Mocked<any> = axios as any
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
    const user = new User('test@email.com')
    user.token = 'test_token'

    await userModObj.actions.SIGN_UP({commit}, user)

    expect(url).toBe('/api/signup')
    await expect(commit).toHaveBeenCalledWith(
      'IS_SIGNUP', user)

    await expect(commit).toHaveBeenCalledWith(
      'SET_USER', user)

    expect(userModObj.state.error).toBe(false)

  })

  it('action sign in works', async () => {
    let url = ''
    let body = {}
    const myAxios: jest.Mocked<any> = axios as any
    const token = 'mocktoken'

    myAxios.post.mockImplementation(
      (_url: string, _body: string) => {
        return new Promise((resolve) => {
          url = _url
          body = _body
          resolve({data: {token}})
        })
      }
    )
    const commit = jest.fn()
    const user = new User('test@email.com')
    await userModObj.actions.SIGN_IN({commit}, user)


    expect(url).toBe('/api/signin')
    await expect(commit).toHaveBeenCalledWith(
      'IS_SIGNIN', {token})

    await expect(commit).toHaveBeenCalledWith(
      'SET_USER', user)

    expect(userModObj.state.error).toBe(false)

  })

})


describe('get user', () => {
  const localVue = createLocalVue()
  localVue.use(Vuex)


  it('renders a username using a real Vuex store', () => {
    const user = new User('vuex-email')
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