import Vue from 'vue'
import Vuex from 'vuex'
import {IUserState} from './modules/user'
Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'
// const modules = {
//   user: UserModule
// }
export interface IRootState {
  user: IUserState
}

const store = new Vuex.Store<IRootState>({
  strict: debug,
})

export default store

