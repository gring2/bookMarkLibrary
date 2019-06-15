<template>
  <main>
    <RegisterBookMark/>
    <BookmarkList/>
  </main>
</template>

<script lang=ts>
  import { Component, Vue } from 'vue-property-decorator'
  import RegisterBookMark from '@/components/RegisterBookMark.vue'
  import BookmarkList from '@/views/BookmarkList.vue'

  @Component({
    components: {
      RegisterBookMark,
      BookmarkList
    }
  })
  export default class BookmarksPanel extends Vue {
  }

</script>

<style scoped lang="scss">
  main {
    width: 70%;
    margin-right: 5%;
  }
</style>