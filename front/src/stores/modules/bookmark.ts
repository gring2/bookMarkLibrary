import {Action, getModule, Module, Mutation, VuexModule} from 'vuex-module-decorators'
import axios from 'axios'
import store from '@/stores'
import {userMod} from './user'
import BookMark from '@/vo/BookMark'
import Tag from "@/vo/Tag";

const api = '/api/library/urls'

export interface IUserState {
  bookmarks: BookMark[]
}


@Module({dynamic: true, store, namespaced: true, name:'bookmarkMod'})
export default class BookMarkModule extends VuexModule implements IUserState {
  public bookmarks: BookMark[] = []
  public tags: Tag[] = []


  @Mutation
  SET_BOOKMARKS(bookmarks: BookMark[]){
    this.bookmarks = bookmarks
  }

  @Mutation
  SET_TAGS(tags: Tag[]){
    this.tags = tags
  }

  @Action
  public async GET_BOOKMARKS(tags: string[] | null= null){
    const data:{[key: string]: any} = {}

    data['headers'] = userMod.authTokenHeader
    if(tags){
      data['params'] = {'q': tags}

    }
    try {
      const resp = await axios.get(api, data)
      this.context.commit('SET_BOOKMARKS', resp.data['bookmarks'])
      this.context.commit('SET_TAGS', resp.data['tags'])

    }catch (e) {

    }
  }

  @Action
  public async POST_BOOKMARK(data: {'url': string, 'tags'?: string}) {
    try{
      await axios.post(api, data, {headers: userMod.authTokenHeader})
      this.context.dispatch('GET_BOOKMARKS')

    }catch (e) {

    }
  }
}
export const bookmarkMod = getModule(BookMarkModule)
