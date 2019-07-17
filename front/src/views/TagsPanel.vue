<template>
    <aside class="side">
      <ul v-for="tag in tags">
        <TagLink :tag="tag"></TagLink>
      </ul>
    </aside>
</template>

<script lang="ts">
import { Component , Vue } from 'vue-property-decorator'
import TagLink from '@/components/TagLink.vue'
import Tag from '@/vo/Tag'
import {bookmarkMod} from '@/stores/modules/bookmark'


@Component({
  components: {
    TagLink,
  },
})
export default class TagsPanel extends Vue {
  private tags?: Tag[] = []
  private created() {
    this.tags = bookmarkMod.tags
  }
}
</script>

<style scoped lang="scss">
  aside{
    width: 25%
  }
</style>
