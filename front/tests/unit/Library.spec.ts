import { mount } from '@vue/test-utils'
import Library from '@/views/Library.vue'
import Tag from "@/vo/Tag";
import {bookmarkMod} from "@/stores/modules/bookmark";
import BookMark from "@/vo/BookMark";
import BookmarksPanel from '@/views/BookmarksPanel.vue'
import BookmarkList from '@/views/BookmarkList.vue'

describe('Library.vue', () => {

  it('Tagpanel exists in Library', () => {

    const wrapper = mount(Library, {
    })
    expect(wrapper.find('aside').exists()).toBeTruthy()
  })

  it('BookMarkPanel exits in Library', () => {
    const wrapper = mount(Library, {
    })
    expect(wrapper.find('main').exists()).toBeTruthy()

  })


  it('snapshot Loading component created' , async () => {
    const bookmarkPanelStub = mount(BookmarksPanel, {
      stubs: {
            BookmarkList: mount(BookmarkList, {
              computed: {
                isLoading: ()=> {
                  return true
                }

              }
            }).html()
        }
    })

    const wrapper = mount(Library, {
        stubs: {
            BookmarksPanel: bookmarkPanelStub.html()
        }
    })

    expect(wrapper).toMatchSnapshot()
  })

  it('snapshot BookMarkList is mounted' , async () => {
    const tag1 = new Tag(1, 'test1')
    const tag2 = new Tag(2, 'test2')

    bookmarkMod.SET_TAGS([tag1, tag2])

    const bookmark1 = new BookMark('test1', 'testUrl1', 'testThumbnail1')
    const bookmark2 = new BookMark('test2', 'testUrl2', 'testThumbnail2')

    bookmarkMod.SET_BOOKMARKS([bookmark1, bookmark2])

    const bookmarkPanelStub = mount(BookmarksPanel, {
      stubs: {
            BookmarkList: mount(BookmarkList, {
              computed: {
                isLoading: ()=> {
                  return false
                }

              }
            }).html()
        }
    })

    const wrapper = mount(Library, {
        stubs: {
            BookmarksPanel: bookmarkPanelStub.html()
        }
    })

    expect(wrapper).toMatchSnapshot()
  })

})


