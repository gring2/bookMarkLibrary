<template>
    <div :class="$style.container">
      <ul v-if="!isLoading">
        <li v-for="bookmark in bookmarks">
          <BookMark :bookmark="bookmark" ></BookMark>
        </li>
      </ul>
      <Loading v-else>

      </Loading>


    </div>
</template>

<script lang=ts>
  import { Component, Vue } from 'vue-property-decorator'
  import BookMark from '@/components/BookMark.vue'
  import Loading from '@/views/Loading.vue'

  import BookMarkModel from '@/vo/BookMark'
  import {bookmarkMod} from '@/stores/modules/bookmark'

  @Component({
    components: {
      BookMark, Loading
    }
  })
  export default class BookmarkList extends Vue {
    get bookmarks (): BookMarkModel[]  {
      return bookmarkMod.bookmarks
    }

    get isLoading (): boolean {
      return bookmarkMod.loading
    }

  }

</script>

<style module lang="scss">
  @import "@/styles/mixins.scss";
  .container {
    margin-top: 2rem;
    border-top: 1px solid #e4e6e8;
  ul{
    padding: 0;
    list-style-type: none;
    width: 100%;
    height: 100%;
    align-items: center;

    @include flex;

    flex-wrap: wrap;
    -webkit-flex-flow: row wrap;
    justify-content: left;
      li{
        display: block;
        margin-bottom: 2rem;
        padding: 1rem;
      }
  }
  }
</style>
