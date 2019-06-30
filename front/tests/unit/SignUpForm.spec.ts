import {shallowMount, mount, RouterLinkStub, createLocalVue } from '@vue/test-utils'
import SignUpForm from '@/components/SignUpForm.vue'

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