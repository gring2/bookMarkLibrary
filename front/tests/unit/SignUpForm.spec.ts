import {shallowMount} from '@vue/test-utils'
import SignUpForm from '@/components/SignUpForm.vue'
import { userMod } from '@/stores/modules/user'
import User from '@/vo/User'
jest.mock('@/stores/modules/user', () => {
  return {
    __esModule: true, // this property makes it work
    userMod: {SIGN_UP :jest.fn()},
  }
})
beforeEach(() => {
  (userMod.SIGN_UP as any).mockClear()
})

describe('SignUp Form Element test', () => {
  it('setData method change data If property exists', () => {
    const wrapper = shallowMount(SignUpForm)
    const vm: any = wrapper.vm
    vm.setData('email', 'testEmail')
    expect(vm.email).toBe('testEmail')

    vm.setData('password', 'testpassword')
    expect(vm.password).toBe('testpassword')

    vm.setData('passwordConfirm', 'testconfirm')
    expect(vm.passwordConfirm).toBe('testconfirm')

  })
})

describe('store integration test', () => {

  it('call SIGN_UP action', () => {

    const wrapper: any = shallowMount(SignUpForm, {
      data : () => ({
        email: 'testEmail@email.com',
        password: 'testPW',
        passwordConfirm: 'testPWC'
      })
    })
    wrapper.vm.signup()

    const user = new User('testEmail@email.com', 'testPW', 'testPWC')

    expect(userMod.SIGN_UP).toHaveBeenCalledTimes(1)
    expect(userMod.SIGN_UP).toBeCalledWith(user)
  })
})