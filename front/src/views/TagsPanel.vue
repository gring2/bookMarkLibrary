<template>
  <div>
    <aside class="side">
      <ul v-for="tag in tags">
        <Tag :tag="tag"></Tag>
      </ul>
    </aside>

  </div>
</template>

<script lang="ts">
import { Component , Vue } from 'vue-property-decorator'
import Tag from '@/components/Tag.vue'
@Component({
  components: {
    Tag,
  },
})
export default class TagsPanel extends Vue {
  private tags?: string[] = []
  private created() {
    this.tags = ['test1', 'test2']
  }
}
</script>

<style scoped lang="scss">
  aside{
    width: 25%
  }
</style>