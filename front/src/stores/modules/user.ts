import { Module, VuexModule, Mutation, getModule, Action } from 'vuex-module-decorators'
import axios from 'axios'
import store from '@/stores'

import User from '@/vo/User'
import Auth_Token from '@/vo/Auth_Token'

export interface IUserState {
  token: string | null,
  user: User | null
}


@Module({dynamic: true, store, name:'userMod',})
export default class UserModule extends VuexModule implements IUserState {
  public token: string | null = null
  public user: User | null = null
  private error: boolean = false

  @Mutation
  public SET_USER(user: User) {
      this.token = user.token
      this.user = user
  }

  @Mutation
  public IS_SIGNUP(user: User | null) {
    if (user instanceof User) {
      this.error = false

    } else {
      this.error = true
    }
  }

  @Mutation
  public IS_SIGNIN(token: Auth_Token) {
    if (token.isvalid()) {
      this.error = false

    } else {
      this.error = true
    }
  }

 @Action({commit: 'IS_SIGNUP'})
  public  async SIGN_UP(user: User) {
    try {
      await axios.post('/api/signup', {
        user
      })
      this.context.commit('SET_USER', user)
      return user

    } catch {
      return null

    }
  }

  @Action({commit: 'IS_SIGNIN'})
  public  async SIGN_IN(user: User) {
    try {
      const resp = await axios.post('/api/signin', {
        user
      })
      // mock
      // const resp = {data : {token : 'token'}}
      const token = new Auth_Token(resp.data.token)

      if(token.isvalid()) {
        this.context.commit('SET_USER', user)
      }
      console.log('token')
      return token

    } catch {
      return null

    }
  }

}
export const userMod = getModule(UserModule)