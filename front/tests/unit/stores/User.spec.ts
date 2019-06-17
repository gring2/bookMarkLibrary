import User from '@/vo/User'
import userStore from '@/stores/modules/user'
describe('SET USER', () => {

  it('adds a user to the state', () => {
    const user = new User()
    user.email = 'test@email.com'
    user.token = 'test token'
    const state = {
      token: null,
      user: null
    }
    userStore.mutations.SET_USER(state, { user })

    expect(state).toEqual({
      token: 'test token',
      user
    })
  })

  it('get a user state', () => {
    fail('no implemented')
  })
})