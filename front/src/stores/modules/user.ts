import { Module, VuexModule, Mutation, getModule, Action } from 'vuex-module-decorators'
import axios from 'axios'
import store from '@/stores'

import User from '@/vo/User'
export interface IUserState {
  token: string | null,
  user: User | null
}
@Module({dynamic: true, store, name:'userMod',})
export default class UserModule extends VuexModule implements IUserState {
  token: string | null = null;
  user: User | null = null;
  error: boolean = false;

  @Mutation
  public SET_USER(user: User) {
      this.token = user.token
      this.user = user  
  }

  @Mutation
  public IS_SIGNUP(user: User | null) {
    if (user instanceof User){
      this.error = false

    }else{
      this.error = true
    }
  }

 @Action({commit: 'IS_SIGNUP'})
  public  async SIGN_UP(user: User){
    try{
      await axios.post("/api/authenticate", {
        user
      })
      this.context.commit('SET_USER', user)
      return user
  
    }catch{
      return null
      
    }
  }
}
export const userMod = getModule(UserModule)