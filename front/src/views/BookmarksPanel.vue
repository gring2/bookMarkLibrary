<template>
  <main>
    <RegisterBookMark/>
    <ul v-for="bookmark in bookmarks">
        <BookMark :bookmark="bookmark"></BookMark>
    </ul>

  </main>
</template>

<script lang=ts>
  import { Component, Vue } from 'vue-property-decorator'
  import RegisterBookMark from '@/components/RegisterBookMark.vue'

  import BookMark from '@/components/BookMark.vue'

  @Component({
    components: {
      RegisterBookMark,
      BookMark
    }
  })
  export default class BookmarksPanel extends Vue {
    private bookmarks: object[] = []
  }

</script>

<style scoped lang="scss">
  main {
    width: 75%;
  ul{
    display: flex;
    align-items: center;
    justify-content: flex-start;
    flex-wrap: wrap;
    list-style-type: none;
    width: 100%;
    height: 100%;
  li{
    display: block;
  //	margin-right: 5%;
    width: 15%;
    height: 10%;
  }
  }
  }
</style>