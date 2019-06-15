<template>
    <div :class="$style.container">
      <ul v-for="bookmark in bookmarks">
        <li>
          <BookMark :bookmark="bookmark" ></BookMark>
        </li>
      </ul>

    </div>
</template>

<script lang=ts>
  import { Component, Vue } from 'vue-property-decorator'
  import BookMark from '@/components/BookMark.vue'
  import BookMarkModel from '@/vo/BookMark'

  @Component({
    components: {
      BookMark
    }
  })
  export default class BookmarkList extends Vue {
    private bookmarks: BookMarkModel[] = [new BookMarkModel('title', '#', 'https://cdn.qiita.com/assets/qiita-fb-2887e7b4aad86fd8c25cea84846f2236.png')]
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
    justify-content: space-between;
  li{
    display: block;
    margin-bottom: 2rem;
  }
  }
  }
</style>