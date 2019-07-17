import { VuexModule } from 'vuex-module-decorators';
import { createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex'
import BookMark from "@/vo/BookMark";
import BookMarkModule, { bookmarkMod } from '@/stores/modules/bookmark'
import UserModule, { userMod } from '@/stores/modules/user'
import axios from 'axios'
import Tag from "@/vo/Tag";
jest.mock('axios')

jest.mock('@/stores/modules/user', () => {
  return {
    __esModule: true, // this property makes it work
    userMod: {authTokenHeader : {
      'Authentication-Token': 'mock-token'
    }},
  }
})


describe('mutation test', () => {
  let bookmarkModObj: any

  beforeEach(() => {
    bookmarkModObj = new VuexModule({
      state: BookMarkModule.state,
      mutations: BookMarkModule.mutations,
      getters: BookMarkModule.getters,
      actions: BookMarkModule.actions
    })
    const localVue = createLocalVue()
    localVue.use(Vuex)
  })

  it('SET bookmarks to state', () => {
    const bookmark1 = new BookMark('test1', 'testUrl1', 'testThumbnail1')
    const bookmark2 = new BookMark('test2', 'testUrl2', 'testThumbnail2')
    const bookmarks: BookMark[] = [bookmark1, bookmark2]

    const state = {
      bookmarks: []
    }

    bookmarkModObj.mutations.SET_BOOKMARKS(state, bookmarks)
    expect(state.bookmarks).toEqual(
      bookmarks
    )
  })
})

describe('state test', () => {
  let bookmarkModObj: any

  beforeEach(() => {
    bookmarkModObj = new VuexModule({
      state: BookMarkModule.state,
      mutations: BookMarkModule.mutations,
      getters: BookMarkModule.getters,
      actions: BookMarkModule.actions
    })
    const localVue = createLocalVue()
    localVue.use(Vuex)
  })

  it('get bookmark lists', () => {
    const bookmark1 = new BookMark('test1', 'testUrl1', 'testThumbnail1')
    const bookmark2 = new BookMark('test2', 'testUrl2', 'testThumbnail2')
    const bookmarks: BookMark[] = [bookmark1, bookmark2]

    const state = {
      bookmarks
    }

    bookmarkModObj.state = state
    const actual = bookmarkModObj.state.bookmarks
    expect(actual).toBe(bookmarks)
  })
})

describe('action test', () => {
  let bookmarkModObj: any
  let bookmarks: BookMark[]
  let tags: Tag[]
  let myAxios: jest.Mocked<any>
  let url: string;
  let body;
  let params: {}
  let headers: {}

  beforeEach(() => {
    bookmarkModObj = new VuexModule({
      state: BookMarkModule.state,
      mutations: BookMarkModule.mutations,
      getters: BookMarkModule.getters,
      actions: BookMarkModule.actions
    })
    const localVue = createLocalVue()
    localVue.use(Vuex)
    const bookmark1 = new BookMark('test1', 'testUrl1', 'testThumbnail1')
    const bookmark2 = new BookMark('test2', 'testUrl2', 'testThumbnail2')
    const tag1 = new Tag(1, 'test1')
    const tag2 = new Tag(2, 'test2')

    bookmarks = [bookmark1, bookmark2]
    tags = [tag1, tag2]
    url = ''

    myAxios = axios as any

    myAxios.post.mockImplementation(
      (_url: string, _body: string, _headers:{}) => {
        return new Promise((resolve) => {
          url = _url
          body = _body
          headers = _headers
          resolve({data: {bookmarks}})
        })
      }
    )

    myAxios.get.mockImplementation(
      (_url: string, _config: {}) => {
        return new Promise((resolve) => {
          url = _url
          headers = _config
          console.log(_config)
          resolve({data: {bookmarks, tags}})
        })
      }
    )

  })

  it('get bookmarks', async () => {
    const commit = jest.fn()
    const dispatch = jest.fn()
    await bookmarkModObj.actions.GET_BOOKMARKS({commit, dispatch})

    expect(url).toBe('/api/library/urls')
    await expect(commit).toHaveBeenCalledWith(
      'SET_BOOKMARKS', bookmarks)

    expect(headers).toEqual({headers:
      {
        'Authentication-Token': 'mock-token'
      }
    })
  })

   it('get bookmarks using tags', async () => {
    const commit = jest.fn()
    const dispatch = jest.fn()
    await bookmarkModObj.actions.GET_BOOKMARKS({commit, dispatch}, ['first', 'second'])
    expect(headers).toEqual({headers:
      {
        'Authentication-Token': 'mock-token'
      },
      params: {
        q: ['first', 'second']
      }
    })

    await expect(commit).toHaveBeenCalledWith(
      'SET_BOOKMARKS', bookmarks )
    await expect(commit).toHaveBeenCalledWith(
      'SET_TAGS', tags )

   })

})

describe('integrate test', () => {
  it('render bookmark state', () => {
    fail('need to be implemented')
  })
})
