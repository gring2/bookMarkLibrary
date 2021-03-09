<template>
  <span @click="search">{{tag.tag}}</span>
</template>

<script lang="ts">
  import {Component, Vue, Prop} from 'vue-property-decorator'
  import Tag from "@/vo/Tag";

  @Component({

  })
  export default class TagLink extends Vue {
    @Prop() private tag!: Tag

    private search() {
      console.log('search')
    }
  }
</script>

<style scoped lang="scss">
  span{
    cursor: pointer;
    &:hover{
      color: blue;
    }
  }

</style>
