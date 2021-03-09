import {createLocalVue, mount, RouterLinkStub} from '@vue/test-utils'
import { VuexModule } from 'vuex-module-decorators'
import Vuex from 'vuex'
import User from '@/vo/User'
import Auth_Token from '@/vo/Auth_Token'
import UserModule, { userMod } from '@/stores/modules/user'
import Header from '@/views/Header.vue'

import axios from 'axios'
jest.mock('axios')

describe('mutation test', () => {
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

  it('SET_USER adds a user to the state', () => {
    const user = new User('test@email.com')

    const state = {
      token: null,
      user: null
    }

    userModObj.mutations.SET_USER(state, user)
    expect(state.user).toEqual(
        user
    )

  })

  it('AUTHENTICATE change error to true when null is passed', () => {
    const state = {
      error: false,
      token: null
    }
    const token = new Auth_Token(null)

    userModObj.mutations.AUTHENTICATE(state, token)
    expect(state.error).toBeTruthy()
    expect(state.token).toBeNull()
  })

  it('AUTHENTICATE change error to false when null is User', () => {
    const state = {
      error: true,
      token: null
    }
    const token = new Auth_Token('test@email.com')

    userModObj.mutations.AUTHENTICATE(state, token)
    expect(state.error).toBeFalsy()
    expect(state.token).toBe('test@email.com')

  })

  it('AUTHENTICATE set token cookies', () => {
    fail()
  })

  it('expire delete token cookies', () => {
    fail()
  })

})

describe('state test', () => {
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

  it('get a user state', () => {
    const user = new User('test@email.com')
    user.token = 'test token'

    userModObj.state = {
      token: null,
      user
    }

    const actual = userModObj.state.user
    expect(actual).toBe(user)

  })
})

describe('action test', () => {
  let userModObj: any

  beforeEach(() => {
    UserModule.mutations!.GET_USER = jest.fn()
    userModObj = new VuexModule({
      state: UserModule.state,
      mutations: UserModule.mutations,
      getters: UserModule.getters,
      actions: UserModule.actions
    })
    const localVue = createLocalVue()
    localVue.use(Vuex)
  })


  it('sign up works', async () => {
    let url = ''
    let body = {}
    const authentication_token = 'mocktoken'
    const id = 1
    const response = {
      user : {
        authentication_token,
        id
      }
    }

    const myAxios: jest.Mocked<any> = axios as any
    myAxios.post.mockImplementation(
      (_url: string, _body: string) => {
        return new Promise((resolve) => {
          url = _url
          body = _body
          resolve({data: {response}})
        })
      }
    )
    const commit = jest.fn()
    const dispatch = jest.fn()

    const user = new User('test@email.com')

    await userModObj.actions.SIGN_UP({commit, dispatch}, user)

    expect(url).toBe('/api/register')

    await expect(commit).toHaveBeenCalledWith('AUTHENTICATE', new Auth_Token(authentication_token))

    await expect(dispatch).toHaveBeenCalledWith('GET_USER', new Auth_Token(authentication_token))

    expect(userModObj.state.error).toBe(false)

  })

  it('sign up commit AUTHENTICATE with NULL IF response is error', async () => {
    let url = ''

    const myAxios: jest.Mocked<any> = axios as any
    myAxios.post.mockImplementation(
      (_url: string, _body: string) => {
        return new Promise((resolve, reject) => {
          url = _url

          reject()
        })
      }
    )

    const commit = jest.fn()
    const dispatch = jest.fn()

    const user = new User('test@email.com')

    await userModObj.actions.SIGN_UP({commit, dispatch}, user)

    expect(url).toBe('/api/register')
    await expect(commit).toHaveBeenCalledTimes(1)

    await expect(commit).toHaveBeenCalledWith('AUTHENTICATE', null)

  })

  it('sign in works', async () => {
    let url = ''
    let body = {}
    const myAxios: jest.Mocked<any> = axios as any
    const authentication_token = 'mocktoken'
    const id = 1
    const response = {
      user : {
        authentication_token,
        id
      }
    }

    myAxios.post.mockImplementation(
      (_url: string, _body: string) => {
        return new Promise((resolve) => {
          url = _url
          body = _body
          resolve({data: {response}})
        })
      }
    )
    const dispatch = jest.fn()
    const commit = jest.fn()

    const user = new User('test@email.com')
    await userModObj.actions.SIGN_IN({commit, dispatch}, user)

    expect(url).toBe('/api/login')
    await expect(dispatch).toHaveBeenCalledWith('GET_USER', new Auth_Token(authentication_token))

    await expect(commit).toHaveBeenCalledWith('AUTHENTICATE', new Auth_Token(authentication_token))


    expect(userModObj.state.error).toBe(false)

  })

  it('sign in commit AUTHENTICATE with NULL IF response is error', async () => {
    let url = ''
    const myAxios: jest.Mocked<any> = axios as any

    myAxios.post.mockImplementation(
      (_url: string, _body: string) => {
        return new Promise((resolve ,reject) => {
          url = _url
          reject()
        })
      }
    )
    const dispatch = jest.fn()
    const commit = jest.fn()

    const user = new User('test@email.com')
    await userModObj.actions.SIGN_IN({commit, dispatch}, user)

    expect(url).toBe('/api/login')

    await expect(commit).toHaveBeenCalledTimes(1)

    await expect(commit).toHaveBeenCalledWith('AUTHENTICATE', null)

  })

  it('log out works', async () => {
    let url = ''
    let body = {}
    const myAxios: jest.Mocked<any> = axios as any
    const token = 'mocktoken'

    myAxios.post.mockImplementation(
        (_url: string, _body: string) => {
          return new Promise((resolve) => {
            url = _url
            body = _body
            resolve({status: 200})
          })
        }
    )

    const commit = jest.fn()
    await userModObj.actions.LOG_OUT({commit})

    expect(url).toBe('/api/logout')
    await expect(commit).toBeCalledWith('expire')

  })

  it('GET_USER commit SET_USER', async () => {
    let url = ''
    const myAxios: jest.Mocked<any> = axios as any
    const id = 1
    const user = new User('test@email.com')

    myAxios.get.mockImplementation(
        (_url: string) => {
          return new Promise((resolve) => {
            url = _url
            resolve({status: 200, data: user})
          })
        }
    )

    const commit = jest.fn()
    await userModObj.actions.GET_USER({commit}, id)

    expect(url).toBe('/api/current/')
    await expect(commit).toBeCalledWith('SET_USER', user)

  })

})


describe('integrate to component', () => {
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
