import {Action, getModule, Module, Mutation, VuexModule} from 'vuex-module-decorators'
import axios from 'axios'
import store from '@/stores'
import {userMod} from './user'

import router from '@/router'
import BookMark from '@/vo/BookMark'

export interface IUserState {
  bookmarks: BookMark[]
}


@Module({dynamic: true, store, name:'bookmarkMod',})
export default class BookMarkModule extends VuexModule implements IUserState {
  public bookmarks: BookMark[] = []

  @Mutation
  SET_BOOKMARKS(bookmarks: BookMark[]){
    this.bookmarks = bookmarks
  }

  @Action({commit: 'SET_BOOKMARKS'})
  public async GET_BOOKMARKS(tags: string[] | null= null){
    const data:{[key: string]: any} = {}

    const headers = userMod.authTokenHeader
    data['headers'] = headers
    if(tags){
      data['params'] = {'q': tags}

    }

    const resp = await axios.get('/api/bookmarks', data)
    return resp.data
  }
}
export const bookmarkMod = getModule(BookMarkModule)
