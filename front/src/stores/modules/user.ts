import {Action, getModule, Module, Mutation, VuexModule} from 'vuex-module-decorators'
import axios from 'axios'
import store from '@/stores'

import router from '@/router'
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
      this.user = user
  }


  @Mutation
  public AUTHENTICATE(token: Auth_Token) {
    if (token.isvalid()) {
      this.error = false
      this.token = token.token

      router.push({name: 'home'})
    } else {
      this.error = true
    }
  }

 @Action({commit: 'AUTHENTICATE'})
  public  async SIGN_UP(user: User) {
    try {
      const resp = await axios.post('/api/register',
        user
      )
      const authdData = resp.data.response.user

      const token = new Auth_Token(authdData.authentication_token)

      if (token.isvalid()) {
        this.context.dispatch('GET_USER', token)
      }
      return token

    } catch {
      return null

    }
  }

  @Action({commit: 'AUTHENTICATE'})
  public async SIGN_IN(user: User) {
    try {
      const resp = await axios.post('/api/login',
        user
      )
      const authdData = resp.data.response.user
      // mock
      // const resp = {data : {token : 'token'}}
      const token = new Auth_Token(authdData.authentication_token)

      if (token.isvalid()) {
        this.context.dispatch('GET_USER', token)
      }
      return token

    } catch (e){
      return null

    }
  }

  @Action
  public async LOG_OUT() {
    const resp = await axios.post('/api/logout', {
      token : this.token
    })
    //mock data
//    const resp = {status: 200}
    if (resp.status === 200) {
      this.context.commit('expire')
    }

    router.push({name: 'home'})
  }

  @Action({commit: 'SET_USER'})
  public async GET_USER(token: Auth_Token) {
      const headers = {
                        'Authentication-Token': token.token
                        }
    const resp = await axios.get('/api/current/', {headers})
    const data = resp.data
    return new User(data.email);
  }

  @Mutation
  private expire() {
    this.token = null
    this.user = null
  }

}
export const userMod = getModule(UserModule)
