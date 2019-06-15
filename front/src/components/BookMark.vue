<template>
  <div>
    <img src="bookmark.src" alt="">
    <a href="bookmark.url">bookmark.title</a>
  </div>
</template>

<script lang="ts">
  import {Component, Vue, Prop} from 'vue-property-decorator'

  @Component({

  })
  export default class BookMark extends Vue {
    @Prop({default: () => Object.create({src: null, url: null, title: null})}) private bookmark!: object

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