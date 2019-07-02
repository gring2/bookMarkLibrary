import {shallowMount } from '@vue/test-utils'
import SignInForm from '@/components/SignInForm.vue'
import { userMod } from '@/stores/modules/user'
import User from '@/vo/User'
jest.mock('@/stores/modules/user', () => {
  return {
    __esModule: true, // this property makes it work
    userMod: {SIGN_IN :jest.fn()},
  }
})
beforeEach(() => {
  (userMod.SIGN_IN as any).mockClear()
})

describe('SignIn Form Element test', () => {
  it('setData method change data If property exists', () => {
    const wrapper = shallowMount(SignInForm)
    const vm: any = wrapper.vm
    vm.setData('email', 'testEmail')
    expect(vm.email).toBe('testEmail')

    vm.setData('password', 'testpassword')
    expect(vm.password).toBe('testpassword')
  })
})

describe('store integration test', () => {
  it('call SIGN_UP action', () => {

    const wrapper: any = shallowMount(SignInForm, {
      data : () => ({
        email: 'testEmail@email.com',
        password: 'testPW',
      })
    })
    wrapper.vm.signin()

    const user = new User('testEmail@email.com', 'testPW')

    expect(userMod.SIGN_IN).toHaveBeenCalledTimes(1)
    expect(userMod.SIGN_IN).toBeCalledWith(user)
  })
})