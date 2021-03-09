<template>
  <div>
    <img :src="bookmark.img" alt="">
    <a :href="bookmark.url">{{bookmark.name}}</a>
  </div>
</template>

<script lang="ts">
  import {Component, Vue, Prop} from 'vue-property-decorator'
  import BookMarkModel from '@/vo/BookMark'

  @Component({

  })
  export default class BookMark extends Vue {
    @Prop({default: () =>  new BookMarkModel('', '' ,'')}) private bookmark!: BookMarkModel

    private search() {
      console.log('search')
    }
  }
</script>

<style scoped lang="scss">
  $defaultImgSize : 7rem;
  div{
    width: $defaultImgSize;
    height: $defaultImgSize;
    img{
      width: inherit;
      height: $defaultImgSize - 1rem;
    }
    a{
      font-size: 1rem;
    }
  }

</style>
