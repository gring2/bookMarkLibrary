import User from '@/vo/User'
interface State {
  token: string | null,
  user: User | null
}
const state: State =  {
  token: null,
  user: null
}

const getters = {

}

const actions = {

}

const mutations = {
  // tslint:disable-next-line:no-shadowed-variable
  SET_USER(state: State, { user }: {[key: string]: User}) {
    state.token = user.token
    state.user = user
  }

}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}