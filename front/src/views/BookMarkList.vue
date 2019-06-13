<template>
  <section class="content">
    <div>
      <TagsPanel></TagsPanel>
      <BookmarksPanel></BookmarksPanel>
    </div>

  </section>
</template>

<script lang="ts">
  import { Component, Prop, Vue } from 'vue-property-decorator'
  import TagsPanel from '@/views/TagsPanel.vue'
  import BookmarksPanel from '@/views/BookmarksPanel.vue'

  @Component({
    components: {
      TagsPanel,
      BookmarksPanel
    },
  })
  export default class BookMarkList extends Vue {
  }
</script>

<!--<style scoped lang="scss">-->
<!--  @import "@/styles/header.scss"-->
<!--</style>-->

<style scoped lang="scss">
  @import "@/styles/library/urls.scss";
</style>