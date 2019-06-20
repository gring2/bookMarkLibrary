import { Module, VuexModule, Mutation, getModule } from 'vuex-module-decorators'
import store from '@/stores'

import User from '@/vo/User'
export interface IUserState {
  token: string | null,
  user: User | null
}
@Module({dynamic: true, store, name:'userMod'})
export default class UserModule extends VuexModule implements IUserState {
  token: string | null = null;
  user: User | null = null;

  @Mutation
  public SET_USER(user: User) {
    this.token = user.token
    this.user = user
  }

}
export const userMod = getModule(UserModule)