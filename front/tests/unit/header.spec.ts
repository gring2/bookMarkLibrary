import {shallowMount, mount, RouterLinkStub } from '@vue/test-utils'
import Header from '@/views/Header.vue'

describe('Header.vue', () => {
  it('renders default props.email', () => {
    const defaultEmail = 'email'
    const wrapper = shallowMount(Header, {
      stubs: {
        RouterLink: RouterLinkStub
      }
    })
    expect(wrapper.text()).toMatch(defaultEmail)
  })

  it('render props.email when passed', () => {
    const email = 'test email'
    const wrapper = shallowMount(Header, {
      propsData: {
        email
      },
      stubs: {
        RouterLink: RouterLinkStub
      },
      methods: {
        calculateisMobile: () => {

        }
      }


    })
    expect(wrapper.text()).toMatch(email)

  })

  it('do not render sign in button when user is not null', () => {
    const wrapper = mount(Header, {
      propsData: {
        user: {}
      },
      stubs: {
        RouterLink: RouterLinkStub
      },
      methods: {
        calculateisMobile: () => {

        }
      }
    })
    expect(wrapper.find('.login').exists()).toBeFalsy()
  })

  it('render sign in button when user is  null', () => {
    const wrapper = mount(Header, {
      stubs: {
        RouterLink: RouterLinkStub
      },
      methods: {
        calculateisMobile: () => {

        }
      }
    })
    expect(wrapper.find('.login').exists()).toBeTruthy()

  })

  it('no render sign if isMobile is true', () => {
    const wrapper = mount(Header, {
      stubs: {
        RouterLink: RouterLinkStub
      },
      methods: {
        calculateisMobile: () => {
        }
      },
      data:() => {
        return { isMobile: true}
      }
    })

    console.log(wrapper.html())

    expect(wrapper.find('.login').exists()).toBeFalsy()

  })
})
